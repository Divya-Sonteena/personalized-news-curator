import numpy as np
from dataclasses import dataclass
import config

@dataclass
class LinUCBPolicy:
    d: int
    alpha: float = config.LINUCB_ALPHA
    epsilon: float = config.LINUCB_EPSILON

    def __post_init__(self):
        self.A = np.eye(self.d, dtype=np.float64)
        self.b = np.zeros((self.d,), dtype=np.float64)
        self._A_inv = None
        self._dirty = True

    def _ensure_Ainv(self):
        if self._A_inv is None or self._dirty:
            try:
                self._A_inv = np.linalg.inv(self.A)
            except np.linalg.LinAlgError:
                self._A_inv = np.linalg.pinv(self.A)
            self._dirty = False

    def theta(self):
        self._ensure_Ainv()
        return self._A_inv.dot(self.b)

    def score(self, x):
        self._ensure_Ainv()
        theta = self._A_inv.dot(self.b)
        exploit = float(theta.dot(x))
        explore = float(np.sqrt(max(1e-12, x.dot(self._A_inv).dot(x))))
        return exploit + self.alpha * explore, exploit, self.alpha * explore

    def select(self, X):
        # X: n x d
        if X.shape[0] == 0:
            raise ValueError("No candidates")
        if np.random.rand() < self.epsilon:
            return int(np.random.randint(0, X.shape[0]))
        self._ensure_Ainv()
        thetas = self.theta()
        exploits = X.dot(thetas)
        tmp = X.dot(self._A_inv)
        explores = np.sqrt(np.maximum(1e-12, (tmp * X).sum(axis=1)))
        scores = exploits + self.alpha * explores
        return int(np.argmax(scores))

    def update(self, x, reward: float):
        self.A += np.outer(x, x)
        self.b += reward * x
        self._dirty = True

    def to_dict(self):
        return {"d": int(self.d), "alpha": float(self.alpha), "epsilon": float(self.epsilon),
                "A": self.A.tolist(), "b": self.b.tolist()}

    @classmethod
    def from_dict(cls, data):
        p = cls(d=int(data["d"]), alpha=float(data.get("alpha", config.LINUCB_ALPHA)),
                epsilon=float(data.get("epsilon", config.LINUCB_EPSILON)))
        p.A = np.array(data.get("A", np.eye(p.d)), dtype=np.float64)
        p.b = np.array(data.get("b", np.zeros((p.d,))), dtype=np.float64)
        p._dirty = True
        p._A_inv = None
        return p

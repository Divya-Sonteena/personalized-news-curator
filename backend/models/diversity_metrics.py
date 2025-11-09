from collections import Counter
import math

def simpson_index(labels):
    if not labels: return 0.0
    n = len(labels)
    counts = Counter(labels)
    return 1.0 - sum((c/n)**2 for c in counts.values())

def entropy(labels):
    if not labels: return 0.0
    n = len(labels)
    counts = Counter(labels)
    return -sum((c/n)*math.log((c/n)+1e-12) for c in counts.values())

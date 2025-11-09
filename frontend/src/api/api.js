// Minimal API client wrapper
const BACKEND = "http://127.0.0.1:8505";

export function setToken(token, userId) {
  localStorage.setItem("news_rl_token", token);
  localStorage.setItem("news_rl_user", userId);
}

export function getToken() {
  return localStorage.getItem("news_rl_token");
}

export function getUserId() {
  return localStorage.getItem("news_rl_user");
}

export function clearToken() {
  localStorage.removeItem("news_rl_token");
  localStorage.removeItem("news_rl_user");
}

function authHeaders() {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function register(payload) {
  const res = await fetch(`${BACKEND}/api/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function login(payload) {
  const res = await fetch(`${BACKEND}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function recommend(payload) {
  const res = await fetch(`${BACKEND}/api/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function feedback(payload) {
  const res = await fetch(`${BACKEND}/api/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function saveUserConfig(payload) {
  const res = await fetch(`${BACKEND}/api/user/config`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function getLiked(userId) {
  const res = await fetch(`${BACKEND}/api/user/liked?user_id=${encodeURIComponent(userId)}`, {
    headers: { ...authHeaders() },
  });
  return res.json();
}

export async function refreshCatalog() {
  const res = await fetch(`${BACKEND}/api/catalog/refresh`, { method: "POST" });
  return res.json();
}

export async function getArticles() {
  const res = await fetch(`${BACKEND}/api/articles`);
  return res.json();
}

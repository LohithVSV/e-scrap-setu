// js/api.js
// Single place every page calls into. Change the base URL once, everything else just works.

const API_BASE = "http://localhost:8000";

async function request(path, { method = "GET", body = null, auth = true } = {}) {
  const headers = { "Content-Type": "application/json" };

  if (auth) {
    const token = localStorage.getItem("esetu_token");
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Something went wrong" }));
    throw new Error(err.detail || `Request failed: ${res.status}`);
  }

  const text = await res.text();
  return text ? JSON.parse(text) : null;
}

function loginCitizen(phone, password) {
  return request("/auth/citizen/login", { method: "POST", body: { phone, password }, auth: false }).then((res) => {
    localStorage.setItem("esetu_token", res.access_token);
    localStorage.setItem("esetu_user", JSON.stringify(res.user));
    localStorage.setItem("esetu_citizen_id", res.user?.id ?? "");
    localStorage.setItem("esetu_citizen_phone", phone);
    return res;
  });
}

function loginOfficer(employeeId, password) {
  return request("/auth/officer/login", { method: "POST", body: { employee_id: employeeId, password }, auth: false }).then((res) => {
    localStorage.setItem("esetu_token", res.access_token);
    localStorage.setItem("esetu_role", res.role);
    localStorage.setItem("esetu_ward", res.ward || "");
    return res;
  });
}

function signupCitizen(name, phone, password) {
  return request("/auth/citizen/signup", { method: "POST", body: { name, phone, password }, auth: false }).then((res) => {
    localStorage.setItem("esetu_token", res.access_token);
    localStorage.setItem("esetu_user", JSON.stringify(res.user));
    localStorage.setItem("esetu_citizen_id", res.user?.id ?? "");
    localStorage.setItem("esetu_citizen_phone", phone);
    return res;
  });
}

function getDropoffs(ward = null) {
  const query = ward ? `?ward=${ward}` : "";
  return request(`/dropoffs${query}`, { auth: false });
}

function getDropoffByQR(qrCode) {
  return request(`/dropoffs/qr/${qrCode}`, { auth: false });
}

function logCollection(payload) {
  const phone = payload.phone ?? localStorage.getItem("esetu_citizen_phone") ?? null;
  const citizenId = payload.citizen_id ?? Number(localStorage.getItem("esetu_citizen_id")) || null;
  const body = {
    ...payload,
    citizen_id: citizenId,
    phone,
    dropoff_point_id: payload.dropoff_point_id ?? payload.dropoff_id ?? null,
    weight_kg: payload.weight_kg ?? null,
  };

  return request("/collections", { method: "POST", body });
}

function getWardCollections(wardId) {
  return request(`/collections/ward/${wardId}`);
}

function getAllCollections() {
  return request("/collections");
}

function getCitizenCredits(citizenId = null) {
  const id = citizenId ?? localStorage.getItem("esetu_citizen_id");
  const phone = localStorage.getItem("esetu_citizen_phone");

  if (phone) {
    return request(`/rewards/phone/${encodeURIComponent(phone)}`);
  }
  if (!id) return Promise.resolve({ credits: 0, total: 0, redemptions: [] });
  return request(`/rewards/${id}`);
}

function redeemCredits(payload) {
  const phone = payload.phone ?? localStorage.getItem("esetu_citizen_phone") ?? null;
  return request("/rewards/redeem", { method: "POST", body: { ...payload, phone } });
}

function getWardStats(wardId) {
  return request(`/dashboard/ward/${wardId}`);
}

function getThresholdAlerts() {
  return request("/dashboard/alerts");
}

function submitFeedback(collectionId, stars, comment = "") {
  return request("/feedback", { method: "POST", body: { collection_id: collectionId, stars, comment } });
}

function askAssistant(question) {
  return request("/assistant/ask", { method: "POST", body: { question }, auth: false });
}

window.api = {
  loginCitizen,
  loginOfficer,
  signupCitizen,
  getDropoffs,
  getDropoffByQR,
  logCollection,
  getWardCollections,
  getAllCollections,
  getCitizenCredits,
  redeemCredits,
  getWardStats,
  getThresholdAlerts,
  submitFeedback,
};

window.loginCitizen = loginCitizen;
window.loginOfficer = loginOfficer;
window.signupCitizen = signupCitizen;
window.getDropoffs = getDropoffs;
window.getDropoffByQR = getDropoffByQR;
window.logCollection = logCollection;
window.getWardCollections = getWardCollections;
window.getAllCollections = getAllCollections;
window.getCitizenCredits = getCitizenCredits;
window.redeemCredits = redeemCredits;
window.getWardStats = getWardStats;
window.getThresholdAlerts = getThresholdAlerts;
window.submitFeedback = submitFeedback;
window.askAssistant = askAssistant;

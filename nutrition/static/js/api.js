// api.js - Central API client for Django backend
const API_BASE = '/api';

// ── TOKEN HELPERS ──────────────────────────────────────────────────────────────
// The token is stored in localStorage after login and read on every request.
// To log out, call clearToken() and reload.

export function saveToken(token) {
    localStorage.setItem('authToken', token);
}

export function getToken() {
    return localStorage.getItem('authToken');
}

export function clearToken() {
    localStorage.removeItem('authToken');
}

export function isLoggedIn() {
    return !!getToken();
}

// ── CORE REQUEST HELPER ────────────────────────────────────────────────────────
async function apiRequest(endpoint, method = 'GET', data = null) {
    const headers = { 'Content-Type': 'application/json' };

    // Attach token if available (DRF TokenAuthentication format)
    const token = getToken();
    if (token) {
        headers['Authorization'] = `Token ${token}`;
    }

    const options = { method, headers };
    if (data) options.body = JSON.stringify(data);

    const response = await fetch(`${API_BASE}${endpoint}`, options);

    if (!response.ok) {
        let errorMsg = `HTTP ${response.status}`;
        try {
            const errorData = await response.json();
            errorMsg = errorData.message || errorData.error || errorMsg;
        } catch (e) {
            // ignore JSON parse errors
        }
        throw new Error(errorMsg);
    }

    // For 204 No Content
    if (response.status === 204) return { success: true };

    return response.json();
}

// ── AUTHENTICATION ─────────────────────────────────────────────────────────────
// Backend expects { username, password } — NOT email.
// After login/register the response includes a token which we store here.

export const auth = {
    login: (username, password) => apiRequest('/auth/login/', 'POST', { username, password }),
    register: (username, password) => apiRequest('/auth/register/', 'POST', { username, password }),
    getProfile: () => apiRequest('/auth/profile/'),    // used to validate a stored token on page load
    // logout is client-side only: clear the token and reload
    logout: () => { clearToken(); },
};

// ── NUTRITION (Meals & Macros) ─────────────────────────────────────────────────
export const nutrition = {
    getMeals:   (date)    => apiRequest(`/nutrition/meals/${date}/`),
    addMeal:    (meal)    => apiRequest('/nutrition/log-food/', 'POST', meal),
    deleteMeal: (id)      => apiRequest(`/nutrition/meals/${id}/`, 'DELETE'),
    getSummary: (date)    => apiRequest(`/nutrition/dashboard/`),    // current backend endpoint
    getMacros:  ()        => apiRequest('/nutrition/macro/'),
    setMacros:  (targets) => apiRequest('/nutrition/macro/', 'PUT', targets),
};

// ── WORKOUTS & EXERCISES ───────────────────────────────────────────────────────
export const workouts = {
    getLogs:         ()           => apiRequest('/workouts/logs/'),
    addLog:          (log)        => apiRequest('/workouts/logs/', 'POST', log),
    getExercises:    ()           => apiRequest('/workouts/exercises/'),
    getTemplates:    ()           => apiRequest('/workouts/templates/'),
    applyTemplate:   (templateId) => apiRequest(`/workouts/templates/${templateId}/apply/`, 'POST'),
};

// ── PROGRESS (Weight) ──────────────────────────────────────────────────────────
export const progress = {
    getEntries:  ()              => apiRequest('/progress/weight/'),
    addEntry:    (weight, date)  => apiRequest('/progress/weight/', 'POST', { weight, date }),
    deleteEntry: (id)            => apiRequest(`/progress/weight/${id}/`, 'DELETE'),
};

// ── MEDIA (Photos) ─────────────────────────────────────────────────────────────
export const media = {
    getPhotos:   ()         => apiRequest('/media/photos/'),
    deletePhoto: (id)       => apiRequest(`/media/photos/${id}/`, 'DELETE'),
    uploadPhoto: async (formData) => {
        const token = getToken();
        const response = await fetch('/api/media/photos/', {
            method: 'POST',
            headers: token ? { 'Authorization': `Token ${token}` } : {},
            body: formData   // multipart — do NOT set Content-Type manually
        });
        if (!response.ok) throw new Error('Upload failed');
        return response.json();
    },
};

// ── SOCIAL (Friends & Feed) ────────────────────────────────────────────────────
export const social = {
    getFriends:    ()         => apiRequest('/social/friends/'),
    addFriend:     (friendId) => apiRequest('/social/friends/', 'POST', { friend_id: friendId }),
    removeFriend:  (friendId) => apiRequest(`/social/friends/${friendId}/`, 'DELETE'),
    getFeed:       ()         => apiRequest('/social/feed/'),
};
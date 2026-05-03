// auth.js - handles login, signup, session
import { auth, saveToken, clearToken, isLoggedIn } from './api.js';
import { showToast } from './utils.js';
import { initMainApp } from './main.js';

export let currentUser = null;

// Called when the user submits the login form.
// username + password must match what the backend expects.
export async function login(username, password) {
    try {
        const data = await auth.login(username, password);
        if (!data.success) {
            showToast(data.message || 'Login failed.', 'error');
            return;
        }
        saveToken(data.token);          // store token in localStorage
        currentUser = data.user;        // { id, username }
        await initMainApp();
    } catch (err) {
        showToast(err.message, 'error');
    }
}

// Called when the user submits the register form.
export async function register(username, password) {
    try {
        const data = await auth.register(username, password);
        if (!data.success) {
            showToast(data.message || 'Registration failed.', 'error');
            return;
        }
        saveToken(data.token);
        currentUser = data.user;
        await initMainApp();
    } catch (err) {
        showToast(err.message, 'error');
    }
}

// Called on page load to check if a stored token is still valid.
// Hits GET /api/auth/profile/ — if it returns 200 the token works.
export async function checkSession() {
    if (!isLoggedIn()) return false;
    try {
        const profile = await auth.getProfile();
        currentUser = profile;          // { id, username }
        return true;
    } catch {
        // Token is invalid or expired — clean it up
        clearToken();
        return false;
    }
}

// Clears the token locally and reloads the page to show the login screen.
export async function logout() {
    auth.logout();                      // clears localStorage token
    currentUser = null;
    location.reload();
}
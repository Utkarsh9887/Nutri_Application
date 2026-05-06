// main.js - initializes the whole app
import { checkSession, login, logout, register, currentUser } from './auth.js';
import { renderDashboard } from './dashboard.js';
import { renderCalorieTracker, renderMacroTargets } from './meals.js';
import { renderWorkoutPlans } from './workouts.js';
import { renderProgress } from './progress.js';
import { renderPhotos } from './photos.js';
import { renderSocial } from './social.js';
import { renderProfile } from './profile.js';
import { showToast } from './utils.js';

// ── AUTH SCREEN ────────────────────────────────────────────────────────────────
// Renders a login / register card into #authContainer.
// Matches the app's existing dark gradient background and btn-gradient style.

function renderAuth() {
    const container = document.getElementById('authContainer');

    container.innerHTML = `
        <div class="w-full max-w-md">

            <!-- Logo -->
            <div class="flex flex-col items-center mb-8">
                <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center text-white text-2xl shadow-lg mb-4">
                    <i class="fas fa-dumbbell"></i>
                </div>
                <h1 class="text-3xl font-bold text-white">Nutri Ai</h1>
                <p class="text-slate-400 text-sm mt-1">Your smart fitness & nutrition hub</p>
            </div>

            <!-- Card -->
            <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-2xl overflow-hidden">

                <!-- Tab switcher -->
                <div class="flex border-b border-slate-200 dark:border-slate-700">
                    <button
                        id="authTabLogin"
                        class="flex-1 py-4 text-sm font-semibold text-blue-600 border-b-2 border-blue-600 bg-blue-50 dark:bg-slate-700 dark:text-blue-400 transition-all"
                        onclick="switchAuthTab('login')"
                    >
                        <i class="fas fa-sign-in-alt mr-2"></i>Login
                    </button>
                    <button
                        id="authTabRegister"
                        class="flex-1 py-4 text-sm font-semibold text-slate-400 border-b-2 border-transparent hover:text-slate-600 dark:hover:text-slate-200 transition-all"
                        onclick="switchAuthTab('register')"
                    >
                        <i class="fas fa-user-plus mr-2"></i>Register
                    </button>
                </div>

                <!-- Login form -->
                <div id="loginForm" class="p-8 space-y-5">
                    <div>
                        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                            <i class="fas fa-user text-blue-500 mr-1"></i>Username
                        </label>
                        <input
                            id="loginUsername"
                            type="text"
                            placeholder="Enter your username"
                            autocomplete="username"
                            class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-700 text-slate-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                        >
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                            <i class="fas fa-lock text-blue-500 mr-1"></i>Password
                        </label>
                        <div class="relative">
                            <input
                                id="loginPassword"
                                type="password"
                                placeholder="Enter your password"
                                autocomplete="current-password"
                                class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-700 text-slate-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition pr-12"
                            >
                            <button type="button" class="toggle-pw absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600" data-target="loginPassword">
                                <i class="fas fa-eye"></i>
                            </button>
                        </div>
                    </div>
                    <button
                        id="loginBtn"
                        class="w-full btn-gradient py-3 rounded-xl font-semibold text-white flex items-center justify-center gap-2"
                    >
                        <i class="fas fa-sign-in-alt"></i> Login
                    </button>
                    <p class="text-center text-sm text-slate-400">
                        Don't have an account?
                        <button class="text-blue-500 font-semibold hover:underline ml-1" onclick="switchAuthTab('register')">Register here</button>
                    </p>
                </div>

                <!-- Register form -->
                <div id="registerForm" class="p-8 space-y-5 hidden">
                    <div>
                        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                            <i class="fas fa-user text-purple-500 mr-1"></i>Username
                        </label>
                        <input
                            id="registerUsername"
                            type="text"
                            placeholder="Choose a username"
                            autocomplete="username"
                            class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-700 text-slate-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-purple-500 transition"
                        >
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                            <i class="fas fa-lock text-purple-500 mr-1"></i>Password
                        </label>
                        <div class="relative">
                            <input
                                id="registerPassword"
                                type="password"
                                placeholder="At least 6 characters"
                                autocomplete="new-password"
                                class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-700 text-slate-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-purple-500 transition pr-12"
                            >
                            <button type="button" class="toggle-pw absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600" data-target="registerPassword">
                                <i class="fas fa-eye"></i>
                            </button>
                        </div>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                            <i class="fas fa-lock text-purple-500 mr-1"></i>Confirm Password
                        </label>
                        <div class="relative">
                            <input
                                id="registerConfirm"
                                type="password"
                                placeholder="Repeat your password"
                                autocomplete="new-password"
                                class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-700 text-slate-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-purple-500 transition pr-12"
                            >
                            <button type="button" class="toggle-pw absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600" data-target="registerConfirm">
                                <i class="fas fa-eye"></i>
                            </button>
                        </div>
                    </div>
                    <button
                        id="registerBtn"
                        class="w-full btn-gradient py-3 rounded-xl font-semibold text-white flex items-center justify-center gap-2"
                    >
                        <i class="fas fa-user-plus"></i> Create Account
                    </button>
                    <p class="text-center text-sm text-slate-400">
                        Already have an account?
                        <button class="text-blue-500 font-semibold hover:underline ml-1" onclick="switchAuthTab('login')">Login here</button>
                    </p>
                </div>

            </div>

            <!-- Footer note -->
            <p class="text-center text-slate-500 text-xs mt-6">
                Track nutrition • Log workouts • See your progress
            </p>
        </div>
    `;

    // ── Tab switcher (exposed on window so inline onclick can reach it) ──────
    window.switchAuthTab = (tab) => {
        const isLogin = tab === 'login';

        document.getElementById('loginForm').classList.toggle('hidden', !isLogin);
        document.getElementById('registerForm').classList.toggle('hidden', isLogin);

        const loginTab    = document.getElementById('authTabLogin');
        const registerTab = document.getElementById('authTabRegister');

        // Active tab styles
        loginTab.className    = `flex-1 py-4 text-sm font-semibold transition-all border-b-2 ${
            isLogin
                ? 'text-blue-600 border-blue-600 bg-blue-50 dark:bg-slate-700 dark:text-blue-400'
                : 'text-slate-400 border-transparent hover:text-slate-600 dark:hover:text-slate-200'
        }`;
        registerTab.className = `flex-1 py-4 text-sm font-semibold transition-all border-b-2 ${
            !isLogin
                ? 'text-purple-600 border-purple-600 bg-purple-50 dark:bg-slate-700 dark:text-purple-400'
                : 'text-slate-400 border-transparent hover:text-slate-600 dark:hover:text-slate-200'
        }`;

        // Focus the first input of the active form
        const firstInput = isLogin
            ? document.getElementById('loginUsername')
            : document.getElementById('registerUsername');
        setTimeout(() => firstInput.focus(), 50);
    };

    // ── Show / hide password toggles ─────────────────────────────────────────
    container.querySelectorAll('.toggle-pw').forEach(btn => {
        btn.addEventListener('click', () => {
            const input = document.getElementById(btn.dataset.target);
            const isPassword = input.type === 'password';
            input.type = isPassword ? 'text' : 'password';
            btn.querySelector('i').className = isPassword ? 'fas fa-eye-slash' : 'fas fa-eye';
        });
    });

    // ── Enter key submits the visible form ───────────────────────────────────
    container.addEventListener('keydown', (e) => {
        if (e.key !== 'Enter') return;
        const loginHidden = document.getElementById('loginForm').classList.contains('hidden');
        if (!loginHidden) document.getElementById('loginBtn').click();
        else              document.getElementById('registerBtn').click();
    });

    // ── LOGIN handler ─────────────────────────────────────────────────────────
    document.getElementById('loginBtn').addEventListener('click', async () => {
        const btn      = document.getElementById('loginBtn');
        const username = document.getElementById('loginUsername').value.trim();
        const password = document.getElementById('loginPassword').value;

        if (!username || !password) {
            showToast('Please fill in all fields.', 'warning');
            return;
        }

        // Loading state
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Logging in…';

        try {
            await login(username, password);
        } finally {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-sign-in-alt"></i> Login';
        }
    });

    // ── REGISTER handler ──────────────────────────────────────────────────────
    document.getElementById('registerBtn').addEventListener('click', async () => {
        const btn      = document.getElementById('registerBtn');
        const username = document.getElementById('registerUsername').value.trim();
        const password = document.getElementById('registerPassword').value;
        const confirm  = document.getElementById('registerConfirm').value;

        if (!username || !password || !confirm) {
            showToast('Please fill in all fields.', 'warning');
            return;
        }
        if (password.length < 6) {
            showToast('Password must be at least 6 characters.', 'warning');
            return;
        }
        if (password !== confirm) {
            showToast('Passwords do not match.', 'error');
            document.getElementById('registerConfirm').focus();
            return;
        }

        // Loading state
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating account…';

        try {
            await register(username, password);
        } finally {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-user-plus"></i> Create Account';
        }
    });
}

// ── TAB NAVIGATION ─────────────────────────────────────────────────────────────
let activeTab = 'dashboard';

async function switchTab(tabName) {
    activeTab = tabName;
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.add('hidden'));
    document.getElementById(`${tabName}Panel`).classList.remove('hidden');

    if      (tabName === 'dashboard') await renderDashboard();
    else if (tabName === 'calorie')   await renderCalorieTracker();
    else if (tabName === 'macro')     await renderMacroTargets();
    else if (tabName === 'workout')   await renderWorkoutPlans();
    else if (tabName === 'progress')  await renderProgress();
    else if (tabName === 'photos')    await renderPhotos();
    else if (tabName === 'social')    await renderSocial();
    else if (tabName === 'profile')   await renderProfile();
}

// ── MAIN APP INIT ──────────────────────────────────────────────────────────────
export async function initMainApp() {
    document.getElementById('authContainer').classList.add('hidden');
    document.getElementById('mainApp').classList.remove('hidden');

    // Greet by username (currentUser now has { id, username } from the fixed auth)
    document.getElementById('userGreeting').innerHTML = `👋 Hello, ${currentUser.username}`;
    document.getElementById('userGoal').innerHTML = '';   // goal field not in model yet

    // Dark mode
    if (localStorage.getItem('darkMode') === 'true') document.body.classList.add('dark');
    document.getElementById('darkModeToggle').addEventListener('click', () => {
        document.body.classList.toggle('dark');
        localStorage.setItem('darkMode', document.body.classList.contains('dark'));
    });

    // Logout
    document.getElementById('logoutBtn').addEventListener('click', async () => {
        if (confirm('Log out?')) await logout();
    });

    // Tab listeners
    document.querySelectorAll('.nav-tab').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active-tab'));
            btn.classList.add('active-tab');
            switchTab(btn.getAttribute('data-tab'));
        });
    });

    await switchTab('dashboard');
}

// ── BOOTSTRAP ──────────────────────────────────────────────────────────────────
(async function bootstrap() {
    const loggedIn = await checkSession();
    if (loggedIn) {
        await initMainApp();
    } else {
        renderAuth();
    }
})();
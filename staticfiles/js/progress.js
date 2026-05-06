// progress.js - weight tracking: chart, log form, entry history
import { progress as apiProgress } from './api.js';
import { showToast, getLocalDate, destroyChart, chartStore } from './utils.js';

export async function renderProgress() {
    const panel = document.getElementById('progressPanel');
    if (!panel) return;

    // Loading skeleton
    panel.innerHTML = `
        <div class="flex items-center justify-center py-16 text-muted">
            <i class="fas fa-spinner fa-spin mr-2"></i> Loading progress…
        </div>`;

    let entries = [];
    try {
        entries = await apiProgress.getEntries();
    } catch (err) {
        panel.innerHTML = `<div class="bg-red-50 text-red-600 p-6 rounded-xl text-center">
            Failed to load progress data. Please refresh.</div>`;
        return;
    }

    // ── Derived stats ──────────────────────────────────────────────────────────
    const latest     = entries.length ? entries[entries.length - 1].weight : null;
    const first      = entries.length ? entries[0].weight : null;
    const totalChange = (latest !== null && first !== null) ? +(latest - first).toFixed(1) : null;
    const changeLabel = totalChange === null ? '—'
        : totalChange > 0 ? `+${totalChange} kg` : `${totalChange} kg`;
    const changeColor = totalChange === null ? 'text-muted'
        : totalChange <= 0 ? 'text-green-600' : 'text-red-500';

    // 7-day average
    const last7 = entries.slice(-7);
    const avg7  = last7.length
        ? (last7.reduce((s, e) => s + e.weight, 0) / last7.length).toFixed(1)
        : '—';

    panel.innerHTML = `
        <!-- Stat cards -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="bg-surface rounded-xl p-5 border border-border text-center">
                <p class="text-xs text-muted mb-1">Current Weight</p>
                <p class="text-2xl font-bold">${latest !== null ? latest + ' kg' : '—'}</p>
            </div>
            <div class="bg-surface rounded-xl p-5 border border-border text-center">
                <p class="text-xs text-muted mb-1">Starting Weight</p>
                <p class="text-2xl font-bold">${first !== null ? first + ' kg' : '—'}</p>
            </div>
            <div class="bg-surface rounded-xl p-5 border border-border text-center">
                <p class="text-xs text-muted mb-1">Total Change</p>
                <p class="text-2xl font-bold ${changeColor}">${changeLabel}</p>
            </div>
            <div class="bg-surface rounded-xl p-5 border border-border text-center">
                <p class="text-xs text-muted mb-1">7-Day Average</p>
                <p class="text-2xl font-bold">${avg7 !== '—' ? avg7 + ' kg' : '—'}</p>
            </div>
        </div>

        <div class="grid lg:grid-cols-3 gap-6">

            <!-- Chart -->
            <div class="lg:col-span-2 bg-surface rounded-xl p-6 border border-border">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="font-bold text-lg"><i class="fas fa-chart-line text-blue-600 mr-2"></i>Weight Over Time</h3>
                    <div class="flex gap-2">
                        <button class="chart-range-btn px-3 py-1 text-xs rounded-full bg-blue-100 dark:bg-blue-900 text-blue-600 font-semibold" data-range="30">30d</button>
                        <button class="chart-range-btn px-3 py-1 text-xs rounded-full border border-border text-muted" data-range="90">90d</button>
                        <button class="chart-range-btn px-3 py-1 text-xs rounded-full border border-border text-muted" data-range="all">All</button>
                    </div>
                </div>
                ${entries.length < 2
                    ? `<div class="flex flex-col items-center justify-center py-12 text-muted">
                           <i class="fas fa-chart-line text-4xl mb-3 opacity-30"></i>
                           <p>Log at least 2 entries to see your chart.</p>
                       </div>`
                    : `<div class="chart-container"><canvas id="weightChart"></canvas></div>`
                }
            </div>

            <!-- Log form -->
            <div class="bg-surface rounded-xl p-6 border border-border space-y-4">
                <h3 class="font-bold text-lg"><i class="fas fa-plus-circle text-green-600 mr-2"></i>Log Weight</h3>
                <div>
                    <label class="block text-sm font-medium mb-1">Weight (kg)</label>
                    <input
                        id="weightInput"
                        type="number"
                        step="0.1"
                        min="20"
                        max="500"
                        placeholder="e.g. 75.5"
                        class="w-full px-4 py-3 rounded-xl border border-border bg-slate-50 dark:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                </div>
                <div>
                    <label class="block text-sm font-medium mb-1">Date</label>
                    <input
                        id="weightDate"
                        type="date"
                        value="${getLocalDate()}"
                        class="w-full px-4 py-3 rounded-xl border border-border bg-slate-50 dark:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                </div>
                <button id="logWeightBtn" class="w-full btn-gradient py-3 rounded-xl font-semibold flex items-center justify-center gap-2">
                    <i class="fas fa-save"></i> Save Entry
                </button>
                <p class="text-xs text-muted text-center">Logging the same date updates the existing entry.</p>
            </div>
        </div>

        <!-- History table -->
        <div class="bg-surface rounded-xl p-6 border border-border">
            <h3 class="font-bold text-lg mb-4"><i class="fas fa-history text-purple-600 mr-2"></i>Entry History</h3>
            ${entries.length === 0
                ? `<p class="text-muted text-center py-6">No entries yet. Log your first weight above!</p>`
                : `<div class="overflow-x-auto">
                    <table class="w-full text-sm">
                        <thead>
                            <tr class="border-b border-border text-muted text-left">
                                <th class="pb-2 pr-4">Date</th>
                                <th class="pb-2 pr-4">Weight</th>
                                <th class="pb-2 pr-4">Change</th>
                                <th class="pb-2"></th>
                            </tr>
                        </thead>
                        <tbody id="weightHistoryBody">
                            ${buildHistoryRows(entries)}
                        </tbody>
                    </table>
                   </div>`
            }
        </div>
    `;

    // ── Draw chart ─────────────────────────────────────────────────────────────
    if (entries.length >= 2) {
        drawChart(entries, 30);

        document.querySelectorAll('.chart-range-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.chart-range-btn').forEach(b => {
                    b.className = 'chart-range-btn px-3 py-1 text-xs rounded-full border border-border text-muted';
                });
                btn.className = 'chart-range-btn px-3 py-1 text-xs rounded-full bg-blue-100 dark:bg-blue-900 text-blue-600 font-semibold';
                const range = btn.dataset.range === 'all' ? Infinity : parseInt(btn.dataset.range);
                drawChart(entries, range);
            });
        });
    }

    // ── Log weight button ──────────────────────────────────────────────────────
    document.getElementById('logWeightBtn').addEventListener('click', async () => {
        const btn    = document.getElementById('logWeightBtn');
        const weight = parseFloat(document.getElementById('weightInput').value);
        const date   = document.getElementById('weightDate').value;

        if (isNaN(weight) || weight <= 0) {
            showToast('Enter a valid weight.', 'warning');
            return;
        }
        if (!date) {
            showToast('Pick a date.', 'warning');
            return;
        }

        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving…';

        try {
            await apiProgress.addEntry(weight, date);
            showToast('Weight saved!');
            await renderProgress();    // re-render to update chart + stats
        } catch (err) {
            showToast(err.message || 'Failed to save.', 'error');
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-save"></i> Save Entry';
        }
    });

    // ── Delete buttons ─────────────────────────────────────────────────────────
    document.querySelectorAll('.delete-weight-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            if (!confirm('Delete this entry?')) return;
            try {
                await apiProgress.deleteEntry(parseInt(btn.dataset.id));
                showToast('Entry deleted.');
                await renderProgress();
            } catch (err) {
                showToast('Failed to delete.', 'error');
            }
        });
    });
}

// ── Helpers ────────────────────────────────────────────────────────────────────

function buildHistoryRows(entries) {
    // Show newest first in the table
    return [...entries].reverse().map((entry, i, arr) => {
        const prev   = arr[i + 1];   // next in reversed = previous in time
        const diff   = prev ? +(entry.weight - prev.weight).toFixed(1) : null;
        const diffHtml = diff === null ? '<span class="text-muted">—</span>'
            : diff === 0 ? '<span class="text-muted">0.0 kg</span>'
            : diff < 0
                ? `<span class="text-green-600">▼ ${Math.abs(diff)} kg</span>`
                : `<span class="text-red-500">▲ ${diff} kg</span>`;
        return `
            <tr class="border-b border-border hover:bg-slate-50 dark:hover:bg-slate-800">
                <td class="py-2 pr-4">${entry.date}</td>
                <td class="py-2 pr-4 font-semibold">${entry.weight} kg</td>
                <td class="py-2 pr-4">${diffHtml}</td>
                <td class="py-2 text-right">
                    <button class="delete-weight-btn text-red-400 hover:text-red-600 text-xs" data-id="${entry.id}">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>`;
    }).join('');
}

function drawChart(allEntries, rangeDays) {
    destroyChart(chartStore, 'weightChart');

    const cutoff = rangeDays === Infinity ? null : (() => {
        const d = new Date();
        d.setDate(d.getDate() - rangeDays);
        return d.toISOString().split('T')[0];
    })();

    const filtered = cutoff
        ? allEntries.filter(e => e.date >= cutoff)
        : allEntries;

    const labels  = filtered.map(e => e.date);
    const weights = filtered.map(e => e.weight);

    const canvas = document.getElementById('weightChart');
    if (!canvas) return;

    chartStore['weightChart'] = new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: 'Weight (kg)',
                data: weights,
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59,130,246,0.08)',
                borderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6,
                fill: true,
                tension: 0.3,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: ctx => ` ${ctx.parsed.y} kg`
                    }
                }
            },
            scales: {
                x: {
                    ticks: { maxTicksLimit: 8, maxRotation: 0 },
                    grid:  { display: false }
                },
                y: {
                    ticks: { callback: v => `${v} kg` },
                    grid:  { color: 'rgba(100,116,139,0.1)' }
                }
            }
        }
    });
}
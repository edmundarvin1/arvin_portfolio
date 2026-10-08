// Trading P&L Dashboard
// This file fetches data from the backend API and updates the dashboard

const API_BASE_URL = '/api'; // Backend API endpoint

let pnlChart = null;

// Fetch trading data from backend
async function fetchTradingData() {
    try {
        const response = await fetch(`${API_BASE_URL}/trading/summary`);
        if (!response.ok) throw new Error('Failed to fetch data');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching trading data:', error);
        throw error;
    }
}

// Update metrics cards
function updateMetrics(data) {
    document.getElementById('total-pnl').textContent = `$${data.totalPnL.toFixed(2)}`;
    document.getElementById('win-rate').textContent = `${data.winRate.toFixed(1)}%`;
    document.getElementById('total-trades').textContent = data.totalTrades;
    document.getElementById('sharpe-ratio').textContent = data.sharpeRatio.toFixed(2);
}

// Create P&L chart
function createPnLChart(data) {
    const ctx = document.getElementById('pnl-chart').getContext('2d');

    if (pnlChart) {
        pnlChart.destroy();
    }

    pnlChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: 'Cumulative P&L',
                data: data.cumulativePnL,
                borderColor: '#000',
                backgroundColor: 'rgba(0, 0, 0, 0.05)',
                borderWidth: 1.5,
                tension: 0.1,
                pointRadius: 0,
                pointHoverRadius: 4,
                pointHoverBackgroundColor: '#000',
                pointHoverBorderColor: '#fff',
                pointHoverBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: '#000',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    padding: 12,
                    displayColors: false,
                    cornerRadius: 4
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: '#e5e5e5',
                        borderColor: '#e5e5e5'
                    },
                    ticks: {
                        color: '#666',
                        font: {
                            size: 12
                        }
                    }
                },
                x: {
                    grid: {
                        display: false,
                        borderColor: '#e5e5e5'
                    },
                    ticks: {
                        color: '#666',
                        font: {
                            size: 12
                        }
                    }
                }
            }
        }
    });
}

// Update trades table
function updateTradesTable(trades) {
    const tbody = document.querySelector('#trades-list tbody');
    tbody.innerHTML = '';

    trades.forEach(trade => {
        const row = tbody.insertRow();
        const pnlColor = trade.pnl >= 0 ? '#000' : '#666';
        row.innerHTML = `
            <td>${new Date(trade.date).toLocaleDateString()}</td>
            <td>${trade.pair}</td>
            <td>${trade.type}</td>
            <td style="color: ${pnlColor}">${trade.pnl >= 0 ? '+' : ''}$${trade.pnl.toFixed(2)}</td>
        `;
    });
}

// Initialize dashboard
async function initDashboard() {
    const loadingEl = document.getElementById('loading');
    const errorEl = document.getElementById('error');
    const contentEl = document.getElementById('dashboard-content');

    try {
        loadingEl.style.display = 'block';
        errorEl.style.display = 'none';

        const data = await fetchTradingData();

        updateMetrics(data.summary);
        createPnLChart(data.chartData);
        updateTradesTable(data.recentTrades);

        loadingEl.style.display = 'none';
        contentEl.style.display = 'block';

    } catch (error) {
        loadingEl.style.display = 'none';
        errorEl.style.display = 'block';
        errorEl.textContent = `Error loading dashboard: ${error.message}`;
    }
}

// Auto-refresh every 30 seconds
setInterval(initDashboard, 30000);

// Load on page load
document.addEventListener('DOMContentLoaded', initDashboard);

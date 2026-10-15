// Gym Analytics Dashboard
// This file fetches data from Google Sheets via backend API

const API_BASE_URL = '/api'; // Backend API endpoint

let volumeChart = null;
let exerciseChart = null;

// Fetch gym data from backend
async function fetchGymData() {
    try {
        const response = await fetch(`${API_BASE_URL}/gym/summary`);
        if (!response.ok) throw new Error('Failed to fetch data');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching gym data:', error);
        throw error;
    }
}

// Update metrics cards
function updateMetrics(data) {
    document.getElementById('total-workouts').textContent = data.totalWorkouts;
    document.getElementById('total-volume').textContent = data.totalVolume.toLocaleString();
    document.getElementById('current-streak').textContent = `${data.currentStreak} days`;
    document.getElementById('prs-month').textContent = data.prsThisMonth;
}

// Create volume over time chart
function createVolumeChart(data) {
    const ctx = document.getElementById('volume-chart').getContext('2d');

    if (volumeChart) {
        volumeChart.destroy();
    }

    volumeChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.dates,
            datasets: [{
                label: 'Volume (kg)',
                data: data.volumes,
                backgroundColor: 'rgba(0, 0, 0, 0.08)',
                borderColor: 'transparent',
                borderWidth: 0
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

// Create exercise progress chart
function createExerciseChart(data) {
    const ctx = document.getElementById('exercise-chart').getContext('2d');

    if (exerciseChart) {
        exerciseChart.destroy();
    }

    // Generate grayscale colors for different exercises
    const grayScales = ['#000', '#333', '#666', '#999'];

    exerciseChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: data.exercises.map((exercise, index) => ({
                label: exercise.name,
                data: exercise.weights,
                borderColor: grayScales[index % grayScales.length],
                backgroundColor: `rgba(0, 0, 0, ${0.05 + (index * 0.03)})`,
                borderWidth: 1.5,
                tension: 0.1,
                pointRadius: 0,
                pointHoverRadius: 4,
                pointHoverBackgroundColor: grayScales[index % grayScales.length],
                pointHoverBorderColor: '#fff',
                pointHoverBorderWidth: 2
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        boxWidth: 12,
                        padding: 15,
                        color: '#000',
                        font: {
                            size: 12,
                            weight: 400
                        }
                    }
                },
                tooltip: {
                    backgroundColor: '#000',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    padding: 12,
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

// Update PRs list
function updatePRsList(prs) {
    const container = document.getElementById('prs-list');
    container.innerHTML = '';

    prs.forEach(pr => {
        const prItem = document.createElement('div');
        prItem.className = 'pr-item';
        prItem.innerHTML = `
            <div class="pr-exercise">${pr.exercise}</div>
            <div class="pr-details">
                <span class="pr-weight">${pr.weight}kg × ${pr.reps}</span>
                <span class="pr-date">${new Date(pr.date).toLocaleDateString()}</span>
            </div>
        `;
        container.appendChild(prItem);
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

        const data = await fetchGymData();

        updateMetrics(data.summary);
        createVolumeChart(data.volumeData);
        createExerciseChart(data.exerciseProgress);
        updatePRsList(data.personalRecords);

        loadingEl.style.display = 'none';
        contentEl.style.display = 'block';

    } catch (error) {
        loadingEl.style.display = 'none';
        errorEl.style.display = 'block';
        errorEl.textContent = `Error loading dashboard: ${error.message}`;
    }
}

// Load on page load
document.addEventListener('DOMContentLoaded', initDashboard);

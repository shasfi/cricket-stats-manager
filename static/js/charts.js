// Charts.js - Cricket Statistics Data Visualization

let playerBattingChart = null;
let playerBowlingChart = null;

// Chart.js default configuration for dark theme
Chart.defaults.color = '#fff';
Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.1)';
Chart.defaults.backgroundColor = 'rgba(255, 255, 255, 0.1)';

// Color palette for different cricket formats
const formatColors = {
    'Test': {
        background: 'rgba(220, 53, 69, 0.2)',
        border: 'rgba(220, 53, 69, 1)',
        point: 'rgba(220, 53, 69, 1)'
    },
    'ODI': {
        background: 'rgba(13, 202, 240, 0.2)',
        border: 'rgba(13, 202, 240, 1)',
        point: 'rgba(13, 202, 240, 1)'
    },
    'T20': {
        background: 'rgba(25, 135, 84, 0.2)',
        border: 'rgba(25, 135, 84, 1)',
        point: 'rgba(25, 135, 84, 1)'
    }
};

// Initialize player performance charts
function initializePlayerCharts(playerId) {
    fetchPlayerStats(playerId, '')
        .then(data => {
            if (data && data.years.length > 0) {
                createBattingChart(data);
                createBowlingChart(data);
            } else {
                showNoDataMessage();
            }
        })
        .catch(error => {
            console.error('Error initializing charts:', error);
            showErrorMessage();
        });
}

// Update charts with format filter
function updatePlayerCharts(playerId, format) {
    fetchPlayerStats(playerId, format)
        .then(data => {
            if (data && data.years.length > 0) {
                updateBattingChart(data);
                updateBowlingChart(data);
            } else {
                showNoDataMessage();
            }
        })
        .catch(error => {
            console.error('Error updating charts:', error);
            showErrorMessage();
        });
}

// Fetch player statistics from API
async function fetchPlayerStats(playerId, format) {
    try {
        const url = `/api/player_stats/${playerId}${format ? `?format=${format}` : ''}`;
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching player stats:', error);
        throw error;
    }
}

// Create batting performance chart
function createBattingChart(data) {
    const ctx = document.getElementById('battingChart');
    if (!ctx) return;

    // Destroy existing chart
    if (playerBattingChart) {
        playerBattingChart.destroy();
    }

    // Group data by format
    const formatData = groupDataByFormat(data);
    const datasets = [];

    Object.keys(formatData).forEach(format => {
        const formatStats = formatData[format];
        const colors = formatColors[format] || formatColors['Test'];

        // Runs dataset
        datasets.push({
            label: `${format} - Runs`,
            data: formatStats.years.map((year, index) => ({
                x: year,
                y: formatStats.runs[index]
            })),
            borderColor: colors.border,
            backgroundColor: colors.background,
            pointBackgroundColor: colors.point,
            pointBorderColor: colors.border,
            tension: 0.4,
            yAxisID: 'y'
        });

        // Average dataset
        datasets.push({
            label: `${format} - Average`,
            data: formatStats.years.map((year, index) => ({
                x: year,
                y: formatStats.average[index]
            })),
            borderColor: colors.border,
            backgroundColor: 'transparent',
            pointBackgroundColor: colors.point,
            pointBorderColor: colors.border,
            borderDash: [5, 5],
            tension: 0.4,
            yAxisID: 'y1'
        });
    });

    playerBattingChart = new Chart(ctx, {
        type: 'line',
        data: { datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Batting Performance Over Time',
                    color: '#fff'
                },
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        color: '#fff',
                        usePointStyle: true
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: 'rgba(255, 255, 255, 0.2)',
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    type: 'linear',
                    display: true,
                    title: {
                        display: true,
                        text: 'Year',
                        color: '#fff'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#fff'
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Runs',
                        color: '#fff'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#fff'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Average',
                        color: '#fff'
                    },
                    grid: {
                        drawOnChartArea: false,
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#fff'
                    }
                }
            }
        }
    });
}

// Create bowling performance chart
function createBowlingChart(data) {
    const ctx = document.getElementById('bowlingChart');
    if (!ctx) return;

    // Destroy existing chart
    if (playerBowlingChart) {
        playerBowlingChart.destroy();
    }

    // Group data by format
    const formatData = groupDataByFormat(data);
    const datasets = [];

    Object.keys(formatData).forEach(format => {
        const formatStats = formatData[format];
        const colors = formatColors[format] || formatColors['Test'];

        // Filter out years with no bowling data
        const bowlingData = formatStats.years.map((year, index) => ({
            year,
            wickets: formatStats.wickets[index],
            economy: formatStats.economy_rate[index]
        })).filter(item => item.wickets > 0 || item.economy > 0);

        if (bowlingData.length > 0) {
            // Wickets dataset
            datasets.push({
                label: `${format} - Wickets`,
                data: bowlingData.map(item => ({
                    x: item.year,
                    y: item.wickets
                })),
                borderColor: colors.border,
                backgroundColor: colors.background,
                pointBackgroundColor: colors.point,
                pointBorderColor: colors.border,
                tension: 0.4,
                yAxisID: 'y'
            });

            // Economy rate dataset
            datasets.push({
                label: `${format} - Economy`,
                data: bowlingData.map(item => ({
                    x: item.year,
                    y: item.economy
                })),
                borderColor: colors.border,
                backgroundColor: 'transparent',
                pointBackgroundColor: colors.point,
                pointBorderColor: colors.border,
                borderDash: [5, 5],
                tension: 0.4,
                yAxisID: 'y1'
            });
        }
    });

    if (datasets.length === 0) {
        showNoBowlingDataMessage();
        return;
    }

    playerBowlingChart = new Chart(ctx, {
        type: 'line',
        data: { datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Bowling Performance Over Time',
                    color: '#fff'
                },
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        color: '#fff',
                        usePointStyle: true
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: 'rgba(255, 255, 255, 0.2)',
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    type: 'linear',
                    display: true,
                    title: {
                        display: true,
                        text: 'Year',
                        color: '#fff'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#fff'
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Wickets',
                        color: '#fff'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#fff'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Economy Rate',
                        color: '#fff'
                    },
                    grid: {
                        drawOnChartArea: false,
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#fff'
                    }
                }
            }
        }
    });
}

// Update batting chart with new data
function updateBattingChart(data) {
    if (playerBattingChart) {
        createBattingChart(data);
    }
}

// Update bowling chart with new data
function updateBowlingChart(data) {
    if (playerBowlingChart) {
        createBowlingChart(data);
    }
}

// Group data by cricket format
function groupDataByFormat(data) {
    const formatData = {};
    
    data.formats.forEach((format, index) => {
        if (!formatData[format]) {
            formatData[format] = {
                years: [],
                runs: [],
                average: [],
                strike_rate: [],
                wickets: [],
                bowling_average: [],
                economy_rate: []
            };
        }
        
        formatData[format].years.push(data.years[index]);
        formatData[format].runs.push(data.runs[index] || 0);
        formatData[format].average.push(data.average[index] || 0);
        formatData[format].strike_rate.push(data.strike_rate[index] || 0);
        formatData[format].wickets.push(data.wickets[index] || 0);
        formatData[format].bowling_average.push(data.bowling_average[index] || 0);
        formatData[format].economy_rate.push(data.economy_rate[index] || 0);
    });
    
    return formatData;
}

// Show message when no data is available
function showNoDataMessage() {
    const battingChart = document.getElementById('battingChart');
    const bowlingChart = document.getElementById('bowlingChart');
    
    if (battingChart) {
        battingChart.parentElement.innerHTML = `
            <div class="text-center text-muted py-5">
                <i class="fas fa-chart-line fa-3x mb-3"></i>
                <h5>No Batting Data</h5>
                <p>No batting statistics available for the selected filter.</p>
            </div>
        `;
    }
    
    if (bowlingChart) {
        bowlingChart.parentElement.innerHTML = `
            <div class="text-center text-muted py-5">
                <i class="fas fa-chart-bar fa-3x mb-3"></i>
                <h5>No Bowling Data</h5>
                <p>No bowling statistics available for the selected filter.</p>
            </div>
        `;
    }
}

// Show message when no bowling data is available
function showNoBowlingDataMessage() {
    const bowlingChart = document.getElementById('bowlingChart');
    
    if (bowlingChart) {
        bowlingChart.parentElement.innerHTML = `
            <div class="text-center text-muted py-5">
                <i class="fas fa-dot-circle fa-3x mb-3"></i>
                <h5>No Bowling Data</h5>
                <p>This player has no bowling statistics for the selected period.</p>
            </div>
        `;
    }
}

// Show error message
function showErrorMessage() {
    const battingChart = document.getElementById('battingChart');
    const bowlingChart = document.getElementById('bowlingChart');
    
    const errorMessage = `
        <div class="text-center text-danger py-5">
            <i class="fas fa-exclamation-triangle fa-3x mb-3"></i>
            <h5>Error Loading Data</h5>
            <p>Unable to load chart data. Please try again later.</p>
        </div>
    `;
    
    if (battingChart) {
        battingChart.parentElement.innerHTML = errorMessage;
    }
    
    if (bowlingChart) {
        bowlingChart.parentElement.innerHTML = errorMessage;
    }
}

// Cleanup charts on page unload
window.addEventListener('beforeunload', function() {
    if (playerBattingChart) {
        playerBattingChart.destroy();
    }
    if (playerBowlingChart) {
        playerBowlingChart.destroy();
    }
});

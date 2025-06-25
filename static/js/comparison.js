// Comparison.js - Player Comparison Charts and Utilities

let comparisonChart = null;

// Initialize comparison chart
function initializeComparisonChart(comparisonData) {
    const ctx = document.getElementById('comparisonChart');
    if (!ctx) return;

    // Destroy existing chart
    if (comparisonChart) {
        comparisonChart.destroy();
    }

    // Prepare data for radar chart
    const chartData = prepareComparisonData(comparisonData);
    
    if (!chartData) {
        showComparisonError();
        return;
    }

    comparisonChart = new Chart(ctx, {
        type: 'radar',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: `Player Comparison - ${comparisonData.format} Cricket`,
                    color: '#fff',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        color: '#fff',
                        usePointStyle: true,
                        padding: 20
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: 'rgba(255, 255, 255, 0.2)',
                    borderWidth: 1,
                    callbacks: {
                        label: function(context) {
                            const datasetLabel = context.dataset.label;
                            const value = context.parsed.r;
                            const metric = context.label;
                            
                            // Format tooltip based on metric type
                            let formattedValue = value;
                            if (metric.includes('Average') || metric.includes('Economy')) {
                                formattedValue = value.toFixed(2);
                            }
                            
                            return `${datasetLabel}: ${formattedValue}`;
                        }
                    }
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.2)'
                    },
                    angleLines: {
                        color: 'rgba(255, 255, 255, 0.2)'
                    },
                    pointLabels: {
                        color: '#fff',
                        font: {
                            size: 12
                        }
                    },
                    ticks: {
                        color: '#fff',
                        backdropColor: 'transparent',
                        callback: function(value) {
                            return Math.round(value);
                        }
                    }
                }
            },
            elements: {
                line: {
                    borderWidth: 3
                },
                point: {
                    radius: 4,
                    hoverRadius: 6
                }
            }
        }
    });
}

// Prepare data for comparison radar chart
function prepareComparisonData(comparisonData) {
    const player1Stats = comparisonData.player1.stats;
    const player2Stats = comparisonData.player2.stats;
    
    if (!player1Stats || !player2Stats) {
        return null;
    }

    // Define metrics for comparison
    const metrics = [
        { key: 'runs', label: 'Total Runs', normalize: true },
        { key: 'batting_average', label: 'Batting Average', normalize: false },
        { key: 'hundreds', label: 'Centuries', normalize: true },
        { key: 'fifties', label: 'Half Centuries', normalize: true },
        { key: 'wickets', label: 'Wickets', normalize: true },
        { key: 'catches', label: 'Catches', normalize: true }
    ];

    // Filter metrics that have data for at least one player
    const validMetrics = metrics.filter(metric => 
        (player1Stats[metric.key] || 0) > 0 || (player2Stats[metric.key] || 0) > 0
    );

    if (validMetrics.length === 0) {
        return null;
    }

    // Normalize values for radar chart
    const normalizedData = normalizeMetrics(validMetrics, player1Stats, player2Stats);

    return {
        labels: validMetrics.map(metric => metric.label),
        datasets: [
            {
                label: comparisonData.player1.name,
                data: normalizedData.player1,
                backgroundColor: 'rgba(13, 110, 253, 0.2)',
                borderColor: 'rgba(13, 110, 253, 1)',
                pointBackgroundColor: 'rgba(13, 110, 253, 1)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(13, 110, 253, 1)'
            },
            {
                label: comparisonData.player2.name,
                data: normalizedData.player2,
                backgroundColor: 'rgba(25, 135, 84, 0.2)',
                borderColor: 'rgba(25, 135, 84, 1)',
                pointBackgroundColor: 'rgba(25, 135, 84, 1)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(25, 135, 84, 1)'
            }
        ]
    };
}

// Normalize metrics for radar chart display
function normalizeMetrics(metrics, player1Stats, player2Stats) {
    const player1Data = [];
    const player2Data = [];

    metrics.forEach(metric => {
        const player1Value = player1Stats[metric.key] || 0;
        const player2Value = player2Stats[metric.key] || 0;

        if (metric.normalize) {
            // For countable metrics, normalize to percentage of max
            const maxValue = Math.max(player1Value, player2Value);
            if (maxValue > 0) {
                player1Data.push((player1Value / maxValue) * 100);
                player2Data.push((player2Value / maxValue) * 100);
            } else {
                player1Data.push(0);
                player2Data.push(0);
            }
        } else {
            // For averages and rates, use direct values (capped at reasonable max)
            const maxCap = metric.key === 'batting_average' ? 100 : 10;
            player1Data.push(Math.min(player1Value, maxCap));
            player2Data.push(Math.min(player2Value, maxCap));
        }
    });

    return {
        player1: player1Data,
        player2: player2Data
    };
}

// Create performance comparison bar chart
function createPerformanceComparison(comparisonData) {
    const ctx = document.getElementById('performanceChart');
    if (!ctx) return;

    const player1Stats = comparisonData.player1.stats;
    const player2Stats = comparisonData.player2.stats;

    const metrics = ['runs', 'batting_average', 'hundreds', 'fifties', 'wickets'];
    const labels = ['Total Runs', 'Batting Average', 'Centuries', 'Half Centuries', 'Wickets'];

    const player1Data = metrics.map(metric => player1Stats[metric] || 0);
    const player2Data = metrics.map(metric => player2Stats[metric] || 0);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: comparisonData.player1.name,
                    data: player1Data,
                    backgroundColor: 'rgba(13, 110, 253, 0.7)',
                    borderColor: 'rgba(13, 110, 253, 1)',
                    borderWidth: 1
                },
                {
                    label: comparisonData.player2.name,
                    data: player2Data,
                    backgroundColor: 'rgba(25, 135, 84, 0.7)',
                    borderColor: 'rgba(25, 135, 84, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Statistical Comparison',
                    color: '#fff'
                },
                legend: {
                    display: true,
                    labels: {
                        color: '#fff'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff'
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#fff'
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
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

// Calculate comparison summary
function calculateComparisonSummary(comparisonData) {
    const player1Stats = comparisonData.player1.stats;
    const player2Stats = comparisonData.player2.stats;

    const categories = [
        { key: 'runs', label: 'Total Runs', higher_better: true },
        { key: 'batting_average', label: 'Batting Average', higher_better: true },
        { key: 'hundreds', label: 'Centuries', higher_better: true },
        { key: 'fifties', label: 'Half Centuries', higher_better: true },
        { key: 'wickets', label: 'Wickets', higher_better: true },
        { key: 'bowling_average', label: 'Bowling Average', higher_better: false },
        { key: 'economy_rate', label: 'Economy Rate', higher_better: false }
    ];

    let player1Wins = 0;
    let player2Wins = 0;
    let ties = 0;

    categories.forEach(category => {
        const value1 = player1Stats[category.key] || 0;
        const value2 = player2Stats[category.key] || 0;

        // Skip if both values are 0
        if (value1 === 0 && value2 === 0) return;

        if (category.higher_better) {
            if (value1 > value2) player1Wins++;
            else if (value2 > value1) player2Wins++;
            else ties++;
        } else {
            // For bowling average and economy rate, lower is better
            if (value1 > 0 && value2 > 0) {
                if (value1 < value2) player1Wins++;
                else if (value2 < value1) player2Wins++;
                else ties++;
            } else if (value1 > 0 && value2 === 0) {
                player1Wins++;
            } else if (value2 > 0 && value1 === 0) {
                player2Wins++;
            }
        }
    });

    return {
        player1: {
            name: comparisonData.player1.name,
            wins: player1Wins
        },
        player2: {
            name: comparisonData.player2.name,
            wins: player2Wins
        },
        ties: ties,
        total: player1Wins + player2Wins + ties
    };
}

// Show comparison error message
function showComparisonError() {
    const chartContainer = document.getElementById('comparisonChart').parentElement;
    chartContainer.innerHTML = `
        <div class="text-center text-muted py-5">
            <i class="fas fa-exclamation-triangle fa-3x mb-3"></i>
            <h5>Unable to Generate Comparison</h5>
            <p>Insufficient data available for comparison visualization.</p>
        </div>
    `;
}

// Export comparison data as CSV
function exportComparisonCSV(comparisonData) {
    const player1Stats = comparisonData.player1.stats;
    const player2Stats = comparisonData.player2.stats;

    const headers = ['Metric', comparisonData.player1.name, comparisonData.player2.name];
    const rows = [
        ['Matches', player1Stats.matches || 0, player2Stats.matches || 0],
        ['Total Runs', player1Stats.runs || 0, player2Stats.runs || 0],
        ['Batting Average', player1Stats.batting_average || 0, player2Stats.batting_average || 0],
        ['Highest Score', player1Stats.highest_score || 0, player2Stats.highest_score || 0],
        ['Centuries', player1Stats.hundreds || 0, player2Stats.hundreds || 0],
        ['Half Centuries', player1Stats.fifties || 0, player2Stats.fifties || 0],
        ['Wickets', player1Stats.wickets || 0, player2Stats.wickets || 0],
        ['Bowling Average', player1Stats.bowling_average || 0, player2Stats.bowling_average || 0],
        ['Economy Rate', player1Stats.economy_rate || 0, player2Stats.economy_rate || 0],
        ['Catches', player1Stats.catches || 0, player2Stats.catches || 0]
    ];

    let csvContent = headers.join(',') + '\n';
    rows.forEach(row => {
        csvContent += row.join(',') + '\n';
    });

    // Create and download CSV file
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `cricket_comparison_${comparisonData.player1.name.replace(/\s+/g, '_')}_vs_${comparisonData.player2.name.replace(/\s+/g, '_')}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Cleanup comparison chart on page unload
window.addEventListener('beforeunload', function() {
    if (comparisonChart) {
        comparisonChart.destroy();
    }
});

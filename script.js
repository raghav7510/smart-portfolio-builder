// ===== THEME TOGGLE =====
const themeToggle = document.getElementById('themeToggle');
const htmlElement = document.documentElement;

// Load saved theme
const savedTheme = localStorage.getItem('theme') || 'light';
htmlElement.setAttribute('data-theme', savedTheme);
themeToggle.textContent = savedTheme === 'dark' ? '☀️' : '🌙';

themeToggle.addEventListener('click', () => {
    const currentTheme = htmlElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    htmlElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    themeToggle.textContent = newTheme === 'dark' ? '☀️' : '🌙';
});

// ===== TAB SWITCHING =====
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.getAttribute('data-tab');
        
        // Remove active class from all
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(t => t.classList.remove('active'));
        
        // Add active to clicked
        btn.classList.add('active');
        document.getElementById(tabName).classList.add('active');
    });
});

// ===== FORMATTING FUNCTIONS =====
function formatNumber(num) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).replace('₹', '₹ ');
}

function formatNumberSimple(num) {
    return new Intl.NumberFormat('en-IN').format(Math.round(num));
}

// ===== PORTFOLIO CALCULATOR =====
const portfolioForm = document.getElementById('portfolioForm');
const portfolioResults = document.getElementById('portfolioResults');
const portfolioEmpty = document.getElementById('portfolioEmpty');

// Live input formatting
document.getElementById('income').addEventListener('input', (e) => {
    document.getElementById('incomeValue').textContent = formatNumberSimple(e.target.value);
    updateSavingsIndicator();
});

document.getElementById('expenses').addEventListener('input', (e) => {
    document.getElementById('expensesValue').textContent = formatNumberSimple(e.target.value);
    updateSavingsIndicator();
});

document.getElementById('initialInvestment').addEventListener('input', (e) => {
    document.getElementById('initialValue').textContent = formatNumberSimple(e.target.value);
});

document.getElementById('monthlyContribution').addEventListener('input', (e) => {
    document.getElementById('contributionValue').textContent = formatNumberSimple(e.target.value);
});

document.getElementById('horizon').addEventListener('input', (e) => {
    const years = e.target.value;
    document.getElementById('horizonValue').textContent = years + ' ' + (years === '1' ? 'year' : 'years');
});

document.getElementById('riskScore').addEventListener('input', (e) => {
    const score = parseInt(e.target.value);
    const riskLabel = document.getElementById('riskLabel');
    
    if (score <= 8) {
        riskLabel.textContent = '🛡️ Conservative';
    } else if (score <= 14) {
        riskLabel.textContent = '⚖️ Balanced';
    } else if (score <= 18) {
        riskLabel.textContent = '📈 Aggressive';
    } else {
        riskLabel.textContent = '🚀 Maximum Growth';
    }
});

function updateSavingsIndicator() {
    const income = parseFloat(document.getElementById('income').value) || 0;
    const expenses = parseFloat(document.getElementById('expenses').value) || 0;
    const savings = Math.max(0, income - expenses);
    document.getElementById('monthlySavings').textContent = formatNumber(savings);
}

portfolioForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        income: parseFloat(document.getElementById('income').value),
        expenses: parseFloat(document.getElementById('expenses').value),
        initial_investment: parseFloat(document.getElementById('initialInvestment').value),
        monthly_contribution: parseFloat(document.getElementById('monthlyContribution').value),
        investment_horizon: parseInt(document.getElementById('horizon').value),
        risk_score: parseInt(document.getElementById('riskScore').value)
    };

    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            showError(data.error || 'Calculation failed');
            return;
        }

        displayPortfolioResults(data);
        portfolioEmpty.style.display = 'none';
        portfolioResults.style.display = 'flex';
    } catch (error) {
        console.error('Error:', error);
        showError('An error occurred. Please try again.');
    }
});

function displayPortfolioResults(data) {
    // Profile card
    const profile = data.profile;
    document.getElementById('profileCard').style.background = 
        `linear-gradient(135deg, ${profile.color} 0%, ${adjustBrightness(profile.color, -20)} 100%)`;
    document.getElementById('profileIcon').textContent = profile.emoji;
    document.getElementById('profileTitle').textContent = profile.title;
    document.getElementById('profileName').textContent = profile.profile;

    // Metrics
    document.getElementById('metric1').textContent = formatNumber(data.metrics.monthly_savings);
    document.getElementById('metric2').textContent = formatNumber(data.metrics.annual_savings);
    document.getElementById('metric3').textContent = formatNumber(data.metrics.emergency_fund);
    document.getElementById('metric4').textContent = formatNumber(data.metrics.total_investable);

    // Allocation chart
    drawAllocationChart(data.portfolio);

    // Scenarios
    document.getElementById('worstValue').textContent = formatNumber(data.scenarios.worst.final_value);
    document.getElementById('worstGain').textContent = formatNumber(data.scenarios.worst.gain) + ' gain';
    
    document.getElementById('expectedValue').textContent = formatNumber(data.scenarios.expected.final_value);
    document.getElementById('expectedGain').textContent = formatNumber(data.scenarios.expected.gain) + ' gain';
    
    document.getElementById('bestValue').textContent = formatNumber(data.scenarios.best.final_value);
    document.getElementById('bestGain').textContent = formatNumber(data.scenarios.best.gain) + ' gain';

    // Projection chart
    drawProjectionChart(data.scenarios);

    // Insights
    displayInsights(data.insights);
}

function drawAllocationChart(portfolio) {
    const ctx = document.getElementById('allocationChart').getContext('2d');
    
    const colors = {
        'Equity': '#3B82F6',
        'Debt': '#10B981',
        'Gold': '#F59E0B',
        'Cash': '#6B7280'
    };

    if (window.allocationChartInstance) {
        window.allocationChartInstance.destroy();
    }

    window.allocationChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(portfolio),
            datasets: [{
                data: Object.values(portfolio),
                backgroundColor: Object.keys(portfolio).map(k => colors[k]),
                borderColor: getComputedStyle(document.documentElement).getPropertyValue('--bg'),
                borderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary'),
                        padding: 15,
                        font: { size: 12, weight: 'bold' }
                    }
                }
            }
        }
    });
}

function drawProjectionChart(scenarios) {
    const ctx = document.getElementById('projectionChart').getContext('2d');

    if (window.projectionChartInstance) {
        window.projectionChartInstance.destroy();
    }

    const worstData = scenarios.worst.projections;
    const expectedData = scenarios.expected.projections;
    const bestData = scenarios.best.projections;

    window.projectionChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: expectedData.map(p => p.year.toFixed(1) + 'y'),
            datasets: [
                {
                    label: 'Worst Case',
                    data: worstData.map(p => p.value),
                    borderColor: '#EF4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    tension: 0.4,
                    fill: false
                },
                {
                    label: 'Expected',
                    data: expectedData.map(p => p.value),
                    borderColor: '#F59E0B',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 0,
                    pointHoverRadius: 6
                },
                {
                    label: 'Best Case',
                    data: bestData.map(p => p.value),
                    borderColor: '#10B981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary'),
                        font: { size: 12 }
                    }
                }
            },
            scales: {
                y: {
                    ticks: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary'),
                        callback: (value) => '₹' + formatNumberSimple(value)
                    }
                },
                x: {
                    ticks: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary')
                    }
                }
            }
        }
    });
}

function displayInsights(insights) {
    const grid = document.getElementById('insightsGrid');
    grid.innerHTML = '';

    insights.forEach(insight => {
        const item = document.createElement('div');
        item.className = 'insight-item';
        item.innerHTML = `
            <div class="insight-icon">${insight.icon}</div>
            <div class="insight-title">${insight.title}</div>
            <div class="insight-message">${insight.message}</div>
        `;
        grid.appendChild(item);
    });
}

// ===== SIP CALCULATOR =====
const sipForm = document.getElementById('sipForm');
const sipResults = document.getElementById('sipResults');
const sipEmpty = document.getElementById('sipEmpty');

document.getElementById('sipAmount').addEventListener('input', (e) => {
    document.getElementById('sipAmountValue').textContent = formatNumberSimple(e.target.value);
});

document.getElementById('sipReturn').addEventListener('input', (e) => {
    document.getElementById('sipReturnValue').textContent = e.target.value + '%';
});

document.getElementById('sipYears').addEventListener('input', (e) => {
    document.getElementById('sipYearsValue').textContent = e.target.value + ' years';
});

sipForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = {
        monthly_sip: parseFloat(document.getElementById('sipAmount').value),
        annual_return: parseFloat(document.getElementById('sipReturn').value) / 100,
        years: parseInt(document.getElementById('sipYears').value)
    };

    try {
        const response = await fetch('/api/sip-calculator', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            showError(data.error || 'Calculation failed');
            return;
        }

        displaySIPResults(data);
        sipEmpty.style.display = 'none';
        sipResults.style.display = 'flex';
    } catch (error) {
        console.error('Error:', error);
        showError('An error occurred. Please try again.');
    }
});

function displaySIPResults(data) {
    document.getElementById('sipInvested').textContent = formatNumber(data.total_invested);
    document.getElementById('sipFinal').textContent = formatNumber(data.final_value);
    document.getElementById('sipGain').textContent = formatNumber(data.gain);
    document.getElementById('sipGainPct').textContent = data.gain_percentage.toFixed(2) + '%';
    document.getElementById('compoundingValue').textContent = formatNumber(data.gain);

    drawSIPChart(data);
}

function drawSIPChart(data) {
    const ctx = document.getElementById('sipChart').getContext('2d');

    if (window.sipChartInstance) {
        window.sipChartInstance.destroy();
    }

    const months = Array.from({ length: data.months + 1 }, (_, i) => i);
    const invested = months.map(m => data.monthly_sip * m);
    const values = [];

    months.forEach(month => {
        const monthlyRate = (data.annual_return) / 12;
        let value = 0;
        for (let m = 1; m <= month; m++) {
            value += data.monthly_sip * Math.pow(1 + monthlyRate, month - m + 1);
        }
        values.push(value);
    });

    window.sipChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: months.map(m => (m / 12).toFixed(1) + 'y'),
            datasets: [
                {
                    label: 'Portfolio Value',
                    data: values,
                    borderColor: '#10B981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Total Invested',
                    data: invested,
                    borderColor: '#3B82F6',
                    backgroundColor: 'rgba(59, 130, 246, 0.05)',
                    tension: 0.4,
                    fill: false,
                    borderDash: [5, 5]
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary'),
                        font: { size: 12 }
                    }
                }
            },
            scales: {
                y: {
                    ticks: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary'),
                        callback: (value) => '₹' + formatNumberSimple(value)
                    }
                },
                x: {
                    ticks: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary')
                    }
                }
            }
        }
    });
}

// ===== COMPARISON =====
const comparisonForm = document.getElementById('comparisonForm');
const comparisonResults = document.getElementById('comparisonResults');
const comparisonEmpty = document.getElementById('comparisonEmpty');

document.getElementById('compAmount').addEventListener('input', (e) => {
    document.getElementById('compAmountValue').textContent = formatNumberSimple(e.target.value);
});

document.getElementById('compReturn').addEventListener('input', (e) => {
    document.getElementById('compReturnValue').textContent = e.target.value + '%';
});

document.getElementById('compYears').addEventListener('input', (e) => {
    document.getElementById('compYearsValue').textContent = e.target.value + ' years';
});

comparisonForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = {
        amount: parseFloat(document.getElementById('compAmount').value),
        annual_return: parseFloat(document.getElementById('compReturn').value) / 100,
        years: parseInt(document.getElementById('compYears').value)
    };

    try {
        const response = await fetch('/api/comparison', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            showError(data.error || 'Comparison failed');
            return;
        }

        displayComparisonResults(data);
        comparisonEmpty.style.display = 'none';
        comparisonResults.style.display = 'flex';
    } catch (error) {
        console.error('Error:', error);
        showError('An error occurred. Please try again.');
    }
});

function displayComparisonResults(data) {
    // Lump Sum
    document.getElementById('lumpInvested').textContent = formatNumber(data.lump_sum.invested);
    document.getElementById('lumpFinal').textContent = formatNumber(data.lump_sum.final);
    document.getElementById('lumpGain').textContent = formatNumber(data.lump_sum.gain);

    // SIP
    document.getElementById('sipInvested2').textContent = formatNumber(data.sip.invested);
    document.getElementById('sipFinal2').textContent = formatNumber(data.sip.final);
    document.getElementById('sipGain2').textContent = formatNumber(data.sip.gain);

    // Advantage
    const advantageBox = document.getElementById('advantageBox');
    const title = document.getElementById('advantageTitle');
    const amount = document.getElementById('advantageAmount');
    const reason = document.getElementById('advantageReason');

    if (data.sip_advantage >= 0) {
        advantageBox.style.borderLeftColor = '#10B981';
        advantageBox.style.background = 'linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%)';
        title.textContent = '✅ SIP Wins!';
        title.style.color = '#10B981';
        amount.textContent = 'SIP is better by ' + formatNumber(data.sip_advantage);
        reason.textContent = 'SIP reduces timing risk and benefits from rupee cost averaging.';
    } else {
        advantageBox.style.borderLeftColor = '#3B82F6';
        advantageBox.style.background = 'linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%)';
        title.textContent = '💰 Lump Sum Wins!';
        title.style.color = '#3B82F6';
        amount.textContent = 'Lump Sum is better by ' + formatNumber(Math.abs(data.sip_advantage));
        reason.textContent = 'Lump sum works better in rising markets as money is invested immediately.';
    }

    drawComparisonChart(data);
}

function drawComparisonChart(data) {
    const ctx = document.getElementById('comparisonChart').getContext('2d');

    if (window.comparisonChartInstance) {
        window.comparisonChartInstance.destroy();
    }

    window.comparisonChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Lump Sum', 'SIP'],
            datasets: [{
                label: 'Final Value',
                data: [data.lump_sum.final, data.sip.final],
                backgroundColor: ['#3B82F6', '#10B981'],
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'x',
            plugins: {
                legend: {
                    labels: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary')
                    }
                }
            },
            scales: {
                y: {
                    ticks: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary'),
                        callback: (value) => '₹' + formatNumberSimple(value)
                    }
                },
                x: {
                    ticks: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary')
                    }
                }
            }
        }
    });
}

// ===== UTILITIES =====
function showError(message) {
    alert('Error: ' + message);
}

function adjustBrightness(color, percent) {
    const num = parseInt(color.replace('#', ''), 16);
    const amt = Math.round(2.55 * percent);
    const R = Math.max(0, Math.min(255, (num >> 16) + amt));
    const G = Math.max(0, Math.min(255, (num >> 8 & 0x00FF) + amt));
    const B = Math.max(0, Math.min(255, (num & 0x0000FF) + amt));
    return '#' + (0x1000000 + R * 0x10000 + G * 0x100 + B).toString(16).slice(1);
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateSavingsIndicator();
});

"""
Smart Portfolio Builder - Professional Edition
Financial Planning Application
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="Smart Portfolio Builder",
    page_icon="chart_with_upwards_trend",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ===== SESSION STATE FOR TAB NAVIGATION =====
if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = 0

# ===== DARK THEME CSS - FIXES FOR STREAMLIT =====
st.markdown("""
    <style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    /* DARK THEME COLOR SCHEME */
    :root {
        --bg-dark: #0e1117;
        --bg-darker: #010409;
        --bg-card: #161b22;
        --bg-elevated: #21262d;
        --text-primary: #c9d1d9;
        --text-secondary: #8b949e;
        --accent-blue: #a855f7;
        --accent-purple: #d946ef;
        --accent-green: #3fb950;
        --border-color: #30363d;
    }

    /* HIDE SIDEBAR COMPLETELY */
    [data-testid="stSidebar"] {
        display: none !important;
    }

    /* FIX MAIN CONTAINER - REMOVE WHITE BACKGROUNDS */
    [data-testid="stAppViewContainer"] {
        background-color: var(--bg-dark) !important;
        color: var(--text-primary) !important;
    }

    .main {
        max-width: 1400px;
        margin: 0 auto;
    }

    /* HIDE DECORATOR ELEMENTS THAT CAUSE WHITE TUBES */
    [data-testid="stDecoration"] {
        display: none !important;
    }

    /* FIX MARKDOWN TEXT VISIBILITY */
    p, span, div, label {
        color: var(--text-primary) !important;
    }

    /* HEADER STYLING - CLEARLY VISIBLE */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        margin-bottom: 16px !important;
    }

    h1 { font-size: 32px !important; }
    h2 { font-size: 24px !important; }
    h3 { font-size: 18px !important; }

    /* MAIN HEADER */
    .main-header {
        color: var(--text-primary);
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 8px;
        line-height: 1.2;
        text-align: center !important;
    }

    .sub-header {
        color: var(--text-secondary);
        font-size: 14px;
        margin-bottom: 24px;
    }

    /* SECTION DIVIDER */
    .divider {
        height: 2px;
        background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple), transparent);
        margin: 8px auto 24px;
        width: 100%;
        border-radius: 1px;
    }

    /* CENTER ALIGNMENT */
    .center-header {
        text-align: center !important;
    }

    .center-section {
        text-align: center;
    }

    .center-divider {
        margin: 8px auto 24px;
    }

    /* CALCULATOR CENTERING */
    .calculator-wrapper {
        display: flex;
        justify-content: center;
        max-width: 1200px;
        margin: 0 auto;
    }

    .calculator-wrapper > div {
        flex: 1;
    }

    /* METRIC CARD - DARK THEME */
    .metric-card {
        background: var(--bg-elevated) !important;
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        border-color: var(--accent-blue);
        background: var(--bg-card) !important;
    }

    .metric-label {
        font-size: 11px;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 800;
        color: var(--accent-blue);
        margin: 8px 0;
    }

    /* FORM STYLING - NO WHITE TUBES */
    .form-container {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* INPUT FIELDS */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stSlider > div > div > div > input,
    input {
        background-color: var(--bg-elevated) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px !important;
        padding: 10px 12px !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
    }

    input:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 2px rgba(88, 166, 255, 0.1) !important;
        outline: none !important;
    }

    /* SELECT DROPDOWN */
    .stSelectbox > div > div > select {
        background-color: var(--bg-elevated) !important;
    }

    /* SLIDER */
    .stSlider > div {
        color: var(--text-primary) !important;
    }

    /* RADIO BUTTONS */
    .stRadio > div {
        color: var(--text-primary) !important;
    }

    /* BUTTON STYLING */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-purple) 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        border: none !important;
        border-radius: 6px !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        font-size: 14px !important;
    }

    .stButton > button:hover {
        opacity: 0.9 !important;
        transform: translateY(-1px) !important;
    }

    /* TAB STYLING */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0 !important;
        border-bottom: 1px solid var(--border-color);
    }

    .stTabs [data-baseweb="tab"] {
        color: var(--text-secondary) !important;
        padding: 12px 16px !important;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: var(--accent-blue) !important;
        border-bottom: 2px solid var(--accent-blue) !important;
    }

    /* ALERT STYLING */
    .alert {
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 16px;
        border-left: 4px solid;
    }

    .alert-success {
        background: rgba(63, 185, 80, 0.1);
        border-left-color: var(--accent-green);
        color: var(--accent-green);
    }

    .alert-warning {
        background: rgba(248, 113, 113, 0.1);
        border-left-color: #f87171;
        color: #fca5a5;
    }

    .alert-danger {
        background: rgba(239, 68, 68, 0.1);
        border-left-color: #ef4444;
        color: #fca5a5;
    }

    /* CHART CONTAINER */
    .plotly-graph-div {
        background: var(--bg-card) !important;
    }

    /* REMOVE PLOTLY WATERMARK */
    .modebar {
        display: none !important;
    }

    /* EXPANDER STYLING */
    .stExpander {
        background: var(--bg-elevated) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px !important;
    }

    .streamlit-expanderHeader {
        color: var(--text-primary) !important;
    }

    /* FOOTER */
    .footer {
        color: var(--text-secondary);
        padding: 32px 0;
        margin-top: 48px;
        border-top: 1px solid var(--border-color);
        text-align: center;
        font-size: 13px;
        line-height: 1.6;
    }

    /* SPACING UTILITIES */
    .spacer {
        height: 20px;
    }

    .spacer-lg {
        height: 40px;
    }

    /* RESPONSIVE */
    @media (max-width: 768px) {
        h1 { font-size: 24px !important; }
        h2 { font-size: 18px !important; }
        h3 { font-size: 16px !important; }
    }
    </style>
""", unsafe_allow_html=True)

# ===== HELPER FUNCTIONS =====
def format_currency(value):
    """Format number as Indian currency"""
    if value >= 1_00_00_000:
        return f"Rs {value / 1_00_00_000:.2f} Cr"
    elif value >= 1_00_000:
        return f"Rs {value / 1_00_000:.2f} L"
    else:
        return f"Rs {value:,.0f}"

def format_percentage(value):
    """Format as percentage"""
    return f"{value:.2f}%"

def get_risk_profile(risk_score):
    """Get portfolio profile based on risk score"""
    profiles = {
        'low': {
            'name': 'Conservative - Capital Protector',
            'color': '#3fb950',
            'allocation': {'Equity': 25, 'Debt': 55, 'Gold': 12, 'Cash': 8}
        },
        'medium': {
            'name': 'Moderate - Growth Seeker',
            'color': '#f6ad55',
            'allocation': {'Equity': 50, 'Debt': 30, 'Gold': 12, 'Cash': 8}
        },
        'high': {
            'name': 'Aggressive - Growth Investor',
            'color': '#f87171',
            'allocation': {'Equity': 70, 'Debt': 15, 'Gold': 10, 'Cash': 5}
        },
        'very_high': {
            'name': 'Very Aggressive - Wealth Builder',
            'color': '#79c0ff',
            'allocation': {'Equity': 85, 'Debt': 8, 'Gold': 5, 'Cash': 2}
        }
    }
    
    if risk_score <= 8:
        return profiles['low']
    elif risk_score <= 14:
        return profiles['medium']
    elif risk_score <= 18:
        return profiles['high']
    else:
        return profiles['very_high']

def calculate_sip(monthly, return_rate, years):
    """Calculate SIP returns"""
    months = years * 12
    monthly_rate = return_rate / 12
    invested = monthly * months
    final_value = 0
    
    for m in range(1, months + 1):
        final_value += monthly * ((1 + monthly_rate) ** (months - m + 1))
    
    return {
        'invested': invested,
        'final': final_value,
        'gain': final_value - invested,
        'gain_pct': (final_value - invested) / invested * 100 if invested > 0 else 0
    }

def calculate_retirement(age, ret_age, savings, monthly, return_rate, inflation, expenses):
    """Calculate retirement corpus"""
    years_left = ret_age - age
    years_retired = 85 - ret_age
    
    monthly_rate = return_rate / 12
    months_left = years_left * 12
    
    # Future value of current savings
    fv_savings = savings * ((1 + monthly_rate) ** months_left)
    
    # Future value of monthly contributions
    fv_monthly = 0
    for m in range(1, months_left + 1):
        fv_monthly += monthly * ((1 + monthly_rate) ** (months_left - m + 1))
    
    total_projected = fv_savings + fv_monthly
    
    # Corpus needed
    monthly_retired = expenses * ((1 + inflation) ** years_left)
    corpus_needed = monthly_retired * 12 * years_retired
    
    return {
        'corpus_needed': corpus_needed,
        'corpus_projected': total_projected,
        'shortfall': max(0, corpus_needed - total_projected),
        'sufficient': total_projected >= corpus_needed
    }

def calculate_tax(income, regime='new'):
    """Calculate income tax (India)"""
    if regime == 'new':
        if income <= 300000:
            tax = 0
        elif income <= 600000:
            tax = (income - 300000) * 0.05
        elif income <= 900000:
            tax = 15000 + (income - 600000) * 0.10
        elif income <= 1200000:
            tax = 45000 + (income - 900000) * 0.15
        else:
            tax = 90000 + (income - 1200000) * 0.20
    else:  # Old regime
        if income <= 250000:
            tax = 0
        elif income <= 500000:
            tax = (income - 250000) * 0.05
        elif income <= 1000000:
            tax = 12500 + (income - 500000) * 0.20
        else:
            tax = 112500 + (income - 1000000) * 0.30
    
    cess = tax * 0.03
    total_tax = tax + cess
    
    return {
        'tax': tax,
        'cess': cess,
        'total': total_tax,
        'after_tax': income - total_tax,
        'effective_rate': total_tax / income * 100 if income > 0 else 0
    }

def calculate_emi(principal, rate, years):
    """Calculate loan EMI"""
    monthly_rate = rate / 12 / 100
    months = years * 12
    
    if monthly_rate == 0:
        emi = principal / months
    else:
        emi = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    
    total_payment = emi * months
    total_interest = total_payment - principal
    
    return {
        'emi': emi,
        'total_payment': total_payment,
        'total_interest': total_interest
    }

# ===== MAIN APP =====

# HEADER WITH ENHANCED STYLING
st.markdown("""
<div style="margin-bottom: 8px;">
    <div class="main-header">Smart Portfolio Builder</div>
    <div class="sub-header">Professional Financial Planning & Investment Analytics Platform</div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ANIMATED STATS SECTION
st.markdown("""
<style>
@keyframes fadeInScale {
    from {
        opacity: 0;
        transform: scale(0.95);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 40px;
    animation: fadeInScale 0.6s ease-out;
}

.stat-box {
    background: linear-gradient(135deg, rgba(88, 166, 255, 0.1) 0%, rgba(121, 192, 255, 0.05) 100%);
    border: 1px solid rgba(88, 166, 255, 0.2);
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.stat-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple));
}

.stat-box::after {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 50% 0%, rgba(88, 166, 255, 0.1), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.stat-box:hover {
    border-color: var(--accent-blue);
    background: linear-gradient(135deg, rgba(88, 166, 255, 0.15) 0%, rgba(121, 192, 255, 0.1) 100%);
    transform: translateY(-6px);
    box-shadow: 0 12px 30px rgba(88, 166, 255, 0.15);
}

.stat-box:hover::after {
    opacity: 1;
}

.stat-number {
    font-size: 36px;
    font-weight: 900;
    color: var(--accent-blue);
    margin-bottom: 8px;
}

.stat-label {
    font-size: 12px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}

.stat-desc {
    font-size: 11px;
    color: var(--text-secondary);
    margin-top: 8px;
    opacity: 0.8;
}
</style>

<div class="stats-grid">
    <div class="stat-box">
        <div class="stat-number">12.5 L</div>
        <div class="stat-label">Average Portfolio</div>
        <div class="stat-desc">Typical investment size managed</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">38%</div>
        <div class="stat-label">Tax Savings</div>
        <div class="stat-desc">Average annual reduction</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">2.3 Cr</div>
        <div class="stat-label">Retirement Corpus</div>
        <div class="stat-desc">Typical retirement goal</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">8.5%</div>
        <div class="stat-label">Avg Returns</div>
        <div class="stat-desc">Projected annual growth</div>
    </div>
</div>
""", unsafe_allow_html=True)

# BENEFITS SECTION
st.markdown("""
<style>
.benefits-banner {
    background: linear-gradient(135deg, rgba(88, 166, 255, 0.08) 0%, rgba(248, 113, 113, 0.05) 100%);
    border: 1px solid rgba(88, 166, 255, 0.15);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 40px;
    animation: slideUp 0.7s ease-out;
}

.benefits-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
}

.benefit-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 0;
}

.benefit-check {
    color: var(--accent-green);
    font-weight: 900;
    font-size: 20px;
}

.benefit-text {
    font-size: 13px;
    color: var(--text-primary);
    font-weight: 500;
}
</style>

<div class="benefits-banner">
    <div class="benefits-grid">
        <div class="benefit-item">
            <div class="benefit-check">+</div>
            <div class="benefit-text">Instant Accurate Results</div>
        </div>
        <div class="benefit-item">
            <div class="benefit-check">+</div>
            <div class="benefit-text">India Tax Specific</div>
        </div>
        <div class="benefit-item">
            <div class="benefit-check">+</div>
            <div class="benefit-text">100% Free Forever</div>
        </div>
        <div class="benefit-item">
            <div class="benefit-check">+</div>
            <div class="benefit-text">No Sign-up Required</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ENHANCED TOOLS SECTION
st.markdown("""
<h3 class='main-header' style='margin-top: 0px; margin-bottom: 16px;'>Powerful Financial Tools</h3>
""", unsafe_allow_html=True)

st.markdown("<div class='spacer-lg'></div>", unsafe_allow_html=True)

# CTA SECTION - MOVED BEFORE TOOLS
st.markdown("""
<style>
.cta-section {
    background: linear-gradient(135deg, rgba(88, 166, 255, 0.12) 0%, rgba(248, 113, 113, 0.08) 100%);
    border: 1px solid rgba(88, 166, 255, 0.2);
    border-radius: 14px;
    padding: 40px;
    text-align: center;
    margin-bottom: 40px;
    animation: slideUp 0.9s ease-out;
    position: relative;
    overflow: hidden;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
}

.cta-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at center, rgba(88, 166, 255, 0.05), transparent);
    pointer-events: none;
}

.cta-content {
    position: relative;
    z-index: 1;
}

.cta-headline {
    font-size: 28px;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 12px;
}

.cta-subtext {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 24px;
    line-height: 1.6;
}
</style>

<div class="cta-section">
    <div class="cta-content">
        <div class="cta-headline">Start Planning Your Financial Future</div>
        <div class="cta-subtext">Use our powerful calculators to make informed investment decisions and achieve your goals</div>
    </div>
</div>
""", unsafe_allow_html=True)

# TRUST SECTION - MOVED BEFORE TOOLS
st.markdown("""
<style>
.trust-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 12px;
    margin-bottom: 40px;
    animation: slideUp 1s ease-out;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
}

.trust-item {
    background: linear-gradient(135deg, rgba(88, 166, 255, 0.08), transparent);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 16px;
    text-align: center;
    transition: all 0.3s ease;
}

.trust-item:hover {
    border-color: var(--accent-blue);
    background: linear-gradient(135deg, rgba(88, 166, 255, 0.12), transparent);
}

.trust-icon {
    font-size: 28px;
    margin-bottom: 8px;
}

.trust-label {
    font-size: 11px;
    color: var(--text-secondary);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.trust-value {
    font-size: 16px;
    color: var(--accent-blue);
    font-weight: 700;
    margin-top: 4px;
}
</style>

<div class="trust-grid">
    <div class="trust-item">
        <div class="trust-icon">✓</div>
        <div class="trust-label">Instant</div>
        <div class="trust-value">Results</div>
    </div>
    <div class="trust-item">
        <div class="trust-icon">✓</div>
        <div class="trust-label">Accurate</div>
        <div class="trust-value">Math</div>
    </div>
    <div class="trust-item">
        <div class="trust-icon">✓</div>
        <div class="trust-label">India</div>
        <div class="trust-value">Focused</div>
    </div>
    <div class="trust-item">
        <div class="trust-icon">✓</div>
        <div class="trust-label">Always</div>
        <div class="trust-value">Free</div>
    </div>
    <div class="trust-item">
        <div class="trust-icon">✓</div>
        <div class="trust-label">No Sign</div>
        <div class="trust-value">Up</div>
    </div>
    <div class="trust-item">
        <div class="trust-icon">✓</div>
        <div class="trust-label">Mobile</div>
        <div class="trust-value">Ready</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='spacer-lg'></div>", unsafe_allow_html=True)

# TABS FOR ALL CALCULATORS - MOVED BEFORE TOOLS
st.markdown("""
<h3 class='main-header' style='text-align: center; margin-bottom: 24px;'>Our Calculators</h3>
<div class="divider" style='max-width: 300px; margin-left: auto; margin-right: auto;'></div>

<style>
.stTabs [data-baseweb="tab-list"] {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin: 0 auto;
}

.stTabs [data-baseweb="tab"] {
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.08), transparent) !important;
    border: 1px solid rgba(168, 85, 247, 0.2) !important;
    border-radius: 8px !important;
    padding: 14px 28px !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    transition: all 0.3s ease !important;
    min-width: auto !important;
}

.stTabs [data-baseweb="tab"]:hover {
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.15), rgba(168, 85, 247, 0.05)) !important;
    border-color: #a855f7 !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.25), rgba(168, 85, 247, 0.1)) !important;
    border-color: #a855f7 !important;
    box-shadow: 0 4px 12px rgba(168, 85, 247, 0.2) !important;
}

.stTabs [aria-selected="true"] span {
    color: #a855f7 !important;
}
</style>
<div class='spacer-lg'></div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Portfolio", "SIP", "Retirement", "Tax", "EMI", "Mutual Funds"
])

# ===== TAB 1: PORTFOLIO CALCULATOR =====
with tab1:
    st.markdown("<h3 class='main-header'>Portfolio Allocation Calculator</h3>", unsafe_allow_html=True)
    
    # Center the content
    col_spacer1, col_main, col_spacer2 = st.columns([0.5, 2, 0.5])
    
    with col_main:
        st.markdown("<h4 style='color: var(--text-primary); margin-bottom: 16px; text-align: center;'>Your Details</h4>", unsafe_allow_html=True)
        
        income = st.number_input("Monthly Income (Rs)", min_value=10000, value=50000, step=1000, key="port_income")
        expenses = st.number_input("Monthly Expenses (Rs)", min_value=0, value=30000, step=1000, key="port_exp")
        initial = st.number_input("Initial Investment (Rs)", min_value=0, value=100000, step=10000, key="port_init")
        monthly = st.number_input("Monthly Investment (Rs)", min_value=0, value=5000, step=1000, key="port_mon")
        horizon = st.slider("Investment Horizon (Years)", 1, 50, 10, key="port_hor")
        risk = st.slider("Risk Profile", 0, 20, 10, key="port_risk")
        
        if st.button("Calculate Portfolio", use_container_width=True, key="btn_port"):
            st.session_state.portfolio_calc = True
        
        if st.session_state.get('portfolio_calc', False):
            if income <= expenses:
                st.markdown("""
                    <div class="alert alert-danger">
                    Income must be greater than expenses
                    </div>
                """, unsafe_allow_html=True)
            else:
                profile = get_risk_profile(risk)
                monthly_save = income - expenses
                annual_save = monthly_save * 12
                
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Your Profile</div>
                        <div style="font-size: 16px; color: var(--accent-blue); font-weight: 600; margin-top: 8px; text-align: center;">{profile['name']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Monthly Saving</div>
                            <div class="metric-value">{format_currency(monthly_save)}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col_b:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Annual Saving</div>
                            <div class="metric-value">{format_currency(annual_save)}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                fig = go.Figure(data=[go.Pie(
                    labels=list(profile['allocation'].keys()),
                    values=list(profile['allocation'].values()),
                    marker=dict(colors=['#58a6ff', '#3fb950', '#f6ad55', '#79c0ff']),
                )])
                fig.update_layout(
                    height=350, 
                    showlegend=True,
                    paper_bgcolor='rgba(22, 27, 34, 0)',
                    font=dict(color='#c9d1d9', size=12)
                )
                st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='spacer-lg'></div>", unsafe_allow_html=True)

# POWERFUL FINANCIAL TOOLS SECTION - NOW AT THE END
st.markdown("""
<h3 class='main-header' style='text-align: center;'>Powerful Financial Tools</h3>
<div class="divider" style='max-width: 300px; margin-left: auto; margin-right: auto;'></div>
""", unsafe_allow_html=True)

# Define tool cards in Python, then render them
tools_data = [
    {
        "icon": "P",
        "title": "Portfolio Optimizer",
        "desc": "Smart allocation based on risk tolerance with multi-scenario analysis",
        "features": ["Risk-based allocation", "Equity & Debt mix", "Gold & Cash balance"]
    },
    {
        "icon": "S",
        "title": "SIP Calculator",
        "desc": "Unlock the power of compounding with systematic investment planning",
        "features": ["Compound growth", "Return projections", "Gain analysis"]
    },
    {
        "icon": "R",
        "title": "Retirement Planner",
        "desc": "Calculate exact corpus needed and ensure long-term financial security",
        "features": ["Corpus calculation", "Inflation adjusted", "Shortfall analysis"]
    },
    {
        "icon": "T",
        "title": "Tax Optimizer",
        "desc": "Compare New vs Old tax regime and maximize your post-tax income",
        "features": ["Regime comparison", "Tax calculation", "Cess included"]
    },
    {
        "icon": "E",
        "title": "EMI Calculator",
        "desc": "Analyze loan payments and understand complete interest breakdown",
        "features": ["EMI calculation", "Interest breakdown", "Amortization view"]
    },
    {
        "icon": "M",
        "title": "Mutual Fund Analyzer",
        "desc": "Compare investment options and project returns over time",
        "features": ["Lump sum & SIP", "Return projection", "Gain analysis"]
    }
]

# Render tool cards with proper CSS styling
st.markdown("""
<style>
.tools-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 28px;
    margin-bottom: 40px;
    animation: slideUp 0.8s ease-out;
    max-width: 1100px;
    margin-left: auto;
    margin-right: auto;
}

@media (max-width: 1024px) {
    .tools-container {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .tools-container {
        grid-template-columns: 1fr;
    }
}

.tool-card {
    background: linear-gradient(135deg, var(--bg-elevated) 0%, rgba(33, 38, 45, 0.5) 100%);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 32px;
    transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    position: relative;
    cursor: pointer;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    height: 100%;
}

.tool-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: linear-gradient(90deg, #a855f7, #d946ef, #f87171);
}

.tool-card::after {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at top right, rgba(168, 85, 247, 0.1), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
}

.tool-card:hover {
    border-color: #a855f7;
    transform: translateY(-8px);
    box-shadow: 0 24px 60px rgba(168, 85, 247, 0.2);
    background: linear-gradient(135deg, rgba(33, 38, 45, 0.95) 0%, rgba(168, 85, 247, 0.1) 100%);
}

.tool-card:hover::after {
    opacity: 1;
}

.tool-icon {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 16px;
    display: inline-block;
    padding: 14px 18px;
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.2), rgba(217, 70, 239, 0.1));
    border-radius: 10px;
    border: 2px solid rgba(168, 85, 247, 0.3);
    color: #a855f7;
    width: fit-content;
}

.tool-title {
    font-size: 20px;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 14px;
    letter-spacing: -0.5px;
}

.tool-desc {
    font-size: 14px;
    color: var(--text-secondary);
    line-height: 1.7;
    margin-bottom: 20px;
    flex-grow: 1;
}

.tool-features {
    font-size: 12px;
    color: var(--text-secondary);
    border-top: 2px solid rgba(168, 85, 247, 0.1);
    padding-top: 18px;
    margin-top: auto;
}

.tool-feature {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 8px 0;
    padding: 4px 0;
}

.tool-feature::before {
    content: '✓';
    color: #a855f7;
    font-weight: 800;
    font-size: 14px;
    min-width: 18px;
}
</style>

<div class="tools-container">
""", unsafe_allow_html=True)

# Render each tool card with full information
for tool in tools_data:
    features_html = "".join([f'<div class="tool-feature">{feat}</div>' for feat in tool["features"]])
    
    st.markdown(f"""
    <div class="tool-card">
        <div class="tool-icon">{tool['icon']}</div>
        <div class="tool-title">{tool['title']}</div>
        <div class="tool-desc">{tool['desc']}</div>
        <div class="tool-features">
            {features_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ===== TAB 2: SIP CALCULATOR =====
with tab2:
    st.markdown("<h3 class='main-header'>SIP Growth Calculator</h3>", unsafe_allow_html=True)
    
    col_spacer1, col_main, col_spacer2 = st.columns([0.5, 2, 0.5])
    
    with col_main:
        st.markdown("<h4 style='color: var(--text-primary); margin-bottom: 16px; text-align: center;'>Investment Details</h4>", unsafe_allow_html=True)
        monthly_sip = st.number_input("Monthly SIP (Rs)", min_value=100, value=5000, step=100, key="sip_mon")
        sip_return = st.slider("Expected Return (%) per year", 0.0, 25.0, 12.0, key="sip_ret")
        sip_years = st.slider("Investment Period (Years)", 1, 50, 10, key="sip_yrs")
        
        if st.button("Calculate SIP", use_container_width=True, key="btn_sip"):
            result = calculate_sip(monthly_sip, sip_return / 100, sip_years)
            st.session_state.sip_result = result
        
        if 'sip_result' in st.session_state:
            result = st.session_state.sip_result
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Invested</div>
                        <div class="metric-value">{format_currency(result['invested'])}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_b:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Final Value</div>
                        <div class="metric-value">{format_currency(result['final'])}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            col_c, col_d = st.columns(2)
            with col_c:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Total Gain</div>
                        <div class="metric-value">{format_currency(result['gain'])}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_d:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Gain %</div>
                        <div class="metric-value">{format_percentage(result['gain_pct'])}</div>
                    </div>
                """, unsafe_allow_html=True)

# ===== TAB 3: RETIREMENT CALCULATOR =====
with tab3:
    st.markdown("<h3 class='main-header'>Retirement Planning Calculator</h3>", unsafe_allow_html=True)
    
    col_spacer1, col_main, col_spacer2 = st.columns([0.5, 2, 0.5])
    
    with col_main:
        st.markdown("<h4 style='color: var(--text-primary); margin-bottom: 16px; text-align: center;'>Retirement Details</h4>", unsafe_allow_html=True)
        age = st.number_input("Current Age", min_value=20, value=30, step=1, key="ret_age")
        ret_age = st.number_input("Retirement Age", min_value=35, value=60, step=1, key="ret_ret_age")
        savings = st.number_input("Current Savings (Rs)", min_value=0, value=500000, step=50000, key="ret_sav")
        ret_monthly = st.number_input("Monthly Savings (Rs)", min_value=0, value=10000, step=1000, key="ret_mon")
        ret_return = st.slider("Expected Return (%) per year", 0.0, 20.0, 10.0, key="ret_ret")
        inflation = st.slider("Expected Inflation (%)", 0.0, 10.0, 5.0, key="ret_inf")
        ret_expenses = st.number_input("Monthly Expenses (Rs)", min_value=1000, value=50000, step=1000, key="ret_exp")
        
        if st.button("Calculate Retirement", use_container_width=True, key="btn_ret"):
            result = calculate_retirement(age, ret_age, savings, ret_monthly, ret_return/100, inflation/100, ret_expenses)
            st.session_state.ret_result = result
        
        if 'ret_result' in st.session_state:
            result = st.session_state.ret_result
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Corpus Needed</div>
                        <div class="metric-value">{format_currency(result['corpus_needed'])}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_b:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Projected</div>
                        <div class="metric-value">{format_currency(result['corpus_projected'])}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            status = "On Track" if result['sufficient'] else "Shortfall"
            shortfall_color = "alert-success" if result['sufficient'] else "alert-warning"
            
            st.markdown(f"""
                <div class="alert {shortfall_color}">
                {status}: {format_currency(result['shortfall']) if not result['sufficient'] else 'Your retirement is secure!'}
                </div>
            """, unsafe_allow_html=True)

# ===== TAB 4: TAX CALCULATOR =====
with tab4:
    st.markdown("<h3 class='main-header'>Income Tax Calculator (India)</h3>", unsafe_allow_html=True)
    
    col_spacer1, col_main, col_spacer2 = st.columns([0.5, 2, 0.5])
    
    with col_main:
        st.markdown("<h4 style='color: var(--text-primary); margin-bottom: 16px; text-align: center;'>Tax Details</h4>", unsafe_allow_html=True)
        tax_income = st.number_input("Annual Income (Rs)", min_value=0, value=500000, step=50000, key="tax_inc")
        tax_regime = st.radio("Tax Regime", ["New Regime (2023+)", "Old Regime"], key="tax_reg")
        regime = 'new' if 'New' in tax_regime else 'old'
        
        if st.button("Calculate Tax", use_container_width=True, key="btn_tax"):
            result = calculate_tax(tax_income, regime)
            st.session_state.tax_result = result
        
        if 'tax_result' in st.session_state:
            result = st.session_state.tax_result
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Income Tax</div>
                        <div class="metric-value">{format_currency(result['tax'])}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_b:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Total Tax</div>
                        <div class="metric-value">{format_currency(result['total'])}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            col_c, col_d = st.columns(2)
            with col_c:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">After Tax Income</div>
                        <div class="metric-value">{format_currency(result['after_tax'])}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_d:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Effective Rate</div>
                        <div class="metric-value">{format_percentage(result['effective_rate'])}</div>
                    </div>
                """, unsafe_allow_html=True)

# ===== TAB 5: EMI CALCULATOR =====
with tab5:
    st.markdown("<h3 class='main-header'>Loan EMI Calculator</h3>", unsafe_allow_html=True)
    
    col_spacer1, col_main, col_spacer2 = st.columns([0.5, 2, 0.5])
    
    with col_main:
        st.markdown("<h4 style='color: var(--text-primary); margin-bottom: 16px; text-align: center;'>Loan Details</h4>", unsafe_allow_html=True)
        principal = st.number_input("Loan Amount (Rs)", min_value=10000, value=500000, step=10000, key="emi_prin")
        interest_rate = st.number_input("Interest Rate (% per year)", min_value=0.0, value=8.0, step=0.1, key="emi_rate")
        loan_years = st.number_input("Loan Period (Years)", min_value=1, value=5, step=1, key="emi_yrs")
        
        if st.button("Calculate EMI", use_container_width=True, key="btn_emi"):
            result = calculate_emi(principal, interest_rate, loan_years)
            st.session_state.emi_result = result
        
        if 'emi_result' in st.session_state:
            result = st.session_state.emi_result
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Monthly EMI</div>
                        <div class="metric-value">{format_currency(result['emi'])}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_b:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Total Interest</div>
                        <div class="metric-value">{format_currency(result['total_interest'])}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Total Payment</div>
                    <div class="metric-value">{format_currency(result['total_payment'])}</div>
                </div>
            """, unsafe_allow_html=True)

# ===== TAB 6: MUTUAL FUND CALCULATOR =====
with tab6:
    st.markdown("<h3 class='main-header'>Mutual Fund Investment Calculator</h3>", unsafe_allow_html=True)
    
    col_spacer1, col_main, col_spacer2 = st.columns([0.5, 2, 0.5])
    
    with col_main:
        st.markdown("<h4 style='color: var(--text-primary); margin-bottom: 16px; text-align: center;'>Investment Details</h4>", unsafe_allow_html=True)
        mf_type = st.radio("Investment Type", ["Lump Sum", "SIP"], key="mf_type")
        
        if mf_type == "Lump Sum":
            mf_amount = st.number_input("Investment (Rs)", min_value=1000, value=100000, step=10000, key="mf_lump")
        else:
            mf_amount = st.number_input("Monthly Investment (Rs)", min_value=100, value=5000, step=100, key="mf_sip")
        
        mf_return = st.slider("Expected Return (%) per year", 0.0, 25.0, 12.0, key="mf_ret")
        mf_years = st.slider("Investment Period (Years)", 1, 50, 10, key="mf_yrs")
        
        if st.button("Calculate Returns", use_container_width=True, key="btn_mf"):
            if mf_type == "Lump Sum":
                months = mf_years * 12
                monthly_rate = mf_return / 100 / 12
                final = mf_amount * ((1 + monthly_rate) ** months)
                invested = mf_amount
            else:
                result_mf = calculate_sip(mf_amount, mf_return / 100, mf_years)
                final = result_mf['final']
                invested = result_mf['invested']
            
            st.session_state.mf_result = {
                'invested': invested,
                'final': final,
                'gain': final - invested,
                'gain_pct': (final - invested) / invested * 100 if invested > 0 else 0
            }
        
        if 'mf_result' in st.session_state:
            result = st.session_state.mf_result
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Amount Invested</div>
                        <div class="metric-value">{format_currency(result['invested'])}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_b:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Final Value</div>
                        <div class="metric-value">{format_currency(result['final'])}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            col_c, col_d = st.columns(2)
            with col_c:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Total Gain</div>
                        <div class="metric-value">{format_currency(result['gain'])}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_d:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Return %</div>
                        <div class="metric-value">{format_percentage(result['gain_pct'])}</div>
                    </div>
                """, unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div class="spacer-lg"></div>
<div class="footer">
    <strong>Smart Portfolio Builder</strong> - Financial Planning Platform<br>
    Made for your financial freedom<br>
    Email: raghav74dhanotiya@gmail.com | Phone: +91 9109657983
</div>
""", unsafe_allow_html=True)
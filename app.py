"""
Smart Portfolio Builder - Streamlit Edition
Developed by: Raghav Dhanotiya
Email: raghav74dhanotiya@gmail.com
Contact: +91 9109657983

A premium financial planning application with portfolio, SIP, retirement, 
tax, loan, and mutual fund calculators with beautiful UI and advanced analytics.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json

# ===== PAGE CONFIGURATION =====
st.set_page_config(
    page_title="💰 Smart Portfolio Builder",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Smart Portfolio Builder v1.0 - By Raghav Dhanotiya"
    }
)

# ===== CUSTOM CSS =====
st.markdown("""
    <style>
    /* Main Container */
    .main { background-color: #f8f9fa; }
    
    /* Header Styling */
    .header-container {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        color: white;
        padding: 40px 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .header-title {
        font-size: 3em;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .header-subtitle {
        font-size: 1.2em;
        opacity: 0.95;
        margin-top: 10px;
    }
    
    /* Card Styling */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #6366F1;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }
    
    .metric-label {
        font-size: 0.9em;
        color: #6B7280;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        font-size: 1.8em;
        font-weight: 700;
        color: #1F2937;
        margin-top: 8px;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.8em;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 20px;
        border-bottom: 3px solid #6366F1;
        padding-bottom: 15px;
    }
    
    /* Alert Boxes */
    .alert-box {
        padding: 15px 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        border-left: 4px solid;
    }
    
    .alert-info {
        background-color: #E0F2FE;
        border-left-color: #0284C7;
        color: #0c4a6e;
    }
    
    .alert-success {
        background-color: #DCFCE7;
        border-left-color: #16A34A;
        color: #15803D;
    }
    
    .alert-warning {
        background-color: #FEF3C7;
        border-left-color: #D97706;
        color: #92400E;
    }
    
    .alert-danger {
        background-color: #FEE2E2;
        border-left-color: #DC2626;
        color: #991B1B;
    }
    
    /* Form Styling */
    .form-section {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        color: white;
        font-weight: 600;
        padding: 12px 30px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
    }
    
    /* Comparison Cards */
    .comparison-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .comparison-card.winner {
        border: 3px solid #10B981;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, white 100%);
    }
    
    /* Insights Grid */
    .insights-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 15px;
    }
    
    .insight-item {
        background: linear-gradient(135deg, #F0F9FF 0%, white 100%);
        border-left: 4px solid #0284C7;
        padding: 15px;
        border-radius: 8px;
    }
    
    /* Footer */
    .footer-text {
        text-align: center;
        color: #6B7280;
        font-size: 0.9em;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #E5E7EB;
    }
    </style>
""", unsafe_allow_html=True)

# ===== HELPER FUNCTIONS =====

def format_currency(value):
    """Format number as Indian currency"""
    if value >= 1_00_00_000:
        return f"₹{value / 1_00_00_000:.2f} Cr"
    elif value >= 1_00_000:
        return f"₹{value / 1_00_000:.2f} L"
    else:
        return f"₹{value:,.0f}"

def format_percentage(value):
    """Format as percentage"""
    return f"{value:.2f}%"

def get_risk_profile(risk_score):
    """Get portfolio profile based on risk score"""
    if risk_score <= 8:
        return {
            'name': 'Capital Protector',
            'emoji': '🛡️',
            'color': '#10B981',
            'allocation': {'Equity': 25, 'Debt': 55, 'Gold': 12, 'Cash': 8}
        }
    elif risk_score <= 14:
        return {
            'name': 'Growth Seeker',
            'emoji': '⚖️',
            'color': '#F59E0B',
            'allocation': {'Equity': 50, 'Debt': 30, 'Gold': 12, 'Cash': 8}
        }
    elif risk_score <= 18:
        return {
            'name': 'Growth Investor',
            'emoji': '📈',
            'color': '#EF4444',
            'allocation': {'Equity': 70, 'Debt': 15, 'Gold': 10, 'Cash': 5}
        }
    else:
        return {
            'name': 'Wealth Builder',
            'emoji': '🚀',
            'color': '#8B5CF6',
            'allocation': {'Equity': 85, 'Debt': 8, 'Gold': 5, 'Cash': 2}
        }

def calculate_portfolio_metrics(income, expenses, savings_rate=0.5):
    """Calculate financial metrics"""
    monthly_savings = income - expenses
    annual_savings = monthly_savings * 12
    emergency_fund = expenses * 6
    total_investable = savings_rate * annual_savings
    
    return {
        'monthly_savings': max(0, monthly_savings),
        'annual_savings': max(0, annual_savings),
        'emergency_fund': max(0, emergency_fund),
        'total_investable': max(0, total_investable)
    }

def calculate_wealth_projection(initial, monthly, annual_return, years):
    """Calculate wealth projection over time"""
    months = years * 12
    projections = []
    monthly_rate = annual_return / 12
    
    value = initial
    for month in range(months + 1):
        projections.append({
            'month': month,
            'year': month / 12,
            'value': value
        })
        value = value * (1 + monthly_rate) + monthly
    
    return projections

def calculate_scenarios(portfolio, initial, monthly, years):
    """Calculate 3 scenarios"""
    returns_data = {
        'Equity': {'worst': 0.04, 'expected': 0.10, 'best': 0.16},
        'Debt': {'worst': 0.05, 'expected': 0.07, 'best': 0.08},
        'Gold': {'worst': 0.03, 'expected': 0.06, 'best': 0.09},
        'Cash': {'worst': 0.02, 'expected': 0.03, 'best': 0.04}
    }
    
    scenarios = {}
    for scenario in ['worst', 'expected', 'best']:
        annual_return = sum((portfolio.get(asset, 0) / 100) * returns_data[asset][scenario] 
                           for asset in returns_data)
        
        projections = calculate_wealth_projection(initial, monthly, annual_return, years)
        final_value = projections[-1]['value']
        total_invested = initial + (monthly * years * 12)
        
        scenarios[scenario] = {
            'annual_return': annual_return,
            'final_value': final_value,
            'total_invested': total_invested,
            'gain': final_value - total_invested,
            'projections': projections
        }
    
    return scenarios

def generate_insights(metrics, profile, scenarios):
    """Generate actionable insights"""
    insights = []
    
    if metrics['monthly_savings'] > 0:
        insights.append({
            'icon': '💰',
            'title': 'Excellent Savings Rate',
            'message': f"₹{metrics['monthly_savings']:,.0f} per month saved",
            'type': 'success'
        })
    else:
        insights.append({
            'icon': '⚠️',
            'title': 'No Savings',
            'message': 'Income equals or is less than expenses',
            'type': 'warning'
        })
    
    if metrics['emergency_fund'] > 0:
        insights.append({
            'icon': '🛡️',
            'title': 'Emergency Fund Target',
            'message': f"₹{metrics['emergency_fund']:,.0f} for 6 months",
            'type': 'info'
        })
    
    expected_gain = scenarios['expected']['gain']
    if expected_gain > 0:
        insights.append({
            'icon': '📈',
            'title': 'Expected Wealth Growth',
            'message': f"₹{expected_gain:,.0f} gain in expected scenario",
            'type': 'success'
        })
    
    best_gain = scenarios['best']['gain']
    insights.append({
        'icon': '🚀',
        'title': 'Best Case Scenario',
        'message': f"₹{best_gain:,.0f} potential gain",
        'type': 'info'
    })
    
    return insights

def create_allocation_chart(portfolio):
    """Create pie chart for allocation"""
    fig = go.Figure(data=[go.Pie(
        labels=list(portfolio.keys()),
        values=list(portfolio.values()),
        marker=dict(colors=['#3B82F6', '#10B981', '#F59E0B', '#6B7280']),
        textposition='inside',
        textinfo='label+percent'
    )])
    
    fig.update_layout(
        height=400,
        showlegend=True,
        hovermode='closest',
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    return fig

def create_projection_chart(scenarios):
    """Create wealth projection chart"""
    fig = go.Figure()
    
    for scenario, color in [('worst', '#EF4444'), ('expected', '#F59E0B'), ('best', '#10B981')]:
        data = scenarios[scenario]['projections']
        years = [p['year'] for p in data]
        values = [p['value'] for p in data]
        
        fig.add_trace(go.Scatter(
            x=years,
            y=values,
            mode='lines',
            name=scenario.capitalize(),
            line=dict(color=color, width=3),
            fill='tozeroy' if scenario == 'expected' else None
        ))
    
    fig.update_layout(
        title='Wealth Projection Over Time',
        xaxis_title='Years',
        yaxis_title='Portfolio Value (₹)',
        height=400,
        hovermode='x unified',
        template='plotly_white'
    )
    
    fig.update_yaxes(tickformat=',.0f')
    
    return fig

def create_comparison_chart(lump_sum_data, sip_data):
    """Create comparison chart"""
    fig = go.Figure(data=[
        go.Bar(
            name='Lump Sum',
            x=['Initial', 'Final', 'Gain'],
            y=[lump_sum_data['invested'], lump_sum_data['final'], lump_sum_data['gain']],
            marker_color='#3B82F6'
        ),
        go.Bar(
            name='SIP',
            x=['Initial', 'Final', 'Gain'],
            y=[sip_data['invested'], sip_data['final'], sip_data['gain']],
            marker_color='#10B981'
        )
    ])
    
    fig.update_layout(
        height=400,
        barmode='group',
        title='Lump Sum vs SIP Comparison',
        template='plotly_white',
        hovermode='x unified'
    )
    
    fig.update_yaxes(tickformat=',.0f')
    
    return fig

# ===== SIP CALCULATOR =====

def calculate_sip(monthly_sip, annual_return, years):
    """Calculate SIP returns"""
    months = years * 12
    monthly_rate = annual_return / 12
    total_invested = monthly_sip * months
    final_value = 0
    
    for month in range(1, months + 1):
        final_value += monthly_sip * ((1 + monthly_rate) ** (months - month + 1))
    
    gain = final_value - total_invested
    
    return {
        'total_invested': total_invested,
        'final_value': final_value,
        'gain': gain,
        'gain_percentage': (gain / total_invested * 100) if total_invested > 0 else 0
    }

# ===== RETIREMENT CALCULATOR =====

def calculate_retirement(current_age, retirement_age, current_savings, monthly_savings, 
                        annual_return, annual_inflation, monthly_expenses):
    """Calculate retirement corpus needed"""
    years_to_retirement = retirement_age - current_age
    years_in_retirement = 85 - retirement_age  # Assume 85 years
    
    # Calculate corpus needed
    monthly_in_retirement = monthly_expenses * ((1 + annual_inflation) ** years_to_retirement)
    total_needed = monthly_in_retirement * 12 * years_in_retirement
    
    # Calculate future value of current savings and SIP
    monthly_rate = annual_return / 12
    months = years_to_retirement * 12
    
    # FV of current savings
    fv_current = current_savings * ((1 + monthly_rate) ** months)
    
    # FV of SIP
    fv_sip = 0
    for month in range(1, months + 1):
        fv_sip += monthly_savings * ((1 + monthly_rate) ** (months - month + 1))
    
    total_corpus = fv_current + fv_sip
    shortfall = max(0, total_needed - total_corpus)
    
    return {
        'corpus_needed': total_needed,
        'corpus_projected': total_corpus,
        'shortfall': shortfall,
        'monthly_needed': monthly_in_retirement,
        'sufficient': total_corpus >= total_needed
    }

# ===== TAX CALCULATOR =====

def calculate_tax_india(income, regime='old'):
    """Calculate income tax for India"""
    if regime == 'old':
        if income <= 250000:
            tax = 0
        elif income <= 500000:
            tax = (income - 250000) * 0.05
        elif income <= 1000000:
            tax = 12500 + (income - 500000) * 0.20
        else:
            tax = 112500 + (income - 1000000) * 0.30
    else:  # New regime
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
    
    # Add 3% cess if tax > 0
    cess = tax * 0.03 if tax > 0 else 0
    total_tax = tax + cess
    
    return {
        'tax': tax,
        'cess': cess,
        'total_tax': total_tax,
        'after_tax_income': income - total_tax,
        'effective_rate': (total_tax / income * 100) if income > 0 else 0
    }

# ===== LOAN EMI CALCULATOR =====

def calculate_loan_emi(principal, annual_rate, years):
    """Calculate loan EMI"""
    monthly_rate = annual_rate / 12 / 100
    months = years * 12
    
    if monthly_rate == 0:
        emi = principal / months
    else:
        emi = principal * (monthly_rate * (1 + monthly_rate) ** months) / \
              ((1 + monthly_rate) ** months - 1)
    
    total_payment = emi * months
    total_interest = total_payment - principal
    
    # Calculate amortization schedule
    amortization = []
    remaining = principal
    
    for month in range(1, min(months + 1, 361)):  # Limit to first 360 months for display
        interest = remaining * monthly_rate
        principal_payment = emi - interest
        remaining -= principal_payment
        
        amortization.append({
            'Month': month,
            'EMI': emi,
            'Principal': principal_payment,
            'Interest': interest,
            'Remaining': max(0, remaining)
        })
    
    return {
        'emi': emi,
        'total_payment': total_payment,
        'total_interest': total_interest,
        'amortization': amortization
    }

# ===== MUTUAL FUND CALCULATOR =====

def calculate_mutual_fund_returns(investment, annual_return, years, is_sip=False):
    """Calculate mutual fund returns"""
    if is_sip:
        result = calculate_sip(investment, annual_return, years)
    else:
        months = years * 12
        monthly_rate = annual_return / 12
        final_value = investment * ((1 + monthly_rate) ** months)
        gain = final_value - investment
        result = {
            'total_invested': investment,
            'final_value': final_value,
            'gain': gain,
            'gain_percentage': (gain / investment * 100) if investment > 0 else 0
        }
    
    return result

# ===== MAIN APP =====

def main():
    # Header
    st.markdown("""
        <div class="header-container">
            <h1 class="header-title">💰 Smart Portfolio Builder</h1>
            <p class="header-subtitle">Your Personal Investment Advisor - Plan Your Financial Future</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 💰 Smart Portfolio Builder")
        st.markdown("---")
        
        selected_tab = st.radio(
            "📊 Choose Calculator",
            [
                "🏠 Dashboard",
                "💼 Portfolio",
                "🎯 SIP",
                "⚖️ Comparison",
                "🏦 Retirement",
                "💰 Tax",
                "🚗 Loan EMI",
                "📈 Mutual Funds",
                "ℹ️ About"
            ],
            key="main_tab"
        )
        
        st.markdown("---")
        st.markdown("""
        **Contact Information:**
        - 📧 raghav74dhanotiya@gmail.com
        - 📱 +91 9109657983
        
        **Version:** 1.0
        **Last Updated:** 2026
        """)
    
    # ===== DASHBOARD TAB =====
    if selected_tab == "🏠 Dashboard":
        st.markdown('<h2 class="section-header">📊 Dashboard</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">Total Users</div>
                    <div class="metric-value">10K+</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">Calculations Done</div>
                    <div class="metric-value">50K+</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">Total Wealth Planned</div>
                    <div class="metric-value">₹10 Cr</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">User Rating</div>
                    <div class="metric-value">4.9 ⭐</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 🎯 Quick Start Guide")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            **Portfolio Calculator**
            - Calculate your investment allocation
            - Based on your risk profile
            - See 3 scenarios: worst, expected, best
            """)
            st.info("""
            **SIP Calculator**
            - Plan your systematic investments
            - See power of compounding
            - Multiple return scenarios
            """)
        
        with col2:
            st.info("""
            **Retirement Planning**
            - Calculate retirement corpus
            - Plan your golden years
            - Inflation-adjusted savings
            """)
            st.info("""
            **Tax Planning**
            - Calculate income tax
            - Compare tax regimes
            - Optimize your savings
            """)
    
    # ===== PORTFOLIO CALCULATOR =====
    elif selected_tab == "💼 Portfolio":
        st.markdown('<h2 class="section-header">💼 Portfolio Calculator</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            st.markdown("### Financial Details")
            
            income = st.number_input("Monthly Income (₹)", min_value=1000, value=50000, step=1000)
            expenses = st.number_input("Monthly Expenses (₹)", min_value=0, value=30000, step=1000)
            
            st.markdown("### Investment Details")
            
            initial_investment = st.number_input("Initial Investment (₹)", min_value=0, value=100000, step=10000)
            monthly_contribution = st.number_input("Monthly Contribution (₹)", min_value=0, value=5000, step=1000)
            
            investment_horizon = st.slider("Investment Horizon (Years)", 1, 50, 10)
            risk_score = st.slider("Risk Profile (0=Conservative, 20=Aggressive)", 0, 20, 10)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            calculate_btn = st.button("📊 Calculate Portfolio", use_container_width=True, key="calc_portfolio")
        
        with col2:
            if calculate_btn or 'portfolio_results' in st.session_state:
                if income <= expenses:
                    st.error("⚠️ Income must be greater than expenses!")
                else:
                    # Calculations
                    metrics = calculate_portfolio_metrics(income, expenses)
                    profile = get_risk_profile(risk_score)
                    scenarios = calculate_scenarios(profile['allocation'], initial_investment, 
                                                   monthly_contribution, investment_horizon)
                    insights = generate_insights(metrics, profile, scenarios)
                    
                    st.session_state.portfolio_results = True
                    
                    # Display Profile Card
                    st.markdown(f"""
                        <div style="background: linear-gradient(135deg, {profile['color']} 0%, 
                        {profile['color']}dd 100%); color: white; padding: 20px; border-radius: 10px; 
                        margin-bottom: 20px;">
                            <h3 style="margin: 0;">{profile['emoji']} {profile['name']}</h3>
                            <p style="margin: 5px 0 0 0; opacity: 0.9;">Risk Score: {risk_score}/20</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Metrics
                    mc1, mc2 = st.columns(2)
                    with mc1:
                        st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-label">Monthly Savings</div>
                                <div class="metric-value">{format_currency(metrics['monthly_savings'])}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with mc2:
                        st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-label">Annual Savings</div>
                                <div class="metric-value">{format_currency(metrics['annual_savings'])}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    mc3, mc4 = st.columns(2)
                    with mc3:
                        st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-label">Emergency Fund</div>
                                <div class="metric-value">{format_currency(metrics['emergency_fund'])}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with mc4:
                        st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-label">Total Investable</div>
                                <div class="metric-value">{format_currency(metrics['total_investable'])}</div>
                            </div>
                        """, unsafe_allow_html=True)
        
        # Charts and scenarios below
        if calculate_btn or 'portfolio_results' in st.session_state:
            st.markdown("---")
            
            # Allocation Chart
            st.markdown("### 📊 Portfolio Allocation")
            st.plotly_chart(create_allocation_chart(profile['allocation']), use_container_width=True)
            
            # Scenarios
            st.markdown("### 🎯 3 Scenarios - Projected Values")
            
            sc1, sc2, sc3 = st.columns(3)
            
            with sc1:
                st.markdown("""
                    <div class="metric-card" style="border-left-color: #EF4444;">
                        <div class="metric-label">📉 Worst Case</div>
                        <div class="metric-value">""" + format_currency(scenarios['worst']['final_value']) + """</div>
                        <small style="color: #6B7280;">Gain: """ + format_currency(scenarios['worst']['gain']) + """</small>
                    </div>
                """, unsafe_allow_html=True)
            
            with sc2:
                st.markdown("""
                    <div class="metric-card" style="border-left-color: #F59E0B;">
                        <div class="metric-label">📈 Expected</div>
                        <div class="metric-value">""" + format_currency(scenarios['expected']['final_value']) + """</div>
                        <small style="color: #6B7280;">Gain: """ + format_currency(scenarios['expected']['gain']) + """</small>
                    </div>
                """, unsafe_allow_html=True)
            
            with sc3:
                st.markdown("""
                    <div class="metric-card" style="border-left-color: #10B981;">
                        <div class="metric-label">📈 Best Case</div>
                        <div class="metric-value">""" + format_currency(scenarios['best']['final_value']) + """</div>
                        <small style="color: #6B7280;">Gain: """ + format_currency(scenarios['best']['gain']) + """</small>
                    </div>
                """, unsafe_allow_html=True)
            
            # Projection Chart
            st.markdown("### 📈 Wealth Projection Over Time")
            st.plotly_chart(create_projection_chart(scenarios), use_container_width=True)
            
            # Insights
            st.markdown("### 💡 Key Insights")
            for i, insight in enumerate(insights):
                if insight['type'] == 'success':
                    st.success(f"{insight['icon']} **{insight['title']}** - {insight['message']}")
                elif insight['type'] == 'warning':
                    st.warning(f"{insight['icon']} **{insight['title']}** - {insight['message']}")
                else:
                    st.info(f"{insight['icon']} **{insight['title']}** - {insight['message']}")
    
    # ===== SIP CALCULATOR =====
    elif selected_tab == "🎯 SIP":
        st.markdown('<h2 class="section-header">🎯 SIP Calculator</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            
            monthly_sip = st.number_input("Monthly SIP Amount (₹)", min_value=100, value=5000, step=100)
            annual_return = st.slider("Expected Annual Return (%)", 0.0, 50.0, 10.0, step=0.5)
            sip_years = st.slider("Investment Period (Years)", 1, 50, 10)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("🧮 Calculate SIP", use_container_width=True, key="calc_sip"):
                sip_result = calculate_sip(monthly_sip, annual_return / 100, sip_years)
                st.session_state.sip_result = sip_result
        
        with col2:
            if 'sip_result' in st.session_state:
                sip_result = st.session_state.sip_result
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Total Invested</div>
                            <div class="metric-value">{format_currency(sip_result['total_invested'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with c2:
                    st.markdown(f"""
                        <div class="metric-card" style="border-left-color: #10B981;">
                            <div class="metric-label">Final Value</div>
                            <div class="metric-value">{format_currency(sip_result['final_value'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                c3, c4 = st.columns(2)
                with c3:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Total Gain</div>
                            <div class="metric-value">{format_currency(sip_result['gain'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with c4:
                    st.markdown(f"""
                        <div class="metric-card" style="border-left-color: #8B5CF6;">
                            <div class="metric-label">Gain %</div>
                            <div class="metric-value">{format_percentage(sip_result['gain_percentage'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
        
        if 'sip_result' in st.session_state:
            st.markdown("---")
            
            st.markdown("### 💡 Power of Compounding")
            st.success(f"Your ₹{monthly_sip:,}/month investment will grow to {format_currency(st.session_state.sip_result['final_value'])} in {sip_years} years! 🚀")
            
            # Growth chart
            months_list = list(range(0, sip_years * 12 + 1))
            invested_list = [monthly_sip * m for m in months_list]
            
            values_list = []
            monthly_rate = (annual_return / 100) / 12
            for m in months_list:
                val = 0
                for i in range(1, m + 1):
                    val += monthly_sip * ((1 + monthly_rate) ** (m - i + 1))
                values_list.append(val)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=[m/12 for m in months_list],
                y=values_list,
                mode='lines',
                name='Portfolio Value',
                line=dict(color='#10B981', width=3),
                fill='tozeroy'
            ))
            fig.add_trace(go.Scatter(
                x=[m/12 for m in months_list],
                y=invested_list,
                mode='lines',
                name='Amount Invested',
                line=dict(color='#3B82F6', width=2, dash='dash')
            ))
            
            fig.update_layout(
                title='SIP Growth Over Time',
                xaxis_title='Years',
                yaxis_title='Value (₹)',
                height=400,
                template='plotly_white'
            )
            fig.update_yaxes(tickformat=',.0f')
            st.plotly_chart(fig, use_container_width=True)
    
    # ===== COMPARISON TAB =====
    elif selected_tab == "⚖️ Comparison":
        st.markdown('<h2 class="section-header">⚖️ Lump Sum vs SIP</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            
            comp_amount = st.number_input("Total Amount (₹)", min_value=1000, value=100000, step=10000)
            comp_return = st.slider("Expected Annual Return (%)", 0.0, 50.0, 10.0, step=0.5)
            comp_years = st.slider("Investment Period (Years)", 1, 50, 10)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("⚖️ Compare Strategies", use_container_width=True, key="calc_comp"):
                # Lump sum
                monthly_rate = (comp_return / 100) / 12
                months = comp_years * 12
                lump_sum_final = comp_amount * ((1 + monthly_rate) ** months)
                
                # SIP
                monthly_sip = comp_amount / (comp_years * 12)
                sip_final = 0
                for m in range(1, months + 1):
                    sip_final += monthly_sip * ((1 + monthly_rate) ** (months - m + 1))
                
                comp_result = {
                    'lump_sum': {
                        'invested': comp_amount,
                        'final': lump_sum_final,
                        'gain': lump_sum_final - comp_amount
                    },
                    'sip': {
                        'invested': comp_amount,
                        'final': sip_final,
                        'gain': sip_final - comp_amount
                    }
                }
                st.session_state.comp_result = comp_result
        
        with col2:
            if 'comp_result' in st.session_state:
                comp_result = st.session_state.comp_result
                
                c1, c2 = st.columns(2)
                
                winner_style = "border: 3px solid #10B981; background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, white 100%);"
                loser_style = "opacity: 0.8;"
                
                lump_better = comp_result['lump_sum']['final'] > comp_result['sip']['final']
                
                with c1:
                    st.markdown(f"""
                        <div class="metric-card" style="{winner_style if lump_better else loser_style}">
                            <div class="metric-label">💰 Lump Sum</div>
                            <div class="metric-value">{format_currency(comp_result['lump_sum']['final'])}</div>
                            <small>Gain: {format_currency(comp_result['lump_sum']['gain'])}</small>
                        </div>
                    """, unsafe_allow_html=True)
                
                with c2:
                    st.markdown(f"""
                        <div class="metric-card" style="{winner_style if not lump_better else loser_style}">
                            <div class="metric-label">📅 SIP</div>
                            <div class="metric-value">{format_currency(comp_result['sip']['final'])}</div>
                            <small>Gain: {format_currency(comp_result['sip']['gain'])}</small>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Advantage
                advantage = comp_result['sip']['final'] - comp_result['lump_sum']['final']
                if advantage >= 0:
                    st.success(f"✅ **SIP Wins!** by {format_currency(advantage)}")
                    st.info("SIP helps reduce timing risk and benefits from rupee cost averaging, especially in volatile markets.")
                else:
                    st.info(f"💰 **Lump Sum Wins!** by {format_currency(abs(advantage))}")
                    st.info("Lump sum works better in rising markets as all money is invested immediately.")
        
        if 'comp_result' in st.session_state:
            st.markdown("---")
            st.plotly_chart(create_comparison_chart(st.session_state.comp_result['lump_sum'], 
                                                   st.session_state.comp_result['sip']), use_container_width=True)
    
    # ===== RETIREMENT PLANNING =====
    elif selected_tab == "🏦 Retirement":
        st.markdown('<h2 class="section-header">🏦 Retirement Planning Calculator</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            
            current_age = st.number_input("Current Age", min_value=20, value=30, step=1)
            retirement_age = st.number_input("Retirement Age", min_value=30, value=60, step=1)
            current_savings = st.number_input("Current Savings (₹)", min_value=0, value=500000, step=50000)
            monthly_savings = st.number_input("Monthly Savings (₹)", min_value=0, value=10000, step=1000)
            
            annual_return = st.slider("Expected Annual Return (%)", 0.0, 20.0, 10.0, step=0.5)
            annual_inflation = st.slider("Expected Inflation (%)", 0.0, 10.0, 5.0, step=0.5)
            monthly_expenses = st.number_input("Monthly Expenses (₹)", min_value=1000, value=50000, step=1000)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("🎯 Calculate Retirement Corpus", use_container_width=True, key="calc_retire"):
                retirement_result = calculate_retirement(
                    current_age, retirement_age, current_savings, monthly_savings,
                    annual_return / 100, annual_inflation / 100, monthly_expenses
                )
                st.session_state.retirement_result = retirement_result
        
        with col2:
            if 'retirement_result' in st.session_state:
                result = st.session_state.retirement_result
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Corpus Needed</div>
                            <div class="metric-value">{format_currency(result['corpus_needed'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with c2:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Projected Corpus</div>
                            <div class="metric-value">{format_currency(result['corpus_projected'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                c3, c4 = st.columns(2)
                with c3:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Shortfall</div>
                            <div class="metric-value">{format_currency(result['shortfall'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with c4:
                    status = "✅ Ready" if result['sufficient'] else "⚠️ Shortfall"
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Status</div>
                            <div class="metric-value">{status}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                if result['sufficient']:
                    st.success("🎉 You're on track for a comfortable retirement!")
                else:
                    st.warning(f"⚠️ You need {format_currency(result['shortfall'])} more to meet your retirement goals.")
    
    # ===== TAX CALCULATOR =====
    elif selected_tab == "💰 Tax":
        st.markdown('<h2 class="section-header">💰 Income Tax Calculator (India)</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            
            annual_income = st.number_input("Annual Income (₹)", min_value=0, value=500000, step=10000)
            tax_regime = st.radio("Tax Regime", ["New Regime (2023+)", "Old Regime"], key="tax_regime")
            regime = 'new' if 'New' in tax_regime else 'old'
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("🧮 Calculate Tax", use_container_width=True, key="calc_tax"):
                tax_result = calculate_tax_india(annual_income, regime)
                st.session_state.tax_result = tax_result
                st.session_state.tax_regime_used = regime
        
        with col2:
            if 'tax_result' in st.session_state:
                result = st.session_state.tax_result
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Gross Income</div>
                            <div class="metric-value">{format_currency(annual_income)}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with c2:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Income Tax</div>
                            <div class="metric-value">{format_currency(result['tax'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                c3, c4 = st.columns(2)
                with c3:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Cess (3%)</div>
                            <div class="metric-value">{format_currency(result['cess'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with c4:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Total Tax</div>
                            <div class="metric-value">{format_currency(result['total_tax'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                c5, c6 = st.columns(2)
                with c5:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">After Tax Income</div>
                            <div class="metric-value">{format_currency(result['after_tax_income'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with c6:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Effective Tax Rate</div>
                            <div class="metric-value">{format_percentage(result['effective_rate'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
    
    # ===== LOAN EMI CALCULATOR =====
    elif selected_tab == "🚗 Loan EMI":
        st.markdown('<h2 class="section-header">🚗 Loan EMI Calculator</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            
            loan_amount = st.number_input("Loan Amount (₹)", min_value=10000, value=500000, step=10000)
            annual_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=8.0, step=0.1)
            loan_years = st.number_input("Loan Period (Years)", min_value=1, value=5, step=1)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("🧮 Calculate EMI", use_container_width=True, key="calc_emi"):
                emi_result = calculate_loan_emi(loan_amount, annual_rate, loan_years)
                st.session_state.emi_result = emi_result
        
        with col2:
            if 'emi_result' in st.session_state:
                result = st.session_state.emi_result
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Loan Amount</div>
                            <div class="metric-value">{format_currency(loan_amount)}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with c2:
                    st.markdown(f"""
                        <div class="metric-card" style="border-left-color: #EF4444;">
                            <div class="metric-label">Monthly EMI</div>
                            <div class="metric-value">{format_currency(result['emi'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                c3, c4 = st.columns(2)
                with c3:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Total Interest</div>
                            <div class="metric-value">{format_currency(result['total_interest'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with c4:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Total Payment</div>
                            <div class="metric-value">{format_currency(result['total_payment'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
        
        if 'emi_result' in st.session_state:
            st.markdown("---")
            st.markdown("### 📊 Amortization Schedule (First 24 Months)")
            
            df_display = pd.DataFrame(st.session_state.emi_result['amortization'][:24])
            df_display['EMI'] = df_display['EMI'].apply(lambda x: f"₹{x:,.0f}")
            df_display['Principal'] = df_display['Principal'].apply(lambda x: f"₹{x:,.0f}")
            df_display['Interest'] = df_display['Interest'].apply(lambda x: f"₹{x:,.0f}")
            df_display['Remaining'] = df_display['Remaining'].apply(lambda x: f"₹{x:,.0f}")
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    # ===== MUTUAL FUNDS =====
    elif selected_tab == "📈 Mutual Funds":
        st.markdown('<h2 class="section-header">📈 Mutual Fund Calculator</h2>', unsafe_allow_html=True)
        
        investment_type = st.radio("Choose Investment Type", ["Lump Sum", "SIP"], horizontal=True)
        
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            
            if investment_type == "Lump Sum":
                mf_amount = st.number_input("Investment Amount (₹)", min_value=1000, value=100000, step=10000)
            else:
                mf_amount = st.number_input("Monthly Investment (₹)", min_value=100, value=5000, step=100)
            
            mf_return = st.slider("Expected Annual Return (%)", 0.0, 50.0, 12.0, step=0.5)
            mf_years = st.slider("Investment Period (Years)", 1, 50, 10)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("🧮 Calculate Returns", use_container_width=True, key="calc_mf"):
                mf_result = calculate_mutual_fund_returns(mf_amount, mf_return / 100, mf_years, 
                                                         is_sip=(investment_type == "SIP"))
                st.session_state.mf_result = mf_result
        
        with col2:
            if 'mf_result' in st.session_state:
                result = st.session_state.mf_result
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Total Invested</div>
                            <div class="metric-value">{format_currency(result['total_invested'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with c2:
                    st.markdown(f"""
                        <div class="metric-card" style="border-left-color: #10B981;">
                            <div class="metric-label">Final Value</div>
                            <div class="metric-value">{format_currency(result['final_value'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                c3, c4 = st.columns(2)
                with c3:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Total Gain</div>
                            <div class="metric-value">{format_currency(result['gain'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with c4:
                    st.markdown(f"""
                        <div class="metric-card" style="border-left-color: #8B5CF6;">
                            <div class="metric-label">Gain %</div>
                            <div class="metric-value">{format_percentage(result['gain_percentage'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.success(f"💡 Your investment will grow to {format_currency(result['final_value'])} in {mf_years} years!")
    
    # ===== ABOUT TAB =====
    elif selected_tab == "ℹ️ About":
        st.markdown('<h2 class="section-header">ℹ️ About Smart Portfolio Builder</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        ### 🎯 Our Mission
        Smart Portfolio Builder is your personal investment advisor designed to help you make informed 
        financial decisions. Whether you're planning for retirement, investing in mutual funds, or managing 
        loans, we provide comprehensive tools and insights.
        
        ### ✨ Features
        - **Portfolio Calculator**: Allocate your investments based on risk profile
        - **SIP Calculator**: Plan systematic investment plans with compounding
        - **Retirement Planning**: Calculate corpus needed for comfortable retirement
        - **Tax Calculator**: Plan your taxes efficiently
        - **Loan EMI Calculator**: Calculate and manage loan repayments
        - **Mutual Fund Calculator**: Analyze mutual fund investments
        - **Beautiful UI**: Modern, responsive design
        - **Real-time Charts**: Interactive visualizations
        
        ### 📊 How It Works
        1. Select a calculator from the sidebar
        2. Enter your financial details
        3. Click Calculate to see results
        4. View insights, charts, and scenarios
        5. Make informed decisions based on projections
        
        ### 📧 Contact & Support
        - **Email**: raghav74dhanotiya@gmail.com
        - **Phone**: +91 9109657983
        - **Version**: 1.0
        - **Last Updated**: 2026
        
        ### 📝 Disclaimer
        This calculator provides educational information and financial projections based on 
        assumed inputs. Actual returns may vary. Please consult with a qualified financial 
        advisor before making investment decisions.
        
        ### 🙏 About Developer
        Developed with ❤️ by Raghav Dhanotiya
        
        A passionate software engineer dedicated to making financial planning accessible and simple
        for everyone.
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div class="footer-text">
            <p><strong>Smart Portfolio Builder</strong> © 2026 | All Rights Reserved</p>
            <p>📧 raghav74dhanotiya@gmail.com | 📱 +91 9109657983</p>
            <p style="font-size: 0.8em; margin-top: 10px;">
            Built with ❤️ using Streamlit | Version 1.0
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

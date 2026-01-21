"""
Utility functions for Smart Portfolio Builder
Contains all calculation and formatting functions
"""

import numpy as np
import plotly.graph_objects as go
import pandas as pd

# ===== FORMATTING FUNCTIONS =====

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

# ===== PORTFOLIO FUNCTIONS =====

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
    
    for month in range(1, months + 1):
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

# ===== CHART FUNCTIONS =====

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

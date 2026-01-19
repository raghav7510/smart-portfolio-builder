"""
Smart Portfolio Builder
Developed by: Raghav Dhanotiya
Email: raghav74dhanotiya@gmail.com
Contact: +91 9109657983

A modern web application for personal investment portfolio planning
with beautiful UI/UX and powerful financial calculations.
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime
from functools import wraps
import logging
import os

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'), 
            static_folder=os.path.join(BASE_DIR, 'static'))

# ===== LOGGING & ERROR HANDLING =====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_input(**constraints):
    """Decorator to validate input parameters"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.json or {}
            errors = []
            
            for param, (min_val, max_val) in constraints.items():
                value = data.get(param)
                if value is not None:
                    try:
                        num_value = float(value)
                        if num_value < min_val:
                            errors.append(f"{param} must be >= {min_val}")
                        elif num_value > max_val:
                            errors.append(f"{param} must be <= {max_val}")
                    except (ValueError, TypeError):
                        errors.append(f"{param} must be a valid number")
            
            if errors:
                return jsonify({'success': False, 'errors': errors}), 400
            return f(*args, **kwargs)
        return wrapper
    return decorator

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'success': False, 'error': 'Invalid request'}), 400

@app.errorhandler(500)
def server_error(error):
    logger.error(f"Server error: {error}")
    return jsonify({'success': False, 'error': 'Server error'}), 500

# ===== PORTFOLIO CALCULATIONS =====

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

def get_portfolio_allocation(risk_score):
    """Get allocation based on risk score (0-20)"""
    allocations = {
        'Conservative': {'Equity': 25, 'Debt': 55, 'Gold': 12, 'Cash': 8},
        'Balanced': {'Equity': 50, 'Debt': 30, 'Gold': 12, 'Cash': 8},
        'Aggressive': {'Equity': 70, 'Debt': 15, 'Gold': 10, 'Cash': 5},
        'Maximum Growth': {'Equity': 85, 'Debt': 8, 'Gold': 5, 'Cash': 2}
    }
    
    if risk_score <= 8:
        profile = 'Conservative'
        emoji = '🛡️'
        title = 'Capital Protector'
        color = '#10B981'
    elif risk_score <= 14:
        profile = 'Balanced'
        emoji = '⚖️'
        title = 'Growth Seeker'
        color = '#F59E0B'
    elif risk_score <= 18:
        profile = 'Aggressive'
        emoji = '📈'
        title = 'Growth Investor'
        color = '#EF4444'
    else:
        profile = 'Maximum Growth'
        emoji = '🚀'
        title = 'Wealth Builder'
        color = '#8B5CF6'
    
    return {
        'profile': profile,
        'emoji': emoji,
        'title': title,
        'color': color,
        'allocation': allocations[profile]
    }

def calculate_wealth_projection(initial_investment, monthly_contribution, annual_return, years):
    """Calculate wealth projection over time"""
    monthly_rate = annual_return / 12
    projections = []
    
    value = initial_investment
    for month in range(0, years * 12 + 1):
        projections.append({
            'month': month,
            'year': round(month / 12, 2),
            'value': round(value, 2)
        })
        value = value * (1 + monthly_rate) + monthly_contribution
    
    return projections

def calculate_scenarios(portfolio, initial_investment, monthly_contribution, years):
    """Calculate 3 scenarios: worst, expected, best"""
    returns_data = {
        'Equity': {'worst': 0.04, 'expected': 0.10, 'best': 0.16},
        'Debt': {'worst': 0.05, 'expected': 0.07, 'best': 0.08},
        'Gold': {'worst': 0.03, 'expected': 0.06, 'best': 0.09},
        'Cash': {'worst': 0.02, 'expected': 0.03, 'best': 0.04}
    }
    
    scenarios = {'worst': 0, 'expected': 0, 'best': 0}
    
    for asset, weight in portfolio.items():
        for scenario in scenarios:
            scenarios[scenario] += (weight / 100) * returns_data[asset][scenario]
    
    results = {}
    for scenario, annual_return in scenarios.items():
        projections = calculate_wealth_projection(initial_investment, monthly_contribution, annual_return, years)
        final_value = projections[-1]['value']
        results[scenario] = {
            'annual_return': round(scenarios[scenario] * 100, 2),
            'final_value': round(final_value, 2),
            'total_invested': round(initial_investment + (monthly_contribution * years * 12), 2),
            'gain': round(final_value - (initial_investment + (monthly_contribution * years * 12)), 2),
            'projections': projections
        }
    
    return results

def generate_insights(metrics, profile, scenarios):
    """Generate actionable insights from calculations"""
    insights = []
    
    if metrics['monthly_savings'] > 0:
        insights.append({
            'type': 'positive',
            'title': 'Good Savings Rate',
            'message': f"₹{int(metrics['monthly_savings'])} monthly",
            'icon': '💰'
        })
    else:
        insights.append({
            'type': 'warning',
            'title': 'No Savings',
            'message': 'Income ≤ Expenses',
            'icon': '⚠️'
        })
    
    emergency = metrics['emergency_fund']
    if emergency > 0:
        insights.append({
            'type': 'info',
            'title': 'Emergency Fund',
            'message': f"₹{int(emergency)} (6 months)",
            'icon': '🛡️'
        })
    
    best_case = scenarios['best']['final_value']
    expected = scenarios['expected']['final_value']
    insights.append({
        'type': 'projection',
        'title': 'Wealth Growth',
        'message': f"₹{int(expected)} expected",
        'icon': '📈'
    })
    
    return insights

# ===== ROUTES =====

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Railway"""
    return jsonify({'status': 'healthy'}), 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
@validate_input(
    income=(1000, 50000000),
    expenses=(0, 50000000),
    initial_investment=(0, 100000000),
    monthly_contribution=(0, 1000000),
    investment_horizon=(1, 50),
    risk_score=(0, 20)
)
def calculate():
    """Main calculation endpoint"""
    try:
        data = request.json
        
        monthly_income = float(data.get('income', 50000))
        monthly_expenses = float(data.get('expenses', 30000))
        initial_investment = float(data.get('initial_investment', 100000))
        monthly_contribution = float(data.get('monthly_contribution', 5000))
        investment_horizon = int(data.get('investment_horizon', 10))
        risk_score = int(data.get('risk_score', 10))
        custom_allocation = data.get('custom_allocation', None)
        
        if monthly_income <= monthly_expenses:
            return jsonify({
                'success': False,
                'error': 'Income must be greater than expenses'
            }), 400
        
        metrics = calculate_portfolio_metrics(monthly_income, monthly_expenses)
        profile_data = get_portfolio_allocation(risk_score)
        portfolio = custom_allocation if custom_allocation else profile_data['allocation']
        scenarios = calculate_scenarios(portfolio, initial_investment, monthly_contribution, investment_horizon)
        insights = generate_insights(metrics, profile_data, scenarios)
        
        return jsonify({
            'success': True,
            'metrics': metrics,
            'profile': profile_data,
            'portfolio': portfolio,
            'scenarios': scenarios,
            'insights': insights,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Calculation error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/sip-calculator', methods=['POST'])
@validate_input(
    monthly_sip=(100, 10000000),
    annual_return=(0, 1),
    years=(1, 50)
)
def sip_calculator():
    """SIP calculator endpoint"""
    try:
        data = request.json
        monthly_sip = float(data.get('monthly_sip', 5000))
        annual_return = float(data.get('annual_return', 0.10))
        years = int(data.get('years', 10))
        
        monthly_rate = annual_return / 12
        total_invested = monthly_sip * years * 12
        final_value = 0
        
        for month in range(1, years * 12 + 1):
            final_value += monthly_sip * ((1 + monthly_rate) ** (years * 12 - month + 1))
        
        gain = final_value - total_invested
        
        return jsonify({
            'success': True,
            'monthly_sip': monthly_sip,
            'months': years * 12,
            'total_invested': round(total_invested, 2),
            'final_value': round(final_value, 2),
            'gain': round(gain, 2),
            'gain_percentage': round((gain / total_invested) * 100, 2) if total_invested > 0 else 0,
        })
    except Exception as e:
        logger.error(f"SIP calculation error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/comparison', methods=['POST'])
@validate_input(
    amount=(1000, 100000000),
    annual_return=(0, 1),
    years=(1, 50)
)
def comparison():
    """Compare lump sum vs SIP"""
    try:
        data = request.json
        amount = float(data.get('amount', 100000))
        annual_return = float(data.get('annual_return', 0.10))
        years = int(data.get('years', 10))
        
        lump_sum_final = amount * ((1 + annual_return) ** years)
        
        monthly_sip = amount / (years * 12)
        monthly_rate = annual_return / 12
        sip_final = 0
        
        for month in range(1, years * 12 + 1):
            sip_final += monthly_sip * ((1 + monthly_rate) ** (years * 12 - month + 1))
        
        sip_advantage = sip_final - lump_sum_final
        
        return jsonify({
            'success': True,
            'lump_sum': {
                'invested': round(amount, 2),
                'final': round(lump_sum_final, 2),
                'gain': round(lump_sum_final - amount, 2)
            },
            'sip': {
                'invested': round(amount, 2),
                'final': round(sip_final, 2),
                'gain': round(sip_final - amount, 2)
            },
            'sip_advantage': round(sip_advantage, 2),
            'better_strategy': 'SIP' if sip_advantage > 0 else 'Lump Sum',
        })
    except Exception as e:
        logger.error(f"Comparison error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)

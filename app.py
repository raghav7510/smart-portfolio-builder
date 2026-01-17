from flask import Flask, render_template, request, jsonify
import numpy as np
from datetime import datetime
from functools import wraps
import logging

app = Flask(__name__)

# ===== LOGGING & ERROR HANDLING =====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_input(**constraints):
    """Decorator to validate input parameters"""from flask import Flask, render_template, request, jsonify
import numpy as np
from datetime import datetime
from functools import wraps
import logging

app = Flask(__name__)

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
    elif risk_score <= 14:
        profile = 'Balanced'
        emoji = '⚖️'
        title = 'Growth Seeker'
    elif risk_score <= 18:
        profile = 'Aggressive'
        emoji = '📈'
        title = 'Growth Investor'
    else:
        profile = 'Maximum Growth'
        emoji = '🚀'
        title = 'Wealth Builder'
    
    return {
        'profile': profile,
        'emoji': emoji,
        'title': title,
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
            'year': month / 12,
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
    
    # Savings insights
    if metrics['monthly_savings'] > 0:
        insights.append({
            'type': 'positive',
            'title': '💰 Good Savings Rate',
            'message': f"You can save ₹{int(metrics['monthly_savings'])} monthly",
            'action': 'Optimize your portfolio with this amount'
        })
    else:
        insights.append({
            'type': 'warning',
            'title': '⚠️ No Savings',
            'message': 'Your expenses exceed income',
            'action': 'Reduce expenses or increase income'
        })
    
    # Emergency fund insights
    emergency = metrics['emergency_fund']
    if emergency > 0:
        insights.append({
            'type': 'info',
            'title': '🛡️ Emergency Fund Target',
            'message': f"Build ₹{int(emergency)} (6 months expenses)",
            'action': 'Keep this in liquid investments'
        })
    
    # Profile insights
    insights.append({
        'type': 'profile',
        'title': f"{profile['emoji']} {profile['title']}",
        'message': f"Your risk profile: {profile['profile']}",
        'action': f"Allocation: {', '.join([f'{k} {v}%' for k, v in scenarios.items()])}"
    })
    
    # Growth insights
    best_case = scenarios['best']['final_value']
    expected = scenarios['expected']['final_value']
    insights.append({
        'type': 'projection',
        'title': '📈 Wealth Growth',
        'message': f"Expected: ₹{int(expected)} | Best case: ₹{int(best_case)}",
        'action': 'Stay invested and maintain discipline'
    })
    
    return insights

# ===== ROUTES =====

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
    """Main calculation endpoint with validation"""
    try:
        data = request.json
        
        # Extract inputs with validation
        monthly_income = float(data.get('income', 50000))
        monthly_expenses = float(data.get('expenses', 30000))
        initial_investment = float(data.get('initial_investment', 100000))
        monthly_contribution = float(data.get('monthly_contribution', 5000))
        investment_horizon = int(data.get('investment_horizon', 10))
        risk_score = int(data.get('risk_score', 10))
        custom_allocation = data.get('custom_allocation', None)
        
        # Validate logical constraints
        if monthly_income <= monthly_expenses:
            return jsonify({
                'success': False,
                'error': 'Income must be greater than expenses',
                'suggestion': 'Adjust your monthly expenses'
            }), 400
        
        # Calculate financial metrics
        metrics = calculate_portfolio_metrics(monthly_income, monthly_expenses)
        
        # Get portfolio profile
        profile_data = get_portfolio_allocation(risk_score)
        portfolio = custom_allocation if custom_allocation else profile_data['allocation']
        
        # Calculate scenarios
        scenarios = calculate_scenarios(portfolio, initial_investment, monthly_contribution, investment_horizon)
        
        # Add helpful insights
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

@app.route('/api/allocation-breakdown', methods=['POST'])
def allocation_breakdown():
    """Get detailed allocation breakdown"""
    data = request.json
    portfolio = data.get('portfolio', {})
    
    asset_details = {
        'Equity': {
            'color': '#3B82F6',
            'description': 'Stocks and equity funds',
            'risk': 'High',
            'return': '8-16% annually',
            'examples': 'NSE, BSE stocks, equity mutual funds'
        },
        'Debt': {
            'color': '#10B981',
            'description': 'Bonds and fixed income',
            'risk': 'Low',
            'return': '5-8% annually',
            'examples': 'Government securities, bonds'
        },
        'Gold': {
            'color': '#F59E0B',
            'description': 'Precious metals',
            'risk': 'Moderate',
            'return': '3-9% annually',
            'examples': 'Gold ETF, sovereign gold bonds'
        },
        'Cash': {
            'color': '#6B7280',
            'description': 'Liquid reserves',
            'risk': 'Very Low',
            'return': '2-4% annually',
            'examples': 'Savings account, money market'
        }
    }
    
    breakdown = []
    for asset, weight in portfolio.items():
        details = asset_details.get(asset, {})
        breakdown.append({
            'asset': asset,
            'weight': weight,
            'color': details.get('color'),
            'description': details.get('description'),
            'risk': details.get('risk'),
            'return': details.get('return'),
            'examples': details.get('examples')
        })
    
    return jsonify({'breakdown': breakdown})

@app.route('/api/sip-calculator', methods=['POST'])
@validate_input(
    monthly_sip=(100, 10000000),
    annual_return=(0, 1),
    years=(1, 50)
)
def sip_calculator():
    """SIP (Systematic Investment Plan) calculator with validation"""
    try:
        data = request.json
        monthly_sip = float(data.get('monthly_sip', 5000))
        annual_return = float(data.get('annual_return', 0.10))
        years = int(data.get('years', 10))
        
        monthly_rate = annual_return / 12
        total_invested = monthly_sip * years * 12
        final_value = 0
        
        # Calculate SIP future value
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
            'power_of_compounding': round(gain, 2)
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
    """Compare lump sum vs SIP with validation"""
    try:
        data = request.json
        amount = float(data.get('amount', 100000))
        annual_return = float(data.get('annual_return', 0.10))
        years = int(data.get('years', 10))
        
        # Lump sum
        lump_sum_final = amount * ((1 + annual_return) ** years)
        
        # SIP (same total invested over time)
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
            'recommendation': 'SIP is better for risk-averse investors' if sip_advantage >= 0 else 'Lump sum performs better in rising markets'
        })
    except Exception as e:
        logger.error(f"Comparison error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)

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
    elif risk_score <= 14:
        profile = 'Balanced'
        emoji = '⚖️'
        title = 'Growth Seeker'
    elif risk_score <= 18:
        profile = 'Aggressive'
        emoji = '📈'
        title = 'Growth Investor'
    else:
        profile = 'Maximum Growth'
        emoji = '🚀'
        title = 'Wealth Builder'
    
    return {
        'profile': profile,
        'emoji': emoji,
        'title': title,
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
            'year': month / 12,
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
    
    # Savings insights
    if metrics['monthly_savings'] > 0:
        insights.append({
            'type': 'positive',
            'title': '💰 Good Savings Rate',
            'message': f"You can save ₹{int(metrics['monthly_savings'])} monthly",
            'action': 'Optimize your portfolio with this amount'
        })
    else:
        insights.append({
            'type': 'warning',
            'title': '⚠️ No Savings',
            'message': 'Your expenses exceed income',
            'action': 'Reduce expenses or increase income'
        })
    
    # Emergency fund insights
    emergency = metrics['emergency_fund']
    if emergency > 0:
        insights.append({
            'type': 'info',
            'title': '🛡️ Emergency Fund Target',
            'message': f"Build ₹{int(emergency)} (6 months expenses)",
            'action': 'Keep this in liquid investments'
        })
    
    # Profile insights
    insights.append({
        'type': 'profile',
        'title': f"{profile['emoji']} {profile['title']}",
        'message': f"Your risk profile: {profile['profile']}",
        'action': f"Allocation: {', '.join([f'{k} {v}%' for k, v in scenarios.items()])}"
    })
    
    # Growth insights
    best_case = scenarios['best']['final_value']
    expected = scenarios['expected']['final_value']
    insights.append({
        'type': 'projection',
        'title': '📈 Wealth Growth',
        'message': f"Expected: ₹{int(expected)} | Best case: ₹{int(best_case)}",
        'action': 'Stay invested and maintain discipline'
    })
    
    return insights

# ===== ROUTES =====

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
    """Main calculation endpoint with validation"""
    try:
        data = request.json
        
        # Extract inputs with validation
        monthly_income = float(data.get('income', 50000))
        monthly_expenses = float(data.get('expenses', 30000))
        initial_investment = float(data.get('initial_investment', 100000))
        monthly_contribution = float(data.get('monthly_contribution', 5000))
        investment_horizon = int(data.get('investment_horizon', 10))
        risk_score = int(data.get('risk_score', 10))
        custom_allocation = data.get('custom_allocation', None)
        
        # Validate logical constraints
        if monthly_income <= monthly_expenses:
            return jsonify({
                'success': False,
                'error': 'Income must be greater than expenses',
                'suggestion': 'Adjust your monthly expenses'
            }), 400
        
        # Calculate financial metrics
        metrics = calculate_portfolio_metrics(monthly_income, monthly_expenses)
        
        # Get portfolio profile
        profile_data = get_portfolio_allocation(risk_score)
        portfolio = custom_allocation if custom_allocation else profile_data['allocation']
        
        # Calculate scenarios
        scenarios = calculate_scenarios(portfolio, initial_investment, monthly_contribution, investment_horizon)
        
        # Add helpful insights
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

@app.route('/api/allocation-breakdown', methods=['POST'])
def allocation_breakdown():
    """Get detailed allocation breakdown"""
    data = request.json
    portfolio = data.get('portfolio', {})
    
    asset_details = {
        'Equity': {
            'color': '#3B82F6',
            'description': 'Stocks and equity funds',
            'risk': 'High',
            'return': '8-16% annually',
            'examples': 'NSE, BSE stocks, equity mutual funds'
        },
        'Debt': {
            'color': '#10B981',
            'description': 'Bonds and fixed income',
            'risk': 'Low',
            'return': '5-8% annually',
            'examples': 'Government securities, bonds'
        },
        'Gold': {
            'color': '#F59E0B',
            'description': 'Precious metals',
            'risk': 'Moderate',
            'return': '3-9% annually',
            'examples': 'Gold ETF, sovereign gold bonds'
        },
        'Cash': {
            'color': '#6B7280',
            'description': 'Liquid reserves',
            'risk': 'Very Low',
            'return': '2-4% annually',
            'examples': 'Savings account, money market'
        }
    }
    
    breakdown = []
    for asset, weight in portfolio.items():
        details = asset_details.get(asset, {})
        breakdown.append({
            'asset': asset,
            'weight': weight,
            'color': details.get('color'),
            'description': details.get('description'),
            'risk': details.get('risk'),
            'return': details.get('return'),
            'examples': details.get('examples')
        })
    
    return jsonify({'breakdown': breakdown})

@app.route('/api/sip-calculator', methods=['POST'])
@validate_input(
    monthly_sip=(100, 10000000),
    annual_return=(0, 1),
    years=(1, 50)
)
def sip_calculator():
    """SIP (Systematic Investment Plan) calculator with validation"""
    try:
        data = request.json
        monthly_sip = float(data.get('monthly_sip', 5000))
        annual_return = float(data.get('annual_return', 0.10))
        years = int(data.get('years', 10))
        
        monthly_rate = annual_return / 12
        total_invested = monthly_sip * years * 12
        final_value = 0
        
        # Calculate SIP future value
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
            'power_of_compounding': round(gain, 2)
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
    """Compare lump sum vs SIP with validation"""
    try:
        data = request.json
        amount = float(data.get('amount', 100000))
        annual_return = float(data.get('annual_return', 0.10))
        years = int(data.get('years', 10))
        
        # Lump sum
        lump_sum_final = amount * ((1 + annual_return) ** years)
        
        # SIP (same total invested over time)
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
            'recommendation': 'SIP is better for risk-averse investors' if sip_advantage >= 0 else 'Lump sum performs better in rising markets'
        })
    except Exception as e:
        logger.error(f"Comparison error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=True)


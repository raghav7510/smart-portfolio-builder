import streamlit as st
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
import numpy as np

# --------------------------------------------------
# PAGE CONFIG - PREMIUM
# --------------------------------------------------
st.set_page_config(
    page_title="Smart Portfolio Builder",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# --------------------------------------------------
# PREMIUM DESIGN SYSTEM
# --------------------------------------------------
COLORS_LIGHT = {
    "bg": "#fafbfc",
    "bg_secondary": "#f0f2f5",
    "card": "#ffffff",
    "text": "#0a0e27",
    "text_secondary": "#54586e",
    "text_muted": "#7a8196",
    "border": "#dde1e6",
    "primary": "#1e3a8a",
    "primary_light": "#3b82f6",
    "primary_lighter": "#eff6ff",
    "green": "#059669",
    "green_light": "#10b981",
    "amber": "#d97706",
    "red": "#dc2626",
    "purple": "#7c3aed",
}

COLORS_DARK = {
    "bg": "#0a0e27",
    "bg_secondary": "#141829",
    "card": "#1a1f3a",
    "text": "#f8fafc",
    "text_secondary": "#cbd5e1",
    "text_muted": "#94a3b8",
    "border": "#334155",
    "primary": "#60a5fa",
    "primary_light": "#93c5fd",
    "primary_lighter": "#0f172a",
    "green": "#10b981",
    "green_light": "#34d399",
    "amber": "#fbbf24",
    "red": "#f87171",
    "purple": "#a78bfa",
}

dark_mode = st.toggle("🌙 Dark mode", value=False)
colors = COLORS_DARK if dark_mode else COLORS_LIGHT

# Premium CSS with animations and interactions
st.markdown(f"""
<style>
/* ===== RESET & GLOBALS ===== */
* {{ margin: 0; padding: 0; box-sizing: border-box; }}

html, body, .stApp {{
    background-color: {colors['bg']};
    color: {colors['text']};
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}}

.block-container {{
    max-width: 900px;
    padding: 2rem 1.5rem;
}}

/* ===== TYPOGRAPHY ===== */
h1, h2, h3 {{
    color: {colors['text']};
    font-weight: 700;
    letter-spacing: -0.4px;
}}

h1 {{
    font-size: 2.5rem;
    line-height: 1.1;
    margin-bottom: 0.5rem;
    background: linear-gradient(135deg, {colors['primary']}, {colors['primary_light']});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

h2 {{
    font-size: 1.6rem;
    margin: 0 0 1rem 0;
    color: {colors['text']};
}}

h3 {{
    font-size: 1.15rem;
    color: {colors['text_secondary']};
}}

p {{
    color: {colors['text_secondary']};
    line-height: 1.7;
    font-size: 0.95rem;
}}

/* ===== HELPER TEXT ===== */
.helper {{
    color: {colors['text_muted']};
    font-size: 0.9rem;
    line-height: 1.6;
    margin: 0.5rem 0 1.25rem 0;
}}

/* ===== PREMIUM CARD ===== */
.card {{
    background-color: {colors['card']};
    border: 1px solid {colors['border']};
    border-radius: 20px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}}

.card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, {colors['primary']}, {colors['primary_light']});
    opacity: 0;
    transition: opacity 0.3s ease;
}}

.card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
    border-color: {colors['primary_light']};
}}

.card:hover::before {{
    opacity: 1;
}}

/* ===== STEP INDICATOR ===== */
.step-indicator {{
    display: inline-block;
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, {colors['primary']}, {colors['primary_light']});
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}}

/* ===== PREMIUM BUTTONS ===== */
.stButton > button {{
    background: linear-gradient(135deg, {colors['primary']}, {colors['primary_light']}) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
    box-shadow: 0 2px 8px rgba(30, 58, 138, 0.15) !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(30, 58, 138, 0.3) !important;
}}

.stButton > button:active {{
    transform: translateY(0) !important;
}}

/* ===== INPUTS ===== */
.stNumberInput > label {{
    color: {colors['text']} !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    margin-bottom: 0.5rem !important;
}}

.stNumberInput input {{
    border-radius: 12px !important;
    border: 2px solid {colors['border']} !important;
    color: {colors['text']} !important;
    background-color: {colors['card']} !important;
    padding: 0.85rem 1rem !important;
    transition: all 0.2s ease !important;
    font-size: 0.95rem !important;
}}

.stNumberInput input:focus {{
    border-color: {colors['primary_light']} !important;
    box-shadow: 0 0 0 3px {colors['primary_lighter']} !important;
}}

/* ===== RADIO BUTTONS ===== */
.stRadio > label {{
    color: {colors['text']} !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 0 !important;
    transition: all 0.2s ease !important;
}}

.stRadio > label:hover {{
    color: {colors['primary']} !important;
}}

/* ===== PREMIUM METRICS ===== */
.metric-card {{
    background: linear-gradient(135deg, {colors['primary_lighter']}, {colors['bg_secondary']});
    border: 2px solid {colors['border']};
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
}}

.metric-card:hover {{
    border-color: {colors['primary_light']};
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(59, 130, 246, 0.1);
}}

.metric-label {{
    color: {colors['text_muted']};
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.5rem;
}}

.metric-value {{
    color: {colors['primary']};
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
}}

.metric-subtext {{
    color: {colors['text_secondary']};
    font-size: 0.75rem;
    margin-top: 0.5rem;
}}

/* ===== PERSONA CARD ===== */
.persona {{
    background: linear-gradient(135deg, {colors['primary_lighter']}, {colors['bg_secondary']});
    padding: 2rem;
    border-radius: 16px;
    text-align: center;
    border: 2px solid {colors['border']};
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}}

.persona:hover {{
    transform: translateY(-6px);
    box-shadow: 0 15px 40px rgba(59, 130, 246, 0.15);
    border-color: {colors['primary_light']};
}}

.persona-emoji {{
    font-size: 3.5rem;
    margin-bottom: 1rem;
    animation: float 3s ease-in-out infinite;
}}

@keyframes float {{
    0%, 100% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-8px); }}
}}

.persona-title {{
    font-size: 1.4rem;
    font-weight: 800;
    color: {colors['text']};
    margin-bottom: 0.5rem;
    background: linear-gradient(135deg, {colors['primary']}, {colors['primary_light']});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

.persona-desc {{
    color: {colors['text_secondary']};
    font-size: 0.95rem;
    line-height: 1.6;
}}

/* ===== SCENARIO BOXES ===== */
.scenario {{
    text-align: center;
    padding: 1.25rem;
    border-radius: 14px;
    border: 2px solid {colors['border']};
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}}

.scenario::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, currentColor, transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}}

.scenario:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}}

.scenario-label {{
    color: {colors['text_muted']};
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.6rem;
}}

.scenario-value {{
    font-size: 1.8rem;
    font-weight: 800;
    line-height: 1;
}}

/* ===== TRUST BADGE ===== */
.trust-badge {{
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.05));
    border: 1.5px solid {colors['border']};
    border-radius: 12px;
    padding: 1rem;
    font-size: 0.85rem;
    color: {colors['text_secondary']};
    text-align: center;
    margin: 1.5rem 0;
    backdrop-filter: blur(10px);
}}

/* ===== FOOTER ===== */
.footer {{
    margin-top: 3rem;
    padding-top: 2rem;
    border-top: 2px solid {colors['border']};
    text-align: center;
    color: {colors['text_muted']};
    font-size: 0.8rem;
    line-height: 1.8;
}}

/* ===== ANIMATIONS ===== */
@keyframes slideInUp {{
    from {{
        opacity: 0;
        transform: translateY(20px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

.card {{ animation: slideInUp 0.5s ease-out forwards; }}

@keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.8; }}
}}

.pulse {{ animation: pulse 2s ease-in-out infinite; }}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {{
    .block-container {{ max-width: 100%; padding: 1rem 0.75rem; }}
    h1 {{ font-size: 2rem; }}
    h2 {{ font-size: 1.3rem; }}
    .card {{ padding: 1.5rem; margin-bottom: 1.5rem; }}
    .persona-emoji {{ font-size: 2.5rem; }}
}}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# PREMIUM HEADER
# --------------------------------------------------
st.markdown(f"""
<div style="text-align: center; margin-bottom: 2rem; padding: 2rem 0;">
    <h1>📊 Smart Portfolio Builder</h1>
    <p class="helper" style="font-size: 1.05rem; margin-top: 0.75rem;">
        Discover your ideal investment strategy in minutes. <span style="color: {colors['primary']}; font-weight: 700;">Smart. Simple. Personalized.</span>
    </p>
    <div class="trust-badge">
        🏆 AI-Powered Insights • 100% Educational • Zero Bias • Your Privacy Protected
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SECTION 1: FINANCIAL SNAPSHOT
# --------------------------------------------------
st.markdown(f'<div class="card">', unsafe_allow_html=True)
st.markdown(f'<div class="step-indicator">1</div>', unsafe_allow_html=True)
st.markdown('<h2>💰 Your Financial Snapshot</h2>', unsafe_allow_html=True)
st.markdown('<p class="helper">Let\'s understand your financial foundation. Enter your monthly income and expenses.</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    income = st.number_input(
        "📈 Monthly Income",
        min_value=0,
        step=5000,
        value=50000,
        help="Your total monthly earnings (after taxes)"
    )
with col2:
    expenses = st.number_input(
        "💸 Monthly Expenses",
        min_value=0,
        step=5000,
        value=30000,
        help="Your typical monthly spending"
    )

savings = income - expenses
emergency_fund = expenses * 6

# Display premium metrics
st.markdown("<div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 2rem;'>", unsafe_allow_html=True)

st.markdown(f"""
<div class="metric-card">
    <div class="metric-label">Monthly Surplus</div>
    <div class="metric-value" style="color: {colors['green']};"> ₹{savings:,}</div>
    <div class="metric-subtext">Available for investing</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="metric-card">
    <div class="metric-label">Emergency Fund Goal</div>
    <div class="metric-value" style="color: {colors['primary']};"> ₹{emergency_fund:,}</div>
    <div class="metric-subtext">6 months of expenses</div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

if savings < 0:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(220, 38, 38, 0.1), rgba(239, 68, 68, 0.05)); border-left: 4px solid {colors['red']}; border-radius: 12px; padding: 1.25rem; margin-top: 1.5rem;">
        <p style="color: {colors['red']}; font-weight: 700; margin: 0;">⚠️ Expenses exceed income</p>
        <p style="color: {colors['text_secondary']}; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Consider reviewing your spending to create an investment surplus.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# SECTION 2: INVESTMENT BEHAVIOR
# --------------------------------------------------
st.markdown(f'<div class="card">', unsafe_allow_html=True)
st.markdown(f'<div class="step-indicator">2</div>', unsafe_allow_html=True)
st.markdown('<h2>🎯 Your Investment Behavior</h2>', unsafe_allow_html=True)
st.markdown('<p class="helper">These questions help us understand your risk tolerance and investment personality.</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    q1 = st.radio(
        "⏱️ Investment Timeline",
        ["Less than 1 year", "1–3 years", "3–5 years", "5+ years"],
        key="q1",
        help="How long can your money stay invested?"
    )
    
    q2 = st.radio(
        "📉 Market Volatility Response",
        ["Sell everything", "Wait it out", "Buy more"],
        key="q2",
        help="If markets drop 20%, what's your move?"
    )
    
    q3 = st.radio(
        "💼 Income Stability",
        ["Unpredictable", "Fairly stable", "Very stable"],
        key="q3",
        help="How predictable is your income?"
    )

with col2:
    q4 = st.radio(
        "📚 Investment Experience",
        ["Just starting", "Some experience", "Very experienced"],
        key="q4",
        help="How comfortable are you with investing?"
    )
    
    q5 = st.radio(
        "🎪 Your Priority",
        ["Safety first", "Balance", "High growth"],
        key="q5",
        help="What matters most to you?"
    )

# Scoring
score_map = {
    "Less than 1 year": 1, "1–3 years": 2, "3–5 years": 3, "5+ years": 4,
    "Sell everything": 1, "Wait it out": 2, "Buy more": 4,
    "Unpredictable": 1, "Fairly stable": 2, "Very stable": 3,
    "Just starting": 1, "Some experience": 2, "Very experienced": 3,
    "Safety first": 1, "Balance": 2, "High growth": 3
}

score = sum([score_map[q1], score_map[q2], score_map[q3], score_map[q4], score_map[q5]])

if score <= 8:
    profile = "Conservative"
    emoji = "🛡️"
    type_name = "Capital Protector"
    desc = "You prioritize stability and preserve capital. You're comfortable with steady, predictable returns."
    profile_color = colors['green']
elif score <= 12:
    profile = "Balanced"
    emoji = "⚖️"
    type_name = "Growth Seeker"
    desc = "You balance growth with stability. Moderate risk appeals to you as you build long-term wealth."
    profile_color = colors['primary']
else:
    profile = "Growth-Focused"
    emoji = "🚀"
    type_name = "Opportunity Taker"
    desc = "You embrace market dynamics for higher returns. You're comfortable with volatility on your wealth journey."
    profile_color = colors['red']

st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# SECTION 3: INVESTOR PERSONA
# --------------------------------------------------
st.markdown(f'<div class="card">', unsafe_allow_html=True)
st.markdown(f'<div class="step-indicator">3</div>', unsafe_allow_html=True)
st.markdown('<h2>👤 Your Investor Profile</h2>', unsafe_allow_html=True)

st.markdown(f"""
<div class="persona" style="border-color: {profile_color} !important;">
    <div class="persona-emoji">{emoji}</div>
    <div class="persona-title">{type_name}</div>
    <div class="persona-desc">{desc}</div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# SECTION 4: PORTFOLIO ALLOCATION
# --------------------------------------------------
allocations = {
    "Conservative": {"Equity": 30, "Debt": 50, "Gold": 10, "Cash": 10},
    "Balanced": {"Equity": 50, "Debt": 30, "Gold": 10, "Cash": 10},
    "Growth-Focused": {"Equity": 70, "Debt": 15, "Gold": 10, "Cash": 5}
}

portfolio = allocations[profile]

st.markdown(f'<div class="card">', unsafe_allow_html=True)
st.markdown(f'<div class="step-indicator">4</div>', unsafe_allow_html=True)
st.markdown('<h2>📊 Your Optimized Portfolio</h2>', unsafe_allow_html=True)
st.markdown('<p class="helper">Based on your profile, here\'s your recommended asset allocation. This is a starting point for discussion, not financial advice.</p>', unsafe_allow_html=True)

if MATPLOTLIB_AVAILABLE:
    # Premium pie chart
    fig, ax = plt.subplots(figsize=(7, 7))
    colors_pie = [colors['primary'], colors['green'], colors['amber'], colors['text_muted']]
    
    wedges, texts, autotexts = ax.pie(
        portfolio.values(),
        labels=portfolio.keys(),
        autopct="%1.1f%%",
        startangle=90,
        colors=colors_pie,
        textprops={'color': 'white', 'weight': 'bold', 'fontsize': 11},
        wedgeprops={'edgecolor': colors['card'], 'linewidth': 2}
    )
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(11)
        autotext.set_weight('bold')
    
    ax.axis("equal")
    fig.patch.set_facecolor('none')
    
    st.pyplot(fig, use_container_width=True)

# Premium breakdown table
st.markdown("<div style='margin-top: 2rem;'>", unsafe_allow_html=True)
st.markdown(f"<p style='font-weight: 700; color: {colors['text']}; margin-bottom: 1rem;'>Asset Class Breakdown</p>", unsafe_allow_html=True)

for asset, pct in portfolio.items():
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 1rem; background-color: {colors['bg_secondary']}; border-radius: 10px; margin-bottom: 0.75rem; border-left: 4px solid {colors['primary']};">
        <span style="font-weight: 600; color: {colors['text']};">{asset}</span>
        <span style="font-weight: 800; font-size: 1.1rem; color: {colors['primary']};">{pct}%</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# SECTION 5: EXPECTED RETURNS
# --------------------------------------------------
returns = {
    "Equity": (0.04, 0.10, 0.16),
    "Debt": (0.05, 0.07, 0.08),
    "Gold": (0.03, 0.06, 0.09),
    "Cash": (0.02, 0.03, 0.04)
}

worst = expected = best = 0
for asset, weight in portfolio.items():
    w, e, b = returns[asset]
    worst += weight/100 * w
    expected += weight/100 * e
    best += weight/100 * b

st.markdown(f'<div class="card">', unsafe_allow_html=True)
st.markdown(f'<div class="step-indicator">5</div>', unsafe_allow_html=True)
st.markdown('<h2>📈 Expected Return Scenarios</h2>', unsafe_allow_html=True)
st.markdown('<p class="helper">Based on historical patterns, here are three possible 1-year return scenarios. Remember: past performance doesn\'t guarantee future results.</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="scenario" style="background: linear-gradient(135deg, rgba(220, 38, 38, 0.08), rgba(239, 68, 68, 0.04)); border-color: {colors['red']};")
        <div class="scenario-label">⚠️ Challenging</div>
        <div class="scenario-value" style="color: {colors['red']};">{worst*100:.1f}%</div>
        <p style="color: {colors['text_muted']}; font-size: 0.75rem; margin-top: 0.5rem;">Market downturn scenario</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="scenario" style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(139, 92, 246, 0.04)); border-color: {colors['primary']};")
        <div class="scenario-label">📊 Expected</div>
        <div class="scenario-value" style="color: {colors['primary']};">{expected*100:.1f}%</div>
        <p style="color: {colors['text_muted']}; font-size: 0.75rem; margin-top: 0.5rem;">Historical average</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="scenario" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.08), rgba(52, 211, 153, 0.04)); border-color: {colors['green']};")
        <div class="scenario-label">✨ Favorable</div>
        <div class="scenario-value" style="color: {colors['green']};">{best*100:.1f}%</div>
        <p style="color: {colors['text_muted']}; font-size: 0.75rem; margin-top: 0.5rem;">Bullish scenario</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER - PREMIUM
# --------------------------------------------------
st.markdown(f"""
<div class="footer">
    <p style="font-weight: 700; color: {colors['text']}; margin-bottom: 1rem;">📋 Important Disclaimer</p>
    <p>
        This is an <strong>educational tool only</strong>. It does not provide investment, tax, or financial advice. 
        The allocation and return scenarios are <strong>illustrative</strong> based on historical patterns. 
        <strong>Past performance doesn't guarantee future results.</strong> Always consult a qualified financial advisor 
        before making investment decisions.
    </p>
    <p style="margin-top: 1rem; color: {colors['text_muted']}; font-size: 0.8rem;">
        © 2026 Smart Portfolio Builder • Your Privacy is Protected • No Data Stored • Educational Use Only
    </p>
</div>
""", unsafe_allow_html=True)

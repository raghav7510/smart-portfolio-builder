import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Smart Portfolio Builder",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# DESIGN SYSTEM
# --------------------------------------------------
COLORS_LIGHT = {
    "bg": "#f8fafc",
    "card": "#ffffff",
    "text": "#0f172a",
    "text_dim": "#64748b",
    "border": "#e2e8f0",
    "primary": "#1e40af",
    "green": "#15803d",
    "amber": "#b45309",
    "red": "#b91c1c",
}

COLORS_DARK = {
    "bg": "#0f172a",
    "card": "#1e293b",
    "text": "#f1f5f9",
    "text_dim": "#94a3b8",
    "border": "#334155",
    "primary": "#3b82f6",
    "green": "#22c55e",
    "amber": "#f59e0b",
    "red": "#ef4444",
}

dark_mode = st.toggle("🌙 Dark mode")
colors = COLORS_DARK if dark_mode else COLORS_LIGHT

# Apply consistent CSS
st.markdown(f"""
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body, .stApp {{ 
    background-color: {colors['bg']};
    color: {colors['text']};
}}

.block-container {{ 
    max-width: 680px;
    padding: 1.25rem 1rem;
}}

h1, h2 {{ 
    color: {colors['text']};
    font-weight: 700;
    line-height: 1.3;
}}

h1 {{ font-size: 2rem; margin-bottom: 0.5rem; }}
h2 {{ font-size: 1.375rem; margin: 0 0 0.75rem 0; }}

p {{ color: {colors['text_dim']}; line-height: 1.6; }}
.helper {{ color: {colors['text_dim']}; font-size: 0.9rem; margin-bottom: 1rem; }}

.card {{
    background-color: {colors['card']};
    border: 1px solid {colors['border']};
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}}

.stButton > button {{
    background-color: {colors['primary']} !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.25rem !important;
    font-weight: 600 !important;
}}

.stNumberInput > label {{
    color: {colors['text']} !important;
    font-weight: 500 !important;
}}

.stNumberInput input {{
    border-radius: 8px !important;
    border: 1.5px solid {colors['border']} !important;
    color: {colors['text']} !important;
    background-color: {colors['card']} !important;
}}

.stRadio > label {{
    color: {colors['text']} !important;
    font-weight: 500;
}}

.metric {{
    background-color: rgba(30, 64, 175, 0.08);
    border: 1px solid {colors['border']};
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}}

.metric-label {{
    color: {colors['text_dim']};
    font-size: 0.85rem;
    margin-bottom: 0.3rem;
}}

.metric-value {{
    color: {colors['primary']};
    font-size: 1.5rem;
    font-weight: 700;
}}

.persona {{
    padding: 1.2rem;
    border-radius: 12px;
    text-align: center;
    border: 2px solid {colors['border']};
}}

.persona-emoji {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}}

.persona-title {{
    font-size: 1.2rem;
    font-weight: 700;
    color: {colors['text']};
    margin-bottom: 0.3rem;
}}

.persona-desc {{
    color: {colors['text_dim']};
    font-size: 0.9rem;
}}

.scenario {{
    text-align: center;
    padding: 0.9rem;
    border-radius: 10px;
    border: 1px solid {colors['border']};
}}

.trust-badge {{
    background-color: rgba(100, 116, 139, 0.1);
    border: 1px solid {colors['border']};
    border-radius: 8px;
    padding: 0.8rem;
    font-size: 0.85rem;
    color: {colors['text_dim']};
    text-align: center;
    margin-top: 1rem;
}}

.footer {{
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px solid {colors['border']};
    text-align: center;
    color: {colors['text_dim']};
    font-size: 0.85rem;
}}

@media (max-width: 600px) {{
    h1 {{ font-size: 1.5rem; }}
    h2 {{ font-size: 1.1rem; }}
}}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(f"""
<h1 style="margin: 0 0 0.5rem 0;">📊 Smart Portfolio Builder</h1>
<p class="helper">Understand your money. Build a smarter portfolio.</p>
<div class="trust-badge">📚 Educational • No advice • For learning only</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SECTION 1: YOUR FINANCES
# --------------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h2>Step 1: Your finances</h2>', unsafe_allow_html=True)
st.markdown('<p class="helper">Tell us what comes in and what goes out each month.</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    income = st.number_input("📈 Monthly income", min_value=0, step=5000)
with col2:
    expenses = st.number_input("💸 Monthly expenses", min_value=0, step=5000)

savings = income - expenses
emergency_fund = expenses * 6

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="metric">
        <div class="metric-label">Your monthly surplus</div>
        <div class="metric-value">₹{savings:,}</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric" style="background-color: rgba(21, 128, 61, 0.08); border-color: {colors['green']};">
        <div class="metric-label">Emergency fund goal</div>
        <div class="metric-value" style="color: {colors['green']};">₹{emergency_fund:,}</div>
    </div>
    """, unsafe_allow_html=True)

if savings < 0:
    st.markdown(f"""<p style="color: {colors['red']}; font-weight: 500;">💡 Expenses exceed income. Adjust to invest.</p>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# SECTION 2: YOUR INVESTMENT STYLE
# --------------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h2>Step 2: Your investment style</h2>', unsafe_allow_html=True)
st.markdown('<p class="helper">Quick questions to understand how you invest.</p>', unsafe_allow_html=True)

q1 = st.radio("How long can you keep money invested?", 
    ["Less than 1 year", "1–3 years", "3–5 years", "5+ years"], 
    key="q1")

q2 = st.radio("If markets drop 20%, you would:",
    ["Sell everything", "Wait it out", "Buy more"],
    key="q2")

q3 = st.radio("Your income is:",
    ["Unpredictable", "Fairly stable", "Very stable"],
    key="q3")

q4 = st.radio("Your investment experience:",
    ["Just starting", "Some experience", "Very experienced"],
    key="q4")

q5 = st.radio("Most important to you:",
    ["Safety first", "Balance", "High growth"],
    key="q5")

# Score
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
    desc = "You prefer steady, predictable returns."
elif score <= 12:
    profile = "Balanced"
    emoji = "⚖️"
    type_name = "Growth Seeker"
    desc = "You balance safety with growth potential."
else:
    profile = "Growth-Focused"
    emoji = "🚀"
    type_name = "Opportunity Taker"
    desc = "You're comfortable with ups and downs for higher returns."

st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# SECTION 3: YOUR PROFILE
# --------------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h2>Step 3: Your profile</h2>', unsafe_allow_html=True)

st.markdown(f"""
<div class="persona">
    <div class="persona-emoji">{emoji}</div>
    <div class="persona-title">{type_name}</div>
    <div class="persona-desc">{desc}</div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# SECTION 4: YOUR PORTFOLIO
# --------------------------------------------------
allocations = {
    "Conservative": {"Equity": 30, "Debt": 50, "Gold": 10, "Cash": 10},
    "Balanced": {"Equity": 50, "Debt": 30, "Gold": 10, "Cash": 10},
    "Growth-Focused": {"Equity": 70, "Debt": 15, "Gold": 10, "Cash": 5}
}

portfolio = allocations[profile]

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h2>Step 4: Your portfolio mix</h2>', unsafe_allow_html=True)
st.markdown('<p class="helper">How we\'d suggest spreading your investments.</p>', unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(5, 5))
colors_pie = ['#1e40af', '#15803d', '#b45309', '#64748b']
ax.pie(portfolio.values(), labels=portfolio.keys(), autopct="%1.0f%%", 
       startangle=90, colors=colors_pie, textprops={'color': 'white', 'weight': 'bold'})
ax.axis("equal")
fig.patch.set_facecolor('none')
st.pyplot(fig, use_container_width=True)

# Asset breakdown
for asset, pct in portfolio.items():
    st.markdown(f"""<p style="display: flex; justify-content: space-between; padding: 0.4rem 0;">
        <span>{asset}</span>
        <span style="font-weight: 700; color: {colors['primary']};">{pct}%</span>
    </p>""", unsafe_allow_html=True)

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

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h2>Step 5: What to expect</h2>', unsafe_allow_html=True)
st.markdown('<p class="helper">Possible 1-year returns based on history. Not guaranteed.</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="scenario" style="background-color: rgba(255, 68, 68, 0.08); border-color: {colors['red']};">
        <p style="color: {colors['text_dim']}; font-size: 0.8rem; margin: 0 0 0.3rem 0;">Challenging</p>
        <p style="color: {colors['red']}; font-size: 1.3rem; font-weight: 700; margin: 0;">{worst*100:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="scenario" style="background-color: rgba(30, 64, 175, 0.08); border-color: {colors['primary']};">
        <p style="color: {colors['text_dim']}; font-size: 0.8rem; margin: 0 0 0.3rem 0;">Expected</p>
        <p style="color: {colors['primary']}; font-size: 1.3rem; font-weight: 700; margin: 0;">{expected*100:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="scenario" style="background-color: rgba(21, 128, 61, 0.08); border-color: {colors['green']};">
        <p style="color: {colors['text_dim']}; font-size: 0.8rem; margin: 0 0 0.3rem 0;">Favorable</p>
        <p style="color: {colors['green']}; font-size: 1.3rem; font-weight: 700; margin: 0;">{best*100:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(f"""
<div class="footer">
    <p><strong>Disclaimer:</strong> This is an educational tool only. It's not investment or financial advice. 
    Past returns don't guarantee future results. Always consult a financial advisor before investing.</p>
</div>
""", unsafe_allow_html=True)

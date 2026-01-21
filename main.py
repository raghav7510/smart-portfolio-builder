"""
Smart Portfolio Builder - Streamlit Multi-Page Edition
Developed by: Raghav Dhanotiya
Email: raghav74dhanotiya@gmail.com
Contact: +91 9109657983

A premium financial planning application with portfolio, SIP, retirement, 
tax, loan, and mutual fund calculators with top-of-the-line UI and advanced analytics.
"""

import streamlit as st

# ===== PAGE CONFIGURATION =====
st.set_page_config(
    page_title="💰 Smart Portfolio Builder",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "Smart Portfolio Builder v2.0 - By Raghav Dhanotiya | Multi-Page Edition"
    }
)

# ===== ULTRA PREMIUM CUSTOM CSS =====
st.markdown("""
    <style>
    /* Root Colors */
    :root {
        --primary: #6366F1;
        --primary-light: #818CF8;
        --primary-dark: #4F46E5;
        --secondary: #8B5CF6;
        --accent: #EC4899;
        --success: #10B981;
        --warning: #F59E0B;
        --danger: #EF4444;
        --dark: #1F2937;
        --light: #F9FAFB;
        --gray: #6B7280;
    }
    
    /* Global Styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body, html {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
    }
    
    /* Main Container */
    .main {
        background: transparent;
    }
    
    /* Top Navigation Bar */
    .nav-container {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        padding: 12px 30px;
        border-radius: 0;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.15);
        margin-bottom: 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 20px;
    }
    
    .nav-title {
        color: white;
        font-size: 1.5em;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .nav-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.85em;
    }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #EC4899 100%);
        color: white;
        padding: 60px 40px;
        border-radius: 20px;
        margin-bottom: 50px;
        box-shadow: 0 20px 60px rgba(99, 102, 241, 0.25);
        text-align: center;
    }
    
    .hero-title {
        font-size: 3.5em;
        font-weight: 800;
        margin-bottom: 15px;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        font-size: 1.3em;
        opacity: 0.95;
        margin-bottom: 30px;
        line-height: 1.6;
    }
    
    /* Feature Cards Grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin-bottom: 50px;
    }
    
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 2px solid transparent;
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #6366F1, #8B5CF6, #EC4899);
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(99, 102, 241, 0.2);
        border-color: #6366F1;
    }
    
    .feature-icon {
        font-size: 2.5em;
        margin-bottom: 15px;
        display: block;
    }
    
    .feature-title {
        font-size: 1.3em;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 10px;
    }
    
    .feature-desc {
        font-size: 0.95em;
        color: #6B7280;
        line-height: 1.6;
        margin-bottom: 15px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 6px solid #6366F1;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(99, 102, 241, 0.15);
    }
    
    .metric-label {
        font-size: 0.85em;
        color: #6B7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 2em;
        font-weight: 800;
        color: #1F2937;
        background: linear-gradient(135deg, #6366F1, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Form Section */
    .form-section {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        border-left: 6px solid #6366F1;
    }
    
    .form-title {
        font-size: 1.3em;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        color: white !important;
        font-weight: 700;
        padding: 14px 40px;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        font-size: 1em;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Sections & Headers */
    .section-header {
        font-size: 2em;
        font-weight: 800;
        color: #1F2937;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .section-divider {
        height: 3px;
        background: linear-gradient(90deg, #6366F1, #8B5CF6, transparent);
        margin-bottom: 30px;
        border-radius: 2px;
    }
    
    /* Alert Boxes */
    .alert-box {
        padding: 18px 24px;
        border-radius: 12px;
        margin-bottom: 20px;
        border-left: 5px solid;
        font-weight: 500;
    }
    
    .alert-info {
        background: linear-gradient(135deg, #E0F2FE 0%, #F0F9FF 100%);
        border-left-color: #0284C7;
        color: #0c4a6e;
    }
    
    .alert-success {
        background: linear-gradient(135deg, #DCFCE7 0%, #F0FDF4 100%);
        border-left-color: #16A34A;
        color: #15803D;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #FEF3C7 0%, #FFFBEB 100%);
        border-left-color: #D97706;
        color: #92400E;
    }
    
    .alert-danger {
        background: linear-gradient(135deg, #FEE2E2 0%, #FEF2F2 100%);
        border-left-color: #DC2626;
        color: #991B1B;
    }
    
    /* Stat Grid */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }
    
    .stat-item {
        background: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-top: 4px solid #6366F1;
    }
    
    .stat-number {
        font-size: 2em;
        font-weight: 800;
        background: linear-gradient(135deg, #6366F1, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stat-label {
        font-size: 0.9em;
        color: #6B7280;
        margin-top: 5px;
        font-weight: 600;
    }
    
    /* Footer */
    .footer-container {
        background: white;
        padding: 40px 30px;
        border-radius: 15px;
        margin-top: 50px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-top: 3px solid #6366F1;
    }
    
    .footer-text {
        text-align: center;
        color: #6B7280;
        font-size: 0.95em;
        line-height: 1.8;
    }
    
    .footer-contact {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin-top: 20px;
        text-align: center;
    }
    
    .contact-item {
        color: #1F2937;
        font-weight: 600;
    }
    
    /* Gradient Text */
    .gradient-text {
        background: linear-gradient(135deg, #6366F1, #8B5CF6, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Input Styling */
    .stNumberInput > div > div > input,
    .stSlider > div > div > div > input {
        border: 2px solid #E5E7EB !important;
        border-radius: 10px !important;
        padding: 10px 12px !important;
    }
    
    .stNumberInput > div > div > input:focus,
    .stSlider > div > div > div > input:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }
    
    /* Comparison Cards */
    .comparison-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }
    
    .comparison-item {
        background: white;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
        border: 3px solid #E5E7EB;
        transition: all 0.3s ease;
    }
    
    .comparison-item.best {
        border-color: #10B981;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, white 100%);
        transform: scale(1.05);
    }
    
    .comparison-item:hover {
        box-shadow: 0 12px 30px rgba(0,0,0,0.12);
    }
    
    /* Loading Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Animations */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .slide-in {
        animation: slideIn 0.5s ease-out;
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

# ===== HOME PAGE CONTENT =====

st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">💰 Smart Portfolio Builder</h1>
        <p class="hero-subtitle">Your Personal Investment Advisor - Plan Your Financial Future with Precision & Confidence</p>
    </div>
""", unsafe_allow_html=True)

# Stat Cards
st.markdown("### 📊 Our Impact")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="stat-item">
            <div class="stat-number">10K+</div>
            <div class="stat-label">Active Users</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="stat-item">
            <div class="stat-number">50K+</div>
            <div class="stat-label">Calculations</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="stat-item">
            <div class="stat-number">₹10 Cr</div>
            <div class="stat-label">Wealth Planned</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="stat-item">
            <div class="stat-number">4.9 ⭐</div>
            <div class="stat-label">User Rating</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Feature Grid
st.markdown("### 🚀 Premium Tools & Features")
st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <span class="feature-icon">💼</span>
            <div class="feature-title">Portfolio Calculator</div>
            <div class="feature-desc">Calculate optimal investment allocation based on your risk profile with advanced scenario analysis</div>
            <small style="color: #8B5CF6; font-weight: 600;">→ Multi-scenario analysis</small>
        </div>
        
        <div class="feature-card">
            <span class="feature-icon">🎯</span>
            <div class="feature-title">SIP Calculator</div>
            <div class="feature-desc">Plan systematic investments and witness the power of compounding over time</div>
            <small style="color: #8B5CF6; font-weight: 600;">→ Real-time projections</small>
        </div>
        
        <div class="feature-card">
            <span class="feature-icon">🏦</span>
            <div class="feature-title">Retirement Planning</div>
            <div class="feature-desc">Calculate retirement corpus with inflation adjustment and ensure financial security</div>
            <small style="color: #8B5CF6; font-weight: 600;">→ Inflation-adjusted</small>
        </div>
        
        <div class="feature-card">
            <span class="feature-icon">💰</span>
            <div class="feature-title">Tax Planning</div>
            <div class="feature-desc">Compare tax regimes and optimize your tax liability with smart planning strategies</div>
            <small style="color: #8B5CF6; font-weight: 600;">→ Multiple scenarios</small>
        </div>
        
        <div class="feature-card">
            <span class="feature-icon">🚗</span>
            <div class="feature-title">Loan EMI Calculator</div>
            <div class="feature-desc">Calculate EMI, total interest, and amortization schedules for any loan</div>
            <small style="color: #8B5CF6; font-weight: 600;">→ Detailed breakdown</small>
        </div>
        
        <div class="feature-card">
            <span class="feature-icon">📈</span>
            <div class="feature-title">Mutual Fund Advisor</div>
            <div class="feature-desc">Get expert recommendations for mutual funds matching your investment goals</div>
            <small style="color: #8B5CF6; font-weight: 600;">→ Performance metrics</small>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Quick Access Section
st.markdown("### 🎯 Quick Access Calculators")
st.info("👉 Use the **sidebar menu** (☰) or **left navigation** to access all premium calculators and tools")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💼 Portfolio", "Click Sidebar", "Advanced Risk Analysis")

with col2:
    st.metric("🎯 SIP Plan", "Click Sidebar", "Compounding Power")

with col3:
    st.metric("🏦 Retirement", "Click Sidebar", "Future Planning")

st.markdown("---")

# Footer
st.markdown("""
    <div class="footer-container">
        <div class="footer-text">
            <h3 style="color: #1F2937; margin-bottom: 15px;">📞 Get in Touch</h3>
            <div class="footer-contact">
                <div class="contact-item">📧 raghav74dhanotiya@gmail.com</div>
                <div class="contact-item">📱 +91 9109657983</div>
                <div class="contact-item">🌐 Smart Portfolio v2.0</div>
            </div>
            <p style="margin-top: 30px; font-size: 0.85em; opacity: 0.8;">
                © 2026 Smart Portfolio Builder | Premium Financial Planning Platform<br>
                Built with ❤️ for Your Financial Freedom
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

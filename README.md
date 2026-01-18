# 🏦 Smart Portfolio Builder

An **amazing, modern web application** for personal investment portfolio planning with beautiful UI/UX and powerful financial calculations.

---

**Developer:** Raghav Dhanotiya  
**Email:** raghav74dhanotiya@gmail.com  
**Contact:** +91 9109657983  

---

## ✨ Features

### 💼 Portfolio Calculator
- Input your financial details (income, expenses, savings)
- Set investment horizon and risk profile
- Get personalized portfolio allocation
- View 3 scenarios (worst, expected, best)
- Beautiful wealth projection charts
- Real-time financial metrics

### 🎯 SIP Calculator
- Calculate Systematic Investment Plan returns
- See compound growth visualization
- Understand power of compounding
- View growth projections over time

### ⚖️ Lump Sum vs SIP Comparison
- Compare two investment strategies
- See which is better for your situation
- Detailed comparison metrics
- Interactive charts

### 🎨 Beautiful Interface
- 🌙 Dark/Light mode toggle
- 📊 Interactive charts with Chart.js
- 📱 Fully responsive design
- ⚡ Smooth animations
- 🎯 Intuitive navigation

## 🚀 Quick Start

### Installation

```bash
# 1. Navigate to project directory
cd "Smart Portfolio Builder"

# 2. Install dependencies
pip install -r requirements_streamlit.txt

# 3. Run the app
python app.py
```

Open browser: **http://localhost:5000**

## 📋 Project Structure

```
Smart Portfolio Builder/
├── app.py                        # Flask backend with all calculations
├── requirements_streamlit.txt    # Python dependencies (Flask, Werkzeug)
├── README.md                     # This file
├── .gitignore                    # Git ignore rules
├── templates/
│   └── index.html               # Beautiful HTML5 interface
└── static/
    ├── style.css                # Modern CSS3 with animations
    └── script.js                # Interactive JavaScript
```

## 🎨 Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js
- **Design**: Modern Glassmorphism + Gradient effects
- **Responsive**: Mobile-first design
- **Animations**: Smooth CSS transitions

## 🎯 How to Use

### 1. Portfolio Calculator
- **Step 1**: Enter your monthly income and expenses
- **Step 2**: Set your initial investment and monthly contribution
- **Step 3**: Choose investment horizon and risk level
- **Step 4**: Click "Calculate Portfolio"
- **Result**: View allocation, metrics, projections, and insights

### 2. SIP Calculator
- Enter monthly SIP amount
- Set expected annual return (%)
- Choose investment period
- See compound growth and total gains

### 3. Comparison Tool
- Set total investment amount
- Enter expected return rate
- Choose time period
- Compare Lump Sum vs SIP strategies

## 📊 Portfolio Profiles

| Profile | Risk Level | Best For |
|---------|-----------|----------|
| 🛡️ **Conservative** | 0-8 | Capital protection, stability |
| ⚖️ **Balanced** | 9-14 | Growth + stability balance |
| 📈 **Aggressive** | 15-18 | Long-term growth |
| 🚀 **Maximum Growth** | 19-20 | High growth target |

### Asset Classes & Returns

| Asset | Risk | Return | Examples |
|-------|------|--------|----------|
| **Equity** | High | 8-16% | Stocks, equity mutual funds |
| **Debt** | Low | 5-8% | Bonds, government securities |
| **Gold** | Moderate | 3-9% | Gold ETF, sovereign bonds |
| **Cash** | Very Low | 2-4% | Savings, money market |

## 🌙 Features

### Dark/Light Mode
- Click the theme toggle (moon/sun icon)
- Preference saved locally
- Reduces eye strain

### Real-Time Calculations
- Live updates as you type
- Instant financial metrics
- Dynamic charts

### Interactive Charts
- Allocation pie charts
- Wealth projection lines
- Scenario comparisons
- SIP growth visualization

## 📱 Responsive Design

- **Desktop**: Full layout with side-by-side panels
- **Tablet**: Optimized grid
- **Mobile**: Stacked, touch-friendly interface

## 🔒 Privacy & Security

- ✅ No login required
- ✅ No data stored
- ✅ No analytics tracking
- ✅ All calculations local
- ✅ Open source

## 🚀 Deploy Online (Free)

### Option 1: Render (Easiest)
1. Push to GitHub
2. Go to [render.com](https://render.com)
3. Connect GitHub repo
4. Deploy! (Free tier available)

### Option 2: Railway
1. Push to GitHub
2. Go to [railway.app](https://railway.app)
3. Select repo
4. Auto-deploys with ₹5 monthly free credit

### Option 3: PythonAnywhere
1. Go to [pythonanywhere.com](https://pythonanywhere.com)
2. Create free account
3. Upload files
4. Configure web app

## ⚠️ Important Notes

- **Educational Purpose Only** - Not actual financial advice
- **Consult Professionals** - Always speak with financial advisor
- **Past Performance** - Doesn't guarantee future results
- **Market Changes** - Returns vary with market conditions
- **Personal Circumstances** - Results depend on your situation

## 🐛 Troubleshooting

### App won't start?
```bash
# Make sure Flask is installed
pip install Flask==2.3.0

# Try different port
python app.py  # Uses 5000 by default
```

### Port 5000 in use?
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill it
taskkill /PID <PID> /F

# Or change port in app.py
```

### Charts not showing?
- Refresh page (Ctrl+F5)
- Clear browser cache
- Try different browser

## 📚 Mathematical Formulas

### Wealth Projection
```
Future Value = PV × (1 + r)^n + PMT × [((1 + r)^n - 1) / r]
```

### SIP Final Value
```
FV = PMT × [((1 + r)^n - 1) / r] × (1 + r)
```

### Emergency Fund
```
Emergency Fund = Monthly Expenses × 6
```

## 📞 Support

For issues or suggestions:
- Check README.md (this file)
- Review HTML/CSS/JS for UI issues
- Check app.py for calculation issues
- Verify all inputs are correct

## 📝 License

Free to use and modify for personal/educational purposes.

---

## 🎉 Getting Started Now

```bash
# Quick start
cd "Smart Portfolio Builder"
pip install -r requirements_streamlit.txt
python app.py
```

Visit: **http://localhost:5000**

---

**Made with ❤️ for smart investing | Investment Planning Made Easy** 🏦

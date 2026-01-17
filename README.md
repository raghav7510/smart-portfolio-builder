# 🚀 Quick Start Guide

## How to Run the App

### Step 1: Navigate to Project Directory
```bash
cd "c:\Users\ragha\OneDrive\Documents\Smart Portfolio Builder"
```

### Step 2: Install Dependencies (First Time Only)
```bash
pip install -r requirements.txt
```

### Step 3: Run the App
```bash
python app.py
```

### Step 4: Open in Browser
- Go to: **http://localhost:5000**
- App will be running on http://127.0.0.1:5000

---

## 📱 How to Use

### **Home Tab** 🏠
- Learn about portfolio building
- Understand portfolio allocation basics
- Get started with the builder

### **Portfolio Builder Tab** 🔨
1. **Enter Financial Info**
   - Monthly income
   - Monthly expenses
   - Initial investment amount
   - Monthly contribution (SIP)
   - Investment time horizon

2. **Answer Risk Quiz** (5 questions)
   - Investment timeline
   - Market reaction behavior
   - Income stability
   - Experience level
   - Financial goals

3. **View Results**
   - Your investor profile (Conservative/Balanced/Aggressive/Maximum Growth)
   - Recommended portfolio allocation
   - 3-scenario wealth projection
   - Interactive charts

### **Tools & Calculators Tab** 🛠️

#### 💡 SIP Calculator
- Calculate monthly SIP returns
- See how consistent investing grows wealth
- Understand rupee cost averaging benefits

#### ⚖️ Lump Sum vs SIP
- Compare investing ₹100,000 at once vs monthly
- See which strategy wins
- Understand SIP advantage over time

#### 📊 Inflation Calculator
- Enter investment amount and expected return
- See nominal vs real value
- Understand purchasing power impact
- Plan for inflation-adjusted goals

#### 🎯 Retirement Calculator
- Calculate retirement corpus needed
- Check if you're on track
- Based on 25× annual expenses rule
- Shows gap if any

### **Results Tab** 📈
- Your financial snapshot
- Investor profile card
- Portfolio allocation breakdown
- Wealth projection over time (3 scenarios)
- Clickable assets to learn more

---

## 🌙 Features

### Dark Mode
- Click the moon icon (🌙) in top-right
- Toggles between light and dark themes
- Your preference is saved automatically

### Real-Time Metrics
- See financial numbers update as you type
- Emergency fund calculation
- Monthly surplus display
- Investable amount updates

### Asset Education
- Click any asset in portfolio allocation
- Learn about Equity, Debt, Gold, Cash
- See investment examples
- Get pro tips

---

## 💡 Tips & Tricks

1. **Start with realistic numbers** - Use actual income/expenses for accurate results

2. **Use the Risk Quiz** - It's designed to find your true risk profile, not just numbers

3. **Check Inflation Impact** - Always view returns in "real" terms, not just nominal

4. **Compare SIP vs Lump Sum** - See why regular investing often beats lump sum

5. **Plan Retirement Early** - The earlier you start, the easier it becomes

6. **Use Dark Mode at Night** - Reduces eye strain and looks professional

7. **Click Assets** - Learn about each asset class in the modal popup

8. **Export Results** - Screenshots work great for sharing or archiving

---

## 📊 Calculator Formulas

### Monthly Surplus
```
Surplus = Income - Expenses
```

### Emergency Fund
```
Emergency Fund = Monthly Expenses × 6
```

### Wealth Projection
```
Future Value = Present Value × (1 + Rate)^Years + (Monthly Amount × [(1 + Rate)^Years - 1] / Rate)
```

### Real Return (Inflation-Adjusted)
```
Real Value = Amount × (1 + Return - Inflation)^Years
```

### Retirement Corpus
```
Corpus Needed = Annual Expenses × 25
(Based on 4% withdrawal rate)
```

---

## 🎯 Financial Goals You Can Set

1. **Emergency Fund** - Build 6 months expenses
2. **Wealth Creation** - Reach ₹50L in 10 years
3. **Retirement** - Accumulate corpus for retirement
4. **Goal Purchase** - Save for home, car, etc.
5. **Financial Freedom** - Reach financial independence

---

## ⚠️ Important Notes

- This is **EDUCATIONAL** tool only
- Not actual financial advice
- Always consult a qualified financial advisor
- Past performance ≠ Future results
- Market conditions change
- Personal circumstances vary
- Use for learning and planning

---

## 🐛 Troubleshooting

### App doesn't open?
- Make sure Python is installed
- Check if Flask is installed: `pip install Flask`
- Try a different port if 5000 is busy

### Charts not showing?
- Refresh the page (Ctrl+F5)
- Clear browser cache
- Try a different browser

### Calculations wrong?
- Double-check input values
- Make sure all fields are filled
- Try refreshing the page

---

## 📞 Support

For issues or suggestions:
- Check FEATURES.md for complete feature list
- Review this guide for common questions
- Verify all inputs are correct
- Try the app in a different browser

---

**Happy Portfolio Planning!** 🎉

Go to **http://localhost:5000** and start building your investment strategy today!

# 🌐 Web GUI Quick Start

## Launch the GUI

### Option 1: Using the launcher script (Easiest)
```bash
./run_gui.sh
```

### Option 2: Direct command
```bash
streamlit run streamlit_app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## Using the GUI

### 1️⃣ Configure Parameters (Sidebar)

**Assets**
- Choose from presets: "Gold & Silver", "Gold Only", "Silver Only", or "Custom"
- Custom mode lets you add Copper, Palladium, Platinum

**Simulation Settings**
- **Simulations**: 1K - 100K (more = smoother results)
- **Historical Data**: 1-10 years
- **Forecast Horizons**: Select multiple months (e.g., 8, 12, 16)
- **Random Seed**: For reproducibility

**Model**
- **GBM**: Standard geometric Brownian motion
- **Jump Diffusion**: Better for commodities (captures fat tails)
- **Scenario Analysis**: Compare bull/base/bear cases
- **Statistical Diagnostics**: Show parameter estimates and tests

### 2️⃣ Run Simulation

Click the big **"🚀 Run Simulation"** button

### 3️⃣ View Results

#### Summary Cards
- Current live prices
- Median forecast for each asset
- Probability of gain
- Sharpe ratio

#### Interactive Charts
- **Fan Charts**: Click and drag to zoom, hover for exact values
- **Quantile Bands**: See 5th-95th and 25th-75th percentiles
- **Terminal Distributions**: Optional histogram of final prices

#### Risk Metrics Table
- Value at Risk (VaR) 95%, 99%
- Conditional VaR (CVaR)
- Sharpe Ratio
- Maximum Drawdown
- Probability of Gain

#### Statistical Diagnostics (Expandable)
- Parameter estimates (μ, σ, correlation)
- Normality tests (Jarque-Bera)
- Jump parameters (if using jump model)
- Recommendations based on data

#### Scenario Analysis (If enabled)
- Bull/Base/Bear comparison tables
- See how results change with different assumptions

### 4️⃣ Download Results

Click **"📥 Download Risk Metrics"** buttons to save CSV files

---

## Tips for Best Results

### 🎯 Recommended Settings

**For Quick Analysis:**
- Simulations: 10,000
- Model: GBM
- Horizons: 12 months

**For Detailed Analysis:**
- Simulations: 50,000
- Model: Jump Diffusion
- Horizons: 8, 12, 16 months
- Enable: Scenario Analysis + Diagnostics

**For Long-Term Forecast:**
- Historical Data: 5 years
- Horizons: 12, 24, 36 months
- Simulations: 30,000

### 📊 Interpreting Results

**Median vs Mean**
- If Mean > Median → Positive skew (upside potential)
- If Mean < Median → Negative skew (downside risk)

**Probability of Gain**
- > 70% → Strong upward trend
- 50-70% → Moderate upward bias
- < 50% → Downward or flat trend

**Sharpe Ratio**
- \> 2.0 → Excellent risk-adjusted return
- 1.0-2.0 → Good
- 0.5-1.0 → Moderate
- < 0.5 → Poor

**VaR 95%**
- 5% chance of losing more than this amount
- Use for risk budgeting and position sizing

### 🔬 When to Use Jump Diffusion

Check **Statistical Diagnostics** after running:
- If "Normal?" shows "No" → Use Jump Diffusion
- If Kurtosis > 5 → Fat tails present
- Commodities typically have jumps

---

## GUI Features

### ✨ What Makes It Easy to Use

1. **No Command Line** - Everything in the browser
2. **Live Prices** - See current market prices at the top
3. **Interactive Charts** - Zoom, pan, hover for details
4. **Color-Coded Metrics** - Visual indicators for risk
5. **Expandable Sections** - Hide complexity when not needed
6. **Download Reports** - One-click CSV export
7. **Responsive Design** - Works on any screen size

### 🎨 Visual Design

- **Gold theme** - Professional precious metals aesthetic
- **Clean layout** - Easy to scan and understand
- **Metric cards** - Key numbers highlighted
- **Organized tabs** - Switch between assets easily

---

## Troubleshooting

**Issue**: GUI won't start
```bash
pip install streamlit
```

**Issue**: "Module not found" error
```bash
cd "/Users/murtazashakir/Coding Projects/Gold Sim"
streamlit run streamlit_app.py
```

**Issue**: Charts not loading
- Check internet connection (needs Yahoo Finance data)
- Try reducing horizons or simulations

**Issue**: Slow performance
- Reduce number of simulations
- Use fewer horizons
- Close other browser tabs

---

## Keyboard Shortcuts

While the GUI is running:
- `Ctrl+C` (in terminal) → Stop server
- Browser `F5` → Refresh page
- Browser `Ctrl+Shift+R` → Hard refresh (clear cache)

---

## Comparison: GUI vs CLI

| Feature | GUI | CLI |
|---------|-----|-----|
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Visual Appeal** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Interactivity** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Speed** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Automation** | ⭐⭐ | ⭐⭐⭐⭐⭐ |

**Use GUI when:**
- You want easy, visual analysis
- Exploring different parameters
- Presenting to others
- Learning the tool

**Use CLI when:**
- Automating analyses
- Running on server
- Batch processing
- Scripting workflows

---

## Next Steps

1. **Launch**: Run `./run_gui.sh`
2. **Explore**: Try different settings
3. **Analyze**: Run with Jump Diffusion + Scenarios
4. **Download**: Save your results
5. **Share**: Show interactive charts to colleagues

---

## Screenshots

### Main Dashboard
- Live prices at top
- Summary metrics in cards
- Interactive fan charts
- Risk metrics table
- Download buttons

### Sidebar Controls
- Asset selection with presets
- Simulation parameter sliders
- Model selection radio buttons
- One-click run button

### Charts
- Zoomable fan charts
- Hover tooltips with exact values
- Probability bands
- Start price reference line

---

**Ready to start?**

```bash
./run_gui.sh
```

Your browser will open automatically with the full-featured Monte Carlo forecaster! 🚀

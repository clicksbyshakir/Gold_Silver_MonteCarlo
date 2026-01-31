# Quick Start Guide - Enhanced Monte Carlo Simulation

## 🚀 Getting Started in 30 Seconds

### 1. Install Dependencies
```bash
pip install numpy pandas matplotlib yfinance
```

### 2. Run Basic Simulation
```bash
python Gold_Silver_MonteCarlo
```

That's it! The simulation will:
- Download 3 years of gold/silver data
- Run 20,000 simulations
- Show forecasts for 8, 12, and 16 months
- Display fan charts and risk metrics

---

## 🎯 Recommended Setup

For the best experience, install optional packages:

```bash
pip install plotly scipy pyyaml
```

Then run with recommended settings:

```bash
python Gold_Silver_MonteCarlo --model jump --interactive
```

This enables:
- ✅ Jump diffusion for realistic tail risk
- ✅ Interactive Plotly charts (zoom, hover, share)
- ✅ Statistical validation tests
- ✅ All 10 risk metrics

---

## 📊 Common Use Cases

### Use Case 1: Investment Analysis
**Goal**: Forecast gold/silver prices for next year

```bash
python Gold_Silver_MonteCarlo --horizons 12 --n-sims 30000 --interactive
```

**Look for**:
- Median forecast (50th percentile)
- Probability of gain
- VaR 95% (downside risk)

---

### Use Case 2: Risk Management
**Goal**: Calculate portfolio risk metrics

```bash
python Gold_Silver_MonteCarlo \
  --model jump \
  --horizons 8,12 \
  --output-dir ./risk_report
```

**Outputs**:
- `risk_metrics_8m.csv` - VaR, CVaR, Sharpe ratio
- `risk_metrics_12m.csv` - For longer horizon
- Fan charts showing uncertainty bands

---

### Use Case 3: Stress Testing
**Goal**: Compare bull/base/bear scenarios

```bash
python Gold_Silver_MonteCarlo \
  --scenario-analysis \
  --horizons 12 \
  --n-sims 20000
```

**See**:
- Bear case: Lower returns, higher volatility
- Base case: Historical parameters
- Bull case: Higher returns, lower volatility

---

### Use Case 4: Research & Validation
**Goal**: Validate model assumptions

```bash
python Gold_Silver_MonteCarlo \
  --model jump \
  --years 5 \
  --n-sims 50000 \
  --scenario-analysis \
  --output-dir ./research
```

**Analyze**:
- Jarque-Bera test results (normality)
- Estimated jump parameters
- Historical vs. simulated distributions

---

## 📈 Understanding the Output

### Terminal Statistics
```
Terminal Price Quantiles:
      Gold (GC=F)  Silver (SI=F)
p50       5725.10          97.31    ← Median forecast
mean      5814.42         103.55    ← Mean forecast
```

- **p50 (Median)**: Most likely outcome
- **mean**: Average across all simulations
- If mean > median: Positive skew (upside potential)

### Risk Metrics
```
Risk Metrics:
               VaR 95%  CVaR 95%  Sharpe Ratio  Prob Gain
Gold (GC=F)     262.70    509.53          1.48       90.1
```

- **VaR 95%**: 5% chance of losing more than this
- **CVaR 95%**: Average loss in worst 5% of cases
- **Sharpe Ratio**: >1 is good, >2 is excellent
- **Prob Gain**: >50% suggests upward trend

### Fan Charts

![Fan Chart Explanation](https://via.placeholder.com/600x300?text=Fan+Chart+Guide)

- **Dark blue line** = Median forecast
- **Medium blue band** = 25th-75th percentile (50% of outcomes)
- **Light blue band** = 5th-95th percentile (90% of outcomes)
- **Red dashed line** = Current price

---

## 🔧 Troubleshooting

### Issue: "Module not found"
```bash
pip install yfinance numpy pandas matplotlib
```

### Issue: No plots showing
- Make sure you're not in a headless environment
- Try adding `--output-dir ./results` to save charts

### Issue: "Plotly not available"
```bash
pip install plotly
```
Or run without `--interactive` flag (uses matplotlib)

### Issue: Download fails
- Check internet connection
- Yahoo Finance may be temporarily down
- Try reducing `--years` to 1 or 2

---

## 💡 Pro Tips

1. **Use Jump Model for Commodities**
   ```bash
   --model jump
   ```
   Gold/silver have fat tails; jump diffusion is more realistic

2. **More Simulations = Smoother Results**
   ```bash
   --n-sims 50000
   ```
   Use 50K+ for publication-quality analysis

3. **Save Your Work**
   ```bash
   --output-dir ./my_analysis_$(date +%Y%m%d)
   ```
   Saves CSV files and interactive HTML charts

4. **Check Statistical Tests**
   If Jarque-Bera p-value < 0.05, returns are non-normal → use jump model

5. **Scenario Analysis is Free**
   ```bash
   --scenario-analysis
   ```
   Always worth running to test sensitivity

---

## 📚 Learn More

- **Full Documentation**: See [README.md](file:///Users/murtazashakir/Coding%20Projects/Gold%20Sim/README.md)
- **Feature Comparison**: Run `python COMPARISON.py`
- **Implementation Details**: See [walkthrough.md](file:///Users/murtazashakir/.gemini/antigravity/brain/51d9ce7e-76d5-4b03-91a0-175c09013189/walkthrough.md)
- **Configuration Options**: Edit [config.yaml](file:///Users/murtazashakir/Coding%20Projects/Gold%20Sim/config.yaml)

---

## 🎓 Next Steps

After running your first simulation:

1. **Interpret Results**
   - Look at median forecast and probability of gain
   - Check VaR for downside risk
   - Review Sharpe ratio for risk-adjusted return

2. **Run Scenarios**
   - Add `--scenario-analysis` flag
   - Compare bull/base/bear cases
   - Understand parameter sensitivity

3. **Customize**
   - Try different `--horizons`
   - Adjust `--n-sims` for speed vs. accuracy
   - Experiment with `--years` of historical data

4. **Save Results**
   - Use `--output-dir` to save CSV and HTML files
   - Share interactive charts with stakeholders
   - Build a library of analyses over time

---

## ⚡ Command Reference

| Command | Description |
|---------|-------------|
| `python Gold_Silver_MonteCarlo` | Basic run with defaults |
| `--help` | Show all options |
| `--model jump` | Use jump diffusion model |
| `--interactive` | Interactive Plotly charts |
| `--scenario-analysis` | Bull/base/bear scenarios |
| `--n-sims 50000` | Run 50K simulations |
| `--horizons 6,12,18,24` | Custom time horizons |
| `--years 5` | Use 5 years of history |
| `--output-dir ./results` | Save outputs to folder |

---

**Ready to analyze? Start with:**

```bash
python Gold_Silver_MonteCarlo --model jump --interactive --scenario-analysis
```

This gives you the full experience with all enhanced features! 🚀

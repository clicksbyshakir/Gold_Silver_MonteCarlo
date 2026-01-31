# Gold & Silver Monte Carlo Simulation

Enhanced Monte Carlo simulation for forecasting gold and silver spot prices with advanced statistical modeling and comprehensive risk analysis.

## 🌐 NEW: Web GUI Available!

We now offer a **beautiful web interface** that makes running simulations much easier!

### Quick Start (GUI)
```bash
./run_gui.sh
```

The web app will open in your browser with:
- ✨ Intuitive controls (no command line needed)
- 📊 Interactive charts with zoom and hover
- 📈 Live price displays
- 🎨 Clean, professional design
- 💾 One-click downloads

**See [GUI_QUICKSTART.md](GUI_QUICKSTART.md) for detailed GUI instructions.**

### Quick Start (Command Line)
```bash
python Gold_Silver_MonteCarlo --model jump --interactive
```

**See below for full CLI documentation.**

---

## Features

### Core Capabilities
- **Correlated Geometric Brownian Motion (GBM)** - Standard model for asset price evolution
- **Jump Diffusion Model** - Captures extreme price movements and fat tails (Merton model)
- **Multiple Time Horizons** - Default: 8, 12, and 16 months
- **20,000 Simulation Paths** - High-quality statistical estimates

### Risk Metrics
- **Value at Risk (VaR)** - 95% and 99% confidence levels
- **Conditional VaR (CVaR)** - Expected shortfall beyond VaR
- **Sharpe Ratio** - Risk-adjusted return measure
- **Maximum Drawdown** - Worst peak-to-trough decline
- **Probability Analysis** - Likelihood of gains/losses

### Visualization
- **Interactive Fan Charts** (Plotly) - Zoom, pan, and hover for detailed insights
- **Static Fan Charts** (Matplotlib) - Publication-quality plots
- **Terminal Distribution Histograms** - Price distribution at each horizon
- **Quantile Bands** - 5th-95th and 25th-75th percentile ranges

### Analysis Tools
- **Scenario Analysis** - Bull, base, and bear market projections
- **Statistical Diagnostics** - Normality tests (Jarque-Bera), skewness, kurtosis
- **Parameter Estimation** - Automatic estimation from historical data
- **Configuration Support** - Easy parameter tuning via YAML or command-line

## Installation

### Requirements
```bash
pip install numpy pandas matplotlib yfinance
```

### Optional (for enhanced features)
```bash
pip install plotly scipy pyyaml
```

## Usage

### Basic Usage
Run with default parameters (GBM model, 8/12/16 month horizons):
```bash
python Gold_Silver_MonteCarlo
```

### With Interactive Plots
```bash
python Gold_Silver_MonteCarlo --interactive
```

### Jump Diffusion Model
```bash
python Gold_Silver_MonteCarlo --model jump --interactive
```

### With Scenario Analysis
```bash
python Gold_Silver_MonteCarlo --scenario-analysis
```

### Custom Parameters
```bash
python Gold_Silver_MonteCarlo \
  --tickers GC=F SI=F \
  --years 5 \
  --n-sims 50000 \
  --horizons 6,12,18,24 \
  --model jump \
  --interactive \
  --scenario-analysis \
  --output-dir ./my_results
```

### All Available Options
```bash
python Gold_Silver_MonteCarlo --help
```

## Command-Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--tickers` | Asset tickers (space-separated) | `GC=F SI=F` |
| `--years` | Years of historical data | `3` |
| `--n-sims` | Number of simulations | `20000` |
| `--horizons` | Forecast horizons in months (comma-separated) | `8,12,16` |
| `--model` | Model type: `gbm` or `jump` | `gbm` |
| `--interactive` | Use interactive Plotly charts | `False` |
| `--scenario-analysis` | Run bull/base/bear scenarios | `False` |
| `--output-dir` | Directory for saving outputs | `None` |

## Output

### Console Output
The simulation prints:
1. **Model Configuration** - Selected model, number of simulations, assets
2. **Historical Parameters** - Estimated drift (μ), volatility (σ), correlation
3. **Statistical Diagnostics** - Normality tests, skewness, kurtosis
4. **Jump Parameters** (if using jump model) - Jump intensity, mean, and volatility
5. **For Each Horizon:**
   - Terminal price quantiles (1st, 5th, 10th, 25th, 50th, 75th, 90th, 95th, 99th percentiles)
   - Comprehensive risk metrics table
6. **Scenario Analysis** (if enabled) - Bull/base/bear forecasts

### File Outputs (when `--output-dir` is specified)
- `summary_{horizon}m.csv` - Terminal price statistics
- `risk_metrics_{horizon}m.csv` - Risk metrics table
- `{asset}_fanchart_{horizon}m.html` - Interactive fan charts (if `--interactive`)

### Visualizations
- **Fan Charts** - Show median projection with uncertainty bands
- **Terminal Distribution** - Histogram of final prices
- **Start Price Reference** - Red dashed line showing current price

## Model Details

### Geometric Brownian Motion (GBM)
Standard model for asset prices:
```
dS_t = μ S_t dt + σ S_t dW_t
```
where:
- `μ` = drift (mean log return)
- `σ` = volatility (std dev of log returns)
- `dW_t` = correlated Brownian motion

### Jump Diffusion Model
Extends GBM with discontinuous jumps:
```
dS_t = μ S_t dt + σ S_t dW_t + J_t S_t dN_t
```
where:
- `J_t` = jump size (log-normal)
- `dN_t` = Poisson process (jump occurrence)

Jump parameters are auto-estimated from historical data by:
1. Identifying returns beyond 3 standard deviations as "jumps"
2. Estimating jump frequency (λ), mean jump size (μ_J), and jump volatility (σ_J)

### Correlation
Assets are simulated with correlated random shocks using Cholesky decomposition of the historical correlation matrix.

## Risk Metrics Explained

| Metric | Description |
|--------|-------------|
| **VaR 95%** | Maximum expected loss at 95% confidence (5% chance of worse outcome) |
| **VaR 99%** | Maximum expected loss at 99% confidence (1% chance of worse outcome) |
| **CVaR 95%** | Average loss in worst 5% of scenarios |
| **CVaR 99%** | Average loss in worst 1% of scenarios |
| **Sharpe Ratio** | Annualized return divided by annualized volatility |
| **Prob Gain** | Percentage of simulations where price increases |
| **Max Drawdown** | Average worst decline from peak across all paths |

## Scenario Analysis

The scenario analysis adjusts parameters to model different market conditions:

| Scenario | Drift Adjustment | Volatility |
|----------|-----------------|------------|
| **Bear** | μ - 0.5σ | 1.3× normal |
| **Base** | μ (historical) | 1.0× normal |
| **Bull** | μ + 0.5σ | 0.8× normal |

## Examples

### Example 1: Quick Analysis
```bash
python Gold_Silver_MonteCarlo
```
Output: Standard GBM simulation with matplotlib charts.

### Example 2: Full Analysis with All Features
```bash
python Gold_Silver_MonteCarlo \
  --model jump \
  --interactive \
  --scenario-analysis \
  --n-sims 50000 \
  --output-dir ./results
```
Output: Jump diffusion model with interactive charts, scenario analysis, and saved outputs.

### Example 3: Long-Term Forecast
```bash
python Gold_Silver_MonteCarlo \
  --horizons 12,24,36 \
  --years 5 \
  --interactive
```
Output: 1, 2, and 3-year forecasts using 5 years of historical data.

### Example 4: Single Asset (Gold Only)
```bash
python Gold_Silver_MonteCarlo \
  --tickers GC=F \
  --interactive
```
Output: Gold-only analysis.

## Configuration File (Advanced)

For repeated analyses with custom settings, you can create a `config.yaml` file. See the included `config.yaml` for all available options.

## Interpreting Results

### Fan Charts
- **Dark blue line** = Median forecast (50th percentile)
- **Medium shaded area** = 25th-75th percentile range (50% of outcomes)
- **Light shaded area** = 5th-95th percentile range (90% of outcomes)
- **Red dashed line** = Current price

### Terminal Distribution
- Shows the full distribution of possible prices at the horizon
- Useful for identifying skewness and tail risk
- Compare median vs. mean to assess asymmetry

### Risk Metrics Table
- **VaR/CVaR**: Negative values indicate potential loss
- **Sharpe Ratio**: Higher is better (>1 is good, >2 is excellent)
- **Prob Gain**: >50% suggests upward drift
- **Max Drawdown**: Negative percentage showing worst decline

## Limitations & Assumptions

1. **Historical Estimates** - Parameters are based on historical data; future may differ
2. **Constant Parameters** - Assumes drift and volatility remain constant (not GARCH)
3. **No Transaction Costs** - Pure price evolution without trading frictions
4. **Log-Normal Distribution** - Prices can't go negative (standard for commodities)
5. **No External Shocks** - Doesn't model policy changes, supply disruptions, etc.
6. **Correlation Stability** - Assumes asset correlation remains constant

## Tips for Better Results

1. **Use More History** - Set `--years 5` or more for stable parameter estimates
2. **More Simulations** - Use `--n-sims 50000` for smoother distributions
3. **Jump Model for Commodities** - Gold/silver often exhibit jumps; try `--model jump`
4. **Check Diagnostics** - If Jarque-Bera test rejects normality, consider jump model
5. **Scenario Analysis** - Always run scenarios to understand parameter sensitivity

## Troubleshooting

**Issue**: "yfinance" module not found  
**Solution**: `pip install yfinance`

**Issue**: "Plotly not available" warning  
**Solution**: `pip install plotly` for interactive charts (optional)

**Issue**: Charts not displaying  
**Solution**: Ensure you're running in an environment with display (not headless server)

**Issue**: Data download fails  
**Solution**: Check internet connection; Yahoo Finance may be temporarily unavailable

**Issue**: "SciPy not available" warning  
**Solution**: `pip install scipy` for statistical tests (optional)

## License

This code is provided as-is for educational and research purposes.

## Author

Enhanced Monte Carlo Simulation for Commodities  
Created: January 2026

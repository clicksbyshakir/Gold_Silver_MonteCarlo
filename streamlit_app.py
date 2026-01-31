#!/usr/bin/env python3
"""
Gold & Silver Monte Carlo Simulator - Web GUI
==============================================
A modern, user-friendly web interface for forecasting precious metal prices.

Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime, timedelta
import sys
import warnings
import importlib.util
warnings.filterwarnings('ignore')

# Import our simulator classes from the extensionless file
from pathlib import Path

# Load the Monte Carlo module using exec
mc_file = Path(__file__).parent / "Gold_Silver_MonteCarlo"
with open(mc_file, 'r') as f:
    mc_code = f.read()

# Create a namespace and execute the code
mc_namespace = {}
exec(mc_code, mc_namespace)

# Import classes
MonteCarloSimulator = mc_namespace['MonteCarloSimulator']
StatisticalTests = mc_namespace['StatisticalTests']


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Gold & Silver Forecaster",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main styling */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 600;
    }
    
    /* Headers */
    h1 {
        color: #1f4788;
        font-weight: 700;
        padding-bottom: 20px;
        border-bottom: 3px solid #FFD700;
    }
    
    h2 {
        color: #2c5aa0;
        font-weight: 600;
        margin-top: 30px;
    }
    
    h3 {
        color: #3d5a80;
        font-weight: 500;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1f4788;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #FFD700;
        color: #1f4788;
        font-weight: 600;
        border-radius: 8px;
        padding: 10px 24px;
        border: none;
        font-size: 16px;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #FFC700;
        box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
        transform: translateY(-2px);
    }
    
    /* Tables */
    .dataframe {
        font-size: 14px;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 8px;
    }
    
    /* Cards */
    div[data-testid="metric-container"] {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'simulation_run' not in st.session_state:
    st.session_state.simulation_run = False
if 'results' not in st.session_state:
    st.session_state.results = {}

# ============================================================================
# SIDEBAR - INPUT CONTROLS
# ============================================================================

with st.sidebar:
    st.title("⚙️ Configuration")
    
    st.markdown("---")
    
    # Asset Selection
    st.subheader("📈 Assets")
    
    preset = st.radio(
        "Select Preset",
        ["Gold & Silver", "Gold Only", "Silver Only", "Custom"],
        label_visibility="collapsed"
    )
    
    if preset == "Gold & Silver":
        selected_tickers = ["GC=F", "SI=F"]
    elif preset == "Gold Only":
        selected_tickers = ["GC=F"]
    elif preset == "Silver Only":
        selected_tickers = ["SI=F"]
    else:
        selected_tickers = st.multiselect(
            "Choose assets",
            ["GC=F", "SI=F", "HG=F", "PA=F", "PL=F"],
            default=["GC=F", "SI=F"],
            help="GC=Gold, SI=Silver, HG=Copper, PA=Palladium, PL=Platinum"
        )
    
    st.markdown("---")
    
    # Simulation Parameters
    st.subheader("🎲 Simulation")
    
    n_sims = st.select_slider(
        "Number of Simulations",
        options=[1000, 5000, 10000, 20000, 50000, 100000],
        value=20000,
        help="More simulations = smoother results but slower"
    )
    
    years_history = st.slider(
        "Years of Historical Data",
        min_value=1,
        max_value=10,
        value=3,
        help="Data used to estimate parameters"
    )
    
    horizons = st.multiselect(
        "Forecast Horizons (months)",
        [3, 6, 8, 12, 16, 18, 24, 36],
        default=[8, 12, 16],
        help="Time periods to forecast"
    )
    
    seed = st.number_input(
        "Random Seed",
        min_value=1,
        value=42,
        help="For reproducibility"
    )
    
    st.markdown("---")
    
    # Model Configuration
    st.subheader("🔬 Model")
    
    model_type = st.radio(
        "Model Type",
        ["GBM (Geometric Brownian Motion)", "Jump Diffusion (Fat Tails)"],
        help="Jump Diffusion better captures extreme events"
    )
    
    enable_scenarios = st.checkbox(
        "Enable Scenario Analysis",
        value=False,
        help="Compare Bull/Base/Bear cases"
    )
    
    show_diagnostics = st.checkbox(
        "Show Statistical Diagnostics",
        value=True,
        help="Display normality tests and parameters"
    )
    
    st.markdown("---")
    
    # Run Button
    run_simulation = st.button("🚀 Run Simulation", use_container_width=True)
    
    st.markdown("---")
    st.caption("💡 Tip: Use Jump Diffusion for commodities with fat tails")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_data(ttl=3600)
def get_current_prices(tickers):
    """Get current prices for display."""
    prices = {}
    for ticker in tickers:
        try:
            data = yf.Ticker(ticker)
            hist = data.history(period="1d")
            if not hist.empty:
                prices[ticker] = hist['Close'].iloc[-1]
            else:
                prices[ticker] = None
        except:
            prices[ticker] = None
    return prices

def create_metric_card(label, value, delta=None, delta_color="normal"):
    """Create a styled metric card."""
    return st.metric(label=label, value=value, delta=delta, delta_color=delta_color)

def create_fan_chart(paths, s0, horizon_months, label, quantiles=[0.05, 0.25, 0.50, 0.75, 0.95]):
    """Create an interactive Plotly fan chart."""
    n_steps = paths.shape[0]
    x = np.arange(1, n_steps + 1)
    
    q_vals = {q: np.quantile(paths, q, axis=1) for q in quantiles}
    
    fig = go.Figure()
    
    # Add percentile bands
    fig.add_trace(go.Scatter(
        x=x, y=q_vals[0.05],
        mode='lines', line=dict(width=0), showlegend=False,
        hovertemplate='Day %{x}<br>5th %%ile: $%{y:.2f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=x, y=q_vals[0.95],
        mode='lines', line=dict(width=0), fillcolor='rgba(68, 114, 196, 0.15)',
        fill='tonexty', name='5th-95th Percentile',
        hovertemplate='Day %{x}<br>95th %%ile: $%{y:.2f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=x, y=q_vals[0.25],
        mode='lines', line=dict(width=0), showlegend=False,
        hovertemplate='Day %{x}<br>25th %%ile: $%{y:.2f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=x, y=q_vals[0.75],
        mode='lines', line=dict(width=0), fillcolor='rgba(68, 114, 196, 0.3)',
        fill='tonexty', name='25th-75th Percentile',
        hovertemplate='Day %{x}<br>75th %%ile: $%{y:.2f}<extra></extra>'
    ))
    
    # Median line
    fig.add_trace(go.Scatter(
        x=x, y=q_vals[0.50],
        mode='lines', line=dict(color='darkblue', width=3),
        name='Median Projection',
        hovertemplate='Day %{x}<br>Median: $%{y:.2f}<extra></extra>'
    ))
    
    # Starting price
    fig.add_trace(go.Scatter(
        x=[1, n_steps], y=[s0, s0],
        mode='lines', line=dict(color='red', width=2, dash='dash'),
        name=f'Start: ${s0:.2f}',
        hovertemplate='Start Price: $%{y:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"{label} — {horizon_months} Month Forecast",
        xaxis_title="Trading Days",
        yaxis_title="Price ($)",
        hovermode='x unified',
        template='plotly_white',
        height=500,
        font=dict(size=12),
        title_font=dict(size=18, color='#1f4788', family='Arial Black')
    )
    
    return fig

def create_terminal_distribution(terminal_prices, s0, label):
    """Create terminal price distribution histogram."""
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=terminal_prices,
        nbinsx=50,
        name='Terminal Prices',
        marker=dict(color='steelblue', line=dict(color='darkblue', width=1)),
        hovertemplate='Price: $%{x:.2f}<br>Count: %{y}<extra></extra>'
    ))
    
    # Add vertical lines for start and median
    median = np.median(terminal_prices)
    fig.add_vline(x=s0, line_dash="dash", line_color="red", 
                  annotation_text=f"Start: ${s0:.2f}", annotation_position="top")
    fig.add_vline(x=median, line_dash="solid", line_color="darkblue",
                  annotation_text=f"Median: ${median:.2f}", annotation_position="top")
    
    fig.update_layout(
        title=f"{label} — Terminal Price Distribution",
        xaxis_title="Price ($)",
        yaxis_title="Frequency",
        template='plotly_white',
        height=400,
        showlegend=False
    )
    
    return fig

def format_risk_metrics_table(risk_df):
    """Format risk metrics for display."""
    # Round and format
    display_df = risk_df.copy()
    
    # Define formatting
    format_dict = {
        'Mean Price': '${:.2f}',
        'Median Price': '${:.2f}',
        'Std Dev': '${:.2f}',
        'VaR 95%': '${:.2f}',
        'VaR 99%': '${:.2f}',
        'CVaR 95%': '${:.2f}',
        'CVaR 99%': '${:.2f}',
        'Sharpe Ratio': '{:.2f}',
        'Prob Gain': '{:.1f}%',
        'Max Drawdown %': '{:.2f}%'
    }
    
    for col, fmt in format_dict.items():
        if col in display_df.columns:
            display_df[col] = display_df[col].apply(lambda x: fmt.format(x))
    
    return display_df

# ============================================================================
# MAIN CONTENT
# ============================================================================

# Header
st.title("📊 Gold & Silver Monte Carlo Forecaster")
st.markdown("**Advanced price forecasting with Monte Carlo simulation**")

# Show current prices
if selected_tickers:
    current_prices = get_current_prices(selected_tickers)
    
    cols = st.columns(len(selected_tickers))
    for i, ticker in enumerate(selected_tickers):
        with cols[i]:
            price = current_prices.get(ticker)
            if price:
                asset_name = ticker.replace('=F', '').replace('GC', 'Gold').replace('SI', 'Silver').replace('HG', 'Copper')
                st.metric(f"{asset_name} ({ticker})", f"${price:.2f}", "Live Price")
            else:
                st.metric(ticker, "N/A", "Price unavailable")

st.markdown("---")

# ============================================================================
# RUN SIMULATION
# ============================================================================

if run_simulation:
    if not selected_tickers:
        st.error("⚠️ Please select at least one asset to simulate.")
    elif not horizons:
        st.error("⚠️ Please select at least one forecast horizon.")
    else:
        st.session_state.simulation_run = True
        
        # Determine labels
        labels = tuple([f"{t.replace('=F', '').replace('GC', 'Gold').replace('SI', 'Silver').replace('HG', 'Copper').replace('PA', 'Palladium').replace('PL', 'Platinum')} ({t})" 
                       for t in selected_tickers])
        
        with st.spinner("🔄 Downloading historical data..."):
            # Initialize simulator
            simulator = MonteCarloSimulator(tickers=tuple(selected_tickers), labels=labels)
            
            try:
                # Download prices
                simulator.download_prices(years=years_history)
                s0, mu, sigma, corr, last_date = simulator.estimate_params()
                
                st.success(f"✅ Data downloaded through {last_date.date()}")
                
            except Exception as e:
                st.error(f"❌ Error downloading data: {str(e)}")
                st.stop()
        
        # Estimate jump parameters if needed
        jump_params = None
        if "Jump" in model_type:
            with st.spinner("📊 Estimating jump parameters..."):
                jump_params = simulator.estimate_jump_params()
        
        # Show diagnostics if enabled
        if show_diagnostics:
            with st.expander("📈 Statistical Diagnostics", expanded=False):
                st.subheader("Parameter Estimates")
                
                param_df = pd.DataFrame({
                    'Asset': labels,
                    'Current Price': [f'${p:.2f}' for p in s0],
                    'Daily Mean Return (μ)': [f'{m:.6f}' for m in mu],
                    'Daily Volatility (σ)': [f'{v:.6f}' for v in sigma]
                })
                st.dataframe(param_df, use_container_width=True, hide_index=True)
                
                st.subheader("Correlation Matrix")
                corr_df = pd.DataFrame(corr, index=labels, columns=labels)
                st.dataframe(corr_df.style.background_gradient(cmap='RdYlGn', vmin=-1, vmax=1).format("{:.3f}"),
                           use_container_width=True)
                
                # Normality tests
                returns = np.log(simulator.prices / simulator.prices.shift(1)).dropna()
                normality_results = StatisticalTests.test_normality(returns)
                
                if not normality_results.empty:
                    st.subheader("Normality Tests (Jarque-Bera)")
                    st.dataframe(normality_results, use_container_width=True)
                    
                    # Recommendation
                    any_non_normal = (normality_results['Normal?'] == 'No').any()
                    if any_non_normal:
                        st.warning("⚠️ Returns show non-normality (fat tails). Consider using Jump Diffusion model.")
                
                # Jump parameters
                if jump_params:
                    st.subheader("Jump Diffusion Parameters")
                    jump_df = pd.DataFrame(jump_params).T
                    jump_df.index.name = 'Asset'
                    st.dataframe(jump_df, use_container_width=True)
        
        # Store results
        st.session_state.results = {
            'simulator': simulator,
            's0': s0,
            'mu': mu,
            'sigma': sigma,
            'corr': corr,
            'labels': labels,
            'jump_params': jump_params,
            'horizons': sorted(horizons),
            'model_type': model_type,
            'n_sims': n_sims,
            'seed': seed
        }
        
        # Run simulations for each horizon
        trading_days_per_month = 21
        
        for horizon_idx, hm in enumerate(sorted(horizons)):
            st.markdown("---")
            st.header(f"📅 {hm}-Month Forecast")
            
            n_steps = int(hm * trading_days_per_month)
            
            with st.spinner(f"🎲 Running {n_sims:,} simulations for {hm} months..."):
                # Simulate
                if "Jump" in model_type and jump_params:
                    paths = simulator.simulate_jump_diffusion(n_steps, n_sims, seed=seed+hm, jump_params=jump_params)
                else:
                    paths = simulator.simulate_gbm(n_steps, n_sims, seed=seed+hm)
                
                # Calculate metrics
                risk_metrics = simulator.calculate_risk_metrics(paths)
                terminal = paths[-1, :, :]
            
            # Summary cards
            st.subheader("📊 Summary Metrics")
            metric_cols = st.columns(4)
            
            for asset_idx, label in enumerate(labels):
                median_price = np.median(terminal[:, asset_idx])
                pct_change = ((median_price - s0[asset_idx]) / s0[asset_idx]) * 100
                prob_gain = risk_metrics.loc[label, 'Prob Gain']
                sharpe = risk_metrics.loc[label, 'Sharpe Ratio']
                
                with metric_cols[asset_idx % 4]:
                    st.metric(
                        f"{label.split('(')[0].strip()} Median",
                        f"${median_price:,.2f}",
                        f"{pct_change:+.1f}%"
                    )
                
                with metric_cols[(asset_idx + len(labels)) % 4]:
                    color = "normal" if prob_gain >= 50 else "inverse"
                    st.metric(
                        f"{label.split('(')[0].strip()} Prob. Gain",
                        f"{prob_gain:.1f}%",
                        delta_color=color
                    )
            
            # Fan charts
            st.subheader("📈 Price Projections")
            
            chart_tabs = st.tabs([label.split('(')[0].strip() for label in labels])
            
            for asset_idx, (label, tab) in enumerate(zip(labels, chart_tabs)):
                with tab:
                    fig = create_fan_chart(paths[:, :, asset_idx], s0[asset_idx], hm, label)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Terminal distribution
                    if st.checkbox(f"Show terminal distribution for {label.split('(')[0].strip()}", key=f"dist_{hm}_{asset_idx}"):
                        dist_fig = create_terminal_distribution(terminal[:, asset_idx], s0[asset_idx], label)
                        st.plotly_chart(dist_fig, use_container_width=True)
            
            # Risk metrics table
            st.subheader("⚠️ Risk Metrics")
            
            # Style the dataframe
            styled_risk = risk_metrics.style.apply(
                lambda x: ['background-color: #d4edda' if 'Sharpe' in x.name and v > 1 
                          else 'background-color: #f8d7da' if 'Sharpe' in x.name and v < 0.5
                          else '' for v in x], axis=1
            )
            
            st.dataframe(risk_metrics.round(2), use_container_width=True)
            
            # Download button for this horizon
            csv = risk_metrics.to_csv()
            st.download_button(
                label=f"📥 Download {hm}-Month Risk Metrics (CSV)",
                data=csv,
                file_name=f"risk_metrics_{hm}m.csv",
                mime="text/csv",
                key=f"download_{hm}"
            )
        
        # Scenario analysis
        if enable_scenarios and len(horizons) > 0:
            st.markdown("---")
            st.header("🎯 Scenario Analysis")
            
            base_horizon = sorted(horizons)[len(horizons)//2]  # Middle horizon
            n_steps_scenario = int(base_horizon * trading_days_per_month)
            
            st.info(f"Comparing Bull/Base/Bear scenarios for {base_horizon}-month horizon")
            
            scenarios = {
                'Bear 🐻': (simulator.mu - 0.5 * simulator.sigma, simulator.sigma * 1.3),
                'Base ➡️': (simulator.mu, simulator.sigma),
                'Bull 🐂': (simulator.mu + 0.5 * simulator.sigma, simulator.sigma * 0.8)
            }
            
            original_mu = simulator.mu.copy()
            original_sigma = simulator.sigma.copy()
            
            scenario_results = {}
            
            with st.spinner("Running scenario simulations..."):
                for scenario_name, (mu_adj, sigma_adj) in scenarios.items():
                    simulator.mu = mu_adj
                    simulator.sigma = sigma_adj
                    paths_scenario = simulator.simulate_gbm(n_steps_scenario, n_sims=10000, seed=seed)
                    terminal_scenario = paths_scenario[-1, :, :]
                    
                    scenario_results[scenario_name] = {}
                    for asset_idx, label in enumerate(labels):
                        scenario_results[scenario_name][label] = {
                            'Median': np.median(terminal_scenario[:, asset_idx]),
                            'Mean': np.mean(terminal_scenario[:, asset_idx]),
                            '5th %ile': np.percentile(terminal_scenario[:, asset_idx], 5),
                            '95th %ile': np.percentile(terminal_scenario[:, asset_idx], 95)
                        }
            
            # Restore
            simulator.mu = original_mu
            simulator.sigma = original_sigma
            
            # Display scenario results
            for label in labels:
                st.subheader(f"{label.split('(')[0].strip()} Scenarios")
                
                scenario_df = pd.DataFrame({
                    scenario: scenario_results[scenario][label]
                    for scenario in scenarios.keys()
                }).T
                
                # Format as currency
                for col in scenario_df.columns:
                    scenario_df[col] = scenario_df[col].apply(lambda x: f'${x:,.2f}')
                
                st.dataframe(scenario_df, use_container_width=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>Gold & Silver Monte Carlo Forecaster</strong></p>
    <p>Powered by Yahoo Finance | Built with Streamlit</p>
    <p style='font-size: 12px;'>⚠️ Disclaimer: For educational purposes only. Not financial advice.</p>
</div>
""", unsafe_allow_html=True)

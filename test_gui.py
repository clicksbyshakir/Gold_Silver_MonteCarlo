#!/usr/bin/env python3
"""
Test script to verify Streamlit GUI works correctly
"""

import subprocess
import sys
import time

print("="*70)
print("STREAMLIT GUI - PRE-FLIGHT CHECK")
print("="*70)

# Check imports
print("\n1. Checking dependencies...")
try:
    import streamlit
    print("   ✅ Streamlit installed:", streamlit.__version__)
except ImportError:
    print("   ❌ Streamlit not found. Installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "streamlit", "-q"])
    import streamlit
    print("   ✅ Streamlit installed:", streamlit.__version__)

try:
    import plotly
    print("   ✅ Plotly installed:", plotly.__version__)
except ImportError:
    print("   ❌ Plotly not found. Installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "plotly", "-q"])
    import plotly
    print("   ✅ Plotly installed:", plotly.__version__)

try:
    import yfinance
    print("   ✅ yfinance installed")
except ImportError:
    print("   ❌ yfinance not found")
    sys.exit(1)

# Check files
print("\n2. Checking files...")
from pathlib import Path

files_to_check = [
    "streamlit_app.py",
    "Gold_Silver_MonteCarlo",
    "run_gui.sh"
]

for file in files_to_check:
    if Path(file).exists():
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} not found")
        sys.exit(1)

# Check simulator can be imported
print("\n3. Checking simulator module...")
try:
    mc_file = Path("Gold_Silver_MonteCarlo")
    with open(mc_file, 'r') as f:
        mc_code = f.read()
    
    mc_namespace = {}
    exec(mc_code, mc_namespace)
    
    MonteCarloSimulator = mc_namespace['MonteCarloSimulator']
    StatisticalTests = mc_namespace['StatisticalTests']
    
    print("   ✅ MonteCarloSimulator can be imported")
    print("   ✅ StatisticalTests can be imported")
except Exception as e:
    print(f"   ❌ Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*70)
print("✅ ALL CHECKS PASSED")
print("="*70)
print("\nReady to launch GUI!")
print("\nTo start the GUI, run:")
print("  ./run_gui.sh")
print("\nOr:")
print("  streamlit run streamlit_app.py")
print("\n" + "="*70)

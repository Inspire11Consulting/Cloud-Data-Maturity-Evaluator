"""
Simple entry point for Cloud & Data Maturity Evaluator.
Imports and runs the Streamlit application.

Run with: streamlit run main.py
"""

# Import and run the Streamlit app
# Streamlit will execute this file, so we import the app module which runs on import
from app import main

# The run_app() function is called when the module is imported
# This ensures the app runs when Streamlit executes this file
main.run_app()


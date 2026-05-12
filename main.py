import streamlit as st
from controllers import main_controller

st.set_page_config(
    page_title="Grow Your Forest — Simulador ESG",
    page_icon="🌱",
    layout="wide"
)

st.markdown("""
<style>
    .stProgress > div > div { background-color: #1D9E75 !important; }
    .tree-display { font-size: 36px; letter-spacing: 4px; }
</style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main_controller()
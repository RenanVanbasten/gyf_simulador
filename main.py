import streamlit as st
import pandas as pd
from views import render_sidebar_mock, render_floresta_view, render_ghg_view, render_frota_view

# Configuração da página
st.set_page_config(page_title="Grow Your Forest — UI Preview", layout="wide")

# CSS para manter o estilo visual
st.markdown("""
<style>
    .stProgress > div > div { background-color: #1D9E75 !important; }
</style>
""", unsafe_allow_html=True)

# 1. Mocks (Dados Fictícios)
mock_imp = {
    "total_co2": 4500,
    "co2_combustivel": 3000,
    "co2_papel": 1500,
    "diesel_salvo": 1.2,
    "bpa": 50.0,
    "arvores": 22,
    "progresso": 50,
    "recibos": 10
}

mock_df = pd.DataFrame({
    'motorista': ['Motorista Teste', 'Ana Silva', 'João Souza'],
    'local_pedagio': ['Bandeirantes', 'Anhanguera', 'Dutra'],
    'co2_economizado_g': [450, 500, 300],
    'valor_pago': [15.0, 12.0, 18.0]
})

# 2. Lógica de Navegação
tipo_v, aba = render_sidebar_mock()

if aba == "🌳 Floresta":
    render_floresta_view(mock_imp)
elif aba == "📊 Impacto GHG":
    render_ghg_view(mock_imp)
elif aba == "🚛 Gestão de Frota":
    render_frota_view(mock_df, mock_imp)
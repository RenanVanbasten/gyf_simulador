import streamlit as st
import pandas as pd
import plotly.express as px

def render_floresta_visual(arvores):
    """Renderiza a floresta com emojis."""
    if arvores == 0: return "🌱"
    estagios = ["🌱", "🌿", "🌳"]
    icones = [estagios[min(i // 3, 2)] for i in range(min(arvores, 20))]
    if arvores > 20: icones.append(f" +{arvores - 20}")
    return " ".join(icones)

def render_sidebar_mock():
    """Barra lateral para o protótipo."""
    st.sidebar.title("🌱 Grow Your Forest")
    st.sidebar.markdown("**Protótipo de Interface**")
    st.sidebar.markdown("---")
    tipo_v = st.sidebar.selectbox("🚗 Tipo de Veículo", ["Leve", "Pesado"])
    aba = st.sidebar.radio("Navegação", ["🌳 Floresta", "📊 Impacto GHG", "🚛 Gestão de Frota"])
    st.sidebar.markdown("---")
    st.sidebar.caption("Modo de Visualização Isolada")
    return tipo_v, aba

def render_floresta_view(imp):
    """Aba da Floresta."""
    st.title("🌳 Minha Floresta Virtual (Preview)")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🌳 Árvores", imp['arvores'])
    col2.metric("💨 CO₂ Evitado", f"{imp['total_co2']/1000:.2f} kg")
    col3.metric("⛽ Combustível", f"{imp['diesel_salvo']:.2f} L")
    col4.metric("🧾 Recibos", imp['recibos'])
    
    st.markdown("---")
    st.subheader("Sua floresta")
    html_forest = render_floresta_visual(imp['arvores'])
    st.markdown(f"<div style='font-size:36px'>{html_forest}</div>", unsafe_allow_html=True)
    st.progress(imp['progresso'] / 100)

def render_ghg_view(imp):
    """Aba de Impacto GHG."""
    st.title("📊 Detalhamento GHG (Preview)")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(values=[imp['co2_combustivel'], imp['co2_papel']], 
                     names=['Combustível', 'Papel'],
                     color_discrete_sequence=["#1D9E75", "#8BC926"])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.write("### Resumo de Emissões")
        st.json(imp)

def render_frota_view(df, imp):
    """Aba de Frota."""
    st.title("🚛 Gestão de Frota (Preview)")
    st.write("### Dados Brutos de Simulação")
    st.dataframe(df, use_container_width=True)
    st.info(f"Insight: {imp['arvores']} árvores foram salvas por esta frota.")
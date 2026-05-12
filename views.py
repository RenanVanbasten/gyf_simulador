import streamlit as st
import pandas as pd
import plotly.express as px

def render_floresta_visual(arvores):
    """Renderiza a floresta com emojis escalonados."""
    if arvores == 0: return "🌱"
    estagios = ["🌱", "🌿", "🌳"]
    icones = [estagios[min(i // 3, 2)] for i in range(min(arvores, 20))]
    if arvores > 20: icones.append(f" +{arvores - 20}")
    return " ".join(icones)

def render_sidebar():
    """Renderiza a barra lateral oficial."""
    st.sidebar.title("🌱 Grow Your Forest")
    st.sidebar.markdown("**Simulador de Impacto Ambiental**")
    st.sidebar.markdown("---")
    tipo_v = st.sidebar.selectbox("🚗 Tipo de Veículo", ["Leve", "Pesado"])
    st.sidebar.markdown("---")
    aba = st.sidebar.radio("Navegação", ["🌳 Floresta", "📊 Impacto GHG", "🚛 Gestão de Frota"])
    st.sidebar.markdown("---")
    st.sidebar.caption("Metodologia: GHG Protocol · IPCC 2021")
    return tipo_v, aba

def render_floresta_view(imp):
    """Renderiza a aba Floresta com dados reais do Model."""
    st.title("🌳 Minha Floresta Virtual")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🌳 Árvores", imp['arvores'])
    col2.metric("💨 CO₂ Evitado", f"{imp['total_co2']/1000:.2f} kg")
    
    col3.metric(f"⛽ {imp['tipo_combustivel']} Salvo", f"{imp['combustivel_salvo']:.2f} L")
    
    col4.metric("🧾 Recibos", imp['recibos'])
    
    st.markdown("---")
    st.subheader("Sua floresta")
    
    floresta_html = render_floresta_visual(imp['arvores'])
    st.markdown(f"<div style='font-size:36px'>{floresta_html}</div>", unsafe_allow_html=True)
    
    st.progress(imp['progresso'] / 100)

def render_ghg_view(imp):
    st.title("📊 Detalhamento GHG — Escopo 1 & 3")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(values=[imp['co2_combustivel'], imp['co2_papel']], 
                     names=['Escopo 1 (Combustível)', 'Escopo 3 (Papel)'],
                     color_discrete_sequence=["#1D9E75", "#8BC926"])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Resumo de Impacto")
        st.write(f"Tipo de Veículo: **{imp['tipo_combustivel']}**")
        st.json(imp)

def render_frota_view(df, imp):
    st.title("🚛 Gestão de Frota")
    st.subheader("Dados de Passagens")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.info(f"O uso da Taggy nesta frota já evitou a emissão de {imp['total_co2']/1000:.2f} kg de CO₂.")
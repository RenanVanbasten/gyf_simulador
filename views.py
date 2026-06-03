import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    """Renderiza a página completa de Gestão de Frota e seus dashboards acoplados."""
    st.title("🚛 Gestão de Frota")
    st.subheader("Dados de Passagens")
    st.dataframe(df, width="stretch", hide_index=True)
    st.info(f"O uso da Taggy nesta frota já evitou a emissão de {imp['total_co2']/1000:.2f} kg de CO₂.")
    
    st.divider()
    render_ranking_motoristas(df)
    
    st.divider()
    render_scatter_eficiencia(df)
    
    st.divider()
    render_evolucao_mensal(df)

def render_login_view():
    """Renderiza uma tela de login centralizada e bonita."""
    _, col_centro, _ = st.columns([1, 1.5, 1])
    
    with col_centro:
        st.markdown("<h1 style='text-align: center;'>🌱 Grow Your Forest</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Gestão de Frotas Sustentáveis</p>", unsafe_allow_html=True)
        
        with st.form("form_login"):
            st.subheader("Acesse sua Conta")
            email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            botao_entrar = st.form_submit_button("Entrar no Painel", width="stretch")
            
            if botao_entrar:
                return email, senha, True
                
    return None, None, False

def render_ranking_motoristas(df):
    df_copia = df.copy()
    if "co2_economizado_g" not in df_copia.columns:
        df_copia["co2_economizado_g"] = 48.0 

    ranking = df_copia.groupby("motorista").agg({
        "co2_economizado_g": "sum",
        "valor_pago": "sum",
        "local_pedagio": "count"
    }).reset_index()
    ranking.rename(columns={"local_pedagio": "viagens"}, inplace=True)
    
    ranking["economia_rs"] = ranking["co2_economizado_g"] * 0.02
    ranking["score_esg"] = ((ranking["co2_economizado_g"] * 0.5) + (ranking["economia_rs"] * 0.3) + (ranking["viagens"] * 0.2))
    ranking["score_esg"] = ranking["score_esg"].round(1)
    ranking = ranking.sort_values(by="score_esg", ascending=True)

    fig = px.bar(
        ranking, x="score_esg", y="motorista", orientation="h", color="economia_rs",
        text="score_esg", title="🏆 Ranking ESG de Motoristas",
        labels={"score_esg": "Score ESG", "motorista": "Motorista"}
    )
    fig.update_layout(height=500, xaxis_title="Pontuação ESG", yaxis_title="Motoristas")
    st.plotly_chart(fig, width="stretch")

    st.subheader("📋 Detalhamento do Ranking")
    st.dataframe(ranking[["motorista", "co2_economizado_g", "economia_rs", "viagens", "score_esg"]], width="stretch")


def render_scatter_eficiencia(df):
    df_copia = df.copy()
    if "co2_economizado_g" not in df_copia.columns:
        df_copia["co2_economizado_g"] = 48.0

    comparacao = df_copia.groupby("motorista").agg({
        "co2_economizado_g": "sum",
        "valor_pago": "sum",
        "local_pedagio": "count"
    }).reset_index()
    comparacao.rename(columns={"local_pedagio": "viagens"}, inplace=True)
    comparacao["economia_rs"] = comparacao["co2_economizado_g"] * 0.02

    fig = px.scatter(
        comparacao, x="economia_rs", y="co2_economizado_g", size="viagens", color="motorista",
        hover_name="motorista", text="motorista", title="💡 Economia Financeira vs Impacto Ambiental",
        labels={"economia_rs": "Economia Financeira (R$)", "co2_economizado_g": "CO₂ Economizado (g)"},
        size_max=60
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(height=600)
    st.plotly_chart(fig, width="stretch")
    st.info("🔍 Como interpretar o gráfico:\n\n• Bolhas maiores = mais viagens realizadas\n• Mais para direita = maior economia financeira\n• Mais para cima = maior impacto ambiental positivo")


def render_evolucao_mensal(df):
    df_copia = df.copy()
    if "co2_economizado_g" not in df_copia.columns:
        df_copia["co2_economizado_g"] = 48.0

    if "data_passagem" in df_copia.columns and "data" not in df_copia.columns:
        df_copia["data"] = df_copia["data_passagem"]
    elif "data" not in df_copia.columns:
        df_copia["data"] = pd.date_range(start="2026-01-01", periods=len(df_copia), freq="D")

    df_copia["mes"] = pd.to_datetime(df_copia["data"]).dt.strftime("%b/%Y")
    evolucao = df_copia.groupby("mes").agg({"co2_economizado_g": "sum", "valor_pago": "sum"}).reset_index()
    evolucao["economia_rs"] = evolucao["co2_economizado_g"] * 0.02

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=evolucao["mes"], y=evolucao["co2_economizado_g"], mode="lines+markers", name="CO₂ Economizado"))
    fig.add_trace(go.Scatter(x=evolucao["mes"], y=evolucao["economia_rs"], mode="lines+markers", name="Economia Financeira"))
    fig.update_layout(title="📈 Evolução ESG da Frota", xaxis_title="Mês", yaxis_title="Indicadores", height=500)
    st.plotly_chart(fig, width="stretch")
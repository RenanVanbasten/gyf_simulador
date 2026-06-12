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
    aba = st.sidebar.radio("Navegação", ["🌳 Floresta", "📊 Impacto GHG", "🚛 Gestão de Frota", "👤 Gerenciar Motoristas"])
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
    st.markdown("Análise detalhada das emissões de CO₂ evitadas com base na metodologia do GHG Protocol.")
    
    col_grafico, col_metricas = st.columns([1.2, 1])
    
    with col_grafico:
        fig = px.pie(
            values=[imp['co2_combustivel'], imp['co2_papel']], 
            names=['Escopo 1 (Combustível)', 'Escopo 3 (Papel)'],
            color_discrete_sequence=["#1D9E75", "#8BC926"],
            title="Distribuição do Carbono Evitado por Escopo"
        )
        fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
        
    with col_metricas:
        st.subheader("🌿 Resumo de Impacto Ambiental")
        st.markdown(f"Tipo de Veículo Analisado: **{imp['tipo_combustivel']}**")
        st.divider()
        
        c1, c2 = st.columns(2)
        c1.metric(
            label="💨 Total de CO₂ Evitado", 
            value=f"{imp['total_co2']/1000:.2f} kg",
            help="Soma do carbono que deixou de ser emitido pelo combustível salvo e pelo papel evitado."
        )
        c2.metric(
            label="⛽ Combustível Salvo", 
            value=f"{imp['combustivel_salvo']:.2f} L",
            help="Volume estimado de combustível que deixou de ser queimado nas desacelerações e arrancadas de pedágio."
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        c3, c4 = st.columns(2)
        c3.metric(
            label="🧾 Recibos de Papel Evitados", 
            value=f"{imp['recibos']} un",
            help="Quantidade de comprovantes físicos térmicos que deixaram de ser impressos."
        )
        c4.metric(
            label="🧪 Preservação de BPA", 
            value=f"{imp['bpa']:.1f} mg",
            help="Quantidade de Bisfenol A (composto químico tóxico do papel térmico) evitada na operação."
        )

    co2_evitado_kg = imp['total_co2'] / 1000
    
    percentual_desperdicio = 0.65
    co2_sem_tag_kg = co2_evitado_kg / percentual_desperdicio
    
    co2_com_tag_kg = co2_sem_tag_kg - co2_evitado_kg
    
    dados_comparativos = pd.DataFrame({
        "Indicador Analisado": [
            "Pegada de Carbono do Evento (CO₂)", 
            "Eficiência Energética por Passagem",
            "Paradas Obrigatórias em Cabines", 
            "Geração de Resíduos (Recibos)"
        ],
        "Cenário SEM Tag (Tradicional)": [
            f"{co2_sem_tag_kg:.2f} kg", 
            "Alto Consumo (Arrancadas/Fila)",
            f"{imp['recibos']} paradas completas", 
            f"{imp['recibos']} papéis térmicos"
        ],
        "Cenário COM Tag (Grow Your Forest)": [
            f"{co2_com_tag_kg:.2f} kg", 
            f"Consumo Otimizado (Fluxo Livre)", 
            "0 paradas (Passagem Direta)", 
            "0 papéis (100% Digital)"
        ]
    })
    
    st.dataframe(dados_comparativos, width="stretch", hide_index=True)
    
    st.success(
        f"📉 **Resultado do Diagnóstico:** A manutenção do fluxo constante permitiu mitigar "
        f"**{co2_evitado_kg:.2f} kg** de CO₂ que seriam desperdiçados na fricção mecânica das paradas. "
        f"Isso representa uma redução de **{(percentual_desperdicio * 100):.0f}%** na pegada de carbono operacional deste evento!"
    )

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
    """Renderiza o gráfico de dispersão corrigido, usando dados reais do banco."""
    df_copia = df.copy()
  
    if "co2_economizado_g" not in df_copia.columns:
        df_copia["co2_economizado_g"] = df_copia["valor_pago"] * 4.0

    comparacao = df_copia.groupby("motorista").agg({
        "co2_economizado_g": "sum",
        "valor_pago": "sum",
        "local_pedagio": "count"
    }).reset_index()
    
    comparacao.rename(columns={"local_pedagio": "viagens"}, inplace=True)
    
    comparacao["economia_rs"] = (comparacao["co2_economizado_g"] * 0.02).round(2)
    
    comparacao["CO₂ Evitado (kg)"] = (comparacao["co2_economizado_g"] / 1000).round(2)

    fig = px.scatter(
        comparacao, 
        x="economia_rs", 
        y="CO₂ Evitado (kg)", 
        size="viagens", 
        color="motorista",
        hover_name="motorista", 
        title="💡 Economia Financeira vs Impacto Ambiental da Frota",
        labels={
            "economia_rs": "Economia Financeira Acumulada (R$)",
            "CO₂ Evitado (kg)": "Total de CO₂ Economizado (kg)"
        },
        size_max=50
    )

    fig.update_layout(
        height=500,
        margin=dict(l=40, r=40, t=60, b=40),
        legend_title_text="Motoristas"
    )

    st.plotly_chart(fig, width="stretch")
    
    st.info("""
    🔍 **Como interpretar o gráfico interativo:**
    
    • **Tamanho da Bolha:** Quanto maior a bolha, mais passagens de pedágio o motorista realizou.
    • **Eixo Horizontal (Direita):** Quanto mais para a direita, maior o retorno financeiro gerado.
    • **Eixo Vertical (Cima):** Quanto mais para cima, maior a quantidade de carbono evitada pelo motorista.
    
    *Dica: Passe o mouse sobre as bolhas para ver o detalhamento individual de cada condutor.*
    """)

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

def render_crud_motoristas_view(df_motoristas):
    """Renderiza a interface de gerenciamento (CRUD) de motoristas com formulários blindados."""
    st.title("👤 Gerenciamento de Motoristas")
    st.markdown("Cadastre, visualize e remova motoristas da sua frota.")
    
    st.subheader("➕ Cadastrar Novo Motorista")
    with st.form("form_cadastro_motorista", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome Completo")
        with col2:
            cpf = st.text_input("CPF (Apenas os 11 números)")
        
        botao_cadastrar = st.form_submit_button("Salvar Motorista", width="stretch")
        
        if botao_cadastrar:
            cpf_limpo = cpf.strip() if cpf else ""
            if not nome:
                st.error("Por favor, insira o nome completo do motorista.")
            elif not cpf_limpo.isdigit() or len(cpf_limpo) != 11:
                st.error("Erro: O CPF deve conter exatamente 11 dígitos numéricos (sem letras, pontos ou traços).")
            else:
                return "CRIAR", {"nome": nome, "cpf": cpf_limpo}

    st.divider()

    st.subheader("Motoristas Cadastrados")
    
    if df_motoristas.empty:
        st.info("Nenhum motorista cadastrado para a sua frota ainda.")
    else:
        st.dataframe(df_motoristas[["nome", "cpf"]], width="stretch", hide_index=True)
        
        st.subheader("🗑️ Remover Motorista")
        
        with st.form("form_remocao_motorista"):
            opcoes = {f"{row['nome']} ({row['cpf']})": row['id'] for _, row in df_motoristas.iterrows()}
            selecionado = st.selectbox("Selecione o motorista que deseja remover:", list(opcoes.keys()))
            
            botao_excluir = st.form_submit_button("Excluir Motorista Selecionado", type="primary", width="stretch")
            
            if botao_excluir:
                return "DELETAR", {"id": opcoes[selecionado]}
            
    return None, None
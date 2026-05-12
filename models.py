import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

@st.cache_data
def carregar_dados():
    """
    Tenta conectar ao PostgreSQL. Se não disponível,
    usa dados de demonstração para o simulador.
    """
    try:
        host     = st.secrets.get("db_host", "localhost")
        porta    = st.secrets.get("db_port", "5432")
        banco    = st.secrets.get("db_name", "grow_your_forest")
        usuario  = st.secrets.get("db_user", "postgres")
        senha    = st.secrets.get("db_password", "")
        engine   = create_engine(f"postgresql://{usuario}:{senha}@{host}:{porta}/{banco}")
        return pd.read_sql("SELECT * FROM transacoes_pedagio", engine)
    except Exception:
        return pd.DataFrame({
            'motorista': [
                'Lucas Mendes', 'Maria Silva', 'Lucas Mendes',
                'Carlos Souza', 'Maria Silva', 'Lucas Mendes',
                'Carlos Souza', 'Ana Lima', 'Maria Silva', 'Ana Lima'
            ],
            'local_pedagio': [
                'Bandeirantes', 'Anhanguera', 'Dutra',
                'Bandeirantes', 'Imigrantes', 'Anhanguera',
                'Dutra', 'Bandeirantes', 'Anhanguera', 'Imigrantes'
            ],
            'co2_economizado_g': [45, 50, 48, 45, 52, 47, 44, 51, 49, 53],
            'valor_pago': [12.5, 10.0, 15.0, 12.5, 18.0, 10.0, 15.0, 12.5, 10.0, 18.0]
        })

def calcular_impacto_ghg(df, tipo_veiculo):
    """
    Calcula emissões evitadas com base no GHG Protocol.
    Escopo 1: combustível (marcha lenta evitada)
    Escopo 3: papel térmico (BPA eliminado)
    """
    recibos = len(df)


    if tipo_veiculo == "Pesado":
        fator_parada  = 0.15  
        fator_emissao = 2600  
    else:
        fator_parada  = 0.05  
        fator_emissao = 2300 

    co2_combustivel = (recibos * fator_parada) * fator_emissao
    co2_papel       = recibos * 45.0                            
    total_co2       = co2_combustivel + co2_papel

    arvores   = int(total_co2 // 200)
    progresso = int((total_co2 % 200) / 200 * 100)
    bpa_mg    = recibos * 7.5 

    return {
       "total_co2"      : total_co2,
        "co2_combustivel": co2_combustivel,
        "co2_papel"      : co2_papel,
        "combustivel_salvo": recibos * fator_parada, 
        "tipo_combustivel": "Diesel" if tipo_veiculo == "Pesado" else "Gasolina",
        "bpa"            : bpa_mg,
        "arvores"        : arvores,
        "progresso"      : progresso,
        "recibos"        : recibos,
    }

def render_floresta(arvores):
    """Renderiza floresta virtual com emojis escalonados."""
    if arvores == 0:
        return "🌱"
    estagios = ["🌱", "🌿", "🌳"]
    icones = []
    for i in range(min(arvores, 20)):
        estagio = min(i // 3, 2)
        icones.append(estagios[estagio])
    if arvores > 20:
        icones.append(f" +{arvores - 20}")
    return "  ".join(icones)
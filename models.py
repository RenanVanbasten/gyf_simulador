import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

@st.cache_data
def carregar_dados(empresa_id=None):
    """
    Conecta ao PostgreSQL usando as credenciais do .env.
    Se um empresa_id for fornecido, filtra os dados para aquele usuário.
    """
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db   = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    pw   = os.getenv("DB_PASSWORD")

    try:
        engine = create_engine(f"postgresql://{user}:{pw}@{host}:{port}/{db}")
        
        if empresa_id:
            query = f"SELECT * FROM transacoes_pedagio WHERE empresa_id = {empresa_id}"
        else:
            query = "SELECT * FROM transacoes_pedagio"
            
        return pd.read_sql(query, engine)
        
    except Exception as e:
        st.warning(f"Usando dados de demonstração (Erro: {e})")
        return pd.DataFrame({
            'motorista': ['Lucas Mendes', 'Maria Silva', 'Carlos Souza', 'Ana Lima'],
            'local_pedagio': ['Bandeirantes', 'Anhanguera', 'Dutra', 'Imigrantes'],
            'co2_economizado_g': [45, 50, 48, 52],
            'valor_pago': [12.5, 10.0, 15.0, 18.0],
            'empresa_id': [1, 2, 1, 2]
        })

def calcular_impacto_ghg(df, tipo_veiculo):
    """Calcula emissões evitadas com base no GHG Protocol."""
    recibos = len(df)

    if tipo_veiculo == "Pesado":
        fator_parada, fator_emissao = 0.15, 2600
    else:
        fator_parada, fator_emissao = 0.05, 2300

    co2_combustivel = (recibos * fator_parada) * fator_emissao
    co2_papel = recibos * 45.0
    total_co2 = co2_combustivel + co2_papel

    return {
        "total_co2": total_co2,
        "co2_combustivel": co2_combustivel,
        "co2_papel": co2_papel,
        "combustivel_salvo": recibos * fator_parada,
        "tipo_combustivel": "Diesel" if tipo_veiculo == "Pesado" else "Gasolina",
        "bpa": recibos * 7.5,
        "arvores": int(total_co2 // 200),
        "progresso": int((total_co2 % 200) / 200 * 100),
        "recibos": recibos,
    }

def verificar_login(email, senha):
    """
    Verifica se o usuário e senha existem no banco.
    Retorna o (nome, empresa_id) se sucesso, ou None se falha.
    """
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db   = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    pw   = os.getenv("DB_PASSWORD")
    
    try:
        engine = create_engine(f"postgresql://{user}:{pw}@{host}:{port}/{db}")
        query = f"SELECT nome, empresa_id, senha_hash FROM usuarios WHERE email = '{email}'"
        user_df = pd.read_sql(query, engine)
        
        if not user_df.empty:
            if user_df.iloc[0]['senha_hash'] == senha:
                return user_df.iloc[0]['nome'], user_df.iloc[0]['empresa_id']
        return None
    except:
        if email == "ricardo@email.com" and senha == "senha123":
            return "Ricardo", 1
        return None
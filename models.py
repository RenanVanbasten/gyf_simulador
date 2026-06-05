import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

@st.cache_data
def carregar_dados(empresa_id=None):
    """Conecta ao PostgreSQL e traz as transações reais do banco."""
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db   = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    pw   = os.getenv("DB_PASSWORD")

    try:
        engine = create_engine(f"postgresql://{user}:{pw}@{host}:{port}/{db}")
        
        if empresa_id and str(empresa_id).lower() != 'none':
            try:
                empresa_id = int(empresa_id)
                query = f"SELECT * FROM transacoes_pedagio WHERE empresa_id = {empresa_id} ORDER BY data_passagem DESC"
            except (ValueError, TypeError):
                query = "SELECT * FROM transacoes_pedagio ORDER BY data_passagem DESC"
        else:
            query = "SELECT * FROM transacoes_pedagio ORDER BY data_passagem DESC"
            
        return pd.read_sql(query, engine)
        
    except Exception as e:
        st.error(f"Erro crítico de conexão com o banco de dados: {e}")
        return pd.DataFrame(columns=['motorista', 'local_pedagio', 'valor_pago', 'empresa_id', 'data_passagem'])
    
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

def listar_motoristas_banco(empresa_id):
    """Retorna um DataFrame com todos os motoristas da empresa logada."""
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db   = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    pw   = os.getenv("DB_PASSWORD")
    
    try:
        empresa_id_limpo = int(empresa_id)
        
        engine = create_engine(f"postgresql://{user}:{pw}@{host}:{port}/{db}")
        query = f"SELECT id, nome, cpf FROM motoristas WHERE empresa_id = {empresa_id_limpo} ORDER BY nome"
        return pd.read_sql(query, engine)
    except Exception as e:
        st.error(f"Erro ao listar motoristas: {e}")
        return pd.DataFrame(columns=["id", "nome", "cpf"])

def salvar_motorista_banco(nome, cpf, empresa_id):
    """Insere o motorista e gera viagens automáticas para ele no banco de dados."""
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db   = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    pw   = os.getenv("DB_PASSWORD")
    
    try:
        empresa_id_limpo = int(empresa_id)
        engine = create_engine(f"postgresql://{user}:{pw}@{host}:{port}/{db}")
        
        with engine.connect() as conexao:
            from sqlalchemy import text
            
            # 2. MÁGICA DO MVP: Gera apenas 1 passagem padrão para o motorista não iniciar zerado nos gráficos
            query_viagens = """
                INSERT INTO transacoes_pedagio (empresa_id, motorista, local_pedagio, valor_pago, data_passagem) VALUES 
                (:empresa_id, :nome, 'Dutra', 15.00, '2026-05-20 12:00:00');
            """
            conexao.execute(text(query_viagens), {"empresa_id": empresa_id_limpo, "nome": nome})
            
            
            query_viagens = """
                INSERT INTO transacoes_pedagio (empresa_id, motorista, local_pedagio, valor_pago, data_passagem) VALUES 
                (:empresa_id, :nome, 'Bandeirantes', 12.50, '2026-05-10 08:00:00'),
                (:empresa_id, :nome, 'Anhanguera', 10.00, '2026-05-15 14:30:00'),
                (:empresa_id, :nome, 'Imigrantes', 18.00, '2026-05-20 17:15:00');
            """
            conexao.execute(text(query_viagens), {"empresa_id": empresa_id_limpo, "nome": nome})
            
            conexao.commit()
            
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar motorista e viagens: {e}")
        return False

def deletar_motorista_banco(motorista_id):
    """Remove um motorista do banco pelo ID."""
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db   = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    pw   = os.getenv("DB_PASSWORD")
    
    try:
        engine = create_engine(f"postgresql://{user}:{pw}@{host}:{port}/{db}")
        query = "DELETE FROM motoristas WHERE id = :id"
        with engine.connect() as conexao:
            from sqlalchemy import text
            conexao.execute(text(query), {"id": motorista_id})
            conexao.commit()
        return True
    except Exception as e:
        st.error(f"Erro ao deletar motorista: {e}")
        return False
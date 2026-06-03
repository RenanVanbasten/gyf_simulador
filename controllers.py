import streamlit as st
from models import carregar_dados, calcular_impacto_ghg, verificar_login
from views import render_sidebar, render_floresta_view, render_ghg_view, render_frota_view, render_login_view

def main_controller():
    """Controlador principal com gerenciamento de autenticação e sessão."""
    
    if "logado" not in st.session_state:
        st.session_state["logado"] = False
        st.session_state["usuario_nome"] = ""
        st.session_state["empresa_id"] = None

    if not st.session_state["logado"]:
        email, senha, clicou = render_login_view()
        
        if clicou:
            resultado = verificar_login(email, senha)
            
            if resultado:
                nome_usuario, empresa_id = resultado
                st.session_state["logado"] = True
                st.session_state["usuario_nome"] = nome_usuario
                st.session_state["empresa_id"] = empresa_id
                st.success(f"Bem-vindo de volta, {nome_usuario}!")
                st.rerun()
            else:
                st.error("E-mail ou senha incorretos. Tente novamente.")
                
    else:
        if st.sidebar.button("🚪 Sair do Sistema", width="stretch"):
            st.session_state["logado"] = False
            st.session_state["usuario_nome"] = ""
            st.session_state["empresa_id"] = None
            st.rerun()

        df = carregar_dados(st.session_state["empresa_id"])
        tipo_v, aba = render_sidebar()
        st.sidebar.markdown(f"👤 Gestor: **{st.session_state['usuario_nome']}**")

        imp = calcular_impacto_ghg(df, tipo_v)

        if aba == "🌳 Floresta":
            render_floresta_view(imp)
        elif aba == "📊 Impacto GHG":
            render_ghg_view(imp)
        elif aba == "🚛 Gestão de Frota":
            render_frota_view(df, imp)
from models import carregar_dados, calcular_impacto_ghg
from views import render_sidebar, render_floresta_view, render_ghg_view, render_frota_view

def main_controller():
    """Controlador principal da aplicação."""
    df = carregar_dados()

    tipo_v, aba = render_sidebar()

    imp = calcular_impacto_ghg(df, tipo_v)

    if aba == "🌳 Floresta":
        render_floresta_view(imp)
    elif aba == "📊 Impacto GHG":
        render_ghg_view(imp)
    elif aba == "🚛 Gestão de Frota":
        render_frota_view(df, imp)
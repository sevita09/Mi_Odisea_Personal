from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from layout.layout_base import cargarData, construirLayoutPrincipal

# Crear la app antes de importar módulos que registran callbacks
app = Dash(
    external_stylesheets=[dbc.themes.CERULEAN, dbc.icons.FONT_AWESOME],
)
app.title = "MOP — Mi Odisea Personal"

# Habilitar registro de callbacks que referencian componentes que se cargan dinámicamente
app.config.suppress_callback_exceptions = True
app._favicon = ("../assets/icono.ico")

# Quitar para probar en local y agregar para desplegar en Prod
server = app.server

#app.layout = html.Div([
#    dcc.Store(id="auth-store", storage_type="session", data=False),
#    dcc.Location(id="url", refresh=False),
#    html.Div(id="page-content"),
#])

data = cargarData()
app.layout = construirLayoutPrincipal(data)

if __name__ == '__main__':
    app.run(debug=True)
"""
Layout base del dashboard de MOP.
"""

import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import dcc, html

from configuraciones import ZOOM_REGIONS as regionesZoom
# importar funciones reutilizables (mapa, carga de datos) desde el módulo de funciones
from funciones.layout_base import construirMapa, cargarData

def construirBarraNavegacion() -> dbc.Navbar:
    """
    Construye la barra de navegación superior del dashboard.

    Devuelve un componente `dbc.Navbar` con marca y botón para abrir el
    modal de añadir viaje.
    """
    return dbc.NavbarSimple(
        children=[
            dbc.Nav([
                dbc.Button("✈ Agregar viaje", id="open-modal-btn", className="btn-add", color="info"),
            ]),

            dbc.Col(className="me-3"),  # Espaciador para empujar el enlace a la derecha
            
            dbc.NavLink(
                [html.I(className="fab fa-github-alt me-2")],
                href="https://github.com/sevita09/Mi_Odisea_Personal",
                active="exact",
            )
        ],
        brand=[
            dbc.Container([
                html.Img(src="https://i.postimg.cc/kGMK8dCc/Captura-de-pantalla-2025-09-28-a-la-s-12-56-16-a-m.png", height="40px"),
                dbc.NavbarBrand("MOP", className="nav-brand-name")
            ])
        ],
        brand_href="/",
        color="dark",
        dark=True,
        sticky="top",
        fluid=True,
        className="navbar"
    )

def tarjetaKpi(title: str, element_id: str) -> dbc.Col:
    """
    Devuelve una columna con una tarjeta KPI sencilla.

    La tarjeta contiene un icono, un título y un elemento cuyo contenido
    debe ser actualizado por callbacks de Dash usando el id proporcionado.
    """
    return dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.H5(title, className="kpi-title"),
                html.H4(id=element_id, children="-", className="kpi-value"),
            ], className="d-flex flex-column justify-content-center align-items-center gap-2 h-100 p-3")
        ], className="card-header-dark h-100")
    , md=3)

def tarjetaMapa(df: pd.DataFrame) -> dbc.Col:
    """
    Construye la columna que contiene la tarjeta con el mapa.

    Incluye el encabezado con botones de zoom por región y el gráfico
    generado por `construirMapa`.
    """
    return dbc.Col([
        dbc.Card([
            dbc.CardHeader(
                dbc.Row([
                    dbc.Col(html.H5("Mapa", className="header-title")),
                    dbc.Col(
                        dbc.ButtonGroup(
                            [dbc.Button(region,
                                        id={"type": "zoom-btn", "index": region},
                                        size="lg", color="info", className="zoom-btn")
                             for region in regionesZoom],
                            size="lg",
                        ),
                        className="text-end",
                    ),
                ], align="center"),
                className="card-header-dark",
            ),
            dbc.CardBody(
                dcc.Graph(id="world-map", figure=construirMapa(df), config={"displayModeBar": False}, className="map-graph"),
                className="no-padding",
            ),
        ], className="base-card no-padding"),
    ], lg=9, className="mb-4")



def tarjetaProgreso() -> dbc.Col:
    """
    Construye la columna con el panel de progreso global.

    El contenido del panel se llenará dinámicamente mediante callbacks.
    """
    return dbc.Col([
        dbc.Card([
            dbc.CardHeader(
                html.H5("Viajes", className="header-title text-center"),
                className="card-header-dark"
            ),
            dbc.CardBody(
                id="progress-panel",
                className="progress-panel",
            ),
        ], className="base-card no-padding"),
    ])


def modalAgregarViaje() -> dbc.Modal:
    """
    Modal para añadir un nuevo viaje.

    Contiene campos básicos (título, lugar, lat/lon). Los callbacks se
    encargan de abrir/cerrar el modal y procesar los datos cuando se
    pulse el botón de guardar.
    """
    return dbc.Modal([
        dbc.ModalHeader("Añadir Nuevo Viaje"),
        dbc.ModalBody([
            dbc.Input(id="journey-title", placeholder="Título del viaje", className="mb-2"),
            dbc.Input(id="journey-place", placeholder="Lugar (ciudad/país)", className="mb-2"),
            dbc.Row([
                dbc.Col(dbc.Input(id="journey-lat", placeholder="Latitud")),
                dbc.Col(dbc.Input(id="journey-lon", placeholder="Longitud")),
            ], className="g-2"),
        ]),
        dbc.ModalFooter([
            dbc.Button("Guardar", id="save-journey", color="primary"),
            dbc.Button("Cerrar", id="close-modal", className="ms-2"),
        ]),
    ], id="add-journey-modal", is_open=False)

def construirLayoutPrincipal(df: pd.DataFrame) -> html.Div:
    """
    Compone y devuelve el layout principal del dashboard usando las
    funciones auxiliares definidas en este módulo.
    """
    return html.Div([
        construirBarraNavegacion(),

        dbc.Container([
            # Fila de KPI
            dbc.Row([
                tarjetaKpi("Países Visitados", "kpi-paises"),
                tarjetaKpi("Ciudades Exploradas", "kpi-ciudades"),
                tarjetaKpi("Viajes Registrados", "kpi-viajes"),
                tarjetaKpi("Distancia Total (km)", "kpi-distancia"),
            ], className="mt-4 align-items-stretch"),

            dbc.Row([
                
            ], className="mt-4"),

            # Mapa + Panel de progreso
            dbc.Row([
                tarjetaMapa(df),
                tarjetaProgreso(),
            ]),
    ], fluid=True, className="container-padding"),

        modalAgregarViaje(),

        dcc.Store(id="map-region-store", data="Mundo"),
    ], className="map-layout")
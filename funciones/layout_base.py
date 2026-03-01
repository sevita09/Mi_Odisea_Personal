import os
import pandas as pd
import plotly.graph_objects as go

from configuraciones import CSV_PATH, ZOOM_REGIONS as regionesZoom


def construirMapa(df: pd.DataFrame) -> go.Figure:
    """
    Construye y devuelve una figura de mapa mundial.

    Si `df` contiene columnas `lat` y `lon`, se dibujan puntos de tipo
    scatter con información de lugar. Si no, devuelve un mapa vacío como
    marcador de posición.
    """
    fig = go.Figure()

    # --- Países visitados ---
    iso_paises = df["iso_alpha"].dropna().unique().tolist()
    if iso_paises:
        fig.add_trace(go.Choropleth(
            locations=iso_paises,
            z=[1] * len(iso_paises),
            colorscale=[[0, "#1F6FEB"], [1, "#1F6FEB"]],
            showscale=False,
            marker_line_color="#0d1b2a",
            marker_line_width=0.5,
            hovertemplate="%{location}<extra></extra>",
        ))
    
    # --- Puntos de ciudades ---
    if not df.empty:
        fig.add_trace(go.Scattergeo(
            lat=df["lat"],
            lon=df["lon"],
            text=df["ciudad"] + ", " + df["pais"],
            mode="markers",
            marker=dict(size=5, color="#5ed0ea", symbol="circle",
                        line=dict(width=0.5, color="#ffffff")),
            hovertemplate="<b>%{text}</b><extra></extra>",
            showlegend=False,
        ))

    # --- Diseño del mapa ---
    geo_kwargs = dict(
        bgcolor="#0B0F19",
        showland=True, landcolor="#454B52",
        showocean=True, oceancolor="#0B0F19",
        showcountries=True, countrycolor="#6D6D72",
        showlakes=False, lakecolor="#0B0F19",
        showframe=False, framecolor="#454B52",
        coastlinecolor="#454B52",
        projection_type="equirectangular",
    )

    fig.update_geos(**geo_kwargs)
    fig.update_layout(
        paper_bgcolor="#0B0F19",
        plot_bgcolor="#0B0F19",
        margin=dict(l=0, r=0, t=0, b=0),
        height=490,
    )
    return fig

def cargarData() -> pd.DataFrame:
    """
    Carga el CSV de viajes; crea uno vacío si no existe.
    """
    if not os.path.exists(CSV_PATH):
        df = pd.DataFrame(columns=["id", "pais", "iso_alpha", "ciudad", "lat", "lon", "fecha", "continente"])
        df.to_csv(CSV_PATH, index=False)
    df = pd.read_csv(CSV_PATH)
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
    df.dropna(subset=["lat", "lon"], inplace=True)
    return df
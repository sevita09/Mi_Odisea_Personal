import os

MOP_USERNAME = os.getenv("MOP_USERNAME", "admin")
MOP_PASSWORD = os.getenv("MOP_PASSWORD", "mop2024")

CSV_PATH = os.path.join(os.path.dirname(__file__), "viajes.csv")

# Total de países en el mundo (aprox.)
TOTAL_PAISES = 195

# Continentes reconocidos
ALL_CONTINENTS = [
    "América",
    "Europa",
    "Asia",
    "África",
    "Oceanía",
    "Antártida"
]

# Regiones de zoom para el mapa
ZOOM_REGIONS = {
    "Mundo": {"projection_type": "natural earth", "scope": "world", "center": None},
    "América": {"scope": "america"},
    "Europa": {"scope": "europe"},
    "Asia": {"scope": "asia"},
    "África": {"scope": "africa"},
    "Oceanía": {"projection_type": "natural earth", "scope": "world",
                "center": {"lat": -25, "lon": 140},
                "lataxis": {"range": [-50, 5]}, "lonaxis": {"range": [110, 180]}},
}
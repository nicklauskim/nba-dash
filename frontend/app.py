import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
import plotly.express as px

from layout import layout
from callbacks import register_callbacks


# Initialize app with a Bootstrap theme
app = dash.Dash(__name__, 
                external_stylesheets=[
                    dbc.themes.ZEPHYR,
                    "https://cdn.jsdelivr.net/npm/ag-grid-community/styles/ag-grid.css",
                    "https://cdn.jsdelivr.net/npm/ag-grid-community/styles/ag-theme-alpine.css"
                ],
                suppress_callback_exceptions=True)
app.layout = layout
register_callbacks(app)
app.title = "NBA Play Explorer"


if __name__ == "__main__":
    app.run(debug=True)

    
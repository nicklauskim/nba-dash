from dash import html, dcc
import dash_bootstrap_components as dbc
import os
import sys
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend', 'services')))
from database import get_players, get_teams, get_dates, get_action_types, get_sub_types, get_shot_types, get_shot_zone_areas

def make_dropdown_options(df, label_col, value_col):
    return [{"label": row[label_col], "value": row[value_col]} for _, row in df.iterrows()]

player_options = make_dropdown_options(get_players(), "full_name", "person_id")
team_options = make_dropdown_options(get_teams(), "full_name", "id")
date_options = make_dropdown_options(get_dates(), "gamedate", "gamedate")

action_type_options = {
    'All Shots': 'ALL_SHOTS',
    'Made Shot': 'Made Shot',
    'Missed Shot': 'Missed Shot',
    'Rebound': 'Rebound',
    'Turnover': 'Turnover',
    'Free Throw': 'Free Throw',
}

sub_type_options = make_dropdown_options(get_sub_types(), "subtype", "subtype")
shot_type_options = make_dropdown_options(get_shot_types(), "shot_type", "shot_type")
shot_zone_area_options = make_dropdown_options(get_shot_zone_areas(), "shot_zone_area", "shot_zone_area")


layout = dbc.Container(
    [
        dcc.Location(id='url', refresh=False),

        # --- Header with Navbar ---
        dbc.Row(
            [
                dbc.Col(
                    html.H2(
                        "NBA Data Dashboard",
                        className="my-4",
                        style={"textAlign": "left", "fontSize": "32px"}
                    ),
                    md=8,
                ),
                dbc.Col(
                    dbc.Nav(
                        [
                            dbc.NavLink("Home", href="/", id="nav-home", active="exact", className="nav-link-custom"),
                            dbc.NavLink("Visuals", href="/visuals", id="nav-visuals", active="exact", className="nav-link-custom"),
                            dbc.NavLink("Updates", href="/updates", id="nav-updates", active="exact", className="nav-link-custom"),
                            dbc.NavLink("About", href="/about", id="nav-about", active="exact", className="nav-link-custom"),
                        ],
                        pills=False,
                        justified=True,
                        className="my-4 justify-content-end nav-bar-container",
                    ),
                    md=4,
                ),
            ],
            align="center",
        ),

        html.Hr(style={"marginBottom": "10px"}),

        html.Div(id='page-content'),

        dcc.Store(id="filtered-data-store"),
        dcc.Store(id="filter-store"),
    ],
    fluid=True,
)

# -------------------
# Individual Pages
# -------------------

def landing_page():
    return html.Div(
        style={"textAlign": "center", "padding": "100px"},
        children=[
            html.H1("Welcome to the NBA Play Explorer", style={"marginBottom": "40px"}),
            html.P("This tool lets you explore NBA plays through stats, plots, and even video highlights."),
            html.Button("Take me there!", id="enter-app-btn", n_clicks=0)
        ]
    )


def filter_page():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H3("Set Your Play Filters", className="mb-0")),
                    dbc.CardBody([
                        html.Label("Season", className="mt-2"),
                        dcc.Dropdown(
                            id="season-dropdown", 
                            options=[{'label': f"{year}-{year+1}", 'value': year} for year in range(2016, 2025)],
                            value=2024,
                            placeholder="Select a season",
                            style={"color": "black", "backgroundColor": "white"},
                        ),

                        html.Label("Team", className="mt-3"),
                        dcc.Dropdown(
                            id="team-dropdown", 
                            options=[{'label': 'Any', 'value': 'ANY'}],
                            value='ANY',
                            placeholder="Select a team",
                            style={"color": "black", "backgroundColor": "white"},
                        ),

                        html.Label("Player", className="mt-3"),
                        dcc.Dropdown(
                            id="player-dropdown", 
                            options=player_options,
                            placeholder="Choose a player",
                            value=[203999],
                            multi=True,
                            style={"color": "black", "backgroundColor": "white"},
                        ),

                        html.Label("Season Type", className="mt-3"),
                        dcc.Dropdown(
                            id="season-type-dropdown", 
                            options=[
                                {"label": "Regular Season", "value": 0},
                                {"label": "Playoffs", "value": 1},
                            ],
                            value=0,
                            style={"color": "black", "backgroundColor": "white"},
                        ),

                        html.Label("Date Range", className="mt-3"),
                        dcc.DatePickerRange(
                            id="date-range",
                            start_date=date(2024, 10, 1),
                            end_date=date(2025, 4, 30),
                        ),

                        html.Label("Action Type", className="mt-3"),
                        dcc.Dropdown(
                            id="action-type-dropdown", 
                            options=[{"label": k, "value": v} for k, v in action_type_options.items()],
                            placeholder="Select an action type",
                            value='Made Shot',
                            style={"color": "black", "backgroundColor": "white"},
                        ),

                        html.Div([
                            dcc.Loading(
                                id="filter-loading-spinner",
                                type="circle",
                                color="#0372e8",
                                children=html.Div([
                                    html.Button("Submit", id="submit-filters-btn", n_clicks=0, style={"marginTop": "20px"}),
                                    html.Div(id="dummy-submit-output", style={"display": "none"})
                                ])
                            ),
                            html.Div(id="loading-message", style={"marginTop": "30px", "fontStyle": "italic"})
                        ], style={"textAlign": "center", "marginTop": "20px"})
                    ]),
                ], style={"boxShadow": "0 2px 12px rgba(0,0,0,0.1)", "borderRadius": "12px", "padding": "20px"})
            ], lg={"size": 8, "offset": 2}, md={"size": 10, "offset": 1}, sm=12, width=10)
        ])
    ], fluid=True)


def visualization_page():
    return html.Div([
        html.Div([
            html.Button("← Back to Filters", id="back-to-filters-btn", n_clicks=0),
        ], style={"marginBottom": "20px"}),

        dbc.NavbarSimple(
            brand="NBA Play Visualizer",
            brand_href="#",
            color="light",
            dark=False,
            className="mb-4",
            style={"fontFamily": "Inter", "fontSize": "22px"}
        ),

        dcc.Loading(
            id="loading-spinner",
            type="circle",
            children=[
                dbc.Row(
                    [
                        dbc.Col(dcc.Graph(id="shot-chart"), xs=12, sm=12, md=6, lg=6, xl=6,
                                style={"display": "flex", "justifyContent": "center"}),
                        dbc.Col(dcc.Graph(id="performance-graph"), xs=12, sm=12, md=6, lg=6, xl=6,
                                style={"display": "flex", "justifyContent": "center"})
                    ],
                    className="mb-4",
                    justify="center"
                ),
                html.Hr(style={"marginTop": "30px", "marginBottom": "20px"}),
                html.H3("Video Highlights"),
                html.Div(id="data-table")
            ]
        )
    ],
    style={
        "backgroundColor": "white",
        "color": "black",
        "padding": "20px",
        "borderRadius": "10px"
    })

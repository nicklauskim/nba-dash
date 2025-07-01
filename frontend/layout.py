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
    'All Shots': 'ALL SHOTS',
    'Made Shot': 'Made Shot',
    'Missed Shot': 'Missed Shot',
    'Rebound': 'Rebound',
    'Turnover': 'Turnover',
    'Free Throw': 'Free Throw',
}

sub_type_options = make_dropdown_options(get_sub_types(), "subtype", "subtype")
shot_type_options = make_dropdown_options(get_shot_types(), "shot_type", "shot_type")
shot_zone_area_options = make_dropdown_options(get_shot_zone_areas(), "shot_zone_area", "shot_zone_area")

# --- Navbar ---
navbar = dbc.Navbar(
    dbc.Container([
        html.A(
            dbc.Row([
                # dbc.Col(dbc.NavbarBrand("NBA Play by Play Data Explorer", className="navbar-brand"),
                dbc.Col(dbc.NavbarBrand("NBA Play by Play Data Explorer", className="ms-2")),
            ], align="center", className="g-0"),
            href="/",
            style={"textDecoration": "none"},  
        ),
        dbc.Nav([
            dbc.NavLink("Home", href="/", id="nav-home", active="exact", className="px-3"),
            dbc.NavLink("Visuals", href="/visuals", id="nav-visuals", active="exact", className="px-3"),
            dbc.NavLink("Updates", href="/updates", id="nav-updates", active="exact", className="px-3"),
            dbc.NavLink("About", href="/about", id="nav-about", active="exact", className="px-3"),
        ], className="ms-auto", navbar=True),
    ],
    fluid=True,),
    color="primary",
    dark=True,
    sticky="top",
    className="shadow"
)

# --- App Layout ---
layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Hr(),
    html.Div(id='page-content'),
    html.Footer([
        html.Hr(),
        html.P("Built in Python using Plotly, Dash, PostgreSQL, FastAPI, and most importantly, lots of NBA data", className="text-center text-muted small")
    ], className="mt-5"),
    dcc.Store(id="filtered-data-store"),
    dcc.Store(id="filter-store"),
], fluid=True, className="main-container")

# -------------------
# Individual Pages
# -------------------

def landing_page():
    return html.Div(
        className="fade-in",
        style={"textAlign": "center", "padding": "100px"},
        children=[
            html.H1("Welcome to the NBA Play Explorer", className="mb-4"),
            html.P("This tool lets you explore NBA plays through stats, plots, and even video highlights."),
            dbc.Container([
                html.Button("Take me there!", id="enter-app-btn", n_clicks=0, className="btn btn-primary mt-3"),
            ])
        ]
    )


def filter_page():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H3("Set Your Play Filters", className="mb-0")),
                    dbc.CardBody([
                        html.Label("Season"),
                        dcc.Dropdown(
                            id="season-dropdown",
                            options=[{'label': f"{year}-{year+1}", 'value': year} for year in range(2016, 2025)],
                            value=2024,
                            placeholder="Select a season",
                        ),
                        html.Label("Team", className="mt-3"),
                        dcc.Dropdown(
                            id="team-dropdown",
                            options=[{'label': 'Any', 'value': 'ANY'}],
                            value='ANY',
                            placeholder="Select a team",
                        ),
                        html.Label("Player", className="mt-3"),
                        dcc.Dropdown(
                            id="player-dropdown",
                            options=player_options,
                            placeholder="Choose a player",
                            value=[203999],
                            multi=True,
                        ),
                        html.Label("Season Type", className="mt-3"),
                        dcc.Dropdown(
                            id="season-type-dropdown",
                            options=[
                                {"label": "Regular Season", "value": 0},
                                {"label": "Playoffs", "value": 1},
                            ],
                            value=0,
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
                        ),
                        html.Label("Shot Value", className="mt-3"),
                        dcc.Dropdown(
                            id="two-three-dropdown",
                            options=[
                                {"label": "All Shots", "value": "ALL"},
                                {"label": "Two-Pointers", "value": "2"},
                                {"label": "Three-Pointers", "value": "3"},
                            ],
                            value="ALL",
                            placeholder="Select shot value",
                        ),
                        html.Div([
                            dcc.Loading(
                                id="filter-loading-spinner",
                                type="circle",
                                color="#fb3429",
                                children=html.Div([
                                    html.Button("Submit", id="submit-filters-btn", n_clicks=0, className="btn btn-primary mt-4"),
                                    html.Div(id="dummy-submit-output", style={"display": "none"})
                                ])
                            ),
                            html.Div(id="loading-message", className="mt-4 fst-italic")
                        ], className="text-center")
                    ]),
                ], className="fade-in")
            ], lg={"size": 8, "offset": 2}, md={"size": 10, "offset": 1}, sm=12)
        ], className="g-4")
    ], fluid=True)


def visualization_page():
    return html.Div([
        html.Button("← Back to Filters", id="back-to-filters-btn", n_clicks=0, className="btn btn-outline-secondary mb-3"),
        
        dcc.Loading(
            id="loading-spinner",
            type="circle",
            children=[
                dbc.Row([
                    dbc.Col(dcc.Graph(id="shot-chart"), xs=12, md=6, className="d-flex justify-content-center"),
                    dbc.Col(dcc.Graph(id="performance-graph"), xs=12, md=6, className="d-flex justify-content-center"),
                ], className="mb-4 g-4"),
                html.Hr(className="my-4"),
                html.Div(id="data-table"),
                html.Hr(className="my-4"),
                html.H3("Video Highlights"),
                html.Div([
                    html.Hr(),
                    html.H4("Video Playback Options"),
                    dcc.RadioItems(
                        id="autoplay-toggle",
                        options=[
                            {"label": "Play Combined Video (Autoplay)", "value": "combined"},
                            {"label": "Play Clips One-by-One", "value": "manual"},
                        ],
                        value="manual",
                        labelStyle={"display": "block", "marginBottom": "5px"},
                        style={"marginBottom": "15px"}
                    ),
                    html.Button("Show Video Player", id="show-video-btn", n_clicks=0),
                    html.Div(id="video-player-section")
                ], style={"marginTop": "30px"})
            ]
        )
    ], className="bg-white text-dark p-4 rounded shadow-sm fade-in")

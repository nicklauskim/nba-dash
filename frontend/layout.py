from dash import html, dcc
import dash_bootstrap_components as dbc
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend', 'services')))
from database import get_players, get_teams, get_dates, get_action_types, get_sub_types, get_shot_types, get_shot_zone_areas


def make_dropdown_options(df, label_col, value_col):
    return [{"label": row[label_col], "value": row[value_col]} for _, row in df.iterrows()]


player_options = make_dropdown_options(get_players(), "full_name", "person_id")
team_options = make_dropdown_options(get_teams(), "full_name", "id")
date_options = make_dropdown_options(get_dates(), "gamedate", "gamedate")
# action_type_options = make_dropdown_options(get_action_types(), "actiontype", "actiontype")
action_type_options = {
    'Made Shot': 'Made Shot',
    'Missed Shot': 'Missed Shot',
    'Rebound': 'Rebound',
    'Turnover': 'Turnover',
    'Free Throw': 'Free Throw',
    
}
sub_type_options = make_dropdown_options(get_sub_types(), "subtype", "subtype")
shot_type_options = make_dropdown_options(get_shot_types(), "shot_type", "shot_type")
shot_zone_area_options = make_dropdown_options(get_shot_zone_areas(), "shot_zone_area", "shot_zone_area")



# Sidebar with filters
# sidebar = dbc.Col(
#     [
#         html.H5("Filters"),
#         html.Hr(),
#         dbc.Label("Continent"),
#         dcc.Dropdown(
#             id="continent-filter",
#             options=[{'label': 'Lakers', 'value': 'LAL'}, {'label': 'Celtics', 'value': 'BOS'}],
#             value="Europe",
#             clearable=False
#         ),
#     ],
#     width=3,
#     style={"background": "#f8f9fa", "padding": "20px"},
# )


# Main content with tabs
main_content = dbc.Col(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Data Visualization", tab_id="tab-graph"),
                dbc.Tab(label="Video Content", tab_id="tab-video"),
            ],
            id="tabs",
            active_tab="tab-graph"
        ),
        html.Div(id="tab-content", className="p-4"),
    ],
    width=9
)

layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H2("NBA Data Dashboard", className="text-center my-4")),
        ),
        dcc.Location(id='url', refresh=False),
        # dbc.Row([main_content]),
        html.Div(id='page-content'),
        # Store component that holds the selected data; not actually a visible component
        dcc.Store(id="filtered-data-store")

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
                # Card-style wrapper
                dbc.Card([
                    dbc.CardHeader(html.H3("Set Your Play Filters", classname="mb-0")),
                    
                    dbc.CardBody([
                        html.Label("Season", classname="mt-2"),
                        dcc.Dropdown(
                            id="season-dropdown", 
                            options=[{'label': f"{year}-{year+1}", 'value': year} for year in range(2016, 2025)],
                            placeholder="Select a season",
                            value=2024
                        ),

                        html.Label("Team", classname="mt-3"),
                        dcc.Dropdown(
                            id="team-dropdown", 
                            options=[
                                {'label': 'Any', 'value': 'ANY'},
                                # Add more teams...
                            ],
                            value='ANY',
                            placeholder="Select a team"
                        ),

                        html.Label("Player", className="mt-3"),
                        dcc.Dropdown(
                            id="player-dropdown", 
                            options=player_options,
                            placeholder="Choose a player",
                            value=203999
                        ),

                        html.Label("Season Type", className="mt-3"),
                        dcc.Dropdown(
                            id="season-type-dropdown", 
                            options=[
                                {"label": "Regular Season", "value": 0},
                                {"label": "Playoffs", "value": 1},
                            ],
                            value=0
                        ),

                        html.Label("Date Range", className="mt-3"),
                        dcc.DatePickerRange(
                            id="date-range",
                            start_date='2024-10-01',    # make this change depending on season
                            end_date='2025-04-30',
                        ),

                        html.Label("Action Type", className="mt-3"),
                        dcc.Dropdown(
                            id="action-type-dropdown", 
                            options=action_type_options,
                            placeholder="Select an action type",
                            value='Made Shot'
                        ),

                        html.Div([
                            dcc.Loading(
                                id="filter-loading-spinner",
                                type="default",    # 'graph', 'cube', 'circle', 'dot' or 'default'
                                color="#0372e8",  # Spinner color
                                fullscreen=False,
                                children=html.Div([
                                    html.Button("Submit", id="submit-filters-btn", n_clicks=0),
                                    html.Div(id="dummy-submit-output", style={"display": "none"})  # required for spinner
                                ])
                            ),
                            html.Div(id="loading-message", style={"marginTop": "10px", "fontStyle": "italic"})
                        ])
                    ]),
                ],
                style={"boxShadow": "0 2px 12px rgba(0,0,0,0.1)", "borderRadius": "12px", "padding": "20px"})
            ],
            lg={"size": 8, "offset": 2},
            md={"size": 10, "offset": 1},
            sm=12,
            width=10  # width out of 12 columns
            )
        ])
    ],
    fluid=True
)


def visualization_page():
    return html.Div([
        html.Div([
            html.Button("← Back to Filters", id="back-to-filters-btn", n_clicks=0),
        ], style={"marginBottom": "20px"}),


        dcc.Loading(
            id="loading-spinner",
            type="circle",  # or "default", "dot"
            children=[
                # Row with two side-by-side plots
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(id="shot-chart"), 
                            width=6, 
                            xs=12, sm=12, md=12, lg=6, xl=6,  # Full-width on small screens, half-width on large
                            style={"display": "flex", "justifyContent": "center"}
                        ),
                        dbc.Col(
                            dcc.Graph(id="performance-graph"), 
                            width=6, 
                            xs=12, sm=12, md=12, lg=6, xl=6,
                            style={"display": "flex", "justifyContent": "center"}
                        )
                    ], 
                    className="mb-4",
                    justify="center"
                ),
                html.Hr(style={"marginTop": "30px", "marginBottom": "20px"}),
                # Data table section below
                html.H3("Play Data Table"),
                html.Div(id="data-table")
            ]
        ),

        html.Button("Show Video Player", id="show-video-btn", n_clicks=0),

        html.Div(id="video-player-section")
    ])



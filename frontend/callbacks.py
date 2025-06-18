import dash
from dash import Input, Output, State, ctx, html, dcc, dash_table 
from dash.exceptions import PreventUpdate
from dash_ag_grid import AgGrid
from layout import landing_page, filter_page, visualization_page
from utils import draw_nba_half_court, plot_events, shot_type_heatmap, shot_type_bar_chart
import requests
from datetime import date
import pandas as pd
import plotly.express as px


def register_callbacks(app):
    # Navigation routing
    @app.callback(
        Output("page-content", "children"),
        Input("url", "pathname"),
        prevent_initial_call=True
    )
    def display_page(pathname):
        print("🏁 Routing to:", pathname)
        if pathname == "/":
            return landing_page()
        elif pathname == "/filters":
            return filter_page()
        elif pathname == "/visuals":
            return visualization_page()
        else:
            return html.H1("404 - Page not found")
        
    # Landing → Filters navigation
    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        Input("enter-app-btn", "n_clicks"),
        prevent_initial_call="initial_duplicate"
    )
    def go_to_filters(click):
        if click:
            return "/filters"
        raise PreventUpdate
    
    # Filters → Visuals navigation + fetch filtered data
    @app.callback(
        Output("filtered-data-store", "data"),
        Output("filter-store", "data"),
        Output("url", "pathname"),
        Output("dummy-submit-output", "children"),
        Input("submit-filters-btn", "n_clicks"),
        State("season-dropdown", "value"),
        State("season-type-dropdown", "value"),
        State("team-dropdown", "value"),
        State("player-dropdown", "value"),
        State("date-range", "start_date"),
        State("date-range", "end_date"),
        State("action-type-dropdown", "value"),
        prevent_initial_call=True
    )
    def submit_filters(n, season, season_type, team, player, start_date, end_date, action_type):
        if n:
            # player_id = get_player_id(player)  # Function to map player name to ID
            payload = {
                "season": season,
                "season_type": season_type,
                "team": team,
                "player": player,
                "start_date": start_date,
                "end_date": end_date,
                "action_type": action_type
            }
            response = requests.post("http://localhost:8000/api/filter_plays", json=payload)
            print("Status Code:", response.status_code)
            print("Response Text:", response.text)  # 👈 see what’s actually returned

            if response.status_code != 200:
                raise ValueError("Bad response from backend")
            
            # Fetch filtered data (or pull from dcc.Store/session)
            response = requests.get("http://localhost:8000/api/get_filtered_data")
            data = response.json()
            # Store in cache or session if needed

            # Prepare human-readable filter metadata
            summary = {
                "player_name": player,
                "season": season,
                "team": team,
                "season_type": "Regular" if season_type == 0 else "Playoffs",
                "date_range": [start_date, end_date],
                "action_type": action_type
            }
            return data, summary, "/visuals", "done"
        raise PreventUpdate

    # Filter dropdowns
    # Update player/team options based on season
    @app.callback(
        Output("date-range", "start_date"),
        Output("date-range", "end_date"),
        Input("season-dropdown", "value"),
        prevent_initial_call=True
    )
    def update_date_range(season):
        if season:
            # NBA regular seasons typically start in October and end in April
            # Playoffs go through June
            start = date(season, 10, 1)
            end = date(season + 1, 6, 30)
            return start, end
        return dash.no_update, dash.no_update
    


    # Visuals: Render plots and table (could be refined to use dcc.Store)
    @app.callback(
        # Output("player-header", "children"),
        # Output("filters-header", "children"),
        Output("shot-chart", "figure"),
        Output("performance-graph", "figure"),
        Output("data-table", "children"),
        Input("filtered-data-store", "data"),
        Input("filter-store", "data")
    )
    def load_visuals(data, filters):
        if not data:
            return px.scatter(title="No data"), px.scatter(), "No results"

        # Display player name and some filters at top of page
        player_name = filters.get("player_name", "All Players")
        season = filters.get("season", "All Seasons")
        action_type = filters.get("action_type", "All Actions")

        player_header = f"{player_name}: {action_type}s, {season}"

        df = pd.DataFrame(data).sort_values(by=["gamedate", "eventnum"], ascending=True)

        # 1. Shot chart 2. Area/zones
        fig1 = plot_events(df, draw_nba_half_court())

        fig2 = shot_type_heatmap(df, draw_nba_half_court())

        # Define column definitions with custom options
        column_defs = [
            {"headerName": "Season", "field": "season_stats", "sortable": True, "filter": True},
            {"headerName": "Game Date", "field": "gamedate", "sortable": True, "filter": "agDateColumnFilter"},
            {"headerName": "Opponent", "field": "opponent", "sortable": True, "filter": True},
            {"headerName": "Description", "field": "description_stats", "sortable": True, "filter": True},
            {"headerName": "Action Type", "field": "actiontype", "sortable": True, "filter": True},
            {"headerName": "Subtype", "field": "subtype", "sortable": True, "filter": True},
        ]

        # Data
        table = AgGrid(
            id="play-data-table",
            columnDefs=column_defs,
            rowData=df[["season_stats", "gamedate", "opponent", "description_stats", "actiontype", "subtype"]].to_dict("records"),
            className="ag-theme-alpine",
            columnSize="sizeToFit",  # auto-fit to container
            style={"height": "400px", "width": "100%", "marginTop": "20px"},
            defaultColDef={
                "resizable": True,
                "sortable": True,
                "filter": True,
                "minWidth": 120,
            },
            dashGridOptions={
                "pagination": True,
                "paginationPageSize": 10,
            }
        )

        return fig1, fig2, table


    @app.callback(
    Output("filter-summary", "children"),
    Input("filter-store", "data")
    )
    def update_filter_summary(data):
        if not data:
            return ""
        player = data.get("player_name", "All Players")
        season = data.get("season", "All Seasons")
        team = data.get("team", "All Teams")
        season_type = data.get("season_type", "Any")
        action_type = data.get("action_type", "All Actions")
        start_date, end_date = data.get("date_range", ["-", "-"])
        return f"{player} | Season: {season} | Team: {team} | Type: {season_type} | Dates: {start_date} to {end_date} | Action: {action_type}"


    # Show/hide filters section
    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        Input("back-to-filters-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def show_filters(click):
        if click:
            return "/filters"
        raise PreventUpdate


    # Show/hide video player
    @app.callback(
        Output("video-player-section", "style"),
        Input("show-video-btn", "n_clicks"),
        Input("filtered-data-store", "data"),
        prevent_initial_call=True
    )
    def show_video(n, data):
        if n % 2 == 1:
            return {"display": "block"}
        return {"display": "none"}
    

    # VIDEO PLAYER
    # @app.callback(
    #     Output("video-player", "children"),
    #     Input("next-clip-button", "n_clicks"),
    #     State
    # )
    # def load_video(n_clicks, data):
    #     if not data:
    #         raise PreventUpdate
        
    #     clips = [row["video_url"] for row in data if row.get("video_url", "").endswith(".mp4")]
    #     if not clips:
    #         return html.Div("No video clips available for selected filters.")
        
    #     index = n_clicks % len(clips)
    #     selected_clip = clips[index]

    #     return html.Video(
    #         src=selected_clip,
    #         controls=True,
    #         autoPlay=True,
    #         style={"width": "100%", "maxWidth": "720px", "height": "auto"}
    #     )
        

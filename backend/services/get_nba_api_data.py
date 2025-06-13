"""
This module supplies the functions for retrieving data using the nba_api package.
Types of data retrieved include:
- Player and team statistics for a specific season
- Game logs for individual players and teams
- Shot chart data
- Play-by-play data
"""

# Import libraries
import time
import pandas as pd

from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import (
    commonplayerinfo,
    teaminfocommon,
    playercareerstats,
    leaguedashteamstats,
    playergamelogs,
    teamgamelogs,
    shotchartdetail,
    playbyplay,
    playbyplayv3
)




def get_player_id(full_name):
    """Retrieve the player ID for a given full name."""
    player_list = players.find_players_by_full_name(full_name)
    if player_list:
        return player_list[0]['id']
    else:
        raise ValueError(f"Player '{full_name}' not found.")


def get_team_id(full_name):
    """Retrieve the team ID for a given full name."""
    team_list = teams.find_teams_by_full_name(full_name)
    if team_list:
        return team_list[0]['id']
    else:
        raise ValueError(f"Team '{full_name}' not found.")


def get_player_info(player_ids, batch_size=100):
    """
    Retrieves player information for a list of player IDs.

    Parameters:
    - player_ids (list): A list of player IDs.
    - batch (int): The number of players to process in each batch.

    Returns:
    - pd.DataFrame: A DataFrame containing player information.
    """
    all_player_data = []

    for i in range(0, len(player_ids), batch_size):
        batch_ids = player_ids[i:i+batch_size]
        for player_id in batch_ids:
            try:
                player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
                player_data = player_info.get_data_frames()[0]
                all_player_data.append(player_data)
                print(f"Fetched data for player ID {player_id}")
            except Exception as e:
                print(f"Error fetching data for player ID {player_id}: {e}")
            time.sleep(1)  # Delay to avoid hitting rate limits
        # print(f"Processed batch {i // batch_size + 1} of {len(player_ids) // batch_size + 1}")
        time.sleep(5)  # Additional delay between batches

    return pd.concat(all_player_data, ignore_index=True)




def get_player_season_stats(player_id, per_mode='PerGame'):
    """
    Retrieves season statistics for a specific player.

    Parameters:
    - player_id (int): The unique identifier for the player.
    - per_mode36 (str): The type of stats ('PerGame', 'Per36', 'Totals').

    Returns:
    - pd.DataFrame: A DataFrame containing the player's season statistics.
    """
    stats = playercareerstats.PlayerCareerStats(player_id=player_id, per_mode36=per_mode)
    return stats.get_data_frames()[0]


def get_team_season_stats(team_id, season='2024-25', season_type='Regular Season'):
    """
    Retrieves season statistics for a specific player.

    Parameters:
    - team_id (int): The unique identifier for the team.
    - season (str): The NBA season (e.g., '2024-25').
    - season_type (str): The type of season ('Regular Season', 'Playoffs', 'Pre Season').

    Returns:
    - pd.DataFrame: A DataFrame containing the team's season statistics, including advanced metrics.
    """
    stats = leaguedashteamstats.LeagueDashTeamStats(team_id=team_id, season=season, season_type_all_star=season_type)
    return stats.get_data_frames()[0]


def get_player_game_logs(player_id, season='2024-25', season_type='Regular Season', last_n_games = 5):
    """
    Retrieves game logs for a specific player.

    Parameters:
    - player_id (int): The unique identifier for the player.
    - season (str): The NBA season (e.g., '2024-25').
    - season_type (str): The type of season ('Regular Season', 'Playoffs', etc.).
    - last_n_games (int): The number of last games to retrieve logs for.

    Returns:
    - pd.DataFrame: A DataFrame containing the player's game logs.
    """
    logs = playergamelogs.PlayerGameLogs(player_id=player_id, season_nullable=season, season_type_nullable=season_type, last_n_games_nullable = str(last_n_games))
    return logs.get_data_frames()[0]


def get_team_game_logs(team_id, season='2024-25', season_type='Regular Season', last_n_games = 5):
    """
    Retrieves game logs for a specific team.

    Parameters:
    - team_id (int): The unique identifier for the team.
    - season (str): The NBA season (e.g., '2024-25').
    - season_type (str): The type of season ('Regular Season', 'Playoffs', etc.).
    - last_n_games (int): The number of last games to retrieve logs for.

    Returns:
    - pd.DataFrame: A DataFrame containing the team's game logs.
    """
    logs = teamgamelogs.TeamGameLogs(team_id_nullable=team_id, season_nullable=season, season_type_nullable=season_type, last_n_games_nullable = str(last_n_games))
    return logs.get_data_frames()[0]


def get_shot_chart_data(player_id=0, team_id=0, season='2024-25', season_type='Regular Season', last_n_games = 5):
    """
    Retrieves shot chart data for a specific game.

    Parameters:
    - player_id (int): The player's ID. Default is 0 to include all players.
    - team_id (int): The team's ID. Default is 0 to include all teams.
    - season (str): The NBA season (e.g., '2024-25').
    - season_type (str): The type of season ('Regular Season', 'Playoffs', etc.).
    - opponent_team_id
    - game_id_nullable
    - last_n_games (int): The number of last games to retrieve logs for.
    - season_segment_nullable
    - date_from_nullable
    - date_to_nullable
    - outcome_nullable
    - location_nullable
    - start_period_nullable
    - end_period_nullable
    - period
    - game_segment_nullable
    - clutch_time_nullable
    - point_diff_nullable


    Returns:
    - pd.DataFrame: A DataFrame containing shot chart data.
    """
    shot_chart = shotchartdetail.ShotChartDetail(
        player_id=player_id,
        team_id=team_id,
        season_nullable=season,
        season_type_all_star=season_type,
        context_measure_simple='FGA',    # or 'PTS' for only made baskets
        last_n_games=str(last_n_games),
    )
    return shot_chart.get_data_frames()[0]


def get_play_by_play_data(game_id, start_period=1, end_period=4):
    """
    Fetches play-by-play data for a specific NBA game using the playbyplayv3 endpoint.

    Parameters:
    - game_id (str): The unique identifier for the NBA game (e.g., '0021700807').
    - start_period (int): The starting period to retrieve data from (default is 1).
    - end_period (int): The ending period to retrieve data up to (default is 4).

    Returns:
    - pd.DataFrame: A DataFrame containing the play-by-play data for the specified game.
    """
    # Initialize the PlayByPlayV3 endpoint
    pbp = playbyplayv3.PlayByPlayV3(game_id=game_id, start_period=start_period, end_period=end_period)

    # Retrieve the data as a DataFrame
    pbp_data = pbp.get_data_frames()[0]

    return pbp_data




# Test usage
if __name__ == "__main__":
    # Specify the game ID (example: '0021900001')
    game_id = '0021900001'

    # Retrieve and merge data for the specified game
    sample_data = get_player_info(player_ids=[203999, 201566, 201935])

    # Display the first few rows of the combined DataFrame
    print(sample_data.head(10))
    print(sample_data.iloc[0, :])
    print(sample_data.columns)
    print(sample_data.dtypes)

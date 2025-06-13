# Data cleaning and merging functions for preprocessing prior to inserting into the database

import pandas as pd

from get_nba_api_data import (
    get_player_id,
    get_team_id,
    get_player_info,
    get_player_season_stats,
    get_team_season_stats,
    get_shot_chart_data,
    get_play_by_play_data   
)
from utils import rename_columns, clean_timestamp



def clean_player_df(df):
    """
    Cleans the player information DataFrame by renaming columns and tidying some columns.

    Parameters:
    - df (pd.DataFrame): The player information DataFrame.

    Returns:
    - pd.DataFrame: A cleaned DataFrame with SQL database-compatible column names and data types.
    """
    df = df.copy()
    desired_columns = ['PERSON_ID', 'FIRST_NAME', 'LAST_NAME', 'BIRTHDATE', 'SCHOOL', 'COUNTRY',
                       'HEIGHT', 'WEIGHT', 'SEASON_EXP', 'POSITION', 'ROSTERSTATUS', 
                       'FROM_YEAR', 'TO_YEAR', 'DRAFT_YEAR', 'DRAFT_ROUND', 'DRAFT_NUMBER']
    df = df[desired_columns]
    df.rename(columns=rename_columns(df.columns), inplace=True)
    
    df['birthdate'] = df['birthdate'].apply(clean_timestamp)
    df['birthdate'] = pd.to_datetime(df['birthdate'], errors='coerce')
    df['weight'] = pd.to_numeric(df['weight'], errors='coerce').fillna(0).astype('Int64')
    df['draft_year'] = pd.to_numeric(df['draft_year'], errors='coerce').fillna(0).astype('Int64')
    df['draft_round'] = pd.to_numeric(df['draft_round'], errors='coerce').fillna(0).astype('Int64')
    df['draft_number'] = pd.to_numeric(df['draft_number'], errors='coerce').fillna(0).astype('Int64')

    # for col in df.select_dtypes(include=['object', 'string']).columns:
    #     df[col] = df[col].astype('string')

    return df


def clean_team_df(df):
    pass


def clean_roster_df(df):
    pass


def clean_player_season_stats(df):
    pass
    # Add column marking season

def clean_team_season_stats(df):
    pass
    # Add column marking season



# def merge_shot_and_pbp_data(shots_df, pbp_df):
#     """
#     Merges shot chart data with play-by-play data on GAME_ID and EVENTNUM.

#     Parameters:
#     - shots_df (pd.DataFrame): The shot chart DataFrame.
#     - pbp_df (pd.DataFrame): The play-by-play DataFrame.

#     Returns:
#     - pd.DataFrame: A merged DataFrame containing combined data.
#     """
#     if 'EVENTNUM' not in pbp_df.columns:
#         raise KeyError("The play-by-play DataFrame does not contain 'EVENTNUM' column.")
    
#     merged_df = pd.merge(
#         shots_df,
#         pbp_df,
#         left_on=['GAME_ID', 'GAME_EVENT_ID'],
#         right_on=['GAME_ID', 'EVENTNUM'],
#         how='inner'
#     )
#     return merged_df


# def get_combined_game_data(game_id, player_id=0, team_id=0, season='2023-24', season_type='Regular Season'):
#     """
#     Retrieves and merges shot chart and play-by-play data for a specific game.

#     Parameters:
#     - game_id (str): The unique identifier for the NBA game.
#     - player_id (int): The player's ID. Default is 0 to include all players.
#     - team_id (int): The team's ID. Default is 0 to include all teams.
#     - season (str): The NBA season (e.g., '2023-24').
#     - season_type (str): The type of season ('Regular Season', 'Playoffs', etc.).

#     Returns:
#     - pd.DataFrame: A merged DataFrame containing combined data.
#     """
#     shots_df = get_shot_chart_data(game_id, player_id, team_id, season, season_type)
#     pbp_df = get_play_by_play_data(game_id)
#     return merge_shot_and_pbp_data(shots_df, pbp_df)
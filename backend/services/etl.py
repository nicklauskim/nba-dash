# Collect data and store into PostreSQL database for easier retrieval

# Import data collecting and processing functions
import pandas as pd
import time
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import CommonTeamRoster
from get_nba_api_data import (
    get_player_id,
    get_team_id,
    get_player_info,
    get_player_season_stats,
    get_team_season_stats,
    get_shot_chart_data,
    get_play_by_play_data
)
from data_processing import clean_player_df, clean_team_df, clean_roster_df, clean_player_season_stats, clean_team_season_stats
from database import store_dataframe, store_large_dataframe
from sqlalchemy import Integer, String, Date


def insert_player_data():
    # Insert player table in chunks to avoid API crashes
    player_ids=[player['id'] for player in players.get_players()[5000:]]
    # print(player_ids)
    # print(len(player_ids))
    player_data = get_player_info(player_ids)
    dtype_mapping = {
      'person_id': Integer(),
      'first_name': String(30),
      'last_name': String(30),
      'birthdate': Date(),
      'school': String(50),
      'country': String(50),
      'height': String(10),
      'weight': Integer(),
      'season_exp': Integer(),
      'position': String(30),
      'rosterstatus': String(10),
      'from_year': Integer(),
      'to_year': Integer(),
      'draft_year': Integer(),
      'draft_round': Integer(),
      'draft_number': Integer()
    }
    store_dataframe(clean_player_df(player_data), 'players', dtype_mapping)


def insert_team_data():
    # Team table
    teams_df = pd.DataFrame(teams.get_teams())
    dtype_mapping = {
        'team_id': Integer(),
        'team_name': String(50),
        'team_abbreviation': String(10),
        'team_nickname': String(30),
        'city': String(30),
        'state': String(30),
        'year_founded': Integer(),
    }    
    store_dataframe(teams_df, 'teams', dtype_mapping)
    


def insert_roster_data(season="2024-25"):
    all_teams = teams.get_teams()
    all_rosters = []

    for team in all_teams:
        team_id = team["id"]
        try:
            print(f"Fetching {team['full_name']}...")
            roster = CommonTeamRoster(team_id=team_id, season=season)
            df = roster.get_data_frames()[0]
            df["season"] = season
            all_rosters.append(df)
            time.sleep(1)  # avoid API rate limiting
        except Exception as e:
            print(f"Error with {team['full_name']}: {e}")

    combined = pd.concat(all_rosters, ignore_index=True)

    dtype_mapping = {
        'player_id': Integer(),
        'team_id': Integer(),
        'season': String(10),            
        'player_name': String(50),        
        'jersey': String(10),                 
        'position': String(10),                 
        'height': String(10),               
        'weight': Integer(),              
        'birth_date': Date(),  # Assuming birth_date is in YYYY-MM-DD format         
        'age': Integer(),
        'college': String(50),
        'experience': String(10),                
        'nationality': String(30)
    }

    store_dataframe(combined, 'rosters', dtype_mapping)


def insert_play_by_play_data():
    # Play by play table
    store_large_dataframe("../../datasets/playbyplay_final.csv", 'play_by_play')



def main():
    # insert_player_data()
    # insert_team_data()
    insert_roster_data(season="2024-25")
    # insert_play_by_play_data()



if __name__ == "__main__":
    main()


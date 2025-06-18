# Set up database credentials and connection

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import psycopg2
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from models.filters import FilterRequest


# Load environment variables from .env file
load_dotenv()

# Get database credentials from environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


# Construct the database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)



###########################################
# OBTAINING DATA FROM DATABASE (TO POPULATE DROPDOWNS)
###########################################

def get_players(active=True):
    where_clause = "WHERE rosterstatus = 'Active'" if active else ""
    query = f"""
        SELECT person_id, first_name || ' ' || last_name AS full_name
        FROM players
        {where_clause}
        ORDER BY full_name;
    """
    return pd.read_sql(query, engine)


def get_teams():
    query = "SELECT DISTINCT id, full_name FROM teams ORDER BY full_name ASC;"
    df = pd.read_sql(query, engine)
    return df


def get_dates():
    query = "SELECT DISTINCT gamedate FROM play_by_play ORDER BY gamedate;"
    df = pd.read_sql(query, engine)
    return df


def get_action_types():
    query = "SELECT DISTINCT actiontype FROM play_by_play WHERE actiontype IS NOT NULL ORDER BY actiontype;"
    df = pd.read_sql(query, engine)
    return df


def get_sub_types():
    query = "SELECT DISTINCT subtype FROM play_by_play WHERE subtype IS NOT NULL ORDER BY subtype;"
    df = pd.read_sql(query, engine)
    return df


def get_shot_types():
    query = "SELECT DISTINCT shot_type FROM play_by_play WHERE shot_type IS NOT NULL ORDER BY shot_type;"
    df = pd.read_sql(query, engine)
    return df


def get_shot_zone_areas():
    query = "SELECT DISTINCT shot_zone_area FROM play_by_play WHERE shot_zone_area IS NOT NULL ORDER BY shot_zone_area;"
    df = pd.read_sql(query, engine)
    return df



###########################################
# INSERTING DATA INTO DATABASE
###########################################

# For small/medium-sized data, like player_info: SQLAlchemy engine
def store_dataframe(df: pd.DataFrame, table_name: str, dtype_mapping: dict):
    """
    Stores a pandas DataFrame into a PostgreSQL table.

    Parameters:
    - df (pd.DataFrame): The DataFrame to store.
    - table_name (str): The name of the target table in the database.
    """
    try:
        df.to_sql(table_name, engine, schema='public', if_exists='append', index=False, dtype=dtype_mapping, method='multi')
        print(f"Data stored in table '{table_name}' successfully.")
    except SQLAlchemyError as e:
        print(f"Error storing data in table '{table_name}': {e}")


# For large data: like play-by-play data: fast COPY-based insert
def store_large_dataframe(csv_file_path: str, table_name: str):
    """
    Efficiently loads large CSV file into a PostgreSQL table using psycopg2 COPY.
    
    Parameters:
    - csv_file_path (str): Path to the CSV data file.
    - table_name (str): Destination table in the database.
    """
    try:
        with psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        ) as conn:
            with conn.cursor() as cur:
                with open(csv_file_path, 'r') as f:
                    # Construct the SQL COPY command
                    copy_sql = f"""
                        COPY {table_name} FROM STDIN WITH CSV HEADER
                        NULL ''
                    """
                    cur.copy_expert(sql=copy_sql, file=f)
                    conn.commit()
        print(f"CSV '{csv_file_path}' copied into table '{table_name}' successfully.")
    except Exception as e:
        print(f"Error copying CSV into table '{table_name}': {e}")



from datetime import datetime, date
from decimal import Decimal

def serialize_row(row):
    return {
        k: (
            v.isoformat() if isinstance(v, (datetime, date))
            else float(v) if isinstance(v, Decimal)
            else v
        )
        for k, v in row.items()
    }



# Retrieving data from the database
def get_filtered_playbyplay(filters: FilterRequest):
    """
    Retrieves filtered data from playbyplay data table.

    Parameters:
    - filter_column (str): The column to filter by.
    - filter_value (str): The value to filter for.

    Returns:
    - list of dicts: A DataFrame containing the filtered data.
    """
    base_query = """
        SELECT * 
        FROM play_by_play
        WHERE 1=1
    """

    conditions = []
    parameters = {}

    if filters.player:
        placeholders = ", ".join([f":player_{i}" for i in range(len(filters.player))])
        conditions.append(f"personid IN ({placeholders})")
        for i, pid in enumerate(filters.player):
            parameters[f"player_{i}"] = pid
    # if filters.team:
    #     conditions.append("teamid = :team")
    #     parameters["team"] = filters.team
    if filters.season:
        conditions.append("season_stats = :season")
        parameters["season"] = filters.season
    if filters.season_type is not None:
        conditions.append("playoffs = :season_type")
        parameters["season_type"] = filters.season_type
    if filters.start_date:
        conditions.append("gamedate >= :start_date")
        parameters["start_date"] = filters.start_date
    if filters.end_date:
        conditions.append("gamedate <= :end_date")
        parameters["end_date"] = filters.end_date
    if filters.action_type:
        if filters.action_type == "ALL_SHOTS":
            conditions.append("TRIM(actiontype) IN (:made, :missed)")
            parameters["made"] = "Made Shot"
            parameters["missed"] = "Missed Shot"
        else:
            conditions.append("TRIM(actiontype) = :action_type")
            parameters["action_type"] = filters.action_type
    
    final_query = base_query + " AND \n" + " AND \n".join(conditions)
    # ORDER BY?
    print(final_query)
    print(parameters)

    with engine.connect() as conn:
        try:
            result = conn.execute(text(final_query), parameters)
            data = result.mappings().all()
            print("✅ Rows returned:", len(data))
            return data

        
        except SQLAlchemyError as e:
            print(f"Error retrieving data from table 'play_by_play': {e}")
            return None


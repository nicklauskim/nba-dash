
-- DROP TABLE IF EXISTS players CASCADE;
-- DROP TABLE IF EXISTS play_by_play;
DROP TABLE rosters;


CREATE TABLE IF NOT EXISTS players (
    person_id SERIAL PRIMARY KEY,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    birthdate DATE,
    school VARCHAR(50),
    country VARCHAR(50),
    height VARCHAR(10),
    weight INT, -- in pounds
    season_exp INT,
    position VARCHAR(10),
    rosterstatus VARCHAR(10), -- e.g., 'active', 'inactive', 'retired'
    from_year INT,
    to_year INT,
    draft_year INT,
    draft_round INT,
    draft_number INT
);


CREATE TABLE IF NOT EXISTS teams (
    id INT PRIMARY KEY,
    full_name TEXT NOT NULL,
    abbreviation TEXT,
    nickname TEXT,
    city TEXT,
    state TEXT,
    year_founded INT
);


CREATE TABLE IF NOT EXISTS rosters (
    player_id INT NOT NULL,     -- unique NBA player ID
    team_id INT NOT NULL,     -- NBA team ID
    season TEXT NOT NULL,        -- e.g., '2023-24'
    player_name TEXT NOT NULL,        -- full name
    jersey TEXT,                 -- jersey number (some might be empty)
    position TEXT,                 -- e.g., 'G', 'F-C'
    height TEXT,                 -- 'F-I' format
    weight INT,              
    birth_date DATE,                 
    age INT,
    college TEXT,
    experience TEXT,                 -- e.g., 'R' for rookie, '5' for 5 years
    nationality TEXT,
    PRIMARY KEY (player_id, team_id, season),
    FOREIGN KEY (player_id) REFERENCES players(person_id),
    FOREIGN KEY (team_id) REFERENCES teams(id)
);



CREATE TABLE IF NOT EXISTS play_by_play (
   GAME_ID INT,
   EVENTNUM INT,
   WCTIMESTRING VARCHAR(32),
   PCTIMESTRING VARCHAR(32),
   PERSON1TYPE INT,
   PLAYER1_ID INT,
   PLAYER1_TEAM_ID INT,
   PERSON2TYPE INT,
   PLAYER2_ID INT,
   PLAYER2_TEAM_ID INT,
   PERSON3TYPE INT,
   PLAYER3_ID INT,
   PLAYER3_TEAM_ID INT,

   ACTIONNUMBER INT,
   PERIOD INT,
   TEAMID INT,
   PERSONID INT,
   XLEGACY INT,
   YLEGACY INT,
   ISFIELDGOAL INT,
   SCOREHOME INT,
   SCOREAWAY INT,
   POINTSTOTAL INT,
   LOCATION CHAR(1),
   DESCRIPTION_STATS VARCHAR(256),
   ACTIONTYPE VARCHAR(256),
   SUBTYPE VARCHAR(256),
   ACTIONID INT,
   SEASON_STATS INT,
   PLAYOFFS INT,
   SHOTVALUE INT,

   EVENT_TYPE VARCHAR(256),
   ACTION_TYPE VARCHAR(256),
   SHOT_TYPE VARCHAR(32),
   SHOT_ZONE_BASIC VARCHAR(32),
   SHOT_ZONE_AREA VARCHAR(32),
   SHOT_ZONE_RANGE VARCHAR(32),
   SHOT_DISTANCE INT,
   LOC_X INT,
   LOC_Y INT,
   SHOT_ATTEMPTED_FLAG INT,
   SHOT_MADE_FLAG INT,

   ENDTIME VARCHAR(10),
   EVENTS VARCHAR(1024),
   FG2A INT,
   FG2M INT,
   FG3A INT,
   FG3M INT,
   GAMEDATE DATE,
   GAMEID_PBP INT,
   NONSHOOTINGFOULSTHATRESULTEDINFTS INT,
   OFFENSIVEREBOUNDS INT,
   OPPONENT CHAR(3),
   SHOOTINGFOULSDRAWN INT,
   STARTSCOREDIFFERENTIAL INT,
   STARTTIME VARCHAR(10),
   STARTTYPE VARCHAR(32),
   TURNOVERS INT,
   DESCRIPTION_PBP VARCHAR(256),
   URL VARCHAR(256),

   PRIMARY KEY (GAME_ID, EVENTNUM)
--    CONSTRAINT fk_personid FOREIGN KEY (PERSONID) REFERENCES players(person_id)
);




























-- CREATE TABLE player_season_stats (
--     stat_id SERIAL PRIMARY KEY,
--     player_id INT REFERENCES players(player_id),
--     season_id INT REFERENCES seasons(season_id),
--     team_id INT REFERENCES teams(team_id),
--     games_played INT,
--     points_per_game DECIMAL(5,2),
--     assists_per_game DECIMAL(5,2),
--     rebounds_per_game DECIMAL(5,2),
--     steals_per_game DECIMAL(5,2),
--     blocks_per_game DECIMAL(5,2),
--     turnovers_per_game DECIMAL(5,2),
--     field_goal_percentage DECIMAL(5,2),
--     three_point_percentage DECIMAL(5,2),
--     free_throw_percentage DECIMAL(5,2),
--     minutes_per_game DECIMAL(5,2),
--     PRIMARY KEY (player_id, season_id)
-- );


-- CREATE TABLE team_season_stats (
--     stat_id SERIAL PRIMARY KEY,
--     team_id INT REFERENCES teams(team_id),
--     season_id INT REFERENCES seasons(season_id),
--     games_played INT,
--     wins INT,
--     losses INT,
--     points_per_game DECIMAL(5,2),
--     assists_per_game DECIMAL(5,2),
--     rebounds_per_game DECIMAL(5,2),
--     steals_per_game DECIMAL(5,2),
--     blocks_per_game DECIMAL(5,2),
--     turnovers_per_game DECIMAL(5,2),
--     field_goal_percentage DECIMAL(5,2),
--     three_point_percentage DECIMAL(5,2),
--     free_throw_percentage DECIMAL(5,2),
--     minutes_per_game DECIMAL(5,2),
--     PRIMARY KEY (team_id, season_id)
-- );




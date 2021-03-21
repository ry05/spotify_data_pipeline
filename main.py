import sqlalchemy
import pandas as pd 
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3

DATABASE_LOC = "sqlite:///recent_tracks.sqlite"
USER_ID = "Ramshankar Yadhunath"
TOKEN = "BQC_pZfW70IMy5v2jlYGj7SkQjeUHNt3IxJXwQOkqExItchP8Fx45Hf8yCay_C5fQ2bXio8PQC5w7l5k2Bzd12pF0y0oI_MCVC9Kav6eIGDHZA0oTskMNABcSeXKHttJDsZevju3nloobRL-8FEZ2j8uNN4OmQBSH_PhNUI_"

def validate(df):
    """
    Validate the data
    """

    # is data empty?
    if df.empty:
        print("No songs downloaded. Finishing execution.")
        return False
    
    # primary key constraint
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary key constraint is violated!")

    # check for nulls
    if df.isnull().values.any():
        raise Exception("Missing values exist!")

if __name__ == "__main__":
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token = TOKEN)
    }

    # I want to see what I have played in the last 365 days
    today = datetime.datetime.now()
    last_year = today - datetime.timedelta(days=365)
    last_year_unix = int(last_year.timestamp()) * 1000

    # get data
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=last_year_unix),
        headers = headers)
    data = r.json()

    # diagnose
    print(data)

    # filter data to get only what you need
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    # get data into pandas dataframe
    df = pd.DataFrame({
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamps": timestamps
    })

    print(df)

    # validate
    if validate(df):
        print("Data valid, proceed to Load Stage")

    # Load

    engine = sqlalchemy.create_engine(DATABASE_LOC) # database will be created if it does not exist
    conn = sqlite3.connect("recent_tracks.sqlite")
    cursor = conn.cursor() # pointer to refer to specific rows in a db

    # create table
    sql_query = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamps VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """
    cursor.execute(sql_query)
    print("Opened db succesfully")
    
    # populate the database
    try:
        df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database")
    conn.close()
    print("Close database successfully")


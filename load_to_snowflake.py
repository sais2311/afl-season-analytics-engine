import os
import pandas as pd
from snowflake.connector import connect
from snowflake.connector.pandas_tools import write_pandas

# Trying to match my Snowflake columns
COLUMNS = ["round", "hteam", "ateam", "hscore", "ascore",
           "hgoals", "hbehinds", "agoals", "abehinds",
           "hteamid", "ateamid", "winner", "result", "venue", "date"]

# Reading the clean dataset
df = pd.read_csv("games_clean.csv")[COLUMNS]


df.columns = [c.upper() for c in df.columns]
print(f"Rows to load: {len(df)}")

# Connect it to Snowflake
conn = connect(
    account="VISIGIC-YN04601",
    user="saipanini",
    password=os.environ["SNOWFLAKE_PASSWORD"],
    warehouse="AFL_WH",
    database="AFL",
    schema="PUBLIC",
)

# Pushing the data 
success, n_chunks, n_rows, _ = write_pandas(conn, df, "GAMES")
print(f"Loaded: {success}, rows written: {n_rows}")

conn.close()

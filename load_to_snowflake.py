import os
import pandas as pd
from snowflake.connector import connect
from snowflake.connector.pandas_tools import write_pandas

# The columns that match our Snowflake GAMES table
COLUMNS = ["round", "hteam", "ateam", "hscore", "ascore",
           "hgoals", "hbehinds", "agoals", "abehinds",
           "hteamid", "ateamid", "winner", "result", "venue", "date"]

# Read the clean season and keep only the columns the table expects
df = pd.read_csv("games_clean.csv")[COLUMNS]

# Snowflake matches column names in UPPERCASE, so align to that
df.columns = [c.upper() for c in df.columns]
print(f"Rows to load: {len(df)}")

# Connect to Snowflake (password read from the environment, never hard-coded)
conn = connect(
    account="VISIGIC-YN04601",
    user="saipanini",
    password=os.environ["SNOWFLAKE_PASSWORD"],
    warehouse="AFL_WH",
    database="AFL",
    schema="PUBLIC",
)

# Push the DataFrame into the GAMES table
success, n_chunks, n_rows, _ = write_pandas(conn, df, "GAMES")
print(f"Loaded: {success}, rows written: {n_rows}")

conn.close()

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from snowflake.connector import connect

QUERY = """
WITH team_games AS (
    SELECT hteam AS team, hscore AS points_for, ascore AS points_against FROM AFL.PUBLIC.GAMES
    UNION ALL
    SELECT ateam AS team, ascore AS points_for, hscore AS points_against FROM AFL.PUBLIC.GAMES
)
SELECT team, AVG(points_for) AS attack, AVG(points_against) AS defence
FROM team_games GROUP BY team
"""

conn = connect(
    account="VISIGIC-YN04601", user="saipanini",
    password=os.environ["SNOWFLAKE_PASSWORD"],
    warehouse="AFL_WH", database="AFL", schema="PUBLIC",
)
df = conn.cursor().execute(QUERY).fetch_pandas_all()
conn.close()

df["ATTACK"] = df["ATTACK"].astype(float)
df["DEFENCE"] = df["DEFENCE"].astype(float)

avg_attack = df["ATTACK"].mean()
avg_defence = df["DEFENCE"].mean()

x_min, x_max = df["ATTACK"].min() - 3, df["ATTACK"].max() + 3
y_min, y_max = df["DEFENCE"].min() - 3, df["DEFENCE"].max() + 3

fig, ax = plt.subplots(figsize=(11, 8))
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_max, y_min)   # reversed => good defence (fewer conceded) sits at the top

# Shade the premiership zone: better-than-average attack AND defence
ax.add_patch(Rectangle((avg_attack, avg_defence), x_max - avg_attack, y_min - avg_defence,
                       color="green", alpha=0.08, zorder=0))

ax.scatter(df["ATTACK"], df["DEFENCE"], s=70, zorder=3)
for _, r in df.iterrows():
    ax.annotate(r["TEAM"], (r["ATTACK"], r["DEFENCE"]),
                fontsize=8, xytext=(5, 5), textcoords="offset points", zorder=4)

ax.axvline(avg_attack, linestyle="--", linewidth=1, color="grey")
ax.axhline(avg_defence, linestyle="--", linewidth=1, color="grey")

ax.set_xlabel("Attack — avg points scored / game  (more = better \u2192)")
ax.set_ylabel("Defence — avg points conceded / game  (fewer = better \u2191)")
ax.set_title("2026 AFL Contender Quadrant — S. Surapaneni")
ax.text(x_max - 0.5, y_min + 0.5, "PREMIERSHIP PROFILE",
        ha="right", va="top", fontsize=11, fontweight="bold", color="green")

plt.tight_layout()
plt.savefig("contender_quadrant.png", dpi=150)
print("Saved contender_quadrant.png")

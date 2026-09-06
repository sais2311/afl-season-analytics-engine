import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from adjustText import adjust_text

games = pd.read_csv("games_clean.csv")

# Last 10 rounds 
last_round = games["round"].max()
window = games[games["round"] > last_round - 10].copy()
n_rounds = window["round"].nunique()

home = window[["hteam", "hscore", "ascore"]].rename(columns={"hteam": "team", "hscore": "pf", "ascore": "pa"})
away = window[["ateam", "ascore", "hscore"]].rename(columns={"ateam": "team", "ascore": "pf", "hscore": "pa"})
tg = pd.concat([home, away])
stats = tg.groupby("team").agg(attack=("pf", "mean"), defence=("pa", "mean")).reset_index()

avg_attack = stats["attack"].mean()
avg_defence = stats["defence"].mean()
stats["zone"] = (stats["attack"] > avg_attack) & (stats["defence"] < avg_defence)

COLOURS = {
    "Adelaide": "#E21937", "Brisbane Lions": "#C0143C", "Carlton": "#2C5AA0",
    "Collingwood": "#FFFFFF", "Essendon": "#E4002B", "Fremantle": "#A265D0",
    "Geelong": "#4A78C0", "Gold Coast": "#E03A3E", "Greater Western Sydney": "#F47920",
    "Hawthorn": "#FBBF15", "Melbourne": "#C8102E", "North Melbourne": "#4A90D9",
    "Port Adelaide": "#00A9B7", "Richmond": "#FFD200", "St Kilda": "#ED1B2E",
    "Sydney": "#ED171F", "West Coast": "#F2A900", "Western Bulldogs": "#5B8DD6",
}

BG = "#0E1117"
plt.rcParams["font.family"] = "DejaVu Sans"
fig, ax = plt.subplots(figsize=(12, 9))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

xp, yp = 4, 4
x_min, x_max = stats["attack"].min()-xp, stats["attack"].max()+xp
y_min, y_max = stats["defence"].min()-yp, stats["defence"].max()+yp
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_max, y_min)

ax.add_patch(Rectangle((avg_attack, avg_defence), x_max-avg_attack, y_min-avg_defence,
                       facecolor="#1DB954", alpha=0.08, edgecolor="none", zorder=0))
ax.axvline(avg_attack, color="#3A3F4B", lw=1, ls="--", zorder=1)
ax.axhline(avg_defence, color="#3A3F4B", lw=1, ls="--", zorder=1)

texts = []
for _, r in stats.iterrows():
    c = COLOURS.get(r["team"], "#888888")
    z = r["zone"]
    ax.scatter(r["attack"], r["defence"], s=300 if z else 150, color=c,
               edgecolors="#FFFFFF" if z else "#2A2F3A", linewidths=1.8 if z else 0.8,
               zorder=5, alpha=0.97)
    texts.append(ax.text(r["attack"], r["defence"], r["team"],
                 color="#FFFFFF" if z else "#AEB4C0",
                 fontsize=11.5 if z else 9, fontweight="bold" if z else "normal", zorder=6))

adjust_text(texts, ax=ax, expand=(1.4, 1.6),
            arrowprops=dict(arrowstyle="-", color="#4A4F5B", lw=0.6))

ax.text(x_max-0.6, y_min+0.6, "FORM PREMIERSHIP ZONE", ha="right", va="top",
        color="#1DB954", fontsize=13, fontweight="bold")
ax.set_title("2026 AFL Form Window \u2014 Last %d Rounds" % n_rounds,
             color="#FFFFFF", fontsize=21, fontweight="bold", pad=26, loc="left")
ax.text(0.0, 1.02, "Attack vs defence over the run home  \u00b7  who had the profile going into finals",
        transform=ax.transAxes, color="#8A909C", fontsize=11.5, ha="left")
ax.set_xlabel("ATTACK  \u2014  avg points scored / game  \u2192", color="#AEB4C0", fontsize=11, labelpad=10)
ax.set_ylabel("DEFENCE  \u2014  avg conceded / game  \u2191  (fewer = better)", color="#AEB4C0", fontsize=11, labelpad=10)

ax.grid(True, color="#191E28", lw=0.6)
ax.set_axisbelow(True)
for s in ax.spines.values():
    s.set_color("#2A2F3A")
ax.tick_params(colors="#6A707C")
fig.text(0.5, 0.015, "Data: Squiggle API   \u00b7   Built by Sai Surapaneni",
         color="#5A606C", fontsize=9.5, ha="center")

plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig("form_window.png", dpi=200, facecolor=BG, bbox_inches="tight")
print("Saved form_window.png |", n_rounds, "rounds | zone:", list(stats[stats.zone].team))

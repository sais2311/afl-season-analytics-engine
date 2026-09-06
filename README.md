# AFL Season Analytics Engine (2026)

An automated data pipeline that pulls the full 2026 AFL season from a public API,
validates it, loads it into a Snowflake cloud data warehouse, and produces five
complementary analyses of the season — including an opponent-adjusted power ranking
and a contender quadrant.

Built to mirror real AFL data-engineering roles (Champion Data, AFL clubs):
API integration, SQL + Python, cloud warehousing, and data-quality validation.

## Architecture

```text
Squiggle API  ->  Python         ->  Python             ->  Snowflake   ->  SQL / Python
                  (extract)          (clean + validate)     (warehouse)     (5 analyses)
                                         |
                                         +--> Data-quality checks + QA report
```

## The pipeline

1. **Extract** (`fetch_data.py`) — pulls the 2026 season from the Squiggle API,
   saves to `season_2026.json` (fetch-once, then work from disk).
2. **Validate & clean** (`validate_games.py`, `clean_data.py`) — data-quality checks:
   score reconciliation (goals x 6 + behinds), missing-value checks, round completeness.
   Draws (null winner) detected and handled explicitly. Outputs `games_clean.csv`.
3. **Load** (`load_to_snowflake.py`) — loads the clean season into a typed
   Snowflake table (`AFL.PUBLIC.GAMES`) via `write_pandas`.
4. **Analyse** (`01`–`05` .sql, `contender_quadrant.py`) — five analyses run off the warehouse.

## The five analyses

| # | Analysis | What it shows |
|---|----------|---------------|
| 1 | Power Ranking | Opponent-adjusted margin rating — who was actually best, vs the ladder |
| 2 | Contender Quadrant | Attack vs defence scatter; top-right = premiership profile |
| 3 | Offence/Defence Split | Teams ranked separately on attack and defence |
| 4 | Strength of Schedule | Who had the easy draw vs the brutal one |
| 5 | Season Form | 5-game rolling form — who surged, who faded into finals |

## Key findings (2026 home-and-away season)

Five analyses, one story: who was actually best, why they were good, who had it
easy or hard, and who was peaking at the right time. The recurring theme — the
ladder hides things a margin-based, opponent-adjusted view brings out.

### 1. Power Ranking — the ladder and the "best team" aren't the same
- **Sydney rated #1** on opponent-adjusted margin (**+27.8**), ahead of **Fremantle
  (+26.1)** — even though Fremantle won the minor premiership. Sydney was the more
  *dominant* team; Fremantle won more games. That gap is the whole point of a power
  ranking.
- **Geelong is the ladder's most underrated side:** 5th on the ladder, but **3rd** on
  the adjusted rating — they combined strong margins with a slightly harder-than-average
  draw.
- **Hawthorn is the mirror image:** 4th on the ladder, **5th** on the rating. Their
  percentage (120.1) actually trailed 5th-placed Geelong's (122.3), and they drew twice —
  signs of a team that won more games than their margins alone "deserved."

### 2. Strength of Schedule — not everyone played the same season
- **Western Bulldogs faced the hardest draw in the league (+4.4);** **Hawthorn the
  easiest (−2.3).**
- Adjusting for it flips the story on the Dogs: a below-average raw margin (**−4.0**)
  becomes **above the line (+0.4)** once you account for the schedule — a genuinely
  better side than 8th suggests.
- This is the single clearest example of why raw win/loss records mislead: two teams
  with the same record did not play the same season.

### 3. Offence/Defence Split — *why* teams were good, not just that they were
- **Fremantle won the minor premiership on defence:** **#1 defence** (72.4 conceded)
  but only **5th attack**. A side that suffocated opponents rather than outscoring them.
- **Brisbane were the opposite:** **#2 attack** (108.7) but **11th defence** (89.3) —
  elite firepower without a finals-grade defence.
- **Sydney were the only genuinely complete team:** **#1 attack and #3 defence**.
- **Adelaide were the quiet achiever:** a modest **7th attack** but **#2 defence** — a
  stingy side that flew under the radar.

### 4. Contender Quadrant — five teams with the premiership profile
- **Above average at both ends (the top-right zone):** Sydney, Fremantle, Adelaide,
  Hawthorn, Geelong.
- **Brisbane were the only high-scoring side to miss the zone** — elite attack dragged
  down by a leaky defence. Historically, that defensive gap is a finals problem.
- **Sydney sit furthest into the top-right** — the most complete profile in the league.

### 5. Season Form — who was peaking at the right time
- **Hawthorn were the 2nd-hottest team over the final five rounds**, surging into
  September — form that showed up when they beat Fremantle away in the first week of finals.
- **Carlton (+46) and Geelong (+40) were the season's biggest improvers**, both climbing
  hard down the stretch.
- **Gold Coast were the collapse of the year:** they started like contenders and faded
  badly — roughly a **−68 swing** in rolling form from early season to late.
- **The Western Bulldogs were actually *fading* into finals** — which, paired with their
  hardest-in-the-league draw, tells a nuanced story: a genuinely good side by the numbers,
  but not one in hot form.

### A note on limitations (because honesty matters)
- **The quadrant axes are raw, not opponent-adjusted.** A team from an easy draw looks
  better than it is. Opponent-adjusting the axes (using the strength-of-schedule numbers
  already computed) is the obvious next version.
- **These ratings measure full-season performance.** They can't account for finals
  availability — injuries, suspensions, late changes. That's where human judgment has to
  layer on top of the numbers, and it's why a model is a tool, not an oracle.

## Data quality

Validation is a first-class step, not an afterthought. Checks run before any data
reaches the warehouse: score reconciliation against AFL scoring rules, null checks on
analysis-critical fields, and round-completeness. The draw-detection case is a worked
example — three null-winner rows were flagged, traced to genuine drawn games, and
handled as half-wins rather than silently corrupting the ratings.

## Tech stack

Python (requests, pandas, matplotlib) · Snowflake · SQL · Git

## Data source

[Squiggle API](https://api.squiggle.com.au) — public AFL fixtures, scores, and ladder.

## Setup

\`\`\`
python3 -m venv venv && source venv/bin/activate
pip install requests pandas matplotlib "snowflake-connector-python[pandas]"
export SNOWFLAKE_PASSWORD='your_password'
python fetch_data.py && python clean_data.py && python load_to_snowflake.py
\`\`\`

---
*Built by Sai Surapaneni — data science student, aspiring AFL analyst.*

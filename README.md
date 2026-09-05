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

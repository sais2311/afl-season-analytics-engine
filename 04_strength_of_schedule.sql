/*
Average rating of each team's opponents.
*/

WITH team_games AS (
    SELECT hteam AS team, ateam AS opponent, hscore - ascore AS margin FROM AFL.PUBLIC.GAMES
    UNION ALL
    SELECT ateam AS team, hteam AS opponent, ascore - hscore AS margin FROM AFL.PUBLIC.GAMES
),
base AS (
    SELECT team, AVG(margin) AS base_margin FROM team_games GROUP BY team
)
SELECT
    tg.team,
    ROUND(AVG(b_opp.base_margin), 1) AS strength_of_schedule
FROM team_games tg
JOIN base b_opp ON tg.opponent = b_opp.team
GROUP BY tg.team
ORDER BY strength_of_schedule DESC;

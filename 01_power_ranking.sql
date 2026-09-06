/*
Power Ranking
Base rating 
Strength of Schedule (the avg opponent rating).
*/

WITH team_games AS (
    SELECT hteam AS team, ateam AS opponent, hscore - ascore AS margin FROM AFL.PUBLIC.GAMES
    UNION ALL
    SELECT ateam AS team, hteam AS opponent, ascore - hscore AS margin FROM AFL.PUBLIC.GAMES
),
base AS (
    SELECT team, AVG(margin) AS base_margin
    FROM team_games
    GROUP BY team
)
SELECT
    tg.team,
    ROUND(b_self.base_margin, 1)                          AS base_margin,
    ROUND(AVG(b_opp.base_margin), 1)                       AS strength_of_schedule,
    ROUND(b_self.base_margin + AVG(b_opp.base_margin), 1)  AS adjusted_rating
FROM team_games tg
JOIN base b_self ON tg.team = b_self.team
JOIN base b_opp  ON tg.opponent = b_opp.team
GROUP BY tg.team, b_self.base_margin
ORDER BY adjusted_rating DESC;

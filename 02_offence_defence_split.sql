-- Offence/Defence Split: rank teams separately on attack (points scored)
-- and defence (points conceded). Reveals WHY teams were good.

WITH team_games AS (
    SELECT hteam AS team, hscore AS points_for, ascore AS points_against FROM AFL.PUBLIC.GAMES
    UNION ALL
    SELECT ateam AS team, ascore AS points_for, hscore AS points_against FROM AFL.PUBLIC.GAMES
)
SELECT
    team,
    ROUND(AVG(points_for), 1)                       AS attack,
    ROUND(AVG(points_against), 1)                   AS defence,
    ROUND(AVG(points_for) - AVG(points_against), 1) AS margin,
    RANK() OVER (ORDER BY AVG(points_for) DESC)     AS attack_rank,
    RANK() OVER (ORDER BY AVG(points_against) ASC)  AS defence_rank
FROM team_games
GROUP BY team
ORDER BY margin DESC;

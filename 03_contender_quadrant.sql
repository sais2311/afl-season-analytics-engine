/*
Contender Quadrant: attack vs defence coordinates for all 18 teams.
*/

WITH team_games AS (
    SELECT hteam AS team, hscore AS points_for, ascore AS points_against FROM AFL.PUBLIC.GAMES
    UNION ALL
    SELECT ateam AS team, ascore AS points_for, hscore AS points_against FROM AFL.PUBLIC.GAMES
)
SELECT team, AVG(points_for) AS attack, AVG(points_against) AS defence
FROM team_games
GROUP BY team;

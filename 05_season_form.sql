-- Season Form: 5-game rolling average margin per team, round by round.
-- Reveals who surged into finals and who faded.

WITH team_games AS (
    SELECT hteam AS team, round, hscore - ascore AS margin FROM AFL.PUBLIC.GAMES
    UNION ALL
    SELECT ateam AS team, round, ascore - hscore AS margin FROM AFL.PUBLIC.GAMES
)
SELECT
    team,
    round,
    margin,
    ROUND(
        AVG(margin) OVER (
            PARTITION BY team
            ORDER BY round
            ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
        ), 1
    ) AS rolling_form_5
FROM team_games
ORDER BY team, round;

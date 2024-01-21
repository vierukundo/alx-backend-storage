--  script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for each student
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN u_id INT)
BEGIN
    UPDATE users
    SET average_score = (
        SELECT IFNULL(SUM(corrections.score * projects.weight) / SUM(projects.weight), 0) AS av
        FROM projects
        JOIN corrections ON corrections.project_id = projects.id
        WHERE user_id = u_id
    )
    WHERE id = u_id;
END//
DELIMITER ;

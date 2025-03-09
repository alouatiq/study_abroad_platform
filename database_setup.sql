CREATE DATABASE IF NOT EXISTS study_abroad_db;

CREATE USER IF NOT EXISTS 'portfolio_dev' @'localhost' IDENTIFIED BY 'portfolio_dev_pwd';

GRANT ALL PRIVILEGES ON study_abroad_db.* TO 'portfolio_dev' @'localhost';

GRANT
SELECT
    ON performance_schema.* TO 'portfolio_dev' @'localhost';
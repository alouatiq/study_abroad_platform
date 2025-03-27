-- Create the main project database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS study_abroad_db;

-- Create a local user for development purposes with a secure password
CREATE USER IF NOT EXISTS 'portfolio_dev'@'localhost' IDENTIFIED BY 'portfolio_dev_pwd';

-- Grant full privileges on the project database to the new user
GRANT ALL PRIVILEGES ON study_abroad_db.* TO 'portfolio_dev'@'localhost';

-- Grant SELECT permission on performance_schema for monitoring queries (optional, safe)
GRANT SELECT ON performance_schema.* TO 'portfolio_dev'@'localhost';

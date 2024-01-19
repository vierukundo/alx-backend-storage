-- This script creates a table with these attributes:
-- id, integer, never null, auto increment and primary key
-- email, string (255 characters), never null and unique
-- name, string (255 characters)

-- Create the users table
CREATE TABLE IF NOT EXISTS users (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        email CHAR(255) NOT NULL UNIQUE,
        name CHAR(255)
);

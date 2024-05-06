CREATE DATABASE IF NOT EXISTS `reviewspot-db`;
USE `reviewspot-db`;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS businesses;

SET FOREIGN_KEY_CHECKS = 1;

-- Create the 'businesses' table
CREATE TABLE businesses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    address VARCHAR(100),
    phone VARCHAR(20),
    owner_id VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state CHAR(2) NOT NULL,
    zip_code CHAR(5) NOT NULL
);

-- Create the 'reviews' table
CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rating FLOAT NOT NULL CHECK (rating BETWEEN 0 AND 5),
    comment TEXT,
    business_id INT NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    FOREIGN KEY (business_id) REFERENCES businesses(id) ON DELETE CASCADE
);


-- maybe add these
-- CREATE INDEX idx_business_owner ON businesses(owner_id);
-- CREATE INDEX idx_review_user ON reviews(user_id);
-- CREATE INDEX idx_review_business ON reviews(business_id);
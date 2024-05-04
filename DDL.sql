CREATE TABLE businesses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    address VARCHAR(100),
    phone VARCHAR(20),
    owner_id VARCHAR(50) NOT NULL
);

CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rating FLOAT NOT NULL,
    comment TEXT,
    business_id INT NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    FOREIGN KEY (business_id) REFERENCES businesses(id)
);
-- Create db tables in production server

CREATE TABLE user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(64),
    email VARCHAR(64),
    password VARCHAR(64)
);
CREATE TABLE tutor (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(64),
    email VARCHAR(64),
    phone_number VARCHAR(10),
    pay INT,
    description VARCHAR(10000),
    subject VARCHAR(100),
    grade INT,
    average_stars INT,
    image VARCHAR(5000),
    num_stars INT
);
CREATE TABLE review (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tutor_id INT,
    title VARCHAR(250),
    username VARCHAR(64),
    rating INT,
    content VARCHAR(10000)
);

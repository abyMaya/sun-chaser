DROP DATABASE SUN_Chaser;
DROP USER 'admin';

CREATE USER 'admin' IDENTIFIED BY 'chaser';
CREATE DATABASE SUN_Chaser;
USE SUN_Chaser;
GRANT ALL PRIVILEGES ON gutara_chat.* TO 'admin';

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY
);
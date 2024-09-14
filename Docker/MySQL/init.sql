DROP DATABASE SUN_Chaser;
DROP USER 'admin';

CREATE USER 'admin' IDENTIFIED BY 'chaser';
CREATE DATABASE SUN_Chaser;
USE SUN_Chaser;
GRANT ALL PRIVILEGES ON SUN_Chaser.* TO 'admin';

CREATE TABLE Users (
    user_id VARCHAR(255) PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE Regions(
    region_id INT PRIMARY KEY AUTO_INCREMENT,
    region_name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE WeatherStations(
    station_id INT PRIMARY KEY AUTO_INCREMENT,
    station_name  VARCHAR(255) NOT NULL UNIQUE,
    region_id INT NOT NULL,
    FOREIGN KEY (region_id) REFERENCES Regions(region_id)
);

CREATE TABLE Spots(
    spot_id INT PRIMARY KEY AUTO_INCREMENT,
    spot_name VARCHAR(255) NOT NULL UNIQUE,
    region_id INT NOT NULL,
    station_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (region_id) REFERENCES Regions(region_id),
    FOREIGN KEY (station_id) REFERENCES WeatherStations(station_id)
);

CREATE TABLE WeatherData(
    weather_id INT PRIMARY KEY AUTO_INCREMENT,
    station_id INT NOT NULL,
    weather_date DATETIME NOT NULL,
    sunny_rate DECIMAL(5,4),
    cloudy_rate DECIMAL(5,4),
    rainny_rate DECIMAL(5,4),
    FOREIGN KEY (station_id) REFERENCES WeatherStations(station_id)
);



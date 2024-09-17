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

-- Regions WeatherStationsマスタ登録
-- https://www.data.jma.go.jp/tokyo/shosai/chiiki/tenki/47670yokohama.html
INSERT INTO Regions VALUES (0, '関東甲信地方');
INSERT INTO Regions VALUES (0, '東海地方');
INSERT INTO Regions VALUES (0, '北陸地方');

INSERT INTO WeatherStations VALUES (0, '東京', 1);
INSERT INTO WeatherStations VALUES (0, '横浜', 1);
INSERT INTO WeatherStations VALUES (0, '銚子', 1);
INSERT INTO WeatherStations VALUES (0, '熊谷', 1);
INSERT INTO WeatherStations VALUES (0, '水戸', 1);
INSERT INTO WeatherStations VALUES (0, '宇都宮', 1);
INSERT INTO WeatherStations VALUES (0, '前橋', 1);
INSERT INTO WeatherStations VALUES (0, '長野', 1);
INSERT INTO WeatherStations VALUES (0, '甲府', 1);

INSERT INTO WeatherStations VALUES (0, '静岡', 2);
INSERT INTO WeatherStations VALUES (0, '名古屋', 2);
INSERT INTO WeatherStations VALUES (0, '岐阜', 2);
INSERT INTO WeatherStations VALUES (0, '津', 2);

INSERT INTO WeatherStations VALUES (0, '新潟', 3);
INSERT INTO WeatherStations VALUES (0, '富山', 3);
INSERT INTO WeatherStations VALUES (0, '金沢', 3);
INSERT INTO WeatherStations VALUES (0, '福井', 3);





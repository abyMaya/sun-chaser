DROP DATABASE SUN_Chaser;
DROP USER 'admin';

CREATE USER 'admin' IDENTIFIED BY 'chaser';
CREATE DATABASE SUN_Chaser;
USE SUN_Chaser;
GRANT ALL PRIVILEGES ON SUN_Chaser.* TO 'admin';

CREATE TABLE Users (
    user_id CHAR(36) PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at BIGINT,
    updated_at BIGINT
);

CREATE TABLE Regions(
    region_id INT PRIMARY KEY AUTO_INCREMENT,
    region_name VARCHAR(255) NOT NULL UNIQUE,
    created_at BIGINT,
    updated_at BIGINT
);

CREATE TABLE WeatherStations(
    station_id INT PRIMARY KEY AUTO_INCREMENT,
    station_name  VARCHAR(255) NOT NULL UNIQUE,
    region_id INT NOT NULL,
    FOREIGN KEY (region_id) REFERENCES Regions(region_id),
    created_at BIGINT,
    updated_at BIGINT
);

CREATE TABLE Spots(
    spot_id INT PRIMARY KEY AUTO_INCREMENT,
    spot_name VARCHAR(255) NOT NULL UNIQUE,
    region_id INT NOT NULL,
    FOREIGN KEY (region_id) REFERENCES Regions(region_id),
    station_id INT NOT NULL,
    FOREIGN KEY (station_id) REFERENCES WeatherStations(station_id),
    created_at BIGINT,
    updated_at BIGINT    
);

CREATE TABLE WeatherData(
    weather_id INT PRIMARY KEY AUTO_INCREMENT,
    station_id INT NOT NULL,
    FOREIGN KEY (station_id) REFERENCES WeatherStations(station_id),
    weather_date DATE NOT NULL,
    sunny_rate DECIMAL(4,2),
    cloudy_rate DECIMAL(4,2),
    rainny_rate DECIMAL(4,2)   
);

CREATE TABLE UsersSpots(
    users_spot_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id CHAR(36) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    spot_id INT NOT NULL,
    FOREIGN KEY (spot_id) REFERENCES Spots(spot_id),
    created_at BIGINT,
    updated_at BIGINT    
);

-- Regions WeatherStationsマスタ登録
-- https://www.data.jma.go.jp/tokyo/shosai/chiiki/tenki/47670yokohama.html
INSERT INTO Regions VALUES (0, '関東甲信地方', UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO Regions VALUES (0, '東海地方', UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO Regions VALUES (0, '北陸地方', UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

INSERT INTO WeatherStations VALUES (0, '東京', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO WeatherStations VALUES (0, '横浜', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO WeatherStations VALUES (0, '銚子', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO WeatherStations VALUES (0, '熊谷', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO WeatherStations VALUES (0, '水戸', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO WeatherStations VALUES (0, '宇都宮', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO WeatherStations VALUES (0, '前橋', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO WeatherStations VALUES (0, '長野', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO WeatherStations VALUES (0, '甲府', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

INSERT INTO WeatherStations VALUES (0, '静岡', 2, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO WeatherStations VALUES (0, '名古屋', 2, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO WeatherStations VALUES (0, '岐阜', 2, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO WeatherStations VALUES (0, '津', 2, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

INSERT INTO WeatherStations VALUES (0, '新潟', 3, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO WeatherStations VALUES (0, '富山', 3, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO WeatherStations VALUES (0, '金沢', 3, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO WeatherStations VALUES (0, '福井', 3, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- Spots テーブルに初期データを挿入
INSERT INTO Spots (spot_name, region_id, station_id, created_at, updated_at) VALUES 
('東京タワー', 1, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('横浜ランドマークタワー', 1, 2, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('銚子電鉄犬吠埼駅', 1, 3, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('静岡浅間神社', 2, 10, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('名古屋城', 2, 11, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('富山黒部峡谷鉄道', 3, 13, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('金沢21世紀美術館', 3, 15, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
('上高地', 1, 8, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- WeatherData.csv挿入
LOAD DATA INFILE '/docker-entrypoint-initdb.d/weatherdata_1.csv'
INTO TABLE WeatherData
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(station_id, weather_date, sunny_rate, cloudy_rate, rainny_rate);


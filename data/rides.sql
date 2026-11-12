USE users;

CREATE TABLE rides (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    bike_id INT NOT NULL,
    
    ride_date DATE NOT NULL,
    start_time TIME NOT NULL,
    full_time TIME NOT NULL,
    
    distance DECIMAL(5,1) NOT NULL,
    elevation DECIMAL(5,1) NOT NULL,
    avg_speed DECIMAL(5,1) NOT NULL,
    max_speed DECIMAL(5,1) NOT NULL,
    temperature DECIMAL(5,1) NOT NULL,
    humidity DECIMAL(5,1) NOT NULL,
    wind DECIMAL(5,1) NOT NULL,
    
    weather JSON,
    surface JSON,
    notes TEXT,
    
	PRIMARY KEY (id),

    CONSTRAINT fk_rides_users
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
        
	CONSTRAINT fk_rides_bikes
		FOREIGN KEY (bike_id)
        REFERENCES bikes(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

SHOW TABLES;
DESCRIBE rides;
SELECT *FROM rides;
SHOW CREATE TABLE rides;
TRUNCATE TABLE rides;

ALTER TABLE rides
ADD COLUMN ride_name VARCHAR(150) AFTER bike_id;

ALTER TABLE rides
ADD COLUMN gpx_file VARCHAR(255) NULL AFTER notes;
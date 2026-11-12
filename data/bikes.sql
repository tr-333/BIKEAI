USE users;

CREATE TABLE bikes (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,

    bike_type VARCHAR(30),
    brand VARCHAR(100),
    model VARCHAR(100),
    production_year YEAR,
    purchase_year YEAR,
    frame_size VARCHAR(30),
    

    handlebar_type VARCHAR(30),
    shifting_type VARCHAR(40),
    brake_control VARCHAR(40),

    brake_type VARCHAR(40),
    brake_model VARCHAR(150),
    brake_rotors VARCHAR(150),

    front_gears TINYINT,
    rear_gears TINYINT,
    drivetrain_brand VARCHAR(100),
    drivetrain_model VARCHAR(100),
    chain VARCHAR(150),
    cassette VARCHAR(150),
    crankset VARCHAR(150),
    bottom_bracket VARCHAR(150),

    wheel_size VARCHAR(10),
    front_hub VARCHAR(150),
    rear_hub VARCHAR(150),

    tire_brand VARCHAR(100),
    tire_model VARCHAR(150),
    tire_width SMALLINT,

    PRIMARY KEY (id),

    CONSTRAINT fk_bikes_users
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

SHOW TABLES;
DESCRIBE bikes;
SELECT *FROM bikes;
SHOW CREATE TABLE bikes;
TRUNCATE TABLE bikes;

ALTER TABLE bikes
ADD COLUMN initial_mileage INT AFTER frame_size;


ALTER TABLE bikes
ADD COLUMN maintenance VARCHAR(30),
ADD COLUMN shifting_mechanism VARCHAR(30),
ADD COLUMN shifting_model VARCHAR(150),
ADD COLUMN rear_shifting_model VARCHAR(150),

ADD COLUMN shifting_replacement_date DATE,
ADD COLUMN shifting_mileage INT,

ADD COLUMN rear_shifting_replacement_date DATE,
ADD COLUMN rear_shifting_mileage INT,

ADD COLUMN crankset_replacement_date DATE,
ADD COLUMN crankset_mileage INT,

ADD COLUMN cassette_replacement_date DATE,
ADD COLUMN cassette_mileage INT,

ADD COLUMN chain_replacement_date DATE,
ADD COLUMN chain_mileage INT,

ADD COLUMN bottom_bracket_replacement_date DATE,
ADD COLUMN bottom_bracket_mileage INT,

ADD COLUMN kind_pads VARCHAR(40),

ADD COLUMN brake_model_replacement_date DATE,
ADD COLUMN brake_model_mileage INT,

ADD COLUMN rear_brake_model VARCHAR(150),
ADD COLUMN rear_brake_model_replacement_date DATE,
ADD COLUMN rear_brake_model_mileage INT,

ADD COLUMN brake_rotors_replacement_date DATE,
ADD COLUMN brake_rotors_mileage INT,

ADD COLUMN rear_brake_rotors VARCHAR(150),
ADD COLUMN rear_brake_rotors_replacement_date DATE,
ADD COLUMN rear_brake_rotors_mileage INT,

ADD COLUMN brake_pads VARCHAR(150),
ADD COLUMN brake_pads_replacement_date DATE,
ADD COLUMN brake_pads_mileage INT,

ADD COLUMN rear_brake_pads VARCHAR(150),
ADD COLUMN rear_brake_pads_replacement_date DATE,
ADD COLUMN rear_brake_pads_mileage INT,

ADD COLUMN front_hub_replacement_date DATE,
ADD COLUMN front_hub_mileage INT,

ADD COLUMN rear_hub_replacement_date DATE,
ADD COLUMN rear_hub_mileage INT,

ADD COLUMN tire_replacement_date DATE,
ADD COLUMN tire_mileage INT,

ADD COLUMN rear_tire_brand VARCHAR(100),
ADD COLUMN rear_tire_model VARCHAR(150),
ADD COLUMN rear_tire_width SMALLINT,

ADD COLUMN rear_tire_replacement_date DATE,
ADD COLUMN rear_tire_mileage INT;

ALTER TABLE bikes
CHANGE COLUMN brake_model_replacement_date brake_replacement_date DATE,
CHANGE COLUMN brake_model_mileage brake_mileage INT,
CHANGE COLUMN rear_brake_model_replacement_date rear_brake_replacement_date DATE,
CHANGE COLUMN rear_brake_model_mileage rear_brake_mileage INT;
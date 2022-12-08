-- Active: 1670168866705@@127.0.0.1@3306@pr2-- Active: 1670168866705@@127.0.0.1@3306
/*CREATE DATABASE pr2;*/

CREATE TABLE Home (
    homeid int NOT NULL AUTO_INCREMENT,
    name varchar(100) NOT NULL,
    address varchar(100),
    description varchar(100),
    home_ownerid int,
    PRIMARY KEY (homeid)
);

CREATE TABLE Sensor (
    sensorID varchar(50) NOT NULL,
    room VARCHAR(100),
    homeid int not null,
    PRIMARY KEY (sensorID)
);

CREATE TABLE Home_Owner (
    home_ownerid int not null AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(50),
    PRIMARY KEY (home_ownerid)
);


INSERT INTO Home_Owner (name, password) VALUES ('Default USER', '1234');
INSERT INTO Home (name, address, description, home_ownerid) VALUES ('Casa principal', 'Lleida', 'Casa Familiar', 1);
INSERT INTO Sensor (sensorID, room, homeid) VALUES ('Temperatura1', 'Menjador', 1);
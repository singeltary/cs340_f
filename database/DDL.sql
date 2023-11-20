SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

--creating table for Donors
DROP TABLE IF EXISTS Donors;
CREATE TABLE Donors (
	donorID int AUTO_INCREMENT,
	name varchar(48) NOT NULL,
	street varchar(48) NOT NULL,
	city varchar(30) NOT NULL,
	state_ab char(2) NOT NULL,
	zip char(5) NOT NULL,
	bloodType varchar(3) NOT NULL,
	PRIMARY KEY (donorID)
);

--donations table. 
DROP TABLE IF EXISTS Donations;
CREATE TABLE Donations (
	donationID int AUTO_INCREMENT,
	name varchar(48) NOT NULL,
	quantity float NOT NULL,
	date datetime NOT NULL,	
	donorID int NOT NULL,
	bloodType varchar(3) NOT NULL,
	PRIMARY KEY (donationID),
	FOREIGN KEY (donorID) REFERENCES Donors(donorID),
	FOREIGN KEY (bloodType) REFERENCES Bloodstock(bloodType) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Bloodstock;
CREATE TABLE Bloodstock (
	bloodType varchar(3) NOT NULL,
	quantity float NOT NULL DEFAULT 0,
	PRIMARY KEY (bloodType)
);

DROP TABLE IF EXISTS Recipients;
CREATE TABLE Recipients (
	recipientID int AUTO_INCREMENT,
	name varchar(48) NOT NULL,
	street varchar(48) NOT NULL,
	city varchar(30) NOT NULL,
	state_ab char(2) NOT NULL,
	zip char(5) NOT NULL,
	PRIMARY KEY (recipientID)
);

DROP TABLE IF EXISTS Transfers;
CREATE TABLE Transfers (
	transferID int AUTO_INCREMENT,
	date datetime NOT NULL,
	quantity float NOT NULL,
	recipientID int NOT NULL,
	bloodType varchar(3) NOT NULL,
	FOREIGN KEY (recipientID) REFERENCES Recipients(recipientID) ON DELETE CASCADE,
	FOREIGN KEY (bloodType) REFERENCES Bloodstock(bloodType) ON DELETE CASCADE,
	PRIMARY KEY (transferID)
);

INSERT INTO Bloodstock (bloodType) 
VALUES ('A+'), ('A-'), ('B+'), ('B-'), ('AB+'), ('AB-'), ('O+'), ('O-');

INSERT INTO Donors (name, street, city, state_ab, zip, bloodType)
VALUES ('Eddie Lee Capers', '927 Cascade St', 'Columbia', 'MD', '20854', 'A+'),
('JW Stillwater', '6829 Glengarry Ct', 'Elkridge', 'MD', '21053', 'B+'),
('Leo Carpazzi', '2011 Clipper Rd', 'Baltimore', 'MD', '21211', 'AB-'),
('Dabney Coleperson', '2048 Sleddington Ct', 'Dublin', 'MD', '21032', 'O-'),
('Bob Ducca', '413 Hollywood Dr', 'Crownsville', 'MD', '21032', 'A-');

INSERT INTO Donations (name, quantity, date, donorID, bloodType) 
VALUES ('JW Stillwater', 22.1, 20231005, (SELECT donorID FROM Donors WHERE name = 'JW Stillwater'), (SELECT bloodType FROM Donors WHERE name = 'JW Stillwater')),
('Dabney Coleperson', 3.2, 20220214, (SELECT donorID FROM Donors WHERE name = 'Dabney Coleperson'), (SELECT bloodType FROM Donors WHERE name = 'Dabney Coleperson')),
('Leo Carpazzi', 1.4, 20220626, (SELECT donorID FROM Donors WHERE name = 'Leo Carpazzi'), (SELECT bloodType FROM Donors WHERE name = 'Leo Carpazzi')),
('Bob Ducca', 2.7, 20230505, (SELECT donorID FROM Donors WHERE name = 'Bob Ducca'), (SELECT bloodType FROM Donors WHERE name = 'Bob Ducca'));

INSERT INTO Recipients (name, street, city, state_ab, zip)
VALUES ('Lidsville Memorial', '53 Merlo St', 'Millers Crossing', 'MD', '21205'),
('Shady Grove Hospital', '361 Barnacle St', 'Bayonne', 'MD', '21513'),
('North Left Birthing Barn', '277 Carrion St', 'Marzipan', 'MD', '29413'),
('Gabbo Elective Surgery', '51 Syrup Cir', 'Sharktooth', 'MD', '25162');

INSERT INTO Transfers (date, quantity, recipientID, bloodType)
VALUES (20190505, 2533.1, (SELECT recipientID FROM Recipients WHERE name = 'Lidsville Memorial'), 'O+'),
(20210525, 534.1, (SELECT recipientID FROM Recipients WHERE name = 'North Left Birthing Barn'), 'AB+'),
(20230101, 15316.2, (SELECT recipientID FROM Recipients WHERE name = 'Gabbo Elective Surgery'), 'O-');

SET FOREIGN_KEY_CHECKS=1;
COMMIT;

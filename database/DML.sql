

--get blood types for blood type inputs
SELECT type FROM Bloodstock;

--RECIPIENTS
--add recipient org
INSERT INTO Recipients (name, street, city, state, zip) VALUES
(:nameInput, :streetInput, :cityInput, :stateInput, :zipInput);

--update recipient
UPDATE Recipients SET name=:nameInput, street=:streetInput, city=:cityInput, state=:stateInput, zip=:zipInput WHERE recipientID = :recipientID_from_form

--display Recipients
SELECT * FROM Recipients;

--display 1 recipient. for update/delete
SELECT recipientID, name, street, city, state, zip FROM Recipients WHERE recipientID=:recipientID_from_menu

--remove recipient
DELETE FROM Recipients WHERE recipientID = :recipientID_selected_from_Recipients_page

--TRANSFERS
--display Transfers based on date
SELECT transferID, quantity, recipientID, type FROM Transfers WHERE date = :dateFromInput;

--display Transfers based on recipient
SELECT transferID, quantity, type FROM Transfers WHERE recipientID=:recipientID_from_menu

--add transfer
INSERT INTO Transfers (quantity, date, recipientID, type) VALUES
(:quantityInput, :dateInput, :recipientIDInput, :typeInput);

--update transfer
UPDATE Transfers SET quantity=:quantityInput, date=:dateInput, recipientID=:recipientIDInput, type=:typeInput) WHERE transferID = :transferID_from_form

--DONORS
--add donor
INSERT INTO Donors (name, street, city, state, zip, type) VALUES
(:nameInput, :streetInput, :cityInput, :stateInput, :zipInput, typeInput);

--update donor information on Update Donor Form
UPDATE Donors SET name=:nameInput, street=:streetInput, city=:cityInput, state=:stateInput, zip=:zipInput, type=:typeInput WHERE donorID = :donorID_from_form

--display all Donors
SELECT * FROM Donors;

--find donor by name. for update/delete
SELECT donorID, name, street, city, state, zip, type FROM Donors WHERE name = :nameInput

--remove donor
DELETE FROM Donors WHERE id = :donorID_selected_from_menu

--DONATIONS
--new donation
INSERT INTO Donations VALUES (name, date, quantity, donorID, type) VALUES
((SELECT name FROM Donors WHERE donorID = :donorIDInput), :dateInput, :quantityInput, (SELECT type FROM Donors WHERE donorID = :donorIDInput));

--update donation
UPDATE Donations SET name=:nameInput, quantity=:quantityInput, donorID=:donorIDInput, type=:typeInput WHERE donationID = :donationID_from_form

--BLOODSTOCK
--update Bloodstock
UPDATE Bloodstock SET quantity=:quantityInput WHERE type = :typeInput_from_form


--DONOR-RECIPIENT TABLES
--display Donors/Donations/Recipients based on date, type, i.e., where'd your blood end up?
SELECT donorID, name, type AS Donors FROM Donors
JOIN Donations ON Donations.type = Donors.type
JOIN Transfers ON Transfers.type = Donations.type AND Donations.date <= Transfers.date
JOIN Recipients ON Recipients.recipientID = Transfers.recipientID
ORDER BY name ASC;





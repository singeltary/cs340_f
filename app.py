import os

from flask import Flask, json, redirect, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_singeltb"
app.config["MYSQL_PASSWORD"] = "0566"  # last 4 of onid
app.config["MYSQL_DB"] = "cs340_singeltb"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"


mysql = MySQL(app)


# Routes
@app.route("/")
def root():
    return render_template("main.j2")


@app.route("/donors", methods=["GET", "POST"])
def donors():
    query1 = "SELECT * FROM Donors;"
    cur = mysql.connection.cursor()
    cur.execute(query1)
    results = cur.fetchall()
    return render_template("donors.j2", people=results)


@app.route("/add_donor", methods=["POST", "GET"])
def add_donor():
    if request.method == "POST":
        name = request.form.get("name")
        street = request.form.get("street")
        city = request.form.get("city")
        state_ab = request.form.get("state")
        zip = request.form.get("zip")
        bloodType = request.form.get("type")

        query_add = "INSERT INTO Donors (name, street, city, state_ab, zip, bloodType) VALUES (%s, %s, %s, %s, %s, %s);"
        cur = mysql.connection.cursor()
        cur.execute(query_add, (name, street, city, state_ab, zip, bloodType))
        mysql.connection.commit()
        return redirect("/donors")


@app.route("/update_donor/<int:donorID>", methods=["GET", "POST"])
def update_donor(donorID):
    if request.method == "GET":
        query1 = "SELECT * FROM Donors WHERE donorID = %s" % donorID
        cur = mysql.connection.cursor()
        cur.execute(query1)
        results = cur.fetchall()
        return render_template("update_donor.j2", donor=results)
    if request.method == "POST":
        name = request.form.get("name")
        street = request.form.get("street")
        city = request.form.get("city")
        state_ab = request.form.get("state")
        zip = request.form.get("zip")
        bloodType = request.form.get("type")
        query2 = "UPDATE Donors SET Donors.name = %s, Donors.street = %s, Donors.city = %s, Donors.state_ab = %s, Donors.zip = %s, Donors.bloodType = %s WHERE Donors.donorID = %s"

        cur = mysql.connection.cursor()
        cur.execute(query2, (name, street, city, state_ab, zip, bloodType, donorID))
        mysql.connection.commit()
        return redirect("/donors")


@app.route("/delete_donor/<int:donorID>", methods=["GET", "POST"])
def delete_donor(donorID):
    query_del = "DELETE FROM Donors WHERE donorID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query_del, (donorID,))
    mysql.connection.commit()
    return redirect("/donors")


@app.route("/bloodstock", methods=["GET"])
def bloodstock():
    query1 = "SELECT * FROM Bloodstock;"
    cur = mysql.connection.cursor()
    cur.execute(query1)
    results = cur.fetchall()
    return render_template("bloodstock.j2", blood=results)


@app.route("/add_bloodstock", methods=["POST"])
def add_bloodstock():
    bloodType = request.form.get("type")
    quantity = request.form.get("quantity")

    query_add = "INSERT INTO Bloodstock (bloodType, quantity) VALUES (%s, %s);"
    cur = mysql.connection.cursor()
    cur.execute(query_add, (bloodType, quantity))
    mysql.connection.commit()
    return redirect("/bloodstock")


@app.route("/update_bloodstock/<string:blood_type>", methods=["GET", "POST"])
def update_bloodstock(blood_type):
    if request.method == "GET":
        query1 = "SELECT * FROM Bloodstock WHERE bloodType = '%s'" % blood_type
        cur = mysql.connection.cursor()
        cur.execute(
            query1,
        )
        results = cur.fetchall()
        return render_template("update_bloodstock.j2", blood=results)
    if request.method == "POST":
        quantity = request.form.get("quantity")
        query2 = "UPDATE Bloodstock SET Bloodstock.quantity = %s WHERE Bloodstock.bloodType = %s"

        cur = mysql.connection.cursor()
        cur.execute(query2, (quantity, blood_type))
        mysql.connection.commit()
        return redirect("/bloodstock")


@app.route("/delete_bloodstock/<string:blood_type>", methods=["GET", "POST"])
def delete_bloodstock(blood_type):
    query_del = "DELETE FROM Bloodstock WHERE bloodType = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query_del, (blood_type,))
    mysql.connection.commit()
    return redirect("/bloodstock")


@app.route("/donations", methods=["GET"])
def donations():
    query1 = "SELECT * FROM Donations;"
    cur = mysql.connection.cursor()
    cur.execute(query1)
    results = cur.fetchall()
    return render_template("donations.j2", donations=results)


@app.route("/add_donation", methods=["POST"])
def add_donation():
    donorID = request.form.get("donorID")
    type = request.form.get("type")
    quantity = request.form.get("quantity")
    date = request.form.get("date")

    query_add = (
        "INSERT INTO Donations (donorID, type, quantity, date) VALUES (%s, %s, %s, %s);"
    )
    cur = mysql.connection.cursor()
    cur.execute(query_add, (donorID, type, quantity, date))
    mysql.connection.commit()
    return redirect("/donations")


@app.route("/update_donation/<int:donationID>", methods=["GET", "POST"])
def update_donation(donationID):
    if request.method == "GET":
        query1 = "SELECT * FROM Donations WHERE donationID = %s" % donationID
        cur = mysql.connection.cursor()
        cur.execute(query1)
        results = cur.fetchall()
        donors_query = "SELECT donorID FROM Donors;"
        cur.execute(donors_query)
        donors = cur.fetchall()
        return render_template("update_donation.j2", donation=results, donors=donors)
    if request.method == "POST":
        donorID = request.form.get("donorID")
        type = request.form.get("bloodType")
        quantity = request.form.get("quantity")
        date = request.form.get("donationDate")
        query2 = "UPDATE Donations SET Donations.donorID = %s, Donations.bloodType = %s, Donations.quantity = %s, Donations.date = %s WHERE Donations.donationID = %s"

        cur = mysql.connection.cursor()
        cur.execute(query2, (donorID, type, quantity, date, donationID))
        mysql.connection.commit()
        return redirect("/donations")


@app.route("/delete_donation/<int:donationID>", methods=["GET", "POST"])
def delete_donation(donationID):
    query_del = "DELETE FROM Donations WHERE donationID = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query_del, (donationID,))
    mysql.connection.commit()
    return redirect("/donations")


@app.route("/recipients", methods=["GET", "POST"])
def recipients():
    query_rec = "SELECT * FROM Recipients;"
    cur = mysql.connection.cursor()
    cur.execute(query_rec)
    results = cur.fetchall()
    return render_template("recipients.j2", recipients=results)


@app.route("/add_recipient", methods=["POST"])
def add_recipient():
    if request.method == "POST":
        name = request.form.get("name")
        street = request.form.get("street")
        city = request.form.get("city")
        state_ab = request.form.get("state")
        zip = request.form.get("zip")

        query_add = "INSERT INTO Recipients (name, street, city, state_ab, zip) VALUES (%s, %s, %s, %s, %s);"
        cur = mysql.connection.cursor()
        cur.execute(query_add, (name, street, city, state_ab, zip))
        mysql.connection.commit()
        return redirect("/recipients")


@app.route("/update_recipient/<int:recipientID>", methods=["GET", "POST"])
def update_recipient(recipientID):
    if request.method == "GET":
        query1 = "SELECT * FROM Recipients WHERE recipientID = %s" % recipientID
        cur = mysql.connection.cursor()
        cur.execute(query1)
        results = cur.fetchall()
        return render_template("update_recipient.j2", recipient=results)
    if request.method == "POST":
        name = request.form.get("name")
        street = request.form.get("street")
        city = request.form.get("city")
        state_ab = request.form.get("state")
        zip = request.form.get("zip")
        query2 = "UPDATE Recipients SET Recipients.name = %s, Recipients.street = %s, Recipients.city = %s, Recipients.state_ab = %s, Recipients.zip = %s WHERE Recipients.recipientID = %s"

        cur = mysql.connection.cursor()
        cur.execute(query2, (name, street, city, state_ab, zip, recipientID))
        mysql.connection.commit()
        return redirect("/recipients")


@app.route("/delete_recipient/<int:recipientID>", methods=["GET", "POST"])
def delete_recipient(recipientID):
    query_del = "DELETE FROM Recipients WHERE recipientID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query_del, (recipientID,))
    mysql.connection.commit()
    return redirect("/recipients")


@app.route("/transfers", methods=["GET", "POST"])
def transfers():
    if request.method == "GET":
        query_t = "SELECT * FROM Transfers;"
        cur = mysql.connection.cursor()
        cur.execute(query_t)
        results = cur.fetchall()
        return render_template("transfers.j2", transfers=results)


@app.route("/add_transfer", methods=["GET", "POST"])
def add_transfer():
    if request.method == "POST":
        date = request.form.get("date")
        quantity = request.form.get("quantity")
        recipientID = request.form.get("recipientID")
        bloodType = request.form.get("type")

        query_add = "INSERT INTO Transfers (date, quantity, recipientID, bloodType) VALUES (%s, %s, %s, %s);"
        cur = mysql.connection.cursor()
        cur.execute(query_add, (date, quantity, recipientID, bloodType))
        mysql.connection.commit()
        return redirect("/transfers")


@app.route("/update_transfer/<int:transferID>", methods=["GET", "POST"])
def update_transfer(transferID):
    if request.method == "GET":
        query1 = "SELECT * FROM Transfers WHERE transferID = %s" % transferID
        cur = mysql.connection.cursor()
        cur.execute(query1)
        results = cur.fetchall()
        recipient_query = "SELECT recipientID FROM Recipients;"
        cur.execute(recipient_query)
        recipients = cur.fetchall()
        return render_template(
            "update_transfer.j2", transfer=results, recipients=recipients
        )
    if request.method == "POST":
        date = request.form.get("date")
        recipientID = request.form.get("recipientID")
        quantity = request.form.get("quantity")
        bloodType = request.form.get("type")
        query2 = "UPDATE Transfers SET Transfers.date = %s, Transfers.quantity = %s, Transfers.recipientID = %s, Transfers.bloodType = %s WHERE Transfers.transferID = %s"

        cur = mysql.connection.cursor()
        cur.execute(query2, (date, quantity, recipientID, bloodType, transferID))
        mysql.connection.commit()
        return redirect("/transfers")


@app.route("/delete_transfer/<int:transferID>", methods=["GET", "POST"])
def delete_transfer(transferID):
    query_del = "DELETE FROM Transfers WHERE transferID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query_del, (transferID,))
    mysql.connection.commit()
    return redirect("/transfers")


# Listener
if __name__ == "__main__":
    app.run(port=21039, debug=True)

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_singeltb'
app.config['MYSQL_PASSWORD'] = '0566' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_singeltb'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)


# Routes
@app.route('/')
def root():
    return render_template("main.j2")
    
@app.route('/donors', methods = ["GET", "POST"])
def donors():
    query1 = 'SELECT * FROM Donors;';
    cur = mysql.connection.cursor()
    cur.execute(query1)
    results = cur.fetchall()
    return render_template("donors.j2", people=results)
    
@app.route('/add_donor', methods=["POST", "GET"])
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
        
@app.route('/update_donor/<int:donorID>', methods=["GET", "POST"])
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
        return redirect('/donors')
        
@app.route('/delete_donor/<int:donorID>', methods=['GET','POST'])
def delete_donor(donorID):
    query_del = "DELETE FROM Donors WHERE donorID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query_del, (donorID,))
    mysql.connection.commit()
    return redirect('/donors')

# Listener
if __name__ == "__main__":
    app.run(port=21039, debug=True)

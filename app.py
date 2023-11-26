from flask import Flask, render_template, json, request, redirect, url_for
import os
import database.db_connector as db
from flask_mysqldb import MySQL

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

#Read Donors
@app.route('/donors', methods=['POST', 'GET'])
def display_donors():
    if request.method == "GET":
        query = "SELECT * FROM Donors;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("donors.j2", people=results)
 
#Create new donor
@app.route('/add_donor', methods=['POST', 'GET'])
def add_donor(): 
    if request.method == "POST":
        name = request.form.get("name")
        street = request.form.get("street")
        city = request.form.get("city")
        state_ab = request.form.get("state")
        zip = request.form.get("zip")
        bloodType = request.form.get("type")
                
        query = "INSERT INTO Donors (name, street, city, state_ab, zip, bloodType) VALUES (%s, %s, %s, %s, %s, %s);"
        cur = db.execute_query(db_connection=db_connection, query=query, query_params=(name, street, city, state_ab, zip, bloodType))
        return redirect("/donors")

#Update donor    
@app.route('/update_donor/<int:donorID>', methods=['GET', 'POST'])
def update_donor(donorID):
    if request.method == "GET":
        query1 = "SELECT * FROM Donors WHERE donorID = %s" % donorID
        cur_get = db.execute_query(db_connection=db_connection, query=query1)
        donor_up = cur_get.fetchall()
        return render_template("update_donor.j2", donor=donor_up)
        
@app.route('/update_donor_c', methods=['GET','POST'])
def update_donor_c():
    if request.method == "POST":
        name = request.form.get("name")
        street = request.form.get("street")
        city = request.form.get("city")
        state_ab = request.form.get("state")
        zip = request.form.get("zip")
        bloodType = request.form.get("type")
        
        query2 = "UPDATE Donors SET Donors.name = %s, Donors.street = %s, Donors.city = %s, Donors.state_ab = %s, Donors.zip = %s, Donors.bloodType = %s WHERE Donors.donorID = %s"
        #cur_post = db.execute_query(db_connection=db_connection, query=query2, query_params=(name, street, city, state_ab, zip, bloodType))
        cur = mysql.connection.cursor()
        cur.execute(query2, (name, street, city, state_ab, zip, bloodType))
        mysql.connection.commit()
        return render_template('success.j2')

#Delete donor
@app.route('/delete_donor/<int:donorID>', methods=['GET','POST'])
def delete_donor(donorID):
    query_del = "DELETE FROM Donors WHERE donorID = '%s';"
    cur_del = db.execute_query(db_connection=db_connection, query=query_del, query_params=(donorID,))
    return render_template('success.j2')

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 21037))
    app.run(port=port, debug=True) 

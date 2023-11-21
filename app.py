from flask import Flask, render_template, json
import os
import database.db_connector as db

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/donors', methods=['POST', 'GET'])
def display_donors():
    if request.method == "GET":
        query = "SELECT * FROM Donors;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("donors.j2", people=results)
        
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

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 21037))
    app.run(port=port, debug=True) 

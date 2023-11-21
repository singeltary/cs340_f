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
    query = "SELECT * FROM Donors;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("donors.j2", people=results)

#@app.route('/add_donor', methods=['POST','GET']
def add_donor():
    if request.method == "POST":
        if request.form.get("add_donor"):
            name = request.form["name"]
            street = request.form["street"]
            city = request.form["city"]
            state_ab = request.form["state"]
            zip = request.form["zip"]
            bloodType = request.form["type"]
                
            query = "INSERT INTO Donors (name, street, city, state_ab, zip, bloodType) VALUES (%s, %s, %s, %s, %s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, street, city, state_ab, zip, bloodType))
            mysql.connection.commit()
            return redirect("/donors")

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 21037))
    app.run(port=port, debug=True) 

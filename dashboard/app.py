from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    conn = sqlite3.connect("../data/db.sqlite3")
    c = conn.cursor()
    c.execute("SELECT * FROM urls ORDER BY timestamp DESC")
    data = c.fetchall()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template
import sqlite3
from database import init_db
from sniffer import start_sniffer

app = Flask(__name__)

init_db()
start_sniffer()

@app.route("/")
def dashboard():

    conn = sqlite3.connect("nids.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM attacks")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT attack, COUNT(*) FROM attacks GROUP BY attack")
    attack_data = cursor.fetchall()

    labels = [row[0] for row in attack_data]
    values = [row[1] for row in attack_data]

    return render_template(
        "dashboard.html",
        total=total,
        labels=labels,
        values=values
    )


@app.route("/logs")
def logs():

    conn = sqlite3.connect("nids.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM attacks ORDER BY time DESC")
    rows = cursor.fetchall()

    return render_template("logs.html", rows=rows)


if __name__ == "__main__":
    app.run(debug=True)
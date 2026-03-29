from flask import Flask, request, render_template
import mysql.connector
import os

app = Flask(__name__)

# Get DB credentials from environment variables
db_config = {
    'host': os.environ.get('RDS_HOST'),
    'user': os.environ.get('RDS_USER'),
    'password': os.environ.get('RDS_PASSWORD'),
    'database': 'microdegree_db'
}

# Ensure DB and table are present
def init_db():
    conn = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password']
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS microdegree_db")
    conn.database = db_config['database']
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            number VARCHAR(20) NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def form():
    message = ""
    if request.method == "POST":
        email = request.form["email"]
        number = request.form["number"]

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, number) VALUES (%s, %s)", (email, number))
        conn.commit()
        cursor.close()
        conn.close()

        message = "Submitted Successfully!"
    return render_template("form.html", message=message)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

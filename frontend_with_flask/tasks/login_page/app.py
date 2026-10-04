from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="signup_db"
        )

        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return "Signup successful!"

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="signup_db"
        )

        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, password)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            return "Login successful!"
        else:
            return "Invalid username or password!"

    return render_template("login.html")


app.run(debug=True)
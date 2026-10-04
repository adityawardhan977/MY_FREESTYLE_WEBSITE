from flask import Flask, render_template, request, redirect
import mysql.connector
import joblib
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup",methods=['GET','POST'])

def post():
    connection=mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="Free_style_website"
    )

    if request.method=="POST":
             
        username=request.form["username"]
        password=request.form["password"]

        cursor=connection.cursor()
        cursor.execute(
        "INSERT INTO signup_table (username,password) VALUES (%s,%s);",
        (username,password)
        )

        connection.commit()

        cursor.close()
        connection.close()
        
        return render_template("home.html")
    
    return render_template("signup.html")

@app.route("/login",methods=['GET','POST'])

def login_post():
    connection=mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="Free_style_website"
    )

    if request.method=='POST':
        username=request.form["username"]
        password=request.form["password"]

        cursor=connection.cursor(buffered=True)
        cursor.execute(
            "SELECT * FROM signup_table WHERE username = %s AND password = %s",
            (username,password)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            return render_template("home.html")
        else:
            return "invalid password"

    return render_template("login.html")

tasks=[]
@app.route("/to_do_list",methods=['GET','POST'])
def list():
    if request.method=='POST':
        task=request.form["to_do_list"]
        tasks.append(task)
        return redirect("/to_do_list")
    
    return render_template("to_do_list.html", tasks=tasks)

@app.route("/delete/<int:index>")
def pop(index):
    tasks.pop(index)
    return redirect("/to_do_list")

@app.route("/drop_out_prediction",methods=["GET","POST"])
def predict():
    if request.method=="POST":
        data={
         "Age":float(request.form["Age"]),
            "Family_Income": float(request.form["Family_Income"]),
            "Household_Size": float(request.form["Household_Size"]),
            "Scholarship": float(request.form["Scholarship"]),
            "Tuition_Base": float(request.form["Tuition_Base"]),
            "Semester": float(request.form["Semester"]),
            "Course_Load": float(request.form["Course_Load"]),
            "Work_Hours": float(request.form["Work_Hours"]),
            "Emergency_Expense": float(request.form["Emergency_Expense"]),
            "Sem_GPA": float(request.form["Sem_GPA"]),
            "Attendance": float(request.form["Attendance"]),
            "LMS_Logins": float(request.form["LMS_Logins"]),
            "Advising_Visits": float(request.form["Advising_Visits"]),
            "Failed_Courses": float(request.form["Failed_Courses"]),
            "Financial_Stress": float(request.form["Financial_Stress"]),
            "Censored": float(request.form["Censored"])
        }

        data=pd.DataFrame([data])

        data["Housing_Status_Off-Campus"]=0
        data["Housing_Status_On-Campus"]=0
        data["Housing_Status_With Parents"]=0

        Housing_Status = request.form["Housing_Status"]

        if Housing_Status=="Off-Campus":
         data["Housing_Status_Off-Campus"]=1
        elif Housing_Status=="On-Campus":
         data["Housing_Status_On-Campus"]=1
        elif Housing_Status=="With Parents":
            data["Housing_Status_With Parents"]=1

        model=joblib.load("logistic_model.pkl")
        feature_columns=joblib.load("feature_columns.pkl")
        scaler=joblib.load("scaler.pkl")

        data=data[feature_columns]

        data=scaler.transform(data)

        prediction=model.predict(data)[0]

        return render_template(
            "drop_out_prediction.html",
            prediction=prediction
        )
    return render_template("drop_out_prediction.html")

app.run(debug=True)
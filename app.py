from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from helpers import login_required
import datetime
import cv2
import pytesseract
#from mytestfiles import image_to_text

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///history.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():    
    
    name = "SYD 5165"
    users = db.execute("SELECT * FROM user_info WHERE car_plate_no=(?)", name)
    for i in range(len(users)):
        db.execute("INSERT INTO info (id, real_name, CLASS, car_plate_no, date) VALUES (?,?,?,?,?)", users[i]["id"], users[i]["real_name"], users[i]["class"], name, datetime.datetime.now())

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return render_template("errorfile.html")
    if request.method == "POST":
        name = request.form.get("email")
        password = request.form.get("password")
        if not name or not password:
            flash("Invalid Username/ Invalid Password")
            return redirect("/login")
        rows = db.execute("SELECT * FROM users WHERE username=(?)", name)
        if (len(rows) != 1 or not check_password_hash(rows[0]["password"], password)):
            flash("Invalid Password")
            return redirect("/login")
            
        session["user_id"] = rows[0]["id"]

        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return render_template("errorfile.html")
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if (password != confirmation):
            flash("Invalid password")
            return redirect("/register")

        else:
            size = db.execute("SELECT username FROM users WHERE username=(?)", name)
            if (len(size) == 1):
                flash('Username is Used')
                return redirect("/register")
            else:
                hash_password = generate_password_hash(password)
                values = db.execute("INSERT INTO users(username, password, registered_date) VALUES (?,?,?)", name, hash_password, datetime.datetime.now())
                flash('Registered!')
                session["user_id"] = values
                return redirect("/")
    else:
        return render_template("register.html")

@app.route("/forgotpassword", methods=["GET", "POST"])
def forgotpassword():
    if "user_id" in session:
        return render_template("errorfile.html")
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        length = db.execute("SELECT username FROM users WHERE username=(?)", name)
        if len(length) != 1:
            flash("Non registered User")
            return redirect("/forgotpassword")
        else:
            hashed = generate_password_hash(password)
            db.execute("UPDATE users SET password=(?)", hashed)
            return redirect("/login")
    else:
        return render_template("forgotpassword.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return render_template("errorfile.html")
    ids = session["user_id"]
    name = db.execute("SELECT username FROM users WHERE id=(?)", ids)
    registered_date = db.execute("SELECT registered_date FROM users WHERE id=(?)", ids)

    if request.method == "POST":
        real_name = request.form.get("real_name")
        # Cannot use class since its a method in Python
        classes = request.form.get("classes")
        student_id = request.form.get("student_id")
        car_plate = request.form.get("car_plate_no")
        
        check_length = db.execute("SELECT id FROM user_info WHERE id=(?)", ids)
        if len(check_length) == 1:
            try:
                db.execute("UPDATE TABLE user_info SET real_name=(?), student_id=(?), class=(?), car_plate_no=(?)", real_name, classes, student_id, car_plate)
            except:
                return render_template("profile.html", name=name[0]["username"], real_name= request.form.get("real_name", "Student Name"), registered_date=registered_date[0]["registered_date"], classes = request.form.get("classes", "Class"), student_id = request.form.get("student_id", "Student No") ,car_plate_no = request.form.get("car_plate_no", "Car Plate"))
        elif len(check_length) == 0:
            db.execute("INSERT INTO user_info VALUES(?, ?, ?, ?, ?, ?)", ids, real_name, student_id, classes, car_plate, registered_date[0]["registered_date"])
        
        return render_template("profile.html", name=name[0]["username"], real_name= request.form.get("real_name", "Student Name"), registered_date=registered_date[0]["registered_date"], classes = request.form.get("classes", "Class"), student_id = request.form.get("student_id", "Student No") ,car_plate_no = request.form.get("car_plate_no", "Car Plate"))

        
    else:
        check_length = db.execute("SELECT id FROM user_info WHERE id=(?)", ids)
        if len(check_length) == 1:
            informations = db.execute("SELECT real_name, student_id, class, car_plate_no FROM user_info WHERE id=(?)", ids)
            return render_template("profile.html", name=name[0]["username"], real_name=informations[0]["real_name"], student_id=informations[0]["student_id"], classes=informations[0]["class"], car_plate_no=informations[0]["car_plate_no"], registered_date=registered_date[0]["registered_date"])
        else:
            return render_template("profile.html", name=name[0]["username"], real_name= request.form.get("real_name", "Student Name"), registered_date=registered_date[0]["registered_date"], classes = request.form.get("classes", "Class"), student_id = request.form.get("student_id", "Student No") ,car_plate_no = request.form.get("car_plate_no", "Car Plate"))

@app.route("/deregister", methods=["POST", "GET"])
def deregister():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        check_name = db.execute("SELECT username FROM users WHERE username=(?)", name)
        if (len(check_name) != 1):
            flash("Invalid User")
            return redirect("/deregister")
        else:
            check_password = db.execute("SELECT password FROM users WHERE username=(?)", name)
            if (check_password_hash(check_password[0]["password"], password)):
                id_selected = db.execute("SELECT id FROM users WHERE username=(?)", name)
                session.clear()
                db.execute("DELETE FROM users WHERE username=(?)", name)
                db.execute("DELETE FROM user_info WHERE id=(?)", id_selected[0]["id"])
                return redirect("/")

            else:
                flash("Invalid Password")
                return redirect("/deregister")
    else:
        return render_template("deregister.html")


@login_required
@app.route("/logs")
def logs():    
    logs = db.execute("SELECT * FROM info")
    return render_template("logs.html", logs=logs)

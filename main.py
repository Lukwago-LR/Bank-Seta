from flask import Flask, render_template, request, session
import sqlite3

# Create database, create table Users and insert users
from database import get_user_credentials, All_Table, get_user_from_type, insert_new_schedule, Insert_Into_User

# db = sqlite3.connect("bank_seta.db")
# creating  all tables
# All_Table(db)
# Insert_Into_User(db)

app = Flask(__name__)
app.secret_key = "any"


@app.route("/", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        data = request.form
        session['user_name'] = data['name']
        db = sqlite3.connect("bank_seta.db")
        user = get_user_credentials(db, data['name'], data['password'])
        if user:
            if data["name"] == user[1] and data["password"] == user[3] and data["users"] == user[4]:
                if user[4] == "Student":
                    return render_template("student.html", name=data["name"], msg_sent=True)
                elif user[4] == "Administrator":
                    return render_template("administrator.html", name=data["name"], msg_sent=True)
                elif user[4] == "Volunteer":
                    return render_template("volunteer.html", name=data["name"], msg_sent=True)
            else:
                return render_template("login.html", login_message="Invalid credentials")

    return render_template("login.html", msg_sent=False)


@app.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return render_template("logout.html")


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        data = request.form
        if data['pass'] == data['password_confirm']:
            return render_template("logout.html")

    return render_template("register.html")


@app.route("/rank", methods=['GET'])
def rank():
    return render_template("rank.html", name=session.get('user_name'))


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        data = request.form
        print(data["videoInput"])
    return render_template("upload.html", name=session.get('user_name'))


@app.route("/schedule", methods=['GET', 'POST'])
def schedule():
    if request.method == "POST":
        data = request.form
        db = sqlite3.connect("bank_seta.db")
        user = get_user_from_type(db, "Administrator", session.get('user_name'))
        insert_new_schedule(db, "New", data["scheduled_subject"], data["topic"], data["from"], data["to"],
                            data["datepicker"])
        return render_template("administrator.html", name=session.get('user_name'))
    return render_template("schedule.html", name=session.get('user_name'))


@app.route("/content", methods=['GET', 'POST'])
def content():
    return render_template("content.html", name=session.get('user_name'))


@app.route("/student", methods=['GET', 'POST'])
def student():
    return render_template("student.html", name=session.get('user_name'))


@app.route("/administrator", methods=['GET', 'POST'])
def administrator():
    return render_template("administrator.html", name=session.get('user_name'))


@app.route("/volunteer", methods=['GET', 'POST'])
def volunteer():
    return render_template("volunteer.html", name=session.get('user_name'))


@app.route("/screen", methods=['GET', 'POST'])
def screen():
    return render_template("screen.html", name=session.get('user_name'))


if __name__ == '__main__':
    app.run(debug=True)

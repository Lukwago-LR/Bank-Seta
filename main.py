import sqlite3
from io import BytesIO

from flask import Flask, render_template, request, session, redirect, url_for, send_file

from database import get_user_credentials, get_user_from_type, insert_new_schedule, insert_new_Maths, \
    insert_new_Science, get_volunteer_status, get_content, get_all_unverified_volunteer, verify_volunteer

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
            session['user_id'] = user[0]
            if data["name"] == user[1] and data["password"] == user[3] and data["users"] == user[4]:
                if user[4] == "Student":
                    return render_template("student.html", name=data["name"], msg_sent=True)
                elif user[4] == "Administrator":
                    return render_template("administrator.html", name=data["name"], msg_sent=True)
                elif user[4] == "Volunteer":
                    status = get_volunteer_status(db, user[0])
                    if "Unverified" in status:
                        return render_template("verification.html", name=data["name"], msg_sent=True)
                    else:
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
    try:
        if request.method == "POST":
            data = request.form
            if "video_submit" in data:
                video_url = data["videoInput"]
                content_name = data["content_name"]
                sub_topic_topic_subject = data["topics"].split("(")
                sub_topic = sub_topic_topic_subject[0]
                topic_subject = sub_topic_topic_subject[1].split("-")
                topic = topic_subject[0]
                subject = topic_subject[1].split(")")[0]

                db = sqlite3.connect("bank_seta.db")
                if subject == "Maths":
                    insert_new_Maths(db, topic, sub_topic, content_name, video_url)
                    return render_template("upload.html", upload_status="file uploaded successfully")
                elif subject == "Science":
                    insert_new_Science(db, topic, sub_topic, content_name, video_url)
                    return render_template("upload.html", upload_status="file uploaded successfully")
        return render_template("upload.html")
    except Exception:
        redirect(url_for('upload', upload_status="Error"))


@app.route("/files", methods=['GET', 'POST'])
def file_upload():
    try:
        if request.method == "POST":
            data = request.form
            file = request.files['file']
            sub_topic_topic_subject = data["topics"].split("(")
            sub_topic = sub_topic_topic_subject[0]
            topic_subject = sub_topic_topic_subject[1].split("-")
            topic = topic_subject[0]
            subject = topic_subject[1].split(")")[0]

            db = sqlite3.connect("bank_seta.db")
            if subject == "Maths":
                insert_new_Maths(db, topic, sub_topic, file.filename, file.read())
                return render_template("upload.html", upload_status="file uploaded successfully")
            elif subject == "Science":
                insert_new_Science(db, topic, sub_topic, file.filename, file.read())
                redirect(url_for('upload', upload_status="file uploaded successfully"))

        return render_template("upload.html")
    except Exception:
        redirect(url_for('upload', upload_status="Error"))


@app.route("/schedule", methods=['GET', 'POST'])
def schedule():
    if request.method == "POST":
        data = request.form
        db = sqlite3.connect("bank_seta.db")
        get_user_from_type(db, "Administrator", session.get('user_name'))
        insert_new_schedule(db, "New", data["scheduled_subject"], data["topic"], data["from"], data["to"],
                            data["datepicker"])
        return render_template("administrator.html", name=session.get('user_name'))
    return render_template("schedule.html", name=session.get('user_name'))


@app.route("/content", methods=['GET', 'POST'])
def content():
    return render_template("content.html", name=session.get('user_name'))


@app.route("/surf<topic>", methods=['GET', 'POST'])
def surf(topic):
    db = sqlite3.connect("bank_seta.db")
    cont = get_content(db, topic)
    return render_template("download.html", name=session.get('user_name'), content=cont, topic=topic)


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
    db = sqlite3.connect("bank_seta.db")
    volunteers = get_all_unverified_volunteer(db)
    return render_template("screen.html", users=volunteers)


@app.route('/download/<topic>')
def download(topic):
    db = sqlite3.connect("bank_seta.db")
    download_f = get_content(db, topic)
    return send_file(BytesIO(download_f[0][4]), download_name=download_f[0][3], as_attachment=True)


@app.route('/verify/<volunteer_id>')
def verify(volunteer_id):
    db = sqlite3.connect("bank_seta.db")
    verify_volunteer(db, volunteer_id)
    return render_template("screen.html")


if __name__ == '__main__':
    app.run(debug=True)

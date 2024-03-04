import sqlite3
from io import BytesIO

from flask import Flask, render_template, request, session, redirect, url_for, send_file

from database import get_user_credentials, get_user_from_type, insert_new_schedule, insert_new_Maths, \
    insert_new_Science, get_volunteer_status, get_content, get_all_unverified_volunteer, verify_volunteer, \
    get_all_new_schedules, register_user, update_slot_status, insert_schedule_volunteer, all_schedules, \
    delete_single_schedule, get_my_schedules, insert_into_subjects, insert_into_history, check_history, \
    get_current_rank, ranking, delete_new_schedule, get_single_file, get_science_content, get_maths_content, \
    deleting_content
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "any"


@app.route("/", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        data = request.form
        db = sqlite3.connect("bank_seta.db")
        user = get_user_credentials(db, data['email'])
        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            if check_password_hash(user[3], data["password"]) and data["users"] == user[4]:
                if user[4] == "Student":
                    return render_template("student.html", name=user[1], msg_sent=True)
                elif user[4] == "Administrator":
                    return render_template("administrator.html", name=user[1], msg_sent=True)
                elif user[4] == "Volunteer":
                    status = get_volunteer_status(db, user[0])
                    if "Unverified" in status:
                        return render_template("verification.html", name=user[1], msg_sent=True)
                    else:
                        schedules = get_all_new_schedules(db, "New")
                        return render_template("volunteer.html", name=user[1], schedules=schedules,
                                               user_id=user[0])
            else:
                return render_template("login.html", login_message="Invalid credentials")
        else:
            return render_template("login.html", login_message="Invalid credentials")

    return render_template("login.html", msg_sent=False)


@app.route("/", methods=['GET'])
def logout():
    session.clear()
    return render_template("login.html")


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        data = request.form
        if data['pass'] == data['password_confirm']:
            db = sqlite3.connect("bank_seta.db")
            register_user(db, data['name'], data['email'], data['usertype'], generate_password_hash(data['pass']))
            return render_template("login.html")
    return render_template("register.html")


@app.route("/surf<topic>", methods=['GET', 'POST'])
def surf(topic):
    db = sqlite3.connect("bank_seta.db")
    return_files = []
    grades = []
    contents = get_content(db, topic)

    if contents:
        for cont in contents:
            return_files.append(check_history(db, session.get('user_id'), cont[0]))
            grades.append(get_current_rank(db, cont[0]))

        return render_template("download.html", name=session.get('user_name'), content=contents, topic=topic,
                               return_f=return_files, rank=grades, len=len(contents))
    return render_template("download.html", name=session.get('user_name'), content=contents, topic=topic, return_f=[],
                           rank=[], len=0)


@app.route("/rank<cont_id>/<cont_name>", methods=['GET', 'POST'])
def rank(cont_id, cont_name):
    if request.method == "POST":
        data = request.form
        db = sqlite3.connect("bank_seta.db")
        insert_into_history(db, session.get('user_id'), cont_id)
        ranking(db, cont_id, data['rank_name'])
        return render_template("rank.html", student_id=session.get('user_id'), content_name=cont_name, show=False)
    else:
        return render_template("rank.html", student_id=session.get('user_id'), content_name=cont_name, show=True)


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
                insert_into_subjects(db)

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
            print(subject)

            db = sqlite3.connect("bank_seta.db")
            insert_into_subjects(db)

            if subject == "Maths":
                insert_new_Maths(db, topic, sub_topic, file.filename, file.read())
                return render_template("upload.html", upload_status="file uploaded successfully")
            elif subject == "Science":
                insert_new_Science(db, topic, sub_topic, file.filename, file.read())
                redirect(url_for('upload', upload_status="file uploaded successfully"))
        return render_template("upload.html", upload_status="file uploaded successfully")
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
        return render_template("schedule.html", upload_status='Schedule created successfully',
                               name=session.get('user_name'))
    return render_template("schedule.html", upload_status='', name=session.get('user_name'))


@app.route("/content", methods=['GET', 'POST'])
def content():
    db = sqlite3.connect("bank_seta.db")
    maths_grades = []
    science_grades = []

    maths_content = get_maths_content(db)
    science_content = get_science_content(db)

    if maths_content or science_content:
        if maths_content:
            for cont in maths_content:
                maths_grades.append(get_current_rank(db, cont[0]))

        if science_content:
            for cont in science_content:
                science_grades.append(get_current_rank(db, cont[0]))

        return render_template("content.html", name=session.get('user_name'), maths_content=maths_content,
                               science_content=science_content, maths_rank=maths_grades, science_rank=science_grades,
                               maths_len=len(maths_content), science_len=len(science_content))

    return render_template("content.html", name=session.get('user_name'), maths_content=[],
                           science_content=[], maths_rank=0, science_rank=0, maths_len=0, science_len=0)


@app.route("/student", methods=['GET', 'POST'])
def student():
    return render_template("student.html", name=session.get('user_name'))


@app.route("/administrator", methods=['GET', 'POST'])
def administrator():
    return render_template("administrator.html", name=session.get('user_name'))


@app.route("/volunteer", methods=['GET', 'POST'])
def volunteer():
    db = sqlite3.connect("bank_seta.db")
    schedules = get_all_new_schedules(db, "New")
    return render_template("volunteer.html", name=session.get('user_name'), schedules=schedules,
                           user_id=session.get('user_id'))


@app.route("/screen", methods=['GET', 'POST'])
def screen():
    db = sqlite3.connect("bank_seta.db")
    volunteers = get_all_unverified_volunteer(db)
    return render_template("screen.html", users=volunteers)


@app.route('/download<content_id>/<topic>')
def download(content_id, topic):
    db = sqlite3.connect("bank_seta.db")
    download_f = get_single_file(db, content_id, topic)
    return send_file(BytesIO(download_f[4]), download_name=download_f[3], as_attachment=True)


@app.route('/verify<volunteer_id>')
def verify(volunteer_id):
    db = sqlite3.connect("bank_seta.db")
    verify_volunteer(db, volunteer_id)
    return render_template("screen.html")


@app.route('/slots<slot_id>')
def slots(slot_id):
    db = sqlite3.connect("bank_seta.db")
    update_slot_status(db, slot_id)
    insert_schedule_volunteer(db, slot_id, session.get('user_id'))
    return redirect(url_for('volunteer', name=session.get('user_name')))


@app.route('/periods')
def periods():
    db = sqlite3.connect("bank_seta.db")
    schedules = all_schedules(db)
    p = get_all_new_schedules(db, "New")
    return render_template('slots.html', schedules=schedules, periods=p)


@app.route('/delete_schedules<schedule_id>')
def delete_schedule(schedule_id):
    db = sqlite3.connect("bank_seta.db")
    delete_single_schedule(db, schedule_id)
    return redirect(url_for('periods'))


@app.route('/my_schedules<user_id>')
def my_schedules(user_id):
    db = sqlite3.connect("bank_seta.db")
    schedules = get_my_schedules(db, user_id)
    return render_template('myschedules.html', schedules=schedules)


@app.route('/deleting_schedules<schedule_id>')
def deleting_new_schedule(schedule_id):
    db = sqlite3.connect("bank_seta.db")
    delete_new_schedule(db, schedule_id)
    return redirect(url_for('periods'))


@app.route('/delete_content<content_id>/<subject>')
def delete_content(content_id, subject):
    db = sqlite3.connect("bank_seta.db")
    deleting_content(db, content_id, subject)
    return redirect(url_for('content'))


if __name__ == '__main__':
    app.run(debug=True)

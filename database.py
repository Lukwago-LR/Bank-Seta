def Insert_Into_User(db):
    cursor = db.cursor()

    cursor.execute("INSERT INTO Users (name, email, password, type) VALUES('Bob','bobsaved@gmail.com','123',"
                   "'Student')")

    cursor.execute("INSERT INTO Users (name, email, password, type) VALUES('John','john@gmail.com','1234',"
                   "'Administrator')")

    cursor.execute("INSERT INTO Users (name, email, password, type) VALUES('Tim','timsaved@gmail.com','12345',"
                   "'Volunteer')")
    db.commit()

    # Close the cursor and the connection
    cursor.close()


def get_user_credentials(db, email):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users WHERE email=?", (email,))
    user = cursor.fetchone()
    cursor.close()
    return user


def get_user_from_type(db, user_type, name):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users WHERE type=? and name=?", (user_type, name))
    user = cursor.fetchone()
    cursor.close()
    return user


def get_volunteer_status(db, user_id):
    cursor = db.cursor()
    str_sql = f"SELECT status FROM Volunteers WHERE id={user_id}"
    cursor.execute(str_sql)
    user = cursor.fetchone()
    cursor.close()
    return user


def get_all_unverified_volunteer(db):
    cursor = db.cursor()
    str_sql = "SELECT Users.name, Users.email, Volunteers.status, Volunteers.id FROM Users INNER JOIN Volunteers ON " \
              "Users.id=Volunteers.id WHERE Volunteers.status='Unverified' "
    cursor.execute(str_sql)
    users = cursor.fetchall()
    cursor.close()
    return users


def register_user(db, username, email, usertype, password):
    cursor = db.cursor()
    if usertype == "Volunteer":
        cursor.execute("INSERT INTO Users (name, email, password, type) VALUES(?,?,?,?)",
                       (username, email, password, usertype))
        db.commit()
        user_ID = cursor.execute("SELECT MAX(id) FROM Users WHERE type='Volunteer'")
        s_id = user_ID.fetchone()
        cursor.execute("INSERT INTO Volunteers (id, status) VALUES(?,?)", (s_id[0], "Unverified"))
        db.commit()
    else:
        cursor.execute("INSERT INTO Users (name, email, password, type) VALUES(?,?,?,?)",
                       (username, email, password, usertype))
        db.commit()

    cursor.close()


def insert_new_schedule(db, status, subject, topic, fro, to, d):
    cursor = db.cursor()
    cursor.execute("INSERT INTO Schedules (status, subject, topic,  slot_time, slot_date) VALUES (?, "
                   "?, ?, ?, ?)", (status, subject, topic, f"{fro}" + "-" + f"{to}", d))
    db.commit()
    cursor.close()


def insert_into_subjects(db):
    cursor = db.cursor()
    sql = "INSERT INTO Subjects (rank) VALUES (0)"
    cursor.execute(sql)
    db.commit()
    cursor.close()


def get_subjects_id(db):
    cursor = db.cursor()
    sql = "SELECT MAX(id) FROM Subjects"
    cursor.execute(sql)
    subj_id = cursor.fetchone()
    cursor.close()
    return subj_id


def insert_new_Maths(db, topic, sub_topic, content_name, source):
    cursor = db.cursor()
    subj_id = get_subjects_id(db)
    cursor.execute("INSERT INTO Maths (id, Topic, Sub_Topic, Content_Name, Source) VALUES (?, ?, "
                   "?, ?, ?)", (subj_id[0], topic, sub_topic, content_name, source))
    db.commit()
    cursor.close()


def insert_new_Science(db, topic, sub_topic, content_name, source):
    cursor = db.cursor()
    subj_id = get_subjects_id(db)
    cursor.execute("INSERT INTO Science (id, Topic, Sub_Topic, Content_Name, Source) VALUES (?, ?, "
                   "?, ?, ?)", (subj_id[0], topic, sub_topic, content_name, source))
    db.commit()
    cursor.close()


def All_Table(db):
    cursor = db.cursor()

    # layer one tables
    # cursor.execute(
    #     "CREATE TABLE Users (id INTEGER PRIMARY KEY AUTOINCREMENT ,name VARCHAR(255) NOT NULL,email VARCHAR(255) NOT "
    #     "NULL,password VARCHAR(255) NOT NULL,type VARCHAR(255) NOT NULL)")

    # cursor.execute("CREATE TABLE Subjects(id INTEGER PRIMARY KEY AUTOINCREMENT, rank INTEGER "
    #                "NOT NULL)")
    #
    # cursor.execute(
    #     "CREATE TABLE Science(id INTEGER PRIMARY KEY AUTOINCREMENT, Topic VARCHAR(255) NOT NULL, Sub_Topic VARCHAR("
    #     "255) NOT NULL, Content_Name VARCHAR(255) NOT NULL, Source VARCHAR(255) NOT NULL,FOREIGN KEY (id) REFERENCES "
    #     "Subjects(id))")

    # cursor.execute("CREATE TABLE Maths(id INTEGER PRIMARY KEY AUTOINCREMENT, Topic VARCHAR(255) NOT NULL, Sub_Topic "
    #                "VARCHAR(255) NOT NULL, Content_Name VARCHAR(255) NOT NULL, Source VARCHAR(255) NOT NULL, "
    #                "FOREIGN KEY (id) REFERENCES Subjects(id))")

    # cursor.execute("CREATE TABLE Notifications(id INTEGER PRIMARY KEY AUTOINCREMENT,status VARCHAR(255) NOT NULL,"
    #                "Recipient VARCHAR(255) NOT NULL)")

    # cursor.execute("CREATE TABLE Schedules(id INTEGER PRIMARY KEY AUTOINCREMENT,status VARCHAR(255) NOT NULL,"
    #                "subject VARCHAR(255) NOT NULL,topic VARCHAR(255) NOT NULL,slot_time VARCHAR(255) NOT NULL,"
    #                "slot_date DATE NOT NULL)")

    # cursor.execute("CREATE TABLE Volunteers(id INTEGER PRIMARY KEY, status VARCHAR(255) NOT NULL,FOREIGN KEY (id) "
    #                "REFERENCES Users(id))")

    # cursor.execute("CREATE TABLE History(id INTEGER NOT NULL, s_id INTEGER NOT NULL,PRIMARY KEY (id, s_id), "
    #                "FOREIGN KEY (s_id) REFERENCES Users(id), FOREIGN KEY (id) REFERENCES Subjects(id))")

    # cursor.execute("CREATE TABLE Volunteer_Schedule(s_id INTEGER NOT NULL, v_id INTEGER NOT NULL, PRIMARY KEY(s_id, "
    #                "v_id),FOREIGN KEY (s_id) REFERENCES Schedules(id), FOREIGN KEY (v_id) REFERENCES Volunteers(id))")

    db.commit()
    cursor.close()


def get_content(db, search_string):
    cursor = db.cursor()
    if "Maths" in search_string:
        s = f"SELECT * FROM Maths WHERE Sub_Topic='{search_string.split('(')[0]}'"
        cursor.execute(s)
        download_file = cursor.fetchall()
        cursor.close()
    elif "Science" in search_string:
        s = f"SELECT * FROM Science WHERE Sub_Topic='{search_string.split('(')[0]}'"
        cursor.execute(s)
        download_file = cursor.fetchall()
        cursor.close()
    return download_file


def get_single_file(db, search_id, search_string):
    cursor = db.cursor()
    if "Maths" in search_string:
        s = f"SELECT * FROM Maths WHERE id=? AND Sub_Topic=?"
        cursor.execute(s, (search_id, search_string.split('(')[0]))
        download_file = cursor.fetchone()
        cursor.close()
    elif "Science" in search_string:
        s = f"SELECT * FROM Science WHERE id=? AND Sub_Topic=?"
        cursor.execute(s, (search_id, search_string.split('(')[0]))
        download_file = cursor.fetchone()
        cursor.close()
    return download_file


def all_schedules(db):
    cursor = db.cursor()
    s = "SELECT Users.name, Users.email, Schedules.subject, Schedules.topic, Schedules.slot_time, " \
        "Schedules.slot_date, Schedules.status, Schedules.id FROM Users INNER JOIN Volunteer_Schedule ON Users.id = " \
        "Volunteer_Schedule.v_id INNER JOIN Schedules ON Schedules.id = Volunteer_Schedule.s_id "
    cursor.execute(s)
    download_file = cursor.fetchall()
    cursor.close()
    return download_file


def verify_volunteer(db, volunteer_id):
    try:
        cursor = db.cursor()
        # Using parameterized query to prevent SQL injection
        cursor.execute("UPDATE Volunteers SET status=? WHERE id=?", ('Verified', int(volunteer_id)))
        db.commit()  # Commit changes to the database
        cursor.close()
        return True  # Indicates successful update
    except Exception as e:
        # Handle exceptions (e.g., database errors)
        print(f"Error verifying volunteer: {e}")
        return False  # Indicates failure


def get_all_new_schedules(db, schedule_status):
    try:
        cursor = db.cursor()
        # Using parameterized query to prevent SQL injection
        s = f"SELECT * FROM Schedules WHERE status='{schedule_status}'"
        cursor.execute(s)
        schedules = cursor.fetchall()
        cursor.close()
        return schedules
    except Exception as e:
        # Handle exceptions (e.g., database errors)
        print(f"Error fetching schedules: {e}")
        return None


def update_slot_status(db, slot_id):
    try:
        cursor = db.cursor()
        # Using parameterized query to prevent SQL injection
        cursor.execute("UPDATE Schedules SET status=? WHERE id=?", ('Scheduled', slot_id))
        db.commit()  # Commit changes to the database
        cursor.close()
        return True  # Indicates successful update
    except Exception as e:
        # Handle exceptions (e.g., database errors)
        print(f"Error verifying volunteer: {e}")
        return False  # Indicates failure


def insert_schedule_volunteer(db, slot_id, volunteer_id):
    cursor = db.cursor()
    cursor.execute("INSERT INTO Volunteer_Schedule (s_id, v_id) VALUES (?, ?)", (slot_id, volunteer_id))
    db.commit()
    cursor.close()


def delete_single_schedule(db, schedule_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM Volunteer_Schedule WHERE s_id = ?", (schedule_id,))
    cursor.execute("DELETE FROM Schedules WHERE id = ?", (schedule_id,))
    db.commit()
    cursor.close()


def delete_new_schedule(db, schedule_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM Schedules WHERE id = ?", (schedule_id,))
    db.commit()
    cursor.close()


def get_my_schedules(db, user_id):
    cursor = db.cursor()
    sql = """
        SELECT Schedules.subject, Schedules.topic, Schedules.slot_time, Schedules.slot_date, Schedules.status, Schedules.id 
        FROM Schedules 
        INNER JOIN Volunteer_Schedule ON Schedules.id = Volunteer_Schedule.s_id 
        WHERE Volunteer_Schedule.v_id = ?
    """
    cursor.execute(sql, (user_id,))
    download_file = cursor.fetchall()
    cursor.close()
    return download_file


def ranking(db, content_id, current_rank):
    cursor = db.cursor()
    new_rank = int(get_current_rank(db, content_id)[0]) + int(current_rank)
    sql = "UPDATE Subjects SET rank=? WHERE id=?"
    cursor.execute(sql, (new_rank, content_id))
    db.commit()
    cursor.close()


def insert_into_history(db, user_id, content_id):
    cursor = db.cursor()
    sql = "INSERT INTO History (id, s_id) VALUES (?, ?)"
    cursor.execute(sql, (content_id, user_id))
    db.commit()
    cursor.close()


def check_history(db, user_id, content_id):
    cursor = db.cursor()
    sql = "SELECT * FROM History WHERE id=? AND s_id=?"
    cursor.execute(sql, (content_id, user_id))
    download_file = cursor.fetchone()
    cursor.close()
    return download_file


def get_current_rank(db, content_id):
    cursor = db.cursor()
    sql = "SELECT Subjects.rank FROM Subjects WHERE id=?"
    cursor.execute(sql, (content_id,))
    rank = cursor.fetchone()
    cursor.close()
    return rank


def get_maths_content(db):
    cursor = db.cursor()
    s = f"SELECT * FROM Maths INNER JOIN Subjects ON Maths.id=Subjects.id ORDER BY Subjects.rank DESC"
    cursor.execute(s)
    maths_file = cursor.fetchall()
    cursor.close()
    return maths_file


def get_science_content(db):
    cursor = db.cursor()
    s = f"SELECT * FROM Science INNER JOIN Subjects ON Science.id=Subjects.id ORDER BY Subjects.rank DESC"
    cursor.execute(s)
    science_file = cursor.fetchall()
    cursor.close()
    return science_file


def deleting_content(db, content_id, subject):
    cursor = db.cursor()
    if 'Maths' in subject:
        cursor.execute("DELETE FROM Maths WHERE id = ?", (content_id,))
    elif 'Science' in subject:
        cursor.execute("DELETE FROM Science WHERE id = ?", (content_id,))

    cursor.execute("DELETE FROM Subjects WHERE id = ?", (content_id,))
    db.commit()
    cursor.close()


# Notification module
def new_volunteer_log(db, user_id):
    pass


def complete_verification(user_id):
    pass


def new_content_uploaded():
    pass


# Account Management
def change_password():
    pass


def change_username():
    pass


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


def get_user_credentials(db, name, password):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users WHERE name=? and password=?", (name, password))
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


def register(db, username, email, usertype, password):
    cursor = db.cursor()
    if usertype == "Volunteer":
        cursor.execute("INSERT INTO Users (name, email, password, type) VALUES(?,?,?,?)",
                       (username, email, password, usertype))
        db.commit()
        user_id = cursor.execute("SELECT MAX(id) FROM Users WHERE type='Volunteer'")
        cursor.execute("INSERT INTO Volunteers (id, status) VALUES(?,?)", (user_id, "Unverified"))
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


def insert_new_Maths(db, topic, sub_topic, content_name, source):
    cursor = db.cursor()
    cursor.execute("INSERT INTO Maths (Topic, Sub_Topic, Content_Name, Source) VALUES (?, "
                   "?, ?, ?)", (topic, sub_topic, content_name, source))
    db.commit()
    cursor.close()


def insert_new_Science(db, topic, sub_topic, content_name, source):
    cursor = db.cursor()
    cursor.execute("INSERT INTO Science (Topic, Sub_Topic, Content_Name, Source) VALUES (?, "
                   "?, ?, ?)", (topic, sub_topic, content_name, source))
    db.commit()
    cursor.close()


def All_Table(db):
    cursor = db.cursor()

    # layer one tables
    cursor.execute(
        "CREATE TABLE Users (id INTEGER PRIMARY KEY AUTOINCREMENT ,name VARCHAR(255) NOT NULL,email VARCHAR(255) NOT "
        "NULL,password VARCHAR(255) NOT NULL,type VARCHAR(255) NOT NULL)")

    cursor.execute("CREATE TABLE Science(Id INTEGER PRIMARY KEY AUTOINCREMENT, Topic VARCHAR(255) NOT NULL, Sub_Topic "
                   "VARCHAR(255) NOT NULL, Content_Name VARCHAR(255) NOT NULL, Source VARCHAR(255) NOT NULL)")

    cursor.execute("CREATE TABLE Maths(Id INTEGER PRIMARY KEY AUTOINCREMENT, Topic VARCHAR(255) NOT NULL, Sub_Topic "
                   "VARCHAR(255) NOT NULL, Content_Name VARCHAR(255) NOT NULL, Source VARCHAR(255) NOT NULL)")

    cursor.execute("CREATE TABLE Notifications(id INTEGER PRIMARY KEY AUTOINCREMENT,status VARCHAR(255) NOT NULL,"
                   "Recipient VARCHAR(255) NOT NULL)")

    cursor.execute("CREATE TABLE Schedules(id INTEGER PRIMARY KEY AUTOINCREMENT,status VARCHAR(255) NOT NULL,"
                   "subject VARCHAR(255) NOT NULL,topic VARCHAR(255) NOT NULL,slot_time VARCHAR(255) NOT NULL,"
                   "slot_date DATE NOT NULL)")

    cursor.execute("CREATE TABLE Downloads(id INTEGER NOT NULL PRIMARY KEY,name VARCHAR(255) NOT NULL,rank INTEGER "
                   "NOT NULL,FOREIGN KEY (id) REFERENCES Students(id))")

    cursor.execute("CREATE TABLE Volunteers(id INTEGER PRIMARY KEY, status VARCHAR(255) NOT NULL,FOREIGN KEY (id) "
                   "REFERENCES Users(id))")

    cursor.execute("CREATE TABLE Student_Download(s_id INTEGER NOT NULL, d_id INTEGER NOT NULL, PRIMARY KEY(s_id, "
                   "d_id), FOREIGN KEY (s_id) REFERENCES Users(id), FOREIGN KEY (d_id) REFERENCES Downloads(id))")

    cursor.execute("CREATE TABLE Volunteer_Schedule(s_id INTEGER NOT NULL, v_id INTEGER NOT NULL, PRIMARY KEY(s_id, "
                   "v_id),FOREIGN KEY (s_id) REFERENCES Schedules(id), FOREIGN KEY (v_id) REFERENCES Volunteers(id))")

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


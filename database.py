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
    c = db.cursor()
    c.execute("SELECT * FROM Users WHERE type=? and name=?", (user_type, name))
    user = c.fetchone()
    c.close()
    return user


def insert_new_schedule(db, status, subject, topic, fro, to, d):
    cursor = db.cursor()
    cursor.execute("INSERT INTO Schedules (status, subject, topic,  slot_time, slot_date) VALUES (?, "
                   "?, ?, ?, ?)", (status, subject, topic, f"{fro}" + "-" + f"{to}", d))
    db.commit()
    cursor.close()


def All_Table(db):
    cursor = db.cursor()

    # layer one tables
    # cursor.execute(
    #     "CREATE TABLE Users (id INTEGER PRIMARY KEY AUTOINCREMENT ,name VARCHAR(255) NOT NULL,email VARCHAR(255) NOT "
    #     "NULL,password VARCHAR(255) NOT NULL,type VARCHAR(255) NOT NULL)")

    # cursor.execute("CREATE TABLE Science(Id INTEGER PRIMARY KEY AUTOINCREMENT, Topic VARCHAR(255) NOT NULL,
    # Sub_Topic VARCHAR(255) NOT NULL, Type VARCHAR(255) NOT NULL, Source VARCHAR(255) NOT NULL)")
    #
    # cursor.execute("CREATE TABLE Maths(Id INTEGER PRIMARY KEY AUTOINCREMENT, Topic VARCHAR(255) NOT NULL, Sub_Topic "
    #                "VARCHAR(255) NOT NULL, Type VARCHAR(255) NOT NULL, Source VARCHAR(255) NOT NULL)")

    # cursor.execute("CREATE TABLE Notifications(id INTEGER PRIMARY KEY AUTOINCREMENT,status VARCHAR(255) NOT NULL,"
    #                "Recipient VARCHAR(255) NOT NULL)")
    #
    # cursor.execute("CREATE TABLE Schedules(id INTEGER PRIMARY KEY AUTOINCREMENT,status VARCHAR(255) NOT NULL,"
    #                "subject VARCHAR(255) NOT NULL,topic VARCHAR(255) NOT NULL,slot_time VARCHAR(255) NOT NULL,"
    #                "slot_date DATE NOT NULL)")

    # cursor.execute("CREATE TABLE Downloads(id INTEGER NOT NULL PRIMARY KEY,name VARCHAR(255) NOT NULL,rank INTEGER "
    #                "NOT NULL,FOREIGN KEY (id) REFERENCES Students(id))")

    # cursor.execute("CREATE TABLE Volunteers(id INTEGER PRIMARY KEY, status VARCHAR(255) NOT NULL,FOREIGN KEY (id) "
    #                "REFERENCES Users(id))")
    #
    # cursor.execute("CREATE TABLE Student_Download(s_id INTEGER NOT NULL, d_id INTEGER NOT NULL, PRIMARY KEY(s_id, "
    #                "d_id), FOREIGN KEY (s_id) REFERENCES Users(id), FOREIGN KEY (d_id) REFERENCES Downloads(id))")

    # cursor.execute("CREATE TABLE Volunteer_Schedule(s_id INTEGER NOT NULL, v_id INTEGER NOT NULL, PRIMARY KEY(s_id, "
    #                "v_id),FOREIGN KEY (s_id) REFERENCES Schedules(id), FOREIGN KEY (v_id) REFERENCES Volunteers(id))")

    db.commit()
    cursor.close()

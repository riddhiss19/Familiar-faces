import sqlite3


connection_obj = sqlite3.connect("profile.db")

cursor_obj = connection_obj.cursor()

# Drop the GEEK table if already exists.
cursor_obj.execute("DROP TABLE IF EXISTS Profile")

# Creating table
table = """ CREATE TABLE Profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname CHAR(25) NOT NULL,
            lastname CHAR(25),
            password CHAR(25),
            linkedin TEXT,
            github TEXT,
            about TEXT, 
            persona TEXT,
            dob TEXT,
            summary TEXT,
            location TEXT,
            expertise TEXT
        ); """

cursor_obj.execute(table)

print("Table is Ready")

# Close the connection
connection_obj.close()

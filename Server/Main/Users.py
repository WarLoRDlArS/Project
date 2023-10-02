"""
Python Script to create and Initialize Users.db
And try some Stuff
"""
import sqlite3
from DbConnect import *

if __name__=="__main__":
    try:
        connect_Usersdb=sqlite3.connect('Users.db')
        cursorUsers=connect_Usersdb.cursor()
        print("Users.db Initialized successfully!!")

        command="""Create table user(
                   UserID text primary key,
                   password text
                   );"""
        
        try:
            result = send_command(connect_Usersdb,cursorUsers,command)
        except:
            print(f"Couldnt execute command: {command}")

        command="""insert into User values (\'larson\',\'helllo\')"""
        try:
            result = send_command(connect_Usersdb,cursorUsers,command)
        except:
            print(f"Couldnt execute command: {command}")

        command="""select * from User"""
        try:
            result = send_command(connect_Usersdb,cursorUsers,command)
        except:
            print(f"Couldnt execute command: {command}")
        
        if result:
            for i in result:
                print(i)
    except:
        print("Couldnt Connect to Users.db")
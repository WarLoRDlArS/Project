import sqlite3
import os

def send_command(cursor,command):
    try:
        cursor.execute(command)
        print("Command executed")
    except:
        print(f"Couldnt execute given command: {command}")

if __name__=="__main__":
    try :
        sqlite_connection = sqlite3.connect("maindb.db")
        cursor = sqlite_connection.cursor() 
        print("Database initialized")

        command = """Create Table Sample(
                        number int Primary Key, 
                        name text);"""
        try:
            cursor.execute(command)
        except:
            print("Couldnt create table")

        for i in range(0,1):
            name=input("Enter name:")
            number=input("Enter number:")
            command = f"insert into sample values ({number},\'{name}\')"
            send_command(cursor,command)

        command = "select * from sample"
        cursor.execute(command)
        temp=cursor.fetchall() 
        for i in temp:
            print(i)

        # if os.path.exists("/home/larson/Dev/python/Project/maindb.db"):
        #     os.remove("/home/larson/Dev/python/Project/maindb.db")
        # else:
        #     print("Couldnt delete database")
        
        sqlite_connection.commit()
        cursor.close()
    except:
        print("Couldnt run script")
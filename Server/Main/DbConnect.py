import sqlite3

def send_command(connection,cursor,command):
    try:
        cursor.execute(command)
        print("Command executed")
        print("Fetching")
        results = cursor.fetchall()
        print("Fetched")
        connection.commit()
        print("Committed")
        if results:
            return results
        else:
            return None
    except sqlite3.Error as e:
        print(f"Couldnt execute given command: {command} due to {e}")

import sqlite3

def ValidateUser(userName,Passw):
    try:
        sqliteConn = sqlite3.connect("Users.db")
        cursor = sqliteConn.cursor()
        command = f"Select password from User where UserID like '{userName}'"
        cursor.execute(command)
        result = cursor.fetchone()
        (resultFinal,*otherwise) = result
        print(resultFinal)
        if Passw == resultFinal:
            return True
        else: 
            return False
    except sqlite3.Error as e:
        print(f"Couldnt Connect to Users.db\n{e}")
    
if __name__ == "__main__":
    print("Enter user Name :")
    user_name=input()
    print("Enter password :")
    password = input()
    print(ValidateUser(user_name,password))

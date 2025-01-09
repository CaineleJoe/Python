import sys
import mysql.connector
from mysql.connector import errorcode

def print_usage():
    print("Usage:")
    print("  python encrypted_database.py add <file_path>")
    print("  python encrypted_database.py read <file_id>")
    print("  python encrypted_database.py delete <file_id>")

def db_connect():
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="bd2024",
        database="encrypted_database"
    )
    return db_connection

def main():
#command validation
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("[Error] Invalid number of arguments.")
        print_usage()
        return

    command = sys.argv[1].lower()
    valid_commands = ["add", "read", "delete"]

    if command not in valid_commands:
        print(f"[Error] Unknown command: '{command}'")
        print_usage()
        return
    else:
        print(f"[OK] Command recognized: {command}")

#Try to connect to the database
    try:
        db_connection = db_connect()
        print("[OK] Successfully connected to MySQL database.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("[Error] Wrong username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("[Error] Database does not exist.")
        else:
            print(f"[Error] {err}")
        sys.exit(1)

 #Close the connection
    if db_connection.is_connected():
        db_connection.close()
        print("[OK] Database connection closed.")

if __name__ == "__main__":
    main()

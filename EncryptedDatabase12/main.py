import os
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

def encrypt_file(src_path, dst_path, key=170, chunk_size=256):
    try:
        with open(src_path, "rb") as src_file, open(dst_path, "wb") as dst_file:
            while True:
                chunk = src_file.read(chunk_size)
                if not chunk:
                    break
                encrypted_chunk = bytes([b ^ key for b in chunk])
                dst_file.write(encrypted_chunk)
        print("[OK] File encrypted and saved to:", dst_path)
    except FileNotFoundError:
        print(f"[Error] Source file not found: {src_path}")
    except PermissionError:
        print(f"[Error] Permission denied. Could not read or write file.")
    except Exception as e:
        print(f"[Error] Something went wrong: {e}")



def handle_add(filepath):
    if not os.path.isfile(filepath):
        print(f"[Error] File does not exist {filepath}")
        return
    desktop_path=os.path.join(os.path.expanduser("~"), "Desktop")
    encrypted_folder=os.path.join(desktop_path, "Encrypted")
    if not os.path.exists(encrypted_folder):
        try:
            os.makedirs(encrypted_folder)
        except Exception as e:
            print(f"[Error] Failed to create folder {encrypted_folder}. Reason: {e}")
            return

    base_name=os.path.basename(filepath)
    encrypted_filename=base_name+"_encrypted"
    encrypted_filepath=os.path.join(encrypted_folder, encrypted_filename)
    #actual file encryption
    encrypt_file(filepath, encrypted_filepath)



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


#Command Handler
    if command=="add":
        filepath=sys.argv[2]
        handle_add(filepath)



 #Close the connection
    if db_connection.is_connected():
        db_connection.close()
        print("[OK] Database connection closed.")

if __name__ == "__main__":
    main()

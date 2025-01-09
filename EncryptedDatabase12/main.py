import os
import random
import sys
from math import gcd
import mysql.connector
from mysql.connector import errorcode


# --------------------------------------------------------------------------------
#                                USAGE
# --------------------------------------------------------------------------------

def print_usage():
    print("Usage:")
    print("  python encrypted_database.py add <file_path>")
    print("  python encrypted_database.py read <file_id>")
    print("  python encrypted_database.py delete <file_id>")


# --------------------------------------------------------------------------------
#                            DATABASE RELATED
# --------------------------------------------------------------------------------

def create_encrypted_files_table(db_connection):
    create_table_query = """
            CREATE TABLE IF NOT EXISTS encrypted_files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                path VARCHAR(255) NOT NULL UNIQUE,
                date_added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """
    cursor = db_connection.cursor()
    cursor.execute(create_table_query)
    db_connection.commit()
    cursor.close()


def db_connect():
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="bd2024",
        database="encrypted_database"
    )
    return db_connection


# --------------------------------------------------------------------------------
#                           PRIME CHECK
# --------------------------------------------------------------------------------

def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2

    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False

    return True


def generate_prime_candidate(bits=16):
    candidate = random.getrandbits(bits)
    candidate |= (1 << (bits - 1)) | 1
    return candidate




def generate_prime_number(bits=16):
    while True:
        candidate = generate_prime_candidate(bits)
        if is_prime(candidate):
            return candidate


# --------------------------------------------------------------------------------
#                           RSA KEY GENERATION
# --------------------------------------------------------------------------------
def generate_rsa_keypair(bits=16):
    p=generate_prime_number(bits)
    q=generate_prime_number(bits)
    while p==q:
        q=generate_prime_number(bits)
    n= p*q
    phi=(p-1)*(q-1)
    e= 65537
    if(gcd(e,phi)!=1):
        e=random.randint(2,phi-1)

    d=pow(e,-1,phi)
    return (n,e),(n,d) #public_key=(n,e) private_key=(n,d)


def save_key_to_file(key_tuple, filename):
    with open(filename, "wb") as f:
        f.write(str(key_tuple[0])+"\n")
        f.write(str(key_tuple[1])+"\n")


def get_keys_folder():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    keys_folder = os.path.join(desktop_path, "keys")

    if not os.path.exists(keys_folder):
        os.makedirs(keys_folder, exist_ok=True)

    return keys_folder



# --------------------------------------------------------------------------------
#                           RSA FILE ENCRYPTION
# --------------------------------------------------------------------------------
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


# --------------------------------------------------------------------------------
#                           ADD COMMAND (RSA)
# --------------------------------------------------------------------------------

def handle_add(filepath, db_connection):
    if not os.path.isfile(filepath):
        print(f"[Error] File does not exist {filepath}")
        return
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    encrypted_folder = os.path.join(desktop_path, "Encrypted")
    if not os.path.exists(encrypted_folder):
        try:
            os.makedirs(encrypted_folder)
        except Exception as e:
            print(f"[Error] Failed to create folder {encrypted_folder}. Reason: {e}")
            return

    base_name = os.path.basename(filepath)
    encrypted_filename = base_name + "_encrypted"
    encrypted_filepath = os.path.join(encrypted_folder, encrypted_filename)
    # actual file encryption
    encrypt_file(filepath, encrypted_filepath)
    # try inserting into database
    try:
        cursor = db_connection.cursor()
        insert_sql = """
                INSERT INTO encrypted_files (name, path)
                VALUES (%s, %s)
            """
        cursor.execute(insert_sql, (base_name, encrypted_filepath))
        db_connection.commit()

        inserted_id = cursor.lastrowid
        cursor.close()

        print(f"[OK] DB record inserted with ID: {inserted_id}")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DUP_ENTRY:
            print("[OK] Updated the file and the private key (Duplicate entry).")
        else:
            print(f"[Error] Could not insert file metadata into DB: {err}")


# --------------------------------------------------------------------------------
#                               MAIN
# --------------------------------------------------------------------------------

def main():
    # command validation
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

    # Try to connect to the database
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

    # create encrypted files table if it doesn't exist
    create_encrypted_files_table(db_connection)

    # Command Handler
    if command == "add":
        filepath = sys.argv[2]
        handle_add(filepath, db_connection)

    # Close the connection
    if db_connection.is_connected():
        db_connection.close()
        print("[OK] Database connection closed.")


if __name__ == "__main__":
    main()

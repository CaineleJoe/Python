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
    p = generate_prime_number(bits)
    q = generate_prime_number(bits)
    while p == q:
        q = generate_prime_number(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    if (gcd(e, phi) != 1):
        e = random.randint(2, phi - 1)

    d = pow(e, -1, phi)
    return (n, e), (n, d)  # public_key=(n,e) private_key=(n,d)


def save_key_to_file(private_key, filename):
    n, d = private_key
    with open(filename, "wb") as f:
        f.write(str(n).encode('utf-8') + b"\n")
        f.write(str(d).encode('utf-8') + b"\n")


def load_private_key(filename):
    with open(filename, "rb") as f:
        lines = f.read().splitlines()
        n = int(lines[0].decode('utf-8'))
        d = int(lines[1].decode('utf-8'))
        return (n, d)


def get_keys_folder():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    keys_folder = os.path.join(desktop_path, "keys")

    if not os.path.exists(keys_folder):
        os.makedirs(keys_folder, exist_ok=True)

    return keys_folder


# --------------------------------------------------------------------------------
#                           RSA FILE ENCRYPTION
# --------------------------------------------------------------------------------

def bytes_to_int(b):
    return int.from_bytes(b, 'big')


def int_to_bytes(i, length):
    return i.to_bytes(length, 'big')


def chunk_data(data, chunk_size):
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


def rsa_encrypt_file(src_path, dst_path, public_key, chunk_size=2):
    n, e = public_key

    try:
        with open(src_path, "rb") as f_in, open(dst_path, "w") as f_out:
            data = f_in.read()
            chunks = chunk_data(data, chunk_size)

            for ch in chunks:
                m_int = bytes_to_int(ch)
                c_int = pow(m_int, e, n)  # RSA encryption: c = m^e mod n
                f_out.write(str(c_int) + "\n")

        print(f"[OK] RSA-encrypted file saved to: {dst_path}")
    except FileNotFoundError:
        print(f"[Error] Source file not found: {src_path}")
    except PermissionError:
        print("[Error] Permission denied.")
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

    try:
        cursor = db_connection.cursor()
        select_sql = "SELECT id FROM encrypted_files WHERE name=%s"
        cursor.execute(select_sql, (base_name,))
        existing_row = cursor.fetchone()
        if existing_row:
            print(f"[Error] File {base_name} already exists in the database. ID={existing_row[0]}")
            cursor.close()
            return
        cursor.close()
    except mysql.connector.Error as err:
        print(f"[Error] Database error while checking for duplicates: {err}")
        return

    encrypted_filename = base_name + "_encrypted"
    encrypted_filepath = os.path.join(encrypted_folder, encrypted_filename)
    # key generation
    public_key, private_key = generate_rsa_keypair(16)
    # actual file encryption
    rsa_encrypt_file(filepath, encrypted_filepath, public_key, 2)
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
        # save the key
        keys_folder = get_keys_folder()
        pk_filename = f"pk_{inserted_id}.txt"
        pk_path = os.path.join(keys_folder, pk_filename)
        save_key_to_file(private_key, pk_path)
        print(f"[OK] Private key saved to: {pk_path}")
        print(f"[OK] DB record inserted with ID: {inserted_id}")

    except mysql.connector.Error as err:
        print(f"[Error] Could not insert file metadata into DB: {err}")
        return


# --------------------------------------------------------------------------------
#                               MAIN
# --------------------------------------------------------------------------------

def rsa_decrypt_file(src_path, dst_path, private_key, chunk_size=2):
    n, d = private_key
    try:
        with open(src_path, "r") as f_in, open(dst_path, "wb") as f_out:
            lines = f_in.read().splitlines()
            for line in lines:
                c_int = int(line)
                m_int = pow(c_int, d, n)  # RSA DECRYPTION
                chunk_bytes = int_to_bytes(m_int, chunk_size)
                f_out.write(chunk_bytes)

        print(f"[OK] RSA-decrypted file saved to: {dst_path}")
    except FileNotFoundError:
        print(f"[Error] Source file not found: {src_path}")
    except PermissionError:
        print("[Error] Permission denied.")
    except Exception as e:
        print(f"[Error] Something went wrong: {e}")


def handle_read(file_id, db_connection):
    try:
        cursor = db_connection.cursor()
        select_sql = "SELECT name,path FROM encrypted_files WHERE id=%s"
        cursor.execute(select_sql, (file_id,))
        row = cursor.fetchone()
        cursor.close()

        if not row:
            print(f"[Error] File not found with ID: {file_id}")
            return
        name, encrypted_path = row
        if not os.path.isfile(encrypted_path):
            print(f"[Error] File does not exist: {encrypted_path}")
            return

        # load the key
        keys_folder = get_keys_folder()
        pk_filename = f"pk_{file_id}.txt"
        pk_path = os.path.join(keys_folder, pk_filename)
        if not os.path.isfile(pk_path):
            print(f"[Error] File does not exist: {pk_path}")
            return

        private_key = load_private_key(pk_path)
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        decrypted_folder = os.path.join(desktop_path, "Decrypted")
        decrypted_path = os.path.join(decrypted_folder, name)
        if not os.path.exists(decrypted_folder):
            try:
                os.makedirs(decrypted_folder)
            except Exception as e:
                print(f"[Error] Failed to create folder {decrypted_folder}. Reason: {e}")
                return
        rsa_decrypt_file(encrypted_path, decrypted_path, private_key, chunk_size=2)
    except mysql.connector.Error as err:
        print(f"[Error] Database error while checking for duplicates: {err}")

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

    if command == "read":
        if int(sys.argv[2]):
            handle_read(int(sys.argv[2]), db_connection)
        else:
            print("[Error] Invalid ID.")
            return

    # Close the connection
    if db_connection.is_connected():
        db_connection.close()
        print("[OK] Database connection closed.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Encrypted File Manager using RSA Encryption and MySQL Database.

This script allows users to encrypt files using a naive RSA implementation,
store metadata in a MySQL database, decrypt files, delete records along
with associated encrypted files and private keys, and list all encrypted files.

Commands:
    add <file_path>      Encrypts the specified file and stores its metadata.
    read <file_id>       Decrypts the file associated with the given ID.
    delete <file_id>     Deletes the record, encrypted file, and private key associated with the given ID.
    list all             Displays all records in the encrypted_files table.

Usage:
    python encrypted_database.py add <file_path>
    python encrypted_database.py read <file_id>
    python encrypted_database.py delete <file_id>
    python encrypted_database.py list all
"""

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
    """
    Prints the usage instructions for the script.
    """
    print("Usage:")
    print("  python encrypted_database.py add <file_path>")
    print("  python encrypted_database.py read <file_id>")
    print("  python encrypted_database.py delete <file_id>")
    print("  python encrypted_database.py list all")


# --------------------------------------------------------------------------------
#                            DATABASE RELATED
# --------------------------------------------------------------------------------

def create_encrypted_files_table(db_connection):
    """
    Creates the 'encrypted_files' table in the database if it does not exist.

    The table stores metadata about encrypted files, including:
        - id: Auto-incremented primary key.
        - name: Name of the original file (unique).
        - path: Path to the encrypted file (unique).
        - date_added: Timestamp of when the record was added.

    Args:
        db_connection (mysql.connector.connection_cext.CMySQLConnection):
            Active database connection.
    """
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
    """
    Establishes a connection to the MySQL database.

    Returns:
        mysql.connector.connection_cext.CMySQLConnection:
            Database connection object.

    Raises:
        mysql.connector.Error: If the connection fails.
    """
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
    """
    Checks if a number is prime using trial division.

    Args:
        n (int): The number to check for primality.

    Returns:
        bool: True if 'n' is prime, False otherwise.
    """
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2

    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False

    return True


def generate_prime_candidate(bits=16):
    """
    Generates a random prime candidate of specified bit length.

    Ensures the candidate is odd and has the highest bit set to ensure bit length.

    Args:
        bits (int, optional): Number of bits for the prime candidate. Defaults to 16.

    Returns:
        int: A prime candidate.
    """
    candidate = random.getrandbits(bits)
    candidate |= (1 << (bits - 1)) | 1  # Ensure it's odd and has the highest bit set
    return candidate


def generate_prime_number(bits=16):
    """
    Generates a prime number of specified bit length.

    Repeatedly generates prime candidates until a prime is found.

    Args:
        bits (int, optional): Number of bits for the prime number. Defaults to 16.

    Returns:
        int: A prime number.
    """
    while True:
        candidate = generate_prime_candidate(bits)
        if is_prime(candidate):
            return candidate


# --------------------------------------------------------------------------------
#                           RSA KEY GENERATION
# --------------------------------------------------------------------------------

def generate_rsa_keypair(bits=16):
    """
    Generates an RSA keypair (public and private keys).

    Args:
        bits (int, optional): Bit length for prime numbers 'p' and 'q'. Defaults to 16.

    Returns:
        tuple:
            - public_key (tuple): (n, e)
            - private_key (tuple): (n, d)
    """
    p = generate_prime_number(bits)
    q = generate_prime_number(bits)
    while p == q:
        q = generate_prime_number(bits)

    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    if (gcd(e, phi) != 1):
        e = random.randint(2, phi - 1)
        while gcd(e, phi) != 1:
            e = random.randint(2, phi - 1)

    d = pow(e, -1, phi)
    return (n, e), (n, d)  # public_key=(n,e) private_key=(n,d)


def save_key_to_file(private_key, filename):
    """
    Saves the private key to a file.

    The private key consists of two integers, 'n' and 'd', each written on separate lines.

    Args:
        private_key (tuple): (n, d) representing the private key.
        filename (str): Path to the file where the key will be saved.
    """
    n, d = private_key
    with open(filename, "wb") as f:
        f.write(str(n).encode('utf-16') + b"\n")
        f.write(str(d).encode('utf-16') + b"\n")


def load_private_key(filename):
    """
    Loads the private key from a file.

    Expects the file to have 'n' and 'd' on separate lines.

    Args:
        filename (str): Path to the private key file.

    Returns:
        tuple: (n, d) representing the private key.

    Raises:
        FileNotFoundError: If the key file does not exist.
        ValueError: If the key file is improperly formatted.
    """
    with open(filename, "rb") as f:
        lines = f.read().splitlines()
        if len(lines) < 2:
            raise ValueError("Invalid key file format.")
        n = int(lines[0].decode('utf-16'))
        d = int(lines[1].decode('utf-16'))
        return (n, d)


def get_keys_folder():
    """
    Retrieves the path to the 'keys' folder on the Desktop.

    Creates the folder if it does not exist.

    Returns:
        str: Path to the 'keys' folder.
    """
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    keys_folder = os.path.join(desktop_path, "keys")

    if not os.path.exists(keys_folder):
        os.makedirs(keys_folder, exist_ok=True)

    return keys_folder


# --------------------------------------------------------------------------------
#                           RSA FILE ENCRYPTION
# --------------------------------------------------------------------------------

def bytes_to_int(b):
    """
    Converts bytes to an integer.

    Args:
        b (bytes): Byte sequence to convert.

    Returns:
        int: Integer representation of the bytes.
    """
    return int.from_bytes(b, 'big')


def int_to_bytes(i, length):
    """
    Converts an integer to bytes of specified length.

    Args:
        i (int): Integer to convert.
        length (int): Number of bytes to represent the integer.

    Returns:
        bytes: Byte sequence representing the integer.
    """
    return i.to_bytes(length, 'big')


def chunk_data(data, chunk_size):
    """
    Splits data into fixed-size chunks.

    Args:
        data (bytes): Data to split.
        chunk_size (int): Size of each chunk in bytes.

    Returns:
        list: List of byte chunks.
    """
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


def rsa_encrypt_file(src_path, dst_path, public_key, chunk_size=2):
    """
    Encrypts a file using RSA and writes the ciphertext to another file.

    Each chunk of the original file is encrypted and written as a separate line.

    Args:
        src_path (str): Path to the source (original) file.
        dst_path (str): Path to the destination (encrypted) file.
        public_key (tuple): (n, e) representing the RSA public key.
        chunk_size (int, optional): Size of each chunk in bytes. Defaults to 2.

    Raises:
        FileNotFoundError: If the source file does not exist.
        PermissionError: If there are permission issues accessing the files.
        Exception: For any other unforeseen errors.
    """
    n, e = public_key

    try:
        with open(src_path, "rb") as f_in, open(dst_path, "w",encoding='utf-16') as f_out:
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


def rsa_decrypt_file(src_path, dst_path, private_key, chunk_size=2):
    """
    Decrypts an RSA-encrypted file and writes the plaintext to another file.

    Each line in the encrypted file represents an encrypted chunk.

    Args:
        src_path (str): Path to the source (encrypted) file.
        dst_path (str): Path to the destination (decrypted) file.
        private_key (tuple): (n, d) representing the RSA private key.
        chunk_size (int, optional): Size of each chunk in bytes. Defaults to 2.

    Raises:
        FileNotFoundError: If the encrypted file does not exist.
        PermissionError: If there are permission issues accessing the files.
        Exception: For any other unforeseen errors.
    """
    n, d = private_key
    try:
        with open(src_path, "r",encoding='utf-16') as f_in, open(dst_path, "wb") as f_out:
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


# --------------------------------------------------------------------------------
#                           ADD COMMAND (RSA)
# --------------------------------------------------------------------------------

def handle_add(filepath, db_connection):
    """
    Handles the 'add' command: encrypts a file, stores metadata, and saves the private key.

    Steps:
        1. Validates the existence of the source file.
        2. Checks for duplicate entries in the database.
        3. Generates RSA keypair.
        4. Encrypts the file using the public key.
        5. Inserts metadata into the database.
        6. Saves the private key to a file.

    Args:
        filepath (str): Path to the file to be encrypted.
        db_connection (mysql.connector.connection_cext.CMySQLConnection):
            Active database connection.
    """
    if not os.path.isfile(filepath):
        print(f"[Error] File does not exist: {filepath}")
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
#                           READ COMMAND (RSA)
# --------------------------------------------------------------------------------

def handle_read(file_id, db_connection):
    """
    Handles the 'read' command: decrypts an encrypted file using its private key.

    Steps:
        1. Retrieves the file's metadata from the database using 'file_id'.
        2. Loads the corresponding private key from the 'keys' folder.
        3. Decrypts the encrypted file and saves the decrypted version.

    Args:
        file_id (int): ID of the file record in the database.
        db_connection (mysql.connector.connection_cext.CMySQLConnection):
            Active database connection.
    """
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
        return


# --------------------------------------------------------------------------------
#                                 DELETE COMMAND
# --------------------------------------------------------------------------------

def handle_delete(file_id, db_connection):
    """
    Handles the 'delete' command: removes the encrypted file, its private key, and the database record.

    Steps:
        1. Retrieves the file's metadata from the database using 'file_id'.
        2. Deletes the encrypted file from the disk.
        3. Deletes the corresponding private key file from the 'keys' folder.
        4. Removes the database record.

    Args:
        file_id (int): ID of the file record in the database.
        db_connection (mysql.connector.connection_cext.CMySQLConnection):
            Active database connection.
    """
    try:
        cursor = db_connection.cursor()
        select_sql = "Select name, path FROM encrypted_files WHERE id=%s"
        cursor.execute(select_sql, (file_id,))
        row = cursor.fetchone()

        if not row:
            print(f"[Error] Record not found with ID: {file_id}")
            cursor.close()
            return

        name, encrypted_path = row
        cursor.close()

        # delete encrypted file from disk

        if os.path.isfile(encrypted_path):
            try:
                os.remove(encrypted_path)
                print(f"[OK] File deleted successfully: {name}")
            except Exception as e:
                print(f"[Error] Failed to delete file: {name}")
        else:
            print(f"[Error] File does not exist: {name}")

        # delete private key file
        keys_folder = get_keys_folder()
        pk_filename = f"pk_{file_id}.txt"
        pk_path = os.path.join(keys_folder, pk_filename)
        if os.path.isfile(pk_path):
            try:
                os.remove(pk_path)
                print(f"[OK] Private key file deleted successfully: {name}")
            except Exception as e:
                print(f"[Error] Failed to delete file: {name}")
        else:
            print(f"[Error] File does not exist: {name}")

        # delete record from database
        cursor = db_connection.cursor()
        delete_sql = "DELETE FROM encrypted_files WHERE id=%s"
        cursor.execute(delete_sql, (file_id,))
        db_connection.commit()
        print(f"[OK] Record deleted successfully: {name}")
        cursor.close()

    except mysql.connector.Error as err:
        print(f"[Error] Database error while deleting ID: {file_id}: {err}")


# --------------------------------------------------------------------------------
#                               LIST COMMAND
# --------------------------------------------------------------------------------

def handle_list(db_connection):
    """
    Handles the 'list all' command: displays all records in the encrypted_files table.

    Steps:
        1. Retrieves all records from the 'encrypted_files' table.
        2. Formats and prints the records in a readable format.

    Args:
        db_connection (mysql.connector.connection_cext.CMySQLConnection):
            Active database connection.
    """
    try:
        cursor = db_connection.cursor()
        select_sql = "SELECT id, name, path, date_added FROM encrypted_files ORDER BY id"
        cursor.execute(select_sql)
        rows = cursor.fetchall()
        cursor.close()
        if not rows:
            print(f"[Error] No records in the database")
            return

        # Print header
        header = f"{'ID':<5} {'Name':<30} {'Path':<50} {'Date Added':<20}"
        print(header)
        print("-" * len(header))

        # Print each row
        for row in rows:
            id_, name, path, date_added = row
            print(f"{id_:<5} {name:<30} {path:<50} {date_added:<20}")

    except mysql.connector.Error as err:
        print(f"[Error] Database error while listing IDs: {err}")


# --------------------------------------------------------------------------------
#                               MAIN
# --------------------------------------------------------------------------------

def main():
    """
    Entry point of the script. Parses command-line arguments and dispatches commands.
    """
    # command validation
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("[Error] Invalid number of arguments.")
        print_usage()
        return

    command = sys.argv[1].lower()
    valid_commands = ["add", "read", "delete", "list"]

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
        if len(sys.argv) == 3:
            filepath = sys.argv[2]
            handle_add(filepath, db_connection)
        else:
            print("[Error] Missing <file_path> for 'add' command.")
            print_usage()

    elif command == "read":
        if len(sys.argv) == 3:
            try:
                file_id = int(sys.argv[2])
                handle_read(file_id, db_connection)
            except ValueError:
                print("[Error] Invalid ID. Only integers are allowed.")
        else:
            print("[Error] Missing <file_id> for 'read' command.")
            print_usage()

    elif command == "delete":
        if len(sys.argv) == 3:
            try:
                file_id = int(sys.argv[2])
                handle_delete(file_id, db_connection)
            except ValueError:
                print("[Error] Invalid ID. Only integers are allowed.")
        else:
            print("[Error] Missing <file_id> for 'delete' command.")
            print_usage()

    elif command == "list" and len(sys.argv) == 3 and sys.argv[2].lower() == "all":
        handle_list(db_connection)
    else:
        print("[Error] Invalid arguments.")
        print_usage()

    # Close the connection
    if db_connection.is_connected():
        db_connection.close()
        print("[OK] Database connection closed.")


if __name__ == "__main__":
    main()

import sys


def print_usage():
    print("Usage:")
    print("  python encrypted_database.py add <file_path>")
    print("  python encrypted_database.py read <file_id>")
    print("  python encrypted_database.py delete <file_id>")


def main():
    if len(sys.argv) < 2 & len(sys.argv) > 3:
        print("[Error] No command provided.")
        print_usage()
        return

    command = sys.argv[1].lower()
    valid_commands = ["add", "read", "delete"]

    if command not in valid_commands:
        print(f"[Error] Unknown command: '{command}'")
        print_usage()
    else:
        print(f"[OK] Command recognized: {command}")
if __name__ == "__main__":
    main()

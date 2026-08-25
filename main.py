import os
import json
import hashlib

DB_PATH = "hashes.json"


def calculate_hash(file_path):
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)

    return sha256_hash.hexdigest()


def load_database():
    if not os.path.isfile(DB_PATH):
        print("Hash database not found. Starting with an empty database.\n")
        return {}

    try:
        with open(DB_PATH, "r") as f:
            data = json.load(f)

        if isinstance(data, dict):
            print("Hash database loaded successfully.\n")
            return data

        print("Database format is invalid. Starting with an empty database.")
        return {}

    except json.JSONDecodeError:
        print("Database is corrupted.")
        return {}

    except Exception as e:
        print(f"Error loading database: {e}")
        return {}


def save_database(database):
    with open(DB_PATH, "w") as f:
        json.dump(database, f, indent=4)


def scan_directory(directory, hashes_db):

    current_files = set()

    unchanged_files = []
    new_files = {}
    modified_files = {}

    for filename in sorted(os.listdir(directory)):

        file_path = os.path.join(directory, filename)

        if not os.path.isfile(file_path):
            continue

        current_files.add(filename)

        current_hash = calculate_hash(file_path)

        stored_info = hashes_db.get(filename)

        if stored_info is None:

            new_files[filename] = current_hash

        elif stored_info["hash"] == current_hash:

            unchanged_files.append(filename)

        else:

            modified_files[filename] = current_hash

    deleted_files = [
        filename
        for filename in hashes_db
        if filename not in current_files
    ]

    return (
        unchanged_files,
        new_files,
        modified_files,
        deleted_files,
        current_files,
    )


def print_report(unchanged, new, modified, deleted, total):

    print("\n================ Scan Report ================\n")

    print(f"Total files scanned : {total}")
    print(f"Unchanged files     : {len(unchanged)}")
    print(f"New files           : {len(new)}")
    print(f"Modified files      : {len(modified)}")
    print(f"Deleted files       : {len(deleted)}")

    print("\nUnchanged Files")
    for file in unchanged:
        print(f"✔ {file}")

    print("\nNew Files")
    for file in new:
        print(f"+ {file}")

    print("\nModified Files")
    for file in modified:
        print(f"* {file}")

    print("\nDeleted Files")
    for file in deleted:
        print(f"- {file}")


def update_database(hashes_db, new, modified, deleted):

    for filename, file_hash in new.items():
        hashes_db[filename] = {
            "hash": file_hash,
            "algorithm": "SHA-256"
        }

    for filename, file_hash in modified.items():
        hashes_db[filename] = {
            "hash": file_hash,
            "algorithm": "SHA-256"
        }

    for filename in deleted:
        del hashes_db[filename]

    save_database(hashes_db)


def main():

    print("\n================== PyFIM ==================\n")

    directory = input("Enter directory path: ").strip()

    if not os.path.isdir(directory):
        print("\nDirectory does not exist.")
        return

    print(f"\nScanning: {directory}\n")

    hashes_db = load_database()

    unchanged, new, modified, deleted, current_files = scan_directory(
        directory,
        hashes_db
    )

    print_report(
        unchanged,
        new,
        modified,
        deleted,
        len(current_files)
    )

    choice = input("\nUpdate hash database? (Y/N): ").strip().upper()

    if choice == "Y":

        update_database(
            hashes_db,
            new,
            modified,
            deleted
        )

        print("\nDatabase updated successfully.")

    else:

        print("\nDatabase was not updated.")

    print("\n================== PyFIM ==================\n")


if __name__ == "__main__":
    main()
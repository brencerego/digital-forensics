import os
import shutil
import hashlib
import csv
from datetime import datetime

SOURCE_DIR = "Evidence_Source"
RECOVERY_DIR = "Recovered_Files"
REPORT_FILE = "recovery_report.csv"

os.makedirs(RECOVERY_DIR, exist_ok=True)

def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            data = file.read(4096)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()

def is_text_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file.read()

        return True

    except (UnicodeDecodeError, OSError):
        return False

def recover_deleted_files():

    recovery_records = []
    recovered_count = 0

    print("\nStarting file recovery scan...")
    print("-" * 45)

    for root, folders, files in os.walk(SOURCE_DIR):

        for filename in files:

            if filename.endswith(".deleted"):

                original_path = os.path.join(root, filename)

                print("\nFound:", original_path)

                if is_text_file(original_path):

                    recovered_name = filename.replace(
                        ".deleted", ""
                    )

                    recovered_path = os.path.join(
                        RECOVERY_DIR, recovered_name
                    )

                    shutil.copy2(
                        original_path,
                        recovered_path
                    )

                    file_hash = calculate_hash(
                        recovered_path
                    )

                    recovery_records.append([
                        filename,
                        recovered_name,
                        os.path.getsize(recovered_path),
                        file_hash,
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "Recovered"
                    ])

                    recovered_count += 1

                    print("Status: Recovered")
                    print("Saved as:", recovered_name)
                    print("SHA-256:", file_hash)

                else:
                    print("Status: Not a readable text file")

    with open(
        REPORT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as report:

        writer = csv.writer(report)

        writer.writerow([
            "Original File",
            "Recovered File",
            "Size (Bytes)",
            "SHA-256 Hash",
            "Recovery Time",
            "Status"
        ])

        writer.writerows(recovery_records)

    print("\n" + "-" * 45)
    print("Recovery process completed.")
    print("Total files recovered:", recovered_count)
    print("Report saved as:", REPORT_FILE)
if __name__ == "__main__":
    recover_deleted_files()
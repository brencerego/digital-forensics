import csv
import os
import shutil
import hashlib
from datetime import datetime

source_folder = "Evidence_Source"
destination_folder = "Collected_Evidence"
os.makedirs(destination_folder,exist_ok=True)
report_file = "Evidence_report.csv"

def calculate_hash(file_path):
    sha256=hashlib.sha256()
    with open(file_path,"rb") as file:
        while True:
            data = file.read(4096)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()

with open(report_file,"w",newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "File Name",
        "Modifiled Time",
        "SHA-256 Hash"
    ])

    for file_name in os.listdir(source_folder):
        source_path = os.path.join(source_folder,file_name)
        if os.path.isfile(source_path):
            destination_path = os.path.join(
                destination_folder,
                file_name
            )

            shutil.copy2(source_path,destination_path)
            file_size = os.path.getsize(source_path)
            modified_time = datetime.fromtimestamp(
                os.path.getmtime(source_path)
            )

            file_hash = calculate_hash(source_path)

            writer.writerow([
            file_name,
            file_size,
            modified_time,
            file_hash
            ])

            
            print("Collected:",file_name)

print("\nDigital evidence collection completed.")
print("Evidence saved in:",destination_folder)
print("Report saved as:",report_file)

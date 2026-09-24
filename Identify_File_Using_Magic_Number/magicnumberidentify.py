import os

MAGIC_NUMBERS = {
    "JPEG Image": [b"\xFF\xD8\xFF"],
    "PDF Document": [b"%PDF"]
}


def identify_file_type(file_path):

    if not os.path.isfile(file_path):
        print("Error: File does not exist.")
        return

    try:
        with open(file_path, "rb") as file:

            header = file.read(16)

        print("\nFile Analysis Report")
        print("-" * 35)
        print("File Name:", os.path.basename(file_path))

        print("Header Bytes:", header.hex(" ").upper())

        detected_type = "Unknown File Type"

        for file_type, signatures in MAGIC_NUMBERS.items():

            for signature in signatures:

                if header.startswith(signature):
                    detected_type = file_type
                    break

           
            if detected_type != "Unknown File Type":
                break

        print("Identified Type:", detected_type)

        
        extension = os.path.splitext(file_path)[1]

        print("File Extension:",
              extension if extension else "None")

        if detected_type == "Unknown File Type":
            print("Result: Signature not found.")
        else:
            print("Result: File signature identified.")

    except PermissionError:
        print("Error: Permission denied.")

    except OSError as error:
        print("Error while reading file:", error)


print("MAGIC NUMBER FILE TYPE DETECTOR")
print("=" * 40)
file_path = input("Enter the path of the file: ")

identify_file_type(file_path)
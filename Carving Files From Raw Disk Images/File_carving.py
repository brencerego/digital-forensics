import os
import csv
import hashlib
from datetime import datetime

# File Carving: Recover JPEG Files from Raw Binary Data
JPEG_START = b"\xFF\xD8\xFF"
JPEG_END = b"\xFF\xD9"


def calculate_hash(data):
    """Calculate SHA-256 hash of recovered data."""
    return hashlib.sha256(data).hexdigest()


def read_raw_file(filename):
    """Read the raw binary file."""
    try:
        with open(filename, "rb") as file:
            data = file.read()

        print("\nRaw file loaded successfully.")
        print("Total bytes:", len(data))
        return data

    except FileNotFoundError:
        print("Error: Raw binary file not found.")
        return None

    except OSError as error:
        print("Error reading file:", error)
        return None


def carve_jpegs(data, output_folder):
    """Find and extract JPEG files from binary data."""
    os.makedirs(output_folder, exist_ok=True)

    recovered_count = 0
    search_position = 0
    recovery_records = []

    while True:
        # Find the beginning of a JPEG image
        start = data.find(JPEG_START, search_position)

        if start == -1:
            break

        # Find the JPEG ending marker
        end_marker = data.find(JPEG_END, start + len(JPEG_START))

        if end_marker == -1:
            print("Incomplete JPEG found at offset:", start)
            search_position = start + len(JPEG_START)
            continue

        # Include the ending marker
        end = end_marker + len(JPEG_END)

        # Extract image bytes
        image_data = data[start:end]

        # Check minimum length
        if len(image_data) < 10:
            search_position = start + len(JPEG_START)
            continue

        recovered_count += 1

        # Create output filename
        output_name = f"recovered_{recovered_count}.jpg"
        output_path = os.path.join(output_folder, output_name)

        # Save recovered image
        with open(output_path, "wb") as output_file:
            output_file.write(image_data)

        # Calculate image hash
        file_hash = calculate_hash(image_data)

        print("\nJPEG image recovered!")
        print("Filename:", output_name)
        print("Start offset:", start)
        print("End offset:", end - 1)
        print("File size:", len(image_data), "bytes")
        print("SHA-256:", file_hash)

        recovery_records.append({
            "filename": output_name,
            "start_offset": start,
            "end_offset": end - 1,
            "size_bytes": len(image_data),
            "sha256": file_hash,
            "status": "Extracted"
        })

        # Continue searching after the recovered image
        search_position = end

    return recovery_records


def generate_report(records, output_folder):
    """Save recovery details in a CSV report."""
    report_path = os.path.join(
        output_folder, "recovery_report.csv"
    )

    fieldnames = [
        "filename",
        "start_offset",
        "end_offset",
        "size_bytes",
        "sha256",
        "status"
    ]

    with open(report_path, "w", newline="") as report_file:
        writer = csv.DictWriter(
            report_file, fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(records)

    print("\nRecovery report saved to:", report_path)


def main():
    print("=" * 50)
    print(" JPEG FILE CARVING TOOL")
    print("=" * 50)

    raw_filename = input(
        "\nEnter raw binary filename (raw_image.bin): "
    ).strip()

    if not raw_filename:
        raw_filename = "raw_image.bin"

    output_folder = "recovered_files"

    # Read raw binary data
    data = read_raw_file(raw_filename)

    if data is None:
        return

    print("\nSearching for JPEG signatures...")

    # Extract JPEG images
    records = carve_jpegs(data, output_folder)

    # Generate CSV report
    generate_report(records, output_folder)

    print("\n" + "=" * 50)
    print(" RECOVERY SUMMARY")
    print("=" * 50)

    print("Total JPEG files recovered:", len(records))
    print("Output folder:", output_folder)

    print(
        "Completed at:",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    if records:
        print("Result: JPEG extraction completed.")
    else:
        print("Result: No complete JPEG markers found.")

    print("=" * 50)


if __name__ == "__main__":
    main()
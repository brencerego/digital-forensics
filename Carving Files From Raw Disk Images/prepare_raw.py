with open("sample.jpg", "rb") as file:
    image = file.read()

raw_data = b"\x00\x11\x22\x33" * 100 + image
raw_data += b"\x44\x55\x66\x77" * 100

with open("raw_image.bin", "wb") as file:
    file.write(raw_data)

print("Raw binary file created successfully.")
import hashlib
filename = input("Enter the file name:")

try:
    with open(filename,"rb") as file:
        data = file.read()

    md5_hash = hashlib.md5(data).hexdigest() 
    sha256_hash = hashlib.sha256(data).hexdigest()
    print("\nMD5 Hash:")
    print(md5_hash)

    print("\nSHA-256 Hash:")
    print(sha256_hash)

except FileNotFoundError:
    print("File not found. Please check the file name.")
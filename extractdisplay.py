import os
import mimetypes
from datetime import datetime
from PIL import Image
from pypdf import PdfReader
from tkinter import Tk, filedialog
 
 
def get_file_type(file_path):
   file_type, _ = mimetypes.guess_type(file_path)
 
   if file_type:
       return file_type
 
   return "Unknown"
 
 
def get_creation_date(file_path):
   timestamp = os.path.getctime(file_path)
   return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
 
 
def get_image_metadata(file_path):
   image = Image.open(file_path)
 
   author = "Not available"
   creation_date = "Not available"
 
   exif_data = image.getexif()
 
   if exif_data:
       for tag_id, value in exif_data.items():
 
           if tag_id == 315:
               author = value
 
           if tag_id == 36867:
               creation_date = value
 
   return author, creation_date
 
 
def get_pdf_metadata(file_path):
   reader = PdfReader(file_path)
 
   metadata = reader.metadata
 
   author = "Not available"
   creation_date = "Not available"
 
   if metadata:
       if metadata.author:
           author = metadata.author
 
       if metadata.creation_date:
           creation_date = str(metadata.creation_date)
 
   return author, creation_date
 
 
def get_text_metadata(file_path):
   author = "Not available"
   creation_date = get_creation_date(file_path)
 
   return author, creation_date
 
 
def main():
 
   root = Tk()
   root.withdraw()
 
   file_path = filedialog.askopenfilename(
       title="Select a file",
       filetypes=[
           ("All Files", "*.*"),
           ("Image Files", "*.jpg *.jpeg *.png"),
           ("PDF Files", "*.pdf"),
           ("Text Files", "*.txt")
       ]
   )
 
   if not file_path:
       print("No file selected.")
       return
 
   file_name = os.path.basename(file_path)
   file_type = get_file_type(file_path)
 
   extension = os.path.splitext(file_path)[1].lower()
 
   if extension in [".jpg", ".jpeg", ".png"]:
       author, creation_date = get_image_metadata(file_path)
 
   elif extension == ".pdf":
       author, creation_date = get_pdf_metadata(file_path)
 
   elif extension == ".txt":
       author, creation_date = get_text_metadata(file_path)
 
   else:
       author = "Not available"
       creation_date = get_creation_date(file_path)
 
   print("\n========== FILE METADATA ==========")
   print("File Name     :", file_name)
   print("File Type     :", file_type)
   print("Author        :", author)
   print("Creation Date :", creation_date)
   print("File Location :", file_path)
   print("===================================\n")
 
 
main()
from dotenv import load_dotenv
from pymongo import MongoClient
import os
from PIL import Image
import io
from pdf2image import convert_from_bytes
from datetime import datetime
from gridfs import GridFS
import pytesseract
import streamlit as st


load_dotenv()
#setting the path to tesseract
tesseract_path = os.getenv("TESSERACT_PATH")
pytesseract.pytesseract.tesseract_cmd = tesseract_path

POPPLER_PATH = st.secrets["POPPLER_PATH"]
    


# loading the connection of mongodb

MONGO_URL = os.getenv("mongo_db_url")

'''MongoDB GridFS
     ↓
   bytes
     ↓
 io.BytesIO
     ↓
 PIL Image
     ↓
    OCR 
'''

# different db  for test history, with a collection to store chat history
client = MongoClient(MONGO_URL)
db = client["test_papers"]
fs = GridFS(db)

def create_collection():
    collection = db["test_history"]
    return collection

def extract_text_of_file(file_bytes: bytes, content_type: str) -> str:
    text = ""

    # -------- PDF --------
    if content_type == "application/pdf":
        images = convert_from_bytes(file_bytes,poppler_path=r"C:\poppler\Library\bin")

        for img in images:
            page_text = pytesseract.image_to_string(
                img, config="--psm 6"
            )
            text += page_text + "\n"

    # -------- Image --------
    elif content_type in ("image/png", "image/jpeg"):
        image = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(
            image, config="--psm 6"
        )

    else:
        return "Unsupported file type."

    return text.strip()

# to store user prompt in mongodb
def store_user(file_bytes : bytes,content_type:str,filename:str)->dict:
    file_id = fs.put(
        file_bytes,
        contentType = content_type,
        filename = filename
    )
    return{
        "role":"user",
        "file_id":file_id,
        "content_type":content_type,
        "timestamp": datetime.now()
    }

# to store assistant answer
def store_assistant(response:str)->dict:
    return {
        "role":"assistant",
        "content":response,
        "timestamp":datetime.now()
    }

# getting file from gridfs

def get_file_from_gridfs(db, file_id):
    fs = GridFS(db)
    file = fs.get(file_id)
    return file.read(), file.content_type, file.filename





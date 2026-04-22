from pymongo import MongoClient
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import re
from datetime import datetime



#loading all credientials
load_dotenv()

MONGO_URL = os.getenv("mongo_db_url")

#first we need to set up the client
'''Database
 └── Collection
      └── Document
'''
# function to make a client.
def start_db():
    client = MongoClient(MONGO_URL)
    db = client["karan_chatbot_db"]
    return db

# function to get collection name
def collection_name(user_input):
    text = user_input.lower()
    text = re.sub(r"[^a-z0-9_ ]", "", text)
    text = "_".join(text.split())
    return text[:50]+f"{datetime.now().strftime("%d/%m/%Y_%H:%M:%S")}"

# function to get a dict to insert into collection
def get_dict(role,text,model):
   return {
        "role": role,
        "content": text,
        "model": model,
        "timestamp": datetime.utcnow()
    }

# function to make a llm
def start_llm(model_name):
    llm = ChatGroq(
        model = model_name,
        temperature = 0
    )
    return llm






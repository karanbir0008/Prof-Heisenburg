from pydantic import BaseModel #it defines how my output will look like
from pydantic_ai import Agent, RunContext #Agent is the brain + decision-maker. and it gives context to tools during execution
from pydantic_ai.settings import ModelSettings #controls how llm behaves
from dotenv import load_dotenv
from googleapiclient.discovery import build
from pymongo import MongoClient
import os
from datetime import datetime

#loading api key for groq
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube","v3",developerKey=YOUTUBE_API_KEY)

MONGO_URL = os.getenv("mongo_db_url")

def make_mongo_db_collection():
    client = MongoClient(MONGO_URL)
    db = client["youtube_search"]
    collection = db["searched_topics"]
    return collection

def get_dict(text,role):
    return{
        "role":role,
        "content": text,
        "timestamp":datetime.now()
    }

# setting up the return type
class output(BaseModel):
    Topic : str
    video_name : str
    link : str

# setting up the agent
def getting_ai_agent():
    youtube_video_finder = Agent(
        model = "groq:openai/gpt-oss-120b",
        output_type=list[output],
        model_settings=ModelSettings(
            temperature = 0.2,
             max_retries=3 
        ),
        system_prompt=(
    "You must ONLY use the `search_video` tool to answer the user. "
    "Do NOT write text. Do NOT explain. "
    "Return results strictly via the tool output."
)
)


    
    @youtube_video_finder.tool
    def search_video(ctx:RunContext[None],topic_name:str)->list[output]:
        """You have to use this function always. this function takes topic name as input and returns related videos from youtube  """
        
        #setting searcher
       

        search_request = youtube.search().list(
            q=f"{topic_name} detailed explanation cbse",
            part="snippet",
            maxResults=6,
            type="video"
        )
        search_response = search_request.execute()
        video_list = []
        for item in search_response.get("items", []):
            video_id = item["id"]["videoId"]
            video_list.append(output(
                Topic=topic_name,
                video_name=item["snippet"]["title"],
                link=f"https://www.youtube.com/watch?v={video_id}"
                ) )
        return video_list
            
    return youtube_video_finder






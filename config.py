import os
from dotenv import load_dotenv, find_dotenv
load_dotenv()

 

def get_openai_api_key():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key



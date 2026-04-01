import requests
import os 
from dotenv import load_dotenv

load_dotenv()

api_url = os.getenv("API_URL")


def fetch_data():
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()  
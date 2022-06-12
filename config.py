import os

# uncomment for local development with .env file
from dotenv import load_dotenv
load_dotenv()

TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
DB = os.getenv('DB')
USER = os.getenv('USER_DB')
PW = os.getenv('PW')
HOST= os.getenv('HOST')
PORT = os.getenv('PORT')
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.getenv('token')
ADMIN = os.getenv('admin')


# env var tags is a string with each tag separated by comma ","
# use #shorts tag to enhance searching

motive = os.getenv('tags').split(", ")
GPT_API = os.getenv('gpt')

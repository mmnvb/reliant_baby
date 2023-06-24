import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.getenv('token')
ADMIN = os.getenv('admin')

# use #shorts tag to enhance searching
motive = ["Write your tags here", "And here"]

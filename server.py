import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='src/.env')
from src.api_gen import app

PORT = os.getenv("PORT")
app.run("0.0.0.0", PORT, debug=True)
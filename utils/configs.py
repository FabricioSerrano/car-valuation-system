from dotenv import load_dotenv
import os


load_dotenv()
BASE_URL = os.getenv('BASE_URL')
DATABASE_URL = os.getenv('DATABASE_URL')
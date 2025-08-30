from dotenv import load_dotenv
import os


load_dotenv()
BASE_URL = os.getenv('BASE_URL')
DATABASE_URL = os.getenv('DATABASE_URL')

MONTHS = {
    "janeiro": "01", "fevereiro": "02", "março": "03", 
    "abril": "04", "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
    "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"
}

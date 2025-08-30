from dotenv import load_dotenv
import os
import logging
import os


load_dotenv()
BASE_URL = os.getenv('BASE_URL')
DATABASE_URL = os.getenv('DATABASE_URL')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_DIR = os.getenv('LOG_DIR', '_logs')

MONTHS = {
    "janeiro": "01", "fevereiro": "02", "março": "03", 
    "abril": "04", "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
    "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"
}
 
def setup_logging():
    '''Set up logging configuration.'''

    os.makedirs(LOG_DIR, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(LOG_DIR, 'app.log')),
            logging.StreamHandler()
        ]
    )


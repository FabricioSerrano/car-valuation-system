import requests
from utils.configs import BASE_URL, MONTHS
from models import engine
from sqlalchemy.orm import Session
from models.reference_model import Reference
from datetime import datetime
import logging
from time import perf_counter

logger = logging.getLogger('controllers.reference_controller')

class ReferenceController:
    def __init__(self) -> None:
        self.endpoint_url = f"{BASE_URL}/ConsultarTabelaDeReferencia"
        self.controller_execution_time = 60  # in minutes

    def get_all_references(self) -> list[dict[str, str]] | None:
        '''Fetch all reference data from the external API.'''

        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'origin': 'https://veiculos.fipe.org.br',
            'priority': 'u=0, i',
            'referer': 'https://veiculos.fipe.org.br/?aspxerrorpath=/',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
            'x-requested-with': 'XMLHttpRequest',
        }

        response = requests.post(self.endpoint_url, headers=headers)

        if response.ok:
            return list[dict[str, str]](response.json())
        
        return None
    

    def transform_reference_data(self, references: list[dict[str, str]]) -> list[Reference]:
        '''Transform raw reference data into Reference model instances.'''

        if references is None:
            return []

        referece_list = [
            Reference(
                id=int(item['Codigo']), 
                name=item['Mes'],
                reference_date=self.transform_date_string_to_datetime(item['Mes'])
            ) 
            for item in references
        ]

        return referece_list

    def transform_date_string_to_datetime(self, date_string: str) -> datetime | None:
        '''Convert date string in the format "Month/YYYY" to a datetime object.'''

        if date_string is None:
            return None
        
        month, year = date_string.split('/')

        formated_date = f"01/{MONTHS[month]}/{year.strip()}"

        date_object = datetime.strptime(formated_date, '%d/%m/%Y')

        return date_object
    

    def register_references(self, references: list[Reference]) -> bool:
        '''Register all references of the current year into the database.'''

        references_to_register : list[Reference] = []


        if references is None or len(references) == 0:
            return False
        
        session = Session(engine)

        for reference in references:
            if reference.reference_date.year == datetime.now().year:
                references_to_register.append(reference)

        if session.query(Reference).first() is None:
            session.add_all(references_to_register)
            logger.debug(f'Added {len(references_to_register)} new references.')
        
        else:
            for reference in references_to_register:
                if session.query(Reference).filter(Reference.id == reference.id).first() is None:
                    session.add(reference)
                    logger.debug(f'Added new reference: {reference.name}.')
            
        session.commit()
        session.close()

        return True



    def execute_etl(self) -> None:
        '''Main execution method to fetch, transform, and register references.'''

        start_time = perf_counter()

        logger.info('Fetching references')

        references = self.get_all_references()
        if references is None:
            return
        
        transformed_references = self.transform_reference_data(references)
        if self.register_references(transformed_references) == True:
            logger.info('References registered successfully.')

        else:    
            logger.debug('No new references to registered.')

        end_time = perf_counter()
        execution_time = end_time - start_time
        logger.debug(f'ReferenceController execution time: {execution_time:.2f} seconds.')

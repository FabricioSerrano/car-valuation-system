import requests
from utils.configs import BASE_URL
from models import engine
from sqlalchemy.orm import Session
from models.brand_model import Brand
from models.reference_model import Reference
from sqlalchemy import Column
from time import sleep
import logging

logger = logging.getLogger('controllers.brand_controller')

class BrandController:
    def __init__(self):
        self.endpoint_url = f"{BASE_URL}/ConsultarMarcas"
        self.controller_execution_time = 60  # in minutes


    def get_all_brands(self) -> list[list[Brand]] | None:
        '''Fetch all car brands from the external API.'''

        brands_data_matrix : list[list[Brand]] = []

        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
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

        session = Session(engine)

        references = session.query(Reference).order_by(Reference.id.desc()).all()

        session.close()

        if len(references) == 0:
            return None
        
        for reference in references:
            data = {
                'codigoTabelaReferencia': reference.id,
                'codigoTipoVeiculo': '1',
            }

            response = requests.post(self.endpoint_url, headers=headers, data=data)

            if response.ok:
                brands_data = list[dict[str, str]](response.json())
                if len(brands_data) == 0:
                    continue

                transformed_brand_data = self.transform_brand_data(brands_data, reference.id)

                if transformed_brand_data is None:
                    continue

                brands_data_matrix.append(transformed_brand_data)

                logger.debug(f'Fetched {len(transformed_brand_data)} brands for reference ID {reference.id}.')

            else:
                logger.warning(f'Failed to fetch brands for reference ID {reference.id}. Status code: {response.status_code}')     

            sleep(5)  # To avoid overwhelming the API with requests


        if len(brands_data_matrix) > 0:
            return brands_data_matrix

        return None
    
    def transform_brand_data(self, brands: list[dict[str, str]], reference_id : int | Column[int]) -> list[Brand]:
        '''Transform raw brand data into Brand model instances, associating them with the given reference ID.'''

        if brands is None:
            return []

        return [Brand(id=int(item['Value']), name=item['Label'], reference_id=reference_id) for item in brands]
        
    
    def register_all_brands(self, brands: list[Brand]) -> bool:
        '''Register all brands in the database if they do not already exist.'''

        if brands is None or len(brands) == 0:
            return False
        
        session = Session(engine)

        if session.query(Brand).first() is None:
            session.add_all(brands)
            logger.debug(f'Added {len(brands)} new brands.')
            
        else:
            for brand in brands:
                if session.query(Brand).filter(Brand.id == brand.id).first() is None:
                    session.add(brand)
                    logger.debug(f'Added new brand: {brand.name}.')

        session.commit()
        session.close()

        return True


    def execute_etl(self) -> None:
        '''Main execution method to fetch, transform, and register brands.'''

        logger.info('Fetching brands')

        brands_data = self.get_all_brands()
        if brands_data is None:
            return
        
        for brands in brands_data:
            if self.register_all_brands(brands) == True:
                logger.info('Brands registered successfully.')
                return
            
            logger.debug(f'No new brands registered for reference {brands[0].name}.')
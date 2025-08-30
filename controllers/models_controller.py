import requests
from utils.configs import BASE_URL
from models import engine
from sqlalchemy.orm import Session
from models.reference_model import Reference
from models.brand_model import Brand
from models.years_model import Year
from models.model_model import Model
from time import sleep, perf_counter
import logging


logger = logging.getLogger('controllers.models_controller')

class ModelsController:
    def __init__(self) -> None:
        self.endpoint_url = f"{BASE_URL}/ConsultarModelos"
        self.controller_execution_time = 60  # in minutes

    def get_all_models_and_years_by_brand(self) -> bool:

        start_time = perf_counter()

        models_years_data_dict  : dict[str, dict[int, dict[str, list[Brand | Year]]]] = {}

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

        brands = session.query(Brand).order_by(Brand.created_at.desc()).all()
        refereces = session.query(Reference).order_by(Reference.created_at.desc()).all()

        session.close()

        if len(brands) == 0 or len(refereces) == 0:
            return False
        
        for brand in brands:
            models_years_data_dict[brand.id] = {} # type: ignore
            for reference in refereces:
                models_years_data_dict[brand.id][reference.id] = {} # type: ignore
                data = {
                    'codigoTipoVeiculo': '1',
                    'codigoTabelaReferencia': reference.id,
                    'codigoModelo': '',
                    'codigoMarca': brand.id,
                    'ano': '',
                    'codigoTipoCombustivel': '',
                    'anoModelo': '',
                    'modeloCodigoExterno': '',
                }

                response = requests.post(self.endpoint_url, headers=headers, data=data)

                if not response.ok:
                    logger.warning(f'Failed to fetch models and years for brand ID {brand.id} and reference ID {reference.id}. Status code: {response.status_code}')
                    continue

                raw_json = response.json()
                if raw_json is None or len(raw_json) == 0:
                    continue

                if 'Modelos' in raw_json:
                    for model in raw_json['Modelos']:
                        model_obj = Model(
                            id = int(model['Value']),
                            name = model['Label'],
                            brand_id = brand.id
                        )
                        self.register_model(model_obj)

                if 'Anos' in raw_json:
                    for year in raw_json['Anos']:
                        year_obj = Year(
                            id = year['Value'],
                            name = year['Label']
                        )
                        self.register_year(year_obj)

                sleep(1)  # to avoid overwhelming the API with requests


        

        end_time = perf_counter()
        execution_time = end_time - start_time
        logger.debug(f'ModelsController execution time: {execution_time:.2f} seconds.')
        return True
            


    def register_model(self, model: Model) -> bool:
        '''Register all models in the database if they do not already exist.'''

        if model is None:
            return False
        
        session = Session(engine)
        
        if session.query(Model).filter(Model.id == model.id).first() is None:
            session.add(model)
            logger.debug(f'Added new model: {model.name}.')

        session.commit()
        session.close()
        return True
    
    def register_year(self, year : Year) -> bool:
        '''Register all years in the database if they do not already exist.'''

        if year is None:
            return False
        
        session = Session(engine)
            
        if session.query(Year).filter(Year.id == year.id).first() is None:
            session.add(year)
            logger.debug(f'Added new year: {year.name}.')

        session.commit()
        session.close()

        return True
    
    def execute_etl(self) -> None:
        '''Main execution method to fetch, transform, and register models and years.'''

        logger.info('Fetching models and years.')

        if self.get_all_models_and_years_by_brand() == True:
            logger.info('Models and years registered successfully.')
            return
        
        logger.debug('No new models or years to register.')
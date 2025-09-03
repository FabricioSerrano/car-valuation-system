from utils.configs import BASE_URL
from models import engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import literal
from sqlalchemy import desc
from models.reference_model import Reference
from sqlalchemy import and_
from models.brand_model import Brand
from models.model_model import Model
from models.years_model import Year
from models.fuel_model import Fuel
from models.value_model import ValueModel
from time import sleep
import requests
from time import perf_counter
import logging

logger = logging.getLogger('controllers.value_controller')

class ValueController:
    def __init__(self):
        self.endpoint_url = f"{BASE_URL}/ConsultarValorComTodosParametros"
        self.controller_execution_time = 60  # in minutes

    def get_all_values_per_model(self) -> None:
        start_time = perf_counter()

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

        references = session.query(Reference).order_by(desc(Reference.id)).all()
        years = session.query(Year).order_by(desc(Year.id)).filter(~Year.id.like("32000%")).all()

        subquery = (
            session.query(
                Brand.id.label("brand_id"),
                Brand.name.label("brand_name"),
                Model.id.label("model_id"),
                Model.name.label("model_name")
            )
            .join(Model, Brand.id == Model.brand_id)
            .filter(
                and_(
                    Brand.active == True,
                    Model.active == True
                )
            )
        ).subquery()

        query = (
            session.query(
                subquery.c.brand_id,
                subquery.c.brand_name,
                subquery.c.model_id,
                subquery.c.model_name,
                Fuel.id.label("fuel_id"),
                Fuel.name.label("fuel_name")
            )
            .join(Fuel, literal(True))
        )

        results = query.all()
    

        if len(references) == 0 or len(years) == 0 or len(results) == 0:
            session.close()
            logger.warning("No references, years, or models found. Exiting value retrieval.")
            return
        
        for result in results:
            for year in years:
                for reference in references:
                
                    data = {
                        'codigoTabelaReferencia': reference.id,
                        'codigoMarca': result.brand_id,
                        'codigoModelo': result.model_id,
                        'codigoTipoVeiculo': '1',
                        'anoModelo': str(year.id).split('-')[0],
                        'codigoTipoCombustivel': str(year.id).split('-')[1],
                        'tipoVeiculo': 'carro',
                        'modeloCodigoExterno': '',
                        'tipoConsulta': 'tradicional',
                    }  

                    # To avoid overwhelming the API with requests
                    sleep(2)

                    response = requests.post(
                        self.endpoint_url,
                        headers=headers,
                        data=data,
                    )

                    if not response.ok:
                        logger.warning(f'Failed to fetch value for model ID {result.model_id}, year ID {year.id}, reference ID {reference.id}. Status code: {response.status_code}')
                        continue

                    response_data = response.json()


                    if 'erro' in response_data.keys():
                        logger.debug(f"error found in response for model ID {result.model_id}, year ID {year.id}, reference ID {reference.id}.")
                        continue

                    if response_data.get('Valor') is None:
                        logger.debug(f"No value found for model ID {result.model_id}, year ID {year.id}, reference ID {reference.id}.")
                        continue

                    value = ValueModel(
                        value=response_data.get('Valor'),
                        brand_id=result.brand_id,
                        model_id=result.model_id,
                        year_id=year.id,
                        fuel_id=str(year.id).split('-')[1],
                        reference_id=reference.id,
                    )

                    current_value = session.query(ValueModel).filter(
                        ValueModel.brand_id == value.brand_id,
                        ValueModel.model_id == value.model_id,
                        ValueModel.year_id == value.year_id,
                        ValueModel.fuel_id == value.fuel_id,
                        ValueModel.reference_id == value.reference_id
                    ).first()

                    if current_value is not None:
                        current_value.value = value.value
                        logger.debug(f"Value for model ID {result.model_id}, year ID {year.id}, reference ID {reference.id} updated successfully.")
                        session.commit()
                        continue

                    session.add(value)
                    session.commit()

                    logger.info(f"Value for model ID {result.model_id}, year ID {year.id}, reference ID {reference.id} saved successfully.")
                    

        session.close()

        end_time = perf_counter()
        execution_time = end_time - start_time
        logger.debug(f'ValueController execution time: {execution_time:.2f} seconds.')
        return


    def execute_etl(self) -> bool:
        logger.info('Fetching all values per model.')
        self.get_all_values_per_model()
        return True


        
import requests
from utils.configs import BASE_URL
from models import engine
from sqlalchemy.orm import Session
from models.brand_model import Brand


class BrandController:
    def __init__(self):
        self.endpoint_url = f"{BASE_URL}/ConsultarMarcas"
        self.controller_execution_time = 60  # in minutes

    def get_all_brands(self) -> list[dict[str, str]] | None:
        '''Fetch all car brands from the external API.'''
        
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

        data = {
            'codigoTabelaReferencia': '324',
            'codigoTipoVeiculo': '1',
        }

        response = requests.post(self.endpoint_url, headers=headers, data=data)

        if response.ok:
            return list[dict[str, str]](response.json())

        return None
    
    def transform_brand_data(self, brands: list[dict[str, str]]) -> list[Brand]:
        '''Transform raw brand data into Brand model instances.'''

        if brands is None:
            return []

        return [Brand(id=int(item['Value']), name=item['Label']) for item in brands]
        
    
    def register_all_brands(self, brands: list[Brand]) -> None:
        '''Register all brands in the database if they do not already exist.'''

        session = Session(engine)

        if session.query(Brand).first() is None:
            session.add_all(brands)
            
        else:
            for brand in brands:
                if session.query(Brand).filter(Brand.id == brand.id).first() is None:
                    session.add(brand)

        session.commit()
        session.close()


    def execute_etl(self) -> None:
        '''Main execution method to fetch, transform, and register brands.'''
        brands_data = self.get_all_brands()
        if brands_data is None:
            return
        
        brands = self.transform_brand_data(brands_data)
        self.register_all_brands(brands)
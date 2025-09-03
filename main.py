import schedule
from time import sleep
from controllers.brand_controller import BrandController
from controllers.reference_controller import ReferenceController
from controllers.models_controller import ModelsController
from controllers.fuels_controller import FuelController
from controllers.value_controller import ValueController
from models import base, engine
from utils.configs import setup_logging

base.metadata.create_all(engine)

if __name__ == '__main__':

    setup_logging()

    models_controller = ModelsController()
    brand_controller = BrandController()
    reference_controller = ReferenceController()
    fuel_controller = FuelController()
    value_controller = ValueController()

    reference_controller.execute_etl()
    brand_controller.execute_etl()
    models_controller.execute_etl()  
    fuel_controller.execute_etl()
    value_controller.execute_etl()

    
    schedule.every(reference_controller.controller_execution_time).minutes.do(reference_controller.execute_etl)
    schedule.every(brand_controller.controller_execution_time).minutes.do(brand_controller.execute_etl)
    schedule.every(models_controller.controller_execution_time).minutes.do(models_controller.execute_etl)
    schedule.every(fuel_controller.controller_execution_time).minutes.do(fuel_controller.execute_etl)
    schedule.every(value_controller.controller_execution_time).minutes.do(value_controller.execute_etl)


    while True:
        schedule.run_pending()
        sleep(1)
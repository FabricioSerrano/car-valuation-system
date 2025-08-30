import schedule
from time import sleep
from controllers.brand_controller import BrandController
from controllers.reference_controller import ReferenceController
from models import base, engine

base.metadata.create_all(engine)


if __name__ == '__main__':
    brand_controller = BrandController()
    reference_controller = ReferenceController()

    
    schedule.every(reference_controller.controller_execution_time).minutes.do(reference_controller.execute_etl)
    schedule.every(brand_controller.controller_execution_time).minutes.do(brand_controller.execute_etl)


    while True:
        schedule.run_pending()
        sleep(1)
import logging
from models import engine
from sqlalchemy.orm import Session
from models.years_model import Year
from models.fuel_model import Fuel

logger = logging.getLogger('controllers.fuels_controller')


class FuelController:
    def __init__(self):
        self.controller_execution_time = 60  # in minutes

    def register_all_fuels(self) -> bool:
        '''Register all fuels in the database from the years table'''

        session = Session(engine)

        result = session.query(Year).all()

        if len(result) == 0:
            session.close()
            return False

        for year in result:
            id = str(year.id).split('-')[1]
            fuel = str(year.name).split(' ')[1]

            fuel_obj = Fuel(id=int(id), name=fuel)

            if session.query(Fuel).filter(Fuel.id == fuel_obj.id).first() is None:
                session.add(fuel_obj)
                logger.debug(f'Added new fuel: {fuel_obj.name}.')

        session.commit()
        
        session.close()

        return True
    
    def execute_etl(self) -> None:
        '''Main execution method to register fuels.'''

        if self.register_all_fuels() == True:
            logger.info('fuels registered successfully.')
            return
        
        logger.info('No new fuels registered')
        return
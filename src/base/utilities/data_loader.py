from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker

from .logger import Logger
from .models import *


class DataLoader(Logger):
    def __init__(self, server: str, database: str):
        super().__init__()
        engine = create_engine(server)
        try:
            engine.execute(f'CREATE DATABASE {database}')
            self._logger.warning(f'no existing database called {database}, a new one has been created')
        except ProgrammingError:
            pass
        engine.execute(f'USE {database}')
        self._Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)

    def insert(self, atc: Article):
        self._logger.debug(f'trying to insert new article: {atc}')
        session = self._Session()
        session.add(atc)
        session.commit()
        self._logger.debug(f'insertion finished successfully')
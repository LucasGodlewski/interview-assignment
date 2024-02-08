from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config

engine = create_engine('sqlite:///:memory:', echo=config.DEBUG)
Session = sessionmaker(engine)

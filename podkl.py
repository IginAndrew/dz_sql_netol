import sqlalchemy
from sqlalchemy.orm import sessionmaker

DSN = "postgresql://andrew:12048937@localhost:5432/sql_alchemy"
engine = sqlalchemy.create_engine(DSN)


Session = sessionmaker(bind=engine)
session = Session()
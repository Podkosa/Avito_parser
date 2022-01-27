from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import  declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///avito.db")
Base = declarative_base()
Session = sessionmaker(engine)

def create_db():
    Base.metadata.create_all(engine)
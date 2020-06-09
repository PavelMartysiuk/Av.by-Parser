from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:pass123@localhost/Car_bot')

Base = declarative_base()

Session = sessionmaker(bind=engine)


class CarMark(Base):
    __tablename__ = 'mark'
    id = Column(Integer, primary_key=True)
    mark = Column(String)
    link = Column(String, unique=True)


class CarModel(Base):
    """unique=True for link"""
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    model = Column(String, )
    link = Column(String, unique=True)
    mark_id = Column(Integer, ForeignKey('mark.id'))


class Car(Base):
    __tablename__ = 'car'
    id = Column(Integer, primary_key=True)
    mark_id = Column(Integer, ForeignKey('mark.id'))
    model_id = Column(Integer, ForeignKey('models.id'))
    year = Column(String)
    content = Column(String)
    link = Column(String)
    cost = Column(String)
    location = Column(String)


Base.metadata.create_all(engine)

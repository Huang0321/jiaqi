from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float, DateTime


engine = create_engine("mysql+pymysql://admin:admin@119.28.227.49:3306/trade_pair_data")

Session = sessionmaker(bind=engine)

Base = declarative_base()


class Tabel1(Base):
    __tablename__ = 'binance_gateio_eos_usdt'
    id = Column(Integer, primary_key=True, autoincrement=True)
    exchange1_id = Column(Integer)
    exchange2_id = Column(Integer)
    symbol = Column(String(16), nullable=False)
    a_rate = Column(Float(18), nullable=False)
    b_rate = Column(Float(18), nullable=False)
    time = Column(DateTime(), nullable=False)

class Tabel2(Base):
    __tablename__ = 'binance_gateio_eos_usdt'
    id = Column(Integer, primary_key=True, autoincrement=True)
    exchange1_id = Column(Integer)
    exchange2_id = Column(Integer)
    symbol = Column(String(16), nullable=False)
    a_rate = Column(Float(18), nullable=False)
    b_rate = Column(Float(18), nullable=False)
    time = Column(DateTime(), nullable=False)

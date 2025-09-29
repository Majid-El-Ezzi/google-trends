from sqlalchemy import Column, Integer, String, DateTime
from db import Base

class Trend(Base):
    __tablename__ = 'trends'
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    keyword = Column(String, nullable=False)
    geo = Column(String)
    interest = Column(Integer, nullable=False)
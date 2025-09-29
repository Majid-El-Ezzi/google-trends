from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from db import Base

class Trend(Base):
    __tablename__ = 'trends'
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    keyword = Column(String, nullable=False)
    geo = Column(String,nullable=False,default="")
    interest = Column(Integer, nullable=False)
    
    __table_args__ = (
        UniqueConstraint('date', 'keyword', 'geo', name='unique_date_keyword_geo'),
    ) # this ensure unique combination of date, keyword, geo, used for updating existing records
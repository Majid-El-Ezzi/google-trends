from pydantic import BaseModel, Field
from datetime import datetime

class Record(BaseModel):
    date: datetime
    keyword: str
    geo: str
    interest: int = Field(ge=0, le=100)#   0 <= Interest value <= 100


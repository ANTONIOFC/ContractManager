from sqlalchemy import Column, Integer, String, Float, Date
from database import Base

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    value = Column(Float)
    due_date = Column(Date)
    category = Column(String)
    supplier = Column(String)
    status = Column(String, index=True)
    user = Column(String)
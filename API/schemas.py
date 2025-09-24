from datetime import date
from typing import Literal
from pydantic import BaseModel

class ContractCreate(BaseModel):
    title: str
    value: float
    status: Literal["emitido", "vigente", "cancelado"]
    due_date: date
    category: Literal["Recorrente", "Eventual"]
    supplier: str
    user: str

class ContractResponse(BaseModel):
    id: int
    title: str
    value: float
    status: str
    due_date: date
    category: str
    supplier: str
    user: str    
    class Config:
        from_attributes = True
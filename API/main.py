from datetime import date
import json
import os
from typing import Literal, Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException
import random

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()

class Contract (BaseModel):
    id: Optional[str] = uuid4().hex
    name: str
    value: float
    status: Literal["aberto", "fechado"]
    due_date: date = date.today()
    category: Literal["category 1", "category 2", "category 3"]
    supplier: str
    user: str

CONTRACT_DATABASE = []

CONTRACTS_FILE = "contracts.json"

if os.path.exists(CONTRACTS_FILE):
    with open (CONTRACTS_FILE, "r") as f:
        CONTRACT_DATABASE = json.load(f)


# / -> welcome
@app.get("/")
async def home():
    return "Welcome to my Contract Manager"

@app.get('/list-contracts')
async def list_contracts():
    return {"contracts": CONTRACT_DATABASE}

@app.get('/list-contract-by-index/{index}')
async def list_contract_by_index(index: int):
    if index < 0 or index >= len(CONTRACT_DATABASE):
        # error
        raise HTTPException(404, "Index out of range")
    else:
        return {
            "contracts": CONTRACT_DATABASE[index]
    }

@app.get('/get-random-contract')
async def get_random_contract():
    return random.choice(CONTRACT_DATABASE)

@app.post('/add-contract')
async def add_contract(contract: Contract):
    contract.id = uuid4().hex
    json_contract = jsonable_encoder(contract)
    CONTRACT_DATABASE.append(json_contract)

    with open(CONTRACTS_FILE, "w") as f:
        json.dump(CONTRACT_DATABASE, f)
    return { "message": f'Contrato {contract.name} was added'}


from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy import Float
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import engine, get_db
from datetime import date

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# list all contracts
@app.get("/contracts/", response_model=List[schemas.ContractResponse])
async def lists_contracts(
    supplier: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)):
    return crud.list_contracts(db,skip,limit, supplier)

# list all contracts by status
@app.get("/contracts/by-status", response_model=List[schemas.ContractResponse])
async def list_contracts_by_status(
    status: str | None= None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)):
    return crud.list_contracts_by_status(db,skip,limit,status)

# list all contracts by category
@app.get("/contracts/by-category", response_model=List[schemas.ContractResponse])
async def list_contracts_by_category(
    category: str | None= None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)):
    return crud.list_contracts_by_category(db,skip,limit,category)

# list all contracts by value range
@app.get("/contracts/by-value-range", response_model=List[schemas.ContractResponse])
async def list_contracts_by_value_range(
    start_value: float,
    end_value: float,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)):
    return crud.list_contracts_by_value_range(db,skip,limit,start_value,end_value)


# list all contracts by date range
@app.get("/contracts/by-date-range", response_model=List[schemas.ContractResponse])
async def list_contracts_by_date_range(
    start_date: date | date = date.today(),
    end_date: date | date = date.today(),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)):
    return crud.list_contracts_by_date_range(db,skip,limit,start_date,end_date)


# get one contract
@app.get("/contracts/{id}", response_model=schemas.ContractResponse)
async def get_contract_by_id(id: int, db: Session = Depends(get_db)):
    db_contract = crud.get_contract_by_id(db,id)
    if db_contract is None:
        raise HTTPException(status_code=404, detail="Contrato não encontrado")
    return db_contract

# add a contract
@app.post("/contracts", response_model=schemas.ContractResponse)
async def create_contract(contract: schemas.ContractCreate, db: Session = Depends(get_db)):
    return crud.create_contract(db,contract)

# update a contract
@app.put("/contracts/{id}", response_model=schemas.ContractResponse)
async def update_contract(id: int, contract: schemas.ContractCreate, db: Session = Depends(get_db)):
    db_contract = crud.get_contract_by_id(db,id)
    if db_contract is None:
        raise HTTPException(status_code=404, detail="Contrato não encontrado")
    return crud.update_contract(db, id, contract)

# delete a contract
@app.delete("/contracts/{id}")
async def delete_contract(id: int, db: Session = Depends(get_db)):
    db_contract = crud.get_contract_by_id(db,id)
    if db_contract is None:
        raise HTTPException(status_code=404, detail="Contrato não encontrado")

    crud.delete_contract(db, id)
    
    return { "message": "Contract sucessfuly deleted !"}

def contract_validate(id: int, db: Session = Depends(get_db)):
    db_contract = crud.get_contract_by_id(db,id)
    if db_contract is None:
        raise HTTPException(status_code=404, detail="Contrato não encontrado")

from sqlalchemy import Float
from sqlalchemy.orm import Session
from models import Contract
from schemas import ContractCreate
from datetime import date

def list_contracts(
        db: Session, skip: int, limit: int, supplier: str):
    
    if supplier:
        return db.query(Contract).filter(Contract.supplier==supplier).offset(skip).limit(limit).all()    

    return db.query(Contract).offset(skip).limit(limit).all()

def list_contracts_by_status(
        db: Session, skip: int, limit: int, status: str):
    
    return db.query(Contract).filter(Contract.status==status).offset(skip).limit(limit).all()    

def list_contracts_by_category(
        db: Session, skip: int, limit: int, category: str):
    
    return db.query(Contract).filter(Contract.category==category).offset(skip).limit(limit).all()    

def list_contracts_by_value_range(
        db: Session, skip: int, limit: int, start_value: Float, end_value: Float):
    
    return db.query(Contract).filter(Contract.value >= start_value, Contract.value <= end_value).offset(skip).limit(limit).all()

def list_contracts_by_date_range(
        db: Session, skip: int, limit: int, start_date: date, end_date: date):
    
    return db.query(Contract).filter(Contract.due_date >= start_date, Contract.due_date <= end_date).offset(skip).limit(limit).all()


def get_contract_by_id(db: Session, id: int):
    return db.query(Contract).filter(Contract.id == id).first()

def list_contract_by_user(db: Session, user: str):
    return db.query(Contract).filter(Contract.user == user).first()

def create_contract(db: Session, contract: ContractCreate):
    db_contract = Contract(title=contract.title, value = contract.value, 
                        due_date=contract.due_date, category = contract.category,
                        supplier = contract.supplier, status = contract.status, user = contract.user)
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract

def update_contract(db: Session, id:int, contract: ContractCreate):
    db_contract = db.query(Contract).filter(Contract.id==id).first()

    for key, value in contract.dict(exclude_unset=True).items():
        setattr(db_contract, key, value)
    db.commit()
    db.refresh(db_contract)
    return db_contract


def delete_contract(db: Session, contract_id: int):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    db.delete(contract)
    db.commit()
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, func, select
from typing import List
from app.db.session import get_session
from app.models.transaction import Transaction
from app.schemas import BalanceResponse, TransactionCreate, TransactionRead

router = APIRouter()

@router.post("/", response_model=TransactionRead)
def create_transaction(
    transaction_in: TransactionCreate, 
    session: Session = Depends(get_session)
):
    """
    Create a new transaction (Expense or Income).
    """
    transaction_db = Transaction.model_validate(transaction_in)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    
    return transaction_db


@router.get("/", response_model=List[TransactionRead])
def read_transactions(
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
):
    """
    Get all transactions.
    - **skip**: number of transactions to skip
    - **limit**: number of transactions to return
    """
    query = select(Transaction).offset(skip).limit(limit)
    transactions = session.exec(query).all()

    return transactions

@router.get("/balance", response_model=BalanceResponse)
def get_balance(session: Session = Depends(get_session)):
    """
    Calculate the total balance (Income - Expenses) by executing the sum in the DB.
    """
    income_query = select(func.sum(Transaction.amount)).where(Transaction.is_income == True)
    total_income = session.exec(income_query).one() or 0.0
    
    expense_query = select(func.sum(Transaction.amount)).where(Transaction.is_income == False)
    total_expense = session.exec(expense_query).one() or 0.0
    
    balance = total_income - total_expense
    
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "current_balance": balance
    }

@router.get("/{transaction_id}", response_model=TransactionRead)
def read_transaction(
    transaction_id: int,
    session: Session = Depends(get_session)
):
    """
    Get a transaction by ID.
    """
    query = select(Transaction).where(Transaction.id == transaction_id)
    transaction = session.exec(query).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction
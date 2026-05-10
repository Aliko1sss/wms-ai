from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.transaction import Transaction
from app.models.product import Product
from app.schemas.inventory import TransactionCreate
from uuid import UUID
from datetime import datetime

def get_stock_balance(db: Session, product_id: UUID) -> dict:
    result = db.query(
        func.sum(Transaction.qty_change).label("total"),
        Transaction.location_id
    ).filter(
        Transaction.product_id == product_id
    ).group_by(Transaction.location_id).all()
    
    total = sum(float(r[0] or 0) for r in result)
    locations = {str(r[1]): float(r[0] or 0) for r in result if r[1] is not None}
    return {"total": total, "locations": locations}

def create_transaction(db: Session, tx: TransactionCreate, user_id: UUID) -> Transaction:
    new_tx = Transaction(**tx.model_dump(), performed_by=user_id, created_at=datetime.utcnow())
    db.add(new_tx)
    db.commit()
    db.refresh(new_tx)
    return new_tx
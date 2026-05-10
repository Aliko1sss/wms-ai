from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.product import Product
from app.schemas.inventory import TransactionCreate, StockResponse
from app.services.ledger import create_transaction, get_stock_balance

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.get("/stock/{sku}", response_model=StockResponse)
def get_stock(sku: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.sku == sku).first()
    if not product:
        raise HTTPException(404, "Товар не найден")
    balance = get_stock_balance(db, product.id)
    return {"sku": sku, "name": product.name, "total": balance["total"], "locations": balance["locations"]}

@router.post("/transaction", status_code=201)
def create_tx(tx: TransactionCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not db.query(Product).filter(Product.id == tx.product_id).first():
        raise HTTPException(404, "Товар не найден")
    if tx.location_id and not db.query(Product).filter(Product.id == tx.location_id).first():
        # Упрощено: в проде проверка Location модели
        pass
    return create_transaction(db, tx, user.id)
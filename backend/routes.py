from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import ItemTable
from services import add_item, get_all_items, get_item_byID
from connect import get_db

router = APIRouter()

@router.get("/")
def root():
    return {"message" : "Hello"}

@router.post("/addItems")
def get_item(item: ItemTable, session: Session = Depends(get_db)):
    return add_item(item, session)

@router.get("/itemsList", response_model=list[ItemTable])
def get_itemlist(session: Session = Depends(get_db)):
    return get_all_items(session)

@router.get("/items/{item_id}", response_model=ItemTable)
def get_item_by_id(item_id: int, session: Session = Depends(get_db)):
    return get_item_byID(item_id, session)



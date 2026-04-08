from fastapi import HTTPException
from sqlmodel import Session
from database import ItemTable
from queries import get_count, get_all, get_by_id, put_item

def root():
    return {"message" : "Hello"}

def add_item(item: ItemTable, session: Session):
    item = ItemTable(item_name=item.item_name, price=item.price)
    items = put_item(item, session)
    return items

def get_all_items(session: Session):
    itemlist = get_all(session)

    if not itemlist:
        raise HTTPException(status_code=404, detail="User not found")
    return itemlist

def get_item_byID(item_id: int, session: Session) -> ItemTable:

    number = get_count(session)
    item = get_by_id(item_id, session)

    # Error handling: Return 404 if item_id is not found
    if item_id > number or item_id <= 0:
        raise HTTPException(status_code=404, detail="Invalid Item ID Request")
    return item
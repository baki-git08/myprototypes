from sqlmodel import select, Session
from sqlalchemy import func
from database import ItemTable
from fastapi import HTTPException

def get_all(session: Session):
    return session.exec(select(ItemTable))

def get_count(session: Session):
    stmt = select(func.count()).select_from(ItemTable)
    number = int(session.exec(stmt).one())
    return number

def get_by_id(id_: int, session: Session):
    stmt = select(ItemTable).where(ItemTable.id == id_)
    return session.exec(stmt).first()

def put_item(item: ItemTable, session: Session):
    session.add(item)
    session.commit()

    if len(item.item_name) < 20:
        raise HTTPException(status_code=400, detail="Item name must be at least 20 characters long.")
    return item


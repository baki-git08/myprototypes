from typing import Optional
from sqlmodel import SQLModel, Field

class ItemTable(SQLModel, table=True):
    __tablename__ = "ItemList"
    id: Optional[int] = Field(primary_key=True, default=None)
    item_name: str = Field(index=True, max_length=20)
    price: float = Field(default=0.0)
    is_done: bool = False
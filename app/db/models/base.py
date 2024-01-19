from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, SmallInteger
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:
    id: Any
    create_date = Column(DateTime, default=datetime.now, nullable=False)
    update_date = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    is_active = Column(SmallInteger, default=1)  # 1: active, 0: inactive
    __name__: str

    # to generate tablename from classname
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

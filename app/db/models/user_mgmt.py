from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String

from app.db.models.base import Base


class Users(Base):
    id = Column(Integer, primary_key=True, index=True)
    id_hash = Column(String(256), nullable=False, index=True)
    name = Column(String(256), nullable=False)
    email = Column(String(128), nullable=False)
    pass_hash = Column(String(123), nullable=False)
    pass_salt = Column(String(128), nullable=False)
    id_role = Column(SmallInteger, ForeignKey("roles.id"), nullable=False)


class Roles(Base):
    id = Column(SmallInteger, primary_key=True, index=True)
    name = Column(String(64), nullable=False)

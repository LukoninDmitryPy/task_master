from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from config import PG


Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {"schema": PG['schema']}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=True)
    status = Column(String(100), nullable=False, default='created')
    created_at = Column(DateTime, nullable=False, default='now()')
    updated_at = Column(DateTime, nullable=True)
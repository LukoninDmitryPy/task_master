from datetime import datetime as dt

from db.connection import dbconnect
from db.models import *
from utils.log import get_logger


class Repository:
    def __init__(self, Session):
        self.session = Session()
        self.logger = get_logger(__name__)

    @dbconnect
    def get_task(self, **kwargs):
        return self.session.query(Task).filter_by(**kwargs).first()
    @dbconnect
    def get_tasks(self, order_by, **kwargs):
        if order_by == "asc":
            return self.session.query(Task).filter_by(**kwargs).order_by(Task.created_at.asc()).all()
        else:
            return self.session.query(Task).filter_by(**kwargs).order_by(Task.created_at.desc()).all()
    
    @dbconnect
    def create_task(self, **kwargs):
        task = Task(**kwargs)
        self.session.add(task)
        self.session.commit()
        return task
    
    @dbconnect
    def update_status_task(self, stage:str, **kwargs):
        update_query = {Task.updated_at: dt.now()}
        if stage == 'proc':
            update_query.update({Task.status: 'processing'})
        elif stage == 'complete':
            update_query.update({Task.status: 'complete'})
        elif stage == 'error':
            update_query.update({Task.status: 'error'})
        self.session.query(Task).filter_by(**kwargs).update(update_query)
        self.session.commit()
    

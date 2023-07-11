from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, func

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    id = Column(db.Integer,primary_key=True,autoincrement=True)
    active = Column(db.Boolean, default=1)
    create_time = Column(db.DateTime, default=datetime.now())
    update_time = Column(db.DateTime, default=datetime.now(), onupdate=func.utc_timestamp())


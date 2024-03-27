from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import MetaData, DateTime
from sqlalchemy.orm import declarative_base

meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)
Base = declarative_base(metadata=meta)


class CreatedMixin:
    created_datetime = Column(DateTime, nullable=False, default=datetime.utcnow)


class UpdatedMixin:
    updated_datetime = Column(DateTime)

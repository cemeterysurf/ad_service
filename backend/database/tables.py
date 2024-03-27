from enum import Enum as PyEnum

from passlib.context import CryptContext
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy import DateTime
from sqlalchemy import (
    String, Text, Enum, UniqueConstraint)
from sqlalchemy.orm import relationship

from backend.database.base_table import Base, CreatedMixin, UpdatedMixin
from backend.database.config import PW_CONF

pwd_ctx = CryptContext(**PW_CONF)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    hashed_password = Column(String(255))
    full_name = Column(String(255))
    phone = Column(String(255))

    sessions = relationship('Session', back_populates="user")
    ads = relationship('Ad', back_populates="creator")
    comments = relationship('Comment', back_populates="user")

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, val):
        self.hashed_password = pwd_ctx.hash(val)

    def verify_password(self, password: str):
        return pwd_ctx.verify(password, self.hashed_password)


class Session(Base):
    __tablename__ = 'session'

    token = Column(String, primary_key=True)
    expires = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates="sessions")

    __table_args__ = (
        UniqueConstraint('user_id'),
    )


class AdType(PyEnum):
    purchase = "purchase"
    sell = "sell"
    service = "service"


class Ad(Base, CreatedMixin, UpdatedMixin):
    __tablename__ = "ad"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    body = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    price = Column(String(255), nullable=True, default=None)
    location = Column(String(255), nullable=True, default=None)
    type = Column(Enum(AdType))
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))

    creator = relationship('User', back_populates="ads")
    comments = relationship('Comment', back_populates="ad")
    complaints = relationship('Complaint', back_populates="advert")

    __table_args__ = (
        UniqueConstraint('user_id'),
    )


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    body = Column(Text)
    ad_id = Column(ForeignKey("ad.id", ondelete="CASCADE"))
    created_by = Column(ForeignKey("user.id", ondelete="SET NULL"))

    user = relationship('User', back_populates="comments")
    ad = relationship('Ad', back_populates="comments")

    __table_args__ = (
        UniqueConstraint('created_by'),
    )


class Complaint(Base, CreatedMixin):
    __tablename__ = "complaint"

    id = Column(Integer, primary_key=True, autoincrement=True)
    body = Column(Text)
    created_by = Column(ForeignKey("user.id", ondelete="SET NULL"))
    ad_id = Column(ForeignKey("ad.id", ondelete="CASCADE"))

    ad = relationship('Ad', back_populates="complaints")
    creator = relationship('User', back_populates="complaints")

    __table_args__ = (
        UniqueConstraint('created_by', 'ad_id'),
    )

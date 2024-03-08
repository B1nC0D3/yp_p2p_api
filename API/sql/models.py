from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint, BigInteger, DateTime, Enum
from sqlalchemy.sql import func

from .database import Base
from .models_enums import ReviewStateEnum


class Scope(Base):

    __tablename__ = 'scopes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    def __str__(self):
        return self.name


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    discord_id = Column(BigInteger, unique=True, index=True, nullable=False)


class UserToScope(Base):

    __tablename__ = 'users_to_scopes'
    __table_args__ = (UniqueConstraint('user_id', 'scope_id'),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    scope_id = Column(Integer, ForeignKey('scopes.id'), nullable=False)


class P2PRequest(Base):
    __tablename__ = 'p2p_requests'

    id = Column(Integer, primary_key=True, index=True)
    repository_link = Column(String, index=True, nullable=False)
    comment = Column(String, nullable=False, default='')
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    publication_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    review_state = Column(
        Enum(ReviewStateEnum, name='review_state_enums', values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
    )
    reviewer_id = Column(Integer, ForeignKey('users.id'))
    review_start_date = Column(DateTime(timezone=True))

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    privileges = Column(String, nullable=False, default='users')
    created_at = Column(DateTime, default=func.now())

    subscriptions = relationship("Subscription", back_populates="user")
    logs = relationship("Logs", back_populates="user")


class NewsSource(Base):
    __tablename__ = "news_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    url = Column(String, unique=True, nullable=False)

    headlines = relationship("NewsHeadline", back_populates="source")
    subscriptions = relationship("Subscription", back_populates="source")


class NewsHeadline(Base):
    __tablename__ = "news_headlines"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    url = Column(String, unique=True, nullable=False)
    source_id = Column(Integer, ForeignKey("news_sources.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())

    source = relationship("NewsSource", back_populates="headlines")



class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("news_sources.id"), nullable=False)
    subscription_type = Column(String, nullable=False)  # Например, "daily" или "instant"
    banned = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="subscriptions")
    source = relationship("NewsSource", back_populates="subscriptions")


class Logs(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="logs")

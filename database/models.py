from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.Base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    privileges = Column(String, nullable=False, default='users')
    created_at = Column(DateTime, default=func.now())
    is_banned = Column(Boolean, default=False)

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
    category = Column(String, nullable=False)
    date_published = Column(DateTime, nullable=False)
    source_id = Column(Integer, ForeignKey("news_sources.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())

    source = relationship("NewsSource", back_populates="headlines")



class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("news_sources.id"), nullable=False)
    subscription_type = Column(String, nullable=False)  # Например, "daily" или "instant"

    user = relationship("User", back_populates="subscriptions")
    source = relationship("NewsSource", back_populates="subscriptions")


class Logs(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="logs")


class BotConfig(Base):
    __tablename__ = "bot_config"

    id = Column(Integer, primary_key=True, index=True)
    auto_parse_interval = Column(Integer, nullable=False, default=30)
    subscription_price = Column(Float, default=0)
    crypto_wallet = Column(String, nullable=True)
    about_text_config = Column(String, nullable=False, default='Привет. Ты попал на новостного бота.')
    faq_text_config = Column(String, nullable=False, default='Функционал бота:\n1. Возможность получать новости по запросу')
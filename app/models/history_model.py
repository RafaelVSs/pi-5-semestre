from __future__ import annotations

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from ..db.database import Base

from sqlalchemy.sql import func

class History(Base):
    __tablename__ = "history"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    player_name = Column(String(255), nullable=False)
    average_rebounds = Column(Float, nullable=False)
    position = Column(String(50), nullable=False)
    average_points = Column(Float, nullable=False)
    average_assists = Column(Float, nullable=False)
    classification = Column(String(255), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user_id = Column(Integer, ForeignKey('public.users.id'))
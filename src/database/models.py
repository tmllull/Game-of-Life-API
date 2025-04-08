from sqlalchemy import Column, Date, Integer, String, UniqueConstraint
from src.config.database import Base


class Ecosystem(Base):
    __tablename__ = "ecosystems"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ecosystem = Column(String(255))
    evolutions = Column(Integer)
    messages = Column(Integer)
    total_messages = Column(Integer)
    born_date = Column(Date)
    extinction_date = Column(Date)
    creator = Column(String(255))
    killer = Column(String(255))

    __table_args__ = (UniqueConstraint("id"),)

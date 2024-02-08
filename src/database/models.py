from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

import config
from .db_session import engine
from src.utils.helpers import timed_lru_cache


class Base(DeclarativeBase):
    pass


class InstrumentPriceModifier(Base):
    __tablename__ = 'INSTRUMENT_PRICE_MODIFIER'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    multiplier: Mapped[float] = mapped_column(nullable=False)

    @classmethod
    @timed_lru_cache(seconds=config.CACHE_TTL, maxsize=10)
    def get(cls, session, name: str) -> Optional[float]:
        record = session.query(cls).filter(cls.name == name).first()
        return record.multiplier if record else None

    @classmethod
    def insert(cls, session, name: str, value: float) -> bool:
        record = cls(name=name, multiplier=value)
        session.add(record)
        session.commit()
        return True


Base.metadata.create_all(engine)

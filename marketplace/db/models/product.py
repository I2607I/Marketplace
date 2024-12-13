from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER, TEXT, TIMESTAMP, FLOAT
from sqlalchemy.sql import func

from marketplace.db import DeclarativeBase


class Product(DeclarativeBase):
    __tablename__ = "product"

    id = Column(
        INTEGER,
        primary_key=True,
        autoincrement=True,
        unique=True,
    )
    name = Column(
        TEXT,
        nullable=False,
    )
    description = Column(
        TEXT,
        nullable=True,
    )
    price = Column(
        FLOAT,
        index=True,
        nullable=False,
    )
    currency = Column(
        TEXT,
        nullable=False,
    )
    category = Column(
        TEXT,
        nullable=True,
    )
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )

    def __repr__(self):
        columns = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return f'<{self.__tablename__}: {", ".join(map(lambda x: f"{x[0]}={x[1]}", columns.items()))}>'

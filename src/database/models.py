from sqlalchemy import BigInteger, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    country_name: Mapped[str] = mapped_column(String(255), nullable=False)
    population_before: Mapped[int] = mapped_column(BigInteger, nullable=True)
    population_after: Mapped[int] = mapped_column(BigInteger, nullable=True)
    region: Mapped[str] = mapped_column(String(255), nullable=True)
    sub_region: Mapped[str] = mapped_column(String(255), nullable=False)

    __table_args__ = (
        UniqueConstraint("country_name", name="unique_country_name"),
    )

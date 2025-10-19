# ruff:noqa:F821
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.associations_tables import organization_activities


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(155), nullable=False)
    phones: Mapped[list["Phone"]] = relationship("Phone", back_populates="organization")
    building_id: Mapped[int] = mapped_column(Integer, ForeignKey("buildings.id"), nullable=False)
    building: Mapped["Building"] = relationship("Building", back_populates="organizations")
    activities: Mapped[list["Activity"]] = relationship(
        "Activity", secondary=organization_activities, back_populates="organizations"
    )

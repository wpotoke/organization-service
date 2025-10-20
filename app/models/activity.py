# ruff:noqa:F821
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.associations_tables import organization_activities


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(155), nullable=False, unique=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("activities.id"), nullable=True)

    organizations: Mapped[list["Organization"]] = relationship(
        "Organization", secondary=organization_activities, back_populates="activities"
    )
    parent: Mapped[Optional["Activity"]] = relationship(
        "Activity", back_populates="children", remote_side=[id]
    )
    children: Mapped[list["Activity"]] = relationship("Activity", back_populates="parent")

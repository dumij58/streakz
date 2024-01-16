from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List
from datetime import datetime

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

class Habit(db.Model):
  id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
  title: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
  desc: Mapped[str]
  entries: Mapped[List["Entry"]] = relationship(
    back_populates="habit",
    cascade="all, delete-orphan"
  )
  
  def __repr__(self) -> str:
    return f"Habit(id={self.id!r}, title={self.title!r})"


class Entry(db.Model):
  id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
  habit_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
  habit: Mapped["Habit"] = relationship(back_populates="entries")
  checked_dt: Mapped[datetime] = mapped_column(db.DateTime, nullable=False)

  def __repr__(self) -> str:
    return f"Entry(id={self.id!r}, habit={self.habit!r})"
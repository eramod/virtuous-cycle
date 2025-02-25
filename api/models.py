import datetime
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from api.app import db

class User(db.Model):
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  email: Mapped[str] = mapped_column(unique=True, nullable=False)
  password_hash: Mapped[str] = mapped_column(nullable=False)
  first_name: Mapped[str] = mapped_column(nullable=False)
  last_name: Mapped[str] = mapped_column(nullable=False)
  phone_number: Mapped[str] = mapped_column(nullable=False)

  quotes: Mapped[List["Quote"]] = relationship(back_populates="user")

  # ChatGPT recommended adding these two methods along with switching to a password_hash property. These use werkzeug.security methods to hash the password.
  def set_password(self, password: str):
    """Hash and store password securely"""
    self.password_hash = generate_password_hash(password)

  def check_password(self, password: str) -> bool:
    """Verify password against stored hash"""
    return check_password_hash(self.password_hash, password)

  def __repr__(self):
    return (
      f"<User (ID: {self.id}, Email: {self.email}, "
      f"First Name: {self.first_name}, Last Name: {self.last_name}, "
      f"Phone Number: {self.phone_number})>"
    )

class Quote(db.Model):
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
  content: Mapped[str] = mapped_column(nullable=False)
  attribution: Mapped[str] = mapped_column(nullable=True)
  created: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now(datetime.timezone.utc))

  user: Mapped["User"] = relationship(back_populates="quotes")

  def __repr__(self):
    attribution_part = f", Attribution: {self.attribution}" if self.attribution else ""

    return (
      f"<Quote (ID: {self.id}, Author ID: {self.author_id}, "
      f"Content: {self.content[:30]}..., Created: {self.created})>"
      f"{attribution_part})>"
    )
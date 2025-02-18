import datetime
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.app import db
from typing import List

class User(db.Model):
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  email: Mapped[str] = mapped_column(unique=True, nullable=False)
  first_name: Mapped[str] = mapped_column(nullable=False)
  last_name: Mapped[str] = mapped_column(nullable=False)
  phone_number: Mapped[int] = mapped_column(nullable=False)
  quotes: Mapped[List["Quote"]] = relationship(back_populates="user")

  def __repr__(self):
    f'''
      <User (ID: {self.id}
        Email: {self.email}
        First Name: {self.first_name}
        Last Name: {self.last_name}
        Phone Number: {self.phone_number}
      )>
    '''

class Quote(db.Model):
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
  content: Mapped[str] = mapped_column(nullable=False)
  attribution: Mapped[str]
  created: Mapped[datetime.datetime] = mapped_column(nullable=False)
  user: Mapped["User"] = relationship(back_populates="quotes")

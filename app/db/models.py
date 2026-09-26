from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from pydantic import ConfigDict


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    notes = relationship("Note", cascade="all, delete-orphan")
    

class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True )
    text: Mapped[str] = mapped_column(nullable=False)
    is_done: Mapped[bool] = mapped_column(default=False, nullable=False)
    

from db.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


class UserRepo():
    def __init__(self, sesion=AsyncSession):
        session = session.AsyncSession

    def get_user_by_id(self, user_id: int) -> User | None:
        result = self.session.get(User, user_id)
        return result.scalars().one_or_none()

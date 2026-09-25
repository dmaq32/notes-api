import os
import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.config import get_db
from app.db.models import User
from jwt.exceptions import PyJWTError


load_dotenv()

bearer_scheme = HTTPBearer()


def create_jwt_token(data: dict):
    return jwt.encode(data, key=os.getenv("JWT_SECRET"), algorithm="HS256")



async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
    ) -> User:
    token = creds.credentials            
    try:
        payload = jwt.decode(token, key=os.getenv("JWT_SECRET"), algorithms=["HS256"])
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload["sub"])
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
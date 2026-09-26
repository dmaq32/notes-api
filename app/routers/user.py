from fastapi import HTTPException
from app.db.schemas import UserCreate, UserOut, UserAuth
from app.db.models import User
from app.db.config import get_db
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.rabbitmq.config import channel
from app.utils import create_jwt_token
from datetime import timezone, timedelta, datetime
import json
import bcrypt
import os





user_router = APIRouter(prefix="/users", tags=["users"])




@user_router.post("/register", status_code=201)
async def add_user(
    data: UserCreate, 
    db: AsyncSession = Depends(get_db)
    ):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if user:
        raise HTTPException(status_code=409, detail="Такой пользователь уже зарегистрирован")
    hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()
    user = User(name=data.name, email=data.email, password_hash=hashed )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    message = {"id": user.id, "name": user.name, "email": user.email}
    channel.basic_publish(exchange='',
                      routing_key='test_queue',
                      body=json.dumps(message)
    )
    return message

@user_router.get("/", response_model=list[UserOut])
async def get_users(db: AsyncSession=Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

@user_router.post("/login")
async def authorize(
    data: UserAuth,
    db: AsyncSession=Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401)
    password = bcrypt.checkpw(data.password.encode(), user.password_hash.encode())
    if not password:
        raise HTTPException(status_code=401)
    token = create_jwt_token(
        {"sub": str(user.id), "exp": datetime.now(timezone.utc) + timedelta(hours=1)})
    return {"access_token": token, "token_type": "bearer"}
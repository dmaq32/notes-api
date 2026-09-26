from fastapi import HTTPException
from app.db.schemas import NoteCreate, NoteOut, NoteUpdate, NoteOutEmail
from app.db.models import User, Note
from app.db.config import get_db
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, join
from app.utils import get_current_user
from app.rabbitmq.config import channel
import json



note_router = APIRouter(prefix="/notes", tags=["notes"])


channel.queue_declare(queue='test_queue', durable=True, arguments={'x-queue-type': 'quorum'})



@note_router.post("/add_note", status_code=201)
async def add_note(data: NoteCreate ,
                db: AsyncSession=Depends(get_db),
                user: User = Depends(get_current_user)
    ):  
    note = Note(user_id=user.id,text=data.text)
   
    db.add(note)
    await db.commit()
    await db.refresh(note)

    message = {"note_id": note.id, "user_id": note.user_id, "event": "created"}

    channel.basic_publish(exchange='',
                      routing_key='test_queue',
                      body=json.dumps(message)
    )
    return {
        "id": note.id,
        "user_id": note.user_id,
        "text": note.text,
        "is_done": note.is_done
    }
@note_router.get("/",response_model=list[NoteOut])
async def get_notes(db: AsyncSession=Depends(get_db),user: User=Depends(get_current_user), filter: str | None = None, limit: int=3, offset: int=0):
    stmt = select(Note).where(Note.user_id == user.id).order_by(Note.id).offset(offset).limit(limit)
    if filter is not None:
        result = await db.execute(stmt.where(Note.text.icontains(filter)))
    else:
        result = await db.execute(stmt)

    return result.scalars().all()

@note_router.get("/{note_id}", response_model=NoteOutEmail)
async def get_note(note_id: int, db: AsyncSession=Depends(get_db), user: User = Depends(get_current_user)):
    res = await db.execute(select(Note, User.email).join(User, User.id == Note.user_id).where(Note.user_id == user.id).where(Note.id == note_id))
    row = res.first()
    if row is None:
        raise HTTPException(status_code=404)
    note, email = row
    return {
        "id": note.id,
        "user_id": note.user_id,
        "text": note.text,
        "is_done": note.is_done,
        "email": email
    }


@note_router.delete("/{note_id}", status_code=204)
async def delete_note(note_id: int, user: User=Depends(get_current_user), db: AsyncSession=Depends(get_db)):
    note = await db.get(Note, note_id)
    if not note or note.user_id != user.id:
        raise HTTPException(status_code=404, detail="Note not Found")
    await db.delete(note)
    await db.commit()
    return None

@note_router.patch("/{note_id}", response_model=NoteOut)
async def edit_note(note_id: int, noteupd: NoteUpdate, user: User=Depends(get_current_user),db: AsyncSession=Depends(get_db)):
    note = await db.get(Note, note_id)
    if not note or note.user_id != user.id:
            raise HTTPException(status_code=404, detail="Note not Found")
    if noteupd.text is not None:
        note.text = noteupd.text
    if noteupd.is_done is not None:
        note.is_done = noteupd.is_done
    await db.commit()
    await db.refresh(note)
    return note

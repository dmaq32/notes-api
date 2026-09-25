from app.db.models import Note
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

class NoteRepo:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_id(self, note_id: int) -> Note | None:
        result = await self.session.get(Note,note_id)
        if not result:
            raise HTTPException(status_code=404)
        return result


    async def toggle_is_done(self, note_id: int) -> Note | None:
        Note = await self.get_by_id(note_id=note_id)
        Note.is_done = not Note.is_done
        await self.session.flush()


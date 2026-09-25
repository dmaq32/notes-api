from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    
    model_config = ConfigDict(from_attributes=True)
    

class UserOut(BaseModel):
    id: int
    name: str
    email: str    
    model_config = ConfigDict(from_attributes=True)

class UserAuth(BaseModel):
    email: str
    password: str


class NoteCreate(BaseModel):
    text: str

class NoteUpdate(BaseModel):
    text: str | None = None
    is_done: bool | None = None
    
    model_config = ConfigDict(from_attributes=True)

class NoteOut(BaseModel):
    id: int
    user_id: int
    text: str
    is_done: bool | None = False

    model_config = ConfigDict(from_attributes=True)


class NoteOutEmail(BaseModel):
    id: int
    user_id: int
    text: str
    is_done: bool | None = False
    email: str

    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel
from typing import Optional, List

class User(BaseModel):
    username: str
    email: str
    password: str  # hashed

class Resume(BaseModel):
    user_id: str
    content: str  # or bytes for PDF

class JobPreference(BaseModel):
    user_id: str
    titles: List[str]
    locations: List[str]
    skills: List[str] 
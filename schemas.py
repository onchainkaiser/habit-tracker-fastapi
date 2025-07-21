from pydantic import BaseModel
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        from_attributes = True

class CreateHabit(BaseModel):
    name: str
    category: str
    target_per_day: int

class HabitResponse(BaseModel):
    id: int
    name: str
    category: str
    target_per_day: int
    class Config:
        from_attributes = True

class HabitUpdate(BaseModel):
    name: Optional[str]
    category: Optional[str]
    target_per_day: Optional[int]

class ProgressCreate(BaseModel):
    habit_id: int
    date_tracked: date
    amount_done: int

class ProgressResponse(BaseModel):
    id: int
    habit_id: int
    date_tracked: date
    amount_done: int
    class Config:
        from_attributes = True
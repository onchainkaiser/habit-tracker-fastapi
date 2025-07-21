from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from models import Base, Habit, Progress, User
import models
import schemas
from jose import JWTError, jwt
from auth import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM

app = FastAPI(title="HABIT TRACKER")
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
def read_root():
    return {"message": "Welcome to the habit tracker API"}

@app.post("/habits", response_model=schemas.HabitResponse)
def create_habit(habit: schemas.CreateHabit, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_habit = Habit(
        name=habit.name,
        category=habit.category,
        target_per_day=habit.target_per_day,
        user_id=current_user.id
    )
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    return new_habit

@app.get("/habits", response_model=list[schemas.HabitResponse])
def get_all_habits(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Habit).filter(Habit.user_id == current_user.id).all()

@app.get("/habits/{habit_id}", response_model=schemas.HabitResponse)
def get_habit(habit_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == current_user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

@app.put("/habits/{habit_id}", response_model=schemas.HabitResponse)
def update_habit(habit_id: int, habit_data: schemas.HabitUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == current_user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    if habit_data.name is not None:
        habit.name = habit_data.name
    if habit_data.category is not None:
        habit.category = habit_data.category
    if habit_data.target_per_day is not None:
        habit.target_per_day = habit_data.target_per_day
    db.commit()
    db.refresh(habit)
    return habit

@app.delete("/habits/{habit_id}", status_code=204)
def delete_habit(habit_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == current_user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    db.delete(habit)
    db.commit()
    return Response(status_code=204)

@app.post("/progress", response_model=schemas.ProgressResponse)
def create_progress(progress: schemas.ProgressCreate, db: Session = Depends(get_db)):
    new_progress = Progress(**progress.dict())
    db.add(new_progress)
    db.commit()
    db.refresh(new_progress)
    return new_progress

@app.get("/progress", response_model=list[schemas.ProgressResponse])
def get_all_progress(db: Session = Depends(get_db)):
    return db.query(Progress).all()

@app.get("/habits/{habit_id}/progress", response_model=list[schemas.ProgressResponse])
def get_progress_for_habit(habit_id: int, db: Session = Depends(get_db)):
    return db.query(Progress).filter(Progress.habit_id == habit_id).all()

@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

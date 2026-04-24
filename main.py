from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks")
def create_task(title: str, priority: str, db: Session = Depends(get_db)):
    task = models.Task(title=title, priority=priority)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()
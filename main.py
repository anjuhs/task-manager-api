from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

tasks = []

class Task(BaseModel):
    title: str
    completed: bool = False
    priority: str

@app.get("/")
def home():
    return {"message": "Task Manager API is running"}

@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)
    return {"message": "Task added", "task": task}

@app.get("/tasks")
def get_tasks():
    return tasks
# Task Manager API

A simple REST API built using FastAPI to manage tasks with priority and completion status.

## Features
- Create tasks
- View all tasks
- Update tasks
- Delete tasks
- Persistent storage using SQLite
- Track priority and completion status

## API Endpoints
- GET /tasks
- POST /tasks
- PUT /tasks/{id}
- DELETE /tasks/{id}

## Tech Stack
- Python
- FastAPI

## How to Run

```bash
pip install fastapi uvicorn
uvicorn main:app --reload






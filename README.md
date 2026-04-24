# 🚀 Task Manager API

A fully functional RESTful backend application built using FastAPI with SQLite database integration and deployed on Render.

## 🌐 Live Demo

👉 https://task-manager-api-zayg.onrender.com/docs

## 📌 Features

* Create tasks with priority and status
* View all tasks
* Update tasks
* Delete tasks
* Persistent storage using SQLite database

## 🛠 Tech Stack

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Uvicorn
* Render (Deployment)

## ⚙️ API Endpoints

* GET / → Check API status
* GET /tasks → Get all tasks
* POST /tasks → Create new task
* PUT /tasks/{id} → Update task
* DELETE /tasks/{id} → Delete task

## ▶️ Run Locally

```bash
git clone https://github.com/anjuhs/task-manager-api.git
cd task-manager-api
pip install -r requirements.txt
uvicorn main:app --reload
```

## 📷 API Preview

Visit `/docs` for interactive Swagger UI.

## 💡 Highlights

* Designed RESTful architecture
* Implemented CRUD operations
* Integrated relational database (SQLite)
* Deployed to production using Render

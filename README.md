# 🧠 Habit Tracker API

A secure and simple Habit Tracker API built with **FastAPI**, **JWT Authentication**, and **PostgreSQL**.

This backend allows users to register, log in, and track daily habits with progress entries. It features user-based data separation and token-based auth to ensure privacy and scalability.

---

## 🚀 Features

- 🔐 JWT-based user authentication (`/register`, `/login`)
- 📊 Habit CRUD endpoints (Create, Read, Update, Delete)
- 📈 Track progress for each habit daily
- 👤 Authenticated user access only
- 🛡️ PostgreSQL + SQLAlchemy ORM
- 📄 Swagger docs available at `/docs`

---

## 🧪 API Endpoints

### 🔑 Auth
- `POST /register`: Register a new user
- `POST /login`: Login with username & password

### 🧠 Habits
- `GET /habits`: List your habits
- `GET /habits/{habit_id}`: Get a single habit
- `POST /habits`: Create a new habit
- `PUT /habits/{habit_id}`: Update habit
- `DELETE /habits/{habit_id}`: Delete habit

### 📅 Progress
- `GET /progress`: Get all progress entries
- `POST /progress`: Add a new progress log
- `GET /habits/{habit_id}/progress`: Get progress for a habit

---

## ⚙️ Tech Stack

- **FastAPI** (Web framework)
- **SQLAlchemy** (ORM)
- **PostgreSQL** (Database)
- **PassLib + Bcrypt** (Password hashing)
- **Pydantic** (Validation)
- **Uvicorn** (Server)

---

## 📦 Setup Instructions

1. **Clone repo**
   ```bash
   git clone https://github.com/onchainkaiser/habit-tracker-fastapi.git
   cd habit-tracker-fastapi
2. Create and activate virtual environment

python -m venv myenv
myenv\Scripts\activate

3.Install dependencies
pip install -r requirements.txt

4. Configure database (PostgreSQL)
Create a .env file and add:
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
SECRET_KEY=your_secret_key_here

5. Reset DB (optional)
python reset_db.py

6.Run the server
uvicorn main:app --reload

👤 Author
kaiser codez
GitHub: @onchainkaiser

📌 License
This project is licensed under the MIT License.
---

Let me know if you want:
- Badges (e.g. build passing, python version)
- Docker support
- Deployment setup (e.g. Railway or Render)
- GUI usage guide (for the future `customtkinter` app)

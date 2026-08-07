# 🧠 Dhvani — AI Knowledge Assistant

Dhvani is an AI-powered knowledge assistant built using **FastAPI**, **Streamlit**, and **Google Gemini**.

The project focuses on understanding the complete architecture of modern GenAI applications by building every component from scratch instead of relying on high-level frameworks. It is being developed incrementally—from a simple LLM-powered summarizer to a complete Retrieval-Augmented Generation (RAG) platform.

---

# 🚀 Features

## AI Summarization

- Summarize lengthy notes using Google Gemini
- Multiple summary lengths
  - Short
  - Medium
  - Detailed
- Audience-aware summaries
  - Student
  - Interview Preparation
  - Research
- Custom user instructions
- Prompt-engineering based architecture

---

## Authentication & Security

- User Signup
- User Login
- JWT Authentication
- Password Hashing (bcrypt)
- Protected API Endpoints
- Email Verification
- Daily Usage Tracking

---

## File Support

- Upload PDF Notes
- Extract PDF Content
- Summarize Uploaded Documents

---

## Developer Features

- FastAPI REST APIs
- Interactive Swagger Documentation
- Structured Logging
- Modular Backend Architecture
- Pydantic Validation
- Environment-based Configuration

---

# 🛠 Tech Stack

### Backend

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

### Frontend

- Streamlit

### AI

- Google Gemini API
- Prompt Engineering

### Authentication

- JWT
- Passlib (bcrypt)

### Email

- SMTP (Gmail App Password)

### Utilities

- PyPDF
- python-dotenv
- Uvicorn

---

# 📂 Project Structure

```text
Dhvani/

│

├── backend/
│   ├── auth.py
│   ├── database.py
│   ├── dependencies.py
│   ├── email_service.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   └── main.py
│
├── frontend/
│   └── frontend.py
│
├── uploads/
│
├── requirements.txt
├── .env
├── README.md
└── .gitignore
```

The project structure will continue evolving as new AI capabilities are introduced.

---

# ⚙️ Setup

## Clone Repository

```bash
git clone https://github.com/codedbygunnaj/AI-Notes-Summarizer.git

cd AI-Notes-Summarizer
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
GEMINI_API_KEY=

SECRET_KEY_JWT=

SMTP_EMAIL=
SMTP_PASSWORD=

BACKEND_URL=
```

---

# ▶️ Run the Backend

```bash
uvicorn backend.main:app --reload
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

# ▶️ Run the Frontend

```bash
streamlit run frontend/frontend.py
```

---

# 📬 API

## Authentication

```
POST /auth/signup

POST /auth/login

GET /auth/verify
```

---

## AI

```
POST /summarize
```

Protected using JWT Authentication.

---

# 📌 Current Status

## ✅ Version 2.9

- LLM-powered summarization
- PDF summarization
- Prompt Engineering
- JWT Authentication
- Email Verification
- Protected APIs
- Daily Usage Tracking
- Streamlit Frontend
- Modular FastAPI Backend

---

# 🗺 Roadmap

### Completed

- LLM APIs
- Prompt Engineering
- FastAPI Backend
- Streamlit Frontend
- Authentication
- Email Verification

### In Progress

- Response Analytics
- Better Usage Management

### Upcoming

- Embedding Models
- Vector Databases
- Manual RAG
- Multi-document Chat
- Conversation Memory
- LangChain
- AI Agents
- LangGraph

---

# 🎯 Learning Philosophy

Every feature is built by first understanding the underlying concept instead of directly using frameworks.

```
Concept
    ↓
Why it exists
    ↓
Architecture
    ↓
Implementation
    ↓
Optimization
```

The objective is not only to build AI applications but to understand the reasoning behind every layer involved in modern AI systems.

---

# 👨‍💻 Author

**Gunaj Chugh**

- GitHub: https://github.com/codedbygunnaj
- LinkedIn: https://www.linkedin.com/in/gunajchugh/

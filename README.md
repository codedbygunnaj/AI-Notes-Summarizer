# 🧠 AI Notes Summarizer

An AI-powered Notes Summarizer built using **FastAPI** and **Google Gemini API**.

The project focuses on learning the fundamentals of building GenAI applications from scratch before introducing frameworks like LangChain, RAG, and Agents.

---

## 🚀 Features

- Summarize long notes using Google's Gemini models
- Multiple summary lengths
  - Short
  - Medium
  - Detailed
- Audience-specific summaries
  - Student
  - Interview Preparation
  - Research
- Prompt Engineering based architecture
- REST API using FastAPI
- Interactive Swagger documentation

---

## 🛠 Tech Stack

- Python
- FastAPI
- Google Gemini API
- Pydantic
- python-dotenv
- Uvicorn

---

## 📂 Project Structure

```
AI-Notes-Summarizer/
│
├── backend.py          # FastAPI Backend
├── .env                # Gemini API Key
├── requirements.txt
├── README.md
└── .gitignore
```

> The project structure will evolve as new features are added.

Future folders:

```
prompts/
services/
models/
config/
frontend/
```

---

## ⚙️ Setup

### Clone Repository

```bash
git clone https://github.com/codedbygunnaj/AI-Notes-Summarizer.git
cd AI-Notes-Summarizer
```

### Create Virtual Environment

Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Generate an API key from Google AI Studio.

---

## ▶️ Run the Backend

```bash
uvicorn backend:app --reload
```

Server starts at

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

---

## 📬 API Endpoint

### POST `/summarize`

Example Request

```json
{
  "text": "Your notes go here...",
  "summary_type": "medium",
  "audience": "student"
}
```

Example Response

```json
{
  "summary": "Generated summary..."
}
```

---

## 🧠 Learning Goals

This project is intentionally built without frameworks such as LangChain in the beginning.

The objective is to understand every layer involved in a GenAI application, including:

- LLM APIs
- Prompt Engineering
- FastAPI
- Request Validation
- Software Architecture
- Modular Prompt Design

Later versions will introduce:

- Streamlit Frontend
- Response Timing
- Token Usage
- Better Error Handling
- Markdown/PDF Export
- Embedding Models
- Vector Databases
- RAG
- LangChain
- Tool Calling
- Agents
- LangGraph

---

## 📌 Current Status

### ✅ Version 1

- FastAPI backend
- Gemini API integration
- Prompt engineering
- Audience-aware summaries
- Multiple summary types
- Swagger testing

---

## 🔮 Upcoming Features

- Streamlit Frontend
- Better UI/UX
- Copy & Download Summary
- Response Time Tracking
- Token Usage Analytics
- Modular Project Architecture
- RAG-based PDF Chat
- Multi-LLM Support

---

## 📖 Purpose

This repository documents my journey of learning Generative AI through hands-on projects while understanding the reasoning and architecture behind every component instead of relying solely on high-level frameworks.

Every feature is built with the philosophy:

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

The goal is not just to build working AI applications, but to understand how they work internally.

---
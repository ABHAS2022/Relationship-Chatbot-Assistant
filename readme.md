# 💬 Relationship Chatbot Assistant

A Python-based relationship chatbot assistant powered by Groq-hosted large language models (LLMs), containerized using Docker. It offers meaningful and contextual relationship conversations with persistent chat history using a MariaDB backend.

---

## 📦 Features

- 🤖 LLM-backed intelligent relationship assistant  
- 🗄️ SQLAlchemy ORM with MariaDB storage  
- 🔐 Secure key handling using `GROQ_API_KEY` from system environment  
- 🐳 Easily deployable with Docker and Docker Compose  

---

## 🗂 Project Structure

```
chat_app/
│
├── database/
│   ├── db_connector.py
│   ├── db_queries.py
│   ├── db_tables.py
│   └── db.sql
├── app.py
├── enums.py
├── utils.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/relationship-chatbot.git
cd relationship-chatbot
```

### 2. Set the GROQ_API_KEY (required)

You must export your `GROQ_API_KEY` as a system environment variable **before** running the container.

#### On Linux/macOS:
```bash
export GROQ_API_KEY=your_groq_api_key_here
```

#### On Windows (PowerShell):
```powershell
$env:GROQ_API_KEY = "your_groq_api_key_here"
```

---

## 🐳 Docker Instructions

### 1. Build and Start the App

```bash
docker-compose up --build
```

This will:
- Build the Docker image for the app
- Launch the MariaDB container and initialize it using `db.sql`
- Start the chatbot app, which connects to Groq using the `GROQ_API_KEY` from your system environment

Once running, access the app at: [http://localhost:8501](http://localhost:8501)

---

## 🛠 Tech Stack

- **Python 3.11**
- **Streamlit** for the frontend interface
- **SQLAlchemy** for database interaction
- **MariaDB** as the backend database
- **Groq Cloud API** for LLM inference
- **Docker & Docker Compose** for deployment

---

## 🧠 Database Schema

Two core tables:
- `users`: stores user details and identity hashes
- `messages`: stores chat history including message types, threads, and timestamps

Schema auto-initialized from `db.sql` during the first database boot.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙌 Contributing

Contributions, feedback, or issues are welcome. Fork the repository and open a pull request or issue.

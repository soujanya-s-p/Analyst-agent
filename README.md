# 🤖 Agentic SQL Analytics Analyst (v2026)

A **high-performance, self-healing AI analytics agent** that converts natural-language business questions into **safe, executable SQL queries** over structured data.

Built with **Google Gemini 3 Flash**, **Streamlit**, and **SQLite**, this project demonstrates a **production-grade “Chat with Data” system** — focusing on **reliability, security, and analyst workflow compression**, not chatbot gimmicks.

> **Design Philosophy:**  
> Automate *junior analyst execution* while keeping humans responsible for interpretation and strategy.

---

## 🚀 Key Features

### 🔁 Self-Healing SQL Loop
- Automatically detects SQL execution failures
- Captures `sqlite3.OperationalError` logs
- Re-prompts the LLM with error context
- Retries query generation **up to 3 times**
- Prevents dead-end user experiences

---

### 🔐 Zero-Trust Security Layer
- Regex-based SQL sanitization
- Blocks destructive commands:
  - `DROP`
  - `DELETE`
  - `UPDATE`
  - `ALTER`
- Ensures **read-only analytics access**
- LLM never directly touches the database

---

### ⚡ Dynamic CSV Indexing (High-Scale Ready)
- Optimized for **3,000+ product records**
- CSV ingested into local **SQLite engine**
- Indexed on load for **sub-millisecond queries**
- Scales cleanly for internal BI use cases

---

### 📊 Automated Visualization
- Inspects query output dynamically
- Auto-selects:
  - KPI metrics
  - Bar charts
  - Aggregation summaries
- No manual chart configuration required

---

## 🧠 System Architecture
```bash
User Question (Natural Language)
        ↓
Schema Parser (Tables + Columns)
        ↓
SQL Orchestrator (Gemini 3 Flash)
        ↓
Security Sanitizer (Zero-Trust Regex)
        ↓
Execution Engine (SQLite)
        ↓
Error Handler → Self-Healing Loop (if needed)
        ↓
Pandas DataFrame
        ↓
Automated Visualization (Streamlit)
```


### Architectural Principles
- **Schema-aware prompting**
- **LLM is generation-only**
- **Python owns validation & execution**
- **Fail-safe, not fail-fast**

---

## 🛠️ Core Components

### 🧱 Schema Parser
Extracts table metadata and column types to provide **in-context learning** for the LLM — eliminating hallucinated joins and invalid fields.

### 🧠 SQL Orchestrator
Uses **Google Gen AI SDK (v2026)** with Gemini 3 Flash to generate **raw SQLite queries only** (no markdown, no commentary).

### ⚙️ Execution Engine
- SQLite wrapper in Python
- Handles query execution
- Captures structured error logs
- Feeds errors back into the retry loop

### 🎨 UI / UX Layer
- Built with **Streamlit**
- Real-time interaction
- Auto-rendered charts & metrics
- Business-friendly experience

---

### Output
![Outcome](Animation-1.png)

## 📂 Project Structure

```bash
├── app.py                # Main Streamlit orchestrator & UI logic
├── database_utils.py     # DB engine, schema extraction & SQL sanitization
├── library_data.db       # Local SQLite instance (generated on run)
├── your_products.csv     # 3,000+ item product library
└── requirements.txt      # Project dependencies
```

Install dependencies:

```bash
pip install google-genai streamlit pandas
```
Run the application:

```bash
streamlit run app.py
```

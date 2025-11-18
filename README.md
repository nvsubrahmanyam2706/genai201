# 🛍️ GenAI 201 Capstone: Retail Insights Generator

A simple and efficient Generative AI-powered app that answers retail inventory and sales questions using natural language.

---

## 🚀 Overview

This project allows a store manager to ask questions like:
**“How many Nike white XS T‑shirts are in stock?”**

the system:

1. Converts the question → SQL using Gemini
2. Executes the SQL on MySQL
3. Returns a clear answer

---

## 🧠 Tech Stack

* **Gemini 2.5 Flash** (LLM)
* **Python**
* **MySQL**
* **Streamlit** (Frontend)
* **Few‑shot prompting**

---

## 📁 Project Files

```
main.py                → Streamlit UI
langchain_helper.py    → AI + SQL logic
few_shots.py           → Few-shot examples
global_tshirts_db.sql  → Database schema + data
.env                   → Gemini API key (not included)
```

---

## ⚙️ Setup Instructions

### 1️⃣ Install Python packages

```bash
pip install -r requirements.txt
```

### 2️⃣ Setup MySQL

```bash
mysql -u root -p --protocol=TCP
SOURCE global_tshirts_db.sql;
```

### 3️⃣ Add Gemini API key

Create `.env`:

```
GOOGLE_API_KEY=your_key_here
```

Load it:

```bash
export $(cat .env | xargs)
```

### 4️⃣ Run Streamlit

```bash
streamlit run main.py --server.address=0.0.0.0 --server.port=8501
```

---

## 💬 Sample Questions

* How many t‑shirts are in stock?
* How many Adidas small size shirts do we have?
* Total inventory value for S size?
* Revenue if we sell all Levi’s shirts today after discounts?

---

## 🎯 Key Features

* Natural language → SQL
* Real database insights
* Discount calculations
* Fast and accurate using Gemini
* Clean UI via Streamlit

---

## 🏁 Result

A complete GenAI-driven Retail Insights System ready for demo and evaluation.

---

**Developer - N.V.Subrahmanyam**

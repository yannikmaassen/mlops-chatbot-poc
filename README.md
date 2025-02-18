# MLOps Chatbot

## Project Overview

This project is a proof-of-concept for a **MLOps chatbot** that uses **Retrieval-Augmented Generation (RAG)** to answer MLOps-related questions. It retrieves relevant documentation from a **ChromaDB vector database** and generates responses using **OpenAI's GPT-4**.

---

## Features

- **Web Scraping**: Extracts MLOps documentation from online sources.
- **Text Chunking**: Splits long documents into manageable sections (~300 words).
- **Embeddings & Vector Storage**: Converts text into OpenAI embeddings and stores them in ChromaDB.
- **Retrieval & Chatbot**: Queries ChromaDB for relevant information and generates responses using GPT-4.
- **Streamlit UI**: Provides a simple web interface for users to interact with the chatbot.

---

## Setup Instructions

### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/yourusername/mlops-chatbot-poc.git
cd mlops-chatbot-poc
```

### **2️⃣ Create a Virtual Environment (Recommended)**

```bash
python -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate on macOS/Linux
venv\Scripts\activate  # Activate on Windows
```

### **3️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

---

## Environment Variables Setup

### **1️⃣ Create an `.env.local` File**

In the project root, create a `.env.local` file and add your OpenAI API key:

```ini
OPENAI_API_KEY=your-api-key-here
```

---

## 🗄️ Populate ChromaDB with Documentation

If ChromaDB is empty, run this script to populate it from existing JSON files:

```bash
python src/database.py
```

To check if documents are stored:

```bash
python src/database.py
```

Expected Output:

```python
📊 ChromaDB contains X documents.
```

---

## 💬 Running the Chatbot (Streamlit UI)

Start the chatbot with:

```bash
streamlit run src/app.py
```

This will open the chatbot UI in your browser.

---

## 🛠️ Project Structure

```text
mlops-chatbot/
│── data/                    # Storage for raw data, processed embeddings
│── models/                  # (Optional) Pre-trained models
│── src/                     # Main source code
│   ├── retriever.py         # Handles document retrieval
│   ├── embeddings.py        # Converts text into embeddings
│   ├── chatbot.py           # Chatbot logic (retrieves docs, calls OpenAI)
│   ├── database.py          # Handles ChromaDB interactions
│   ├── app.py               # Streamlit UI
│   ├── config.py            # Loads API keys from .env.local
│── notebooks/               # Jupyter/Colab experiments
│── frontend/                # (Optional) UI components (if needed)
│── requirements.txt         # Dependencies
│── README.md                # Project documentation
│── .gitignore               # Ignore large files (datasets, logs)
│── .env.local               # Stores API keys (not committed to Git)
```

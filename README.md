# 🤖 QA System with Documents (Gemini-Powered)

This Streamlit app allows you to upload a document (PDF, DOCX, or TXT) and ask questions about its content.  
It uses **Google Gemini LLM** for intelligent answers and **LlamaIndex** for efficient document indexing.

---

## 📁 Features
- Upload **PDF, DOCX, or TXT** files  
- Extract text automatically  
- Get **AI-powered answers** using Gemini 2.5 Flash  
- Works even without API key (basic keyword matching mode)  
- Shows **document statistics** and **sample questions**

---

## 🧰 Tech Stack
- **Python 3.10+**
- **Streamlit**
- **LlamaIndex**
- **Google Generative AI (Gemini)**
- **pypdf**, **python-docx**
- **dotenv** for environment management

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/qa-system.git
cd qa-system
```
### 2. Create and activate virtul environment 
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Google API Key
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

### 5. Run the App
```bash
streamlit run streamlit_app.py
```

## How to Use

Upload a document — choose a .pdf, .docx, or .txt file

Wait for the app to process and extract text

Type a question about the content

View the answer (powered by Gemini if API key is set)

Try the predefined quick questions for summary, key points, or main topic

## 🧠 Modes
Mode	Description

🧩 Gemini Mode	Requires Google API Key — provides semantic, intelligent answers

🔍 Basic Mode	Works without API key — keyword-based sentence matching

## 📊 Example Questions

“Summarize this document.”

“What are the main findings?”

“Who are the key people mentioned?”

“What is the main topic discussed?”


🧾 Example Output

Q: What is machine learning?

A: Machine learning is a method of data analysis that automates analytical model building. It is a branch of artificial intelligence based on the idea that systems can learn from data, identify patterns, and make decisions with minimal human intervention.

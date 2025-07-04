# 📄 PDF Summarizer with Google Gemini

A powerful and user-friendly PDF summarization tool built with **Streamlit** and integrated with **Google Gemini (1.5)** to generate AI-powered summaries. Upload any PDF, extract its content, and get customized summaries tailored to your needs.

---

## 🚀 Features

- 🔑 Secure Gemini API integration using `.env`
- 🧠 Choose summary **type** and **length**
- 🎯 Add **focus areas** like conclusions, methodology, recommendations, etc.
- 📄 Limit number of pages to process
- 📋 Downloadable summary output
- 📊 Clean UI with word/character metrics and preview

---

## 📁 Directory Structure

```
root/
├── agent.py      # Handles Gemini API and summarization logic
├── ui.py         # Streamlit user interface
├── main.py       # Application entry point
└── .env          # Your Gemini API key (not committed)
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/vanam-chandra-shekar/pdfagent
cd pdfagent
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # on Linux/Mac
venv\Scripts\activate     # on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in the root directory and add your Gemini API key:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```
Or can pass from UI

You can get the key from [Google AI Studio](https://aistudio.google.com/app/apikey)

---

## ▶️ Running the App

```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 🧪 Example Usage

1. Upload a `.pdf` file (max 50 pages)
2. Select summary type:
   - `general`, `executive`, `bullet_points`, `technical`, `academic`, etc.
3. Choose summary length:
   - `short`, `medium`, or `long`
4. (Optional) Select focus areas
5. View the summary, copy or download it as `.txt`

---

## 📦 Dependencies

- `streamlit`
- `PyPDF2`
- `python-dotenv`
- `google-genai`

Install manually:

```bash
pip install streamlit PyPDF2 python-dotenv google-genai
```

Or use:

```bash
pip install -r requirements.txt
```

---

## 📄 License

This project is open-source and free to use.
---

## 🙌 Credits

Developed by **Vanam Chandra Shekar**  
Guided by OpenAI's tools and Google Gemini API

---

## 🌐 Links

- [Google AI Studio](https://aistudio.google.com/app/apikey)
- [Streamlit Docs](https://docs.streamlit.io/)

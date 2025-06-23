# 🧠 Smart Resume Screener

An AI-powered resume screening tool built in Python + Streamlit. Upload resumes, match them to a job description, and get ranked scores and GPT summaries.

## 🔍 Features
- PDF & TXT resume support
- Keyword-based skill matching using TF-IDF
- GPT-powered 3-line summaries (optional with API key)
- Visual match scores with progress bars
- Matched & missing skills display
- Export results as CSV

## 📦 Tech Used
- Python
- Streamlit
- scikit-learn
- PyMuPDF
- OpenAI GPT (optional)

## ▶️ How to Run

```bash
pip install -r requirements.txt
streamlit run resumetester.py

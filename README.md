# 🧠 Smart Resume Screener

## 🔑 Using Your Own OpenAI API Key

To use this application, you need to provide your own OpenAI API key.

### How to get it:
1. Go to: https://platform.openai.com/account/api-keys
2. Sign in or sign up.
3. Click "Create new secret key"
4. Copy and paste the key into the input field when the app asks for it.

⚠️ Never share your key publicly.

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

just check out my portfolio from where you can test it live 

```bash
pip install -r requirements.txt
streamlit run resumetester.py

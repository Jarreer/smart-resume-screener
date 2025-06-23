import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import fitz  # PyMuPDF for PDF reading
import re

# Optional GPT (disabled unless API key is entered)
try:
    import openai
except ImportError:
    openai = None

# ------------------ Helper Functions ------------------

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def clean_text(text):
    return re.sub(r'\s+', ' ', text.replace('\n', ' ')).strip()

def extract_skills(text):
    keywords = ['python', 'java', 'c#', 'machine learning', 'tensorflow', 'django', 'flask', 'sql', 'react', 'html', 'css', 'pandas', 'numpy', 'git', 'api']
    text = text.lower()
    return [kw for kw in keywords if kw in text]

def generate_summary(text, openai_api_key):
    if not openai or not openai_api_key:
        return "GPT summary not available. No API key provided."
    openai.api_key = openai_api_key
    prompt = f"Summarize this resume in 3 lines:\n{text[:2000]}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"

# ------------------ Streamlit UI ------------------

st.set_page_config(page_title="Smart Resume Screener", layout="wide")
st.title("📄 Smart Resume Screener")
st.markdown("Match resumes to a job description using smart keyword analysis. Upload `.pdf` or `.txt` files.")

col1, col2 = st.columns([2, 1])
job_desc = col1.text_area("📝 Paste Job Description", height=200)
openai_api_key = col2.text_input("🔑 OpenAI API Key (optional)", type="password")

uploaded_files = st.file_uploader("📤 Upload Resumes (.pdf or .txt)", type=["pdf", "txt"], accept_multiple_files=True)

if st.button("🔍 Run Screener"):
    if not job_desc or not uploaded_files:
        st.warning("Please upload resumes and enter a job description.")
    else:
        jd_skills = extract_skills(job_desc)
        filenames, match_scores, summaries = [], [], []

        for file in uploaded_files:
            filename = file.name
            if filename.endswith(".pdf"):
                text = extract_text_from_pdf(file)
            else:
                text = file.read().decode("utf-8")
            text = clean_text(text)

            resume_skills = extract_skills(text)
            combined_texts = [job_desc, text]

            vectorizer = TfidfVectorizer(stop_words='english')
            vectors = vectorizer.fit_transform(combined_texts)
            score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

            # Boost if multiple skills matched
            match_boost = len(set(jd_skills).intersection(resume_skills)) * 0.05
            final_score = min(score + match_boost, 1.0)

            filenames.append(filename)
            match_scores.append(round(final_score * 100, 2))
            summaries.append(generate_summary(text, openai_api_key) if openai_api_key else "No summary")

        df = pd.DataFrame({
            "Resume": filenames,
            "Match Score (%)": match_scores,
            "GPT Summary": summaries
        }).sort_values(by="Match Score (%)", ascending=False).reset_index(drop=True)

        st.success("✅ Matching Complete!")
        st.dataframe(df[["Resume", "Match Score (%)"]], use_container_width=True)

        st.markdown("### 🧠 Resume Summaries")
        for i in range(len(df)):
            with st.expander(f"{df['Resume'][i]} (Score: {df['Match Score (%)'][i]}%)"):
                st.markdown(df['GPT Summary'])

---

# **2️⃣ app.py**

```python
import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import os
import openai

# -----------------------
# OpenAI Configuration
# -----------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# -----------------------
# Streamlit UI
# -----------------------
st.set_page_config(page_title="Legal Document Explainer Bot", layout="wide")
st.title("⚖️ Legal Document Explainer Bot")
st.markdown("Simplify complex legal documents into **easy-to-understand summaries**.")

# File uploader
uploaded_file = st.file_uploader("Upload legal document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

def extract_text(file):
    if file.type == "application/pdf":
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    elif file.type == "text/plain":
        return str(file.read(), "utf-8")
    else:
        return ""

def summarize_text(text):
    prompt = f"Summarize and simplify the following legal text so that a non-legal person can understand:\n\n{text}"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.3,
        max_tokens=1000
    )
    return response.choices[0].text.strip()

if uploaded_file:
    original_text = extract_text(uploaded_file)
    st.subheader("Original Text")
    st.text_area("", original_text, height=300)

    if st.button("Generate Simplified Summary"):
        with st.spinner("Generating summary..."):
            summary = summarize_text(original_text)
        st.subheader("Simplified Summary")
        st.text_area("", summary, height=300)

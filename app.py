import streamlit as st
import openai
import PyPDF2

openai.api_key = "YOUR_OPENAI_API_KEY"

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def analyze_resume(resume_text, job_desc):
    prompt = f"""
    You are an AI Resume Screener. Compare the following resume with the job description and provide:
    1. Candidate summary
    2. Key matching skills
    3. Missing skills
    4. Suitability score out of 100
    5. One-line improvement suggestion

    Resume:
    {resume_text[:3000]}

    Job Description:
    {job_desc}
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response['choices'][0]['message']['content']

st.set_page_config(page_title="AI Resume Screener", layout="wide")
st.title("🤖 AI-Powered Resume Screener")
st.write("Upload a resume and paste a job description to get AI-based evaluation.")

uploaded_file = st.file_uploader("Upload Resume (PDF or Text)", type=["pdf", "txt"])
job_desc = st.text_area("Paste Job Description", height=200)

if st.button("Analyze Resume"):
    if uploaded_file and job_desc:
        if uploaded_file.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(uploaded_file)
        else:
            resume_text = uploaded_file.read().decode("utf-8")
        with st.spinner("Analyzing with AI..."):
            analysis = analyze_resume(resume_text, job_desc)
        st.success("✅ Analysis Complete!")
        st.write(analysis)
    else:
        st.warning("Please upload a resume and enter a job description.")

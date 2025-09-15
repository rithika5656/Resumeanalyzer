import streamlit as st
import re
import PyPDF2

# ------------------------------
# Custom CSS for theme
# ------------------------------
st.markdown("""
    <style>
        /* Background gradient */
        .stApp {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: white;
        }

        /* Titles */
        h1, h2, h3, h4 {
            color: #00ffcc;
        }

        /* Buttons */
        .stButton>button {
            background-color: #00ffcc;
            color: black;
            border-radius: 10px;
            border: none;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #00cc99;
            color: white;
        }

        /* Metrics box */
        .css-1xarl3l {
            background: #1a1a1a;
            border-radius: 10px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# Predefined Skills Dictionary
# ------------------------------
SKILLS_DB = [
    "python", "java", "c++", "sql", "html", "css", "javascript",
    "machine learning", "deep learning", "artificial intelligence",
    "nlp", "data analysis", "pandas", "numpy", "tensorflow", "pytorch",
    "scikit-learn", "django", "flask", "git", "github",
    "aws", "azure", "gcp", "docker", "kubernetes", "linux",
    "problem solving", "communication", "leadership", "teamwork"
]

STOPWORDS = {"and","or","the","in","on","at","to","a","is","was","that","we","with","for","of"}

# ------------------------------
# Helper functions
# ------------------------------
def extract_keywords(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return set([w for w in words if w not in STOPWORDS])

def keyword_match(resume_text, job_desc_text):
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(job_desc_text)

    matched = resume_keywords.intersection(jd_keywords)
    missing = jd_keywords.difference(resume_keywords)

    matched_skills = [s for s in SKILLS_DB if s in matched]
    missing_skills = [s for s in SKILLS_DB if s in missing]

    match_percent = (len(matched) / len(jd_keywords)) * 100 if jd_keywords else 0
    return matched_skills, missing_skills, round(match_percent, 2)

def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def suggest_enhancements(missing_skills):
    suggestions = []
    for skill in missing_skills:
        if skill in ["python", "java", "c++"]:
            suggestions.append(f"Add a project description highlighting {skill} applications.")
        elif skill in ["tensorflow", "pytorch", "scikit-learn"]:
            suggestions.append(f"Mention ML projects where you used {skill}.")
        elif skill in ["aws", "azure", "gcp"]:
            suggestions.append(f"Add cloud deployment/experience with {skill}.")
        elif skill in ["docker", "kubernetes"]:
            suggestions.append(f"Highlight experience in containerization using {skill}.")
        elif skill in ["communication", "leadership", "teamwork"]:
            suggestions.append(f"Include soft skills like {skill} under achievements or roles.")
        else:
            suggestions.append(f"Consider mentioning experience with {skill}.")
    return suggestions

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="AI Resume Enhancer", page_icon="🤖", layout="wide")

st.title("🤖 AI-Powered Resume Keyword Matcher & Enhancer")
st.write("Upload your resume (PDF/text) and paste job description to check keyword match and get AI suggestions.")

resume_file = st.file_uploader("📂 Upload your Resume (PDF)", type=["pdf"])

resume_text = ""
if resume_file is not None:
    resume_text = read_pdf(resume_file)
    st.success("✅ PDF uploaded and text extracted!")

resume_text_manual = st.text_area("Or paste your Resume text here (optional)", height=200)

resume_text = (resume_text + " " + resume_text_manual).strip()

job_desc_text = st.text_area("📋 Paste the Job Description here", height=200)

if st.button("🚀 Check Match"):
    if resume_text.strip() == "" or job_desc_text.strip() == "":
        st.warning("⚠ Please provide Resume (PDF/Text) and Job Description.")
    else:
        matched, missing, match_percent = keyword_match(resume_text, job_desc_text)

        st.subheader("✅ Results")
        st.metric("Match Percentage", f"{match_percent}%")

        st.write("**Matched Skills:**")
        st.write(", ".join(sorted(matched)) if matched else "None")

        st.write("**Missing Skills (important for this JD):**")
        st.write(", ".join(sorted(missing)) if missing else "🎯 None – But you can still enhance!")

        if missing:
            st.subheader("💡 AI Suggestions to Enhance Resume")
            suggestions = suggest_enhancements(missing)
            for s in suggestions:
                st.write(f"- {s}")
        else:
            st.info("🌟 Your resume matches well! You may still add more projects, certifications, or tools to strengthen it further.")

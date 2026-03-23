import streamlit as st
import os
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from loader import load_documents_from_folder
from chunker import chunk_text
from embedder import create_embeddings, model
from retriever import build_faiss_index, search
from analyzer import extract_skills, compare_roles, calculate_skill_gap, generate_learning_roadmap, generate_resume_suggestions
from resume_parser import extract_text_from_resume
from hybrid_retriever import build_bm25_index, hybrid_search
from report_generator import generate_report
import ollama

# ---------------- CONFIG ----------------
st.set_page_config(page_title="CareerRAG Pro", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
.main {background-color: #0e1117;}
h1, h2, h3 {color: #ffffff;}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🚀 CareerRAG Pro")
st.sidebar.write("AI Career Intelligence System")

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Resume Analyzer", "Skill Trends", "Role Comparison", "Career Readiness", "AI Career Advisor"]
)

st.title("CareerRAG Pro - AI Career Intelligence System")

# ---------------- CACHE PIPELINE ----------------
@st.cache_resource
def load_pipeline(text):
    chunks = chunk_text(text, 500, 50)
    bm25 = build_bm25_index(chunks)
    embeddings = create_embeddings(chunks)
    index = build_faiss_index(embeddings)
    return chunks, bm25, index

# ---------------- LOAD DATA ----------------
folder_path = "data"

if not os.path.exists(folder_path):
    st.error("data folder not found")
    st.stop()

with st.spinner("Loading AI pipeline..."):
    text = load_documents_from_folder(folder_path)
    chunks, bm25, index = load_pipeline(text)

# ---------------- HOME ----------------
if page == "Home":
    st.header("Welcome to CareerRAG Pro")
    st.write("""
    AI-powered system to analyze careers, skills, and job roles.
    """)

# ---------------- RESUME ANALYZER ----------------
elif page == "Resume Analyzer":

    st.header("📄 Resume Analyzer")

    uploaded_resume = st.file_uploader("Upload Resume", type=["pdf"])

    if uploaded_resume:
        resume_text = extract_text_from_resume(uploaded_resume)
        resume_skill_counts = extract_skills(resume_text)
        resume_skills = list(resume_skill_counts.keys())

        st.write("### Skills Detected")
        for skill, count in resume_skill_counts.most_common(20):
            st.write(f"• {skill}")

        target_role = st.text_input("Target Role")

        if target_role:
            role_embedding = model.encode([target_role])[0]
            role_docs, _ = search(index, role_embedding, chunks)

            role_text = " ".join(role_docs)
            role_skills = list(extract_skills(role_text).keys())

            suggestions, tips = generate_resume_suggestions(resume_skills, role_skills)

            st.write("### Suggestions")
            for s in suggestions:
                st.write("•", s)

            st.write("### Tips")
            for t in tips:
                st.write("•", t)

# ---------------- SKILL TRENDS ----------------
elif page == "Skill Trends":

    st.header("📊 Skill Trends")

    skill_counts = extract_skills(text)
    top_skills = skill_counts.most_common(15)

    skills = [s for s, c in top_skills]
    counts = [c for s, c in top_skills]

    fig, ax = plt.subplots()
    ax.barh(skills, counts)
    st.pyplot(fig)

# ---------------- ROLE COMPARISON ----------------
elif page == "Role Comparison":

    st.header("⚔ Role Comparison")

    role1 = st.text_input("Role 1")
    role2 = st.text_input("Role 2")

    if st.button("Compare") and role1 and role2:

        r1_emb = model.encode([role1])[0]
        r2_emb = model.encode([role2])[0]

        docs1, _ = search(index, r1_emb, chunks)
        docs2, _ = search(index, r2_emb, chunks)

        skills1 = extract_skills(" ".join(docs1))
        skills2 = extract_skills(" ".join(docs2))

        comparison = compare_roles(skills1.keys(), skills2.keys())

        st.write("### Common Skills")
        for s in comparison["common_skills"]:
            st.write("•", s)

# ---------------- CAREER READINESS ----------------
elif page == "Career Readiness":

    st.header("📈 Career Readiness")

    user_skills_input = st.text_input("Your Skills")
    target_role = st.text_input("Target Role")

    if target_role and user_skills_input:

        role_embedding = model.encode([target_role])[0]
        role_docs, _ = search(index, role_embedding, chunks)

        role_skills = list(extract_skills(" ".join(role_docs)).keys())
        user_skills = [s.strip() for s in user_skills_input.split(",")]

        score, common, missing = calculate_skill_gap(user_skills, role_skills)

        st.progress(score / 100)

        st.markdown(f"""
        <div style="padding:15px;background:#1c1f26;border-radius:10px">
        <h2 style="color:#4CAF50">{score}%</h2>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.write("### ✅ Matching")
            for s in common:
                st.write("•", s)

        with col2:
            st.write("### ❌ Missing")
            for s in missing[:10]:
                st.write("•", s)

        roadmap = generate_learning_roadmap(missing)

        st.write("### 📚 Roadmap")
        for step in roadmap[:10]:
            st.write("•", step)

        report_file = generate_report(target_role, score, common, missing, roadmap)

        with open(report_file, "rb") as f:
            st.download_button("Download Report", f)

# ---------------- AI ADVISOR ----------------
elif page == "AI Career Advisor":

    st.header("🤖 AI Career Advisor")

    query = st.text_input("Ask something")
    if st.button("Ask AI") and query:

        with st.spinner("Thinking..."):

            query_embedding = model.encode([query])[0]
            results, scores = search(index, query_embedding, chunks)

            context = "\n\n".join(results)

            response = ollama.chat(
                model="gemma:2b",
                messages=[{"role": "user", "content": f"{context}\n{query}"}]
            )

            st.write(response["message"]["content"])
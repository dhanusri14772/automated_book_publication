import os
import datetime
import streamlit as st
from agents.writer_agent import spin_paragraph
from agents.reviewer_agent import ai_review_text, get_next_version
from agents.reward_system import log_feedback
from index_with_chromadb import index_final_version, semantic_search
from fpdf import FPDF
from agents.voice import speak, listen_for_yes_no, listen_for_command

CHAPTER_ID = "Chapter_1"
INPUT_PATH = f"data/{CHAPTER_ID}.txt"
VERSION_DIR = f"versions/{CHAPTER_ID}"
os.makedirs(VERSION_DIR, exist_ok=True)

st.set_page_config(page_title="📘 Book Rewriter", layout="wide")
st.title("📘 Automated Book Rewrite Workflow")


for key in [
    "rewritten", "spun_text", "feedback", "v_next",
    "search_results", "voice_activated", "voice_used",
    "semantic_done", "feedback_given"
]:
    if key not in st.session_state:
        st.session_state[key] = False if key.startswith("voice") or key.endswith("_done") or key.endswith("_given") or key == "rewritten" else ""

# Load Chapter
if not os.path.exists(INPUT_PATH):
    st.error(f"❌ File not found: {INPUT_PATH}")
    st.stop()

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    chapter_text = f.read()

st.subheader("📖 Original Chapter")
with st.expander("Click to view original"):
    st.text_area("Original Chapter", chapter_text, height=300, disabled=True)
    st.image("screenshots/chapter_1.png", caption="🖼️ Screenshot of Source Page", use_column_width=True)

# Rewrite Button 
if not st.session_state.rewritten:
    if st.button("✍️ Rewrite with AI"):
        with st.spinner("Rewriting..."):
            spun = spin_paragraph(chapter_text)
            v_next = get_next_version()
            version_path = os.path.join(VERSION_DIR, f"{v_next}.txt")
            with open(version_path, "w", encoding="utf-8") as f:
                f.write(spun)

            st.session_state.rewritten = True
            st.session_state.spun_text = spun
            st.session_state.v_next = v_next

# Show Rewritten Text 
if st.session_state.rewritten:
    st.subheader("🆕 Rewritten Version")
    st.text_area("AI Generated Rewrite", st.session_state.spun_text, height=300)

    #  AI Review 
    if not st.session_state.feedback:
        with st.spinner("🤖 AI reviewing..."):
            feedback = ai_review_text(st.session_state.spun_text)
            st.session_state.feedback = feedback

    st.subheader("🤖 AI Feedback")
    st.markdown(st.session_state.feedback)

    #  Voice Controls 
    st.markdown("---")
    st.header("🎙️ Voice Command Options")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔊 Summarize Rewrite"):
            speak("Here is a quick summary of the rewritten version.")
            speak(st.session_state.spun_text[:300])

    with col2:
        if st.button("✅ Accept with Voice"):
            speak("Do you want to accept this version?")
            response = listen_for_yes_no()
            st.session_state.voice_activated = (response == 'y')
            st.session_state.voice_used = True
            st.info(f"Voice decision: {'Accepted ✅' if response == 'y' else 'Rejected ❌'}")

    with col3:
        if st.button("🗣️ Edit / Revise via Voice"):
            speak("Say a command: accept, edit, revise, or final")
            command = listen_for_command()
            st.session_state.voice_used = True
            st.info(f"🗣️ Voice command received: {command}")

#  Semantic Search 
if st.session_state.voice_used:
    st.markdown("---")
    st.header("🔍 Semantic Search (Final Rewrite)")

    query = st.text_input("Enter your semantic query:")
    if st.button("🔎 Search") and query:
        with st.spinner("Running semantic search..."):
            results = semantic_search(query, top_k=1)
            st.session_state.search_results = results
            st.session_state.semantic_done = True

    if st.session_state.search_results:
        for result in st.session_state.search_results:
            st.markdown("---")
            st.markdown(f"📌 **Chunk #{result['chunk_id']}** (Distance: {result['distance']:.4f})")
            st.text_area("Semantic Match", result['text'], height=200, disabled=True, key=f"sem_chunk_{result['chunk_id']}")

# Step 6: Feedback 
if st.session_state.semantic_done and not st.session_state.feedback_given:
    st.markdown("---")
    st.header("📝 Feedback & Rating")

    rating = st.slider("Rate this version:", 1, 5, key="final_rating")
    comment = st.text_area("Your Comment:", key="final_comment")

    if st.button("✅ Submit Final Feedback"):
        log_feedback(
            chapter=CHAPTER_ID,
            version=st.session_state.v_next,
            accepted="yes" if rating >= 3 else "no",
            rating=rating,
        )
        index_final_version()
        st.success("📌 Feedback recorded and indexed.")
        st.session_state.feedback_given = True

#  PDF Export 
if st.session_state.feedback_given:
    st.markdown("---")
    st.subheader("📄 Export as PDF")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, st.session_state.spun_text)

    pdf_filename = os.path.join(VERSION_DIR, f"{st.session_state.v_next}.pdf")
    pdf.output(pdf_filename)

    with open(pdf_filename, "rb") as f:
        st.download_button("📥 Download PDF", f, file_name=f"{CHAPTER_ID}_{st.session_state.v_next}.pdf")

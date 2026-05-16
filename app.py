import streamlit as st
from auth import register_user, login_user
from chatbot import ask_ai
from attendance import calc_attendance
from planner import generate_plan
from database import cursor, conn
from voice import listen_voice, speak
from pdf_qa import read_pdf
from ocr import extract_text_from_image
from exam_generator import create_exam_prompt
from interview_bot import coding_prompt
from export_pdf import create_pdf
from analytics import sample_progress_data
import plotly.express as px
import os

st.set_page_config(page_title="AI Student Assistant PRO", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# AUTH PAGE
if not st.session_state.logged_in:

    st.title("🎓 AI Student Assistant PRO")

    mode = st.selectbox("Choose", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if mode == "Register":
        if st.button("Create Account"):
            if register_user(username, password):
                st.success("Registered Successfully")
            else:
                st.error("Username already exists")

    else:
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid Login")

# DASHBOARD
else:

    st.sidebar.title(f"Welcome {st.session_state.username}")

    page = st.sidebar.radio(
        "Menu",
        ["AI Chatbot", "Attendance", "Study Planner", "Chat History"]
    )

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # Chatbot
    if page == "AI Chatbot":
        st.header("💬 AI Chatbot")

        q = st.text_area("Ask anything")

        if st.button("Send"):
            ans = ask_ai(q)

            cursor.execute(
                "INSERT INTO history(username,question,answer) VALUES(?,?,?)",
                (st.session_state.username, q, ans)
            )
            conn.commit()

            st.success(ans)
    
    elif page == "PDF Notes Q&A":
    st.header("📄 Upload PDF Notes")

    uploaded = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded:
        pdf_text = read_pdf(uploaded)

        st.success("PDF Loaded Successfully")

        question = st.text_input("Ask from Notes")

        if st.button("Ask PDF"):
            prompt = f"""
            Use these notes to answer:

            Notes:
            {pdf_text}

            Question:
            {question}
            """

            answer = ask_ai(prompt)

            st.success(answer)

    elif page == "OCR Timetable":
    st.header("🖼 Upload Timetable Image")

    img = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])

    if img:
        text = extract_text_from_image(img)

        st.text_area("Extracted Text", text, height=300)

        if st.button("Summarize Timetable"):
            ans = ask_ai(f"Organize this timetable:\n{text}")
            st.success(ans)

    # Attendance
    elif page == "Attendance":
        st.header("📊 Attendance Tracker")

        attended = st.number_input("Classes Attended", 0)
        total = st.number_input("Total Classes", 1)

        if st.button("Calculate"):
            st.success(f"Attendance = {calc_attendance(attended,total)}%")

    # Planner
    elif page == "Study Planner":
        st.header("📚 Study Planner")

        hrs = st.slider("Study Hours", 1, 12)

        if st.button("Generate Plan"):
            for item in generate_plan(hrs):
                st.write("✅", item)

    elif page == "Voice Chat":
    st.header("🎤 Voice Chatbot")

    if st.button("Start Listening"):
        text = listen_voice()

        st.write("You Said:", text)

        if text:
            reply = ask_ai(text)

            st.success(reply)
            speak(reply)

    # History
    else:
        st.header("🕘 Chat History")

        cursor.execute(
            "SELECT question,answer FROM history WHERE username=?",
            (st.session_state.username,)
        )

        rows = cursor.fetchall()

        for q,a in rows[::-1]:
            st.write("### You:", q)
            st.write("Bot:", a)
            st.markdown("---")

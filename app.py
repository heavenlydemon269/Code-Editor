# app.py
import streamlit as st
import requests
import time
from ai_manager import AIManager   # <-- make sure ai_manager.py is in same folder

# ----------------------------
# CONFIG
# ----------------------------
JUDGE0_URL = "https://judge0-ce.p.rapidapi.com/submissions"
RAPIDAPI_KEY = "YOUR_API_KEY"  # Replace with your Judge0 key
HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "judge0-ce.p.rapidapi.com",
    "content-type": "application/json"
}

# ----------------------------
# STREAMLIT UI
# ----------------------------
st.title("AI Project Simulation")
st.write("👨‍💻 User writes code below. 🤖 AI Manager checks progress.")

default_code = """# Example Project: Build a Calculator
def add(a, b):
    return a + b

print(add(2, 3))
"""

code = st.text_area("Write your Python code:", value=default_code, height=300)

# ----------------------------
# AI MANAGER CHECK
# ----------------------------
if st.button("Check Progress"):
    manager = AIManager(project="calculator")  # ✅ Now manager is defined
    feedback = manager.analyze_code(code)
    st.subheader("AI Manager Feedback:")
    st.text(feedback)

# ----------------------------
# RUN CODE WITH JUDGE0
# ----------------------------
if st.button("Run Code"):
    payload = {
        "language_id": 71,  # Python 3
        "source_code": code,
        "stdin": ""
    }
    res = requests.post(JUDGE0_URL, headers=HEADERS, json=payload).json()
    token = res.get("token")

    # Poll for result
    result = None
    while result is None or result.get("status", {}).get("description") in ["In Queue", "Processing"]:
        time.sleep(1)
        result = requests.get(f"{JUDGE0_URL}/{token}", headers=HEADERS).json()

    st.subheader("Execution Output:")
    st.code(result.get("stdout") or result.get("stderr") or "No output", language="text")

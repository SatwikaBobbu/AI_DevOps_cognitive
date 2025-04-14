import streamlit as st

st.set_page_config(page_title="Cognitive DevOps Dashboard", layout="centered")
st.title("🧠 AI-Augmented DevOps Dashboard")

try:
    with open("log.txt", "r") as log:
        logs = log.readlines()
except FileNotFoundError:
    logs = []

if logs:
    st.subheader("📜 Event Logs")
    for line in reversed(logs[-50:]):
        if "stress" in line:
            st.error(line.strip())
        elif "fatigue" in line:
            st.warning(line.strip())
        else:
            st.success(line.strip())
else:
    st.info("No logs yet. Start the AI system to see events.")

try:
    with open("pause.flag", "r"):
        st.error("🚨 Deployment Paused: Stress or fatigue detected!")
except FileNotFoundError:
    st.success("✅ System Normal: No cognitive issues detected.")

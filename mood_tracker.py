import streamlit as st #type: ignore
import pandas as pd #type: ignore
import matplotlib.pyplot as plt #type: ignore
from datetime import datetime

def load_data():
    try:
        return pd.read_csv("mood_data.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Mood", "Notes"])

def save_data(data):
    data.to_csv("mood_data.csv", index=False)

st.markdown(
    """
    <style>
    body {
        background-color: #ffe6f2;
    }
    .stApp {
        background-color: #ffe6f2;
    }
    h1, h2 {
        color: #ff66b2;
        text-align: center;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    .stButton>button {
        background-color: #ff99cc;
        color: white;
        border-radius: 10px;
        font-size: 18px;
        border: none;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #ff66b2;
    }
    .stSelectbox, .stTextArea {
        background-color: #fff0f5;
        color: #ff66b2;
        border-radius: 10px;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💖 Mood Tracker 💖")
st.subheader("✨ Keep track of your emotions beautifully ✨")

mood_options = ["😊 Happy", "😢 Sad", "😡 Angry", "😰 Anxious", "🥳 Excited", "😐 Neutral"]
mood = st.selectbox("🌸 How are you feeling today?", mood_options)
notes = st.text_area("💭 Write your thoughts...")

if st.button("💾 Save Mood"):
    data = load_data()
    new_entry = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), mood, notes]], columns=["Date", "Mood", "Notes"])
    data = pd.concat([data, new_entry], ignore_index=True)
    save_data(data)
    st.success("🎀 Mood saved successfully! 🎀")
    st.rerun()

st.subheader("📖 Mood History")
data = load_data()

if not data.empty:
    delete_index = st.selectbox("🗑️ Select an entry to delete:", data.index)
    if st.button("❌ Delete Entry"):
        data = data.drop(delete_index).reset_index(drop=True)
        save_data(data)
        st.success("🚀 Entry deleted successfully!")
        st.rerun()

st.write(data)

st.subheader("📊 Mood Distribution")

if not data.empty:
    mood_counts = data["Mood"].value_counts()
    pastel_colors = ["#ff99cc", "#ffb3e6", "#ffccff", "#ff66b2", "#ffcc99", "#c2f0c2"]
    plt.figure(figsize=(6, 6))
    plt.pie(mood_counts, labels=mood_counts.index, autopct="%1.1f%%", startangle=90, colors=pastel_colors)
    plt.title("Mood Percentage 💕", fontsize=14, fontweight="bold", color="#ff66b2")
    st.pyplot(plt)
else:
    st.write("No mood data available yet. Start tracking your feelings! 💖")


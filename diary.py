import streamlit as st
import pandas as pd
import os
from datetime import datetime

def render_diary_ui():
    LOG_DIR = "diary"
    os.makedirs(LOG_DIR, exist_ok=True)
    LOG_FILE = os.path.join(LOG_DIR, "log.csv")
    today = datetime.now().strftime("%Y-%m-%d")

    st.subheader("📔 今日の日記")

    moods = {
        "😀": "ごきげん", "😊": "良い", "😐": "ふつう", "😴": "ねむい",
        "😔": "かなしい", "😡": "イライラ", "🤪": "ハイ", "🥳": "やりきった"
    }
    selected = st.radio("気分", list(moods.keys()), horizontal=True)
    text = st.text_area("日記を書く", height=200).strip()
    if st.button("💾 日記を保存する"):
        if text == "":
            text = "(記入なし)"
        new_row = pd.DataFrame({"date": [today], "mood": [selected], "entry": [text]})
        if os.path.exists(LOG_FILE):
            old = pd.read_csv(LOG_FILE)
            data = pd.concat([old, new_row], ignore_index=True)
        else:
            data = new_row
        data.to_csv(LOG_FILE, index=False)
        st.success("保存しました！")

    if os.path.exists(LOG_FILE):
        st.markdown("### 📚 最近の日記")
        df = pd.read_csv(LOG_FILE)
        df["気分"] = df["mood"] + "（" + df["mood"].map(moods) + "）"
        st.table(df.tail(5).sort_values(by="date", ascending=False)[["date", "気分", "entry"]])


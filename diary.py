import streamlit as st
from datetime import datetime
from db import init_db, insert_diary, get_recent_diaries

# 初期化
init_db()

def render_diary_ui():
    st.subheader("📔 今日の日記")

    moods = {
        "😀": "ごきげん", "😊": "良い", "😐": "ふつう", "😴": "ねむい",
        "😔": "かなしい", "😡": "イライラ", "🤪": "ハイ", "🥳": "やりきった"
    }
    selected_emoji = st.radio("気分を選んでね", list(moods.keys()), horizontal=True)
    diary_text = st.text_input("今日のひとこと日記").strip()
    today = datetime.now().strftime("%Y-%m-%d")

    if st.button("💾 日記を保存する"):
        if diary_text == "":
            diary_text = "(記入なし)"
        insert_diary(today, selected_emoji, diary_text)
        st.success("保存しました！")

    st.markdown("### 📚 最近の日記")
    recent = get_recent_diaries()
    for d, m, e in recent:
        st.markdown(f"- 🗓 **{d}** {m}：{e}")

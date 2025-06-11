import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 保存先ディレクトリとファイル
LOG_DIR = "diary"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "log.csv")

# 今日の日付（YYYY-MM-DD）
today = datetime.now().strftime("%Y-%m-%d")

# タイトル
st.title("📔 今日の日記 - Encouragify")

# 気分の選択肢（絵文字）
moods = {
    "😀": "ごきげん",
    "😊": "良い",
    "😐": "ふつう",
    "😴": "ねむい",
    "😔": "かなしい",
    "😡": "イライラ",
    "🤪": "ハイ",
    "🥳": "やりきった"
}
st.markdown("### 😊 今日の気分を選ぼう！")
selected_emoji = st.radio("気分", list(moods.keys()), horizontal=True)

# 日記入力欄
st.markdown("### ✍️ 今日の気持ちやできたことを書いてみよう")
diary_text = st.text_area("日記を書く", height=200).strip()

# 保存処理
if st.button("💾 保存する"):
    # 空欄対応
    if diary_text == "":
        diary_text = "(記入なし)"

    # 1行分のデータを作成
    new_entry = pd.DataFrame({
        "date": [today],
        "mood": [selected_emoji],
        "entry": [diary_text]
    })

    # CSVへ保存（追記）
    if os.path.exists(LOG_FILE):
        old_data = pd.read_csv(LOG_FILE)
        data = pd.concat([old_data, new_entry], ignore_index=True)
    else:
        data = new_entry

    data.to_csv(LOG_FILE, index=False)
    st.success("保存しました！")

# 最近の日記ログを表示
if os.path.exists(LOG_FILE):
    st.markdown("---")
    st.markdown("### 📚 最近の日記")
    df = pd.read_csv(LOG_FILE)

    # 気分に説明をつける
    df["気分"] = df["mood"] + "（" + df["mood"].map(moods) + "）"

    # 新しい順に5件表示
    recent = df.tail(5).sort_values(by="date", ascending=False)
    st.table(recent[["date", "気分", "entry"]])

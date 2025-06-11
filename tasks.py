import streamlit as st
import json
import os
from datetime import datetime

CONFIG_FILE = "task_config.json"

def render_task_ui():
    st.subheader("✅ 今週のやることを設定しよう")

    # すでに設定済みなら読み込み
    tasks = []
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            tasks = config.get("tasks", [])
            start_date = config.get("start_date", "")
            st.info(f"🗓 登録済み（{start_date}〜）のタスク：")
            for i, t in enumerate(tasks, 1):
                st.markdown(f"- {i}. {t}")

    # 新しい設定フォーム
    st.markdown("### ✍️ 新しいやることを設定")
    task_inputs = []
    for i in range(3):
        task = st.text_input(f"やること {i+1}", value="" if i >= len(tasks) else tasks[i])
        if task:
            task_inputs.append(task.strip())

    if st.button("💾 やることを保存"):
        if not task_inputs:
            st.warning("1つ以上入力してください。")
            return

        new_config = {
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "tasks": task_inputs
        }
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(new_config, f, ensure_ascii=False, indent=2)
        st.success("やることを保存しました！")



import streamlit as st
import json
import os
from db import init_db, get_task_config, save_task_config
from datetime import datetime
import pandas as pd

CONFIG_FILE = "task_config.json"
LOG_FILE = "task_log.csv"

# ===============================
# 📋 やることの設定UI
# ===============================

def render_task_ui():
    st.subheader("✅ 今週のやることを設定しよう")
    init_db()

    # 現在のタスクを取得（関数の最初）
    task_display_area = st.empty()
    config_data = get_task_config()
    tasks = []
    if config_data:
        start_date, *tasks = config_data
        with task_display_area.container():
            st.info(f"🗓 登録済み（{start_date}〜）のタスク：")
            for i, t in enumerate(tasks):
                if t:
                    st.markdown(f"- {i+1}. {t}")

    # 入力欄
    st.markdown("### ✍️ 新しいやることを設定")
    task_inputs = []
    for i in range(3):
        default = "" if i >= len(tasks) else tasks[i]
        task = st.text_input(f"やること {i+1}", value=default, key=f"task_input_{i}")
        if task.strip() != "":
            task_inputs.append(task.strip())

    # 保存ボタン
    if st.button("💾 やることを保存"):
        save_task_config(datetime.now().strftime("%Y-%m-%d"), task_inputs)
        st.success("やることを保存しました！")

        # 保存後に再取得して即表示
        new_data = get_task_config()
        if new_data:
            new_start, *new_tasks = new_data
            with task_display_area.container():
                st.info(f"🗓 登録済み（{new_start}〜）のタスク：")
                for i, t in enumerate(new_tasks):
                    if t:
                        st.markdown(f"- {i+1}. {t}")
                        
# def render_task_ui():
#     st.subheader("✅ 今週のやることを設定しよう")

#     # 現在のタスク読み込み
#     tasks = []
#     if os.path.exists(CONFIG_FILE):
#         with open(CONFIG_FILE, "r", encoding="utf-8") as f:
#             config = json.load(f)
#             tasks = config.get("tasks", [])
#             start_date = config.get("start_date", "")
#             st.info(f"🗓 登録済み（{start_date}〜）のタスク：")
#             for i, t in enumerate(tasks, 1):
#                 st.markdown(f"- {i}. {t}")

#     # 新しいタスク入力欄（最大3つ）
#     st.markdown("### ✍️ 新しいやることを設定")
#     task_inputs = []
#     for i in range(3):
#         default = "" if i >= len(tasks) else tasks[i]
#         task = st.text_input(f"やること {i+1}", value=default)
#         if task.strip() != "":
#             task_inputs.append(task.strip())

#     # 保存処理（空欄でもOK）
#     if st.button("💾 やることを保存"):
#         new_config = {
#             "start_date": datetime.now().strftime("%Y-%m-%d"),
#             "tasks": task_inputs  # ← 空リストも許容
#         }
#         with open(CONFIG_FILE, "w", encoding="utf-8") as f:
#             json.dump(new_config, f, ensure_ascii=False, indent=2)
#         st.success("やることを保存しました！")


# ===============================
# 📅 今日の達成チェックUI
# ===============================
def render_task_check_ui():
    st.subheader("📅 今日のやること達成チェック")

    # タスク設定が存在しない場合
    if not os.path.exists(CONFIG_FILE):
        st.info("まだやることが設定されていません。上で登録してみましょう。")
        return

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)

    tasks = config.get("tasks", [])
    today = datetime.now().strftime("%Y-%m-%d")
    st.write(f"🗓 今日：{today}")

    # タスクが空のときも正常終了
    if not tasks:
        st.info("やることは登録されていません。今日はチェックなしでOKです。")
        return

    # チェック入力
    checked = []
    for i, task in enumerate(tasks):
        done = st.checkbox(f"{i+1}. {task}")
        checked.append(done)

    # 保存処理
    if st.button("✅ 今日の記録を保存"):
        record = {"date": today}
        for i, task in enumerate(tasks):
            record[f"task_{i+1}"] = 1 if checked[i] else 0

        if os.path.exists(LOG_FILE):
            df = pd.read_csv(LOG_FILE)
            df = df[df["date"] != today]  # 上書き対応
            df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
        else:
            df = pd.DataFrame([record])

        df.to_csv(LOG_FILE, index=False)
        st.success("今日のやることを記録しました！")

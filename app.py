import streamlit as st
from diary import render_diary_ui
from tasks import render_task_ui

st.title("🌞 Encouragify")

# ここに各セクションを順に呼び出す
render_diary_ui()
render_task_ui()



import streamlit as st
import requests
import json
import os
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="Intellytics AI 대화 서비스", layout="wide")

# 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "trigger_rerun" not in st.session_state:
    st.session_state.trigger_rerun = False

# --- 사이드바 ---
with st.sidebar:
    st.header("서비스 가이드")
    st.markdown("이 서비스를 통해 다양한 질문을 할 수 있습니다.\n\n질문을 입력하거나 대표 질문을 선택하여 시작하세요.")
    st.selectbox("언어 선택", options=["English", "Korean"])
    if st.button("대화 초기화"):
        st.session_state.chat_history = []

# --- 제목 영역 ---
st.markdown("<h2 style='text-align: center; color: #A50034;'>Intellytics AI 대화 서비스</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>AI와 대화하며 다양한 질문에 대한 답변을 받아보세요.</p>", unsafe_allow_html=True)

# --- 대표 질문 버튼 ---
sample_questions = [
    "이 서비스는 어떤 기능을 제공하나요?",
    "NPS 분석이란 무엇인가요?",
    "VOC 데이터를 어떻게 분석할 수 있나요?",
    "D2C 분석에 대해 설명해주세요."
]


st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
cols = st.columns(len(sample_questions))
for i, q in enumerate(sample_questions):
    if cols[i].button(q):
        st.session_state.chat_history.append(("사용자", q, "user"))
        st.session_state.chat_history.append(("Intellytics AI", "오류가 발생했습니다. 나중에 다시 시도해주세요.", "bot"))
        st.session_state.trigger_rerun = True  # rerun 트리거 설정
st.markdown("</div>", unsafe_allow_html=True)

# --- 스타일 정의 ---
st.markdown("""
<style>
.chat-container {
    width: 100%;
    padding: 10px 20px;
    margin-bottom: 130px; /* 하단 입력창 공간 확보 */
}
.chat-row {
    display: flex;
    margin: 10px 0;
}
.chat-row.user {
    justify-content: flex-start;
}
.chat-row.bot {
    justify-content: flex-start;
}
.bubble {
    padding: 16px 20px;
    border-radius: 12px;
    width: 100%;
    font-size: 15px;
}
.user .bubble {
    background-color: #f4f4f4;
    color: #000;
}
.bot .bubble {
    background-color: #fff2f2;
    color: #a94442;
    border: 1px solid #f5c6cb;
}
.icon {
    font-size: 20px;
    margin-right: 10px;
    margin-top: 4px;
}
.input-fixed {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: white;
    padding: 12px 24px;
    box-shadow: 0 -2px 8px rgba(0,0,0,0.05);
    z-index: 9999;
}
</style>
""", unsafe_allow_html=True)

# --- 채팅 출력 영역 ---
chat_placeholder = st.empty()
with chat_placeholder.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for speaker, message, role in st.session_state.chat_history:
        icon = "👤" if role == "user" else "🤖"
        role_class = "user" if role == "user" else "bot"
        st.markdown(f"""
            <div class="chat-row {role_class}">
                <div class="icon">{icon}</div>
                <div class="bubble">{message}</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 입력 처리 함수 ---
def handle_input():
    user_input = st.session_state.user_input.strip()
    if user_input:
        st.session_state.chat_history.append(("사용자", user_input, "user"))
        st.session_state.chat_history.append(("Intellytics AI", "오류가 발생했습니다. 나중에 다시 시도해주세요.", "bot"))
        st.session_state.user_input = ""
        st.session_state.trigger_rerun = True  # rerun 예약

# --- 고정 입력창 영역 ---
st.markdown('<div class="input-fixed">', unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    st.text_input("", key="user_input", placeholder="질문을 입력하세요…")
    st.form_submit_button("전송", on_click=handle_input)
st.markdown('</div>', unsafe_allow_html=True)

# --- rerun 조건부 실행 (콜백 외부에서!)
if st.session_state.trigger_rerun:
    st.session_state.trigger_rerun = False
    st.rerun()
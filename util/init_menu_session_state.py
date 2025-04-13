import streamlit as st

def initialize_menu_session_state():
    """세션 상태를 초기화합니다."""
    # D2C 확장 여부 저장
    if "d2c_expanded" not in st.session_state:
        st.session_state.d2c_expanded = False
    # Survey Genius 확장 여부 저장
    if "survey_expanded" not in st.session_state:
        st.session_state.survey_expanded = False
    # mellerisearch 확장 여부 저장
    if "mellerisearch_expanded" not in st.session_state:
        st.session_state.mellerisearch_expanded = False
    # hrdx 확장 여부 저장
    if "hrdx_expanded" not in st.session_state:
        st.session_state.hrdx_expanded = False 
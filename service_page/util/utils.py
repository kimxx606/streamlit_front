# utils.py
import streamlit as st

def initialize_expansion_states():
    """세션 상태에 expansion 변수들이 없으면 초기화"""
    if 'd2c_expanded' not in st.session_state:
        st.session_state.d2c_expanded = False
    if 'survey_expanded' not in st.session_state:
        st.session_state.survey_expanded = False
    if 'mellerisearch_expanded' not in st.session_state:
        st.session_state.mellerisearch_expanded = False
    if 'hrdx_expanded' not in st.session_state:
        st.session_state.hrdx_expanded = False

def set_expanded_state(service_name):
    """특정 서비스만 expanded=True로 설정하고 나머지는 False로 설정
    
    Args:
        service_name: 확장할 서비스 이름 ('d2c', 'survey', 'mellerisearch', 'hrdx')
    """
    # 현재 상태 확인
    current_state = getattr(st.session_state, f"{service_name}_expanded", False)
    
    # 이미 확장된 상태면 다시 확장할 필요 없음
    if current_state:
        return False
    
    # 모든 서비스 상태를 False로 초기화
    st.session_state.d2c_expanded = False
    st.session_state.survey_expanded = False
    st.session_state.mellerisearch_expanded = False
    st.session_state.hrdx_expanded = False
    
    # 요청된 서비스만 True로 설정
    setattr(st.session_state, f"{service_name}_expanded", True)
    
    # 상태가 변경되었으므로 rerun 필요
    return True
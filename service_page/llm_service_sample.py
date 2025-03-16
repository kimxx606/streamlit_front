import streamlit as st
import requests
import json
import os

# 서비스 기본 정보
SERVICE_NAME = "LLM 서비스 샘플"
SERVICE_DESCRIPTION = """
이 서비스는 쿠버네티스에 배포된 LLM API를 사용합니다.
기본 설정은 포트 포워딩(kubectl port-forward service/llm-api 8081:80)을 사용합니다.
"""

# 기본 API 엔드포인트
DEFAULT_API_ENDPOINT = "http://localhost:8081/ask"

# 세션 상태 초기화
if 'messages' not in st.session_state:
    st.session_state.messages = []

# 사이드바 구성
with st.sidebar:
    st.title(SERVICE_NAME)
    
    api_endpoint = st.text_input("API 엔드포인트", value=DEFAULT_API_ENDPOINT)
    
    if st.button("채팅 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    st.info("""
    이 애플리케이션은 쿠버네티스에 배포된 LLM API를 사용합니다.
    
    기본 설정은 포트 포워딩(kubectl port-forward service/llm-api 8081:80)을 사용합니다.
    """)

# 함수: API 호출
def ask_llm_api(query, endpoint):
    try:
        response = requests.post(
            endpoint,
            json={"query": query},
            headers={"Content-Type": "application/json"},
            timeout=30  # 30초 타임아웃 설정
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "query": query, 
                "result": f"오류가 발생했습니다: {response.status_code}", 
                "error": response.text
            }
    except Exception as e:
        return {"query": query, "result": f"요청 오류: {str(e)}"}

# 메인 화면
st.markdown(f"<div class='main-title'>{SERVICE_NAME}</div>", unsafe_allow_html=True)

# 서비스 설명
st.markdown(f"<div class='service-description'>{SERVICE_DESCRIPTION}</div>", unsafe_allow_html=True)

# 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("Intellytics VOC를 분석해 보겠습니다. 무엇이든 물어보세요..."):
    # 사용자 입력 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 세션에 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # API 호출 (with spinner)
    with st.spinner("Processing..."):
        result = ask_llm_api(prompt, api_endpoint)
    
    # 응답 처리
    if "error" in result and result["error"]:
        response = f"오류가 발생했습니다: {result['error']}"
    else:
        response = result["result"]
    
    # 응답 표시
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # 세션에 응답 메시지 추가
    st.session_state.messages.append({"role": "assistant", "content": response})

# 초기 메시지
if not st.session_state.messages:
    with st.chat_message("assistant"):
        welcome_message = "Intellytics VOC에 대해 무엇이든 물어보세요!"
        st.markdown(welcome_message)
        st.session_state.messages.append({"role": "assistant", "content": welcome_message})

# 페이지 끝
st.markdown("---")
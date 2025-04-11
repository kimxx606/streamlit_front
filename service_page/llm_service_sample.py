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

# 사이드바 너비 설정
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        min-width: 350px !important;
        max-width: 350px !important;
        transition: none !important;
        width: 350px !important;
    }
</style>
<script>
    // 페이지 로드 시 즉시 사이드바 너비 설정
    (function() {
        function setSidebarWidth() {
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {
                sidebar.style.minWidth = '350px';
                sidebar.style.maxWidth = '350px';
                sidebar.style.width = '350px';
                sidebar.style.transition = 'none';
            }
        }
        
        // 즉시 실행
        setSidebarWidth();
        
        // DOM 로드 후 실행
        document.addEventListener('DOMContentLoaded', setSidebarWidth);
        
        // 약간의 지연 후 다시 실행 (Streamlit이 DOM을 조작한 후)
        setTimeout(setSidebarWidth, 100);
        setTimeout(setSidebarWidth, 300);
    })();
</script>
""", unsafe_allow_html=True)

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
if prompt := st.chat_input("어떤 이야기를 듣고 싶으신가요?"):
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
        welcome_message = "재밌는 이야기를 들려드립니다. 무엇이든 물어보세요."
        st.markdown(welcome_message)
        st.session_state.messages.append({"role": "assistant", "content": welcome_message})
# 자바스크립트를 추가하여 Enter 키로 전송 기능 구현
st.markdown(f"""
<style>
   
    /* 메인 타이틀 스타일 */
    .main-title {{
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #A50034; /* LG 로고 색상으로 메인 제목 변경 */
        text-align: center;
    }}
    
    /* 서비스 설명 스타일 */
    .service-description {{
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #A50034;
        font-size: 1rem;
        line-height: 1.5;
    }}
    
    /* Streamlit 기본 컨테이너 너비 조정 */
    .block-container {{
        max-width: 800px !important;
        padding-left: 20px !important;
        padding-right: 20px !important;
    }}
    
    /* 사이드바 너비 조정 */
    [data-testid="stSidebar"] {{
        min-width: 350px !important;
        max-width: 350px !important;
    }}
    
    /* 사이드바 내부 여백 조정 */
    [data-testid="stSidebar"] .block-container {{
        padding: 2rem 1rem !important;
    }}
    
    /* 사이드바 내부 텍스트 스타일 */
    [data-testid="stSidebar"] h1 {{
        font-size: 1.5rem !important;
        margin-bottom: 1.5rem !important;
    }}
    
    [data-testid="stSidebar"] .stMarkdown {{
        font-size: 0.95rem !important;
    }}
    
    /* 메인 콘텐츠 영역 조정 */
    .main {{
        padding-bottom: 70px !important; /* 입력창 높이만큼 여백 추가 */
        margin-left: auto !important;
        margin-right: auto !important;
        overflow-y: auto !important;
        height: calc(100vh - 80px) !important;
        position: relative !important;
        display: flex !important;
        flex-direction: column !important;
    }}
    
    .sample-questions-description {{
        font-size: 0.9rem;
        color: #666666;
        margin-bottom: 0.3rem;
    }}
    
    .sample-questions-container {{
        display: flex;
        flex-direction: column;
        gap: 5px;
        margin-bottom: 1.5rem;
    }}
    
    /* 언어 선택기 스타일 */
    .language-selector {{
        margin-top: 1rem;
        margin-bottom: 2rem;
    }}
    
    /* 페이지 하단 요소 숨기기 */
    footer {{
        display: none !important;
    }}
    
    /* Streamlit 기본 하단 요소 숨기기 */
    .reportview-container .main footer {{
        display: none !important;
    }}
    
    /* 하단 여백 제거 */
    .block-container {{
        padding-bottom: 0 !important;
        margin-bottom: 0 !important;
    }}
</style>
""", unsafe_allow_html=True)
# 페이지 끝
st.markdown("---")
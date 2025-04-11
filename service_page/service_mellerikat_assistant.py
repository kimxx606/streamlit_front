import streamlit as st
import requests
import json
import os
import streamlit.components.v1 as components

# 외부 CSS 파일 불러오기
def load_css():
    with open("style/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# CSS 로드 함수 호출
load_css()

# d2c, survey genius, mellerisearch expansion 기능
if (st.session_state.d2c_expanded == True) or (st.session_state.mellerisearch_expanded == True) or (st.session_state.survey_expanded == True) or (st.session_state.hrdx_expanded == True):
    st.session_state.d2c_expanded = False
    st.session_state.survey_expanded = False
    st.session_state.mellerisearch_expanded = False
    st.session_state.hrdx_expanded = False
    st.rerun()

# =======================================================================
# 서비스 페이지 개발 가이드
# =======================================================================
# 이 템플릿을 사용하여 새로운 서비스 페이지를 개발할 수 있습니다.
# 자세한 가이드는 service_page/README.md 파일을 참고하세요.
# 
# 주요 커스터마이징 영역:
# 1. 서비스 ID 및 기본 정보 설정 (SERVICE_ID, SERVICE_NAME 등)
# 2. API 통신 함수 수정 (ask_llm_api)
# 3. UI 요소 추가 또는 수정
# 4. 스타일 커스터마이징
# =======================================================================

# ======= 서비스별 커스터마이징 영역 I =======
# 서비스 ID (세션 상태 키 접두사로 사용)
SERVICE_ID = "melleri-assistant"
# ========================================


# ======= 서비스별 커스터마이징 영역 II =======
# 이 부분을 수정하여 다양한 서비스에 화면을 구성합니다.

# ==== MAIN 채팅 화면 정보 ====
# 서비스 기본 정보
SERVICE_NAME = "Mellerikat Assistant 서비스"
SERVICE_DESCRIPTION = """
이 서비스는 mellerikat을 쉽게 이해하고 사용할 수 있도록 지원하며, AI 솔루션 개발을 위한 메뉴얼을 간편하게 제공합니다.<br>
MelleriAssistant는 Intellytics AI Agnet Tool에서 제공하는 Chatbot Generation을 통해서 만들어졌습니다. 나만의 AI 챗봇을 만들고 싶으신 분들은 <a href="https://ai-agent-demo.mkdev-kic.intellytics.lge.com/service_chatbot_generation">여기</a>를 확인하세요!
"""

# SERVICE_DESCRIPTION = """
# 이 서비스는 mellerikat을 이해하고 쉽게 사용할 수 있도록 도와드리며,
# AI 솔루션 개발을 위한 메뉴얼을 간편하게 찾아볼 수 있는 서비스를 제공합니다.<br>
# 본 서비스는 "문서 기반 질의응답 AI 챗봇 시스템 개발"을 기반으로 만들어진 서비스이며,<br>
# mellerikat 메뉴얼 문서가 아닌 본인의 문서로 챗봇 시스템을 만들고 싶다면 <a href="http://mod.lge.com/hub/prism/mellerikat-assistant/-/tree/melleri-assistant/">여기 링크</a>를 참고하세요.
# """

# 대표 질문 리스트
SAMPLE_QUESTIONS = [
    "Mellerikat은 어떤 컴포넌트로 구성되어있나요?",
    "Mellerikat에서 ALO는 어떤 역할을 하나요?",
    "AI Conductor와 Edge Conductor의 역할은 무엇인가요?",
    "AI Contents에는 어떤 종류들이 있나요?",
    "Mellerikat은 어떻게 사용해볼 수 있나요?"
]

# # API 엔드포인트 형식 (중요: 서비스별 SERVICE_ID를 적용하여 엔드포인트에 연결합니다.)
# 실제 운영에서는 아래와 같이 endpoint의 전체 url로 수정해주셔야 합니다.
# 마지막에 API를 구분하는 path는 LLO화 하실 때 확인하실 수 있을 겁니다.
# api_endpoint = "http://" + SERVICE_ID + "." + os.getenv("ROOT_DOMAIN") + "/api/ask_chat"
api_endpoint = "https://melleri-assistant.mkdev-kic.intellytics.lge.com/api/ask_chat"

# # # 테스트를 위한 API 엔드포인트 (테스트용입니다.)
# api_endpoint = os.environ.get("API 엔드포인트", "http://localhost:1444/api/ask_chat")
# api_endpoint = os.environ.get("API 엔드포인트", "http://localhost:8081/ask")
# api_endpoint = st.text_input("API 엔드포인트", value="http://localhost:8081/ask")

# ==== Sidebar 화면 정보 ====
# SIDEBAR_INFO = "### 서비스 안내"
# HTML 문법 가능
SIDEBAR_SEARCHING_GUIDE = """
Mellerikat Assistant는 AI 솔루션 개발 플랫폼 Mellerikat에 대한 질문에 답변합니다.<br>
**구체적인 질문을 통해 Mellerikat의 기능과 사용법에 대한 상세한 안내를 받을 수 있습니다**
"""
# ========================================

# 세션 상태 초기화 (서비스별 고유 키 사용)
if f'{SERVICE_ID}_messages' not in st.session_state:
    st.session_state[f'{SERVICE_ID}_messages'] = []

if f"{SERVICE_ID}_language" not in st.session_state:
    st.session_state[f"{SERVICE_ID}_language"] = "ko"  # 기본 언어는 한국어

if f"{SERVICE_ID}_selected_question" not in st.session_state:
    st.session_state[f"{SERVICE_ID}_selected_question"] = ""

if f"{SERVICE_ID}_user_input" not in st.session_state:
    st.session_state[f"{SERVICE_ID}_user_input"] = ""

if f"{SERVICE_ID}_question_selected" not in st.session_state:
    st.session_state[f"{SERVICE_ID}_question_selected"] = False

if f"{SERVICE_ID}_clear_input" not in st.session_state:
    st.session_state[f"{SERVICE_ID}_clear_input"] = False
    
if f"{SERVICE_ID}_text_input_key_counter" not in st.session_state:
    st.session_state[f"{SERVICE_ID}_text_input_key_counter"] = 0


# ======= API 통신 함수 =======
# API 통신 함수는 서비스별로 필요한 파라미터를 추가하거나 수정할 수 있습니다.
# README.md 파일의 'API 통신' 섹션을 참고하여 커스터마이징하세요.
#
# 파라미터:
# - endpoint: API 엔드포인트 URL
# - query: 사용자 질의 텍스트
# - language: 응답 언어 설정 (기본값: "ko")
#
# 추가 파라미터가 필요한 경우:
# - 서비스 유형별 파라미터 (예: service_type, model_name 등)
# - 데이터 처리 옵션 (예: include_chart=True)
# 
# 응답 형식:
# - success: 성공 여부 (True/False)
# - data: API 응답 데이터 (성공 시)
# - error: 오류 메시지 (실패 시)
def ask_llm_api(endpoint, query, language="ko"):
    try:
        
        # API 엔드포인트 URL 구성 (쿼리 파라미터 사용)
        api_url = f"{endpoint}?question={requests.utils.quote(query)}"
        # print(f"요청 URL: {api_url}")  # 디버깅용
        
        # API 호출 (Body가 아닌 URL 파라미터로 전송)
        response = requests.post(
            api_url,
            headers={"accept": "application/json"},
            timeout=30  # 30초 타임아웃 설정
        )        
        # print(f"응답 상태 코드: {response.status_code}")  # 디버깅용
        
        # API 요청 데이터 준비
        # payload = {
        #     "query": query,
        #     "language": language
        # }
        
        # # API 호출
        # response = requests.post(
        #     endpoint,
        #     json=payload,
        #     headers={"Content-Type": "application/json"},
        #     timeout=30  # 30초 타임아웃 설정
        # )
        
        if response.status_code == 200:
            # 전체 응답 확인
            data = response.json()
            # print(f"API 응답: {data}")  # 디버깅용
            
            # 응답에서 직접 "answer" 필드 추출
            answer = data.get("answer", "응답에 answer 필드가 없습니다.")
            sources = data.get("sources", [])
            
            # 응답 구성
            return {
                "success": True,
                "data": {
                    "result": answer,
                    "sources": sources
                }
            }
            # return {"success": True, "data": response.json()}
        else:
            return {
                "success": False, 
                "error": f"API 오류: {response.status_code}", 
                "details": response.text
            }
            
    except requests.exceptions.Timeout:
        return {"success": False, "error": "API 요청 시간이 초과되었습니다. 나중에 다시 시도해주세요."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "API 서버에 연결할 수 없습니다. 네트워크 연결을 확인해주세요."}
    except Exception as e:
        return {"success": False, "error": f"오류가 발생했습니다: {str(e)}"}


# ======= 화면 구성 시작 =======

# 사이드바 구성
with st.sidebar:
    st.title(SERVICE_NAME)
    
    # st.markdown(SIDEBAR_INFO)
    st.markdown(SIDEBAR_SEARCHING_GUIDE, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 언어 선택 라디오 버튼
    st.markdown("<div class='language-selector'>", unsafe_allow_html=True)
    selected_language = st.radio(
        "언어 선택:", 
        options=["한국어", "English"],
        index=0 if st.session_state.get(f"{SERVICE_ID}_language", "ko") == "ko" else 1,
        key=f"{SERVICE_ID}_language_radio",
        horizontal=True,
        on_change=lambda: st.session_state.update({f"{SERVICE_ID}_language": "ko" if st.session_state[f"{SERVICE_ID}_language_radio"] == "한국어" else "en"})
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 언어 상태 자동 업데이트
    st.session_state[f"{SERVICE_ID}_language"] = "ko" if selected_language == "한국어" else "en"
    
    # 채팅 초기화 버튼
    if st.button("대화 초기화", use_container_width=True, key=f"{SERVICE_ID}_reset_btn"):
        st.session_state[f'{SERVICE_ID}_messages'] = []
        st.session_state[f"{SERVICE_ID}_user_input"] = ""
        st.session_state[f"{SERVICE_ID}_selected_question"] = ""
        st.session_state[f"{SERVICE_ID}_question_selected"] = False
        st.session_state[f"{SERVICE_ID}_clear_input"] = False
        st.session_state[f"{SERVICE_ID}_text_input_key_counter"] = 0
        st.rerun()
    
    st.divider()
    
    st.info("""
    이 애플리케이션은 Intellytics에 배포된 LLM API를 사용합니다.
    """)
    
    # 사이드바 하단에 저작권 정보 표시
    st.markdown("---")
    st.markdown("© 2025 Mellerikat Assistant | 버전 1.0")

# 1. 메인 화면 및 서비스 설명
st.markdown(f"<div class='main-title'>{SERVICE_NAME}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='service-description'>{SERVICE_DESCRIPTION}</div>", unsafe_allow_html=True)

# 2. 대표 질문 섹션
st.markdown("<h3 class='sample-questions-title'>대표 질문</h3>", unsafe_allow_html=True)
st.markdown("<p class='sample-questions-description'>이 서비스의 예시 질문 목록입니다. 궁금한 질문을 클릭하면 바로 실행되니 편하게 활용해 보세요!</p>", unsafe_allow_html=True)

# 3. 대표 질문 버튼 컨테이너 및 버튼
st.markdown("<div class='sample-questions-container'>", unsafe_allow_html=True)
for i, question in enumerate(SAMPLE_QUESTIONS):
    if st.button(question, key=f"{SERVICE_ID}_q_btn_{i}", use_container_width=True):
        st.session_state[f"{SERVICE_ID}_user_input"] = question
        st.session_state[f"{SERVICE_ID}_question_selected"] = True
        st.session_state[f"{SERVICE_ID}_selected_question"] = question  # 선택된 질문 저장
        st.rerun()  # 여기서는 rerun으로 페이지를 새로고침하고 아래의 코드에서 질문 처리
st.markdown("</div>", unsafe_allow_html=True)

# 4. 채팅 컨테이너 생성 - 여기서 정의만 하고 내용은 아래에서 채움
chat_container = st.container()
spinner_container = st.empty()

# 사용자 질문 처리 및 API 호출 함수 정의
def process_user_query(query):
    # 사용자 입력 표시
    with chat_container.chat_message("user"):
        st.markdown(query)
    
    # 세션에 사용자 메시지 추가
    st.session_state[f'{SERVICE_ID}_messages'].append({"role": "user", "content": query})
    
    # API 호출 (with spinner) - 스피너를 채팅 메시지와 입력창 사이에 표시
    with spinner_container, st.spinner("답변을 생성 중입니다..."):
        result = ask_llm_api(endpoint=api_endpoint, query=query, language=st.session_state[f"{SERVICE_ID}_language"])

    # 응답 처리
    if not result.get("success", False):
        response = f"오류가 발생했습니다: {result.get('error', '알 수 없는 오류')}"
    else:
        answer = result.get("data", {}).get("result", "응답을 받지 못했습니다.")
        sources = result.get("data", {}).get("sources", [])
        
        # 응답 텍스트 구성
        response = answer
        
        # 소스 정보가 있다면 추가
        if sources:
            response += "\n\n**출처:**\n"
            for source in sources:
                response += f"- {source}\n"
        
        
        # response = result.get("data", {}).get("result", "응답을 받지 못했습니다.")
    
    # 응답 표시
    with chat_container.chat_message("assistant"):
        st.markdown(response)
    
    # 세션에 응답 메시지 추가
    st.session_state[f'{SERVICE_ID}_messages'].append({"role": "assistant", "content": response})
    
    # 자동 스크롤 컴포넌트 추가 (응답 후)
    components.html(
        """
        <script>
        function findChatContainer() {
            // 여러 가능한 선택자를 시도
            const selectors = [
                '.stChatMessageContainer',
                '[data-testid="stChatMessageContainer"]',
                '.element-container:has(.stChatMessage)',
                '#chat-container-marker',
                '.main .block-container'
            ];
            
            for (const selector of selectors) {
                const element = document.querySelector(selector);
                if (element) {
                    // 스크롤 가능한 부모 요소 찾기
                    let parent = element;
                    while (parent && getComputedStyle(parent).overflowY !== 'auto' && parent !== document.body) {
                        parent = parent.parentElement;
                    }
                    return parent || element;
                }
            }
            
            // 최후의 수단: 메인 컨테이너 반환
            return document.querySelector('.main') || document.body;
        }
        
        function scrollToBottom() {
            const chatContainer = findChatContainer();
            if (chatContainer) {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        }
        
        // 즉시 스크롤 실행
        scrollToBottom();
        
        // 여러 시점에 스크롤 실행
        setTimeout(scrollToBottom, 100);
        setTimeout(scrollToBottom, 300);
        setTimeout(scrollToBottom, 500);
        setTimeout(scrollToBottom, 1000);
        </script>
        """,
        height=0,
        width=0,
    )

# 5. 메시지 표시 영역 - 이제 아래쪽에 위치
with chat_container:
    # 채팅 컨테이너에 ID 추가
    st.markdown("""
    <style>
    /* 채팅 컨테이너에 ID 추가 */
    .stChatMessageContainer {
        max-height: calc(100vh - 250px) !important;
        overflow-y: auto !important;
        width: 800px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding-bottom: 20px !important;
    }
    
    /* 채팅 메시지 스타일 */
    .stChatMessage {
        margin-bottom: 10px !important;
    }
    </style>
    <div id="chat-container-marker"></div>
    """, unsafe_allow_html=True)
    
    # 메시지 표시
    for message in st.session_state[f'{SERVICE_ID}_messages']:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 초기 메시지
    if not st.session_state[f'{SERVICE_ID}_messages']:
        with st.chat_message("assistant"):
            welcome_message = "Intellytics AI Agent에게 물어보세요!"
            st.markdown(welcome_message)
            st.session_state[f'{SERVICE_ID}_messages'].append({"role": "assistant", "content": welcome_message})
    
    # 자동 스크롤 컴포넌트 추가 (개선된 버전)
    if st.session_state[f'{SERVICE_ID}_messages']:
        components.html(
            """
            <script>
            function findChatContainer() {
                // 여러 가능한 선택자를 시도
                const selectors = [
                    '.stChatMessageContainer',
                    '[data-testid="stChatMessageContainer"]',
                    '.element-container:has(.stChatMessage)',
                    '#chat-container-marker',
                    '.main .block-container'
                ];
                
                for (const selector of selectors) {
                    const element = document.querySelector(selector);
                    if (element) {
                        // 스크롤 가능한 부모 요소 찾기
                        let parent = element;
                        while (parent && getComputedStyle(parent).overflowY !== 'auto' && parent !== document.body) {
                            parent = parent.parentElement;
                        }
                        return parent || element;
                    }
                }
                
                // 최후의 수단: 메인 컨테이너 반환
                return document.querySelector('.main') || document.body;
            }
            
            function scrollToBottom() {
                const chatContainer = findChatContainer();
                if (chatContainer) {
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }
            }
            
            // 즉시 스크롤 실행
            scrollToBottom();
            
            // 여러 시점에 스크롤 실행
            setTimeout(scrollToBottom, 100);
            setTimeout(scrollToBottom, 300);
            setTimeout(scrollToBottom, 500);
            setTimeout(scrollToBottom, 1000);
            </script>
            """,
            height=0,
            width=0,
        )

# 채팅 컨테이너 자동 스크롤 스크립트만 유지
st.markdown("""
<div class="chat-bottom-spacing"></div>

<script>
// 채팅 컨테이너를 자동으로 스크롤하는 함수
function scrollChatContainerToBottom() {
    const chatContainer = document.querySelector('.stChatMessageContainer');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

// 페이지 로드 후 및 DOM 변경 시마다 스크롤 함수 실행
document.addEventListener('DOMContentLoaded', function() {
    scrollChatContainerToBottom();
    // DOM 변경을 관찰하여 새 메시지가 추가될 때마다 스크롤
    const observer = new MutationObserver(function(mutations) {
        scrollChatContainerToBottom();
    });
    
    // 페이지 로드 후 잠시 기다린 후 채팅 컨테이너를 찾아 관찰 시작
    setTimeout(function() {
        const chatContainer = document.querySelector('.stChatMessageContainer');
        if (chatContainer) {
            observer.observe(chatContainer, { childList: true, subtree: true });
        }
        scrollChatContainerToBottom();
    }, 1000);
});
</script>
""", unsafe_allow_html=True)

# 채팅 입력을 사용하여 사용자 입력 받기
user_input = st.chat_input("질문을 입력하세요...", key=f"{SERVICE_ID}_chat_input")

# 저장된 대표 질문이 있는지 확인하고 처리
if st.session_state.get(f"{SERVICE_ID}_selected_question"):
    selected_question = st.session_state[f"{SERVICE_ID}_selected_question"]
    st.session_state[f"{SERVICE_ID}_selected_question"] = ""  # 처리 후 초기화
    process_user_query(selected_question)

# 사용자 입력 처리
if user_input and user_input.strip():
    # 대표 질문 선택 상태 초기화
    if f"{SERVICE_ID}_question_selected" in st.session_state:
        st.session_state[f"{SERVICE_ID}_question_selected"] = False
    
    # 줄바꿈 제거
    user_input = user_input.replace("\n", "")
    
    # 사용자 입력을 처리 함수로 전달
    process_user_query(user_input)
    
    # 입력창 초기화 - 여러 세션 상태 변수를 모두 초기화
    st.session_state[f"{SERVICE_ID}_user_input"] = ""
    st.session_state[f"{SERVICE_ID}_clear_input"] = True
    
    # 위젯 키 카운터 증가
    if f"{SERVICE_ID}_text_input_key_counter" in st.session_state:
        st.session_state[f"{SERVICE_ID}_text_input_key_counter"] = \
            st.session_state.get(f"{SERVICE_ID}_text_input_key_counter", 0) + 1
    
    # 페이지 새로고침
    st.rerun()

# 사이드바 너비 즉시 설정 (페이지 로드 시 바로 적용)
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

# 자바스크립트를 추가하여 Enter 키로 전송 기능 구현
st.markdown(f"""
<style>
   
    /* 메인 타이틀 스타일 */


    .main-title {{
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(45deg, #A50034, #FF385C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        text-shadow: 0 5px 10px rgba(0,0,0,0.1);
        letter-spacing: -0.5px;
        animation: fadeIn 1.5s ease-out;
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
        width: 70vw !important;
        max-width: 1200px !important;
        padding-left: 20px !important;
        padding-right: 20px !important;
        margin: 0 auto !important;
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

# CSS 스타일 추가
st.markdown("""
<style>

/* 채팅 하단 간격 */
.chat-bottom-spacing {
    height: 100px !important;
}

/* 채팅 컨테이너 스타일 */
.stChatMessageContainer {
    max-height: calc(100vh - 250px) !important;
    overflow-y: auto !important;
    width: 800px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-bottom: 20px !important;
}

/* 채팅 입력 스타일 - 컨테이너와 동일한 크기로 설정 */
[data-testid="stChatInput"] {
    max-width: 1200px !important;
    width: 70vw !important;
    margin-left: auto !important;
    margin-right: auto !important;
}
</style>

<script>
// ... existing code ...
</script>
""", unsafe_allow_html=True)
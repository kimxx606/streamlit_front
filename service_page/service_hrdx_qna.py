import streamlit as st
import requests
import json
import os
import streamlit.components.v1 as components
from streamlit_extras.stylable_container import stylable_container
from ldap3 import Connection, Server, ALL

# 외부 CSS 파일 불러오기
def load_css():
    with open("style/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# CSS 로드 함수 호출
load_css()

# d2c, mellerisearch expansion 기능
if st.session_state.hrdx_expanded == False:
    st.session_state.d2c_expanded = False
    st.session_state.survey_expanded = False
    st.session_state.mellerisearch_expanded = False
    st.session_state.hrdx_expanded = True
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
SERVICE_ID = "llo-hrdx-demo6"
# ========================================

# 초기 세션 상태 설정
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    
# 로그인 페이지
def login_page():

    st.title("🔐 Login")
    st.markdown("사용을 위해 AD 계정 로그인이 필요합니다.")
    
    user = st.text_input("Username", key="username")
    username = user + "@lge.com"
    password = st.text_input("Password", type="password", key="password")
    
    if st.button("Login", key="login"):
        server = Server('ldaps://lgesaads03.lge.net', get_info=ALL)
        try:
            conn = Connection(server, user=username, password=password, auto_bind=True)
            conn.search("dc=lge,dc=net", "(&(objectclass=person)(CN="+user+"))")
            check_aibd = str(conn.entries)
        except Exception as e:
            st.error("Invalid username or password")
            return False
        
        if (conn) and ("AI빅데이터담당(11002610)" in check_aibd) :   
            st.session_state.authenticated = True
            st.markdown('<div class="success-message">Login successful!</div>', unsafe_allow_html=True)
            st.session_state.auth = (user, password)
            conn.unbind()
            st.rerun()
            return True
        else:
            st.error("Invalid username or password")
            return False
            
def chat_page():
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

    if f"{SERVICE_ID}_country" not in st.session_state:
        st.session_state[f"{SERVICE_ID}_country"] = "United Kingdom"


    # ======= 서비스별 커스터마이징 영역 II =======
    # 이 부분을 수정하여 다양한 서비스에 화면을 구성합니다.

    # ==== MAIN 채팅 화면 정보 ====
    # 서비스 기본 정보
    SERVICE_NAME = {'ko': "HRDX 질의 서비스", "en": "HRDX - QnA Service"}

    SERVICE_DESCRIPTION = {
        "ko":"""해당 서비스는 직원의 업무 경험 및 HR 관련 다양한 정보를 간단한 질문을 통하여 얻을 수 있는 서비스입니다.<br>
        나의 업무 경험 뿐만 아니라, 다른 직원의 업무 경험에 대해서도 조회할 수 있습니다.<br>
        <br>
        예시)<br>
        <br>
        "홍길동"의 업무 경험에 대해서 요약해줘.<br>
        "홍길동"의 업무와 성향을 알려줘.
    """,
        "en" : "..."
    }

    # 대표 질문 리스트
    SAMPLE_QUESTIONS = {
        "ko":[
        "나의 업무 경험을 요약해줘.",
        "나의 업무와 성향을 알려줘.",
        "내 업무 성과를 요약해줘.",
        f'''직원 "{"김무성"}" 과 직원 "{"김수경"}"을 비교해줘''',
        "AI 솔루션 개발 경험을 갖는 직원을 추천해줘",
        "최근 해외 품질이슈 발생 시 처벌이 강화되는 추세여서 품질진단 관련 프로젝트팀을 구성할 예정인데, 적임자를 추천할 때 경험한 업무요약과 추천사유, 동료들의 평가와 함께 상세하게 추천해줘",
        "내 업무에 맞는 추천팀을 알려줘",
        "나의 성과 평가에서 개선할 점을 알려줘"
        ], 
        "en":[
        "under constuction..."
        ]
    }

    # 기본 API 엔드포인트
    #api_endpoint = os.environ.get("API 엔드포인트", "https://llo-hrdx-demo6.mkdev-kic.intellytics.lge.com/api/chat")
    api_endpoint = "http://" + SERVICE_ID + "." + os.getenv("ROOT_DOMAIN") + "/api/chat"
    # api_endpoint = st.text_input("API 엔드포인트", value="http://localhost:8081/ask")

    # ==== Sidebar 화면 정보 ====
    # SIDEBAR_INFO = "### 서비스 안내"
    # HTML 문법 가능
    SIDEBAR_SEARCHING_GUIDE = {
        "ko":"""
    ...<br>
    """,
        "en":"""
    Under construction... <br>       
    """
    }

    sample_questions_description = {
        "ko": "아래 질문을 클릭하면 채팅창에 입력되며 즉시 실행됩니다.",
        "en": "under construction..."
    }

    # ========================================


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
    def ask_llm_api(endpoint, query,language="ko"):
        try:
            
            user, password = st.session_state.get("auth", ("Unknown", "N/A"))
            # API 요청 데이터 준비
            payload = {
                    "emp_account" : user,
                    "question": query,
                    "language": language
            }
            
            # sg-server api
            response = requests.post(
                    endpoint,
                    headers={"accept": "application/json"},
                    params = payload,
                    verify=False
                )
            
            if response.status_code == 200:
                return {"success": True, "data": json.loads(response.json()["response"])["answer"]}
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
        if st.button("Log Out", key="logout_btn", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.pop("auth", None)  # auth 정보 삭제
            st.session_state[f'{SERVICE_ID}_messages'] = []
            #st.session_state["HRDX_Chat_messages"] = []
            st.rerun()
        
        st.title(SERVICE_NAME[st.session_state[SERVICE_ID + '_language']])
        
        # st.markdown(SIDEBAR_INFO)
        #st.markdown(SIDEBAR_SEARCHING_GUIDE[st.session_state[f"{SERVICE_ID}_language"]], unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 언어 선택 라디오 버튼
        # st.markdown("<div class='language-selector'>", unsafe_allow_html=True)
        # selected_language = st.radio(
        #     "Language:", 
        #     options=["한국어", "English"],
        #     index=0 if st.session_state.get(f"{SERVICE_ID}_language", "ko") == "ko" else 1,
        #     key=f"{SERVICE_ID}_language_radio",
        #     horizontal=True,
        #     on_change=lambda: st.session_state.update({f"{SERVICE_ID}_language": "ko" if st.session_state[f"{SERVICE_ID}_language_radio"] == "한국어" else "en"})
        # )
        # st.markdown("</div>", unsafe_allow_html=True)
        
        # # 언어 상태 자동 업데이트
        # st.session_state[f"{SERVICE_ID}_language"] = "ko" if selected_language == "한국어" else "en"
        
        # # 해외 법인 데이터 선택 
        # st.selectbox("Nation", ["United Kingdom", "Germany", "Spain", "Italy", "Brazil"],
        #                 index=0,
        #                 key=st.session_state[f"{SERVICE_ID}_country"],
        #                 disabled=True)
        
        # 채팅 초기화 버튼
        if st.button("대화 초기화", use_container_width=True, key=f"{SERVICE_ID}_reset_btn"):
            st.session_state[f'{SERVICE_ID}_messages'] = []
            st.session_state[f"{SERVICE_ID}_user_input"] = ""
            st.session_state[f"{SERVICE_ID}_selected_question"] = ""
            st.session_state[f"{SERVICE_ID}_question_selected"] = False
            st.session_state[f"{SERVICE_ID}_clear_input"] = False
            st.session_state[f"{SERVICE_ID}_text_input_key_counter"] = 0
            
            # refresh memory on the api server
            # response = requests.post(
            #     refresh_memory_api_url, 
            #     params={"dummy": "dummy"}  # llo qpi 규칙상 입출력 있어야하기 때문에 작성한 dummy
            # )

            st.rerun()
        
        st.divider()
        
        info_text = {"ko": "이 애플리케이션은 **Intellytics**에 배포된 LLM API를 사용합니다.", "en": "The Application uses LLM API distributed by **Intellytics**"}
        version_text = "© 2025 HRDX | Ver 1.0"
        st.info(info_text[st.session_state[f"{SERVICE_ID}_language"]])
        
        # 사이드바 하단에 저작권 정보 표시
        st.markdown("---")
        st.markdown(version_text)

    # 1. 메인 화면 및 서비스 설명
    st.markdown(f"<div class='main-title'>{SERVICE_NAME[st.session_state[SERVICE_ID + '_language']]}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='service-description'>{SERVICE_DESCRIPTION[st.session_state[SERVICE_ID + '_language']]}</div>", unsafe_allow_html=True)

    # 대표 질문 섹션
    st.markdown("<h3 class='sample-questions-title'>FAQ</h3>", unsafe_allow_html=True)
    st.markdown(f"<p class='sample-questions-description'>{sample_questions_description[st.session_state[SERVICE_ID+'_language']]}</p>", unsafe_allow_html=True)
    st.markdown("<div class='sample-questions-container'>", unsafe_allow_html=True)
    # 3. 대표 질문 버튼 컨테이너 및 버튼
    with stylable_container(
        key="sample_questions",
        css_styles="""
        button{
            display: flex;
            justify-content: flex-start;
            text-align: left;            /* 텍스트 자체를 왼쪽 정렬 */
            white-space: normal;         /* 긴 텍스트가 줄바꿈되도록 설정 */
            width: 100%;
        }

        """
    ):
        for i, question in enumerate(SAMPLE_QUESTIONS[st.session_state[SERVICE_ID + '_language']]):
            if st.button(question, key=f"{SERVICE_ID}_q_btn_{i}", use_container_width=True):
                # 선택된 질문을 user_input 세션 상태에 저장 (채팅 입력창에 표시하기 위해)
                st.session_state[f"{SERVICE_ID}_user_input"] = question
                # 대표 질문 선택 플래그 설정 - 입력창에 포커스를 주기 위한 용도로만 사용
                st.session_state[f"{SERVICE_ID}_question_selected"] = True
                st.session_state[f"{SERVICE_ID}_selected_question"] = question
                # 페이지 새로고침 (입력창에 질문 표시)
                st.rerun()
                
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
            #print(result.get("data", {}))
            #response = result.get("data", {}).get("result", "응답을 받지 못했습니다.")
            #response = result.get("data", {}).get("response", "응답을 받지 못했습니다.")
            response = result.get("data")
        
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

    # 채팅 입력을 사용하여 사용자 입력 받기
    user_input = st.chat_input(key=f"{SERVICE_ID}_chat_input")

    # 저장된 대표 질문이 있는지 확인하고 처리
    if st.session_state.get(f"{SERVICE_ID}_selected_question"):
        user_input = st.session_state[f"{SERVICE_ID}_selected_question"]
        st.session_state[f"{SERVICE_ID}_selected_question"] = ""  # 처리 후 초기화
        #process_user_query(selected_question)

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

    # 채팅 컨테이너 자동 스크롤을 위한 스크립트만 유지
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
    
if not st.session_state.authenticated:
    login_page()
else:
    chat_page()
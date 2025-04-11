import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import os

# 외부 CSS 파일 불러오기
def load_css():
    with open("style/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# CSS 로드 함수 호출
load_css()

# d2c, mellerisearch expansion 기능
if st.session_state.mellerisearch_expanded == False:
    st.session_state.d2c_expanded = False
    st.session_state.survey_expanded = False
    st.session_state.mellerisearch_expanded = True
    st.session_state.hrdx_expanded = False
    st.rerun() 

search_components = {
    'sub_agents': ['Communicator', 'Solution Searcher', 'Solution Recommender', 'Solution Guide'], 
    'possible_data_type': ['Tabular', 'Timeseries', 'Image', 'Text'], 
    'possible_task_type': ['Regression', 'Classification', 'Clustering', 'Anomaly Detection', 'Segmentation', 'Object Detection']}

# API 정보
search_port = 8318
endpoint_dict ={
    "create_aichat_communicator": "create_aichat_communicator",
    "Supervisor": "supervisor",
    "Datatype Collector": "communicator_datatype_collector",
    "Datatype Checker": "communicator_datatype_checker",
    "Tasktype Collector": "communicator_tasktype_collector",
    "Tasktype Checker": "communicator_tasktype_checker",
    "Solution Searcher": "solution_searcher",
    "Solution Recommender": "solution_recommender",
    "Solution Guide": "solution_guide"
}

# ======= API 통신 함수 =======
# 응답 형식:
# - success: 성공 여부 (True/False)
# - data: API 응답 데이터 (성공 시)
# - error: 오류 메시지 (실패 시)
def request_search_api(search_port, endpoint_name, state):
    try:
        #print(state)
        # API 요청 데이터 준비
        input = {
            "state": str(state)
        }

        # Endpoint 정의
        # endpoint = f"http://0.0.0.0:{search_port}/api/{endpoint_name}"
        # endpoint = f"https://melleri-search.mkdev-kic.intellytics.lge.com/api/{endpoint_name}"
        endpoint = f"http://{SERVICE_ID}.{os.getenv('ROOT_DOMAIN')}/api/{endpoint_name}"
        
        # API 호출
        response = requests.post(
            endpoint,
            params=input
        )
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
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

# ======= 응답 추가 함수 =======
def add_user_query(chat_container, query):
    # 사용자 입력 표시
    with chat_container.chat_message("user"):
        st.markdown(query)
    
    # 세션에 사용자 메시지 추가
    st.session_state[f'{SERVICE_ID}_messages'].append({"role": "user", "content": query})

def add_answer(chat_container, answer):
    with chat_container.chat_message("assistant"):
        st.markdown(answer, unsafe_allow_html=True)
    
    # 세션에 응답 메시지 추가
    st.session_state[f'{SERVICE_ID}_messages'].append({"role": "assistant", "content": answer})

# ==== MAIN 채팅 화면 정보 ====
# 서비스 기본 정보
SERVICE_ID = "melleri-search-demo"
SERVICE_NAME = "MelleriSearch 서비스"

# ==== Sidebar 화면 정보 ====
# SIDEBAR_INFO = "### 서비스 안내"
# HTML 문법 가능
SIDEBAR_GUIDE = """
**아래에서 원하시는 기능을 선택해주세요.**
"""
# ========================================

# 세션 상태 초기화 (서비스별 고유 키 사용)
def initialize_session_state(remove_history=True):
    if remove_history:
        st.session_state[f'{SERVICE_ID}_messages'] = []
        st.session_state[f"{SERVICE_ID}_text_input_key_counter"] = 0
    st.session_state[f'{SERVICE_ID}_current_agent'] = "Start"
    st.session_state[f'{SERVICE_ID}_state'] = dict({"question": "", "query_dict": {"data_type": "", "task_type:": ""}, "agent_history": []})
    st.session_state[f'{SERVICE_ID}_need_datatype_check'] = True
    st.session_state[f"{SERVICE_ID}_user_input"] = ""
    st.session_state[f"{SERVICE_ID}_selected_question"] = ""
    st.session_state[f"{SERVICE_ID}_question_selected"] = False
    st.session_state[f"{SERVICE_ID}_clear_input"] = False
    st.session_state[f'{SERVICE_ID}_show_guide_question'] = True
    st.rerun()


if f'{SERVICE_ID}_page_option' not in st.session_state:
    st.session_state[f'{SERVICE_ID}_page_option'] = "Search Solution"
    initialize_session_state()
        

# 사이드바 구성
with st.sidebar:
    st.title(SERVICE_NAME)
    
    # st.markdown(SIDEBAR_INFO)
    st.markdown(SIDEBAR_GUIDE, unsafe_allow_html=True)
    
    if st.session_state[f'{SERVICE_ID}_page_option'] == "Search Solution":
        st.markdown("---")
    # 채팅 초기화 버튼
        if st.button("대화 초기화", use_container_width=True, key=f"{SERVICE_ID}_reset_btn"):
            initialize_session_state()
    
    st.divider()
    
    st.info("""
    이 애플리케이션은 Intellytics에 배포된 LLM API를 사용합니다.
    """)
    
    # 사이드바 하단에 저작권 정보 표시
    st.markdown("---")
    st.markdown("© 2025 MelleriSearch | 버전 1.0")
        

# ======= 서비스 공통 영역 =======
# 메인 화면
st.markdown(f"<div class='main-title'>{SERVICE_NAME}</div>", unsafe_allow_html=True)
# Home
if st.session_state[f'{SERVICE_ID}_page_option'] == "Home":
    # 서비스 설명
    SERVICE_DESCRIPTION = """안녕하세요, MelleriSearch는 mellerikat에서 운영 가능한 검증된 AI 솔루션을 조회할 수 있는 검색 Agent입니다.\n  
MelleriSearch에서 제공하는 서비스는 다음과 같습니다.\n  
**AI 솔루션 문서 등록**: 검색 Agent가 빠르고 정확하게 조회할 수 있도록 문서를 추출합니다.\n  
**AI 솔루션 검색**: 검색 Agent가 사용자와 상호작용을 통해 적합한 솔루션을 검색합니다.
"""
    st.markdown(f"<div class='service-description'>{SERVICE_DESCRIPTION}</div>", unsafe_allow_html=True)
    st.image("images/Home1.PNG")
    st.image("images/Home2.PNG")
    

# Register Solution
if st.session_state[f'{SERVICE_ID}_page_option'] == "Register Solution":
    # 서비스 설명
    SERVICE_DESCRIPTION = """안녕하세요, melleriSearch는 mellerikat에서 운영 가능한 검증된 AI 솔루션을 조회할 수 있는 검색 서비스입니다.\n  
현재 서비스는 MelleriSearch에 솔루션을 등록하는 기능입니다.\n  
**필요한 정보를 기입주세요.**  
<br>
#### ■&nbsp;&nbsp;&nbsp;&nbsp; 작성 가이드  
<br>
◇&nbsp;&nbsp;Solution 이름: 영문 소문자, 특수 문자는 -만 허용  
<br><br> 
◇&nbsp;&nbsp;Data 유형: Tabular, Image, Time-series, Text 중 선택  <br><br>
◇&nbsp;&nbsp;Task 유형: Classification, Regression, Clustering, Anomaly Detection, Segmentation, Object Detection 중 선택  <br><br>
◇&nbsp;&nbsp;ALO 버전: v2, v3 중 선택  <br><br>
◇&nbsp;&nbsp;Git 주소: https://github.com/mellerihub/Awesome-AISolutins-for-mellerikat에 등록된 솔루션만 허용
"""
    st.markdown(f"<div class='service-description'>{SERVICE_DESCRIPTION}</div>", unsafe_allow_html=True)
    st.image("images/Register1.PNG")

# Search Solution

if st.session_state[f'{SERVICE_ID}_page_option'] == "Search Solution":

    # 대표 질문 리스트
    SAMPLE_QUESTIONS = [
        "전체 솔루션을 보여줘.",
        "정수기 구독 서비스의 향후 3년간의 월간 수익률을 예측하고 싶어.",
        "이미지 관련 솔루션을 보여줘.",
        "IOT 센서 데이터에 이상 감지를 하고 싶어."
    ]

    SAMPLE_GUIDE_QUESTIONS =[
        "도메인 적합성이 뭐야?",
        "대용량 데이터에 대해 비교해줘",
        "첫 번째 솔루션을 사용할게."
    ]

    # 서비스 설명
    SERVICE_DESCRIPTION = """안녕하세요, melleriSearch는 mellerikat에서 운영 가능한 검증된 AI 솔루션을 조회할 수 있는 검색 서비스입니다.  
    AI로 해결하고 싶은 과제에 대해 설명을 주시면 적합한 솔루션을 찾을 수 있도록 도움을 드리겠습니다.  
    어떤 과제를 수행하고 싶으신가요?
    """

    # 1. 서비스 설명
    st.markdown(f"<div class='service-description'>{SERVICE_DESCRIPTION}</div>", unsafe_allow_html=True)

    # 2. 대표 질문 섹션
    st.markdown("<h3 class='sample-questions-title'>대표 질문</h3>", unsafe_allow_html=True)
    st.markdown("<p class='sample-questions-description'>이 서비스의 예시 질문 목록입니다. 궁금한 질문을 클릭하면 바로 실행되니 편하게 활용해 보세요!</p>", unsafe_allow_html=True)

    # 3. 대표 질문 버튼 컨테이너 및 버튼
    st.markdown("<div class='sample-questions-container'>", unsafe_allow_html=True)
    for i, question in enumerate(SAMPLE_QUESTIONS):
        if st.button(question, key=f"{SERVICE_ID}_q_btn_{i}", use_container_width=True):
            st.session_state[f'{SERVICE_ID}_state'] = dict({"question": "", "query_dict": {"data_type": "", "task_type:": ""}, "agent_history": []})
            st.session_state[f'{SERVICE_ID}_current_agent'] = "Start"
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

        # # 사용자 입력 표시
        # with chat_container.chat_message("user"):
        #     st.markdown(query)
        
        # # 세션에 사용자 메시지 추가
        # st.session_state[f'{SERVICE_ID}_messages'].append({"role": "user", "content": query})
        # 사용자 입력 저장
        add_user_query(chat_container, query)


        # API 호출 (with spinner) - 스피너를 채팅 메시지와 입력창 사이에 표시 (To-Do)
        with spinner_container, st.spinner("답변을 생성 중입니다..."):
            # result = ask_llm_api(endpoint=api_endpoint, query=query, language=st.session_state[f"{SERVICE_ID}_language"])
            if st.session_state[f'{SERVICE_ID}_current_agent'] == "Start":
                st.session_state[f'{SERVICE_ID}_state']['question'] = query
                response = request_search_api(
                    search_port=search_port,
                    endpoint_name=endpoint_dict["Supervisor"],
                    state={
                        "question": st.session_state[f'{SERVICE_ID}_state']['question'],
                        "query_dict": st.session_state[f'{SERVICE_ID}_state']['query_dict'],
                        "agent_history": st.session_state[f'{SERVICE_ID}_state']['agent_history']
                        })
                if response['success']:
                    update_state = response['data']
                    st.session_state[f'{SERVICE_ID}_state'].update(update_state)
                    st.session_state[f'{SERVICE_ID}_current_agent'] = st.session_state[f'{SERVICE_ID}_state']["next"]
                    if st.session_state[f'{SERVICE_ID}_state']["next"] == "Communicator":
                        st.session_state[f'{SERVICE_ID}_current_agent'] = "Communicator Question"
                    else:
                        st.session_state[f'{SERVICE_ID}_current_agent'] = st.session_state[f'{SERVICE_ID}_state']["next"]
                else:
                    display_output = f"오류가 발생했습니다: {response['error']}"
                    add_answer(chat_container, display_output)
                    initialize_session_state(remove_history=False)
            if st.session_state[f'{SERVICE_ID}_current_agent'] == "Solution Searcher":
                response = request_search_api(
                    search_port=search_port,
                    endpoint_name=endpoint_dict[st.session_state[f'{SERVICE_ID}_current_agent']],
                    state={
                        "question": st.session_state[f'{SERVICE_ID}_state']['question'],
                        "agent_history": st.session_state[f'{SERVICE_ID}_state']['agent_history']
                        })
                if response['success']:
                    update_state = response['data']
                    st.session_state[f'{SERVICE_ID}_state'].update(update_state)
                    add_answer(chat_container, st.session_state[f'{SERVICE_ID}_state']["display_output"])
                    initialize_session_state(remove_history=False)
                else:
                    display_output = f"오류가 발생했습니다: {response['error']}"
                    add_answer(chat_container, display_output)
                    initialize_session_state(remove_history=False)

            if st.session_state[f'{SERVICE_ID}_current_agent'] == "Communicator Answer Datatype Checker":
                st.session_state[f'{SERVICE_ID}_state']['communicator_user_answer'] = query
                response = request_search_api(
                    search_port=search_port,
                    endpoint_name=endpoint_dict["Datatype Checker"],
                    state={
                        "communicator_user_answer": st.session_state[f'{SERVICE_ID}_state']['communicator_user_answer'],
                        "query_dict": st.session_state[f'{SERVICE_ID}_state']['query_dict']
                        })
                if response['success']:
                    update_state = response['data']
                    st.session_state[f'{SERVICE_ID}_state'].update(update_state)
                    if st.session_state[f'{SERVICE_ID}_state']['query_dict']['data_type'] != "Need to Fill":
                        st.session_state[f'{SERVICE_ID}_need_datatype_check'] = False
                    st.session_state[f'{SERVICE_ID}_current_agent'] = "Communicator Question"
                else:
                    display_output = f"오류가 발생했습니다: {response['error']}"
                    add_answer(chat_container, display_output)
                    initialize_session_state(remove_history=False)

            if st.session_state[f'{SERVICE_ID}_current_agent'] == "Communicator Answer Datatype Collector":
                st.session_state[f'{SERVICE_ID}_state']['communicator_user_answer'] = query
                response = request_search_api(
                    search_port=search_port,
                    endpoint_name=endpoint_dict["Datatype Collector"],
                    state={
                        "communicator_user_answer": st.session_state[f'{SERVICE_ID}_state']['communicator_user_answer'],
                        "query_dict": st.session_state[f'{SERVICE_ID}_state']['query_dict']
                        })
                if response['success']:
                    update_state = response['data']
                    st.session_state[f'{SERVICE_ID}_state'].update(update_state)
                    st.session_state[f'{SERVICE_ID}_need_datatype_check'] = False
                    st.session_state[f'{SERVICE_ID}_current_agent'] = "Communicator Question"
                else:
                    display_output = f"오류가 발생했습니다: {response['error']}"
                    add_answer(chat_container, display_output)
                    initialize_session_state(remove_history=False)

            if st.session_state[f'{SERVICE_ID}_current_agent'] == "Communicator Answer Tasktype Checker":
                st.session_state[f'{SERVICE_ID}_state']['communicator_user_answer'] = query
                response = request_search_api(
                    search_port=search_port,
                    endpoint_name=endpoint_dict["Tasktype Checker"],
                    state={
                        "communicator_user_answer": st.session_state[f'{SERVICE_ID}_state']['communicator_user_answer'],
                        "query_dict": st.session_state[f'{SERVICE_ID}_state']['query_dict']
                        })
                if response['success']:
                    update_state = response['data']
                    st.session_state[f'{SERVICE_ID}_state'].update(update_state)
                    if st.session_state[f'{SERVICE_ID}_state']['query_dict']['task_type'] != "Need to Fill":
                        st.session_state[f'{SERVICE_ID}_current_agent'] = "Solution Recommender" # To-Do: Supervisor
                    else:
                        st.session_state[f'{SERVICE_ID}_current_agent'] = "Communicator Question"
                else:
                    display_output = f"오류가 발생했습니다: {response['error']}"
                    add_answer(chat_container, display_output)
                    initialize_session_state(remove_history=False)

            if st.session_state[f'{SERVICE_ID}_current_agent'] == "Communicator Answer Tasktype Collector":
                st.session_state[f'{SERVICE_ID}_state']['communicator_user_answer'] = query
                response = request_search_api(
                    search_port=search_port,
                    endpoint_name=endpoint_dict["Tasktype Collector"],
                    state={
                        "communicator_user_answer": st.session_state[f'{SERVICE_ID}_state']['communicator_user_answer'],
                        "query_dict": st.session_state[f'{SERVICE_ID}_state']['query_dict']
                        })
                if response['success']:
                    update_state = response['data']
                    st.session_state[f'{SERVICE_ID}_state'].update(update_state)
                    st.session_state[f'{SERVICE_ID}_current_agent'] = "Solution Recommender"
                else:
                    display_output = f"오류가 발생했습니다: {response['error']}"
                    add_answer(chat_container, display_output)
                    initialize_session_state(remove_history=False)

            if st.session_state[f'{SERVICE_ID}_current_agent'] == "Communicator Question":
                if st.session_state[f'{SERVICE_ID}_need_datatype_check']:
                    if st.session_state[f'{SERVICE_ID}_state']["query_dict"]["data_type"] in search_components['possible_data_type']:
                        response = request_search_api(
                        search_port=search_port,
                        endpoint_name=endpoint_dict["create_aichat_communicator"],
                        state={
                            "data_type": st.session_state[f'{SERVICE_ID}_state']['query_dict']['data_type'],
                            "task_type": st.session_state[f'{SERVICE_ID}_state']['query_dict']['task_type'],
                            "step": "datatype_checker"
                            })
                        if response['success']:
                            aichat = response['data']
                            add_answer(chat_container, aichat['aichat'])
                            st.session_state[f'{SERVICE_ID}_current_agent'] = "Communicator Answer Datatype Checker"
                        else:
                            display_output = f"오류가 발생했습니다: {response['error']}"
                            add_answer(chat_container, display_output)
                            initialize_session_state(remove_history=False)
                    else:
                        add_answer(chat_container, "해결하고자 하는 과제의 데이터 타입을 알려줘. [{}]".format(','.join(search_components['possible_data_type'])))
                        st.session_state[f'{SERVICE_ID}_current_agent'] = "Communicator Answer Datatype Collector"
                else:
                    if st.session_state[f'{SERVICE_ID}_state']["query_dict"]["task_type"] in search_components['possible_task_type']:
                        response = request_search_api(
                        search_port=search_port,
                        endpoint_name=endpoint_dict["create_aichat_communicator"],
                        state={
                            "data_type": st.session_state[f'{SERVICE_ID}_state']['query_dict']['data_type'],
                            "task_type": st.session_state[f'{SERVICE_ID}_state']['query_dict']['task_type'],
                            "step": "tasktype_checker"
                            })
                        if response['success']:
                            aichat = response['data']
                            add_answer(chat_container, aichat['aichat'])
                            st.session_state[f'{SERVICE_ID}_current_agent'] = "Communicator Answer Tasktype Checker"
                        else:
                            display_output = f"오류가 발생했습니다: {response['error']}"
                            add_answer(chat_container, display_output)
                            initialize_session_state(remove_history=False)
                    else:
                        add_answer(chat_container, "해결하고자 하는 과제의 테스크 타입을 알려줘. [{}]".format(','.join(search_components['possible_task_type'])))
                        st.session_state[f'{SERVICE_ID}_current_agent'] = "Communicator Answer Tasktype Collector"
                st.rerun()

            if st.session_state[f'{SERVICE_ID}_current_agent'] == "Solution Recommender":
                response = request_search_api(
                    search_port=search_port,
                    endpoint_name=endpoint_dict[st.session_state[f'{SERVICE_ID}_current_agent']],
                    state={
                        "query_dict": st.session_state[f'{SERVICE_ID}_state']['query_dict'],
                        "agent_history": st.session_state[f'{SERVICE_ID}_state']['agent_history']
                        })
                if response['success']:
                    update_state = response['data']
                    st.session_state[f'{SERVICE_ID}_state'].update(update_state)
                    add_answer(chat_container, st.session_state[f'{SERVICE_ID}_state']["display_output"])
                    st.session_state[f'{SERVICE_ID}_current_agent'] = "Solution Guide"
                    st.rerun()
                else:
                    display_output = f"오류가 발생했습니다: {response['error']}"
                    add_answer(chat_container, display_output)
                    initialize_session_state(remove_history=False)

            if st.session_state[f'{SERVICE_ID}_current_agent'] == "Solution Guide":
                st.session_state[f'{SERVICE_ID}_state']['guide_question'] = query
                response = request_search_api(
                    search_port=search_port,
                    endpoint_name=endpoint_dict[st.session_state[f'{SERVICE_ID}_current_agent']],
                    state={
                        "guide_question": st.session_state[f'{SERVICE_ID}_state']['guide_question'],
                        "agent_history": st.session_state[f'{SERVICE_ID}_state']['agent_history'],
                        "search_result": st.session_state[f'{SERVICE_ID}_state']['search_result']
                        })
                if response['success']:
                    update_state = response['data']
                    print(update_state)
                    st.session_state[f'{SERVICE_ID}_state'].update(update_state)
                    add_answer(chat_container, st.session_state[f'{SERVICE_ID}_state']["display_output"])
                    st.session_state[f'{SERVICE_ID}_current_agent'] == "Solution Guide"
                    st.rerun()
                else:
                    display_output = f"오류가 발생했습니다: {response['error']}"
                    add_answer(chat_container, display_output)
                    initialize_session_state(remove_history=False)

        # 응답 표시
        # with chat_container.chat_message("assistant"):
        #     st.markdown(response, unsafe_allow_html=True)
        
        # # 세션에 응답 메시지 추가
        # st.session_state[f'{SERVICE_ID}_messages'].append({"role": "assistant", "content": response})
        
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
                welcome_message = "MelleriSearch Agent에게 물어보세요!"
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

    # # 페이지 끝에 여백 추가 (입력창이 메시지를 가리지 않도록)
    # st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

    # 채팅 입력을 사용하여 사용자 입력 받기
    user_input = st.chat_input("질문을 입력하세요...", key=f"{SERVICE_ID}_chat_input")

    # Solution Guide대표 질문 섹션
    if (st.session_state[f'{SERVICE_ID}_current_agent'] == "Solution Guide") & (st.session_state[f'{SERVICE_ID}_show_guide_question']):
        if len(st.session_state[f'{SERVICE_ID}_state']['search_result']) == 1: 
            SAMPLE_GUIDE_QUESTIONS = SAMPLE_GUIDE_QUESTIONS[2:]
        st.markdown("<h3 class='sample-questions-title'>추천 결과에 대한 질문</h3>", unsafe_allow_html=True)
        st.markdown("<p class='sample-questions-description'>이 서비스의 예시 질문 목록입니다. 궁금한 질문을 클릭하면 바로 실행되니 편하게 활용해 보세요!</p>", unsafe_allow_html=True)
        st.markdown("<div class='sample-questions-container'>", unsafe_allow_html=True)
        for i, question in enumerate(SAMPLE_GUIDE_QUESTIONS):
            if st.button(question, key=f"{SERVICE_ID}_guide_q_btn_{i}", use_container_width=True):
                st.session_state[f"{SERVICE_ID}_user_input"] = question
                st.session_state[f"{SERVICE_ID}_question_selected"] = True
                st.session_state[f"{SERVICE_ID}_selected_question"] = question  # 선택된 질문 저장
                st.session_state[f'{SERVICE_ID}_show_guide_question']=False
                st.rerun()  # 여기서는 rerun으로 페이지를 새로고침하고 아래의 코드에서 질문 처리
        st.markdown("</div>", unsafe_allow_html=True)



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

    # .main-title {{
    #     font-size: 2.2rem;
    #     font-weight: bold;
    #     margin-bottom: 1rem;
    #     color: #A50034; /* LG 로고 색상으로 메인 제목 변경 */
    #     text-align: center;
    # }}

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

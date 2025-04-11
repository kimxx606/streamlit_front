import streamlit as st
import requests
import json
import os
import streamlit.components.v1 as components
from streamlit_extras.stylable_container import stylable_container
import re
import pandas as pd

# 외부 CSS 파일 불러오기
def load_css():
    with open("style/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# CSS 로드 함수 호출
load_css()

# expansion 기능
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
SERVICE_ID = "voc-analysis"
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

if f"{SERVICE_ID}_country" not in st.session_state:
    st.session_state[f"{SERVICE_ID}_country"] = "United Kingdom"
    
if  f'{SERVICE_ID}_run_id' not in st.session_state:
    st.session_state[f'{SERVICE_ID}_run_id']=None


# ======= 서비스별 커스터마이징 영역 II =======
# 이 부분을 수정하여 다양한 서비스에 화면을 구성합니다.

# ==== MAIN 채팅 화면 정보 ====
# 서비스 기본 정보
SERVICE_NAME = {'ko': "VOC Analysis - 온라인 VOC 분석 서비스 v1.0", "en": "VOC Analysis - Online VOC Analysis Service v1.0"}

SERVICE_DESCRIPTION = {
    "ko":"""

#### 서비스 개요

VOC Analysis는 다양한 온라인 채널에서 수집된 고객 반응에 대해 여러 유형의 텍스트 분석이 가능한 서비스입니다. <br>
상품기획, 마케팅 등 다양한 부서에서 본 서비스를 활용하여 제품의 강/약점을 분석 가능하고, 신제품에 대한 의미있는 인사이트를 발굴할 수 있습니다. <br>
분석 기능 및 로직에 대한 자세한 사항은  🔍<a href="http://mod.lge.com/hub/smartdata/opdxt_llm/voc_logic">**로직 가이드**</a>를 참고해주세요. <br>

#### 사용 방법

**분석 기간, 분석 대상, 분석 유형**을 입력 메세지에 포함하여 요청해주세요.

- 분석하고자 하는 기간의 **연도와 월**을 명시해주세요. (ex. 2025년 1월)
- 분석하고자 하는 특정 **제품군 이름**을 명시해주세요. (ex. 세탁기, 건조기, 냉장고, ...)
- 제공하고 있는 **분석 유형**은 아래 3가지입니다. 원하시는 분석 유형을 명시해주세요.
   1) **감성 분석** - 응답의 긍정/부정적 감정을 분류
   2) **키워드 분석** - 응답의 주요 토픽 추출 및 wordcloud 생성
   3) **응답 유형 분석** - 주요 토픽별로 응답을 분류하고 비슷한 의견을 유형화

#### 데이터 정보
 - 내용 : Intellytics 온라인 VOC Korea 전 제품군 데이터 (한국어)
 - 기간 : 2025.1월 ~ 3월 (3개월)
 
#### 버전 정보

- v1.0 : 서비스 출시

""",
    "en":"""
under construction...
"""
}

# 대표 질문 리스트
SAMPLE_QUESTIONS = {
    "ko":[
    "2025년 1월 세탁기 제품군에 대한 감성 분석 수행해줘.",
    "2025년 2월 냉장고 제품군에 대한 키워드 분석 수행해줘",
    "2025년 3월 정수기 제품군에 대한 응답 유형 분석 수행해줘",
    ], 
    "en":[
    "under constuction..."
    ]
}

# 기본 API 엔드포인트
# api_endpoint = "http://" + SERVICE_ID + "." + os.getenv("ROOT_DOMAIN") + "/anal_voc"
# refresh_api_endpoint = "http://" + SERVICE_ID + "." + os.getenv("ROOT_DOMAIN") + "/refresh_memory"
# feedback_api_endpoint = "http://" + SERVICE_ID + "." + os.getenv("ROOT_DOMAIN") +"/get_langsmith_feedback"
api_endpoint = f"http://dx-d2c-demo-service.{os.getenv('ROOT_DOMAIN')}/api/fallout_chat"
reset_endpoint = f"http://dx-d2c-demo-service.{os.getenv('ROOT_DOMAIN')}/api/reset_chat"
feedback_api_endpoint = f"http://dx-d2c-demo-service.{os.getenv('ROOT_DOMAIN')}/api/get_langsmith_feedback"
# sg analysis api setting
# SERVER_URL='10.157.53.112:1234'
# api_endpoint = f"http://{SERVER_URL}/anal_voc"
# refresh_api_endpoint = f"http://{SERVER_URL}/refresh_memory"
# feedback_api_endpoint = f"http://{SERVER_URL}/get_langsmith_feedback"

# ==== Sidebar 화면 정보 ====
# SIDEBAR_INFO = "### 서비스 안내"
# HTML 문법 가능
SIDEBAR_SEARCHING_GUIDE = {
    "ko":"""
온라인 VOC에 대해 감성 분석, 키워드 분석, 응답 유형 분석 등을 수행하여 사용자에게 의미있는 인사이트를 제공합니다.<br>
""",
    "en":"""
Under construction... <br>       
"""
}

df_format = {
    "제품군 명": [
            "프로젝터",
            "에어컨",
            "레인지", 
            "냉장고",
            "로봇",
            "시스템 에어컨",
            "신발 건조기",
            "스마트홈",
            "TV",
            "청소기",
            "공조 시스템",
            "수처리 필터",
            "세탁기",
            "정수기",
            "XR"
        ],
    "2025-01": [
            957 ,
            1122 ,
            0 ,
            10304 ,
            27 ,
            72 ,
            9 ,
            0 ,
            8372 ,
            5969 ,
            0 ,
            0 ,
            14169 ,
            2520 ,
            0
        ],
    "2025-02": [
            681 ,
            2163 ,
            30 ,
            9477 ,
            20 ,
            38 ,
            12 ,
            0 ,
            9723 ,
            5681 ,
            0 ,
            0 ,
            14711 ,
            2556 ,
            0
        ],
    "2025-03": [
            767 ,
            5813 ,
            16 ,
            9899 ,
            34 ,
            126 ,
            10 ,
            0 ,
            10838 ,
            5469 ,
            0 ,
            0 ,
            15923 ,
            3349 ,
            48 ,
        ]
    
    
}

rs_df = pd.DataFrame(df_format)

# ========================================
from streamlit_feedback import streamlit_feedback


def collect_feedback(run_id):    
    feedback = streamlit_feedback(
        feedback_type="thumbs",
        optional_text_label="(optional) 자세한 피드백을 남겨주세요.",
        key=f"feedback_{run_id}",
    )
    score_mappings = {"thumbs": {"👍": 1, "👎": 0}}
    score_map = list(score_mappings.values())[0]
    if feedback:
        score = score_map.get(feedback["score"], None)
        comment = feedback.get("text", None)
        if comment is None:
            comment=''

        feedback_type_str = list(score_mappings.keys())[0]

        requests.post(
            feedback_api_endpoint, 
            params={'run_id':run_id, 'feedback_type_str':feedback_type_str, 
                    'score':score, 'comment':comment} # llo qpi 규칙상 입출력 있어야하기 때문에 작성한 dummy
        )

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
        # API 요청 데이터 준비
        payload = {
            "query": query,
            "language": language
        }
        
        # # API 호출
        # response = requests.post(
        #     endpoint,
        #     json=payload,
        #     headers={"Content-Type": "application/json"},
        #     timeout=30  # 30초 타임아웃 설정
        # )

        # sg-server api
        response = requests.post(
        endpoint, 
        timeout=300,  # 30초 타임아웃 설정
        params={"input_message": query}  # URL 파라미터로 전달
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


# ======= 화면 구성 시작 =======

# 사이드바 구성
with st.sidebar:
    st.title(SERVICE_NAME[st.session_state[SERVICE_ID + '_language']])
    
    # st.markdown(SIDEBAR_INFO)
    st.markdown(SIDEBAR_SEARCHING_GUIDE[st.session_state[f"{SERVICE_ID}_language"]], unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 언어 선택 라디오 버튼
    st.markdown("<div class='language-selector'>", unsafe_allow_html=True)
    selected_language = st.radio(
        "Language:", 
        options=["한국어", "English"],
        index=0 if st.session_state.get(f"{SERVICE_ID}_language", "ko") == "ko" else 1,
        key=f"{SERVICE_ID}_language_radio",
        horizontal=True,
        on_change=lambda: st.session_state.update({f"{SERVICE_ID}_language": "ko" if st.session_state[f"{SERVICE_ID}_language_radio"] == "한국어" else "en"})
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 언어 상태 자동 업데이트
    st.session_state[f"{SERVICE_ID}_language"] = "ko" if selected_language == "한국어" else "en"
    
    # 해외 법인 데이터 선택 
    st.selectbox("Nation", ["United Kingdom", "Germany", "Spain", "Italy", "Brazil"],
                    index=0,
                    key=st.session_state[f"{SERVICE_ID}_country"],
                    disabled=True)
    
    # 채팅 초기화 버튼
    if st.button("대화 초기화", use_container_width=True, key=f"{SERVICE_ID}_reset_btn"):
        st.session_state[f'{SERVICE_ID}_messages'] = []
        st.session_state[f"{SERVICE_ID}_user_input"] = ""
        st.session_state[f"{SERVICE_ID}_selected_question"] = ""
        st.session_state[f"{SERVICE_ID}_question_selected"] = False
        st.session_state[f"{SERVICE_ID}_clear_input"] = False
        st.session_state[f"{SERVICE_ID}_text_input_key_counter"] = 0
        
        # refresh memory on the api server
        response = requests.post(
            refresh_api_endpoint, 
            params={"dummy": "dummy"}  # llo qpi 규칙상 입출력 있어야하기 때문에 작성한 dummy
        )

        st.rerun()
    
    st.divider()
    
    info_text = {"ko": "이 애플리케이션은 **Intellytics**에 배포된 LLM API를 사용합니다.", "en": "The Application uses LLM API distributed by **Intellytics**"}
    version_text = "© 2025 VOC Analysis | Ver 1.0"
    st.info(info_text[st.session_state[f"{SERVICE_ID}_language"]])
    
    # 사이드바 하단에 저작권 정보 표시
    st.markdown("---")
    st.markdown(version_text)

# 1. 메인 화면 및 서비스 설명
st.markdown(f"<div class='main-title-gradient'>{SERVICE_NAME[st.session_state[SERVICE_ID + '_language']]}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='service-description'>{SERVICE_DESCRIPTION[st.session_state[SERVICE_ID + '_language']]}</div>", unsafe_allow_html=True)

# 대표 질문 섹션
st.markdown("<h3 class='sample-questions-title'>데이터 현황</h3>", unsafe_allow_html=True)
st.markdown("제품군별 VOC 데이터 수(row)는 다음과 같습니다")
st.dataframe(rs_df, hide_index=True, height=190)
st.markdown("<h3 class='sample-questions-title'>대표 질문</h3>", unsafe_allow_html=True)
st.markdown("VOC Analysis에서 확인 가능한 질문 예시를 참고해보세요.")
st.markdown("<div class='sample-questions-container'>", unsafe_allow_html=True)
# 3. 대표 질문 버튼 컨테이너 및 버튼
with stylable_container(
    key="sample_questions",
    css_styles="""
    button{
        display: flex;
        justify-content: flex-start;
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
    
    # distinguish the result example from query
    if "-->" in query:
        query_display = query.split("-->")[0]
    else:
        query_display = query
    
    # 사용자 입력 표시
    with chat_container.chat_message("user"):
        st.markdown(query_display)
    
    # 세션에 사용자 메시지 추가
    st.session_state[f'{SERVICE_ID}_messages'].append({"role": "user", "content": query_display})
    
    # API 호출 (with spinner) - 스피너를 채팅 메시지와 입력창 사이에 표시
    with spinner_container, st.spinner("답변을 생성 중입니다..."):
        result = ask_llm_api(endpoint=api_endpoint, query=query, language=st.session_state[f"{SERVICE_ID}_language"])

    # 응답 처리
    if not result.get("success", False):
        response = f"오류가 발생했습니다: {result.get('error', '알 수 없는 오류')}"
    else:
        print(result.get("data", {}))
        #response = result.get("data", {}).get("result", "응답을 받지 못했습니다.")
        response = result.get("data", {}).get("response", "응답을 받지 못했습니다.")
        response_img = result.get("data", {}).get("image", "no_image")
        run_id = result.get("data", {}).get("run_id", "run_id 응답을 받지 못했습니다.")
    
    # 응답 표시 (x) -> 메세지 표시를 바꿔야 실제 출력 메세지가 바뀜
    with chat_container.chat_message("assistant"):
        st.markdown(response)
    
    # 세션에 응답 메시지 추가
    st.session_state[f'{SERVICE_ID}_messages'].append({"role": "assistant", "content": response})
    st.session_state[f'{SERVICE_ID}_run_id']=run_id

    # 이미지 추가
    if not response_img == "no_image":
        st.session_state[f'{SERVICE_ID}_messages'].append({"role": "assistant", "content": response_img})
            
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
                const container = document.querySelector(selector);
                if (container) return container;
            }
            return null;
        }
        
        // 스크롤 함수
        function scrollToBottom() {
            const chatContainer = findChatContainer();
            if (chatContainer) {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        }
        
        // 0.5초 후 스크롤 (애니메이션이 끝날 때쯤)
        setTimeout(scrollToBottom, 500);
        
        // 안전을 위해 약간의 지연을 두고 다시 시도
        setTimeout(scrollToBottom, 800);
        </script>
        """,
        height=0,
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
            # check if the content is base64 encoded for displaying images
            if not None:
                check_base64 = re.search("^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$", message["content"])
                if check_base64:
                    html_str = f'<img src="data:image/jpeg;base64,{message["content"]}" width="450"/>'
                    wc_text = """주요 키워드를 바탕으로 생성한 Word Cloud는 다음과 같습니다.<br>&nbsp;"""
                    st.markdown(wc_text, unsafe_allow_html=True)
                    st.markdown(html_str, unsafe_allow_html=True)
                else:
                    st.markdown(message["content"])

    if len(st.session_state[f'{SERVICE_ID}_messages'])>1:
        if st.session_state[f'{SERVICE_ID}_messages'][-1]['role']=='assistant':
            collect_feedback(st.session_state[f'{SERVICE_ID}_run_id'])

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
                    const container = document.querySelector(selector);
                    if (container) return container;
                }
                return null;
            }
            
            // 스크롤 함수
            function scrollToBottom() {
                const chatContainer = findChatContainer();
                if (chatContainer) {
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }
            }
            
            // 0.5초 후 스크롤 (애니메이션이 끝날 때쯤)
            setTimeout(scrollToBottom, 500);
            
            // 안전을 위해 약간의 지연을 두고 다시 시도
            setTimeout(scrollToBottom, 800);
            </script>
            """,
            height=0,
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

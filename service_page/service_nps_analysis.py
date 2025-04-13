import streamlit as st
import requests
import json
import os
import time  # 추가: 타임스탬프 생성용
import uuid  # 추가: 고유 ID 생성용
import streamlit.components.v1 as components

from service_page.util.common_util import (
    render_page_title, render_service_description, render_section_divider,
    render_card_container_start, render_card_container_end, render_feature_card,
    render_footer, render_error_message, add_home_link
)

# CSS 스타일 추가
def add_custom_css():
    """외부 CSS 파일을 로드합니다."""
    with open("service_page/style/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


from service_page.util.utils import initialize_expansion_states, set_expanded_state
# d2c, survey genius, mellerisearch expansion 기능
initialize_expansion_states()
if set_expanded_state('survey'):
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
SERVICE_ID = "melleri-assistant" #"nps-analysis"
# ========================================


# ======= 서비스별 커스터마이징 영역 II =======
# 이 부분을 수정하여 다양한 서비스에 화면을 구성합니다.

# ==== MAIN 채팅 화면 정보 ====
# 서비스 기본 정보
SERVICE_NAME = "NPS Analysis 서비스 v1.0"
SERVICE_DESCRIPTION = """
DX Automation for NPS 서비스는 글로벌 <strong>LG-RNPS (Relationship Net Promoter Score)</strong> 설문 결과에 대해 편리하게 질의하고 결과를 빠르게 확인할 수 있는 서비스입니다.<br>
<strong>LG-RNPS</strong>는 LG 전자의 고객 경험 여정 전반에 걸쳐 고객 추천지수를 측정하는 LG 특화 툴로, 고객이 각 여정에서 경험한 LG 브랜드에 대한 타인 추천 가능성을 0점(전혀 추천하지 않을 것이다.)부터 10점(매우 추천할 것이다.)까지 평가합니다.<br>
제공하는 서비스의 코드는 git을 통해서 사용하실 수도 있으며, 코드에 대한 설명 및 가이드가 필요하시면 <a href="http://mod.lge.com/hub/dxtech/d2c_nps/">여기</a>를 참고하세요!
"""

# 대표 질문 리스트
SAMPLE_QUESTIONS = [
    "미국 법인의 제품군별 24년 NPS 결과 분석해줘.",
    "영국 법인의 세탁기 제품군 관련된 nps 결과를 분석해줘.",
    "영국 법인의 CEJ 여정별 24년 NPS 결과 분석해줘.",    
    "영국 법인 세탁기 제품의 배송 여정 관련 비추천 주관식 답변 분석해줘."
]

# # API 엔드포인트 형식 (중요: 서비스별 SERVICE_ID를 적용하여 엔드포인트에 연결합니다.)
# 실제 운영에서는 아래와 같이 endpoint의 전체 url로 수정해주셔야 합니다.
# 마지막에 API를 구분하는 path는 LLO화 하실 때 확인하실 수 있을 겁니다.
# api_endpoint = "http://" + SERVICE_ID + "." + os.getenv("ROOT_DOMAIN") + "/api/ask_chat"
# feedback_endpoint = "http://" + SERVICE_ID + "." + os.getenv("ROOT_DOMAIN") + "/api/feed_back"

# api_endpoint = "https://melleri-assistant.mkdev-kic.intellytics.lge.com/api/ask_chat"
# feedback_endpoint = "https://melleri-assistant.mkdev-kic.intellytics.lge.com/api/ask_chat"

# # # 테스트를 위한 API 엔드포인트 (테스트용입니다.)
api_endpoint = os.environ.get("API 엔드포인트", "http://localhost:1444/api/ask_chat")
feedback_endpoint = os.environ.get("API 엔드포인트", "http://localhost:1444/api/feed_back")


# ==== Sidebar 화면 정보 ====
# SIDEBAR_INFO = "### 서비스 안내"
# HTML 문법 가능
SIDEBAR_SEARCHING_GUIDE = """
LG-RNPS 데이터를 기반으로 2024년 NPS 점수 결과를 점검하고, 이와 연계하여 고객의 추천/비추천 의견을 분석하여 구체적인 원인을 파악할 수 있습니다.(현재 버전: v1.0)
"""

def render_feature_cards():
    render_section_divider()
   
    # 카드 섹션 직접 렌더링 (하나의 문자열로)
    st.markdown("""
    <div class="card-section">
        <div class="feature-card">
            <h3 style="color: #333; margin-bottom: 20px;">
                <span style="margin-right: 10px;">🔍</span> NPS 현황 점검 기능
            </h3>
            <div>
                <p style="margin-bottom: 12px;">
                    <span style="color: #4CAF50; margin-right: 8px;">✓</span>
                    2024년 글로벌 21개국 LG-RNPS 설문 결과에 대해 질의
                </p>
                <p style="margin-bottom: 12px;">
                    <span style="color: #4CAF50; margin-right: 8px;">✓</span>
                    국가 / 제품 / 여정별 NPS 현황을 자연어로 조회
                </p>
            </div>
        </div>
        <div class="feature-card">
            <h3 style="color: #333; margin-bottom: 20px;">
                <span style="margin-right: 10px;">📊</span> NPS 분석 기능
            </h3>
            <div>
                <p style="margin-bottom: 12px;">
                    <span style="color: #4CAF50; margin-right: 8px;">✓</span>
                    NPS 점검 결과와 연계하여 설문 데이터 중 고객의 추천 / 비추천 주관식 답변을 분석하여 구체적인 원인 도출
                </p>
                <p style="margin-bottom: 12px;">
                    <span style="color: #4CAF50; margin-right: 8px;">✓</span>
                    현재 고객의 추천 / 비추천 주관식 답변 분석은 2024년 영국법인에 대한 분석만 가능
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
    
if f'{SERVICE_ID}_message_feedback' not in st.session_state:
    st.session_state[f'{SERVICE_ID}_message_feedback'] = {}  # 메시지별 피드백 상태 저장

if f'{SERVICE_ID}_trace_ids' not in st.session_state:
    st.session_state[f'{SERVICE_ID}_trace_ids'] = {}  # 메시지별 trace_id 저장



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
# 5. ask_llm_api 함수 수정 - trace_id 저장 추가
def ask_llm_api(endpoint, query, language="ko"):
    try:
        # API 엔드포인트 URL 구성 (쿼리 파라미터 사용)
        api_url = f"{endpoint}?question={requests.utils.quote(query)}"
        
        # API 호출 (Body가 아닌 URL 파라미터로 전송)
        response = requests.post(
            api_url,
            headers={"accept": "application/json"},
            timeout=30  # 30초 타임아웃 설정
        )        
        
        if response.status_code == 200:
            # 전체 응답 확인
            data = response.json()
            
            # 응답에서 필드 추출
            answer = data.get("answer", "응답에 answer 필드가 없습니다.")
            sources = data.get("sources", [])
            trace_id = data.get("trace_id", "")  # trace_id 추출
            is_relevant = data.get("is_relevant", True)  # 관련성 여부 추출
            
            # 응답 구성
            return {
                "success": True,
                "data": {
                    "result": answer,
                    "sources": sources if is_relevant else [],  # 관련 있는 경우에만 sources 포함
                    "trace_id": trace_id,  # trace_id 추가
                    "is_relevant": is_relevant  # 관련성 여부 추가
                }
            }
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
    
# 4. 피드백 제출 API 함수 추가 (ask_llm_api 함수 다음에 추가)
def submit_feedback(feedback_type, feedback_text, query, response, trace_id):
    """
    사용자 피드백을 API에 제출하는 함수
    
    Args:
        feedback_type: "like", "dislike", "suggestion" 중 하나
        feedback_text: 피드백 텍스트 (선택사항)
        query: 원본 질문
        response: 챗봇 응답
        trace_id: chat_with_bot에서 반환된 trace_id
    
    Returns:
        dict: 성공 여부와 결과/오류 메시지
    """
    try:
        # 피드백 데이터 구성
        feedback_data = {
            "feedback_type": feedback_type,
            "feedback_text": feedback_text,
            "query": query,
            "response": response,
            "trace_id": trace_id
        }        
                
        response = requests.post(
            feedback_endpoint,
            json=feedback_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )                
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                return {"success": True, "data": result}
            else:
                return {"success": False, "error": result.get("error", "알 수 없는 오류")}
        else:
            return {
                "success": False, 
                "error": f"피드백 API 오류: {response.status_code}",
                "details": response.text
            }
            
    except Exception as e:
        return {"success": False, "error": f"피드백 제출 중 오류: {str(e)}"}

# ======= 새로운 화면 구성을 원하시면 아래 영역을 수정하시면 됩니다. =======
# 사이드바 구성
with st.sidebar:
    st.title("서비스 사용 가이드")
    
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
        # 피드백 상태도 초기화
        st.session_state[f'{SERVICE_ID}_message_feedback'] = {}
        st.session_state[f'{SERVICE_ID}_trace_ids'] = {}
        # 현재 활성화된 모든 dislike_reason_active 상태 초기화
        for key in list(st.session_state.keys()):
            if key.startswith(f'{SERVICE_ID}_dislike_reason_active_'):
                st.session_state.pop(key)
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

# 1.1
render_feature_cards()
# 2. 대표 질문 섹션
render_section_divider("대표 질문")
st.markdown("<p class='sample-questions-description'>이 서비스의 예시 질문 목록입니다. 궁금한 질문을 클릭하면 바로 실행되니 편하게 활용해 보세요!</p>", unsafe_allow_html=True)

# 대표 질문 버튼 컨테이너 시작
cols = st.columns(len(SAMPLE_QUESTIONS))
for i, question in enumerate(SAMPLE_QUESTIONS):
    with cols[i]:
        if st.button(question, key=f"{SERVICE_ID}_q_btn_{i}", use_container_width=True):
            st.session_state[f"{SERVICE_ID}_user_input"] = question
            st.session_state[f"{SERVICE_ID}_question_selected"] = True
            st.session_state[f"{SERVICE_ID}_selected_question"] = question
            st.rerun()


# 채팅 표시를 위한 placeholder 생성
chat_placeholder = st.empty()

# 로딩 스피너를 위한 컨테이너 (채팅 메시지 아래에 위치)
spinner_container = st.empty()

##################################################################################
# --- 스타일 정의 ---
st.markdown("""
<style>
.chat-container {
    width: 100%;
    padding: 10px 20px;
    margin-bottom: 20px; /* 하단 입력창 공간 확보 */
    text-align: left !important; /* 채팅 출력 왼쪽 정렬 */
}
.chat-row {
    display: flex;
    margin: 10px 0;
    justify-content: flex-start !important; /* 항상 왼쪽 정렬 */
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
    text-align: left !important; /* 버블 내용 왼쪽 정렬 */
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
    left: 350px; /* 사이드바 너비만큼 오른쪽으로 이동 */
    right: 0;
    background-color: white;
    padding: 12px 24px;
    box-shadow: 0 -2px 8px rgba(0,0,0,0.05);
    z-index: 9999;
}

/* block-container의 너비를 채팅 입력창과 일치하도록 설정 */
.block-container {
    max-width: 100% !important; /* 전체 너비 사용 */
    padding-left: 20px !important;
    padding-right: 20px !important;
    margin-left: 0 !important; /* 왼쪽 여백 제거 */
}

/* 대표 질문 왼쪽 정렬 */
[data-testid="stHorizontalBlock"] {
    justify-content: flex-start !important;
}

/* 대표 질문 버튼 스타일 */
[data-testid="stHorizontalBlock"] button {
    text-align: left !important;
    justify-content: flex-start !important;
}

/* 메인 타이틀 가운데 정렬 */
.main-title {
    text-align: center !important;
}

/* 서비스 설명 가운데 정렬 */
.service-description {
    text-align: left !important;
    width: 1200px !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* 샘플 질문 설명 왼쪽 정렬 */
.sample-questions-description {
    text-align: left !important;
}

/* 피쳐 카드 컨테이너 스타일 */
.feature-cards-container {
    width: 1200px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    display: flex !important;
    justify-content: center !important;
    gap: 20px !important;
}

/* 카드 섹션 스타일 */
.card-section {
    width: 1200px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    display: flex !important;
    justify-content: center !important;
    gap: 20px !important;
}

.feature-card {
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    height: 220px;
    position: relative;
    width: 700px;
    background-color: white;
}

</style>
""", unsafe_allow_html=True)




#####################################################################################


# 채팅 표시 함수 정의
def display_chat_messages():
    with chat_placeholder.container():
        container_style = "width: calc(100% - 350px) !important; margin-left: 0 !important; margin-right: 0 !important;"
        st.markdown(f'<div class="chat-container" style="{container_style}">', unsafe_allow_html=True)
        
        # 메시지 표시
        for message in st.session_state[f'{SERVICE_ID}_messages']:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-row user">
                    <div class="icon"></div>
                    <div class="bubble">👤{message['content']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-row bot">
                    <div class="icon"></div>
                    <div class="bubble"><b style="color: #A50034;">🤖Intellytics AI</b><br>{message['content']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # 초기 메시지
        if not st.session_state[f'{SERVICE_ID}_messages']:
            st.markdown(f"""
            <div class="chat-row bot">
                <div class="icon"></div>
                <div class="bubble"><b style="color: #A50034;">🤖 Intellytics AI</b><br>Intellytics AI Agent에게 물어보세요!</div>
            </div>
            """, unsafe_allow_html=True)
            st.session_state[f'{SERVICE_ID}_messages'].append({"role": "assistant", "content": "Intellytics AI Agent에게 물어보세요!"})
        
        st.markdown('</div>', unsafe_allow_html=True)

# 처음 페이지 로드 시 채팅 메시지 표시
display_chat_messages()

# 사용자 질문 처리 함수 정의
def process_user_query(query):
    # 세션에 사용자 메시지 추가
    st.session_state[f'{SERVICE_ID}_messages'].append({"role": "user", "content": query})
    
    # 메시지 표시 업데이트
    display_chat_messages()
    
    # API 호출 (with spinner) - 스피너를 채팅 메시지 아래에 표시
    with spinner_container, st.spinner("답변을 생성 중입니다..."):
        result = ask_llm_api(endpoint=api_endpoint, query=query, language=st.session_state[f"{SERVICE_ID}_language"])
    
    # 응답 처리
    if not result.get("success", False):
        response = f"오류가 발생했습니다: {result.get('error', '알 수 없는 오류')}"
    else:
        response = result.get("data", {}).get("result", "응답을 받지 못했습니다.")
    
    # 세션에 응답 메시지 추가
    st.session_state[f'{SERVICE_ID}_messages'].append({"role": "assistant", "content": response})
    
    # 메시지 표시 업데이트
    display_chat_messages()

# 입력창과 버튼을 감싸는 폼 생성
st.markdown('<div class="input-fixed">', unsafe_allow_html=True)
with st.form(key=f"{SERVICE_ID}_chat_form", clear_on_submit=True):
    # 입력창 초기화 여부 확인
    if st.session_state.get(f"{SERVICE_ID}_clear_input", False):
        st.session_state[f"{SERVICE_ID}_user_input"] = ""
        st.session_state[f"{SERVICE_ID}_clear_input"] = False
    
    # 입력창과 버튼을 한 줄에 배치하기 위한 컬럼 생성
    cols = st.columns([15, 1])  # 비율 조정
    
    # 첫 번째 컬럼에 입력창 배치
    with cols[0]:
        current_key = f"{SERVICE_ID}_text_input_{st.session_state[f'{SERVICE_ID}_text_input_key_counter']}"
        user_input = st.text_input("메시지를 입력하세요", 
                                value=st.session_state[f"{SERVICE_ID}_user_input"],
                                placeholder="메시지를 입력하세요...",
                                key=current_key,
                                label_visibility="collapsed")
    
    # 두 번째 컬럼에 버튼 배치
    with cols[1]:
        submitted = st.form_submit_button("→")
st.markdown('</div>', unsafe_allow_html=True)


# 폼 제출 처리
if submitted and user_input.strip():
    # 대표 질문 선택 상태 초기화
    if f"{SERVICE_ID}_question_selected" in st.session_state:
        st.session_state[f"{SERVICE_ID}_question_selected"] = False
    
    # 줄바꿈 제거
    user_input = user_input.replace("\n", "")
    
    # 사용자 입력 처리
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

# 저장된 대표 질문이 있는지 확인하고 처리
if st.session_state.get(f"{SERVICE_ID}_selected_question"):
    selected_question = st.session_state[f"{SERVICE_ID}_selected_question"]
    st.session_state[f"{SERVICE_ID}_selected_question"] = ""  # 처리 후 초기화
    process_user_query(selected_question)
    # 입력창 초기화 및 rerun
    st.session_state[f"{SERVICE_ID}_user_input"] = ""
    st.session_state[f"{SERVICE_ID}_clear_input"] = True
    st.rerun()  #

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
        font-size: 1rem;
        line-height: 1.5;
    }}
    
    /* Streamlit 기본 컨테이너 너비 조정 */
    .block-container {{
        max-width: 100% !important; /* 전체 너비 사용 */
        padding-left: 20px !important;
        padding-right: 20px !important;
        margin-left: 0 !important; /* 왼쪽 여백 제거 */
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
    height: 80px !important;
}

/* 입력 폼 고정 스타일 */
[data-testid="stForm"] {
    position: fixed !important;
    bottom: 20px !important;
    left: calc(50% + 175px) !important; /* 사이드바 너비 고려하여 중앙 정렬 */
    transform: translateX(-50%) !important;
    width: calc(100% - 350px) !important; /* 사이드바 너비(350px)를 뺀 너비로 설정 */
    margin: 0 !important;
    padding: 0px 0px !important;
    background-color: white !important;
    z-index: 9999 !important;
    border: none !important;
    box-shadow: none !important;
}

/* 폼 내부 컬럼 컨테이너 스타일 */
[data-testid="stForm"] > div[data-testid="column-container"] {
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    width: 100% !important;
}

/* 입력창 컬럼 스타일 */
[data-testid="stForm"] > div[data-testid="column-container"] > div:first-child {
    flex: 1 !important;
    width: auto !important;
}

/* 버튼 컬럼 스타일 */
[data-testid="stForm"] > div[data-testid="column-container"] > div:last-child {
    width: 40px !important;
    flex-shrink: 0 !important;
}

/* 입력창 내부 스타일 */
[data-testid="stForm"] [data-testid="stTextInput"] input {
    border-radius: 2px !important;
    border: 0px solid rgba(49, 51, 63, 0.2) !important;
    background-color: white !important;
    padding: 12px 20px !important;
    height: 40px !important;
    font-size: 14px !important;
    width: 100% !important;
    box-sizing: border-box !important;
}

/* 전송 버튼 스타일 */
[data-testid="stForm"] [data-testid="stFormSubmitButton"] {
    width: 40px !important;
    height: 40px !important;
}

/* 전송 버튼 내부 스타일 */
[data-testid="stForm"] [data-testid="stFormSubmitButton"] button {
    width: 40px !important;
    height: 40px !important;
    background-color: #A50034 !important;
    color: white !important;
    border-radius: 20px !important;
    border: none !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 20px !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* 전송 버튼 호버 효과 */
[data-testid="stForm"] [data-testid="stFormSubmitButton"] button:hover {
    background-color: #FA0029 !important;
}

/* 폼 내부 여백 제거 */
[data-testid="stForm"] .element-container {
    margin: 0 !important;
}

/* 컬럼 간격 조정 */
form .stColumns {
    gap: 15px !important;  /* 간격 증가 */
}

/* 채팅 컨테이너 스타일 */
.stChatMessageContainer {
    max-height: calc(100vh - 50px) !important;
    overflow-y: auto !important;
    width: calc(100% - 350px) !important; /* 사이드바 너비를 뺀 너비로 설정 */
    margin-left: 0 !important;
    margin-right: 0 !important;
    padding-bottom: 20px !important;
}

</style>

<script>
// 개선된 채팅 컨테이너 찾기 함수
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

// 개선된 스크롤 함수
function scrollToBottom() {
    const chatContainer = findChatContainer();
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

// 페이지 로드 시 스크롤
document.addEventListener('DOMContentLoaded', function() {
    // 초기 스크롤
    scrollToBottom();
    
    // 메시지 변경 감지
    const observer = new MutationObserver(function(mutations) {
        scrollToBottom();
    });
    
    // 채팅 컨테이너 관찰 시작
    const chatContainer = findChatContainer();
    if (chatContainer) {
        observer.observe(chatContainer, {
            childList: true,
            subtree: true
        });
    }

    // Enter 키 이벤트 처리
    const textInput = document.querySelector('input[type="text"]');
    if (textInput) {
        textInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                const submitButton = document.querySelector('button[type="submit"]');
                if (submitButton) {
                    submitButton.click();
                }
            }
        });
    }
    
    // 여러 시점에 스크롤 실행
    setTimeout(scrollToBottom, 100);
    setTimeout(scrollToBottom, 300);
    setTimeout(scrollToBottom, 500);
    setTimeout(scrollToBottom, 1000);
});

// 주기적으로 스크롤 위치 확인
setInterval(scrollToBottom, 1000);
</script>
""", unsafe_allow_html=True)
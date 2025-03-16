import streamlit as st
import requests
import json
import os

# ======= 서비스별 커스터마이징 영역 =======
# 이 부분만 수정하여 다양한 서비스에 적용 가능합니다

# 서비스 기본 정보
SERVICE_NAME = "Intellytics D2C 분석 서비스"
SERVICE_DESCRIPTION = """
이 서비스는 고객 NPS(Net Promoter Score) 데이터를 분석하여 
비즈니스 인사이트를 제공합니다. 
고객 피드백을 업로드하면 AI가 분석하여 개선점과 
주요 트렌드를 알려드립니다.
"""

# 서비스 ID (세션 상태 키 접두사로 사용)
SERVICE_ID = "nps3"

# 대표 질문 리스트
SAMPLE_QUESTIONS = [
    "NPS 점수가 가장 낮은 상위 3개 제품은 무엇인가요?",
    "지난 분기 대비 NPS 점수가 가장 많이 향상된 카테고리는?",
    "고객 불만이 가장 많은 영역과 개선 방안을 알려주세요"
]

# 기본 API 엔드포인트
DEFAULT_API_ENDPOINT = os.environ.get("SERVICE_API_URL", "http://localhost:8000/nps")

# ======= 서비스별 커스터마이징 영역 끝 =======

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

# 사이드바 구성
with st.sidebar:
    st.title(SERVICE_NAME)
    
    st.markdown("### 서비스 안내")
    st.markdown("NPS 데이터를 분석하여 사용자가 원하는 답변을 제공합니다.")
    st.markdown("**질문이 명확하고 자세할수록 더 정확한 답변을 받을 수 있습니다!**")
    
    st.markdown("---")
    
    # API 엔드포인트 설정
    api_endpoint = st.text_input("API 엔드포인트", value=DEFAULT_API_ENDPOINT, key=f"{SERVICE_ID}_api_endpoint")
    
    # 언어 선택 라디오 버튼
    st.markdown("<div class='language-selector'>", unsafe_allow_html=True)
    language = st.radio("언어 선택:", ("한국어", "English"), 
                        index=0 if st.session_state[f"{SERVICE_ID}_language"] == "ko" else 1,
                        horizontal=True,
                        key=f"{SERVICE_ID}_language_radio")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 언어 상태 업데이트
    st.session_state[f"{SERVICE_ID}_language"] = "ko" if language == "한국어" else "en"
    
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
    이 애플리케이션은 쿠버네티스에 배포된 LLM API를 사용합니다.
    
    기본 설정은 포트 포워딩(kubectl port-forward service/llm-api 8081:80)을 사용합니다.
    """)
    
    # 사이드바 하단에 저작권 정보 표시
    st.markdown("---")
    st.markdown("© 2025 LLM 서비스 템플릿 | 버전 1.0")

# 함수: API 호출
def ask_llm_api(query, endpoint, language="ko", history=None):
    try:
        # API 요청 데이터 준비
        payload = {
            "query": query,
            "language": language,
            "history": history or []
        }
        
        # API 호출
        response = requests.post(
            endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30  # 30초 타임아웃 설정
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

# 메인 화면
st.markdown(f"<div class='main-title'>{SERVICE_NAME}</div>", unsafe_allow_html=True)

# 서비스 설명
st.markdown(f"<div class='service-description'>{SERVICE_DESCRIPTION}</div>", unsafe_allow_html=True)

# 대표 질문 섹션
st.markdown("### 대표 질문")
st.markdown("아래 질문을 클릭하면 채팅 입력창에 복사됩니다. 전송 버튼이나 Enter 키를 눌러 질문을 전송하세요.")

# 대표 질문 버튼 표시
cols = st.columns(len(SAMPLE_QUESTIONS))
for i, question in enumerate(SAMPLE_QUESTIONS):
    if cols[i].button(question, key=f"{SERVICE_ID}_q_btn_{i}"):
        # 선택된 질문을 user_input 세션 상태에 저장 (채팅 입력창에 표시하기 위해)
        st.session_state[f"{SERVICE_ID}_user_input"] = question
        # 대표 질문 선택 플래그 설정 - 입력창에 포커스를 주기 위한 용도로만 사용
        st.session_state[f"{SERVICE_ID}_question_selected"] = True
        # 페이지 새로고침 (입력창에 질문 표시)
        st.rerun()

# 채팅 컨테이너 생성 (스크롤 가능한 영역)
chat_container = st.container()

# 로딩 스피너를 위한 컨테이너 (채팅 메시지와 입력창 사이에 위치)
spinner_container = st.empty()

# 메시지 표시 영역
with chat_container:
    # 메시지 표시
    for message in st.session_state[f'{SERVICE_ID}_messages']:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 초기 메시지
    if not st.session_state[f'{SERVICE_ID}_messages']:
        with st.chat_message("assistant"):
            welcome_message = "NPS 데이터에 대해 무엇이든 물어보세요!"
            st.markdown(welcome_message)
            st.session_state[f'{SERVICE_ID}_messages'].append({"role": "assistant", "content": welcome_message})

# 페이지 끝에 여백 추가 (입력창이 메시지를 가리지 않도록)
st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)

# 사용입력 처리 - 채팅창 아래에 배치
# 입력창과 버튼을 감싸는 폼 생성
with st.form(key=f"{SERVICE_ID}_chat_form", clear_on_submit=True):
    # 입력창 초기화 여부 확인
    if st.session_state.get(f"{SERVICE_ID}_clear_input", False):
        # 초기화 플래그가 설정되어 있으면 빈 문자열로 설정
        st.session_state[f"{SERVICE_ID}_user_input"] = ""
        st.session_state[f"{SERVICE_ID}_clear_input"] = False
    
    # 입력창과 버튼을 한 줄에 배치하기 위한 컬럼 생성
    col1, col2 = st.columns([25, 1])
    
    # 첫 번째 컬럼에 입력창 배치
    with col1:
        # 동적 키를 사용하여 text_input 위젯 생성
        current_key = f"{SERVICE_ID}_text_input_{st.session_state[f'{SERVICE_ID}_text_input_key_counter']}"
        user_input = st.text_input("사용자 입력", 
                                value=st.session_state[f"{SERVICE_ID}_user_input"],
                                placeholder="질문을 입력하세요...",
                                key=current_key,
                                label_visibility="collapsed")
    
    # 두 번째 컬럼에 버튼 배치
    with col2:
        # 폼 제출 버튼 (화살표 아이콘 사용)
        submitted = st.form_submit_button("→", use_container_width=True)

# 폼 제출 처리
if submitted and user_input.strip():
    # 대표 질문 선택 상태 초기화
    if f"{SERVICE_ID}_question_selected" in st.session_state:
        st.session_state[f"{SERVICE_ID}_question_selected"] = False
    
    # 줄바꿈 제거
    user_input = user_input.replace("\n", "")
    
    # 사용자 입력 표시
    with chat_container.chat_message("user"):
        st.markdown(user_input)
    
    # 세션에 사용자 메시지 추가
    st.session_state[f'{SERVICE_ID}_messages'].append({"role": "user", "content": user_input})
    
    # API 호출 (with spinner) - 스피너를 채팅 메시지와 입력창 사이에 표시
    with spinner_container, st.spinner("분석 중입니다..."):
        result = ask_llm_api(user_input, api_endpoint, st.session_state[f"{SERVICE_ID}_language"], 
                            st.session_state[f'{SERVICE_ID}_messages'][:-1])
    
    # 응답 처리
    if result["success"]:
        response = result["data"].get("response", "응답을 받지 못했습니다.")
    else:
        response = f"오류가 발생했습니다: {result['error']}"
    
    # 응답 표시
    with chat_container.chat_message("assistant"):
        st.markdown(response)
    
    # 세션에 응답 메시지 추가
    st.session_state[f'{SERVICE_ID}_messages'].append({"role": "assistant", "content": response})
    
    # 입력창 초기화 - 여러 세션 상태 변수를 모두 초기화
    st.session_state[f"{SERVICE_ID}_user_input"] = ""
    st.session_state[f"{SERVICE_ID}_clear_input"] = True
    
    # 위젯 키 카운터 증가
    if f"{SERVICE_ID}_text_input_key_counter" in st.session_state:
        st.session_state[f"{SERVICE_ID}_text_input_key_counter"] = \
            st.session_state.get(f"{SERVICE_ID}_text_input_key_counter", 0) + 1
    
    # 페이지 새로고침
    st.rerun()

# 자바스크립트를 추가하여 Enter 키로 전송 기능 구현
st.markdown(f"""
<script>
document.addEventListener('DOMContentLoaded', function() {{
    // 대표 질문이 선택되었는지 확인
    const questionSelected = {str(st.session_state.get(f"{SERVICE_ID}_question_selected", False)).lower()};
    
    // 현재 입력창 키 값 가져오기
    const currentInputKey = "{SERVICE_ID}_text_input_{st.session_state[f'{SERVICE_ID}_text_input_key_counter']}";
    
    // 입력창 요소 가져오기
    const textInput = document.querySelector(`input[data-testid="stTextInput"][key="${{currentInputKey}}"]`);
    
    // 대표 질문이 선택되었다면 입력창에 포커스
    if (questionSelected && textInput) {{
        // 입력창에 포커스
        textInput.focus();
    }}
    
    // 일반적인 Enter 키 처리 (Shift+Enter는 줄바꿈)
    if (textInput) {{
        textInput.addEventListener('keydown', function(e) {{
            if (e.key === 'Enter' && !e.shiftKey) {{
                e.preventDefault();
                // 폼 제출 버튼 클릭
                const submitButton = document.querySelector('button[data-testid="stFormSubmitButton"]');
                if (submitButton) {{
                    submitButton.click();
                }}
            }}
        }});
    }}
}});
</script>
<style>
    /* 메인 타이틀 스타일 */
    .main-title {{
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #A50034; /* LG 로고 색상으로 메인 제목 변경 */
    }}
    
    /* 서비스 설명 스타일 */
    .service-description {{
        background-color: #F3F4F6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
    }}
    
    /* 언어 선택기 스타일 */
    .language-selector {{
        margin-top: 1rem;
        margin-bottom: 2rem;
    }}
    
    /* 챗봇 메시지 창 배경 투명도 강화 */
    /* 챗봇 메시지 컨테이너 */
    .stChatMessage {{
        background-color: transparent !important;
    }}
    
    /* 챗봇 메시지 내용 배경 (사용자와 어시스턴트 공통) */
    .stChatMessage [data-testid="chat-message-content"] {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #000000 !important;
        padding: 10px !important;
        border-radius: 8px !important;
    }}
    
    /* 어시스턴트(AI) 메시지 스타일 */
    .stChatMessage.assistant [data-testid="chat-message-content"] {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-left: 3px solid rgba(165, 0, 52, 0.6) !important;
    }}
    
    /* 사용자 메시지 스타일 */
    .stChatMessage.user [data-testid="chat-message-content"] {{
        background-color: rgba(0, 0, 255, 0.9) !important;
        border-right: 3px solid rgba(30, 58, 138, 0.6) !important;
    }}
    
    /* 폼 스타일 */
    form {{
        position: relative;
        margin-top: 20px;
        margin-bottom: 20px;
        width: 100%;
        background-color: white !important;
        border: 1px solid white !important;
        border-radius: 10px !important;
        padding: 10px !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05) !important;
    }}
    
    /* 폼 내부 컬럼 스타일 */
    form .row-widget {{
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
    }}
    
    /* 입력창 스타일 */
    form [data-testid="stTextInput"] {{
        width: 100% !important;
        margin-bottom: 0 !important;
    }}
    
    /* 입력창 내부 스타일 */
    form [data-testid="stTextInput"] input {{
        border-radius: 25px !important;
        border: none !important;
        background-color: #f2f2f2 !important;
        padding: 12px 20px !important;
        height: 40px !important;
        font-size: 14px !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }}
    
    /* 입력창 placeholder 스타일 */
    form [data-testid="stTextInput"] input::placeholder {{
        color: #888888 !important;
        font-size: 14px !important;
    }}
    
    /* 전송 버튼 스타일 */
    form [data-testid="stFormSubmitButton"] {{
        height: 40px !important;
        margin-top: 0 !important;
        margin-left: 0 !important;
    }}
    
    /* 전송 버튼 내부 스타일 */
    form [data-testid="stFormSubmitButton"] button {{
        background-color: #A50034 !important;
        color: white !important;
        border-radius: 50% !important;
        height: 40px !important;
        width: 40px !important;
        margin: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: none !important;
        border: none !important;
        font-size: 20px !important;
        padding: 0 !important;
    }}
    
    /* 전송 버튼 호버 효과 */
    form [data-testid="stFormSubmitButton"] button:hover {{
        background-color: #8A0029 !important;
    }}
    
    /* 전송 버튼 텍스트 스타일 */
    form [data-testid="stFormSubmitButton"] button p {{
        font-size: 24px !important;
        margin: 0 !important;
        padding: 0 !important;
    }}
    
    /* 폼 내부 여백 제거 */
    form .element-container {{
        margin: 0 !important;
        padding: 0 !important;
    }}
    
    /* 컬럼 간격 조정 */
    form .stColumns {{
        gap: 10px !important;
    }}
    
    /* 스피너 위치 조정 */
    .stSpinner {{
        margin-top: 20px !important;
        margin-bottom: 20px !important;
    }}
    
    /* 채팅 메시지 영역에 하단 여백 추가 (입력창 가리지 않도록) */
    .main {{
        padding-bottom: 100px !important;
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
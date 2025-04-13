import streamlit as st
import requests
import json
import os
import time
import streamlit.components.v1 as components

# 외부 CSS 파일 불러오기
def load_css():
    with open("service_page/style/style.css", "r", encoding="utf-8") as f:
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
SERVICE_ID = "chatbot-generation"
# ========================================

# ======= 서비스별 커스터마이징 영역 II =======
# 이 부분을 수정하여 다양한 서비스에 화면을 구성합니다.

# ==== MAIN 채팅 화면 정보 ====
# 서비스 기본 정보
SERVICE_NAME = "Chatbot Generation 서비스"
SERVICE_DESCRIPTION = """
Chatbot Generation 서비스는 사용자가 자신만의 메뉴얼이나 문서를 업로드하여 맞춤형 AI 챗봇을 만들 수 있는 서비스입니다. <br>
문서를 업로드하고 MongoDB 정보를 입력하면, RAG(Retrieval-Augmented Generation) 기술을 활용하여 문서 내용에 대한 질의응답이 가능한 개인화된 챗봇이 생성됩니다.<br>
제공하는 서비스의 코드는 git을 통해서 사용하실 수도 있으며, 코드에 대한 설명 및 가이드가 필요하시면 <a href="http://mod.lge.com/hub/prism/mellerikat-assistant/-/tree/melleri-assistant/">여기</a>를 참고하세요!
"""

# 테스트를 위한 API 엔드포인트 (테스트용입니다.)
api_endpoint = os.environ.get("API 엔드포인트", "http://localhost:1444/api/process_documents")

# ==== Sidebar 화면 정보 ====
SIDEBAR_SEARCHING_GUIDE = """
본 Tool은 여러분의 문서를 기반으로 맞춤형 챗봇을 만들어주는 도구입니다.<br>
<b>문서를 업로드하고 MongoDB 설정을 완료한 후, 챗봇 생성 버튼을 클릭하면 끝!</b>
"""
# ========================================

# 세션 상태 초기화
if f'{SERVICE_ID}_uploaded_files' not in st.session_state:
    st.session_state[f'{SERVICE_ID}_uploaded_files'] = []

if f'{SERVICE_ID}_mongodb_uri' not in st.session_state:
    st.session_state[f'{SERVICE_ID}_mongodb_uri'] = ""

if f'{SERVICE_ID}_collection_name' not in st.session_state:
    st.session_state[f'{SERVICE_ID}_collection_name'] = ""

if f'{SERVICE_ID}_progress' not in st.session_state:
    st.session_state[f'{SERVICE_ID}_progress'] = 0

if f'{SERVICE_ID}_status' not in st.session_state:
    st.session_state[f'{SERVICE_ID}_status'] = ""

if f'{SERVICE_ID}_generation_complete' not in st.session_state:
    st.session_state[f'{SERVICE_ID}_generation_complete'] = False

if f"{SERVICE_ID}_language" not in st.session_state:
    st.session_state[f"{SERVICE_ID}_language"] = "ko"  # 기본 언어는 한국어


# API 통신 함수 (실제 API 연동 시 이 부분 수정 필요)
def process_documents_api(endpoint, files, mongodb_uri, collection_name, options=None):
    try:
        # 실제 API 연동이 아닌 시뮬레이션
        # 실제 구현 시 이 부분을 API
        
        progress_steps = [
            {"percent": 10, "status": "문서 파싱 중..."},
            {"percent": 30, "status": "텍스트 추출 중..."},
            {"percent": 50, "status": "청킹 및 전처리 중..."},
            {"percent": 70, "status": "임베딩 벡터 생성 중..."},
            {"percent": 90, "status": "MongoDB에 저장 중..."},
            {"percent": 100, "status": "챗봇 초기화 중..."}
        ]
        
        # 진행 상태 시뮬레이션
        for step in progress_steps:
            st.session_state[f'{SERVICE_ID}_progress'] = step["percent"]
            st.session_state[f'{SERVICE_ID}_status'] = step["status"]
            time.sleep(0.5)
            # st.rerun()
        
        # 성공 응답 반환
        return {
            "success": True,
            "data": {
                "message": "챗봇이 성공적으로 생성되었습니다.",
                "chatbot_id": "sample-chatbot-id-123",
                "mongodb_collection": collection_name
            }
        }
    except Exception as e:
        return {"success": False, "error": f"오류가 발생했습니다: {str(e)}"}


# 헤더 및 서비스 설명 렌더링
def render_header():
    st.markdown(f"<div class='main-title'>{SERVICE_NAME}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='service-description'>{SERVICE_DESCRIPTION}</div>", unsafe_allow_html=True)

# 기능 카드 렌더링
def render_feature(icon, title, features):
    st.markdown(f"""
    <div class='feature-title'>
        <div class='feature-icon'>{icon}</div>
        {title}
    </div>
    <ul class='feature-list'>
    """ + "".join([f"<li><strong>{f.split(' - ')[0]}</strong> - {f.split(' - ')[1]}</li>" for f in features]) + """
    </ul>
    """, unsafe_allow_html=True)

# 프로세스 단계 렌더링 
def render_process_step(step_number, title, description):
    st.markdown(f"""
    <div class='process-step'>
        <div class='step-header'>
            <div class='step-number'>{step_number}</div>
            <h3 class='step-title' style="font-size: 1.2rem; margin: 0; color: #333;">{title}</h3>
        </div>
        <p class='step-description'>{description}</p>
    """, unsafe_allow_html=True)

# 프로세스 단계 종료 태그
def render_process_step_end():
    st.markdown("</div>", unsafe_allow_html=True)

# ======= 화면 구성 시작 =======

# 사이드바 구성
with st.sidebar:
    st.title(SERVICE_NAME)
    
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
    
    # 설정 초기화 버튼
    if st.button("설정 초기화", use_container_width=True, key=f"{SERVICE_ID}_reset_btn"):
        st.session_state[f'{SERVICE_ID}_uploaded_files'] = []
        st.session_state[f'{SERVICE_ID}_mongodb_uri'] = ""
        st.session_state[f'{SERVICE_ID}_collection_name'] = ""
        st.session_state[f'{SERVICE_ID}_progress'] = 0
        st.session_state[f'{SERVICE_ID}_status'] = ""
        st.session_state[f'{SERVICE_ID}_generation_complete'] = False
        st.rerun()
    
    st.divider()
    
    st.info("""
    이 애플리케이션은 Intellytics에 배포된 LLM API를 사용합니다.
    """)
    
    # 사이드바 하단에 저작권 정보 표시
    st.markdown("---")
    st.markdown("© 2025 Intellytics AI Agent | 버전 1.0")

# 메인 화면 구성
render_header()

# 주요 기능 소개
# 기능 설명 텍스트를 이 부분에서 수정할 수 있습니다
# 형식: ["제목 - 설명", "제목 - 설명", "제목 - 설명"]

# 맞춤형 챗봇 생성 기능 (각 항목의 텍스트를 수정하여 내용 변경 가능)
chatbot_features = [
    ".md/.mdx 파일 기반 벡터 DB 생성 - Markdown 문서를 zip으로 압축해 업로드하면 자동으로 청킹하여 벡터 생성",
    "MongoDB 벡터 DB 연동 - 확장성 있는 저장소로 대용량 문서도 안정적으로 처리"    
]

# 간편한 챗봇 설정 기능 (각 항목의 텍스트를 수정하여 내용 변경 가능)
setup_features = [
    "OpenAI API 연동 - OpenAI API Key만 입력하면 ChatGPT 기반 질의응답 챗봇 즉시 활성화",
    "직관적 인터페이스 - 코딩 지식 없이도 몇 번의 클릭만으로 완성되는 챗봇 설정",    
]

# 소스 참조 기능 (각 항목의 텍스트를 수정하여 내용 변경 가능)
reference_features = [
    "메타데이터 자동 추출 - Markdown 파일 상단의 URL 정보를 자동으로 메타데이터로 저장",
    "답변 신뢰도 향상 - 챗봇의 응답과 함께 출처 확인 가능, 정보의 신뢰성 보장",    
]

render_feature("🤖", "맞춤형 챗봇 구축", chatbot_features)
render_feature("🚀", "간편한 챗봇 설정", setup_features)
render_feature("🔗", "소스 참조 기능", reference_features)

# 챗봇 생성 프로세스 섹션 추가
st.markdown("""
<h4 class="process-section-title">
    챗봇 생성 프로세스
</h4>
""", unsafe_allow_html=True)

# 스텝 1: 문서 업로드
render_process_step(1, "문서 업로드", "챗봇이 학습할 Markdown(.md/.mdx) 파일을 zip으로 압축하여 업로드해주세요. 자동으로 문서 내용을 분석하고 벡터화합니다.")

uploaded_files = st.file_uploader(
    "파일을 여기에 업로드하세요 (zip 압축파일 필수)", 
    type=["zip",], 
    accept_multiple_files=True,
    key=f"{SERVICE_ID}_document_uploader"
)

if uploaded_files:
    st.session_state[f'{SERVICE_ID}_uploaded_files'] = uploaded_files
    st.success(f"{len(uploaded_files)}개의 파일이 업로드되었습니다.")
    
    # 업로드된 파일 목록 표시
    with st.expander("업로드된 파일 목록"):
        for file in uploaded_files:
            st.write(f"📄 {file.name} ({file.size} bytes)")

render_process_step_end()

# 스텝 2: API 키 및 데이터베이스 설정
render_process_step(2, "API 키 및 데이터베이스 설정", "OpenAI API 키와 MongoDB 연결 정보를 입력하여 챗봇의 질의응답 기능과 데이터 저장소를 설정합니다.")

col1, col2 = st.columns(2)
with col1:
    openai_public_key = st.text_input(
        "OpenAI Public Key", 
        placeholder="sk-...",
        type="password",
        key=f"{SERVICE_ID}_openai_public_key"
    )

    openai_secret_key = st.text_input(
        "OpenAI Secret Key", 
        placeholder="sk-...",
        type="password",
        key=f"{SERVICE_ID}_openai_secret_key"
    )

    mongodb_uri = st.text_input(
        "MongoDB URI", 
        placeholder="mongodb://username:password@hostname:port/database",
        value=st.session_state.get(f'{SERVICE_ID}_mongodb_uri', ""),
        key=f"{SERVICE_ID}_mongodb_uri_input"
    )
    if mongodb_uri:
        st.session_state[f'{SERVICE_ID}_mongodb_uri'] = mongodb_uri

with col2:
    model_name = st.selectbox(
        "OpenAI 모델",
        options=["gpt-4o", "gpt-4o-mini"],
        index=1,
        help="챗봇에 사용할 OpenAI 모델을 선택합니다."
    )
    
    embedding_model = st.selectbox(
        "임베딩 모델",
        options=["text-embedding-3-large", "text-embedding-3-small", "text-embedding-ada-002"],
        index=1,
        help="텍스트를 벡터로 변환할 때 사용할 임베딩 모델을 선택합니다."
    )
    
    collection_name = st.text_input(
        "Collection 이름", 
        placeholder="my_chatbot_collection",
        value=st.session_state.get(f'{SERVICE_ID}_collection_name', ""),
        key=f"{SERVICE_ID}_collection_name_input"
    )
    if collection_name:
        st.session_state[f'{SERVICE_ID}_collection_name'] = collection_name

# 고급 설정 옵션
with st.expander("고급 설정 옵션"):
    st.markdown("""
    <p style="color: #555; font-size: 0.95rem; margin-bottom: 1rem;">
        챗봇 생성 과정에서 사용되는 고급 파라미터를 조정할 수 있습니다. 기본값을 사용하시면 대부분의 경우 좋은 결과를 얻을 수 있습니다.
    </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        chunk_size = st.slider("청크 크기", min_value=100, max_value=2000, value=500, 
                              help="문서 분할 시 청크의 크기를 설정합니다.")
    with col2:
        overlap = st.slider("청크 중첩", min_value=0, max_value=200, value=50,
                           help="청크 간 중첩되는 텍스트의 양을 설정합니다.")
    
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.1,
                          help="낮은 값은 더 결정적인 응답을, 높은 값은 더 창의적인 응답을 생성합니다.")
    
    # Langfuse 설정 추가
    st.markdown("##### Langfuse 설정 (선택 사항)")
    st.markdown("Langfuse를 사용하여 챗봇의 성능을 모니터링하고 로깅할 수 있습니다.")
    
    langfuse_col1, langfuse_col2 = st.columns(2)
    with langfuse_col1:
        langfuse_public_key = st.text_input(
            "Langfuse Public Key",
            placeholder="pk-lf-...",
            type="password",
            key=f"{SERVICE_ID}_langfuse_public_key"
        )
    
    with langfuse_col2:
        langfuse_secret_key = st.text_input(
            "Langfuse Secret Key",
            placeholder="sk-lf-...",
            type="password",
            key=f"{SERVICE_ID}_langfuse_secret_key"
        )
    
    langfuse_endpoint = st.text_input(
        "Langfuse Endpoint URL",
        placeholder="https://api.langfuse.com",
        value="https://api.langfuse.com",
        key=f"{SERVICE_ID}_langfuse_endpoint"
    )

render_process_step_end()

# 스텝 3: 챗봇 생성 버튼
render_process_step(3, "챗봇 생성", "모든 정보를 입력한 후 챗봇 생성 버튼을 클릭하세요. 잠시 후 맞춤형 챗봇이 생성됩니다.")

# 진행 상태 표시 영역
progress_placeholder = st.empty()
status_text = st.empty()

# 체크박스를 통한 동의 확인
agree = st.checkbox("입력한 정보가 정확하며, 챗봇 생성에 동의합니다.", key=f"{SERVICE_ID}_agree")

# 생성 버튼
btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
with btn_col2:
    generate_button = st.button(
        "챗봇 생성하기", 
        key=f"{SERVICE_ID}_generate_button", 
        disabled=not (st.session_state.get(f'{SERVICE_ID}_uploaded_files') and 
                    mongodb_uri and collection_name and agree and 
                    openai_public_key and openai_secret_key),
        type="primary",
        use_container_width=True
    )
    
    if generate_button:
        # API 호출
        with st.spinner("챗봇을 생성 중입니다..."):
            # 진행 상태 표시 (초기값 설정)
            progress_bar = progress_placeholder.progress(0)
            status_text.info("시작 중...")
            
            # API 호출
            result = process_documents_api(
                endpoint=api_endpoint,
                files=st.session_state.get(f'{SERVICE_ID}_uploaded_files'),
                mongodb_uri=mongodb_uri,
                collection_name=collection_name,
                options={
                    "chunk_size": chunk_size,
                    "overlap": overlap,
                    "embedding_model": embedding_model,
                    "openai_public_key": openai_public_key,
                    "openai_secret_key": openai_secret_key, 
                    "model_name": model_name,
                    "temperature": temperature,
                    "langfuse_public_key": langfuse_public_key if 'langfuse_public_key' in locals() else None,
                    "langfuse_secret_key": langfuse_secret_key if 'langfuse_secret_key' in locals() else None,
                    "langfuse_endpoint": langfuse_endpoint if 'langfuse_endpoint' in locals() else None
                }
            )
            
            # 결과 처리
            if result["success"]:
                # 성공 메시지
                st.session_state[f'{SERVICE_ID}_generation_complete'] = True
                progress_placeholder.progress(100)
                status_text.success("챗봇 생성이 완료되었습니다!")
                
                # 결과 표시
                st.markdown("""
                <div style="background-color: #f0fff4; padding: 1.2rem; border-radius: 8px; 
                         border-left: 4px solid #38a169; margin-top: 1.5rem;">
                    <h4 style="margin-top: 0; color: #2f855a; font-size: 1.2rem;">✅ 챗봇 생성 완료!</h4>
                    <p style="margin-bottom: 0.8rem; color: #444;">MongoDB 컬렉션: <strong>""" + 
                    result['data']['mongodb_collection'] + """</strong></p>
                    <p style="margin-bottom: 0; color: #444;">이제 'Your Chatbot' 페이지에서 생성된 챗봇과 대화할 수 있습니다.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Your Chatbot으로 이동 버튼
                if st.button("챗봇과 대화하기", key=f"{SERVICE_ID}_goto_chatbot", 
                           use_container_width=True, type="primary"):
                    # 실제로는 페이지 이동 구현 필요
                    pass
            else:
                # 오류 메시지
                progress_placeholder.empty()
                status_text.error(f"오류가 발생했습니다: {result.get('error', '알 수 없는 오류')}")

render_process_step_end()
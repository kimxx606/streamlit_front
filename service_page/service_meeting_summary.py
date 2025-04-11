# import torch
import datetime
import os

import streamlit as st
import streamlit.components.v1 as components

# d2c, survey genius, mellerisearch expansion 기능
if (st.session_state.d2c_expanded == True) or (st.session_state.mellerisearch_expanded == True) or (st.session_state.survey_expanded == True) or (st.session_state.hrdx_expanded == True):
    st.session_state.d2c_expanded = False
    st.session_state.survey_expanded = False
    st.session_state.mellerisearch_expanded = False
    st.session_state.hrdx_expanded = False
    st.rerun()

# 세션 초기화
st.session_state.setdefault("azure_api_key", "")

# 날짜
today = datetime.datetime.now().strftime("%Y-%m-%d")

# 기본 설정
# ======= 서비스별 커스터마이징 영역 I =======
# 서비스 ID (API 엔드포인트 고유값 및 세션 상태 키 접두사로 사용)
# 형식: '-'으로 두 단어를 연결
# 서비스 ID는 서비스별로 API 엔드포인트와 연결에 사용되므로 서비스별 고유한 값으로 선정해야 합니다.
SERVICE_ID = "Meeting-note"

# st.set_page_config(page_title="STT + Meeting Notes", layout="wide")
SERVICE_NAME = "Meeting Note"
SERVICE_DESCRIPTION = """
<div align="center" style="font-size:24px;">
🛠️<em>Under Construction</em>
</div>

### **서비스 개요**

**Meeting Note**는 오디오 파일을 업로드하면 자동으로 음성을 텍스트로 변환(STT)하고, AI가 이를 기반으로 요약된 회의록을 작성해주는 시스템입니다.

---

#### **사용 방법**

1. **오디오 파일 업로드**<br>
&nbsp;&nbsp;&nbsp;&nbsp;- 회의 오디오 파일(.mp3, .wav 등)을 선택하여 시스템에 업로드합니다.

2. **모델 선택**<br>
&nbsp;&nbsp;&nbsp;&nbsp;- 오디오를 텍스트로 변환할 때, 다음 네 가지 모델 중에서 필요에 따라 선택할 수 있습니다.

<style type="text/css">
.table-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-394r{color:#31333F;text-align:left;vertical-align:middle}
.tg .tg-6n1x{background-color:#efefef;color:#31333F;font-weight:bold;text-align:left;vertical-align:middle}
.tg .tg-sqj4{color:#31333F;font-weight:bold;text-align:left;vertical-align:top}
.tg .tg-izkt{color:#31333F;font-weight:bold;text-align:left;vertical-align:top}
.tg .tg-vbte{color:#31333F;text-align:left;vertical-align:middle}
</style>

<div class="table-wrapper">
  <table class="tg">
    <thead>
      <tr>
        <th class="tg-6n1x">모델명</th>
        <th class="tg-6n1x">파라미터 크기</th>
        <th class="tg-6n1x">파일 크기</th>
        <th class="tg-6n1x">정확도 및 속도</th>
        <th class="tg-6n1x">지원 언어</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="tg-sqj4"><span style="font-weight:600">tiny</span></td>
        <td class="tg-394r">39M</td>
        <td class="tg-394r">~75 MB</td>
        <td class="tg-394r">빠르지만 정확도 낮음</td>
        <td class="tg-394r">주요 언어, 명료한 발화 추천</td>
      </tr>
      <tr>
        <td class="tg-izkt"><span style="font-weight:600">base</span></td>
        <td class="tg-vbte">74M</td>
        <td class="tg-vbte">~140 MB</td>
        <td class="tg-vbte">속도와 정확도 균형 우수</td>
        <td class="tg-vbte">한국어 포함 대부분의 언어</td>
      </tr>
      <tr>
        <td class="tg-sqj4"><span style="font-weight:600">small</span></td>
        <td class="tg-394r">244M</td>
        <td class="tg-394r">~465 MB</td>
        <td class="tg-394r">정확도 더 높음, 속도 중간</td>
        <td class="tg-394r">대부분의 언어</td>
      </tr>
      <tr>
        <td class="tg-izkt"><span style="font-weight:600">medium</span></td>
        <td class="tg-vbte">769M</td>
        <td class="tg-vbte">~1.5 GB</td>
        <td class="tg-vbte">정확도 높음, 처리 속도 느림</td>
        <td class="tg-vbte">거의 모든 언어에서 매우 우수</td>
      </tr>
    </tbody>
  </table>
</div>


3. **디바이스 선택 (CPU vs GPU)**  <br>
&nbsp;&nbsp;&nbsp;&nbsp;- 변환 작업은 **CPU 또는 GPU** 중에서 선택하여 수행할 수 있습니다.

<style type="text/css">
.table-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-cly1{text-align:left;vertical-align:middle}
.tg .tg-1wig{font-weight:bold;text-align:left;vertical-align:top}
.tg .tg-6n1x{background-color:#efefef;color:#31333F;font-weight:bold;text-align:left;vertical-align:middle}
.tg .tg-3kij{font-weight:bold;text-align:left;vertical-align:top}
.tg .tg-uw4a{text-align:left;vertical-align:middle}
</style>

<div class="table-wrapper">
  <table class="tg">
    <thead>
      <tr>
        <th class="tg-6n1x">디바이스</th>
        <th class="tg-6n1x">장점</th>
        <th class="tg-6n1x">단점</th>
        <th class="tg-6n1x">권장 상황</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="tg-3kij"><span style="font-weight:600">CPU</span></td>
        <td class="tg-uw4a">별도 환경 설정 없이 사용 가능</td>
        <td class="tg-uw4a">처리 속도 느림</td>
        <td class="tg-uw4a">간단 테스트, 소형 모델 실행 시</td>
      </tr>
      <tr>
        <td class="tg-1wig"><span style="font-weight:600">GPU</span></td>
        <td class="tg-cly1">매우 빠른 처리 속도</td>
        <td class="tg-cly1">CUDA 환경 필요, 메모리 요구</td>
        <td class="tg-cly1">medium 모델 이상 사용 시 강력 추천</td>
      </tr>
    </tbody>
  </table>
</div>


> 💡 **tip**: `medium` 모델은 파라미터 수가 많고 연산량이 크기 때문에 **GPU 환경에서 실행**하는 것이 좋습니다. 반면 `tiny`나 `base`는 CPU 환경에서도 충분히 작동합니다.

4. **텍스트 변환 및 요약**<br>
&nbsp;&nbsp;&nbsp;&nbsp;- 선택한 모델과 디바이스를 기반으로 음성을 텍스트로 변환하며, 이후 AI가 회의의 핵심 내용을 자동으로 요약하여 제공합니다.

---

#### **권장 모델 활용 예시**
&nbsp;&nbsp;&nbsp;&nbsp;- **빠른 처리**가 중요한 짧고 간단한 회의는 **tiny** 또는 **base**.<br>
&nbsp;&nbsp;&nbsp;&nbsp;- **정확도와 속도의 균형**이 중요한 일반적인 회의는 **base** 또는 **small**.<br>
&nbsp;&nbsp;&nbsp;&nbsp;- 긴 회의나 복잡한 내용을 최대한 정확하게 기록하고 요약할 때는 **medium** (**GPU 권장**).

※ <a href="http://mod.lge.com/hub/dxtech/hackathon/meeting_agent/-/blob/main/README.md">사용 가이드</a>
"""

# ==========================================
# SIDEBAR SETTING AREA
# ==========================================

# ==== Sidebar 화면 정보 ====
# HTML 문법 가능
SIDEBAR_SEARCHING_GUIDE = """
회의 **녹음 파일(mp3, wav)**을 올려주시면, **회의록을 자동 생성**해드립니다.
"""

SIDEBAR_INFO = "해당 서비스는 현재 **제작중**입니다."

# ======= 화면 구성 시작 =======

# 사이드바 구성
with st.sidebar:
    st.title(SERVICE_NAME)  # name of service
    st.markdown(SIDEBAR_SEARCHING_GUIDE, unsafe_allow_html=True)  # service guide

    st.divider()  # ---

    # 언어 선택 라디오 버튼
    st.markdown("<div class='language-selector'>", unsafe_allow_html=True)
    selected_language = st.radio(
        "언어 선택:",
        options=["한국어", "English"],
        index=(
            0 if st.session_state.get(f"{SERVICE_ID}_language", "ko") == "ko" else 1
        ),
        key=f"{SERVICE_ID}_language_radio",
        horizontal=True,
        on_change=lambda: st.session_state.update(
            {
                f"{SERVICE_ID}_language": (
                    "ko"
                    if st.session_state[f"{SERVICE_ID}_language_radio"] == "한국어"
                    else "en"
                )
            }
        ),
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # 언어 상태 자동 업데이트
    st.session_state[f"{SERVICE_ID}_language"] = (
        "ko" if selected_language == "한국어" else "en"
    )

    # 채팅 초기화 버튼
    if st.button(
        "대화 초기화", use_container_width=True, key=f"{SERVICE_ID}_reset_btn"
    ):
        st.session_state[f"{SERVICE_ID}_messages"] = []
        st.session_state[f"{SERVICE_ID}_user_input"] = ""
        st.session_state[f"{SERVICE_ID}_selected_question"] = ""
        st.session_state[f"{SERVICE_ID}_question_selected"] = False
        st.session_state[f"{SERVICE_ID}_clear_input"] = False
        st.session_state[f"{SERVICE_ID}_text_input_key_counter"] = 0
        st.rerun()

    st.divider()

    st.info(SIDEBAR_INFO)

    # 사이드바 하단에 저작권 정보 표시
    st.markdown("---")
    st.markdown("© 2025 Meeting Note | Ver 1.0")

# 1. 메인 화면 및 서비스 설명

st.markdown(f"<div class='main-title'>{SERVICE_NAME}</div>", unsafe_allow_html=True)
st.markdown(
    f"<div class='service-description'>{SERVICE_DESCRIPTION}</div>",
    unsafe_allow_html=True,
)

# ==========================================
# 모델 설정 섹션 (버튼 방식으로 변경)
# ==========================================

# Whisper 모델 설정
st.subheader("🧠 음성 -> 텍스트 변환 모델 설정")

# 기본값 초기화 (최초 실행 시)
if "model_size" not in st.session_state:
    st.session_state["model_size"] = "base"

if "device" not in st.session_state:
    st.session_state["device"] = "cpu"

# 모델 선택 라디오 버튼
st.radio(
    "🔍 모델 크기 선택",
    options=["tiny", "base", "small", "medium"],
    index=["tiny", "base", "small", "medium"].index(st.session_state["model_size"]),
    key="model_size",
    horizontal=True,
)

st.info(
    f"현재 설정된 모델: `{st.session_state['model_size']}`"
)  # 현재 설정 정보 표시

# 디바이스 선택 라디오 버튼
st.radio(
    "⚙️ 디바이스 선택",
    options=["cpu", "gpu"],
    index=["cpu", "gpu"].index(st.session_state["device"]),
    key="device",
    horizontal=True,
)

st.info(f"디바이스: `{st.session_state['device']}`")  # 현재 설정 정보 표시

# with st.expander("고급 설정"):
#     chunk_duration = st.slider("Chunk duration (초)", 60, 900, 600, 60)
#     include_timestamps = st.checkbox("타임스탬프 포함", False)
#     generate_notes = st.checkbox("회의 요약 생성", True)

# 파일 업로드 섹션
st.subheader("📁 오디오 파일 업로드")
uploaded_file = st.file_uploader(
    "MP3, WAV, M4A, FLAC 파일 지원", type=["mp3", "wav"]
)

if uploaded_file:
    filename = uploaded_file.name
    filename_wo_ext, _ = os.path.splitext(filename)

    audio_path = f"input/{today}/uploaded_{filename}"
    output_path = f"output/{today}/uploaded_{filename_wo_ext}_text_output.txt"
    notes_path = f"notes/{today}/uploaded_{filename_wo_ext}_notes.md"

    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    with open(audio_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"파일 저장됨: {audio_path}")

# 트랜스크립션 버튼
if st.button("📝 Transcribe & Generate Notes"):
    # 아래 transcription 영역은 LLO API 통신으로 (text -> transcribe -> generate) 수행예정
    st.error(
        f"""
        ❌ 현재 해당 기능은 개발 중입니다. \n\n
        설정 정보:
        - 모델: `{st.session_state.get('model_size', 'base')}`
        - 디바이스: `{st.session_state.get('device', 'cpu')}`
        """
    )
    # run_transcription(audio_path, output_path, notes_path, model_size, device, include_timestamps, chunk_duration, generate_notes)

# ==========================================
# CSS - 정의 구간
# ==========================================

# 사이드바 너비 즉시 설정 (페이지 로드 시 바로 적용)
st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)

# .main-title {{
#     font-size: 2.2rem;
#     font-weight: bold;
#     margin-bottom: 1rem;
#     color: #A50034; /* LG 로고 색상으로 메인 제목 변경 */
#     text-align: center;
# }}

# 자바스크립트를 추가하여 Enter 키로 전송 기능 구현
st.markdown(
    f"""
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
""",
    unsafe_allow_html=True,
)

# CSS 스타일 추가
st.markdown(
    """
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
    max-width: 800px !important;
    width: 800px !important;
    margin-left: auto !important;
    margin-right: auto !important;
}
</style>

<script>
// ... existing code ...
</script>
""",
    unsafe_allow_html=True,
)


# if __name__ == "__main__":
#     main()

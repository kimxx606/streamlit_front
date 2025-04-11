import os
import streamlit as st
import streamlit.components.v1 as components
import requests
import json

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


# ======= API 통신 함수 =======
# 응답 형식:
# - success: 성공 여부 (True/False)
# - data: API 응답 데이터 (성공 시)
# - error: 오류 메시지 (실패 시)

# ==== MAIN 채팅 화면 정보 ====
# 서비스 기본 정보
SERVICE_ID = "melleri-search-register-demo"
SERVICE_NAME = "MelleriSearch 서비스"

# ==== Sidebar 화면 정보 ====
# SIDEBAR_INFO = "### 서비스 안내"
# HTML 문법 가능
SIDEBAR_GUIDE = """
**아래에서 원하시는 기능을 선택해주세요.**
"""
# ========================================

# API 정보
# register_port = 8538
# register_api = f"http://0.0.0.0:{register_port}/api/generate_guide_and_update_db"
# register_api = "https://melleri-search-register.mkdev-kic.intellytics.lge.com/api/generate_guide_and_update_db"
# register_api = f"https://melleri-search.mkdev-kic.intellytics.lge.com/api/{endpoint_name}"

endpoint_name = "generate_guide_and_update_db"
# endpoint = f"http://{SERVICE_ID}.{os.getenv('ROOT_DOMAIN')}/api/{endpoint_name}"
endpoint = "https://melleri-search-register.mkdev-kic.intellytics.lge.com/api/generate_guide_and_update_db"

# 사이드바 구성
with st.sidebar:
    st.title(SERVICE_NAME)
    
    # st.markdown(SIDEBAR_INFO)
    st.markdown(SIDEBAR_GUIDE, unsafe_allow_html=True)
    
    st.markdown("---")
    with st.form(key="form1"):
        solution_name = st.text_input(label="**Solution 이름:**", key="solution_name")
        data_type = st.selectbox(label="**Data 유형:**", options=search_components['possible_data_type'])
        task_type = st.selectbox(label="**Task 유형:**", options=search_components['possible_task_type'])
        alo_ver = st.selectbox(label="**ALO 버전:**", options=["v2", "v3"])
        git_url = st.text_input(label="**Git 주소:**", key="git_url")
        register = st.form_submit_button(label="Solution 등록")
        if register:
            if not bool(solution_name):
                st.error("Solution 이름을 입력해주세요.")
            elif not bool(data_type):
                st.error("Data 유형을 선택해주세요.")
            elif not bool(task_type):
                st.error("Task 유형을 선택해주세요.")
            elif not bool(alo_ver):
                st.error("ALO 버전을 선택해주세요.")
            elif not bool(git_url):
                st.error("Git 주소를 입력해주세요.")
            else:
                params = {
                    "solution_name": solution_name,  # DB에 등록안된 신규 솔루션 명
                    "data_type": data_type,
                    "task_type": task_type,
                    "git_url": git_url,
                    "alo_version": alo_ver,
                    "db_name": "solutions_meta"}
                response = requests.post(endpoint, params= params)
                register_result = response.json()['response']
                if register_result == "Success":
                    st.success("Solution 등록이 완료되었습니다.")
                else:
                    st.error(register_result)

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

# Register Solution

# 서비스 설명
st.image("service_page/images/Register1.PNG")
SERVICE_DESCRIPTION = """안녕하세요, melleriSearch는 mellerikat에서 운영 가능한 검증된 AI 솔루션을 조회할 수 있는 검색 서비스입니다.\n  
현재 서비스는 MelleriSearch에 솔루션을 등록하는 기능입니다.\n  
**필요한 정보를 기입주세요.** \n

#### ■&nbsp;&nbsp;&nbsp;&nbsp; 작성 가이드\n
**- &nbsp;&nbsp;Solution 이름: 영문 소문자, 특수 문자는 -만 허용**\n
**- &nbsp;&nbsp;Data 유형: Tabular, Image, Time-series, Text**\n
**- &nbsp;&nbsp;Task 유형: Classification, Regression, Clustering, Anomaly Detection, Segmentation, Object Detection**\n
**- &nbsp;&nbsp;ALO 버전: v2, v3 중 선택**\n
**- &nbsp;&nbsp;Git 주소: https://github.com/mellerihub/Awesome-AISolutins-for-mellerikat 등록 솔루션만 허용**
"""
st.markdown(f"<div class='service-description'>{SERVICE_DESCRIPTION}</div>", unsafe_allow_html=True)

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

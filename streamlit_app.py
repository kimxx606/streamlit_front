import streamlit as st
from streamlit_elements import elements, mui, html
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# CSS 스타일 추가
def add_custom_css():
    """사용자 정의 CSS 스타일을 추가합니다."""
    st.markdown("""
    <style>
        /* Intellytics AI Agent 메뉴 크기 조정 */
        [data-testid="stSidebarNav"] ul li:nth-child(2) > a {
            font-size: 1.4rem !important;
            font-weight: bold !important;
            padding: 1rem 0.5rem !important;
            color: #A50034 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            border-bottom: 2px solid #A50034 !important;
            margin-bottom: 0.5rem !important;
            display: block !important;
            text-align: center !important;
            background: linear-gradient(to right, rgba(165, 0, 52, 0.1), rgba(165, 0, 52, 0.2)) !important;
            border-radius: 5px !important;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1) !important;
            transition: all 0.3s ease !important;
        }
        
        /* 메뉴 호버 시 효과 강화 */
        [data-testid="stSidebarNav"] ul li:nth-child(2) > a:hover {
            background: linear-gradient(to right, rgba(165, 0, 52, 0.2), rgba(165, 0, 52, 0.3)) !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Intellytics AI Agent 하위 메뉴 스타일 */
        [data-testid="stSidebarNav"] ul li:nth-child(2) ul li a {
            font-size: 1rem !important;
            font-weight: normal !important;
            padding: 0.5rem 0.5rem 0.5rem 1.5rem !important;
            color: #333333 !important;
            text-transform: none !important;
            letter-spacing: normal !important;
            border-bottom: none !important;
            margin-bottom: 0 !important;
            text-align: left !important;
            background: none !important;
            box-shadow: none !important;
        }
        
        /* 메뉴 호버 효과 */
        [data-testid="stSidebarNav"] ul li:nth-child(2) ul li a:hover {
            background-color: rgba(165, 0, 52, 0.1) !important;
            transition: all 0.3s ease !important;
            transform: none !important;
        }
        
        /* 메뉴 활성화 효과 */
        [data-testid="stSidebarNav"] ul li a.active {
            background-color: rgba(165, 0, 52, 0.2) !important;
            border-left: 3px solid #A50034 !important;
        }
    </style>
    """, unsafe_allow_html=True)

# 세션 상태 초기화 함수
def initialize_session_state():
    """세션 상태를 초기화합니다."""
    # 로그인 상태 저장
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # NPS 확장 여부 저장
    if "nps_expanded" not in st.session_state:
        st.session_state.nps_expanded = False  

    # 이전 페이지와 현재 페이지 저장
    if "previous_page" not in st.session_state:
        st.session_state.previous_page = ""
    if "current_page" not in st.session_state:
        st.session_state.current_page = ""

# 로그인 함수
def login():
    """로그인 페이지를 표시하고 처리합니다."""
    st.title("로그인")
    st.write("서비스를 이용하려면 로그인이 필요합니다.")
    
    # 사용자 입력 필드 (실제 인증 로직은 구현되어 있지 않음)
    username = st.text_input("사용자 이름")
    password = st.text_input("비밀번호", type="password")
    
    if st.button("로그인"):
        try:
            # 여기에 실제 인증 로직을 구현할 수 있음
            # 예: API 호출, 데이터베이스 조회 등
            
            # 로그인 성공 처리
            st.session_state.logged_in = True
            st.success("로그인 성공!")
            st.rerun()
        except Exception as e:
            logger.error(f"로그인 중 오류 발생: {str(e)}")
            st.error(f"로그인 중 오류가 발생했습니다: {str(e)}")

# 로그아웃 함수
def logout():
    """로그아웃 페이지를 표시하고 처리합니다."""
    st.title("로그아웃")
    st.write("로그아웃 하시겠습니까?")
    
    if st.button("로그아웃"):
        try:
            # 로그아웃 처리
            st.session_state.logged_in = False
            
            # NPS 확장 상태 초기화
            if st.session_state.nps_expanded:
                st.session_state.nps_expanded = False
            
            st.success("로그아웃 되었습니다.")
            st.rerun()
        except Exception as e:
            logger.error(f"로그아웃 중 오류 발생: {str(e)}")
            st.error(f"로그아웃 중 오류가 발생했습니다: {str(e)}")

# NPS 메인 페이지
def nps_main():
    """NPS 메인 페이지를 표시합니다."""
    try:
        # NPS 메인 페이지 내용 표시
        st.title("NPS 메인 페이지")
        
        # NPS 페이지가 로드될 때 자동으로 하위 메뉴 확장
        if not st.session_state.nps_expanded:
            st.session_state.nps_expanded = True
            st.rerun()
    except Exception as e:
        logger.error(f"NPS 메인 페이지 로드 중 오류 발생: {str(e)}")
        st.error(f"페이지 로드 중 오류가 발생했습니다: {str(e)}")

# D2C 페이지
def d2c_main():
    """D2C 페이지를 표시합니다."""
    try:
        # D2C 페이지 내용
        st.title("D2C 페이지")
        
        # D2C 페이지가 로드될 때 NPS 하위 메뉴 축소
        if st.session_state.nps_expanded:
            st.session_state.nps_expanded = False
            st.rerun()
    except Exception as e:
        logger.error(f"D2C 페이지 로드 중 오류 발생: {str(e)}")
        st.error(f"페이지 로드 중 오류가 발생했습니다: {str(e)}")

# 메인 함수
def main():
    """애플리케이션의 메인 함수입니다."""
    # 페이지 설정 (가장 먼저 호출해야 함)
    st.set_page_config(
        page_title="Intellytics AI Agent",
        page_icon="📊",
        layout="wide"
    )
    
    # 세션 상태 초기화
    initialize_session_state()
    
    # 사용자 정의 CSS 추가
    add_custom_css()
    
    try:
        # # NPS 페이지 및 하위 페이지 설정
        # nps_page = st.Page(nps_main, title="NPS", default=True)
        
        # NPS 하위 페이지
        # nps_subpages = [
            # st.Page("service_page/service_template_main.py", title="NPS 분석 서비스"),
            # st.Page("service_page/nps_1.py", title="Intellytics VOC 서비스"),
            # st.Page("service_page/nps_3.py", title="서비스 Test")
        # ]
        
        # # D2C 페이지 설정
        # d2c_page = st.Page("service_page/d2c.py", title="D2C")
        
        # LLM 서비스 샘플 페이지 설정
        llm_service_sample_page = st.Page("service_page/llm_service_sample.py", title="LLM 서비스 샘플")
        
        if st.session_state.logged_in:
            # 상단 메뉴 구성
            top_level_pages = {
                "Account": [st.Page(logout, title="Log out", icon="")],
                "INTELLYTICS AI AGENT": [st.Page(nps_main, title="Intellytics AI AGENT MAIN", icon="", default=True)]
            }
            
            # # NPS가 확장되어 있으면 하위 메뉴 추가
            # if st.session_state.nps_expanded:
            #     top_level_pages["✨ INTELLYTICS AI AGENT ✨"].extend([
            #         st.Page("service_page/service_template_main.py", title="NPS 분석 서비스", icon=""),
            #         st.Page("service_page/nps_1.py", title="Intellytics VOC 서비스", icon=""),
            #         st.Page("service_page/nps_3.py", title="서비스 Test", icon="")
            #     ])
            # else:
            #     top_level_pages["✨ INTELLYTICS AI AGENT ✨"] = [st.Page(nps_main, title="NPS", icon="", default=True)]
            
            top_level_pages["INTELLYTICS AI AGENT"].append(st.Page("service_page/service_template_main.py", title="Intellytics NPS Agent", icon=""))
            top_level_pages["INTELLYTICS AI AGENT"].append(st.Page("service_page/service_voc.py", title="Intellytics VOC Agent", icon=""))
            top_level_pages["INTELLYTICS AI AGENT"].append(st.Page("service_page/service_d2c.py", title="Intellytics D2C Agent", icon=""))
            
            # # D2C 페이지는 항상 표시
            # top_level_pages["✨ INTELLYTICS AI AGENT ✨"].append(st.Page("service_page/d2c.py", title="Intellytics D2C Agent", icon=""))
            
            # LLM 서비스 샘플 페이지 추가
            top_level_pages["INTELLYTICS AI AGENT"].append(st.Page("service_page/llm_service_sample.py", title="LLM 서비스", icon=""))
            
            # 네비게이션 구성
            pg = st.navigation(top_level_pages)
        else:
            pg = st.navigation([st.Page(login, title="Log in", icon="")])
        
        # 페이지 실행
        pg.run()
        
    except Exception as e:
        logger.error(f"애플리케이션 실행 중 오류 발생: {str(e)}")
        st.error(f"애플리케이션 실행 중 오류가 발생했습니다: {str(e)}")
        st.error("페이지를 새로고침하거나 관리자에게 문의하세요.")

# 애플리케이션 실행
if __name__ == "__main__":
    main()
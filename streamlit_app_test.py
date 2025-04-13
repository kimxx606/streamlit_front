import streamlit as st
from streamlit_elements import elements, mui, html
from util.init_menu_session_state import initialize_menu_session_state
from util.common_util import (
    render_page_title, render_service_description, render_section_divider,
    render_card_container_start, render_card_container_end, render_feature_card,
    render_footer, render_error_message, add_home_link
)
from main_page.agent_main import agent_main
from main_page.d2c_main import d2c_main
from main_page.survey_main import survey_main
from main_page.mellerikat_main import mellerikat_main
from main_page.mellerisearch_main import mellerisearch_main
from main_page.b2bquery_main import b2bquery_main
from main_page.hrdx_main import hrdx_main
from main_page.nps_main import nps_main

# CSS 스타일 추가
def add_custom_css():
    """외부 CSS 파일을 로드합니다."""
    with open("style_main/style_main.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

##########################################
# 타이틀 설정
##########################################

first_title = ""
main_title = "" #"\u00A0\u00A0Project"
poc_title = "\u00A0\u00A0POC"
# 메인 함수
def main():
    """애플리케이션의 메인 함수입니다."""
    # 페이지 설정 (가장 먼저 호출해야 함)
    st.set_page_config(
        page_title="Intellytics AI Agent",
        page_icon=":material/network_intelligence:",
        layout="wide"
    )
    
    # 세션 상태 초기화
    initialize_menu_session_state()
    
    # 사용자 정의 CSS 추가
    add_custom_css()
    
    # 헤더에 홈 링크 기능 추가
    add_home_link()
    
    try:
        # 서비스별 메인 페이지
        main_page = st.Page(agent_main, title="Project", default=True)
        d2c_page = st.Page(d2c_main, title="\u00A0\u00A0\u00A0DX Automation for D2C")
        sg_page = st.Page(survey_main, title="\u00A0\u00A0\u00A0Survey Genius")
        # mellerikat_page = st.Page(mellerikat_main, title="Mellerikat Assistant")
        mellerisearch_page = st.Page(mellerisearch_main, title="\u00A0\u00A0\u00A0MelleriSearch")
        # b2bquery_page = st.Page(b2bquery_main, title="B2B Query")
        hrdx_page = st.Page(hrdx_main, title="\u00A0\u00A0\u00A0HR Analysis")
        nps_page = st.Page(nps_main, title="\u00A0\u00A0\u00A0DX Automation for NPS")
        
        chat_generation_main = st.Page(mellerikat_main, title="Intellytics AI Agent Tool")
        
        # 상단 메뉴 구성
        top_level_pages = {
            # first_title: [main_page],
            main_title: [main_page],
            poc_title: []
        }
        
        # 페이지 구성
        
        # =====================================================================================================
        # D2C 페이지 추가
        top_level_pages[main_title].append(d2c_page)
        # D2C 서브페이지 리스트
        d2c_subpages = [
            # st.Page("service_page/service_d2c_sales.py", title="D2C - Sales Status", icon=":material/stat_minus_2:"), # subdirectory_arrow_right # arrow_menu_open # stat_minus_2 # :material/stat_minus_2:
            st.Page("service_page/service_d2c_sales.py", title=" ▹D2C - Sales Status", icon=""), # ➤
            st.Page("service_page/service_d2c_fallout.py", title=" ▹D2C - Fallout Analysis", icon="")
        ]
        # # D2C 서브페이지 추가
        if st.session_state.d2c_expanded == True:
            top_level_pages[main_title].extend(d2c_subpages)
        # else:
        #     top_level_pages["INTELLYTICS AI AGENT"] = top_level_pages["INTELLYTICS AI AGENT"]
        
        # =====================================================================================================
        # # nps 페이지 추가
        # top_level_pages[main_title].append(st.Page("service_page/service_nps_analysis.py", title="\u00A0\u00A0\u00A0DX Automation for NPS"))
        # # top_level_pages[main_title].append(nps_page)

    
        # =====================================================================================================
        # b2b_query 페이지 추가
        top_level_pages[poc_title].append(st.Page("service_page/service_b2b_query.py", title="\u00A0\u00A0\u00A0B2B Query"))
        
        # top_level_pages["INTELLYTICS AI AGENT"].append(b2bquery_page)
        # # # Mellerikat 서브페이지 추가
        # b2bquery_subpages = [
        #     st.Page("service_page/service_b2b_query.py", title="\u00A0\u00A0B2B - Query")
        # ]
        # if st.session_state.b2bquery_expanded == True:
        #     top_level_pages["INTELLYTICS AI AGENT"].extend(b2bquery_subpages)
        # else:
        #     top_level_pages["INTELLYTICS AI AGENT"] = top_level_pages["INTELLYTICS AI AGENT"]
        
        
        # =====================================================================================================
        # chatbot_generation 페이지 추가
        top_level_pages[poc_title].append(st.Page("service_page/service_chatbot_generation.py", title="\u00A0\u00A0\u00A0DocuMentor"))

        # =====================================================================================================
        # HRDX 페이지 추가
        # top_level_pages[main_title].append(st.Page("service_page/service_hrdx.py", title="\u00A0\u00A0HRDX"))
        
        top_level_pages[poc_title].append(hrdx_page)
        # # Mellerikat 서브페이지 추가
        hrdx_subpages = [
            st.Page("service_page/service_hrdx_qna.py", title=" ▹HR Analysis - 업무요약", icon=""), # ➤
            st.Page("service_page/service_hrdx_recommand.py", title=" ▹HR Analysis - 교육추천", icon="")
        ]
        if st.session_state.hrdx_expanded == True:
            top_level_pages[poc_title].extend(hrdx_subpages)
        # else:
        #     top_level_pages["INTELLYTICS AI AGENT"] = top_level_pages["INTELLYTICS AI AGENT"]

        # =====================================================================================================
        # Mellerikat 페이지 추가
        top_level_pages[poc_title].append(st.Page("service_page/service_mellerikat_assistant.py", title="\u00A0\u00A0\u00A0MelleriAssistant"))
        
        # top_level_pages["INTELLYTICS AI AGENT"].append(mellerikat_page)
        # # # Mellerikat 서브페이지 추가
        # mellerikat_subpages = [
        #     st.Page("service_page/service_mellerikat_assistant.py", title="\u00A0\u00A0Mellerikat - Assistant")
        # ]
        # if st.session_state.mellerikat_expanded == True:
        #     top_level_pages["INTELLYTICS AI AGENT"].extend(mellerikat_subpages)
        # else:
        #     top_level_pages["INTELLYTICS AI AGENT"] = top_level_pages["INTELLYTICS AI AGENT"]
        
            
        # =====================================================================================================
        # Melleri search 페이지 추가
        # top_level_pages[main_title].append(st.Page("service_page/service_mellerisearch.py", title="MelleriSearch"))
        
        top_level_pages[poc_title].append(mellerisearch_page)
        # # Mellerikat 서브페이지 추가
        mellerisearch_subpages = [
            st.Page("service_page/service_mellerisearch_register.py", title=" ▹MS - Register", icon=""), # :material/stat_minus_2:
            st.Page("service_page/service_mellerisearch_search.py", title=" ▹MS - Search", icon="")
        ]
        if st.session_state.mellerisearch_expanded == True:
            top_level_pages[poc_title].extend(mellerisearch_subpages)
        # else:
        #     top_level_pages["INTELLYTICS AI AGENT"] = top_level_pages["INTELLYTICS AI AGENT"]
        
        # =====================================================================================================
        # Survey Genius 페이지 추가
        top_level_pages[poc_title].append(st.Page("service_page/service_sg_analysis.py", title="\u00A0\u00A0\u00A0Survey Analysis"))
        
        # top_level_pages[main_title].append(sg_page)
        # # # Survey Genius 서브페이지 추가
        # sg_subpages = [
        #     st.Page("service_page/service_sg_generation.py", title=" ▹Survey - Generation", icon=""),
        #     st.Page("service_page/service_sg_analysis.py", title=" ▹Survey - Analysis", icon="")
        # ]
        # if st.session_state.survey_expanded == True:
        #     top_level_pages[main_title].extend(sg_subpages)
        # # else:
        # #     top_level_pages["INTELLYTICS AI AGENT"] = top_level_pages["INTELLYTICS AI AGENT"]
        
        # =====================================================================================================
        # VOC Analysis 페이지 추가
        top_level_pages[poc_title].append(st.Page("service_page/service_voc_analysis.py", title="\u00A0\u00A0\u00A0VOC Analysis"))
        
        # =====================================================================================================
        # # Sync Note 페이지 추가
        # top_level_pages[main_title].append(st.Page("service_page/service_meeting_summary.py", title="\u00A0\u00A0\u00A0Meeting Note"))


        # # Chat Generation Page
        # top_level_pages[main_title].append(chat_generation_main)
        # top_level_pages[main_title].append(st.Page("service_page/service_your_chatbot.py", title="\u00A0\u00A0\u00A0Your Chatbot"))
    
        # 네비게이션 구성
        pg = st.navigation(top_level_pages)
 
        # 스타일 정보 추가 (비표시 요소로 마크업만 추가)
        st.markdown("""
        <style>
            /* 헤더의 SVG 아이콘 숨기기 */
            [data-testid="stHeader"] div[data-testid="stDecoration"] {
                display: none !important;
            }
            
            /* 사이드바 메뉴의 축소/확장 버튼 숨기기 */
            [data-testid="stSidebarCollapsedControl"],
            div[data-testid="stSidebarCollapsedControl"],
            div[class*="st-emotion-cache-ov61b"],
            div.st-emotion-cache-ov61b9,
            button[kind="secondary"][data-testid="collapsedControl"],
            .st-emotion-cache-ov61b9 {
                display: none !important;
                opacity: 0 !important;
                visibility: hidden !important;
                width: 0 !important;
                height: 0 !important;
                margin: 0 !important;
                padding: 0 !important;
                position: absolute !important;
                pointer-events: none !important;
            }
            
            /* 사이드바 너비 조정 - 축소 버튼이 사라졌기 때문에 너비 조정 */
            [data-testid="stSidebar"] {
                min-width: 14rem !important;
            }
            
            /* Project 메뉴 항목 클릭 및 호버 효과 비활성화 */
            [data-testid="stSidebarNav"] ul li:first-child a,
            [data-testid="stSidebarNav"] ul li a[href*="Project"] {
                pointer-events: none !important;
                cursor: default !important;
                color: #000 !important;
                opacity: 1.0 !important;
                text-decoration: none !important;
                background: none !important;
                box-shadow: none !important;
                transform: none !important;
                transition: none !important;
            } 
            
            /* 메뉴 호버 효과 제거 - Project 메뉴 항목만 */
            [data-testid="stSidebarNav"] ul li:first-child a:hover,
            [data-testid="stSidebarNav"] ul li a[href*="Project"]:hover {
                background: none !important;
                color: #666 !important;
                transform: none !important;
                box-shadow: none !important;
            }
            
            /* Project 메뉴 활성화 효과 제거 */
            [data-testid="stSidebarNav"] ul li:first-child a.active,
            [data-testid="stSidebarNav"] ul li a[href*="Project"].active {
                background: none !important;
                color: #666 !important;
                transform: none !important;
                box-shadow: none !important;
                font-weight: normal !important;
            }
            
            /* 활성화된 메뉴 항목 스타일 개선 */
            /* [data-testid="stSidebarNav"] ul li a.active {
                background-color: rgba(0, 0, 255, 0.25) !important;
                font-weight: 500 !important;
                color: #A50034 !important;
                border-radius: 4px !important;
                transform: translateX(5px) !important;
                padding-left: 12px !important;
            } */
            [data-testid="stSidebarNav"] ul li a.active {
                background-color: rgba(165, 0, 52, 0.2) !important;
                color: #A50034 !important;
            }

            
            /* 하위 메뉴에서 활성화된 항목 특별 스타일 */
            [data-testid="stSidebarNav"] ul li ul li a.active {
                background-color: rgba(0, 0, 255, 0.35) !important;
                font-weight: 500 !important;
                color: #A50034 !important;
                transform: translateX(8px) !important;
                padding-left: 14px !important;
            }
            
            /* 비활성화된 메뉴 항목 스타일 */
            [data-testid="stSidebarNav"] ul li a:not(.active):not([href*="Project"]) {
                background: none !important;
                font-weight: 400 !important;
                color: #262730 !important;
            }
            
            /* 일반 메뉴 항목의 호버 효과 */
            [data-testid="stSidebarNav"] ul li a:not([href*="Project"]):hover {
                background-color: rgba(55, 55, 55, 0.25) !important;
                color: #A50034 !important;
                transform: translateX(5px) !important;
                transition: all 0.2s ease !important;
                font-weight: 500 !important;
                padding-left: 12px !important;
            }
        </style>
        
        <iframe srcdoc="
        <script>
            // Project 메뉴 항목 클릭 비활성화
            window.addEventListener('load', function() {
                setTimeout(function() {
                    // 모든 사이드바 링크 확인
                    const links = window.parent.document.querySelectorAll('[data-testid=\\'stSidebarNav\\'] ul li a');
                    for (let i = 0; i < links.length; i++) {
                        const link = links[i];
                        // Project 텍스트를 포함하는 링크 찾기
                        if (link.textContent.includes('Project')) {
                            // 클릭 이벤트 방지
                            link.onclick = function(e) {
                                e.preventDefault();
                                e.stopPropagation();
                                return false;
                            };
                            // 추가 스타일링
                            link.style.pointerEvents = 'none';
                            link.style.cursor = 'default';
                            link.style.color = '#666';
                            link.style.opacity = '0.7';
                            link.style.textDecoration = 'none';
                            link.style.background = 'none';
                            link.style.boxShadow = 'none';
                            link.style.transform = 'none';
                        }
                    }
                }, 1000);
            });
        </script>
        " style="display:none;"></iframe>
        """, unsafe_allow_html=True)
        
        # 페이지 실행
        pg.run()
        
    except Exception as e:
        # 향상된 오류 메시지 UI
        st.markdown(f"""
        <div class="error-container">
            <h2 class="error-title">애플리케이션 오류</h2>
            <p class="error-message">애플리케이션 실행 중 예기치 않은 오류가 발생했습니다. 잠시 후 다시 시도하거나 관리자에게 문의해주세요.</p>
            <details>
                <summary>기술적 세부사항</summary>
                <code style="display:block; padding:10px; background-color:#f8f8f8; border-radius:5px; margin-top:10px; white-space:pre-wrap;">
                {str(e)}
                </code>
            </details>
            <a href="/" class="error-action">새로고침</a>
        </div>
        """, unsafe_allow_html=True)

# 애플리케이션 실행
if __name__ == "__main__":
    main()
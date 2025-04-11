import streamlit as st
from streamlit_elements import elements, mui, html

# CSS 스타일 추가
def add_custom_css():
    """외부 CSS 파일을 로드합니다."""
    with open("style_main/style_main.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 세션 상태 초기화 함수
def initialize_session_state():
    """세션 상태를 초기화합니다."""
    # D2C 확장 여부 저장
    if "d2c_expanded" not in st.session_state:
        st.session_state.d2c_expanded = False
    # Survey Genius 확장 여부 저장
    if "survey_expanded" not in st.session_state:
        st.session_state.survey_expanded = False
    # mellerisearch 확장 여부 저장
    if "mellerisearch_expanded" not in st.session_state:
        st.session_state.mellerisearch_expanded = False
    # hrdx 확장 여부 저장
    if "hrdx_expanded" not in st.session_state:
        st.session_state.hrdx_expanded = False

# 공통 HTML 함수들
def render_page_title(title, subtitle):
    """페이지 타이틀과 부제목을 렌더링합니다."""
    st.markdown(f"""
    <div class="title-container">
        <h1 class="main-title-special">{title}</h1>
    </div>
    <p class="subtitle">{subtitle}</p>
    """, unsafe_allow_html=True)

def render_service_description(description):
    """서비스 설명을 렌더링합니다."""
    st.markdown(f"""
    <div class='service-description-special'>
        <div class="description-content">
            <h3>서비스 개요</h3>
            <p>{description}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_section_divider(title="주요 기능"):
    """섹션 구분선을 렌더링합니다."""
    st.markdown(f"<div class='section-divider'><span>{title}</span></div>", unsafe_allow_html=True)

def render_card_container_start():
    """카드 컨테이너 시작 태그를 렌더링합니다."""
    st.markdown("<div class='card-container'>", unsafe_allow_html=True)

def render_card_container_end():
    """카드 컨테이너 종료 태그를 렌더링합니다."""
    st.markdown("</div>", unsafe_allow_html=True)

def render_feature_card(title, features):
    """기능 카드를 렌더링합니다."""
    features_html = ""
    for feature in features:
        features_html += f"<li>{feature}</li>\n"
    
    card_html = f"""
    <div class='card'>
        <div class='card-content'>
            <h3>{title}</h3>
            <ul>{features_html}</ul>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def render_footer(team="DX센터 AI빅데이터담당"):
    """페이지 푸터를 렌더링합니다."""
    st.markdown(f"""
    <div class='footer-info'>
        <p>© 2025 Intellytics AI Agent | 버전 1.0.0 | {team}</p>
    </div>
    """, unsafe_allow_html=True)

def render_error_message(title="페이지 로드 오류", message="페이지를 로드하는 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요."):
    """오류 메시지를 렌더링합니다."""
    st.markdown(f"""
    <div class="error-container">
        <h2 class="error-title">{title}</h2>
        <p class="error-message">{message}</p>
        <button class="error-action" onclick="window.location.reload()">페이지 새로고침</button>
    </div>
    """, unsafe_allow_html=True)

# AI Agent 메인 페이지
def agent_main():
    """Intellytics AI Agent 메인 페이지를 표시합니다."""
    try:
        # 타이틀과 부제목 렌더링
        render_page_title("Intellytics AI Agent", "LLM 서비스 테스트 및 검증 플랫폼")
        
        # 서비스 설명 렌더링
        render_service_description(
            "이 프론트엔드는 DX센터 AI빅데이터담당에서 개발되는 다양한 LLM 서비스 API를 테스트하고 검증하기 위한 용도로 제작되었습니다. "
            "현재 개발 중인 테스트 및 데모 목적의 내부 검증용 도구이며, 최종 사용자 배포용이 아닙니다."
        )
        
        # 섹션 구분자 렌더링
        render_section_divider("서비스 가이드")
        
        # 카드 컨테이너 시작
        render_card_container_start()
        
        # 사용 방법 카드
        st.markdown("""
        <div class='card' id='usage-card'>
            <div class='card-content'>
                <h3>사용 방법</h3>
                <ol>
                    <li>좌측 사이드바에서 원하는 서비스를 선택합니다.</li>
                    <li>선택한 서비스의 테스트 화면으로 이동하여 사용자 질문을 입력합니다.</li>
                    <li>전송하기 버튼을 눌러 해당 서비스의 API 요청을 실행합니다.</li>
                    <li>결과를 확인하고 필요한 피드백을 제공합니다.</li>
                </ol>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 주의 사항 카드
        st.markdown("""
        <div class='card' id='warning-card'>
            <div class='card-content'>
                <h3>주의 사항</h3>
                <ul>
                    <li>본 프론트엔드는 내부 검증용으로만 사용됩니다.</li>
                    <li>테스트 중 발생하는 오류 및 서비스 응답 시간을 점검하며, 피드백을 남겨 주세요.</li>
                    <li>API 연결 상태는 변경될 수 있으며, 일부 기능이 제한될 수 있습니다.</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 카드 컨테이너 종료
        render_card_container_end()
    
        # 푸터 렌더링
        render_footer()
        
        # MAIN 페이지가 로드될 때 D2C 하위 메뉴 축소
        if (st.session_state.d2c_expanded == True) or (st.session_state.mellerisearch_expanded == True) or (st.session_state.survey_expanded == True) or (st.session_state.hrdx_expanded == True):
            st.session_state.d2c_expanded = False
            st.session_state.survey_expanded = False
            st.session_state.mellerisearch_expanded = False
            st.session_state.hrdx_expanded = False
            st.rerun()
        
    except Exception as e:
        # 오류 메시지 렌더링
        render_error_message("main 페이지 로드 오류", "메인 페이지를 로드하는 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요.")

# D2C 페이지
def d2c_main():
    # """D2C 페이지를 표시합니다."""
    try:
        # 타이틀과 부제목 렌더링
        render_page_title("DX Automation for D2C", "D2C 매출 현황 및 원인 분석 도구")
        
        # 서비스 설명 렌더링
        render_service_description(
            "해외법인에서 운영하는 OBS (Online Brand Shop)에서 수집되는 매출 및 고객웹행동 데이터를 기반으로 "
            "매출현황과 판매량을 법인전체/제품군/모델 단위로 파악하고, 매출하락 등의 이슈에 대한 원인을 OBS Funnel 단계 "
            "및 OBS 유입 채널 관점에서 파악하고 해결방안을 제시합니다."
        )

        # 섹션 구분자 렌더링
        render_section_divider()
        
        # 카드 컨테이너 시작
        render_card_container_start()
        
        # Sales Status 카드
        render_feature_card("Sales Status", [
            "법인전체 매출현황/판매량 파악",
            "제품군별 매출현황/판매량 파악",
            "모델별 매출현황/판매량 파악",
            "기간 단위(일, 주, 월, 년)별 집계 및 비교"
        ])
        
        # Fallout Analysis 카드
        render_feature_card("Fallout Analysis", [
            "OBS Funnel 단계 관점 원인 분석",
            "OBS 유입 채널 관점 원인 분석",
            "주요 원인 별 해결방안 제시"
        ])
        
        # 카드 컨테이너 종료
        render_card_container_end()
        
        # 푸터 렌더링
        render_footer("DX센터 AI빅데이터담당 AX기술팀")
        
        # D2C 페이지가 로드될 때 D2C 하위 메뉴 확장
        if st.session_state.d2c_expanded == False:
            st.session_state.d2c_expanded = True
            st.session_state.survey_expanded = False
            st.session_state.mellerisearch_expanded = False
            st.session_state.hrdx_expanded = False
            st.rerun()
        
    except Exception as e:
        # 오류 메시지 렌더링
        render_error_message("d2c 페이지 로드 오류", "D2C 분석 페이지를 로드하는 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요.")

def survey_main():
    # survery genius 메인 페이지 내용 표시
    try:
        # 타이틀과 부제목 렌더링
        render_page_title("Survey Genius", "설문 생성 자동화 및 결과 분석 도구")
        
        # 서비스 설명 렌더링
        render_service_description(
            """
            Survey Genius는 사내 구성원들의 요청에 맞는 설문을 쉽고 간단하게 생성하고, 설문 결과를 분석할 수 있는 도구를 제공하는 서비스입니다.<br>
            설문의 타겟과 목적을 고려하여 사용자가 형식과 개수에 맞는 설문을 자동 생성하고, 설문 결과를 분석하여 차별화된 인사이트를 제공합니다.
            """
        )

        # 섹션 구분자 렌더링
        render_section_divider()
        
        # 카드 컨테이너 시작
        render_card_container_start()
        
        # 설문 생성 카드
        render_feature_card("설문 생성", [
            "타겟/목적에 따른 설문 생성",
            "객관식/주관식 문항 개수 설정",
            "응답 척도 및 선택지 개수 조정"
        ])
        
        # 결과 분석 카드
        render_feature_card("결과 분석", [
            "감성 분석",
            "키워드 분석",
            "키워드별 응답 유형 분석"
        ])
        
        # 카드 컨테이너 종료
        render_card_container_end()
        
        # 푸터 렌더링
        render_footer("DX센터 AI빅데이터담당 오퍼레이션AX기술팀")
        
        # # SG 페이지가 로드될 때 SG 하위 메뉴 확장
        if st.session_state.survey_expanded == False:
            st.session_state.d2c_expanded = False
        #     st.session_state.sg_expanded = False
            st.session_state.survey_expanded = True
        #     st.session_state.mellerikat_expanded = False
            st.session_state.mellerisearch_expanded = False
        #     st.session_state.b2bquery_expanded = False
            st.session_state.hrdx_expanded = False
            
            st.rerun()
        
    except Exception as e:
        # 오류 메시지 렌더링
        render_error_message("nps 페이지 로드 오류", "D2C 분석 페이지를 로드하는 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요.")

def mellerikat_main():
    # mellerikat 메인 페이지 내용 표시
    try:
        # 타이틀과 부제목 렌더링
        render_page_title("Try Mellerikat", "Mellerikat 제품 이해 및 사용자 질의응답 지원 챗봇 시스템")
        
        # 서비스 설명 렌더링
        render_service_description(
            "Try Mellerikat은 Mellerikat 제품을 처음 접하는 사람들이 제품을 쉽게 이해할 수 있도록 돕고, 실제 사용자들이 제품 사용 중 궁금한 점을 해결할 수 있는 질의응답 기능을 제공하는 서비스입니다. "
            "직관적인 설명과 사용자 맞춤형 답변을 통해 제품의 특징과 사용 방법을 안내하며, 원활한 제품 경험을 지원합니다."
        )

        # 섹션 구분자 렌더링
        render_section_divider()
        
        # 카드 컨테이너 시작
        render_card_container_start()
        
        # 질의 응답 카드
        render_feature_card("질의 응답", [
            "사용자의 질문에 실시간 답변 제공",
            "Mellerikat 제품의 핵심 특징 및 사용 방법 안내",
            "자주 묻는 질문(FAQ)를 활용한 빠른 자동 응답"
        ])
        
        # 카드 컨테이너 종료
        render_card_container_end()
        
        # 푸터 렌더링
        render_footer("DX센터 AI빅데이터담당 AX기술팀")
        
        # MAIN 페이지가 로드될 때 D2C 하위 메뉴 축소
        if (st.session_state.d2c_expanded == True) or (st.session_state.mellerisearch_expanded == True) or (st.session_state.survey_expanded == True) or (st.session_state.hrdx_expanded == True):
            st.session_state.d2c_expanded = False
            st.session_state.survey_expanded = False
            st.session_state.mellerisearch_expanded = False
            st.session_state.hrdx_expanded = False
            st.rerun()
        
        
        # # Mellerikat 페이지가 로드될 때 Mellerikat 하위 메뉴 확장
        # if st.session_state.mellerikat_expanded == False:
        #     st.session_state.d2c_expanded = False
        #     st.session_state.sg_expanded = False
        #     st.session_state.survey_expanded = False
        #     st.session_state.mellerikat_expanded = True
        #     st.session_state.mellerisearch_expanded = False
        #     st.session_state.b2bquery_expanded = False
        #     st.session_state.hrdx_expanded = False
            
        #     st.rerun()
        
    except Exception as e:
        # 오류 메시지 렌더링
        render_error_message("페이지 로드 오류", "페이지를 로드하는 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요.")

def mellerisearch_main():
    # mellerisearch 메인 페이지 내용 표시
    try:
        # 타이틀과 부제목 렌더링
        render_page_title("MelleriSearch", "AI Solution 등록과 탐색 및 추천 도구")
        
        # 서비스 설명 렌더링
        render_service_description(
            "사용자의 AI Solution을 Git을 기반으로 AI Solution Database에 저장합니다. 또한 검색을 통해 Mellerikat에서 운영 가능한 검증된 AI 솔루션을 조회할 수 있습니다. "
            "AI로 해결하고 싶은 과제에 대해 설명을 주시면 적합한 Solution을 찾을 수 있는 추천 도구를 제공합니다."
        )

        # 섹션 구분자 렌더링
        render_section_divider()
        
        # 카드 컨테이너 시작
        render_card_container_start()
        
        # AI Solution 메타 문서 등록 카드
        render_feature_card("AI Solution 메타 문서 등록", [
            "AI Solution의 Git 주소를 참조하여, LLM을 이용한 Guide 생성",
            "AI Solution 메타 정보를 DB에 적재"
        ])
        
        # AI Solution 탐색 및 추천 카드
        render_feature_card("AI Solution 탐색 및 추천", [
            "유저의 요청에 따른 AI Solution 탐색",
            "유저의 요청에 따른 AI Solution 추천",
            "추천된 AI Solution에 대한 Q&A"
        ])
        
        # 카드 컨테이너 종료
        render_card_container_end()
        
        # 이미지 표시
        # st.image("service_page/images/Home1.PNG")
        # st.image("service_page/images/Home2.PNG")
        
        # 푸터 렌더링
        render_footer("DX센터 AI빅데이터담당 AX선행기술Task")
        
        # # NPS 페이지가 로드될 때 NPS 하위 메뉴 확장
        if st.session_state.mellerisearch_expanded == False:
            st.session_state.d2c_expanded = False
            st.session_state.survey_expanded = False
            st.session_state.mellerisearch_expanded = True
            st.session_state.hrdx_expanded = False
            st.rerun()
        
    except Exception as e:
        # 오류 메시지 렌더링
        render_error_message("페이지 로드 오류", "페이지를 로드하는 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요.")

def b2bquery_main():
    # B2B 메인 페이지 내용 표시
    try:
        # 타이틀과 부제목 렌더링
        render_page_title("B2B", "B2B 데이터베이스 자연어 탐색/질의 도구")
        
        # 서비스 설명 렌더링
        render_service_description(
            "B2B – Query 는 B2B 데이터베이스를 자연어로 탐색하고, 사용자의 질문에 대해 Domain Specific AI Model 결과를 반영한 응답을 생성해주는 서비스입니다."
        )

        # 섹션 구분자 렌더링
        render_section_divider()
        
        # 카드 컨테이너 시작
        render_card_container_start()
        
        # 자연어 DB 탐색 카드
        render_feature_card("자연어 DB 탐색", [
            "리드 현황 파악",
            "원하는 조건에 해당하는 리드 정보 확인",
            "특정 조건을 만족하는 리드에 대한 통계량 확인"
        ])
        
        # Domain Specific AI Model 결과 확인 카드
        render_feature_card("Domain Specific AI Model 결과 확인", [
            "기회전환지수를 기준으로 원하는 리드 탐색",
            "기회전환지수에 대한 설명 제공"
        ])
        
        # 카드 컨테이너 종료
        render_card_container_end()
        
        # 푸터 렌더링
        render_footer("DX센터 AI빅데이터담당 AX기술팀")
        
        # # B2B 페이지가 로드될 때 하위 메뉴 확장
        # if st.session_state.b2bquery_expanded == False:
        #     st.session_state.d2c_expanded = False
        #     st.session_state.sg_expanded = False
        #     st.session_state.survey_expanded = False
        #     st.session_state.mellerikat_expanded = False
        #     st.session_state.mellerisearch_expanded = False
        #     st.session_state.b2bquery_expanded = True
        #     st.session_state.hrdx_expanded = False
            
        #     st.rerun()
        
    except Exception as e:
        # 오류 메시지 렌더링
        render_error_message("페이지 로드 오류", "페이지를 로드하는 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요.")

def hrdx_main():
    # HRDX 메인 페이지 내용 표시
    try:
        # 타이틀과 부제목 렌더링
        render_page_title("HRDX", "HR 질의 및 교육 추천 서비스")
        
        # 서비스 설명 렌더링
        render_service_description(
            "HR portal, EC 등에 산재한 나의 HR데이터를 종합해 경력, 강점/보완점, 소속 부서 핵심업무 등을 찾아볼 수 있는 개인 HR데이터 검색 서비스 API로서, 이를 이용해 더욱 고도의 HR서비스를 구현할 수 있습니다."
        )

        # 섹션 구분자 렌더링
        render_section_divider()
        
        # 카드 컨테이너 시작
        render_card_container_start()
        
        # 질의 응답 카드
        render_feature_card("HRDX 질의", [
            "개인 업무 경험 요약",
            "개인 업무 성과 요약"
        ])
        
        render_feature_card("HRDX 교육 추천", [
            "업무 경험 기반 교육 추천"
        ])
        
        # 카드 컨테이너 종료
        render_card_container_end()
        
        # 푸터 렌더링
        render_footer("DX센터 AI빅데이터담당 AX기술팀")
        
        # # NPS 페이지가 로드될 때 NPS 하위 메뉴 확장
        if st.session_state.hrdx_expanded == False:
            st.session_state.d2c_expanded = False
            # st.session_state.sg_expanded = False
            st.session_state.survey_expanded = False
        #     st.session_state.mellerikat_expanded = False
            st.session_state.mellerisearch_expanded = False
        #     st.session_state.b2bquery_expanded = False
            st.session_state.hrdx_expanded = True
            
            st.rerun()
        
    except Exception as e:
        # 오류 메시지 렌더링
        render_error_message("페이지 로드 오류", "페이지를 로드하는 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요.")

# main_title = "Case Study"
# logic_title = "Logic"
main_title = ""
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
    initialize_session_state()
    
    # 사용자 정의 CSS 추가
    add_custom_css()
    
    try:
        # 서비스별 메인 페이지
        main_page = st.Page(agent_main, title="Intellytics AI Agent Service", default=True)
        d2c_page = st.Page(d2c_main, title="\u00A0\u00A0\u00A0DX Automation for D2C")
        sg_page = st.Page(survey_main, title="\u00A0\u00A0\u00A0Survey Genius")
        # mellerikat_page = st.Page(mellerikat_main, title="Mellerikat Assistant")
        mellerisearch_page = st.Page(mellerisearch_main, title="\u00A0\u00A0\u00A0MelleriSearch")
        # b2bquery_page = st.Page(b2bquery_main, title="B2B Query")
        hrdx_page = st.Page(hrdx_main, title="\u00A0\u00A0\u00A0HRDX")
        
        chat_generation_main = st.Page(mellerikat_main, title="Intellytics AI Agent Tool")
        
        # 상단 메뉴 구성
        top_level_pages = {
            main_title: [main_page]
        }
        
        # 페이지 구성
        # =====================================================================================================
        # b2b_query 페이지 추가
        top_level_pages[main_title].append(st.Page("service_page/service_b2b_query.py", title="\u00A0\u00A0\u00A0B2B Query"))
        
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
        
        top_level_pages[main_title].append(st.Page("service_page/service_chatbot_generation.py", title="\u00A0\u00A0\u00A0Chatbot Generation"))
        
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
        # HRDX 페이지 추가
        # top_level_pages[main_title].append(st.Page("service_page/service_hrdx.py", title="\u00A0\u00A0HRDX"))
        
        top_level_pages[main_title].append(hrdx_page)
        # # Mellerikat 서브페이지 추가
        hrdx_subpages = [
            st.Page("service_page/service_hrdx_qna.py", title=" ▹HRDX - 질의", icon=""), # ➤
            st.Page("service_page/service_hrdx_recommand.py", title=" ▹HRDX - 교육추천", icon="")
        ]
        if st.session_state.hrdx_expanded == True:
            top_level_pages[main_title].extend(hrdx_subpages)
        # else:
        #     top_level_pages["INTELLYTICS AI AGENT"] = top_level_pages["INTELLYTICS AI AGENT"]

        # =====================================================================================================
        # Mellerikat 페이지 추가
        top_level_pages[main_title].append(st.Page("service_page/service_mellerikat_assistant.py", title="\u00A0\u00A0\u00A0MelleriAssistant"))
        
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
        
        top_level_pages[main_title].append(mellerisearch_page)
        # # Mellerikat 서브페이지 추가
        mellerisearch_subpages = [
            st.Page("service_page/service_mellerisearch_register.py", title=" ▹MS - Register", icon=""), # :material/stat_minus_2:
            st.Page("service_page/service_mellerisearch_search.py", title=" ▹MS - Search", icon="")
        ]
        if st.session_state.mellerisearch_expanded == True:
            top_level_pages[main_title].extend(mellerisearch_subpages)
        # else:
        #     top_level_pages["INTELLYTICS AI AGENT"] = top_level_pages["INTELLYTICS AI AGENT"]
        
        # =====================================================================================================
        # Survey Genius 페이지 추가
        # top_level_pages[main_title].append(st.Page("service_page/service_sg_generation.py", title="\u00A0\u00A0Survey Genius"))
        
        top_level_pages[main_title].append(sg_page)
        # # Survey Genius 서브페이지 추가
        sg_subpages = [
            st.Page("service_page/service_sg_generation.py", title=" ▹Survey - Generation", icon=""),
            st.Page("service_page/service_sg_analysis.py", title=" ▹Survey - Analysis", icon="")
        ]
        if st.session_state.survey_expanded == True:
            top_level_pages[main_title].extend(sg_subpages)
        # else:
        #     top_level_pages["INTELLYTICS AI AGENT"] = top_level_pages["INTELLYTICS AI AGENT"]
        
        # =====================================================================================================
        # VOC Analysis 페이지 추가
        top_level_pages[main_title].append(st.Page("service_page/service_voc_analysis.py", title="\u00A0\u00A0\u00A0VOC Analysis"))
        
        # =====================================================================================================
        # # Sync Note 페이지 추가
        # top_level_pages[main_title].append(st.Page("service_page/service_meeting_summary.py", title="\u00A0\u00A0\u00A0Meeting Note"))


        # Chat Generation Page
        top_level_pages[main_title].append(chat_generation_main)
        top_level_pages[main_title].append(st.Page("service_page/service_your_chatbot.py", title="\u00A0\u00A0\u00A0Your Chatbot"))
        

        # 네비게이션 구성
        pg = st.navigation(top_level_pages)
 

        
        # 스타일 정보 추가 (비표시 요소로 마크업만 추가)
        st.markdown("""
        <div style="display:none">
            <div class="intellytics-branding">
                <div class="intellytics-version">v1.0.0</div>
            </div>
        </div>
        
        <style>
            /* 향상된 페이지 네비게이션 스타일 추가 */
            [data-testid="stSidebarNav"] ul li:nth-child(2) ul {
                margin-top: 1rem !important;
                border-radius: 8px !important;
                padding: 0.5rem !important;
                background-color: rgba(245, 245, 245, 0.7) !important;
            }
            
            /* 현재 선택된 메뉴 강조 효과 */
            [data-testid="stSidebarNav"] ul li a.active {
                font-weight: 1600 !important;
                transform: scale(1.02) !important;
            }
        </style>
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
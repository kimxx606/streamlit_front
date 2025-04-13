import streamlit as st
from util.common_util import (
    render_page_title, render_service_description, render_section_divider,
    render_card_container_start, render_card_container_end, render_footer, render_error_message
)

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
        
        # 서비스 등록 현황 카드
        st.markdown("""
        <div class='card' id='warning-card'>
            <div class='card-content'>
                <h3>서비스 등록 현황</h3>
                <ul>
                    <li>최초 서비스 등록: B2B Qeury, DX Automation for D2C, HRDX, MelleriAssistant, MelleriSearch, Survey Genius</li>
                    <li>2025.04.10 VOC Analaysis</li>
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

import streamlit as st
from util.common_util import (
    render_page_title, render_service_description, render_section_divider,
    render_card_container_start, render_card_container_end, render_feature_card,
    render_footer, render_error_message
)

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
        
    except Exception as e:
        # 오류 메시지 렌더링
        render_error_message("페이지 로드 오류", "페이지를 로드하는 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요.") 
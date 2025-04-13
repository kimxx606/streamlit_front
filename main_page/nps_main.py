import streamlit as st
from util.common_util import (
    render_page_title, render_service_description, render_section_divider,
    render_card_container_start, render_card_container_end, render_feature_card,
    render_footer, render_error_message
)

def nps_main():
    # survery genius 메인 페이지 내용 표시
    try:
        # 타이틀과 부제목 렌더링
        render_page_title("DX Automation for NPS", "설문 생성 자동화 및 결과 분석 도구")
        
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
        render_error_message("nps 페이지 로드 오류", "D2C 분석 페이지를 로드하는 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요.")

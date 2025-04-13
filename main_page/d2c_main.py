import streamlit as st
from util.common_util import (
    render_page_title, render_service_description, render_section_divider,
    render_card_container_start, render_card_container_end, render_feature_card,
    render_footer, render_error_message
)

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
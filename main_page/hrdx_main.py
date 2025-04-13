import streamlit as st
from util.common_util import (
    render_page_title, render_service_description, render_section_divider,
    render_card_container_start, render_card_container_end, render_feature_card,
    render_footer, render_error_message
)

def hrdx_main():
    # HRDX 메인 페이지 내용 표시
    try:
        # 타이틀과 부제목 렌더링
        render_page_title("HR Analysis", "HR 질의 및 교육 추천 서비스")
        
        # 서비스 설명 렌더링
        render_service_description(
            "HR portal, EC 등에 산재한 나의 HR데이터를 종합해 경력, 강점/보완점, 소속 부서 핵심업무 등을 찾아볼 수 있는 개인 HR데이터 검색 서비스 API로서, 이를 이용해 더욱 고도의 HR서비스를 구현할 수 있습니다."
        )

        # 섹션 구분자 렌더링
        render_section_divider()
        
        # 카드 컨테이너 시작
        render_card_container_start()
        
        # 질의 응답 카드
        render_feature_card("HR Analysis - 업무요약", [
            "개인 업무 경험 요약",
            "개인 업무 성과 요약"
        ])
        
        render_feature_card("HR Analysis - 교육추천천", [
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

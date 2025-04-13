import streamlit as st
from util.common_util import (
    render_page_title, render_service_description, render_section_divider,
    render_card_container_start, render_card_container_end, render_feature_card,
    render_footer, render_error_message
)

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
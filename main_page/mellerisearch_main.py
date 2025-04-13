import streamlit as st
from util.common_util import (
    render_page_title, render_service_description, render_section_divider,
    render_card_container_start, render_card_container_end, render_feature_card,
    render_footer, render_error_message
)

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
        st.image("service_page/images/Home1.PNG")
        st.image("service_page/images/Home2.PNG")
        
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

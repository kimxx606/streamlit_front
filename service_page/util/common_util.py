import streamlit as st

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

def add_home_link():
    """헤더에 홈 링크 기능을 추가합니다."""
    st.markdown("""
    <div class="home-link" onclick="window.location.href='/'"></div>
    <iframe class="home-button-script" srcdoc="
        <script>
            // 헤더 텍스트 클릭 이벤트 추가
            window.addEventListener('load', function() {
                setTimeout(function() {
                    const header = window.parent.document.querySelector('[data-testid=\\'stHeader\\']');
                    if (header) {
                        header.addEventListener('click', function(e) {
                            // 헤더 왼쪽 영역 클릭 감지
                            if (e.clientX < 200) {
                                window.parent.location.href = '/';
                            }
                        });
                    }
                }, 1000);
            });
        </script>
    "></iframe>
    """, unsafe_allow_html=True) 
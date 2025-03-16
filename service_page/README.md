# Streamlit 서비스 페이지 개발 가이드

이 가이드는 `service_template_main.py`를 기반으로 새로운 Streamlit 서비스 페이지를 개발하고자 하는 개발자를 위한 문서입니다. 템플릿을 활용하여 자신만의 AI 기반 대화형 서비스를 쉽게 구현할 수 있습니다.

## 1. 템플릿 구조 이해하기

`service_template_main.py` 파일은 크게 다음과 같은 섹션으로 구성되어 있습니다:

1. **서비스 ID 및 세션 상태 초기화**
2. **서비스 커스터마이징 영역**
3. **UI 구성 요소 (사이드바, 메인 화면)**
4. **API 통신 함수**
5. **사용자 입력 처리 로직**
6. **JavaScript 및 CSS 스타일링**

## 2. 새 서비스 페이지 만들기

### 2.1 기본 설정

1. `service_template_main.py`를 복사하여 새 파일명으로 저장합니다 (예: `service_my_service.py`).
2. 서비스 ID를 변경합니다:
   ```python
   # 서비스 ID (세션 상태 키 접두사로 사용)
   SERVICE_ID = "my_service"  # 고유한 ID로 변경
   ```

### 2.2 서비스 정보 커스터마이징

서비스 커스터마이징 영역에서 다음 항목을 수정합니다:

```python
# 서비스 기본 정보
SERVICE_NAME = "내 서비스 이름"
SERVICE_DESCRIPTION = """
여기에 서비스에 대한 설명을 작성합니다.
여러 줄로 작성할 수 있습니다.
"""

# 대표 질문 리스트
SAMPLE_QUESTIONS = [
    "첫 번째 대표 질문은 무엇인가요?",
    "두 번째 대표 질문은 어떤 것이 좋을까요?",
    "세 번째 질문은 어떻게 작성하면 좋을까요?"
]

# 기본 API 엔드포인트
api_endpoint = os.environ.get("API 엔드포인트", "http://localhost:8081/your_service_endpoint")

# 사이드바 정보
SIDEBAR_SEARCHING_GUIDE = """
여기에 사이드바에 표시할 안내 정보를 작성합니다.<br>
**HTML 태그를 사용할 수 있습니다**
"""
```

## 3. API 통신 함수 수정하기

서비스에 맞게 API 통신 함수를 수정합니다:

```python
def ask_llm_api(query, endpoint):
    try:
        # 필요에 따라 요청 데이터 구조 변경
        payload = {
            "query": query,
            "service_type": "your_service_type",  # 필요한 경우 추가 파라미터
            # 기타 필요한 파라미터
        }
        
        response = requests.post(
            endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            # 응답 처리 로직 수정
            return response.json()
        else:
            return {
                "query": query, 
                "result": f"오류가 발생했습니다: {response.status_code}", 
                "error": response.text
            }
    except Exception as e:
        return {"query": query, "result": f"요청 오류: {str(e)}"}
```

## 4. UI 요소 추가 또는 수정하기

### 4.1 사이드바 커스터마이징

사이드바에 추가 기능이 필요한 경우:

```python
with st.sidebar:
    st.title(SERVICE_NAME)
    
    st.markdown(SIDEBAR_SEARCHING_GUIDE, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 추가 위젯 예시
    selected_option = st.selectbox(
        "분석 옵션 선택:",
        ["옵션 1", "옵션 2", "옵션 3"],
        key=f"{SERVICE_ID}_analysis_option"
    )
    
    # 기존 언어 선택 및 초기화 버튼 유지
    # ...
```

### 4.2 메인 화면 커스터마이징

메인 화면에 추가 기능이 필요한 경우:

```python
# 기존 서비스 제목 및 설명 유지
# ...

# 추가 입력 필드 또는 위젯
uploaded_file = st.file_uploader("데이터 파일 업로드", type=["csv", "xlsx"], key=f"{SERVICE_ID}_file_uploader")
if uploaded_file is not None:
    # 파일 처리 로직
    st.success("파일이 성공적으로 업로드되었습니다.")

# 기존 대표 질문 및 채팅 인터페이스 유지
# ...
```

## 5. 스타일 커스터마이징

CSS 스타일을 수정하여 서비스의 시각적 디자인을 변경할 수 있습니다:

```python
st.markdown(f"""
<style>
    /* 메인 타이틀 스타일 */
    .main-title {{
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #YOUR_COLOR_CODE; /* 원하는 색상으로 변경 */
        text-align: center;
    }}
    
    /* 추가 스타일 정의 */
    .custom-container {{
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #YOUR_COLOR_CODE;
    }}
    
    /* 기존 스타일 유지 또는 수정 */
    /* ... */
</style>
""", unsafe_allow_html=True)
```

## 6. 자동 스크롤 기능 활용하기

템플릿에 구현된 자동 스크롤 기능은 다음과 같은 JavaScript 코드로 구현되어 있습니다:

```javascript
// 채팅 영역 자동 스크롤
function scrollChatToBottom() {
    try {
        // 채팅 메시지 컨테이너 찾기
        const chatContainer = document.querySelector('.stChatMessageContainer');
        if (chatContainer) {
            // 강제로 스크롤 위치 설정
            chatContainer.scrollTop = chatContainer.scrollHeight;
            
            // 마지막 메시지 찾기 및 스크롤
            const messages = document.querySelectorAll('.stChatMessage');
            if (messages && messages.length > 0) {
                const lastMessage = messages[messages.length - 1];
                lastMessage.scrollIntoView({ behavior: 'auto', block: 'end' });
                
                // 추가 스크롤 조정
                window.scrollTo(0, document.body.scrollHeight);
            }
        }
        
        // 입력창 포커스
        const textInput = document.querySelector(`input[data-testid="stTextInput"][key="${currentInputKey}"]`);
        if (textInput) {
            textInput.focus();
        }
    } catch (e) {
        console.error("스크롤 오류:", e);
    }
}
```

이 기능을 유지하거나 필요에 따라 수정할 수 있습니다.

## 7. 세션 상태 관리

Streamlit의 세션 상태를 활용하여 대화 기록 및 사용자 설정을 관리합니다:

```python
# 세션 상태 초기화 (서비스별 고유 키 사용)
if f'{SERVICE_ID}_messages' not in st.session_state:
    st.session_state[f'{SERVICE_ID}_messages'] = []

# 추가 세션 상태 변수 정의
if f"{SERVICE_ID}_custom_state" not in st.session_state:
    st.session_state[f"{SERVICE_ID}_custom_state"] = default_value
```

세션 상태 변수에 접근하고 수정하는 방법:

```python
# 세션 상태 읽기
current_value = st.session_state[f"{SERVICE_ID}_custom_state"]

# 세션 상태 업데이트
st.session_state[f"{SERVICE_ID}_custom_state"] = new_value
```

## 8. 폼 제출 처리 커스터마이징

사용자 입력 처리 로직을 수정하여 서비스에 맞게 조정할 수 있습니다:

```python
# 폼 제출 처리
if submitted and user_input.strip():
    # 사용자 입력 전처리
    processed_input = preprocess_user_input(user_input)
    
    # 사용자 입력 표시
    with chat_container.chat_message("user"):
        st.markdown(processed_input)
    
    # 세션에 사용자 메시지 추가
    st.session_state[f'{SERVICE_ID}_messages'].append({"role": "user", "content": processed_input})
    
    # 추가 처리 로직
    # ...
    
    # API 호출 및 응답 처리
    # ...
```

## 9. 고급 기능 추가하기

### 9.1 데이터 시각화

Streamlit의 데이터 시각화 기능을 활용하여 분석 결과를 시각적으로 표현할 수 있습니다:

```python
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 준비
data = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D'],
    'Values': [10, 25, 15, 30]
})

# 차트 표시
st.subheader("분석 결과 시각화")
fig, ax = plt.subplots()
ax.bar(data['Category'], data['Values'])
st.pyplot(fig)
```

### 9.2 탭 인터페이스

여러 기능을 탭으로 구분하여 제공할 수 있습니다:

```python
tab1, tab2, tab3 = st.tabs(["대화", "데이터 분석", "설정"])

with tab1:
    # 기존 채팅 인터페이스
    # ...

with tab2:
    # 데이터 분석 기능
    st.subheader("데이터 분석")
    # ...

with tab3:
    # 설정 옵션
    st.subheader("설정")
    # ...
```

## 10. 배포 및 테스트

1. 개발한 서비스 페이지를 다음 명령으로 실행합니다:
   ```bash
   streamlit run service_page/service_my_service.py
   ```

2. 브라우저에서 `http://localhost:8501`에 접속하여 서비스를 테스트합니다.

3. 다양한 사용자 시나리오를 테스트하여 기능이 정상적으로 작동하는지 확인합니다.

## 11. 문제 해결 팁

1. **세션 상태 문제**: 세션 상태 변수 이름이 충돌하지 않도록 항상 `SERVICE_ID`를 접두사로 사용합니다.

2. **스타일 적용 문제**: CSS 선택자가 Streamlit 컴포넌트와 일치하는지 확인합니다. 브라우저 개발자 도구를 사용하여 요소 검사가 가능합니다.

3. **자동 스크롤 문제**: JavaScript 코드가 올바르게 실행되는지 확인합니다. 브라우저 콘솔에서 오류 메시지를 확인할 수 있습니다.

4. **API 통신 문제**: API 엔드포인트가 올바른지, 요청 형식이 API 요구사항과 일치하는지 확인합니다.

## 12. 모범 사례

1. **코드 모듈화**: 반복되는 기능은 함수로 분리하여 코드 가독성과 유지보수성을 높입니다.

2. **오류 처리**: 사용자 친화적인 오류 메시지를 제공하고, 예외 상황을 적절히 처리합니다.

3. **성능 최적화**: 불필요한 재계산을 피하고, 캐싱을 활용하여 성능을 최적화합니다.

4. **사용자 경험**: 로딩 상태를 명확히 표시하고, 직관적인 UI를 제공합니다.

5. **반응형 디자인**: 다양한 화면 크기에서 테스트하여 모든 환경에서 사용 가능한지 확인합니다.

## 13. 템플릿의 주요 기능 요약

### 13.1 UI 구성 요소
- 사이드바: 서비스 정보, 언어 선택, 대화 초기화 버튼
- 메인 화면: 서비스 제목, 설명, 대표 질문 버튼, 채팅 인터페이스
- 입력 필드: 하단에 고정된 질문 입력 폼

### 13.2 핵심 기능
- 대화형 인터페이스: 사용자 질문과 AI 응답을 채팅 형식으로 표시
- 자동 스크롤: 새 메시지가 추가될 때 자동으로 스크롤
- 다국어 지원: 한국어/영어 전환 기능
- 세션 관리: 대화 기록 유지 및 관리
- API 통신: 외부 LLM API와의 통신

### 13.3 스타일링 특징
- 반응형 디자인: 다양한 화면 크기에 대응
- 고정된 입력 필드: 항상 화면 하단에 표시
- 세련된 시각적 디자인: 그림자 효과, 색상 구성, 애니메이션

이 가이드를 참고하여 `service_template_main.py`를 기반으로 자신만의 Streamlit 서비스 페이지를 개발해보세요. 템플릿의 구조를 이해하고 필요에 맞게 커스터마이징하면 효율적으로 새로운 서비스를 구현할 수 있습니다. 
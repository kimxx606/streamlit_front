# Intellytics AI Agent 서비스

Streamlit을 사용하여 구현된 NPS 분석 서비스 웹 애플리케이션입니다. 사용자 친화적인 인터페이스와 강력한 AI 기반 분석 기능을 제공합니다.

## 주요 기능

- **NPS 데이터 분석**: 고객 NPS(Net Promoter Score) 데이터를 분석하여 비즈니스 인사이트 제공
- **대화형 인터페이스**: 자연어로 질문하고 AI가 분석 결과를 제공하는 채팅 인터페이스
- **다국어 지원**: 한국어/영어 언어 전환 기능
- **반응형 디자인**: 다양한 화면 크기에 최적화된 UI

## UI 개선 사항

- **고정된 입력 필드**: 질문 입력 필드가 화면 하단에 항상 고정되어 있어 사용자 경험 향상
- **자동 스크롤 기능**: 새 메시지가 도착하면 이전 대화 내용이 자동으로 위로 스크롤되어 최신 내용 확인 용이
- **세련된 디자인**: 모던한 색상 구성과 그림자 효과로 시각적 매력 향상
- **대표 질문 버튼**: 자주 묻는 질문을 버튼으로 제공하여 빠른 접근성 제공

## 프로젝트 구조

```
.
├── streamlit_app.py        # 메인 애플리케이션 파일
├── service_page/           # 서비스 페이지 디렉토리
│   ├── service_template_main.py  # NPS 분석 서비스 템플릿
│   └── service_voc.py      # VOC 서비스
├── requirements.txt        # 의존성 패키지 목록
└── tests/                  # 테스트 디렉토리
```

## 기술적 특징

### 프론트엔드
- **Streamlit**: 파이썬 기반 웹 애플리케이션 프레임워크
- **CSS 커스터마이징**: 세련된 UI를 위한 맞춤형 CSS 스타일
- **JavaScript 통합**: 향상된 사용자 경험을 위한 커스텀 JavaScript 기능
  - 자동 스크롤 기능
  - 입력 필드 포커스 관리
  - 실시간 DOM 변경 감지 (MutationObserver)

### 백엔드
- **API 통합**: 외부 LLM API와의 통신
- **세션 관리**: Streamlit 세션 상태를 활용한 대화 기록 유지
- **오류 처리**: 강화된 예외 처리 및 사용자 친화적인 오류 메시지

## 설치 및 실행

### 필수 요구사항

- Python 3.8 이상
- pip (Python 패키지 관리자)

### 설치

1. 저장소 클론:
```bash
git clone https://github.com/yourusername/intellytics-ai-agent.git
cd intellytics-ai-agent
```

2. 가상 환경 생성 및 활성화:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. 의존성 설치:
```bash
pip install -r requirements.txt
```

### 실행

```bash
streamlit run service_page/service_template_main.py
```

기본적으로 애플리케이션은 http://localhost:8501 에서 실행됩니다.

## API 연결

서비스는 기본적으로 다음 API 엔드포인트에 연결됩니다:
```
http://localhost:8081/ask
```

환경 변수 `API 엔드포인트`를 설정하여 API 엔드포인트를 변경할 수 있습니다.

## 사용자 인터페이스 가이드

### 메인 화면
- **상단**: 서비스 제목과 설명
- **중앙**: 대표 질문 버튼과 채팅 인터페이스
- **하단**: 고정된 질문 입력 필드

### 사이드바
- **서비스 정보**: 서비스 제목과 안내 정보
- **언어 선택**: 한국어/영어 전환 라디오 버튼
- **대화 초기화**: 현재 대화 내용을 초기화하는 버튼
- **서비스 정보**: API 연결 정보 및 저작권 정보

### 대화 인터페이스
- **질문 입력**: 하단 입력 필드에 질문 입력 후 Enter 키 또는 전송 버튼 클릭
- **대표 질문**: 미리 정의된 질문 버튼 클릭으로 빠른 질문 가능
- **응답 확인**: AI의 응답이 채팅창에 표시되며, 자동으로 스크롤됨

## 커스터마이징

서비스 템플릿은 다양한 용도로 커스터마이징할 수 있습니다:

1. `SERVICE_ID`: 세션 상태 키 접두사
2. `SERVICE_NAME`: 서비스 제목
3. `SERVICE_DESCRIPTION`: 서비스 설명
4. `SAMPLE_QUESTIONS`: 대표 질문 목록
5. `api_endpoint`: API 엔드포인트 URL

CSS 스타일을 수정하여 UI 디자인을 변경할 수 있습니다.

## 라이센스

© 2025 LLM 서비스 템플릿 | 버전 1.0 
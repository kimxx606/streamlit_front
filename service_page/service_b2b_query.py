import streamlit as st
import requests
import json
import os
import streamlit.components.v1 as components
from streamlit_extras.stylable_container import stylable_container

from service_page.util.utils import initialize_expansion_states, set_expanded_state

# 외부 CSS 파일 불러오기
def load_css():
    with open("service_page/style/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# CSS 로드 함수 호출
load_css()

# d2c, survey genius, mellerisearch expansion 기능
# 세션 상태 초기화 및 확장 상태 관리
initialize_expansion_states()
if set_expanded_state('survey'):
    st.rerun()
    
# if (st.session_state.d2c_expanded == True) or (st.session_state.mellerisearch_expanded == True) or (st.session_state.survey_expanded == True) or (st.session_state.hrdx_expanded == True):
#     st.session_state.d2c_expanded = False
#     st.session_state.survey_expanded = False
#     st.session_state.mellerisearch_expanded = False
#     st.session_state.hrdx_expanded = False
#     st.rerun()

# =======================================================================
# 서비스 페이지 개발 가이드
# =======================================================================
# 이 템플릿을 사용하여 새로운 서비스 페이지를 개발할 수 있습니다.
# 자세한 가이드는 service_page/README.md 파일을 참고하세요.
# 
# 주요 커스터마이징 영역:
# 1. 서비스 ID 및 기본 정보 설정 (SERVICE_ID, SERVICE_NAME 등)
# 2. API 통신 함수 수정 (ask_llm_api)
# 3. UI 요소 추가 또는 수정
# 4. 스타일 커스터마이징
# =======================================================================

# ======= 서비스별 커스터마이징 영역 I =======
# 서비스 ID (세션 상태 키 접두사로 사용)
SERVICE_ID = "b2b-query"
# ========================================

# 세션 상태 초기화 (서비스별 고유 키 사용)
if f'{SERVICE_ID}_messages' not in st.session_state:
    st.session_state[f'{SERVICE_ID}_messages'] = []

if f"{SERVICE_ID}_language" not in st.session_state:
    st.session_state[f"{SERVICE_ID}_language"] = "ko"  # 기본 언어는 한국어
    
if f"{SERVICE_ID}_selected_question" not in st.session_state:
    st.session_state[f"{SERVICE_ID}_selected_question"] = ""

if f"{SERVICE_ID}_user_input" not in st.session_state:
    st.session_state[f"{SERVICE_ID}_user_input"] = ""

if f"{SERVICE_ID}_question_selected" not in st.session_state:
    st.session_state[f"{SERVICE_ID}_question_selected"] = False

if f"{SERVICE_ID}_clear_input" not in st.session_state:
    st.session_state[f"{SERVICE_ID}_clear_input"] = False
    
if f"{SERVICE_ID}_text_input_key_counter" not in st.session_state:
    st.session_state[f"{SERVICE_ID}_text_input_key_counter"] = 0

if f"{SERVICE_ID}_country" not in st.session_state:
    st.session_state[f"{SERVICE_ID}_country"] = "United Kingdom"

if  f'{SERVICE_ID}_run_id' not in st.session_state:
    st.session_state[f'{SERVICE_ID}_run_id']=None


# ======= 서비스별 커스터마이징 영역 II =======
# 이 부분을 수정하여 다양한 서비스에 화면을 구성합니다.

# ==== MAIN 채팅 화면 정보 ====
# 서비스 기본 정보
SERVICE_NAME = {'ko': "B2B Query - SQL Database 질의 응답 서비스", "en": "B2B Query - B2B DB exploration and inquiry response service"}

SERVICE_DESCRIPTION = {
    "ko":"""
    
#### 서비스 개요
▶ B2B 3대 전환 지수<br>
3대 전환 지수란 고객 상태에 따라 Contact(초기 접점 고객), Lead(잠재 고객), Opportunity(기회 고객)로 분류하고, Domain-Specific Model을 활용하여 고객이 다음 단계로 전환될 가능성을 측정하는 지표를 의미합니다.

&nbsp;&nbsp;&nbsp;&nbsp;- 리드 전환 지수 : Contact  가 Lead로 전환될 가능성<br>
&nbsp;&nbsp;&nbsp;&nbsp;- 기회 전환 지수 : Lead가 Opportunity로 전환될 가능성<br>
&nbsp;&nbsp;&nbsp;&nbsp;- 수주 전환 지수 : Opportunity가 수주를 성공할 가능성<br>

특히 기회 전환 지수(잠재 고객)는 매출 성장의 핵심 요소로 평가되며, NewBRM 수주 관리 시스템을 통해 자사 마케팅 팀과 영업 사원에게 XAI 데이터를 함께 텍스트 형태로 제공하고 있습니다.<br>
 
▶ B2B Query 서비스<br>
B2B Query는 B2B 기회 전환 지수 DB에 대한 질문에 응답하는 NL2SQL 기반의 서비스입니다.<br>
기회 전환 지수는 단순한 텍스트 형식의 결과값만 제공되기 때문에, 다른 데이터와 비교하거나 다양한 관점에서 분석하려는 수요가 증가하고 있습니다. 따라서 사용자는 DB에 대한 지식이 없더라도 자연어 질문을 통해 단순한 정보 탐색뿐만 아니라, 기회 전환 지수의 통계 데이터를 함께 확인할 수 있습니다.<br>
B2B Query는 DB 탐색 특화 모델로써, 3대 전환 지수뿐 아니라 정제 된 형식의 어떠한 DB를 삽입하더라도 질문에 대한 응답이 가능합니다. <br>

#### 데이터 설명
New BRM에 2021-03-11 부터 2024-05-26 까지 등록된 리드 정보(개인 정보 제외, 익명화)<br>
<table style="border-collapse:collapse;border-color:#ccc;border-spacing:0;border:none;table-layout: fixed; width: 100%" class="tg">
    <colgroup>
        <col style="width: 16%">
        <col style="width: 4%">
        <col style="width: 40%">
        <col style="width: 40%">
    </colgroup>
    <thead>
        <tr>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:15px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal" colspan="2"><span style="color:black">데이터 테이블</span></td>
            <td style="background-color:#ffffff;border-color:#000000;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:15px;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:middle;word-break:normal">데이터 Column</td>
            <td style="background-color:#ffffff;border-color:#000000;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:15px;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:middle;word-break:normal">설명</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:15px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal" rowspan="7"><span style="color:black">데이터 컬럼</span></td>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:15px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">1</td>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:13px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">Created Date</td>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:13px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">리드 생성일</td>
        </tr>
        <tr>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:15px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">2</td>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:13px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">Lead Channel Type</td>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:13px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">리드 수집 경로</td>
        </tr>
        <tr>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:15px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">3</td>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:13px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">Vertical</td>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:13px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">수직 시장</td>
        </tr>
        <tr>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:15px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">4</td>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:13px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">Account</td>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:13px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">고객사 이름</td>
        </tr>
        <tr>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:15px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">5</td>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:13px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">Lead Stage</td>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:13px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">리드 상태</td>
        </tr>
        <tr>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:15px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">6</td>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:13px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">Opportunity Score</td>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:13px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">기회전환지수</td>
        </tr>
        <tr>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:15px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">7</td>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:13px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">Reason 1~5</td>
            <td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:13px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">기회전환지수 XAI</td>
        </tr>
    </tbody>
</table>



#### 사용 방법
&nbsp;&nbsp;&nbsp;&nbsp;- 리드 DB로 부터 탐색하고 싶은 리드의 특징을 명시하고, 원하는 정보를 질문해주세요. 이전의 질의 결과에 대한 후속 질문도 가능합니다.<br>
&nbsp;&nbsp;&nbsp;&nbsp;- 리드의 생성 날짜, 수집 경로, Vertical, 대상 기업명, Stage, 기회전환지수 및 지수 원인에 대해 응답 할 수 있습니다.
""",
    "en":"""
under construction...
"""
}

# 대표 질문 리스트
SAMPLE_QUESTIONS = {
    "ko":[
    "기회전환지수가 가장 높은 리드 3개 알려줘",
    "2024년 3월에 생성된 리드 중 가장 기회전환지수가 가장 높은 리드의 상세 정보 알려줘",
    "리드가 수집된 경로에 따른 기회전환지수 평균을 알려줘"
    ], 
    "en":[
    "under constuction..."
    ]
}

# cloud: 기본 API 엔드포인트
# api_endpoint = "http://" + SERVICE_ID + "." + os.getenv("ROOT_DOMAIN") + "/b2b_query"
# refresh_api_endpoint = "http://" + SERVICE_ID+ "." + os.getenv("ROOT_DOMAIN")+ "/refresh_memory"
# feedback_api_endpoint = "http://" + SERVICE_ID + "." + os.getenv("ROOT_DOMAIN") +"/get_langsmith_feedback"

api_endpoint = "https://b2b-query.mkdev-kic.intellytics.lge.com/b2b_query"
refresh_api_endpoint = "http://b2b-query.mkdev-kic.intellytics.lge.com/refresh_memory"
feedback_api_endpoint = "http://b2b-query.mkdev-kic.intellytics.lge.com/get_langsmith_feedback"

# local: sg generation api setting
# SERVER_URL='10.157.52.156:8314'
# api_endpoint = f"http://{SERVER_URL}/b2b_query"
# refresh_api_endpoint = f"http://{SERVER_URL}/refresh_memory"

# ==== Sidebar 화면 정보 ====
# SIDEBAR_INFO = "### 서비스 안내"
# HTML 문법 가능
SIDEBAR_SEARCHING_GUIDE = {
    "ko":"""
    2021-03-11 부터 2024-05-26 사이에 생성된 리드의 대한 정보와 해당 리드의 기회전환지수(Domian Specific AI) 결과에 대해 응답 가능합니다.<br>
""",
    "en":"""
Under construction... <br>       
"""
}

sample_questions_description = {
    "ko": "B2B Query에서 확인 할 수 있는 질문 예시를 참고해보세요.",
    "en": "under construction..."
}
# ========================================
from streamlit_feedback import streamlit_feedback


def collect_feedback(run_id):    
    feedback = streamlit_feedback(
        feedback_type="thumbs",
        optional_text_label="(optional) 자세한 피드백을 남겨주세요.",
        key=f"feedback_{run_id}",
    )
    score_mappings = {"thumbs": {"👍": 1, "👎": 0}}
    score_map = list(score_mappings.values())[0]
    if feedback:
        score = score_map.get(feedback["score"], None)
        comment = feedback.get("text", None)
        if comment is None:
            comment=''

        feedback_type_str = list(score_mappings.keys())[0]

        requests.post(
            feedback_api_endpoint, 
            params={'run_id':run_id, 'feedback_type_str':feedback_type_str, 
                    'score':score, 'comment':comment} # llo qpi 규칙상 입출력 있어야하기 때문에 작성한 dummy
        )

# =======Table container 내 출력을 위한 추가 함수=======================================
import pandas as pd
from io import StringIO

def markdown_table_to_df(response_str, skip=False):
    if skip:
        return [(response_str, "normal")]
    
    def find_substring_indices(haystack, needle):
        start = 0
        while True:
            start = haystack.find(needle, start)
            if start == -1: return
            yield start
            start += 1  # Use start += len(needle) to find non-overlapping matches
 
    start_table = "\n|"
    end_table = "|\n\n"
    target_char= "|"
 
    # Finding indices for start_table and end_table
    new_row_indices = list(find_substring_indices(response_str, start_table))
    end_of_table = list(find_substring_indices(response_str, end_table))
    if len(end_of_table) == 0:
        end_table_2 = "|\n\n"
        end_of_table = list(find_substring_indices(response_str, end_table_2))
 
    table_indices = []
    for end_table_index in end_of_table:
        #select only new_row_indices that are smaller than end_table_index
        # And the first of this index will be the start of the current table
        # And the next new_table_start_index must be bigger than the currentend_table_index
        if len(table_indices) > 0:
            new_table_start_index = [new_row_index for new_row_index in new_row_indices if new_row_index < end_table_index and new_row_index > table_indices[-1][1]][0]
        else:
 
            new_table_start_index = [new_row_index for new_row_index in new_row_indices if new_row_index < end_table_index][0]
        table_indices.append((new_table_start_index, end_table_index))
    indices = [index for index, char in enumerate(response_str) if char == target_char]
    if len(indices) < 2:
        return [(response_str, "normal")]
   
    list_of_tuples = [] # List of tuples to store the chunk of the string and the type of chunk
    for table_index in table_indices:
        if table_index == table_indices[0]:
            normal_str_before = response_str[:table_index[0]]
        else:
            normal_str_before = response_str[table_indices[table_indices.index(table_index)-1][1]+1:table_index[0]]
        table_str = response_str[table_index[0]:table_index[1]+1]
   
        list_of_tuples.append((normal_str_before, "normal"))
        list_of_tuples.append((table_str, "table"))
 
        # if the table is the last element in the list_of_tuples
        if table_index == table_indices[-1]:
            normal_str_after = response_str[table_index[1]+1:]
            list_of_tuples.append((normal_str_after, "normal"))
 
    for idx, (string, type) in enumerate(list_of_tuples):
        if type == "table":
            df = pd.read_csv(StringIO(string), sep="|", skipinitialspace=True)
            df.columns=df.columns.str.strip()
            df = df.dropna(axis=1, how='all')
            try:
                df = df[~df.apply(lambda x: all( '---' in val for val in x), axis=1)]
            except:
                df=df[1:]
 
            df.reset_index(drop=True, inplace=True)
            for col in df.columns:
                if df[col].dtype == 'object' :
                    df[col] = df[col].str.strip()
                    if df[col].str.match(r"^-?\d+(\.\d+)?$").all():
                        df[col] = df[col].astype(float)
 
            #replace the string with the dataframe
            list_of_tuples[idx] = (df, "table")
 
    return list_of_tuples


def show_table_html_markdown(list_of_tuples):
    for idx, (string, type) in enumerate(list_of_tuples):
        if type == "table":
            st.dataframe(string, hide_index=True,  use_container_width=True)
        else:
            st.markdown(string)

def display_reponse(response):
    list_of_tuples = markdown_table_to_df(response)
    show_table_html_markdown(list_of_tuples)

# ======= API 통신 함수 =======
# API 통신 함수는 서비스별로 필요한 파라미터를 추가하거나 수정할 수 있습니다.
# README.md 파일의 'API 통신' 섹션을 참고하여 커스터마이징하세요.
#
# 파라미터:
# - endpoint: API 엔드포인트 URL
# - query: 사용자 질의 텍스트
# - language: 응답 언어 설정 (기본값: "ko")
#
# 추가 파라미터가 필요한 경우:
# - 서비스 유형별 파라미터 (예: service_type, model_name 등)
# - 데이터 처리 옵션 (예: include_chart=True)
# 
# 응답 형식:
# - success: 성공 여부 (True/False)
# - data: API 응답 데이터 (성공 시)
# - error: 오류 메시지 (실패 시)
def ask_llm_api(endpoint, query,language="ko"):
    try:

        # b2b-server api
        response = requests.post(
        endpoint, 
        timeout=60,  # 30초 타임아웃 설정
        params={"input_message": query}  # URL 파라미터로 전달
)
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {
                "success": False, 
                "error": f"API 오류: {response.status_code}", 
                "details": response.text
            }
            
    except requests.exceptions.Timeout:
        return {"success": False, "error": "API 요청 시간이 초과되었습니다. 나중에 다시 시도해주세요."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "API 서버에 연결할 수 없습니다. 네트워크 연결을 확인해주세요."}
    except Exception as e:
        return {"success": False, "error": f"오류가 발생했습니다: {str(e)}"}


# ======= 화면 구성 시작 =======

# 사이드바 구성
with st.sidebar:
    st.title(SERVICE_NAME[st.session_state[SERVICE_ID + '_language']])
    
    # st.markdown(SIDEBAR_INFO)
    st.markdown(SIDEBAR_SEARCHING_GUIDE[st.session_state[f"{SERVICE_ID}_language"]], unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 언어 선택 라디오 버튼
    st.markdown("<div class='language-selector'>", unsafe_allow_html=True)
    selected_language = st.radio(
        "Language:", 
        options=["한국어", "English"],
        index=0 if st.session_state.get(f"{SERVICE_ID}_language", "ko") == "ko" else 1,
        key=f"{SERVICE_ID}_language_radio",
        horizontal=True,
        on_change=lambda: st.session_state.update({f"{SERVICE_ID}_language": "ko" if st.session_state[f"{SERVICE_ID}_language_radio"] == "한국어" else "en"})
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 언어 상태 자동 업데이트
    st.session_state[f"{SERVICE_ID}_language"] = "ko" if selected_language == "한국어" else "en"
    
    # 해외 법인 데이터 선택 
    st.selectbox("Nation", ["United Kingdom", "Germany", "Spain", "Italy", "Brazil"],
                    index=0,
                    key=st.session_state[f"{SERVICE_ID}_country"],
                    disabled=True)
    
    # 채팅 초기화 버튼
    if st.button("대화 초기화", use_container_width=True, key=f"{SERVICE_ID}_reset_btn"):
        st.session_state[f'{SERVICE_ID}_messages'] = []
        st.session_state[f"{SERVICE_ID}_user_input"] = ""
        st.session_state[f"{SERVICE_ID}_selected_question"] = ""
        st.session_state[f"{SERVICE_ID}_question_selected"] = False
        st.session_state[f"{SERVICE_ID}_clear_input"] = False
        st.session_state[f"{SERVICE_ID}_text_input_key_counter"] = 0
        
        # refresh memory on the api server
        response = requests.post(
            refresh_api_endpoint, 
            params={"dummy": "dummy"}  # llo qpi 규칙상 입출력 있어야하기 때문에 작성한 dummy
        )

        st.rerun()
    
    st.divider()
    
    info_text = {"ko": "이 애플리케이션은 **Intellytics**에 배포된 LLM API를 사용합니다.", "en": "The Application uses LLM API distributed by **Intellytics**"}
    version_text = "© 2025 B2B Query | Ver 1.0"
    st.info(info_text[st.session_state[f"{SERVICE_ID}_language"]])
    
    # 사이드바 하단에 저작권 정보 표시
    st.markdown("---")
    st.markdown(version_text)

# 1. 메인 화면 및 서비스 설명
st.markdown(f"<div class='main-title'>{SERVICE_NAME[st.session_state[SERVICE_ID + '_language']]}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='service-description'>{SERVICE_DESCRIPTION[st.session_state[SERVICE_ID + '_language']]}</div>", unsafe_allow_html=True)

# 대표 질문 섹션
st.markdown("<h3 class='sample-questions-title'>FAQ</h3>", unsafe_allow_html=True)
st.markdown(f"<p class='sample-questions-description'>{sample_questions_description[st.session_state[SERVICE_ID+'_language']]}</p>", unsafe_allow_html=True)
st.markdown("<div class='sample-questions-container'>", unsafe_allow_html=True)
# 3. 대표 질문 버튼 컨테이너 및 버튼
with stylable_container(
    key="sample_questions",
    css_styles="""
    button{
        display: flex;
        justify-content: flex-start;
        width: 100%;
    }

    """
):
    for i, question in enumerate(SAMPLE_QUESTIONS[st.session_state[SERVICE_ID + '_language']]):
        if st.button(question, key=f"{SERVICE_ID}_q_btn_{i}", use_container_width=True):
            # 선택된 질문을 user_input 세션 상태에 저장 (채팅 입력창에 표시하기 위해)
            st.session_state[f"{SERVICE_ID}_user_input"] = question
            # 대표 질문 선택 플래그 설정 - 입력창에 포커스를 주기 위한 용도로만 사용
            st.session_state[f"{SERVICE_ID}_question_selected"] = True
            st.session_state[f"{SERVICE_ID}_selected_question"] = question
            # 페이지 새로고침 (입력창에 질문 표시)
            st.rerun()
            
st.markdown("</div>", unsafe_allow_html=True)

# 4. 채팅 컨테이너 생성 - 여기서 정의만 하고 내용은 아래에서 채움
chat_container = st.container()
spinner_container = st.empty()

# 사용자 질문 처리 및 API 호출 함수 정의
def process_user_query(query):
    # 사용자 입력 표시
    with chat_container.chat_message("user"):
        st.markdown(query)
    
    # 세션에 사용자 메시지 추가
    st.session_state[f'{SERVICE_ID}_messages'].append({"role": "user", "content": query})
    
    # API 호출 (with spinner) - 스피너를 채팅 메시지와 입력창 사이에 표시
    with spinner_container, st.spinner("답변을 생성 중입니다..."):
        result = ask_llm_api(endpoint=api_endpoint, query=query, language=st.session_state[f"{SERVICE_ID}_language"])

    # 응답 처리
    if not result.get("success", False):
        response = f"오류가 발생했습니다: {result.get('error', '알 수 없는 오류')}"
    else:
        #print(result.get("data", {}))
        #response = result.get("data", {}).get("result", "응답을 받지 못했습니다.")
        response = result.get("data", {}).get("response", "응답을 받지 못했습니다.")
        run_id=result.get("data", {}).get("run_id", "run_id 응답을 받지 못했습니다.")

    # 응답 표시
    with chat_container.chat_message("assistant"):
        display_reponse(response)
        # st.markdown(response)
    
 
    # 세션에 응답 메시지 추가
    st.session_state[f'{SERVICE_ID}_messages'].append({"role": "assistant", "content": response})
    st.session_state[f'{SERVICE_ID}_run_id']=run_id

    # 자동 스크롤 컴포넌트 추가 (응답 후)
    components.html(
        """
        <script>
        function findChatContainer() {
            // 여러 가능한 선택자를 시도
            const selectors = [
                '.stChatMessageContainer',
                '[data-testid="stChatMessageContainer"]',
                '.element-container:has(.stChatMessage)',
                '#chat-container-marker',
                '.main .block-container'
            ];
            
            for (const selector of selectors) {
                const container = document.querySelector(selector);
                if (container) return container;
            }
            return null;
        }
        
        // 스크롤 함수
        function scrollToBottom() {
            const chatContainer = findChatContainer();
            if (chatContainer) {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        }
        
        // 0.5초 후 스크롤 (애니메이션이 끝날 때쯤)
        setTimeout(scrollToBottom, 500);
        
        // 안전을 위해 약간의 지연을 두고 다시 시도
        setTimeout(scrollToBottom, 800);
        </script>
        """,
        height=0,
    )

# 5. 메시지 표시 영역 - 이제 아래쪽에 위치
with chat_container:
    # 채팅 컨테이너에 ID 추가
    st.markdown("""
    <style>
    /* 채팅 컨테이너에 ID 추가 */
    .stChatMessageContainer {
        max-height: calc(100vh - 250px) !important;
        overflow-y: auto !important;
        width: 800px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding-bottom: 20px !important;
    }
    
    /* 채팅 메시지 스타일 */
    .stChatMessage {
        margin-bottom: 10px !important;
    }
    </style>
    <div id="chat-container-marker"></div>
    """, unsafe_allow_html=True)
    
    # 메시지 표시
    for message in st.session_state[f'{SERVICE_ID}_messages']:
        with st.chat_message(message["role"]):
            display_reponse(message["content"])
    if len(st.session_state[f'{SERVICE_ID}_messages'])>1:
        if st.session_state[f'{SERVICE_ID}_messages'][-1]['role']=='assistant':
            collect_feedback(st.session_state[f'{SERVICE_ID}_run_id'])       

    # 초기 메시지
    if not st.session_state[f'{SERVICE_ID}_messages']:
        with st.chat_message("assistant"):
            welcome_message = "Intellytics AI Agent에게 물어보세요!"
            st.markdown(welcome_message)
            st.session_state[f'{SERVICE_ID}_messages'].append({"role": "assistant", "content": welcome_message})
    
    # 자동 스크롤 컴포넌트 추가 (개선된 버전)
    if st.session_state[f'{SERVICE_ID}_messages']:
        components.html(
            """
            <script>
            function findChatContainer() {
                // 여러 가능한 선택자를 시도
                const selectors = [
                    '.stChatMessageContainer',
                    '[data-testid="stChatMessageContainer"]',
                    '.element-container:has(.stChatMessage)',
                    '#chat-container-marker',
                    '.main .block-container'
                ];
                
                for (const selector of selectors) {
                    const container = document.querySelector(selector);
                    if (container) return container;
                }
                return null;
            }
            
            // 스크롤 함수
            function scrollToBottom() {
                const chatContainer = findChatContainer();
                if (chatContainer) {
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }
            }
            
            // 0.5초 후 스크롤 (애니메이션이 끝날 때쯤)
            setTimeout(scrollToBottom, 500);
            
            // 안전을 위해 약간의 지연을 두고 다시 시도
            setTimeout(scrollToBottom, 800);
            </script>
            """,
            height=0,
        )

# 채팅 입력을 사용하여 사용자 입력 받기
user_input = st.chat_input(key=f"{SERVICE_ID}_chat_input")

# 저장된 대표 질문이 있는지 확인하고 처리
if st.session_state.get(f"{SERVICE_ID}_selected_question"):
    user_input = st.session_state[f"{SERVICE_ID}_selected_question"]
    st.session_state[f"{SERVICE_ID}_selected_question"] = ""  # 처리 후 초기화
    #process_user_query(selected_question)

# 사용자 입력 처리
if user_input and user_input.strip():
    # 대표 질문 선택 상태 초기화
    if f"{SERVICE_ID}_question_selected" in st.session_state:
        st.session_state[f"{SERVICE_ID}_question_selected"] = False
    
    # 줄바꿈 제거
    user_input = user_input.replace("\n", "")
    
    # 사용자 입력을 처리 함수로 전달
    process_user_query(user_input)
    
    # 입력창 초기화 - 여러 세션 상태 변수를 모두 초기화
    st.session_state[f"{SERVICE_ID}_user_input"] = ""
    st.session_state[f"{SERVICE_ID}_clear_input"] = True
    
    # 위젯 키 카운터 증가
    if f"{SERVICE_ID}_text_input_key_counter" in st.session_state:
        st.session_state[f"{SERVICE_ID}_text_input_key_counter"] = \
            st.session_state.get(f"{SERVICE_ID}_text_input_key_counter", 0) + 1
    
    # 페이지 새로고침
    st.rerun()



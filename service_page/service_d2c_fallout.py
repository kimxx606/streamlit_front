import streamlit as st
import requests
import json
import os
import uuid
from io import StringIO
import streamlit.components.v1 as components
from streamlit_feedback import streamlit_feedback
from streamlit_extras.stylable_container import stylable_container
from datetime import datetime
import pandas as pd

# 외부 CSS 파일 불러오기
def load_css():
    with open("style/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# CSS 로드 함수 호출
load_css()

# d2c expansion 기능
if st.session_state.d2c_expanded == False:
    st.session_state.d2c_expanded = True
    st.session_state.survey_expanded = False
    st.session_state.mellerisearch_expanded = False
    st.session_state.hrdx_expanded = False
    st.rerun() 
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
SERVICE_ID = "d2c-fallout"
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

if f"{SERVICE_ID}_thread_id" not in st.session_state:
    st.session_state[f"{SERVICE_ID}_thread_id"] = str(uuid.uuid4())

if  f'{SERVICE_ID}_run_id' not in st.session_state:
    st.session_state[f'{SERVICE_ID}_run_id']=None


# ======= 서비스별 커스터마이징 영역 II =======
# 이 부분을 수정하여 다양한 서비스에 화면을 구성합니다.

# ==== MAIN 채팅 화면 정보 ====
# 서비스 기본 정보
SERVICE_NAME = {'ko': "D2C - Fallout Analysis 서비스", "en": "D2C - Fallout Analysis Service"}

SERVICE_DESCRIPTION = {
    "ko":"""
    
OBS 매출현황에서 이슈(매출하락 등)에 대해서 **Funnel 및 유입 채널 관점에서 원인을 분석하고 해결방안**을 찾아볼 수 있는 서비스
<br>

#### 데이터 설명
- **해외영업본부**에서 관리하고 **EAP에 적재되어 있는 고객의 웹행동 정보를 포함한 Google Analytics 데이터**를 전처리하여 활용함
<table style="border-collapse:collapse;border-color:#ccc;border-spacing:0;border:none;table-layout: fixed; width: 100%" class="tg"><colgroup><col style="width: 7%"><col style="width: 4%"><col style="width: 21%"><col style="width: 5%"><col style="width: 19%"><col style="width: 19%"><col style="width: 25%"></colgroup>
<thead>
<tr><td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal" rowspan="2">데이터<br>테이블</td><td style="background-color:#fff;border-color:#ffffff;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal" rowspan="2"></td><td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:middle;word-break:normal">재료(Raw)데이터</td>
<td style="background-color:#fff;border-color:#ccc;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:22px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal" rowspan="8">→</td><td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:middle;word-break:normal" colspan="3">전처리(CL2)데이터</td></tr>
<tr><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"> <span style="color:black">V_DM_BI_MAIN_GA</span>  </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">FUNNEL</span>   </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">TRAFFIC</span>   </td>
<td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">DOMAIN SPECIFIC AI</span>   </td></tr>
<tr><td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal" rowspan="6">데이터<br>컬럼</td><td style="background-color:#FFF;border-color:#ffffff;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">1</span> </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">DATE</span>   </td>
<td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">DATE</span>   </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">DATE</td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">DATE</span>  </td></tr>
<tr><td style="background-color:#FFF;border-color:#ffffff;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">2</span>  </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">MODEL_CODE</span>   </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">WEEK_INFO</span>   </td>
<td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">WEEK_INFO</span>   </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">WEEK_INFO</span>   </td></tr>
<tr><td style="background-color:#FFF;border-color:#ffffff;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">3</span>   </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">VISIT_CNT</span>   </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">MODEL_CODE</span>   </td>
<td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">MODEL_CODE</span>   </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">MODEL_CODE</span>   </td></tr>
<tr><td style="background-color:#FFF;border-color:#ffffff;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">4</span> </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">ATC_CNT</td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">VISIT_CNT</span>   </td>
<td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">PRODUCT_LEVEL</span>   </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">IMPORTANT FEATURE1</span>   </td></tr>
<tr><td style="background-color:#FFF;border-color:#ffffff;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">5 </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">CHECKOUT_CNT</span></td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">ATC_CNT</span>   </td>
<td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">TRAFFIC_TYPE</span>   </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">I<span style="color:black">MPORTANT FEATURE2</span>   </td></tr>
<tr><td style="background-color:#FFF;border-color:#ffffff;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">6</span> </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"> <span style="color:black">TRAFFIC_SOURCE</span>   </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">CHECKOUT_CNT</span>   </td>
<td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"></td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">IMPORTANT FEATURE3</span>   </td></tr>
</thead></table>

🔍 DX Automation for D2C 서비스 구현에 참여하고 싶으신 분들을 위해 [개발 가이드](http://mod.lge.com/hub/cx-llm/dx_d2c)를 제공합니다.

본 서비스는 현재 **2023년 6월 6일부터 2025년 2월 28일까지**까지의 **영국 OBS 사이트 고객의 웹행동 정보**에 대해 질문할 수 있습니다.
""",
    "en":"""
 
A service that **analyzes the causes of issues** (such as sales decline) from **the perspective of the funnel and inflow channels** in the OBS sales status and finds solutions.
<br>

#### Data Description
Managed by the **Overseas Sales & Marketing Company**, utilizing preprocessed Google Analytics data, including customer web behavior information stored in **EAP**.

<table style="border-collapse:collapse;border-color:#ccc;border-spacing:0;border:none;table-layout: fixed; width: 100%" class="tg"><colgroup><col style="width: 7%"><col style="width: 4%"><col style="width: 21%"><col style="width: 5%"><col style="width: 19%"><col style="width: 19%"><col style="width: 25%"></colgroup>
<thead>
<tr><td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal" rowspan="2">Data<br>Table</td><td style="background-color:#fff;border-color:#ffffff;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal" rowspan="2"></td><td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:middle;word-break:normal">Raw Data</td>
<td style="background-color:#fff;border-color:#ccc;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:22px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal" rowspan="8">→</td><td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:middle;word-break:normal" colspan="3">Preprocessed Data</td></tr>
<tr><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"> <span style="color:black">V_DM_BI_MAIN_GA</span>  </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">FUNNEL</span>   </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">TRAFFIC</span>   </td>
<td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">DOMAIN SPECIFIC AI</span>   </td></tr>
<tr><td style="background-color:#fff;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal" rowspan="6">Data<br>Columns</td><td style="background-color:#FFF;border-color:#ffffff;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">1</span> </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">DATE</span>   </td>
<td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">DATE</span>   </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">DATE</td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">DATE</span>  </td></tr>
<tr><td style="background-color:#FFF;border-color:#ffffff;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">2</span>  </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">MODEL_CODE</span>   </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">WEEK_INFO</span>   </td>
<td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">WEEK_INFO</span>   </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">WEEK_INFO</span>   </td></tr>
<tr><td style="background-color:#FFF;border-color:#ffffff;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">3</span>   </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">VISIT_CNT</span>   </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">MODEL_CODE</span>   </td>
<td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">MODEL_CODE</span>   </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">MODEL_CODE</span>   </td></tr>
<tr><td style="background-color:#FFF;border-color:#ffffff;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">4</span> </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">ATC_CNT</td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">VISIT_CNT</span>   </td>
<td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">PRODUCT_LEVEL</span>   </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">IMPORTANT FEATURE1</span>   </td></tr>
<tr><td style="background-color:#FFF;border-color:#ffffff;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">5 </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">CHECKOUT_CNT</span></td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">ATC_CNT</span>   </td>
<td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">TRAFFIC_TYPE</span>   </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal">I<span style="color:black">MPORTANT FEATURE2</span>   </td></tr>
<tr><td style="background-color:#FFF;border-color:#ffffff;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">6</span> </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"> <span style="color:black">TRAFFIC_SOURCE</span>   </td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">CHECKOUT_CNT</span>   </td>
<td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"></td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:middle;word-break:normal"><span style="color:black">IMPORTANT FEATURE3</span>   </td></tr>
</thead></table>

🔍 we provide a [development guide](http://mod.lge.com/hub/cx-llm/dx_d2c) for those who wish to participate in the implementation of DX Automation for D2C services.

This service currently allows inquiries about **Web Behavior inforation of customers on the UK OBS site from November 2024 to February 2025.**
"""
}

# 대표 질문 리스트
SAMPLE_QUESTIONS = {
    "ko":[
    "2024년 11월 둘째 주 대비 2024년 11월 셋째 주 AV 제품군의 Funnel 현황을 비교해줘.",
    "2024년 11월 둘째 주 대비 2024년 11월 셋째 주 AV 제품군의 ATC가 줄어든 원인이 어떻게 되나요?",
    "2024년 11월 둘째 주 대비 2024년 11월 셋째 주 AV 제품군의 ATC 감소 원인의 해결 방안은 무엇인가요?",
    "2024년 11월 둘째 주 대비 2024년 11월 셋째 주 AV 제품군의 유입채널별 트래픽 현황은 어떻게 되나요?",
    "2024년 11월 둘째 주 대비 그 다음주의 모니터 제품군 display 트래픽이 감소한 원인은 무엇인가요?",
    "2024년 11월 둘째 주 대비 그 다음주의 모니터 제품군 display 트래픽 감소 원인의 해결 방안은 무엇인가요?",
    ], 
    "en":[
    "Please conduct a Fallout analysis for the monitor product line comparing the second week of November 2024 to the third week of November 2024.",
    "What are the reasons for the decrease in ATC for the monitor product line comparing the second week of November 2024 to the third week of November 2024?",
    "What are the solutions to address the causes of the ATC decrease for the monitor product line comparing the second week of November 2024 to the third week of November 2024?",
    "What is the traffic status by inflow channel for the monitor product line comparing the second week of November 2024 to the third week of November 2024?",
    "What are the reasons for the decrease in display traffic for the monitor product line comparing the second week of November 2024 to the third week of November 2024?",
    "What are the solutions to address the causes of the display traffic decrease for the monitor product line comparing the second week of November 2024 to the third week of November 2024?"
    ]
}

# # 기본 API 엔드포인트
# api_endpoint = "https://dx-d2c-cloud-service.mkdev-kic.intellytics.lge.com/api/sales_chat" #os.environ.get("API 엔드포인트", "http://localhost:8667/api/sales_chat")
# reset_endpoint = "https://dx-d2c-cloud-service.mkdev-kic.intellytics.lge.com/api/reset_chat" #os.environ.get("API 엔드포인트", "http://localhost:8667/api/reset_chat")

api_endpoint = f"http://dx-d2c-demo-service.{os.getenv('ROOT_DOMAIN')}/api/fallout_chat"
reset_endpoint = f"http://dx-d2c-demo-service.{os.getenv('ROOT_DOMAIN')}/api/reset_chat"
feedback_api_endpoint = f"http://dx-d2c-demo-service.{os.getenv('ROOT_DOMAIN')}/api/get_langsmith_feedback"
# api_endpoint = st.text_input("API 엔드포인트", value="http://localhost:8081/ask")

# ==== Sidebar 화면 정보 ====
# SIDEBAR_INFO = "### 서비스 안내"
# HTML 문법 가능
SIDEBAR_SEARCHING_GUIDE = {
    "ko":"""
OBS 매출현황에서 이슈(매출하락 등)에 대해서 Funnel 및 유입 채널 관점에서 원인을 분석하고 해결방안을 찾아볼 수 있습니다.
""",
    "en":"""
You can analyze the causes of issues (such as sales decline) from the perspective of the funnel and inflow channels in the OBS sales status and find solutions.       
"""
}

sample_questions_description = {
    "ko": "Fallout Analysis에서 자주묻는질문(FAQ)들을 아래에서 참고하세요.",
    "en": "You can refer to the frequently asked questions (FAQ) below about Fallout Analysis."
}

# ========================================
# ======= 유틸 함수 =======
def show_dataframes(df_list):
    if not df_list:
        return
    for df in df_list:
        try:
            if len(df) > 1:             
                st.dataframe(df, use_container_width=True)        
        except:
            pass

def collect_feedback(run_id):    
    if run_id is None:
        return
    
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
            comment="None"

        feedback_type_str = list(score_mappings.keys())[0]

        requests.post(
            feedback_api_endpoint, 
            params={'run_id':run_id, 'feedback_type_str':feedback_type_str, 
                    'score':score, 'comment':comment} # llo qpi 규칙상 입출력 있어야하기 때문에 작성한 dummy
        )


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
def ask_llm_api(endpoint, query, language="ko", nation=None):
    try:
        lang_dict = {"ko": "Korean", "en": "English"}
        # API 요청 데이터 준비
        params = {
            "query": query
        }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "context": {
                "thread_id": st.session_state[f"{SERVICE_ID}_thread_id"],
                "target_language": lang_dict[language],
                "nation": "UK"
            },
            "options": {}
        }
        
        # API 호출
        response = requests.post(api_endpoint, headers=headers, params=params, data=json.dumps(data), timeout=60)
        if response.status_code == 200:
            return {"success": True, "data": response.json()['data']}
        else:
            return {
                "success": False, 
                "error": f"API 오류: {response.status_code}", 
                "details": "detail"
            }
        
        return {"success": True, "data": response.json()['data']} 
            
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
        st.session_state[f"{SERVICE_ID}_thread_id"] = str(uuid.uuid4())
        requests.post(reset_endpoint, params = {"thread_id":st.session_state[SERVICE_ID+'_thread_id']})
        st.rerun()
    
    st.divider()
    
    info_text = {"ko": "이 애플리케이션은 **Intellytics**에 배포된 LLM API를 사용합니다.", "en": "The Application uses LLM API distributed by **Intellytics**"}
    version_text = "© 2025 DX Automation for D2C | Ver 1.0"
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
        with chat_container.chat_message("assistant"):
            st.markdown(response['content'])
        st.session_state[f'{SERVICE_ID}_messages'].append({"role": "assistant", "content": response})
    else:
        response = result.get("data", {}).get("final_answer", "응답을 받지 못했습니다.")
        run_id=result.get("data", {}).get("run_id", None)
        
        # 복합 응답 객체 생성
        combined_content = {
            "text": response['content'],
            "tables": []
        }
        
        # 테이블이 있으면 추가
        if "generated_tables" in result['data']:
            df_list = [pd.read_json(StringIO(dic)) for dic in result['data']['generated_tables']['content']]
            combined_content["tables"] = df_list
        
        # 세션에 단일 메시지로 추가
        st.session_state[f'{SERVICE_ID}_messages'].append({"role": "assistant", "content": combined_content})
        
        # 현재 응답 표시 - 테이블 먼저 표시
        with chat_container.chat_message("assistant"):
            if combined_content["tables"]:
                show_dataframes(combined_content["tables"])
            st.markdown(combined_content["text"])
         
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
                const element = document.querySelector(selector);
                if (element) {
                    // 스크롤 가능한 부모 요소 찾기
                    let parent = element;
                    while (parent && getComputedStyle(parent).overflowY !== 'auto' && parent !== document.body) {
                        parent = parent.parentElement;
                    }
                    return parent || element;
                }
            }
            
            // 최후의 수단: 메인 컨테이너 반환
            return document.querySelector('.main') || document.body;
        }
        
        function scrollToBottom() {
            const chatContainer = findChatContainer();
            if (chatContainer) {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        }
        
        // 즉시 스크롤 실행
        scrollToBottom();
        
        // 여러 시점에 스크롤 실행
        setTimeout(scrollToBottom, 100);
        setTimeout(scrollToBottom, 300);
        setTimeout(scrollToBottom, 500);
        setTimeout(scrollToBottom, 1000);
        </script>
        """,
        height=0,
        width=0,
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
    # for message in st.session_state[f'{SERVICE_ID}_messages']:
    #     if isinstance(message["content"], list): # 현재 list로 반환받는건 df_list 밖에 없음
    #         show_dataframes(message["content"], message["role"])
    #     else:
    #         with st.chat_message(message["role"]):
    #             st.markdown(message["content"])
    
    for message in st.session_state[f'{SERVICE_ID}_messages']:
        with st.chat_message(message["role"]):
            if isinstance(message["content"], dict) and "text" in message["content"]:
                # 복합 콘텐츠 (테이블 + 텍스트) - 테이블 먼저 표시
                if "tables" in message["content"] and message["content"]["tables"]:
                    show_dataframes(message["content"]["tables"])
                st.markdown(message["content"]["text"])
            elif isinstance(message["content"], list):  
                # 기존 형식 지원 (df_list)
                show_dataframes(message["content"])
            else:
                # 텍스트만 있는 경우
                st.markdown(message["content"])
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
                    const element = document.querySelector(selector);
                    if (element) {
                        // 스크롤 가능한 부모 요소 찾기
                        let parent = element;
                        while (parent && getComputedStyle(parent).overflowY !== 'auto' && parent !== document.body) {
                            parent = parent.parentElement;
                        }
                        return parent || element;
                    }
                }
                
                // 최후의 수단: 메인 컨테이너 반환
                return document.querySelector('.main') || document.body;
            }
            
            function scrollToBottom() {
                const chatContainer = findChatContainer();
                if (chatContainer) {
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }
            }
            
            // 즉시 스크롤 실행
            scrollToBottom();
            
            // 여러 시점에 스크롤 실행
            setTimeout(scrollToBottom, 100);
            setTimeout(scrollToBottom, 300);
            setTimeout(scrollToBottom, 500);
            setTimeout(scrollToBottom, 1000);
            </script>
            """,
            height=0,
            width=0,
        )

# # 페이지 끝에 여백 추가 (입력창이 메시지를 가리지 않도록)
# st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

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

# 페이지 로드 시 사이드바 너비를 자바스크립트로 조정
st.markdown("""
<script>
    // 페이지 로드 시 즉시 사이드바 너비 설정
    (function() {
        function setSidebarWidth() {
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {
                sidebar.style.minWidth = '350px';
                sidebar.style.maxWidth = '350px';
                sidebar.style.width = '350px';
                sidebar.style.transition = 'none';
            }
        }
        
        // 즉시 실행
        setSidebarWidth();
        
        // DOM 로드 후 실행
        document.addEventListener('DOMContentLoaded', setSidebarWidth);
        
        // 약간의 지연 후 다시 실행 (Streamlit이 DOM을 조작한 후)
        setTimeout(setSidebarWidth, 100);
        setTimeout(setSidebarWidth, 300);
    })();
</script>
""", unsafe_allow_html=True)

# Enter 키로 채팅 메시지 전송 기능
st.markdown("""
<script>
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        const chatInput = document.querySelector('.stChatInput input');
        if (document.activeElement === chatInput && chatInput.value.trim() !== '') {
            const sendButton = document.querySelector('.stChatInput button');
            if (sendButton) {
                sendButton.click();
            }
        }
    }
});
</script>
""", unsafe_allow_html=True)
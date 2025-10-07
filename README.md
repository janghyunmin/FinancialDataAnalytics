# FinancialDataAnalytics

<h1> 📘 금융데이터분석 – Homework 1 </h1>

주제: Global Compustat 데이터를 활용한 국가별 월별 수익률 분석 (2020–2025)
도구: Python + WRDS + pandas
목표: Global Compustat 데이터를 이용해 기업별·국가별 월간 주식 수익률을 생성하고,
선진국과 신흥국 간의 수익률 특성을 비교한다.

<h1> 📂 프로젝트 구조 </h1>
<br>
<img width="520" height="306" alt="image" src="https://github.com/user-attachments/assets/b52e56e5-cd41-4eda-b9e1-06bfaeb22ae7" />


-------
<h2> 🚀 전체 워크플로우 요약 </h2>
<h3> ✅ 1. WRDS 연결 (connectModule.py) </h3>

1. wrds.Connection()을 통해 WRDS Global Compustat 서버에 연결
2. Compustat 라이브러리 내 테이블 목록을 확인 (g_secm 사용)
3. WRDS 사용자 정보는 .env 파일을 통해 자동 로드

conn = WRDSConnection()        # WRDS 연결
FindTables(conn)               # Compustat 테이블 목록 확인

<h3> ✅ 2. 데이터 수집 (collectModule.py) </h3>

comp.g_secm 테이블에서 기업별 월말 데이터를 불러옴

분석 대상 10개국
🇬🇧 영국 | 🇩🇪 독일 | 🇯🇵 일본 | 🇫🇷 프랑스 | 🇦🇺 호주
🇨🇳 중국 | 🇮🇳 인도 | 🇧🇷 브라질 | 🇿🇦 남아프리카 | 🇹🇷 터키

기간: 2020-01-01 ~ 2025-09-30
결측치 제거 및 전처리 후 data/collectData.csv로 저장

| 컬럼명             | 의미                     |
| --------------- | ---------------------- |
| 'gvkey', 'iid'  | 기업 및 증권 식별자            |
| 'datadate'      | 데이터 기준 월말 날짜           |
| 'loc', 'fic'    | 상장국가 / 법인등록국가          |
| 'prccm'         | 월말 주가 (local currency) |
| 'cshtrm'        | 월간 거래주식수               |
| 'ajexm', 'ajpm' | 조정계수 (배당·분할용, 대부분 1.0) |
| 'curcdm'        | 통화코드                   |
| 'country'       | 상장국가 기준 코드             |


<img width="665" height="299" alt="image" src="https://github.com/user-attachments/assets/ef432d2e-ce75-430c-a24b-0c9fcb379c07" />
<img width="579" height="75" alt="image" src="https://github.com/user-attachments/assets/aa7330b0-6300-48e1-90d2-3b73aaadbf23" />
<img width="807" height="208" alt="image" src="https://github.com/user-attachments/assets/48b30729-900c-4819-a44f-039bd0fc7b1f" />

<h3> 결과 파일: data/outPutData.csv</h3>

| country | datadate   | ew_return | vw_return |
| ------- | ---------- | --------- | --------- |
| JPN     | 2020-03-31 | -0.045    | -0.042    |
| GBR     | 2020-03-31 | -0.031    | -0.028    |
| AUS     | 2020-03-31 | -0.055    | -0.059    |


<h3> ✅ 4. 기간 정의 (Problem 3 – Period Definition) </h3>

목표:
분석 샘플을 두 개의 하위 기간으로 구분하여,
코로나19 위기 시기와 이후 회복 시기의 시장 움직임을 비교할 수 있도록 period 컬럼을 생성합니다.

| 구분                                           | 기간                   | 라벨           |
| -------------------------------------------- | -------------------- | ------------ |
| **COVID-19 위기 기간 (Crisis Period)**           | 2020년 3월 ~ 2021년 12월 | `"Crisis"`   |
| **위기 후 회복 기간 (Post-Crisis Recovery Period)** | 2022년 1월 ~ 2024년 12월 | `"Recovery"` |

✅ 데이터 로드 완료: 994행
💾 기간 라벨 추가 완료: data/outPutData_withPeriod.csv

📊 기간별 데이터 분포:
Recovery    537
Crisis      308
Other       149
Name: count, dtype: int64



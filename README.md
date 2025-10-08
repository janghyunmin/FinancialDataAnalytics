# FinancialDataAnalytics

<h1> 📘 금융데이터분석 – Homework 1 </h1>

주제: Global Compustat 데이터를 활용한 국가별 월별 수익률 분석 (2020–2025) <br>
도구: Python + WRDS + pandas <br>
목표: Global Compustat 데이터를 이용해 기업별·국가별 월간 주식 수익률을 생성하고, 선진국과 신흥국 간의 수익률 특성을 비교한다. <br>

<h1> 📂 프로젝트 구조 </h1>

```markdown
project
├── data
│   ├── collectData.csv ✅ 데이터 수집 완료 (collectData.csv)  
│   ├── outputData.csv ✅ 국가별 수익률 계산 완료 (outputData.csv)  
│   ├── outputDataCovid.csv ✅ 기간 라벨 정의 완료 (outputDataCovid.csv)  
│   └── outputDataSummary.csv ✅ 국가·기간별 기술통계 요약 완료 (outputDataSummary.csv)  
│   
├── subject
    ├── main.py
    ├── connectModule.py ✅ WRDS 연결 및 데이터 수집 (connectModule, collectModule)
    ├── collectModule.py ✅ WRDS 연결 및 데이터 수집 (connectModule, collectModule)
    ├── analyzeModule.py ✅ 국가별 수익률 계산 및 EW/VW 집계 (analyzeModule)
    ├── comparisonModule.py ✅ 선진국 vs 신흥국 비교 분석 (comparisonModule)
    ├── periodModule.py ✅ Covid-19 기간 라벨 정의 (periodModule)
    ├── summaryModule.py ✅ 국가·기간별 통계 요약 (summaryModule)
    └── outputDataModule.py ✅ outputData.csv 파일 검증용
```
<br>
<h2> 🚀 전체 워크플로우 요약 </h2>
<h3> ✅ 1. WRDS 연결 (connectModule.py) </h3> <br>

1. wrds.Connection()을 통해 WRDS Global Compustat 서버에 연결 <br>
2. Compustat 라이브러리 내 테이블 목록을 확인 (g_secm 사용) <br> 
3. WRDS 사용자 정보는 .env 파일을 통해 자동 로드 <br>

conn = WRDSConnection()        # WRDS 연결 <br>
FindTables(conn)               # Compustat 테이블 목록 확인 <br>

<h3> ✅ 2. 데이터 수집 (collectModule.py) </h3> <br>

comp.g_secm 테이블에서 기업별 월말 데이터를 불러옴 <br>

분석 대상 10개국 <br>
🇬🇧 영국 | 🇩🇪 독일 | 🇯🇵 일본 | 🇫🇷 프랑스 | 🇦🇺 호주 <br>
🇨🇳 중국 | 🇮🇳 인도 | 🇧🇷 브라질 | 🇿🇦 남아프리카 | 🇹🇷 터키 <br>

기간: 2020-01-01 ~ 2025-09-30 <br>
결측치 제거 및 전처리 후 data/collectData.csv로 저장 <br>

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

<h3> ✅ 5. 국가 및 기간별 요약 통계 (Problem 4 – Summary Statistics by Country and Period) </h3>

목표:
각 국가(country)와 기간(period: Crisis / Recovery)별로
수익률(ew_return, vw_return)의 분포 특성을 통계적으로 요약한다.

이를 통해 코로나19 위기기와 회복기 사이의 수익률 수준, 변동성, 분포 특성의 차이를 비교한다.
<img width="668" height="406" alt="image" src="https://github.com/user-attachments/assets/c7b7c780-33c9-4463-9929-bdc84fde94d8" />
<img width="660" height="281" alt="image" src="https://github.com/user-attachments/assets/b7ab5abd-8bea-4242-a514-a209275a0d79" />



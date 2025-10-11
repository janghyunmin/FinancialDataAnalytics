<h1>📘 금융데이터분석 – Homework 1</h1>

<b>주제:</b> Global Compustat 데이터를 활용한 국가별 월별 수익률 분석 (2020–2025) <br>
<b>도구:</b> Python + WRDS + pandas <br>
<b>목표:</b> Global Compustat 데이터를 이용해 기업별·국가별 월간 주식 수익률을 생성하고, 선진국과 신흥국 간의 수익률 특성을 비교한다. <br>

<hr>

<h1>📂 프로젝트 구조</h1>

```markdown
project
├── data
│   ├── collectData.csv ✅ 데이터 수집 완료 (Problem 1)
│   ├── outputData.csv ✅ 국가별 수익률 계산 완료 (Problem 2)
│   ├── outputDataCovid.csv ✅ 기간 라벨 정의 완료 (Problem 3)
│   ├── outputDataSummary.csv ✅ 국가·기간별 통계 요약 완료 (Problem 4)
│   └── comparison_developed_vs_emerging.csv ✅ 선진국 vs 신흥국 비교 완료 (Problem 5)
│
├── subject
│   ├── main.py
│   ├── connectModule.py ✅ WRDS 연결 및 테이블 탐색
│   ├── collectModule.py ✅ 데이터 수집 (Compustat g_secm)
│   ├── analyzeModule.py ✅ 국가별 수익률 계산 (EW/VW)
│   ├── periodModule.py ✅ 기간 라벨 정의 (Crisis/Recovery)
│   ├── summaryModule.py ✅ 기술통계 산출
│   ├── comparisonModule.py ✅ Developed vs Emerging 비교
│   └── outputDataModule.py ✅ 결과 검증용
```

<hr> <h2>🧩 Problem 1. Data Collection (데이터 수집)</h2>

<b>목표:</b> Global Compustat 데이터베이스에서 10개국 기업의 월별 데이터를 수집한다. <br>

<b>대상국가 (MSCI 기준):</b> <br>
🇬🇧 영국 | 🇩🇪 독일 | 🇯🇵 일본 | 🇫🇷 프랑스 | 🇦🇺 호주 <br>
🇨🇳 중국 | 🇮🇳 인도 | 🇧🇷 브라질 | 🇿🇦 남아프리카 | 🇹🇷 터키 <br>

<b>기간:</b> 2020년 3월 ~ 2024년 12월 <br>

<b>사용 모듈:</b> connectModule.py, collectModule.py <br>

<b>주요 컬럼:</b> <br>
| 컬럼명         | 의미                     |
| ----------- | ---------------------- |
| gvkey, iid  | 기업 및 증권 식별자            |
| datadate    | 데이터 기준 월말 날짜           |
| loc, fic    | 상장국가 / 법인등록국가          |
| prccm       | 월말 주가 (local currency) |
| cshtrm      | 월간 거래주식수               |
| ajexm, ajpm | 조정계수 (배당·분할용, 대부분 1.0) |
| curcdm      | 통화코드                   |
| country     | 상장국가 코드 (loc/fic 기준)   |

<<<<<<< Updated upstream
💾 <b>저장:</b> data/collectData.csv <br>
=======
기간: 2020-03-01 ~ 2024-12-31
결측치 제거 및 전처리 후 data/collectData.csv로 저장
>>>>>>> Stashed changes

<hr> <h2>🧮 Problem 2. Return Generating Process (수익률 생성)</h2>

<b>목표:</b> <br>
1️⃣ 기업별 월별 수익률 계산 <br>
2️⃣ 시가총액 산출 (Market Cap = prccm × cshtrm) <br>
3️⃣ 국가별 월간 수익률 구성 (EW/VW) <br>

EW (Equally Weighted) : 모든 기업 동일 비중 <br>

VW (Value Weighted) : 시가총액 기준 가중평균 <br>

💾 <b>결과 저장:</b> data/outputData.csv <br>
| country | datadate   | ew_return | vw_return |
| ------- | ---------- | --------- | --------- |
| JPN     | 2020-03-31 | -0.045    | -0.042    |
| GBR     | 2020-03-31 | -0.031    | -0.028    |
| AUS     | 2020-03-31 | -0.055    | -0.059    |

<hr> <h2>🗓️ Problem 3. Period Definition (기간 정의)</h2>

<b>목표:</b> 분석 샘플을 두 개의 하위 기간으로 구분한다. <br>
| 구분                             | 기간                   | 라벨         |
| ------------------------------ | -------------------- | ---------- |
| COVID-19 위기 기간 (Crisis Period) | 2020년 3월 ~ 2021년 12월 | "Crisis"   |
| 위기 후 회복 기간 (Recovery Period)   | 2022년 1월 ~ 2024년 12월 | "Recovery" |

💾 <b>결과 저장:</b> data/outputDataCovid.csv <br>

📊 <b>기간별 데이터 분포:</b> <br>
Recovery 537<br>
Crisis 308<br>
Other 149<br>

<hr> <h2>📊 Problem 4. Summary Statistics by Country and Period</h2>

<b>목표:</b> 각 국가(country)와 기간(period: Crisis / Recovery)별로 수익률(ew_return, vw_return)의 분포를 통계적으로 요약한다. <br>

<b>계산 항목:</b> 평균(mean), 중앙값(median), 표준편차(std), 최소/최대(min/max), 자기상관(autocorr), 왜도(skewness), 초과첨도(kurtosis) <br>

💾 <b>결과 저장:</b> data/outputDataSummary.csv <br>
                                            | country | period   | ew_mean | ew_std | ew_skew | ew_kurtosis |
| ------- | -------- | ------- | ------ | ------- | ----------- |
| AUS     | Crisis   | -0.031  | 0.045  | 0.56    | 1.15        |
| JPN     | Recovery | 0.018   | 0.041  | -0.10   | 0.72        |

<hr> <h2>🌍 Problem 5. Developed vs Emerging Comparative Analysis</h2>

<b>목표:</b> 선진국(Developed)과 신흥국(Emerging) 그룹 간의 수익률, 변동성, 분포 특성을 비교한다. <br>

💾 <b>결과 저장:</b> data/comparison_developed_vs_emerging.csv <br>
| 구분        | 기간       | 평균 수익률 (ew_mean) | 표준편차 (ew_std) | 왜도 (ew_skew) | 초과첨도 (ew_excess_kurtosis) |
| --------- | -------- | ---------------- | ------------- | ------------ | ------------------------- |
| Developed | Crisis   | -0.028           | 0.081         | 0.54         | 1.12                      |
| Emerging  | Crisis   | -0.053           | 0.114         | 0.87         | 2.45                      |
| Developed | Recovery | 0.015            | 0.043         | -0.12        | 0.69                      |
| Emerging  | Recovery | 0.019            | 0.065         | -0.09        | 1.08                      |

<b>※ 모든 수치는 월간 수익률 기준 (1 = 100%)</b> <br>
Crisis = 코로나19 위기기, Recovery = 위기 후 회복기 <br>

<h3>(a) 평균 비교</h3> - Crisis 시기: Emerging(-5.3%) < Developed(-2.8%) → 신흥국의 손실이 더 큼 <br> - Recovery 시기: Emerging(1.9%) > Developed(1.5%) → 신흥국의 반등 폭이 더 큼 <br> <h3>(b) 변동성 및 분포 특성</h3> - 신흥국의 표준편차(0.114)가 선진국(0.081)보다 높음 → 변동성 더 큼 <br> - 왜도·첨도 모두 높음 → 극단적 수익률 빈도 높음 (fat-tail) <br> <h3>(c) 회복 역학</h3> - 선진국: 안정적이고 점진적인 회복 <br> - 신흥국: 리스크는 크지만 빠른 반등세 <br> <hr> <h2>📈 결론 요약</h2>
 
| 항목     | Crisis (2020–2021)             | Recovery (2022–2024) | 비교 요약          |
| ------ | ------------------------------ | -------------------- | -------------- |
| 평균 수익률 | Emerging < Developed           | Emerging > Developed | 신흥국의 반등 폭이 더 큼 |
| 변동성    | Emerging > Developed           | 여전히 높음               | 신흥국 변동성 지속     |
| 왜도/첨도  | Emerging > Developed           | 감소                   | 분포 안정화 진행      |
| 요약     | 신흥국은 위기 시 더 큰 충격, 회복 시 더 빠른 반등 | 선진국은 안정적 회복          | 구조적 리스크 차이     |


<hr> <h2>💾 출력 파일 구조</h2>

| 파일명                                  | 내용                        |
| ------------------------------------ | ------------------------- |
| collectData.csv                      | Compustat 원본 수집 데이터       |
| outputData.csv                       | 국가별 월별 수익률 계산 결과          |
| outputDataCovid.csv                  | 기간 라벨(Crisis/Recovery) 정의 |
| outputDataSummary.csv                | 국가·기간별 통계 요약              |
| comparison_developed_vs_emerging.csv | 선진국 vs 신흥국 비교 분석 결과       |

<hr> <h2>🧩 인사이트</h2>

신흥국 시장은 위기 시 높은 변동성을 보이지만, <br>
회복기에는 더 빠른 성장세를 보인다. <br>
반면 선진국은 안정적이지만 상대적으로 완만한 회복을 기록한다. <br>
이는 글로벌 자금 유입과 위험회피 성향의 구조적 차이를 반영한다. <br>


<hr>

<h2>📈 Problem 6. Correlation and Spillover Effects (상관관계 및 파급효과 분석)</h2>

<b>목표:</b> 코로나19 위기(Crisis)와 회복(Recovery) 시기별로 국가 간 월별 수익률의 상관관계를 계산하고,  
선진국(Developed)과 신흥국(Emerging) 그룹 간의 평균 상관 수준을 비교한다. <br>

<b>분석 파일:</b> data/outputDataCovid.csv <br>
<b>결과 파일:</b> data/correlation_crisis.csv, data/correlation_recovery.csv, data/correlation_summary.csv <br>

---

<h3>📊 (a) Crisis / Recovery 기간별 상관행렬 계산</h3>

- 각 기간별로 국가 간 EW 수익률(`ew_return`)을 이용해 Pearson 상관계수를 계산함.  
- Crisis(2020.03–2021.12) / Recovery(2022.01–2024.12)로 구분하여 상관행렬을 생성.  

예시 (Crisis 기간 – Developed 5개국):
|        | JPN | GBR | FRA | AUS | DEU |
|--------|-----|-----|-----|-----|-----|
| **JPN** | 1.00 | 0.82 | 0.78 | 0.69 | 0.81 |
| **GBR** | 0.82 | 1.00 | 0.83 | 0.71 | 0.79 |
| **FRA** | 0.78 | 0.83 | 1.00 | 0.68 | 0.77 |
| **AUS** | 0.69 | 0.71 | 0.68 | 1.00 | 0.73 |
| **DEU** | 0.81 | 0.79 | 0.77 | 0.73 | 1.00 |

---

<h3>📈 (b) 그룹별 평균 상관계수 비교</h3>

| 그룹 | Crisis 평균 상관계수 | Recovery 평균 상관계수 |
|------|---------------------|-----------------------|
| Developed | 0.78 | 0.63 |
| Emerging  | 0.65 | 0.54 |

- Crisis 기간 동안 상관계수가 전반적으로 상승 → 국가 간 시장 동조화 강화  
- Recovery 기간에는 상관계수가 하락 → 각 시장이 독립적 회복 경로로 이동  
- Developed 그룹은 구조적으로 높은 연계성 유지, Emerging 그룹은 변동성이 상대적으로 큼  

---

<h3>💬 (c) 금융 전이(Contagion) 현상 해석</h3>

- 코로나19 위기(Crisis) 기간에는 시장 간 동조화가 급격히 높아져  
  **금융 전이(Contagion) 현상**이 관찰됨.  
- 글로벌 위험요인(Global Risk Factor)에 의한 공동 충격으로  
  선진국 간 상관성이 특히 상승함.  
- 신흥국은 자금 유출입 불안정성으로 인해 상관성이 높아지기도 하지만,  
  일부 국가는 독립적인 움직임을 보임.  
- 회복기(Recovery)에는 상관성이 완화되며, 시장별 차별화된 회복 패턴이 나타남.

---

<h3>📘 요약</h3>

| 구분 | 특징 | 해석 |
|------|------|------|
| Crisis (2020–2021) | 상관계수 급등 | 금융시장 간 동조화 강화, 전이 효과 발생 |
| Recovery (2022–2024) | 상관계수 완화 | 시장 정상화 및 독립적 회복 |
| Developed | 높은 구조적 연계성 | 글로벌 요인에 민감하게 반응 |
| Emerging | 높은 변동성, 부분 동조화 | 자금 흐름에 따른 이질적 반응 |

---

<h3>💾 결과 파일 요약</h3>

| 파일명 | 설명 |
|--------|------|
| correlation_crisis.csv | Crisis 기간 국가 간 수익률 상관행렬 |
| correlation_recovery.csv | Recovery 기간 국가 간 수익률 상관행렬 |
| correlation_summary.csv | 그룹별 평균 상관계수 비교 요약표 |

---

<h2>🧠 인사이트</h2>

> 코로나19 위기 동안에는 시장 간 동조화가 강화되며  
> 금융 전이(Contagion) 현상이 발생했다. <br>
> 회복기에는 상관성이 완화되고, 각 시장은 독립적인 회복 흐름을 보였다. <br>
> 이는 글로벌 유동성과 위험회피 성향이  
> 시장 간 연계성의 변화를 주도했음을 시사한다. <br>





"""
문제 2. 반환 생성 프로세스
(a) 수집된 데이터를 사용하여 기업 수준의 월간 주식 수익률을 생성합니다.
(b) 기업 수준의 시가총액을 계산합니다.
(c) 국가별 월간 수익률 구성:
• 균등 가중 (EW) 수익률
• 가치 가중(VW) 수익률(기업 시가총액을 가중치로 사용).
"""
# -----------------------
# 문제 2: Return Generating Process
# -----------------------

# analyzeModule.py
import pandas as pd
import numpy as np
import os

def GenerateReturns():
    # -----------------------
    # 1) 데이터 불러오기
    # -----------------------
    input_path = "data/collectData.csv"   # 입력 파일명
    df = pd.read_csv(input_path)
    print(f"원본 데이터 로드 완료: {len(df):,}행")

    # 날짜 정리
    df["datadate"] = pd.to_datetime(df["datadate"], errors="coerce")
    df = df.sort_values(["gvkey", "iid", "datadate"])

    # -----------------------
    # (a) 조정가격 및 월별 수익률 계산
    # -----------------------
    df["adj_price"] = df["prccm"] * df["ajpm"] / df["ajexm"]
    df["adj_price"] = df["adj_price"].replace([np.inf, -np.inf, 0], np.nan)

    # 월별 수익률 계산
    df["ret"] = df.groupby(["gvkey", "iid"])["adj_price"].pct_change()
    df["ret"] = df["ret"].replace([np.inf, -np.inf], np.nan)

    print("월별 수익률 계산 완료")

    # -----------------------
    # (b) 시가총액 계산
    # -----------------------
    df["market_cap"] = df["prccm"] * df["cshtrm"]
    print("시가총액 계산 완료")

    # -----------------------
    # (c) 국가별 EW/VW 월별 수익률 계산
    # -----------------------
    df = df.dropna(subset=["ret", "market_cap", "country"])

    # 균등가중 수익률
    ew = df.groupby(["country", "datadate"])["ret"].mean().reset_index()
    ew = ew.rename(columns={"ret": "ew_return"})

    # 가치가중 수익률
    vw_list = []
    for (country, date), group in df.groupby(["country", "datadate"]):
        if group["market_cap"].sum() > 0:
            vw_ret = np.average(group["ret"], weights=group["market_cap"])
            vw_list.append([country, date, vw_ret])

    vw = pd.DataFrame(vw_list, columns=["country", "datadate", "vw_return"])

    # 타입 통일 (datetime)
    ew["datadate"] = pd.to_datetime(ew["datadate"])
    vw["datadate"] = pd.to_datetime(vw["datadate"])

    # 병합
    merged = pd.merge(ew, vw, on=["country", "datadate"], how="outer")

    # -----------------------
    # 저장
    # -----------------------
    os.makedirs("data", exist_ok=True)
    output_path = "data/outputData.csv"  # 출력 파일명
    merged.to_csv(output_path, index=False)

    print(f"국가별 수익률 요약 저장 완료: {output_path}")
    print("\n미리보기:")
    print(merged.head())

    return merged

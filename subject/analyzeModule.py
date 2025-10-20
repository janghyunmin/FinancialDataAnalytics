# ---------------------------------------
# 📈 문제 2. 수익률 생성 및 국가별 집계 (Market Cap 수정 버전)
# ---------------------------------------

import pandas as pd
import numpy as np
import os

def GenerateReturns():
    input_path = "data/collectData.csv"
    output_path = "data/outputData.csv"

    print("📥 데이터 불러오는 중...")
    df = pd.read_csv(input_path)

    # ------------------------------
    # 1️⃣ 기본 전처리
    # ------------------------------
    df["datadate"] = pd.to_datetime(df["datadate"], errors="coerce")

    # 조정계수 결측 처리
    df["ajexm"] = df["ajexm"].replace(0, np.nan).fillna(1)
    df["ajpm"] = df["ajpm"].replace(0, np.nan).fillna(1)

    # ------------------------------
    # 2️⃣ 조정주가 계산
    # ------------------------------
    df["adj_price"] = df["prccm"] * (df["ajpm"] / df["ajexm"])

    # ------------------------------
    # 3️⃣ 월간 수익률 계산
    # ------------------------------
    df = df.sort_values(["gvkey", "datadate"])
    df["return"] = df.groupby("gvkey")["adj_price"].pct_change()

    # 비정상적 이상치 제거 (±100% 이상 변동은 제거)
    df.loc[df["return"].abs() > 1, "return"] = np.nan

    # ------------------------------
    # 4️⃣ 시가총액(Market Cap) 계산
    # ------------------------------
    if "csho" in df.columns:
        df["market_cap"] = df["adj_price"] * df["csho"]
        print("✅ Market Cap 계산 완료 (adj_price × csho)")
    else:
        raise KeyError("❌ 'csho' 컬럼이 없습니다. collectModule.py에서 발행주식수 데이터를 병합했는지 확인하세요.")

    # ------------------------------
    # 5️⃣ 결측치 제거
    # ------------------------------
    df = df.dropna(subset=["return", "market_cap", "country"])

    # ------------------------------
    # 6️⃣ 국가별 월별 수익률 집계
    # ------------------------------

    # (1) Equally Weighted (EW)
    ew = (
        df.groupby(["country", "datadate"])["return"]
        .mean()
        .reset_index(name="ew_return")
    )

    # (2) Value Weighted (VW)
    def weighted_avg(x):
        if x["market_cap"].sum() == 0:
            return np.nan
        return np.average(x["return"], weights=x["market_cap"])

    vw = (
        df.groupby(["country", "datadate"])
        .apply(weighted_avg)
        .reset_index(name="vw_return")
    )

    # ------------------------------
    # 7️⃣ EW/VW 병합 및 저장
    # ------------------------------
    country_returns = pd.merge(ew, vw, on=["country", "datadate"], how="inner")

    os.makedirs("data", exist_ok=True)
    country_returns.to_csv(output_path, index=False)

    print(f"💾 국가별 수익률 데이터 저장 완료: {output_path}")
    print("\n✅ 미리보기:")
    print(country_returns.head(10))

    return country_returns

# ---------------------------------------
# 📈 문제 2. 수익률 생성 및 국가별 집계 (정상화 버전)
# ---------------------------------------

import pandas as pd
import numpy as np
import os

def GenerateReturns():
    input_path = "data/collectData.csv"
    output_path = "data/outputData.csv"

    print("📥 데이터 불러오는 중...")
    df = pd.read_csv(input_path)

    # 날짜 변환
    df["datadate"] = pd.to_datetime(df["datadate"], errors="coerce")

    # ⚙️ 조정주가 계산
    # 일부 데이터는 ajexm / ajpm이 매우 커서 비정상적이므로 clip 적용
    df["ajexm"] = df["ajexm"].replace(0, np.nan).fillna(1)
    df["ajpm"] = df["ajpm"].replace(0, np.nan).fillna(1)

    df["adj_price"] = df["prccm"] * (df["ajpm"] / df["ajexm"])

    # ⚠️ 수익률 계산 (pct_change → 100배 방지)
    df = df.sort_values(["gvkey", "datadate"])
    df["return"] = df.groupby("gvkey")["adj_price"].pct_change()

    # 수익률이 너무 큰 이상치 제거
    df.loc[df["return"].abs() > 1, "return"] = np.nan

    # 시가총액 계산
    df["market_cap"] = df["adj_price"] * df["cshtrm"]

    # 🧹 결측치 제거
    df = df.dropna(subset=["return", "market_cap", "country"])

    # ------------------------------
    # 국가별 월별 수익률 집계
    # ------------------------------
    ew = df.groupby(["country", "datadate"])["return"].mean().reset_index(name="ew_return")
    vw = df.groupby(["country", "datadate"]).apply(
        lambda x: np.average(x["return"], weights=x["market_cap"])
    ).reset_index(name="vw_return")

    # ------------------------------
    # 병합 및 저장
    # ------------------------------
    country_returns = pd.merge(ew, vw, on=["country", "datadate"], how="inner")

    os.makedirs("data", exist_ok=True)
    country_returns.to_csv(output_path, index=False)
    print(f"💾 국가별 수익률 데이터 저장 완료: {output_path}")

    print("\n✅ 미리보기:")
    print(country_returns.head(10))

    return country_returns

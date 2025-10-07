# ---------------------------------------
# 국가 및 기간별 수익률 기술통계 요약
# ---------------------------------------

import pandas as pd
import numpy as np
import os

def SummaryStatistics():
    input_path = "data/outputDataCovid.csv"
    output_path = "data/outputDataSummary.csv"

    # 1. 데이터 로드
    df = pd.read_csv(input_path)
    df["datadate"] = pd.to_datetime(df["datadate"])
    print(f"✅ 데이터 로드 완료: {len(df):,}행")

    # 2. 분석 대상 필터링 (Crisis / Recovery만)
    df = df[df["period"].isin(["Crisis", "Recovery"])]

    # 3. 그룹별 통계 계산 함수 정의
    def calc_stats(x):
        # 결측 제거
        x = x.dropna()

        if len(x) < 2:
            return pd.Series({
                "mean": np.nan,
                "median": np.nan,
                "std": np.nan,
                "min": np.nan,
                "max": np.nan,
                "autocorr": np.nan,
                "skew": np.nan,
                "excess_kurtosis": np.nan
            })

        return pd.Series({
            "mean": np.mean(x),
            "median": np.median(x),
            "std": np.std(x, ddof=1),
            "min": np.min(x),
            "max": np.max(x),
            "autocorr": x.autocorr(lag=1),
            "skew": x.skew(),
            "excess_kurtosis": x.kurt()  # pandas.kurt() = excess kurtosis
        })

    # 4. 국가 & 기간별 요약 계산 (EW / VW 각각)
    grouped_ew = df.groupby(["country", "period"])["ew_return"].apply(calc_stats)
    grouped_vw = df.groupby(["country", "period"])["vw_return"].apply(calc_stats)

    # 5. MultiIndex 풀기
    ew_df = grouped_ew.reset_index()
    vw_df = grouped_vw.reset_index()

    # 6. 컬럼명 구분 추가
    ew_df = ew_df.add_prefix("ew_")
    vw_df = vw_df.add_prefix("vw_")

    # 7. 병합
    merged = pd.merge(
        ew_df,
        vw_df,
        left_on=["ew_country", "ew_period"],
        right_on=["vw_country", "vw_period"],
        suffixes=("_ew", "_vw")
    )

    # 8. 불필요한 중복 컬럼 제거 및 정리
    merged = merged.rename(columns={
        "ew_country": "country",
        "ew_period": "period"
    }).drop(columns=["vw_country", "vw_period"])

    # 9. 저장
    os.makedirs("data", exist_ok=True)
    merged.to_csv(output_path, index=False)
    print(f"국가 및 기간별 기술통계 저장 완료: {output_path}")

    print("\n 요약 미리보기:")
    print(merged.head())

    return merged

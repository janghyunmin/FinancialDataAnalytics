# ---------------------------------------
# 📊 국가 및 기간별 수익률 요약 통계 계산 (Problem 4)
# ---------------------------------------

import pandas as pd
import numpy as np
import os

def SummaryStatistics():
    input_path = "data/outputDataCovid.csv"   # 기간 구분된 수익률 파일
    output_path = "data/outputDataSummary.csv"

    print("📥 데이터 불러오는 중...")
    df = pd.read_csv(input_path)

    # datadate를 날짜형으로 변환
    df["datadate"] = pd.to_datetime(df["datadate"], errors="coerce")

    # 🧹 결측치 제거 (수익률 없으면 분석 불가)
    df = df.dropna(subset=["ew_return", "vw_return", "country", "period"])

    print(f"✅ 유효 데이터 수: {len(df):,}")

    # ------------------------------
    # 그룹 설정 (국가 × 기간)
    # ------------------------------
    grouped = df.groupby(["country", "period"])

    # ------------------------------
    # ① 동일가중(EW) 수익률 통계
    # ------------------------------
    ew_summary = grouped["ew_return"].agg(
        mean="mean",
        median="median",
        std="std",
        min="min",
        max="max",
        skew="skew"
    )

    # 초과첨도(kurtosis) + 자기상관계수(autocorr)
    ew_summary["excess_kurtosis"] = grouped["ew_return"].apply(pd.Series.kurt)
    ew_summary["autocorr"] = grouped["ew_return"].apply(lambda x: x.autocorr(lag=1))

    # prefix 추가
    ew_summary = ew_summary.add_prefix("ew_")

    # ------------------------------
    # ② 가치가중(VW) 수익률 통계
    # ------------------------------
    vw_summary = grouped["vw_return"].agg(
        mean="mean",
        median="median",
        std="std",
        min="min",
        max="max",
        skew="skew"
    )

    vw_summary["excess_kurtosis"] = grouped["vw_return"].apply(pd.Series.kurt)
    vw_summary["autocorr"] = grouped["vw_return"].apply(lambda x: x.autocorr(lag=1))
    vw_summary = vw_summary.add_prefix("vw_")

    # ------------------------------
    # ③ 결과 병합 및 저장
    # ------------------------------
    summary = pd.concat([ew_summary, vw_summary], axis=1).reset_index()

    os.makedirs("data", exist_ok=True)
    summary.to_csv(output_path, index=False)
    print(f"💾 국가 및 기간별 수익률 통계 저장 완료: {output_path}")

    print("\n📊 요약 미리보기:")
    print(summary.head())

    return summary

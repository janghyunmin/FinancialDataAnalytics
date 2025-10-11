# 통합 검증 스크립트 파일
# ---------------------------------------
# ✅ WRDS 데이터 파이프라인 검증 스크립트
# (collect → analyze → period → summary → compare)
# ---------------------------------------

import pandas as pd
import numpy as np
import os

# 데이터 파일 경로
paths = {
    "collect": "data/collectData.csv",
    "analyze": "data/outputData.csv",
    "period": "data/outputDataCovid.csv",
    "summary": "data/outputDataSummary.csv",
    "compare": "data/comparison_developed_vs_emerging.csv"
}

def check_file_exists(path):
    if os.path.exists(path):
        print(f"✅ {path} 파일 존재")
        return True
    else:
        print(f"❌ {path} 파일 없음")
        return False

def check_range(df, colname, low=-1, high=1):
    valid = df[colname].between(low, high).mean()
    return f"{colname}: {valid*100:.1f}% 정상 범위 내 값"

def pipeline_check():
    print("🚀 WRDS 데이터 파이프라인 무결성 검증 시작\n")

    # ------------------------------
    # ① collectData.csv
    # ------------------------------
    if check_file_exists(paths["collect"]):
        df = pd.read_csv(paths["collect"])
        print(f"원시 데이터: {len(df):,}행, 컬럼: {list(df.columns)}")

    # ------------------------------
    # ② outputData.csv (수익률 생성 후)
    # ------------------------------
    if check_file_exists(paths["analyze"]):
        df = pd.read_csv(paths["analyze"])
        if "ew_return" in df.columns:
            print(f"수익률 데이터 (outputData.csv) 미리보기:")
            print(df[["country", "datadate", "ew_return", "vw_return"]].head())
            print(check_range(df, "ew_return"))
        else:
            print("ew_return 컬럼 없음 — analyzeModule 점검 필요")

    # ------------------------------
    # ③ outputDataCovid.csv (기간 정의 후)
    # ------------------------------
    if check_file_exists(paths["period"]):
        df = pd.read_csv(paths["period"])
        print(f"기간별 데이터 분포:\n{df['period'].value_counts()}\n")

    # ------------------------------
    # ④ outputDataSummary.csv (요약 통계)
    # ------------------------------
    if check_file_exists(paths["summary"]):
        df = pd.read_csv(paths["summary"])
        print(f"국가별 통계 요약 미리보기:\n{df.head(3)}\n")
        print(f"통계 단위 검증: ew_mean 평균 = {df['ew_mean'].mean():.4f}")

    # ------------------------------
    # ⑤ comparison_developed_vs_emerging.csv (그룹 비교)
    # ------------------------------
    if check_file_exists(paths["compare"]):
        df = pd.read_csv(paths["compare"])
        print("\n선진국 vs 신흥국 비교 결과:")
        print(df[["group", "period", "ew_mean", "ew_std", "ew_skew", "ew_excess_kurtosis"]])
        print("\n ew_mean 평균 범위:",
              f"{df['ew_mean'].min():.4f} ~ {df['ew_mean'].max():.4f}")

    print("\n✅ 파이프라인 점검 완료")

if __name__ == "__main__":
    pipeline_check()
# ---------------------------------------
# 📈 Problem 6. Correlation and Spillover Effects
# ---------------------------------------

import pandas as pd
import numpy as np
import os

def AnalyzeCorrelation():
    print("📊 Problem 6: Correlation and Spillover Effects 실행 중...")

    # -----------------------
    # 1️⃣ 데이터 로드
    # -----------------------
    input_path = "data/outputDataCovid.csv"
    df = pd.read_csv(input_path)
    print(f"✅ 데이터 로드 완료: {len(df):,}행")

    # -----------------------
    # 2️⃣ 국가 그룹 정의 (MSCI 기준)
    # -----------------------
    developed = ["GBR", "DEU", "JPN", "FRA", "AUS"]
    emerging  = ["CHN", "IND", "BRA", "ZAF", "TUR"]

    df["group"] = np.where(df["country"].isin(developed), "Developed",
                  np.where(df["country"].isin(emerging), "Emerging", "Other"))

    # -----------------------
    # 3️⃣ Crisis / Recovery 구분
    # -----------------------
    crisis_df = df[df["period"] == "Crisis"]
    recovery_df = df[df["period"] == "Recovery"]

    # -----------------------
    # 4️⃣ 상관행렬 계산 함수
    # -----------------------
    def compute_corr_matrix(sub_df, value_col="ew_return"):
        pivot = sub_df.pivot(index="datadate", columns="country", values=value_col)
        corr_matrix = pivot.corr(method="pearson")
        return corr_matrix

    corr_crisis = compute_corr_matrix(crisis_df, "ew_return")
    corr_recovery = compute_corr_matrix(recovery_df, "ew_return")

    # -----------------------
    # 5️⃣ 파일 저장
    # -----------------------
    os.makedirs("data", exist_ok=True)
    crisis_path = "data/correlation_crisis.csv"
    recovery_path = "data/correlation_recovery.csv"

    corr_crisis.to_csv(crisis_path)
    corr_recovery.to_csv(recovery_path)

    print(f"💾 Crisis 상관행렬 저장 완료: {crisis_path}")
    print(f"💾 Recovery 상관행렬 저장 완료: {recovery_path}")

    # -----------------------
    # 6️⃣ 그룹별 평균 상관계수 계산 (존재 국가만 반영)
    # -----------------------
    def average_corr_by_group(corr_matrix, group_name):
        group_list = developed if group_name == "Developed" else emerging
        available = [g for g in group_list if g in corr_matrix.index]

        if len(available) < 2:
            print(f"⚠️ {group_name} 그룹 내 유효 국가가 부족합니다. ({len(available)}개)")
            return np.nan

        sub_corr = corr_matrix.loc[available, available]
        mask = np.triu(np.ones(sub_corr.shape), k=1).astype(bool)
        avg_corr = sub_corr.where(mask).stack().mean()
        return avg_corr

    summary_data = {
        "group": ["Developed", "Emerging"],
        "Crisis_avg_corr": [
            average_corr_by_group(corr_crisis, "Developed"),
            average_corr_by_group(corr_crisis, "Emerging")
        ],
        "Recovery_avg_corr": [
            average_corr_by_group(corr_recovery, "Developed"),
            average_corr_by_group(corr_recovery, "Emerging")
        ]
    }

    summary_df = pd.DataFrame(summary_data)
    summary_path = "data/correlation_summary.csv"
    summary_df.to_csv(summary_path, index=False)

    print(f"💾 그룹별 평균 상관계수 요약 저장 완료: {summary_path}")
    print("\n📈 그룹별 평균 상관계수 미리보기:")
    print(summary_df)

    # -----------------------
    # 7️⃣ 간단한 해석
    # -----------------------
    print("\n🧠 해석 요약:")
    print(" - Crisis 기간: 상관계수 상승 → 시장 간 동조화 및 금융 전이(Contagion) 현상 발생 가능성")
    print(" - Recovery 기간: 상관계수 하락 → 시장 간 분화 및 정상화 진행")
    print(" - Developed 그룹은 구조적 연계성이 높고, Emerging 그룹은 변동성이 큼")

    return summary_df

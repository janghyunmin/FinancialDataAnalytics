<<<<<<< Updated upstream
=======
# ---------------------------------------
# 🌍 Developed vs Emerging Markets 비교 분석 (pivot 자동 변환 버전)
# ---------------------------------------

>>>>>>> Stashed changes
import pandas as pd
import numpy as np
import os

def CompareGroups():
    input_path = "data/outputDataSummary.csv"
    output_path = "data/comparison_developed_vs_emerging.csv"

<<<<<<< Updated upstream
    df = pd.read_csv(input_path)

    developed = ["GBR", "DEU", "JPN", "FRA", "AUS"]
    emerging = ["CHN", "IND", "BRA", "ZAF", "TUR"]

    df["group"] = np.where(df["country"].isin(developed), "Developed",
                  np.where(df["country"].isin(emerging), "Emerging", "Other"))
    df = df[df["group"].isin(["Developed", "Emerging"])]

    # ✅ 여기 핵심: 이미 국가별 요약통계이므로 단순 평균
    metrics = [col for col in df.columns if ("mean" in col or "std" in col or "skew" in col or "kurt" in col)]
=======
    # 1️⃣ 데이터 로드
    df = pd.read_csv(input_path)
    print(f"✅ 데이터 로드 완료: {len(df):,}행")

    # 데이터 구조 확인 (long-form일 경우 pivot 필요)
    if "ew_level_2" in df.columns:
        print("🔄 long-form 감지 → wide-form 변환 중...")

        # EW 데이터 pivot
        ew_pivot = df.pivot_table(
            index=["country", "period"],
            columns="ew_level_2",
            values="ew_ew_return",
            aggfunc="mean"
        ).add_prefix("ew_")

        # VW 데이터 pivot
        vw_pivot = df.pivot_table(
            index=["country", "period"],
            columns="vw_level_2",
            values="vw_vw_return",
            aggfunc="mean"
        ).add_prefix("vw_")

        # 두 데이터 병합
        df = pd.concat([ew_pivot, vw_pivot], axis=1).reset_index()
        print("✅ long → wide 변환 완료")

    # 2️⃣ 국가 그룹 분류 (MSCI 기준)
    developed = ["GBR", "DEU", "JPN", "FRA", "AUS"]
    emerging  = ["CHN", "IND", "BRA", "ZAF", "TUR"]

    df["group"] = np.where(df["country"].isin(developed), "Developed",
                  np.where(df["country"].isin(emerging), "Emerging", "Other"))

    df = df[df["group"].isin(["Developed", "Emerging"])]

    if df.empty:
        raise ValueError("❌ Developed/Emerging 국가 데이터가 없습니다. country 코드 확인 필요.")

    # 3️⃣ 그룹별 평균 요약 통계 계산
    metrics = [col for col in df.columns if col.startswith(("ew_", "vw_"))]
>>>>>>> Stashed changes
    grouped = (
        df.groupby(["group", "period"])[metrics]
          .mean()
          .reset_index()
    )

<<<<<<< Updated upstream
    os.makedirs("data", exist_ok=True)
    grouped.to_csv(output_path, index=False)
    print(f"✅ 그룹별 평균 통계 저장 완료: {output_path}")

    print(grouped[["group", "period", "ew_mean", "ew_std", "ew_skew", "ew_excess_kurtosis"]])
=======
    # 4️⃣ 파일 저장
    os.makedirs("data", exist_ok=True)
    grouped.to_csv(output_path, index=False)
    print(f"💾 그룹별 비교 결과 저장 완료: {output_path}")

    # 5️⃣ 미리보기 및 간단 비교
    print("\n📊 그룹별 평균 요약 미리보기:")
    print(grouped.head())

    crisis = grouped[grouped["period"] == "Crisis"]
    recovery = grouped[grouped["period"] == "Recovery"]

    ew_cols = [c for c in grouped.columns if c.startswith("ew_")]

    print("\n🔍 Crisis 기간 비교:")
    if not crisis.empty:
        print(crisis[["group"] + ew_cols])
    else:
        print("⚠️ Crisis 기간 데이터 없음")

    print("\n🔍 Recovery 기간 비교:")
    if not recovery.empty:
        print(recovery[["group"] + ew_cols])
    else:
        print("⚠️ Recovery 기간 데이터 없음")

    print("\n✅ Developed vs Emerging Market 비교 완료")

    return grouped

>>>>>>> Stashed changes

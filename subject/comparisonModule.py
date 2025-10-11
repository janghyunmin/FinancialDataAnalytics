import pandas as pd
import numpy as np
import os

def CompareGroups():
    input_path = "data/outputDataSummary.csv"
    output_path = "data/comparison_developed_vs_emerging.csv"

    df = pd.read_csv(input_path)

    developed = ["GBR", "DEU", "JPN", "FRA", "AUS"]
    emerging = ["CHN", "IND", "BRA", "ZAF", "TUR"]

    df["group"] = np.where(df["country"].isin(developed), "Developed",
                  np.where(df["country"].isin(emerging), "Emerging", "Other"))
    df = df[df["group"].isin(["Developed", "Emerging"])]

    # ✅ 여기 핵심: 이미 국가별 요약통계이므로 단순 평균
    metrics = [col for col in df.columns if ("mean" in col or "std" in col or "skew" in col or "kurt" in col)]
    grouped = (
        df.groupby(["group", "period"])[metrics]
          .mean()
          .reset_index()
    )

    os.makedirs("data", exist_ok=True)
    grouped.to_csv(output_path, index=False)
    print(f"✅ 그룹별 평균 통계 저장 완료: {output_path}")

    print(grouped[["group", "period", "ew_mean", "ew_std", "ew_skew", "ew_excess_kurtosis"]])

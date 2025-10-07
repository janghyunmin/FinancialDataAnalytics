# outPutData.csv 파일 검증

import pandas as pd
import numpy as np

df = pd.read_csv("data/outPutData.csv")
print("행 수:", len(df))
print("컬럼:", df.columns.tolist())
print(df.head())

print("\n기간 범위:", df["datadate"].min(), "→", df["datadate"].max())
print("\n국가 목록:", df["country"].unique())
print("\n수익률 요약:")
print(df[["ew_return", "vw_return"]].describe())
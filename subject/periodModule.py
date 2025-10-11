import pandas as pd
import os

def DefinePeriods():
    input_path = "data/outputData.csv"
    output_path = "data/outputDataCovid.csv"

    df = pd.read_csv(input_path)
    df["datadate"] = pd.to_datetime(df["datadate"])

    # 기간 분류
    df["period"] = df["datadate"].apply(lambda x:
        "Crisis" if x < pd.to_datetime("2022-01-01")
        else "Recovery"
    )

    os.makedirs("data", exist_ok=True)
    df.to_csv(output_path, index=False)

    print("💾 기간 분류 완료:", output_path)
    print("📊 기간별 데이터 분포:")
    print(df["period"].value_counts())

    return df

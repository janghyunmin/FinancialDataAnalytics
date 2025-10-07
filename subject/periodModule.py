# periodModule.py
import pandas as pd
import numpy as np
import os

# periodModule.py
import pandas as pd
import numpy as np
import os

def DefinePeriods():
    input_path = "data/outputData.csv"
    output_path = "data/outputDataCovid.csv"

    # 1. 데이터 로드
    df = pd.read_csv(input_path)
    df["datadate"] = pd.to_datetime(df["datadate"])
    print(f"✅ 데이터 로드 완료: {len(df):,}행")

    # 2. 기간 구분 기준 설정
    covid_start = pd.to_datetime("2020-03-01")
    covid_end   = pd.to_datetime("2021-12-31")
    recovery_start = pd.to_datetime("2022-01-01")
    recovery_end   = pd.to_datetime("2024-12-31")

    # 3. 조건문 기반 라벨링
    conditions = [
        (df["datadate"] >= covid_start) & (df["datadate"] <= covid_end),
        (df["datadate"] >= recovery_start) & (df["datadate"] <= recovery_end)
    ]
    labels = ["Crisis", "Recovery"]

    df["period"] = np.select(conditions, labels, default="Other")

    # 4. 저장
    os.makedirs("data", exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"💾 기간 라벨 추가 완료: {output_path}")
    print("\n 기간별 데이터 분포:")
    print(df["period"].value_counts())

    return df
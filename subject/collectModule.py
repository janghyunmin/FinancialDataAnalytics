import os
import pandas as pd

# 1️⃣ 데이터 범위 확인 함수
def CheckFilteredDateRange(conn):
    query = """
        SELECT MIN(datadate) AS min_date, MAX(datadate) AS max_date
        FROM comp.g_secm
        WHERE datadate BETWEEN '2020-03-01' AND '2024-12-31'
    """
    df = conn.raw_sql(query)
    print("🎯 필터된 데이터 날짜 범위 (2020.03~2024.12):")
    print(df)
    return df

# 2️⃣ 데이터 수집 함수
def GetCompustatData(conn):
    print("📦 Global Compustat 데이터 수집 중...")

    start_date = "2020-03-01"
    end_date = "2024-12-31"

    # (1) 월별 시세 데이터
    query_price = f"""
        SELECT gvkey, iid, datadate, fic, loc,
               prccm, ajexm, ajpm, curcdm
        FROM comp.g_secm
        WHERE datadate >= TO_DATE('{start_date}', 'YYYY-MM-DD')
          AND datadate <= TO_DATE('{end_date}', 'YYYY-MM-DD')
    """
    df_price = conn.raw_sql(query_price)
    print(f"✅ 월별 가격 데이터: {len(df_price):,}행")

    # (2) 연간 발행주식수 데이터
    query_shares = f"""
        SELECT gvkey, datadate, cshoi AS csho
        FROM comp.g_funda
        WHERE datadate >= TO_DATE('{start_date}', 'YYYY-MM-DD')
          AND datadate <= TO_DATE('{end_date}', 'YYYY-MM-DD')
    """
    df_shares = conn.raw_sql(query_shares)
    print(f"✅ 연간 발행주식수 데이터: {len(df_shares):,}행")

    # (3) 병합 및 필터링
    df_price["datadate"] = pd.to_datetime(df_price["datadate"])
    df_shares["datadate"] = pd.to_datetime(df_shares["datadate"])

    df_price["country"] = df_price["loc"].fillna(df_price["fic"])
    df_price["country"] = df_price["country"].astype(str).str.upper().str.strip()

    target_codes = ['GB', 'DE', 'JP', 'FR', 'AU', 'CN', 'IN', 'BR', 'ZA', 'TR']
    df_price = df_price[df_price["country"].apply(lambda x: any(code in x for code in target_codes))]

    df_shares = df_shares.sort_values(["gvkey", "datadate"])
    df = pd.merge_asof(
        df_price.sort_values("datadate"),
        df_shares.sort_values("datadate"),
        on="datadate",
        by="gvkey",
        direction="backward"
    )

    df = df.dropna(subset=["prccm", "csho"])
    df = df[(df["datadate"] >= pd.to_datetime(start_date)) &
            (df["datadate"] <= pd.to_datetime(end_date))]

    os.makedirs("data", exist_ok=True)
    output_path = "data/collectData.csv"
    df.to_csv(output_path, index=False)

    print(f"💾 CSV 저장 완료: {output_path}")
    print(f"📊 최종 데이터 행 수: {len(df):,}")
    print(f"📅 데이터 기간: {df['datadate'].min().date()} ~ {df['datadate'].max().date()}")

    return df

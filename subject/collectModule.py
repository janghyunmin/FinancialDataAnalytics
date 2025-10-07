"""
문제 1. 데이터 수집
다음 10개국에 대한 Global Compustat의 월별 기업 수준 데이터 수집
2020년 3월 ~ 2024년 12월 기간:
• 선진국 시장 (5): 영국, 독일, 일본, 프랑스, 호주
• 신흥 시장 (5): 중국, 인도, 브라질, 남아프리카공화국, 튀르키예
선진 시장 대 신흥 시장 분류는 MSCI 표준을 따릅니다.
"""

# collectModule.py
import os
import pandas as pd


# 데이터 실제 존재 유무 확인 Module
def CheckDateRange(conn):
    query = """
        SELECT MIN(datadate) AS min_date, MAX(datadate) AS max_date
        FROM comp.g_secm
    """
    df = conn.raw_sql(query)
    print(" 데이터 날짜 범위:")
    print(df)


# -----------------------
# Compustat 데이터 수집 함수
# -----------------------
def GetCompustatData(conn):
    table_name = "g_secm"
    print(f" {table_name} 테이블에서 데이터 수집 중...")

    start_date = "2020-01-01"
    end_date = "2025-09-30"

    query = f"""
        SELECT gvkey, iid, datadate, fic, loc,
            prccm, cshtrm, ajexm, ajpm, curcdm
        FROM comp.g_secm
        WHERE datadate BETWEEN '2020-01-01' AND '2025-09-30'
    """

    df = conn.raw_sql(query)
    print(f" 원본 데이터: {len(df):,}행")

    print("\n 국가 코드 샘플 (loc):")
    print(df["loc"].value_counts().head(20))

    print("\n 국가 코드 샘플 (fic):")
    print(df["fic"].value_counts().head(20))

    # 국가 코드 통합
    df["country"] = df["loc"].fillna(df["fic"])
    df["country"] = df["country"].str.upper().str.strip()
    df["country"] = df["country"].fillna("").astype(str)   # 추가

    # 느슨한 필터 (부분 일치)
    target_codes = ['GB', 'DE', 'JP', 'FR', 'AU', 'CN', 'IN', 'BR', 'ZA', 'TR']
    df = df[df["country"].apply(lambda x: any(code in x for code in target_codes))]

    # 날짜 변환
    df["datadate"] = pd.to_datetime(df["datadate"])
    df = df.dropna(subset=["prccm", "cshtrm"])

    # 저장
    os.makedirs("data", exist_ok=True)
    output_path = "data/collectData.csv"
    df.to_csv(output_path, index=False)
    print(f"CSV 저장 완료: {output_path}")
    print(f"최종 데이터 행 수: {len(df):,}")

    return df

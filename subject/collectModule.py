"""
문제 1. 데이터 수집
다음 10개국에 대한 Global Compustat의 월별 기업 수준 데이터 수집
2020년 3월 ~ 2024년 12월 기간:
• 선진국 시장 (5): 영국, 독일, 일본, 프랑스, 호주
• 신흥 시장 (5): 중국, 인도, 브라질, 남아프리카공화국, 튀르키예
선진 시장 대 신흥 시장 분류는 MSCI 표준을 따릅니다.
"""

import os
import pandas as pd

# -----------------------
# 데이터 날짜 범위 확인 함수
# -----------------------
def CheckFilteredDateRange(conn):
    query = """
        SELECT MIN(datadate) AS min_date, MAX(datadate) AS max_date
        FROM comp.g_secm
        WHERE datadate BETWEEN '2020-03-01' AND '2024-12-31'
    """
    df = conn.raw_sql(query)
    print("🎯 필터된 데이터 날짜 범위 (2020.03~2024.12):")
    print(df)


# -----------------------
# Compustat 데이터 수집 함수
# -----------------------
def GetCompustatData(conn):
    table_name = "g_secm"
    print(f"📦 {table_name} 테이블에서 데이터 수집 중...")

    # ✅ 날짜 범위 지정
    start_date = "2020-03-01"
    end_date = "2024-12-31"

    # ✅ SQL 쿼리 (명시적 날짜 비교)
    query = f"""
        SELECT gvkey, iid, datadate, fic, loc,
               prccm, cshtrm, ajexm, ajpm, curcdm
        FROM comp.{table_name}
        WHERE datadate >= TO_DATE('{start_date}', 'YYYY-MM-DD')
          AND datadate <= TO_DATE('{end_date}', 'YYYY-MM-DD')
    """

    # ✅ 데이터 로드
    df = conn.raw_sql(query)
    print(f"✅ 원본 데이터: {len(df):,}행")

    # -----------------------
    # 국가 코드 정리
    # -----------------------
    print("\n 국가 코드 샘플 (loc):")
    print(df["loc"].value_counts().head(15))
    print("\n 국가 코드 샘플 (fic):")
    print(df["fic"].value_counts().head(15))

    # loc > fic 순서로 국가코드 채우기
    df["country"] = df["loc"].fillna(df["fic"])
    df["country"] = df["country"].astype(str).str.upper().str.strip()

    # 대상 10개국
    target_codes = ['GB', 'DE', 'JP', 'FR', 'AU', 'CN', 'IN', 'BR', 'ZA', 'TR']
    df = df[df["country"].apply(lambda x: any(code in x for code in target_codes))]

    # 날짜 변환 (형식 보정)
    df["datadate"] = pd.to_datetime(df["datadate"])

    # ✅ Python에서도 추가 필터 (이중 보정)
    df = df[(df["datadate"] >= pd.to_datetime(start_date)) &
            (df["datadate"] <= pd.to_datetime(end_date))]

    # 결측 제거
    df = df.dropna(subset=["prccm", "cshtrm"])

    # 저장
    os.makedirs("data", exist_ok=True)
    output_path = "data/collectData.csv"
    df.to_csv(output_path, index=False)

    print(f"CSV 저장 완료: {output_path}")
    print(f"최종 데이터 행 수: {len(df):,}")
    print(f"데이터 기간: {df['datadate'].min().date()} ~ {df['datadate'].max().date()}")

    return df

import wrds
from dotenv import load_dotenv
import os
import pandas as pd

# -----------------------
# 1) WRDS 연결
# -----------------------
def WRDSConnection():
    print("🔗 WRDS Connection Module Running...")

    load_dotenv()
    wrds_user = os.getenv("WRDS_USER", None)
    wrds_pass = os.getenv("WRDS_PASS", None)

    if wrds_user and wrds_pass:
        conn = wrds.Connection(wrds_username=wrds_user, wrds_password=wrds_pass)
    else:
        conn = wrds.Connection()

    print("✅ WRDS 연결 완료")
    return conn


# -----------------------
# 2) 테이블 목록 확인
# -----------------------
def FindTables(conn):
    print("Compustat(Global) 테이블 검색 중...")

    tables = conn.list_tables(library="comp")
    print(f"comp 라이브러리 테이블 수: {len(tables)}")

    query = "SELECT * FROM comp.g_secm LIMIT 10"
    df = conn.raw_sql(query)
    print(" g_secm 샘플 10행:")
    print(df.head())
    print("\n 컬럼 목록:")
    print(df.columns.tolist())

    cand = [t for t in tables if ("g_" in t or "sec" in t)]
    print("\n🔍 g_ 또는 sec가 포함된 테이블 목록:")
    for t in cand:
        print("  -", t)

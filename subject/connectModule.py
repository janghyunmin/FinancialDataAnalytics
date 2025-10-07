# connectModule.py
import wrds
from dotenv import load_dotenv
import os

# -----------------------
# WRDS 연결 함수
# -----------------------
def WRDSConnection():
    """WRDS 계정으로 연결 후 connection 객체 반환"""
    print("WRDS Module Running...")

    load_dotenv()
    wrds_user = os.getenv("WRDS_USER", None)
    wrds_pass = os.getenv("WRDS_PASS", None)

    if wrds_user and wrds_pass:
        conn = wrds.Connection(wrds_username=wrds_user, wrds_password=wrds_pass)
    else:
        conn = wrds.Connection()

    print("✅ WRDS 연결 완료.")
    return conn


# -----------------------
# Compustat 테이블 탐색 함수
# -----------------------
def FindTables(conn):
    """comp 라이브러리 내 g_ 또는 sec 테이블 목록 확인"""
    print("Compustat(Global) 테이블 검색 중...")

    tables = conn.list_tables(library="comp")
    print(f"comp 라이브러리 테이블 수: {len(tables)}")

    cand = [t for t in tables if ("g_" in t or "sec" in t)]
    print("🔍 g_ 또는 sec가 포함된 테이블 목록:")
    for t in cand:
        print("  -", t)

    return cand

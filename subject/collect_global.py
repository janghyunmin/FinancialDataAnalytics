# collect_compustat_global.py
import os
import re
import pandas as pd
import numpy as np
from datetime import datetime
from dotenv import load_dotenv

import wrds  # WRDS Python API

# -----------------------
# 0) 설정
# -----------------------
START = "2020-03-01"
END   = "2024-12-31"

# 과제 지정 10개국 (MSCI 분류 기준의 대표 국가들)
# Compustat Global의 국가 필드(loc 또는 fic)에는 ISO 2자리 코드가 많이 쓰입니다.
# ISO2 코드 매핑(검증된 표준 코드)
    # Developed 5
    "United Kingdom": "GB",
    "Germany":        "DE",
    "Japan":          "JP",
    "France":         "FR",
    "Australia":      "AU",
    # Emerging 5
    "China":          "CN",
    "India":          "IN",
    "Brazil":         "BR",
    "South Africa":   "ZA",
    "Turkey":         "TR",
}

# 저장 경로
OUT_DIR = "data"
os.makedirs(OUT_DIR, exist_ok=True)

# -----------------------
# 1) WRDS 연결
# -----------------------
load_dotenv()
wrds_user = os.getenv("WRDS_USER", None)
wrds_pass = os.getenv("WRDS_PASS", None)

# print(wrds_user)
# print(wrds_pass)

if wrds_user and wrds_pass:
    # 환경변수로 로그인(선택)
    conn = wrds.Connection(wrds_username=wrds_user, wrds_password=wrds_pass)
else:
    # 최초 실행 시 프롬프트로 묻습니다.
    conn = wrds.Connection()

print("✅ Connected to WRDS.")

# -----------------------
# 2) Compustat(Global) 라이브러리 탐색
# -----------------------
lib = "comp"  # WRDS에서 Compustat 라이브러리 키는 일반적으로 'comp'
tables = conn.list_tables(library=lib)
print(f"📦 {lib} 내 테이블 수: {len(tables)}")

def pick_first_existing(candidates):
    """후보 테이블명 리스트 중 실제 존재하는 첫 번째를 반환"""
    for cand in candidates:
        if cand in tables:
            return cand
    return None

# 월별 시큐리티(가격/수익률) 후보들 (학교/버전에 따라 이름 상이)
monthly_candidates = [
    "g_secm", "g_sec_m", "secm", "sec_m",
    "g_security_monthly", "security_monthly"
]
# 시큐리티 마스터(종목 식별자 iid/gvkey 등)
security_candidates = [
    "g_security", "security", "g_sec_id", "sec_id", "sec_idhist"
]
# 회사(국가코드 loc/fic 보유)
company_candidates = [
    "g_company", "company"
]

tbl_monthly  = pick_first_existing(monthly_candidates)
tbl_secid    = pick_first_existing(security_candidates)
tbl_company  = pick_first_existing(company_candidates)

print("🔎 자동 선택된 테이블(없으면 None):")
print("  - Monthly:", tbl_monthly)
print("  - Security:", tbl_secid)
print("  - Company :", tbl_company)

if tbl_monthly is None:
    # 월별 시계열 테이블 이름이 불명확할 경우, 힌트를 출력하고 종료
    # (사용자 학교의 Compustat Global 스키마에서 list_tables를 확인해 이름을 알려줍니다)
    raise RuntimeError(
        "월별 시큐리티 테이블을 찾지 못했습니다. "
        "conn.list_tables('comp') 결과에서 'g_'와 'sec' 그리고 'm'(monthly) 키워드를 포함한 테이블명을 확인해 주세요."
    )

# -----------------------
# 3) 각 테이블의 핵심 컬럼 추정
# -----------------------
# 컬럼 목록 조회
def cols_of(table):
    q = f"""
    select column_name
    from information_schema.columns
    where table_schema = '{lib}'
      and table_name = '{table}'
    order by ordinal_position
    """
    return [r[0] for r in conn.raw_sql(q).values]

cols_monthly = cols_of(tbl_monthly)
cols_secid   = cols_of(tbl_secid)   if tbl_secid   else []
cols_company = cols_of(tbl_company) if tbl_company else []

print("📑 컬럼 스캔 완료.")

# 월별 테이블에서 날짜/식별자/가격/수익률 후보
date_col   = "datadate" if "datadate" in cols_monthly else ("date" if "date" in cols_monthly else None)
gvkey_col  = "gvkey"    if "gvkey"    in cols_monthly else None
iid_col    = "iid"      if "iid"      in cols_monthly else None

# 가격/수익률 열 후보
price_cols = [c for c in ["prc", "price", "close"] if c in cols_monthly]
ret_cols   = [c for c in ["ret", "return", "retm"] if c in cols_monthly]
shrout_col = "cshoc" if "cshoc" in cols_monthly else ("csho" if "csho" in cols_monthly else None)

if not date_col or not gvkey_col or not iid_col:
    print("⚠️ 경고: 월별 테이블의 핵심 식별 컬럼(gvkey/iid/datadate)이 표준과 다릅니다. 실제 컬럼명을 확인해 주세요.")
    print(" - monthly columns head:", cols_monthly[:30])

# 시큐리티 마스터에서 gvkey/iid 확인
if tbl_secid:
    gvkey_in_secid = "gvkey" in cols_secid
    iid_in_secid   = "iid"   in cols_secid
else:
    gvkey_in_secid = iid_in_secid = False

# 회사 테이블에서 국가 코드 후보 (Compustat Global: loc가 상장국/본국코드로 널리 사용)
country_cols = [c for c in ["loc", "fic", "dloc", "country", "incorp"] if tbl_company and c in cols_company]
if not country_cols:
    print("⚠️ 회사 테이블에서 국가코드 컬럼을 찾지 못했습니다. (loc/fic/country 등)")

# -----------------------
# 4) 국가코드 테이블 구성 (gvkey → 국가)
# -----------------------
country_df = None
if tbl_company and country_cols:
    cc = country_cols[0]  # 우선순위 1개 사용
    q_country = f"""
        select gvkey, {cc} as country_code
        from {lib}.{tbl_company}
    """
    country_df = conn.raw_sql(q_country)
    # ISO2 대문자 정규화
    country_df["country_code"] = country_df["country_code"].astype(str).str.upper().str.strip()
    # 우리가 원하는 10개국만 남기기
    target_iso2 = set(COUNTRIES_ISO2.values())
    country_df = country_df[country_df["country_code"].isin(target_iso2)].drop_duplicates()
    print(f"🌍 회사-국가 매핑 레코드: {len(country_df):,}")
else:
    print("⚠️ 회사-국가 매핑을 생략합니다(테이블/컬럼 미존재). 나중에 보강 필요.")

# -----------------------
# 5) 월별 시계열 데이터 로딩 (기간 필터)
# -----------------------
date_filter_sql = ""
if date_col:
    date_filter_sql = f"where {date_col} between '{START}' and '{END}'"

select_cols = [c for c in [date_col, gvkey_col, iid_col] if c]
value_cols  = [c for c in (ret_cols + price_cols + ([shrout_col] if shrout_col else [])) if c]
col_str     = ", ".join(dict.fromkeys(select_cols + value_cols))  # 중복 제거 유지 순서

q_monthly = f"""
    select {col_str}
    from {lib}.{tbl_monthly}
    {date_filter_sql}
"""
monthly = conn.raw_sql(q_monthly)
print(f"🗓 월별 원본 로우수: {len(monthly):,}")

# 기본 정리/정규화
monthly = monthly.rename(columns={date_col: "date", gvkey_col: "gvkey", iid_col: "iid"})
monthly["date"] = pd.to_datetime(monthly["date"])
if shrout_col and shrout_col in monthly.columns:
    monthly = monthly.rename(columns={shrout_col: "shrout"})
if "prc" in monthly.columns:
    monthly["prc"] = pd.to_numeric(monthly["prc"], errors="coerce")
if "ret" in monthly.columns:
    monthly["ret"] = pd.to_numeric(monthly["ret"], errors="coerce")

# -----------------------
# 6) 국가 조인 및 10개국 필터
# -----------------------
if country_df is not None:
    monthly = monthly.merge(country_df, on="gvkey", how="inner")
    print(f"✅ 10개국 필터 후 로우수: {len(monthly):,}")
else:
    print("⚠️ 국가 필터를 건너뜁니다(회사-국가 매핑 부재). 추후 수동 필터 필요.")

# -----------------------
# 7) 저장
# -----------------------
# 메모리/속도 고려해 Parquet 권장 + CSV 같이 저장
out_parquet = os.path.join(OUT_DIR, "compustat_global_monthly_2020_03_to_2024_12.parquet")
out_csv     = os.path.join(OUT_DIR, "compustat_global_monthly_2020_03_to_2024_12.csv")

# 유용한 서브셋 컬럼만 우선 저장(날짜/식별자/국가/가격/수익률/주식수)
keep_cols = [c for c in ["date","gvkey","iid","country_code","prc","ret","shrout"] if c in monthly.columns]
monthly[keep_cols].to_parquet(out_parquet, index=False)
monthly[keep_cols].to_csv(out_csv, index=False)

print("💾 저장 완료:")
print(" -", out_parquet)
print(" -", out_csv)

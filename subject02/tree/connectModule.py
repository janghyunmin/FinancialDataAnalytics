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
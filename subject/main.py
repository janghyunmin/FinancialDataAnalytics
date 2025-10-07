# main.py
import connectModule
import collectModule
import analyzeModule

# -----------------------
# 실행부
# -----------------------
if __name__ == "__main__":
    # 1. WRDS 연결
    conn = connectModule.WRDSConnection()

    # 2. 테이블 목록 확인 (선택)
    connectModule.FindTables(conn=conn)
    
    # 2-1. 데이터 실제 존재 유무 확인 Module
    collectModule.CheckDateRange(conn = conn)
    
    # 3. 국가별 데이터 수집 Module
    df = collectModule.GetCompustatData(conn=conn)

    # print("\n데이터 미리보기:")
    # print(df.head())

    # 4. 반환 생성 프로세스 Module
    analyzeModule.GenerateReturns()

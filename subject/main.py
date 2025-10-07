# main.py
import connectModule # WRDS 연결 및 테이블 탐색 모듈
import collectModule # Compustat 데이터 수집 모듈
import analyzeModule # 수익률 계산 및 국가별 수익률 집계 모듈
import periodModule # Covid-19 기간 정의 Module
import summaryModule  # 국가·기간별 기술통계 Module

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

    # 5. COVID-19 기간 정의
    # COVID-19 위기 기간 : 2020년 3월 ~ 2021년 12월
    # 위기 후 회복 기간 : 2022년 1월 ~ 2024년 12월
    periodModule.DefinePeriods()
 
    # 6. 국가 및 기간별 요약 통계 계산
    summaryModule.SummaryStatistics()

    print("\n✅ 전체 파이프라인 완료 (수집 → 수익률 → 기간 → 요약통계)")
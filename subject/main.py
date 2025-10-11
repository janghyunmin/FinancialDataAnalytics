import connectModule   # WRDS 연결
import collectModule   # 데이터 수집
import analyzeModule   # 수익률 계산
import periodModule    # 기간 정의
import summaryModule   # 통계 요약
import comparisonModule  # Developed vs Emerging 비교
import correlationModule  # Problem 6 모듈
import presentationModule # 마지막 결과 확인용 모듈

if __name__ == "__main__":
    # 1. WRDS 연결
    conn = connectModule.WRDSConnection()

    # 2. 테이블 목록 확인
    connectModule.FindTables(conn)

    # 3. 데이터 수집
    collectModule.CheckFilteredDateRange(conn)
    collectModule.GetCompustatData(conn)

    # 4. 수익률 생성
    analyzeModule.GenerateReturns()

    # 5. COVID-19 기간 정의
    periodModule.DefinePeriods()

    # 6. 국가 및 기간별 요약 통계 계산
    summaryModule.SummaryStatistics()

    # 7. Developed vs Emerging 시장 비교
    comparisonModule.CompareGroups()

    # 8. 상관관계 및 금융 전이 효과 분석
    correlationModule.AnalyzeCorrelation()

    # 결과 확인
    presentationModule.PlotRepresentativeHistograms()

    print("\n전체 파이프라인 완료 (데이터 수집 → 수익률 생성 → 기간 정의 → 요약 → 비교분석)")

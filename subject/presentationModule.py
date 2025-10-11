# ---------------------------------------
# Problem 7(b): 대표 선진국·신흥국 월별 수익률 히스토그램 (한글 폰트 자동탐지)
# ---------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib import font_manager, rc

# ---------------------------------------
# 한글 폰트 자동 설정 함수
# ---------------------------------------
def set_korean_font():
    possible_fonts = [
        "/System/Library/Fonts/Supplemental/AppleGothic.ttf",  # macOS 최신
        "/Library/Fonts/AppleGothic.ttf",                      # macOS 구버전
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",          # macOS 13+
        "C:/Windows/Fonts/malgun.ttf",                         # Windows
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",     # Ubuntu
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"  # Google Colab
    ]

    for path in possible_fonts:
        if os.path.exists(path):
            font_name = font_manager.FontProperties(fname=path).get_name()
            rc("font", family=font_name)
            plt.rcParams["axes.unicode_minus"] = False
            print(f"✅ 한글 폰트 설정 완료: {font_name}")
            return

    print("한글 폰트를 찾을 수 없음.")

# 실행 시 자동 적용
set_korean_font()


# ---------------------------------------
# 대표 선진국·신흥국 수익률 히스토그램
# ---------------------------------------
def PlotRepresentativeHistograms():
    print("대표 국가 월별 수익률 히스토그램 생성 중...")

    # 1. 데이터 로드
    covid_path = "data/outputDataCovid.csv"

    if not os.path.exists(covid_path):
        raise FileNotFoundError("❌ data/outputDataCovid.csv 파일을 찾을 수 없습니다.")

    df = pd.read_csv(covid_path)
    print(f"✅ 데이터 로드 완료: {len(df):,}행")

    # 2. 국가 코드 및 기간 라벨 보정
    df["country"] = df["country"].astype(str).str.upper().str.strip()
    df["datadate"] = pd.to_datetime(df["datadate"], errors="coerce")

    df["period"] = "Other"
    df.loc[
        (df["datadate"] >= "2020-03-01") & (df["datadate"] <= "2021-12-31"),
        "period"
    ] = "Crisis"
    df.loc[
        (df["datadate"] >= "2022-01-01") & (df["datadate"] <= "2024-12-31"),
        "period"
    ] = "Recovery"

    print("기간 라벨링 완료 (Crisis / Recovery / Other)")

    # 3. 대표 국가 설정
    reps = {
        "Developed": "JPN",  # 일본
        "Emerging": "IND"    # 인도
    }

    os.makedirs("figures", exist_ok=True)

    # 4. 국가별 히스토그램 생성
    for group, country in reps.items():
        subset = df[df["country"].str.contains(country, na=False)]

        if subset.empty:
            print(f" {country} 데이터 없음 - 건너뜀")
            continue

        plt.figure(figsize=(8, 5))
        sns.histplot(
            data=subset,
            x="ew_return",
            hue="period",
            bins=25,
            kde=True,
            palette={"Crisis": "salmon", "Recovery": "skyblue"},
            alpha=0.7
        )

        plt.xlim(-0.2, 0.2)  # 수익률 범위 제한
        plt.title(f"{group} ({country}) 월별 수익률 분포", fontsize=13)
        plt.xlabel("월별 수익률 (EW 기준)")
        plt.ylabel("빈도수")
        plt.legend(title="기간", labels=["Crisis", "Recovery"])
        plt.grid(alpha=0.3)

        # ✅ 저장 후 표시
        save_path = f"figures/hist_{country}_period_fixed.png"
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.show()
        plt.close()

        print(f"✅ 히스토그램 저장 완료: {save_path}")

    print("\n 대표 국가 히스토그램 생성 완료 (Crisis vs Recovery 비교 시각화)")


# ---------------------------------------
# 실행부
# ---------------------------------------
if __name__ == "__main__":
    PlotRepresentativeHistograms()

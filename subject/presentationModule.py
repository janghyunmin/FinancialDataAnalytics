# ---------------------------------------
# 📊 Problem 7 – Presentation of Results (기술통계 + 시각화 + 해석)
# ---------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib import font_manager, rc
import platform

# ---------------------------------------
# ✅ 한글 폰트 자동 설정 (안전 버전)
# ---------------------------------------
def set_korean_font():
    system_name = platform.system()
    font_paths = []

    if system_name == "Darwin":  # macOS
        font_paths = [
            "/System/Library/Fonts/AppleSDGothicNeo.ttc",   # 최신 macOS
            "/System/Library/Fonts/Supplemental/AppleGothic.ttf",  # 구버전 macOS
            "/Library/Fonts/AppleGothic.ttf",               # 추가 설치형
            "/System/Library/Fonts/PingFang.ttc"            # 일부 macOS 14+
        ]
    elif system_name == "Windows":
        font_paths = ["C:/Windows/Fonts/malgun.ttf"]
    elif system_name == "Linux":
        font_paths = [
            "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"
        ]

    for path in font_paths:
        if os.path.exists(path):
            font_name = font_manager.FontProperties(fname=path).get_name()
            rc("font", family=font_name)
            plt.rcParams["axes.unicode_minus"] = False
            print(f"✅ 한글 폰트 설정 완료: {font_name}")
            return

    print("⚠️ 한글 폰트를 찾지 못했습니다. 기본 폰트로 진행합니다.")
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False


# 실행 시 자동 적용
set_korean_font()


# ---------------------------------------
# 7(a) 기술통계 요약표 저장
# ---------------------------------------
def SaveDescriptiveSummary():
    input_path = "data/comparison_developed_vs_emerging.csv"
    output_path = "figures/descriptive_summary_table.csv"

    if not os.path.exists(input_path):
        raise FileNotFoundError("❌ comparison_developed_vs_emerging.csv 파일이 없습니다.")

    df = pd.read_csv(input_path)
    cols = ["group", "period", "ew_mean", "ew_std", "ew_skew", "ew_excess_kurtosis"]

    if not all(c in df.columns for c in cols):
        raise ValueError("❌ 예상 컬럼이 누락되었습니다. summaryModule 실행 필요.")

    summary = df[cols].round(4)
    os.makedirs("figures", exist_ok=True)
    summary.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"💾 기술통계 요약표 저장 완료: {output_path}")
    print(summary.head())
    return summary


# ---------------------------------------
# 7(b) 대표 선진국·신흥국 수익률 히스토그램
# ---------------------------------------
def PlotRepresentativeHistograms():
    print("\n📈 대표 국가 월별 수익률 히스토그램 생성 중...")

    covid_path = "data/outputDataCovid.csv"
    if not os.path.exists(covid_path):
        raise FileNotFoundError("❌ data/outputDataCovid.csv 파일을 찾을 수 없습니다.")

    df = pd.read_csv(covid_path)
    df["country"] = df["country"].astype(str).str.upper().str.strip()
    df["datadate"] = pd.to_datetime(df["datadate"], errors="coerce")

    # 기간 라벨링
    df["period"] = "Other"
    df.loc[(df["datadate"] >= "2020-03-01") & (df["datadate"] <= "2021-12-31"), "period"] = "Crisis"
    df.loc[(df["datadate"] >= "2022-01-01") & (df["datadate"] <= "2024-12-31"), "period"] = "Recovery"

    reps = {"Developed": "JPN", "Emerging": "IND"}
    os.makedirs("figures", exist_ok=True)

    for group, country in reps.items():
        subset = df[df["country"].str.contains(country, na=False)]
        if subset.empty:
            print(f"⚠️ {country} 데이터 없음 - 건너뜀")
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
        plt.xlim(-0.2, 0.2)
        plt.title(f"{group} ({country}) 월별 수익률 분포", fontsize=13)
        plt.xlabel("월별 수익률 (EW 기준)")
        plt.ylabel("빈도수")
        plt.legend(title="기간", labels=["Crisis", "Recovery"])
        plt.grid(alpha=0.3)

        save_path = f"figures/hist_{country}_period_fixed.png"
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()

        print(f"✅ 히스토그램 저장 완료: {save_path}")

    print("\n🎯 대표 국가 히스토그램 생성 완료 (Crisis vs Recovery 비교 시각화)")


# ---------------------------------------
# 7(c) 결과 해석 텍스트 요약
# ---------------------------------------
def SaveDiscussionSummary():
    output_path = "figures/discussion_summary.txt"
    discussion = """🧠 [결과 해석 – Developed vs Emerging Markets]

1️⃣ 위기(Crisis) 기간에는 양 그룹 모두 수익률 분포가 좌측(음의 구간)으로 치우쳐 있으며,
   변동성이 크고 꼬리가 두꺼운(fat-tailed) 형태를 보인다.

2️⃣ 회복(Recovery) 기간에는 분포의 중심이 우측으로 이동하며,
   수익률이 안정화되고 첨도(Kurtosis)가 감소하는 모습을 보인다.

3️⃣ 선진국(일본 JPN)은 분포가 상대적으로 좁고 안정적이며,
   신흥국(인도 IND)은 분포가 넓고 극단값이 자주 발생해 변동성이 높다.

📊 요약:
- Crisis: 신흥국의 음(-)의 수익률과 변동성 ↑
- Recovery: 양(+) 방향 반등 폭 신흥국 > 선진국
"""
    os.makedirs("figures", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(discussion)

    print(f"💾 결과 해석 요약 저장 완료: {output_path}")
    return output_path


# ---------------------------------------
# 실행부
# ---------------------------------------
if __name__ == "__main__":
    print("📘 Problem 7 – Presentation of Results 실행 중...")
    SaveDescriptiveSummary()
    PlotRepresentativeHistograms()
    SaveDiscussionSummary()
    print("\n✅ Problem 7 완료: 기술통계 + 시각화 + 해석 텍스트 생성 완료")

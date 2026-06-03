import matplotlib.pyplot as plt


def setup_chinese_font():
    """
    設定中文字型，避免圖表中文變成方框。
    Windows 通常可用 Microsoft JhengHei。
    """
    plt.rcParams["font.sans-serif"] = [
        "Microsoft JhengHei",
        "SimHei",
        "Arial Unicode MS",
        "DejaVu Sans"
    ]
    plt.rcParams["axes.unicode_minus"] = False


def plot_population_bar(population_df, output_path):
    """
    各縣市人口總數長條圖
    """
    setup_chinese_font()

    df = population_df.sort_values("total", ascending=True)

    plt.figure(figsize=(10, 8))
    plt.barh(df["city"], df["total"])
    plt.title("114年各縣市人口總數")
    plt.xlabel("人口數")
    plt.ylabel("縣市")
    plt.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_aging_index_top10(aging_df, output_path):
    """
    老化指數 Top10 長條圖
    """
    setup_chinese_font()

    df = aging_df.sort_values("aging_index", ascending=False).head(10)
    df = df.sort_values("aging_index", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(df["city"], df["aging_index"])
    plt.title("114年老化指數 Top 10")
    plt.xlabel("老化指數")
    plt.ylabel("縣市")
    plt.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_gender_pie(gender_df, output_path):
    """
    全台男女比例圓餅圖。
    將所有縣市男性、女性人口加總。
    """
    setup_chinese_font()

    total_male = gender_df["male"].sum()
    total_female = gender_df["female"].sum()

    labels = ["男性", "女性"]
    values = [total_male, total_female]

    plt.figure(figsize=(7, 7))
    plt.pie(values, labels=labels, autopct="%1.2f%%", startangle=90)
    plt.title("114年全台男女比例")
    plt.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_population_trend(trend_df, output_path):
    """
    110~114 年人口變化趨勢折線圖。

    這裡使用「相對 110 年的人口變化率」。
    優點：
    1. 不會被人口總量壓扁
    2. 比較容易看出人口增加或減少
    3. 適合呈現趨勢變化
    """
    setup_chinese_font()

    latest_year = trend_df["year"].max()
    start_year = trend_df["year"].min()

    # 選 114 年人口最多的前 8 個縣市
    top_cities = (
        trend_df[trend_df["year"] == latest_year]
        .sort_values("total", ascending=False)
        .head(8)["city"]
        .tolist()
    )

    plot_df = trend_df[trend_df["city"].isin(top_cities)].copy()

    # 計算每個縣市 110 年人口，作為基準值
    base_df = (
        plot_df[plot_df["year"] == start_year][["city", "total"]]
        .rename(columns={"total": "base_population"})
    )

    plot_df = plot_df.merge(base_df, on="city", how="left")

    plot_df["change_rate"] = (
        (plot_df["total"] - plot_df["base_population"]) /
        plot_df["base_population"] * 100
    )

    plt.figure(figsize=(10, 6))

    for city in top_cities:
        city_df = plot_df[plot_df["city"] == city].sort_values("year")
        plt.plot(
            city_df["year"],
            city_df["change_rate"],
            marker="o",
            label=city
        )

    plt.axhline(0, linestyle="--", linewidth=1)
    plt.title("110~114年主要縣市人口變化率趨勢")
    plt.xlabel("年度")
    plt.ylabel("相對110年人口變化率 (%)")
    plt.xticks(sorted(trend_df["year"].unique()))
    plt.legend()
    plt.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close()
import matplotlib.pyplot as plt
import pandas as pd
import os


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
    注意：不是各縣市，而是把所有縣市男性、女性加總。
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
    這裡畫人口最多的前 8 個縣市，避免線太多導致圖很亂。
    """
    setup_chinese_font()

    latest_year = trend_df["year"].max()

    top_cities = (
        trend_df[trend_df["year"] == latest_year]
        .sort_values("total", ascending=False)
        .head(8)["city"]
        .tolist()
    )

    plot_df = trend_df[trend_df["city"].isin(top_cities)]

    plt.figure(figsize=(10, 6))

    for city in top_cities:
        city_df = plot_df[plot_df["city"] == city].sort_values("year")
        plt.plot(city_df["year"], city_df["total"], marker="o", label=city)

    plt.title("110~114年主要縣市人口變化趨勢")
    plt.xlabel("年度")
    plt.ylabel("人口數")
    plt.xticks(sorted(trend_df["year"].unique()))
    plt.legend()
    plt.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close()
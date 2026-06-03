from modules.data_loader import load_all_data
from modules.data_cleaner import clean_population_data
from modules.analyzer import (
    calculate_city_population,
    calculate_aging_index,
    calculate_gender_ratio,
    calculate_population_trend,
    calculate_population_change,
)
from modules.visualizer import (
    plot_population_bar,
    plot_aging_index_top10,
    plot_gender_pie,
    plot_population_trend,
)

import os


def main():
    data_dir = "data"
    results_dir = "results"

    os.makedirs(results_dir, exist_ok=True)

    print("讀取資料中...")
    raw_df = load_all_data(data_dir)

    print("清理資料中...")
    df = clean_population_data(raw_df)

    print("計算 114 年各縣市人口總數...")
    population_114 = calculate_city_population(df, year=114)

    print("計算 114 年老化指數...")
    aging_index_114 = calculate_aging_index(df, year=114)

    print("計算 114 年男女比例...")
    gender_ratio_114 = calculate_gender_ratio(df, year=114)

    print("計算 110~114 年人口趨勢...")
    trend_df = calculate_population_trend(df)

    print("計算人口成長變化...")
    change_df = calculate_population_change(trend_df, start_year=110, end_year=114)

    print("輸出分析結果 CSV...")
    population_114.to_csv(os.path.join(results_dir, "114_city_population.csv"), index=False, encoding="utf-8-sig")
    aging_index_114.to_csv(os.path.join(results_dir, "114_aging_index.csv"), index=False, encoding="utf-8-sig")
    gender_ratio_114.to_csv(os.path.join(results_dir, "114_gender_ratio.csv"), index=False, encoding="utf-8-sig")
    trend_df.to_csv(os.path.join(results_dir, "population_trend.csv"), index=False, encoding="utf-8-sig")
    change_df.to_csv(os.path.join(results_dir, "population_change.csv"), index=False, encoding="utf-8-sig")

    print("繪製圖表中...")
    plot_population_bar(population_114, os.path.join(results_dir, "population_bar.png"))
    plot_aging_index_top10(aging_index_114, os.path.join(results_dir, "aging_index_top10.png"))
    plot_gender_pie(gender_ratio_114, os.path.join(results_dir, "gender_pie.png"))
    plot_population_trend(trend_df, os.path.join(results_dir, "population_trend.png"))

    print("分析完成！")
    print("圖表與 CSV 已輸出到 results 資料夾。")

    print("\n人口減少最多 Top 10：")
    print(change_df.sort_values("change_amount").head(10).to_string(index=False))

    print("\n老化指數最高 Top 10：")
    print(aging_index_114.sort_values("aging_index", ascending=False).head(10).to_string(index=False))


if __name__ == "__main__":
    main()
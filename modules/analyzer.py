import pandas as pd
import numpy as np


def calculate_city_population(df, year):
    """
    計算指定年度各縣市總人口。
    使用 sex == '計' 避免男女重複加總。
    """
    result = df[(df["year"] == year) & (df["sex"] == "計")].copy()

    result = result[["year", "city", "total"]]
    result = result.sort_values("total", ascending=False)

    return result


def calculate_aging_index(df, year):
    """
    老化指數 = 65歲以上人口 / 0~14歲人口 * 100
    """
    result = df[(df["year"] == year) & (df["sex"] == "計")].copy()

    result["aging_index"] = np.where(
        result["young_population"] > 0,
        result["old_population"] / result["young_population"] * 100,
        0
    )

    result = result[[
        "year",
        "city",
        "young_population",
        "old_population",
        "aging_index"
    ]]

    result["aging_index"] = result["aging_index"].round(2)

    return result.sort_values("aging_index", ascending=False)


def calculate_gender_ratio(df, year):
    """
    男女比例 = 男性人口 / 女性人口 * 100
    """
    target = df[df["year"] == year].copy()

    male_df = target[target["sex"] == "男"][["city", "total"]].rename(columns={"total": "male"})
    female_df = target[target["sex"] == "女"][["city", "total"]].rename(columns={"total": "female"})

    result = pd.merge(male_df, female_df, on="city", how="inner")

    result["gender_ratio"] = np.where(
        result["female"] > 0,
        result["male"] / result["female"] * 100,
        0
    )

    result["year"] = year
    result["gender_ratio"] = result["gender_ratio"].round(2)

    return result[["year", "city", "male", "female", "gender_ratio"]]


def calculate_population_trend(df):
    """
    計算每個縣市每一年的總人口，用於折線圖。
    """
    result = df[df["sex"] == "計"].copy()

    result = result[["year", "city", "total"]]
    result = result.sort_values(["city", "year"])

    return result


def calculate_population_change(trend_df, start_year=110, end_year=114):
    """
    計算人口成長量與成長率。
    """
    start_df = trend_df[trend_df["year"] == start_year][["city", "total"]]
    end_df = trend_df[trend_df["year"] == end_year][["city", "total"]]

    start_df = start_df.rename(columns={"total": f"population_{start_year}"})
    end_df = end_df.rename(columns={"total": f"population_{end_year}"})

    result = pd.merge(start_df, end_df, on="city", how="inner")

    result["change_amount"] = result[f"population_{end_year}"] - result[f"population_{start_year}"]

    result["change_rate"] = np.where(
        result[f"population_{start_year}"] > 0,
        result["change_amount"] / result[f"population_{start_year}"] * 100,
        0
    )

    result["change_rate"] = result["change_rate"].round(2)

    return result.sort_values("change_amount")
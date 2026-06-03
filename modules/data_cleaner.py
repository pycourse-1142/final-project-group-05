import pandas as pd
import numpy as np


VALID_CITIES = [
    "新北市", "臺北市", "桃園市", "臺中市", "臺南市", "高雄市",
    "宜蘭縣", "新竹縣", "苗栗縣", "彰化縣", "南投縣", "雲林縣",
    "嘉義縣", "屏東縣", "臺東縣", "花蓮縣", "澎湖縣", "基隆市",
    "新竹市", "嘉義市", "金門縣", "連江縣"
]


def clean_city_name(name):
    """
    統一縣市名稱格式。
    原始資料可能是「新 北 市」、「臺 北 市」這種中間有空白的格式。
    """
    if pd.isna(name):
        return np.nan

    name = str(name)

    name = name.replace(" ", "")
    name = name.replace("　", "")
    name = name.replace("\t", "")
    name = name.strip()

    return name


def to_number(value):
    """
    將人口數轉成數字。
    例如："1,234" -> 1234
    """
    if pd.isna(value):
        return 0

    value = str(value)
    value = value.replace(",", "")
    value = value.replace(" ", "")
    value = value.replace("　", "")
    value = value.strip()

    if value == "":
        return 0

    try:
        return int(value)
    except ValueError:
        return 0


def clean_population_data(raw_df):
    """
    將戶政司原始 CSV 整理成乾淨 DataFrame。

    原始欄位位置：
    0  : 縣市
    1  : 性別
    2  : 總人口
    3  : 0歲
    4  : 1~4歲小計
    9  : 5~9歲
    10 : 10~14歲
    11 : 15~19歲
    ...
    20 : 60~64歲
    21~28 : 65歲以上
    """

    records = []

    for _, row in raw_df.iterrows():
        year = row.get("year")

        city = clean_city_name(row.get(0))
        sex = row.get(1)

        if pd.isna(sex):
            continue

        sex = str(sex).strip()

        # 只保留「計、男、女」
        if sex not in ["計", "男", "女"]:
            continue

        # 原始資料中，縣市名稱只出現在「男」那一列
        # 「計」和「女」通常是 NaN，所以要先保留，後面用 ffill 補
        records.append({
            "year": year,
            "city": city,
            "sex": sex,

            "total": to_number(row.get(2)),

            "age_0": to_number(row.get(3)),
            "age_1_4": to_number(row.get(4)),
            "age_5_9": to_number(row.get(9)),
            "age_10_14": to_number(row.get(10)),

            "age_15_19": to_number(row.get(11)),
            "age_20_24": to_number(row.get(12)),
            "age_25_29": to_number(row.get(13)),
            "age_30_34": to_number(row.get(14)),
            "age_35_39": to_number(row.get(15)),
            "age_40_44": to_number(row.get(16)),
            "age_45_49": to_number(row.get(17)),
            "age_50_54": to_number(row.get(18)),
            "age_55_59": to_number(row.get(19)),
            "age_60_64": to_number(row.get(20)),

            "age_65_69": to_number(row.get(21)),
            "age_70_74": to_number(row.get(22)),
            "age_75_79": to_number(row.get(23)),
            "age_80_84": to_number(row.get(24)),
            "age_85_89": to_number(row.get(25)),
            "age_90_94": to_number(row.get(26)),
            "age_95_99": to_number(row.get(27)),
            "age_100_up": to_number(row.get(28)),
        })

    df = pd.DataFrame(records)

    if df.empty:
        raise ValueError("清理後沒有資料，請檢查 CSV 格式是否正確。")

    # 補縣市名稱
    df["city"] = df["city"].ffill()

    # 移除總計與非縣市資料
    df = df[df["city"].isin(VALID_CITIES)]

    # 過濾人口數異常資料
    df = df[df["total"] > 0]

    # 建立三大年齡層
    df["young_population"] = (
        df["age_0"] +
        df["age_1_4"] +
        df["age_5_9"] +
        df["age_10_14"]
    )

    df["working_age_population"] = (
        df["age_15_19"] +
        df["age_20_24"] +
        df["age_25_29"] +
        df["age_30_34"] +
        df["age_35_39"] +
        df["age_40_44"] +
        df["age_45_49"] +
        df["age_50_54"] +
        df["age_55_59"] +
        df["age_60_64"]
    )

    df["old_population"] = (
        df["age_65_69"] +
        df["age_70_74"] +
        df["age_75_79"] +
        df["age_80_84"] +
        df["age_85_89"] +
        df["age_90_94"] +
        df["age_95_99"] +
        df["age_100_up"]
    )

    return df
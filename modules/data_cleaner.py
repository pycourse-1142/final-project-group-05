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
    例如：
    '新 北 市' -> '新北市'
    '總　　計' -> '總計'
    """
    if pd.isna(name):
        return np.nan

    name = str(name)
    name = name.replace(" ", "")
    name = name.replace("　", "")
    name = name.replace("\t", "")
    name = name.strip()

    if name == "":
        return np.nan

    return name


def to_number(value):
    """
    將人口數轉成 int。
    例如：
    '4,044,831' -> 4044831
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


def make_record(year, city, sex, row):
    """
    把一列原始資料轉成乾淨資料。
    欄位位置依照你的 CSV：
    2  : 總人口
    3  : 0歲
    4  : 1~4歲小計
    9  : 5~9歲
    10 : 10~14歲
    11~20 : 15~64歲
    21~28 : 65歲以上
    """

    return {
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
    }


def clean_population_data(raw_df):
    """
    依照戶政司 CSV 結構整理資料。

    原始資料格式：
    city 空白，sex = 計   -> 該縣市總人口
    city 縣市，sex = 男   -> 該縣市男性人口
    city 空白，sex = 女   -> 該縣市女性人口

    因此不能直接 ffill。
    必須找到「男」那列的縣市名稱，再回推前一列為「計」。
    """

    records = []

    raw_df = raw_df.reset_index(drop=True)

    for i in range(len(raw_df)):
        row = raw_df.iloc[i]

        year = row.get("year")
        city = clean_city_name(row.get(0))
        sex = row.get(1)

        if pd.isna(sex):
            continue

        sex = str(sex).strip()

        # 只有「男」那列會有真正縣市名稱
        if sex != "男":
            continue

        # 排除總計、省級資料、空白資料
        if city not in VALID_CITIES:
            continue

        # 前一列必須是「計」，下一列必須是「女」
        if i - 1 < 0 or i + 1 >= len(raw_df):
            continue

        total_row = raw_df.iloc[i - 1]
        male_row = raw_df.iloc[i]
        female_row = raw_df.iloc[i + 1]

        total_sex = str(total_row.get(1)).strip()
        male_sex = str(male_row.get(1)).strip()
        female_sex = str(female_row.get(1)).strip()

        if total_sex != "計":
            continue

        if male_sex != "男":
            continue

        if female_sex != "女":
            continue

        total_value = to_number(total_row.get(2))
        male_value = to_number(male_row.get(2))
        female_value = to_number(female_row.get(2))

        # 基本檢查：總人口應接近男 + 女
        if abs(total_value - (male_value + female_value)) > 5:
            print(f"警告：{year} {city} 男女人口加總與總人口不一致")
            continue

        records.append(make_record(year, city, "計", total_row))
        records.append(make_record(year, city, "男", male_row))
        records.append(make_record(year, city, "女", female_row))

    df = pd.DataFrame(records)

    if df.empty:
        raise ValueError("清理後沒有資料，請檢查 CSV 格式是否正確。")

    df = df[df["total"] > 0]

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
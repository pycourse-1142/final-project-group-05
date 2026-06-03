import os
import pandas as pd


def load_one_file(file_path, year):
    """
    讀取單一年度 CSV。
    使用 header=None，因為原始資料不是乾淨表格。
    """
    try:
        df = pd.read_csv(file_path, encoding="utf-8-sig", header=None)
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding="cp950", header=None)

    df["year"] = year
    return df


def load_all_data(data_dir="data"):
    """
    讀取 110~114 年資料。
    支援兩種檔名：
    1. 110縣市人口按性別及五齡組.csv
    2. 110縣市人口按性別及五齡組(1).csv
    """
    all_data = []

    for year in range(110, 115):
        filename_1 = f"{year}縣市人口按性別及五齡組.csv"
        filename_2 = f"{year}縣市人口按性別及五齡組(1).csv"

        possible_paths = [
            os.path.join(data_dir, filename_1),
            os.path.join(data_dir, filename_2),
            filename_1,
            filename_2
        ]

        file_path = None

        for path in possible_paths:
            if os.path.exists(path):
                file_path = path
                break

        if file_path is None:
            print(f"找不到 {year} 年資料檔案")
            continue

        print(f"讀取：{file_path}")
        df = load_one_file(file_path, year)
        all_data.append(df)

    if len(all_data) == 0:
        raise FileNotFoundError("沒有讀到任何 CSV 檔案，請確認檔案名稱與位置。")

    return pd.concat(all_data, ignore_index=True)
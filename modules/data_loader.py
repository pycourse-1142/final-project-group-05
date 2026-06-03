import os
import pandas as pd


def load_one_file(file_path, year):
    """
    讀取單一年度 CSV。
    原始檔案不是標準乾淨表格，所以先用 header=None 讀入。
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
    會優先從 data/ 資料夾讀取。
    如果 data/ 找不到，會從專案根目錄讀取。
    """
    all_data = []

    for year in range(110, 115):
        filename = f"{year}縣市人口按性別及五齡組.csv"

        path_in_data = os.path.join(data_dir, filename)
        path_in_root = filename

        if os.path.exists(path_in_data):
            file_path = path_in_data
        elif os.path.exists(path_in_root):
            file_path = path_in_root
        else:
            print(f"找不到檔案：{filename}")
            continue

        print(f"讀取：{file_path}")
        df = load_one_file(file_path, year)
        all_data.append(df)

    if len(all_data) == 0:
        raise FileNotFoundError("沒有讀到任何 CSV 檔案，請確認檔案名稱與位置。")

    return pd.concat(all_data, ignore_index=True)
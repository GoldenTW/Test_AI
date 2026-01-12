import os
import pandas as pd
from pandas import DataFrame


def get_data_file_path(file_name: str) -> str:
    """回傳 data 資料夾內檔案的完整路徑。"""
    current_working_directory = os.getcwd()
    return os.path.join(current_working_directory, "data", file_name)


def merge_two_table(filename: str) -> DataFrame:
    """
    讀取每日各站進出站人數檔案，合併台鐵車站資訊（以車站代碼）。
    會把 staCode -> 車站代碼，並把車站資訊欄位改成中文。
    """
    # 讀每日進出站資料
    file_path = get_data_file_path(filename)
    data = pd.read_csv(file_path)

    # 乘客檔欄位常見是 staCode，先改成 車站代碼 才能合併
    if "車站代碼" not in data.columns:
        if "staCode" in data.columns:
            data = data.rename(columns={"staCode": "車站代碼"})
        else:
            raise KeyError(
                f"{filename} 找不到合併用欄位：'車站代碼' 或 'staCode'\n目前欄位：{list(data.columns)}"
            )

    # 讀車站資訊
    station_data_path = get_data_file_path("台鐵車站資訊.csv")
    station_data = pd.read_csv(station_data_path)

    # 車站檔欄位改成中文（只留需要的欄位也可以更乾淨）
    required_station_cols = ["stationCode", "stationName", "stationAddrTw"]
    missing = [c for c in required_station_cols if c not in station_data.columns]
    if missing:
        raise KeyError(
            f"台鐵車站資訊.csv 缺少欄位：{missing}\n目前欄位：{list(station_data.columns)}"
        )

    station_data_renamed = station_data[required_station_cols].rename(columns={
        "stationCode": "車站代碼",
        "stationName": "車站名稱",
        "stationAddrTw": "車站地址",
    })

    # 合併（left join：保留所有每日資料）
    merged_data = pd.merge(data, station_data_renamed, on="車站代碼", how="left")
    return merged_data


def get_datafolder_files() -> list[str]:
    """取得 data 資料夾內所有含 '每日各站進出站人數' 的檔名。"""
    current_working_directory = os.getcwd()
    data_directory = os.path.join(current_working_directory, "data")

    files_in_data_directory = [
        f for f in os.listdir(data_directory)
        if f.endswith(".csv") and "每日各站進出站人數" in f
    ]

    # 建議排序，避免每次讀進來順序亂跳（例如 2019~2025）
    files_in_data_directory.sort()
    return files_in_data_directory


def all_years_merge() -> DataFrame:
    all_files = get_datafolder_files()
    if not all_files:
        print("data 資料夾找不到 '每日各站進出站人數' 的 csv 檔案")
        return

    all_years_data: list[pd.DataFrame] = []
    for year_file in all_files:
        merged_table = merge_two_table(year_file)
        all_years_data.append(merged_table)

    # 你如果想要「一張總表」通常會 concat
    all_df = pd.concat(all_years_data, ignore_index=True)

    return all_df


def main():
    all_files = get_datafolder_files()
    if not all_files:
        print("data 資料夾找不到 '每日各站進出站人數' 的 csv 檔案")
        return

    all_years_data: list[pd.DataFrame] = []
    for year_file in all_files:
        merged_table = merge_two_table(year_file)
        all_years_data.append(merged_table)

    # 你如果想要「一張總表」通常會 concat
    all_df = pd.concat(all_years_data, ignore_index=True)

    print("檔案數量：", len(all_files))
    print("合併後總筆數：", len(all_df))
    print(all_df.head())



if __name__ == "__main__":
    main()
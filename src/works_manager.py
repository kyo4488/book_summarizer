import pandas as pd

# CSVファイルのパスを指定
CSV_FILE_PATH = "./works_db.csv"


def load_data():
    try:
        # 必要な列のみ読み込み
        df = pd.read_csv(CSV_FILE_PATH)
        required_columns = [
            "作品ID",
            "作品名",
            "ソート用読み",
            "XHTML/HTMLファイルURL",
            "姓名",
        ]
        df = df[required_columns]
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame()

# docker compose exec app python csv-to-xlsx/script.py
import pandas as pd

# CSVファイルのパス
csv_file = '/app/scripts/csv-to-xlsx/ログインした時間_202309.csv'
# 出力されるXLSXファイルのパス
xlsx_file = '/app/scripts/csv-to-xlsx/ログインした時間_202309.xlsx'

# CSVファイルを読み込む
df = pd.read_csv(csv_file)

# DataFrameをXLSXファイルとして保存する
df.to_excel(xlsx_file, index=False)

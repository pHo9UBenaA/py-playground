# docker compose exec app python table-element-extractor/create-tag.py
import csv

def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
    return data

def process_data(data):
    upper_levels = ['', '', '', '']

    results = []

    for row in data[1:]:  # ヘッダー行をスキップ
        current_level = ['', '', '', '']

        for i, value in enumerate(row):
            value = value.strip()
            if value:
                # 値がある場合、現在の階層を更新し、上位階層も更新
                current_level[i] = value
                upper_levels[i] = value
                # 下位階層をクリア
                for j in range(i + 1, 4):
                    upper_levels[j] = ''
                    current_level[j] = ''

        # 上位階層の値を使用して階層文字列を作成
        hierarchy = [upper_levels[i] if not current_level[i] else current_level[i] for i in range(4)]

        # 空でない値を組み合わせて結果を生成
        result = '-'.join(filter(None, hierarchy))
        results.append(result)

    return results


# CSVファイルのパス（適宜変更してください）
file_path = '/app/scripts/table-element-to-markdown/create-tag.csv'

# データの読み込みと処理
data = read_csv(file_path)
results = process_data(data)

# 結果の表示
for result in results:
    print(result)

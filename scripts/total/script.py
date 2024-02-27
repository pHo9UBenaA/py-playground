# https://github.com/pHo9UBenaA/ts-playground の cinii/script.ts の出力をもとに、特定の分類について集計を行うスクリプト
# docker compose exec app python total/script.py

# 抽出した要素は以下のawkコマンドで整形した
# awk -F ': ' '{gsub(/"/, "", $1); gsub(/ /, "", $1); printf "%s(%d), ", $1, $2}' input.txt | sed 's/, $/\n/' | sed 's/, $//' | tr -d '\n' | pbcopy

# ignoreKeysの指定を忘れていたものは以下のコマンドで加算
# echo "1+1" | bc | pbcopy

import os
import json
from collections import defaultdict

# プレフィックスリストの定義（サンプル値）
prefixes = ['articles_', 'books_', 'data_', 'dissertations_', 'person_', 'product_', 'projects_']

def aggregate_values(data, result):
    """
    再帰的にデータを探索し、末端のValueの集計を行い、オブジェクト形式で結果を格納する関数。
    data: 探索するデータ（辞書型またはリスト型）
    result: 現在の集計結果を保持する辞書
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if key not in result:
                result[key] = {}
            aggregate_values(value, result[key])
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and 'value' in item and 'count' in item:
                if 'values' not in result:
                    result['values'] = defaultdict(int)
                result['values'][item['value']] += item['count']

def load_and_aggregate_json(folder_path, prefixes):
    """
    指定されたフォルダ内のJSONファイルを読み込み、プレフィックスごとに集計を行う関数。
    folder_path: JSONファイルが格納されているフォルダのパス
    prefixes: プレフィックスのリスト
    """
    aggregate_results = {prefix: {} for prefix in prefixes}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                file_prefix = next((prefix for prefix in prefixes if file.startswith(prefix)), None)
                if file_prefix:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        aggregate_values(data, aggregate_results[file_prefix])
    return aggregate_results

# 集計を実行するフォルダのパスを指定
folder_path = '/app/scripts/total/target'

# 集計関数を実行して結果を取得
aggregate_results = load_and_aggregate_json(folder_path, prefixes)

# プレフィックスごとの結果の出力
for prefix, result in aggregate_results.items():
    print(f'Prefix: {prefix}')
    print(json.dumps(result, indent=4, ensure_ascii=False))

# BigQueryにて以下のようなクエリの出力結果を元に生成する
# SELECT
#   properties.value.int_value AS user_id,
#   user_pseudo_id,
#   MAX(FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', TIMESTAMP_TRUNC(timestamp_micros(event_timestamp), SECOND), "Asia/Tokyo")) as time,
#   SUM(params.value.int_value) / 1000 AS total_engagement_time_sec
# FROM
#   `product-12345.analytics_123456789.events_*`,
#   UNNEST(event_params) as params,
#   UNNEST(user_properties) as properties
# WHERE
#   -- 適宜変更
#   _TABLE_SUFFIX BETWEEN '20231001' AND '20231031'
#   -- https://support.google.com/analytics/answer/11109416?hl=ja
#   AND params.key = "engagement_time_msec"
#   AND params.value.int_value IS NOT NULL
#   -- nullの場合はログインされていない想定
#   -- 「user_id」にユーザーIDが含まれていない場合があるため、取り急ぎ以下にて絞り込み
#   AND properties.key = "product_user_id"
#   AND properties.value.int_value IS NOT NULL
# GROUP BY properties.value.int_value, user_pseudo_id
# ORDER BY properties.value.int_value
# ;

import pandas as pd
import sys

def process(file_path):
    # CSVを読み込む
    df = pd.read_csv(file_path, parse_dates=['time'], dtype={'user_pseudo_id': 'str', 'user_id': 'Int64'})

    # user_id が 0 と 1 の行を削除する
    df = df[~df['user_id'].isin([0, 1])]

    # user_id を基準にして、time でソートする
    df = df.sort_values(by=['user_id', 'time'])

    # user_id ごとに最初の行だけを取得する
    df = df.groupby('user_id').first().reset_index()

    # 文字列を生成する
    output = "\n".join(f"WHEN '{row['user_pseudo_id']}' THEN '{row['user_id']}'" for _, row in df.iterrows())
    print(output)

if __name__ == "__main__":
    csv_file_path = '/app/scripts/create-when-target.csv'
    process(csv_file_path)

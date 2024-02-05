# docker compose exec app python table-element-extractor/to-markdown.py
# 微調整は必要（配列の箇所やanyが文字列になってしまう箇所など
from bs4 import BeautifulSoup

def process_row(row, num_columns):
    # 各セルのデータを取得し、列数に合わせて調整
    cells = row.find_all(['th', 'td'])
    row_data = []
    is_header = False

    for cell in cells:
        # colspan属性がある場合、複数列にまたがるデータとして処理
        colspan = int(cell.get('colspan', 1))

        # <li>要素が含まれている場合は、特別に処理
        if cell.find('li'):
            cell_data = str(cell)
            cell_data = cell_data.replace('<td>', '').replace('</td>', '').replace('\n', '')
        else:
            cell_data = cell.get_text(strip=True)

        row_data.extend([cell_data] * colspan)

        # th要素が含まれているか確認
        if cell.name == 'th':
            is_header = True

    # 行の先頭に必要な数の空のセルを追加
    row_data = [""] * (num_columns - len(row_data)) + row_data
    return row_data, is_header

def to_array_key(is_array, key):
    if is_array:
        return key + '[]'
    return key

def array_to_dict(arr):
    if not arr:
        return "any"
    if isinstance(arr[0], list):
        result = {}
        for item in arr:
            key = item[0]
            # キーから`[]`を検出した場合、配列型として処理
            if key.endswith('[]'):
                key = key[:-2]  # キーから`[]`を削除
                # 残りの部分を再帰的に解析し、結果を配列型とする
                value = [array_to_dict(item[1:])]
            else:
                value = array_to_dict(item[1:])
            result[key] = value

        return result
    else:
        return "any"  # 直接の値の場合は、型を`any`として扱う


def convert_html_to_type(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')

    # 列数を決定（最もセル数が多い行を基準にする）
    num_columns = max(sum(int(cell.get('colspan', 1)) for cell in row.find_all(['th', 'td'])) for row in table.find_all('tr'))

    layered_row = []

    for index, row in enumerate(table.find_all('tr')):
        if (index == 0 or index == 1):
            continue

        # if(len(row) == num_columns):
            # row = row[1:]

        row_data, is_header = process_row(row, num_columns)
        tmp_row = [x.replace('\n', ' ') for x in row_data]

        tmp_row = tmp_row[2:7]

        is_array = False
        if '..' in tmp_row[4]:
            is_array = True

        if tmp_row[0] != '':

            layered_row.append([to_array_key(is_array, tmp_row[0])])
        if tmp_row[1] != '':
            layered_row[-1].append([to_array_key(is_array, tmp_row[1])])
        if tmp_row[2] != '':
            # layered_row[-1]がarrayであれば[-1][-1]に追加
            if isinstance(layered_row[-1][-1], list):
                layered_row[-1][-1].append([to_array_key(is_array, tmp_row[2])])
            else:
                layered_row[-1].append([to_array_key(is_array, tmp_row[2])])
        if tmp_row[3] != '':
            if isinstance(layered_row[-1][-1], list):
                if isinstance(layered_row[-1][-1][-1], list):
                    layered_row[-1][-1][-1].append([to_array_key(is_array, tmp_row[3])])
                else:
                    layered_row[-1][-1].append([to_array_key(is_array, tmp_row[3])])
            else:
                layered_row[-1].append([to_array_key(is_array, tmp_row[3])])


    print (layered_row)
    result = array_to_dict(layered_row)
    return result
        
    

# HTMLテーブルデータ（以下にHTMLテーブルデータを貼り付けます）
html_table_data = open('/app/scripts/table-element-extractor/table-element.html').read()

result = convert_html_to_type(html_table_data)
print(result)


# docker compose exec app python table-element-extractor/script.py
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

def convert_html_to_markdown(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')

    # 列数を決定（最もセル数が多い行を基準にする）
    num_columns = max(sum(int(cell.get('colspan', 1)) for cell in row.find_all(['th', 'td'])) for row in table.find_all('tr'))

    # テーブルデータの処理
    markdown_table = ""
    for row in table.find_all('tr'):
        row_data, is_header = process_row(row, num_columns)
        row_data = [x.replace('\n', '<br>') for x in row_data]

        markdown_table += "| " + " | ".join(row_data) + " |\n"

        # ヘッダー行の下に区切り線を追加
        if is_header:
            markdown_table += "| " + " | ".join(["---"] * num_columns) + " |\n"

    return markdown_table

def convert_html_to_csv(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')

    # 列数を決定（最もセル数が多い行を基準にする）
    num_columns = max(sum(int(cell.get('colspan', 1)) for cell in row.find_all(['th', 'td'])) for row in table.find_all('tr'))

    csv_table = ""
    for row in table.find_all('tr'):
        row_data, is_header = process_row(row, num_columns)
        row_data = [x.replace('\n', ' ') for x in row_data]
        # row_dataの配列から特定の要素のみ取得する
        # row_data = row_data[2:6]

        row_data = [x.replace('\n', ' ') for x in row_data]
        csv_table += ", ".join(row_data) + "\n"

    return csv_table

# HTMLテーブルデータ（以下にHTMLテーブルデータを貼り付けます）
html_table_data = open('/app/scripts/table-element-extractor/table-element.html').read()

# 変換実行
markdown_table = convert_html_to_markdown(html_table_data)
# csv_table = convert_html_to_csv(html_table_data)
print(markdown_table)

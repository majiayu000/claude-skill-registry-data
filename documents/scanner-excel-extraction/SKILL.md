---
name: scanner-excel-extraction
description: |
  Extract, transform, and structure data from Excel files including multiple sheets, formulas, and formatting. Use when processing Excel data or converting to other formats.

  This skill provides Excel data extraction:
  - Multiple sheet reading
  - Data structuring (JSON/CSV conversion)
  - Formula evaluation
  - Cell formatting extraction
  - Large file handling with chunking

  Triggers: "extract Excel data", "read spreadsheet", "convert Excel to JSON", "convert Excel to CSV", "Excel解析", "スプレッドシート処理", "データ抽出"
allowed-tools:
  - Bash
  - Write
---

# Scanner Excel Extraction Skill

## 概要

このSkillは、scannerエージェントがExcelファイルからデータを抽出し、構造化されたフォーマット（JSON、CSV）に変換する際に使用します。複数シート、数式、書式設定に対応しています。

## 主な機能

1. **複数シート読み込み**: すべてのシートを一括処理
2. **データ構造化**: JSON/CSV形式に変換
3. **数式評価**: セルの数式を計算値に変換
4. **書式情報抽出**: セルの色、太字等の書式
5. **大容量ファイル対応**: チャンク処理でメモリ効率化

## 使用方法

### スクリプト

```bash
python scripts/extract-excel.py <excel-path> [options]
```

**オプション**:
- `--output=json`: JSON形式で出力（デフォルト）
- `--output=csv`: CSV形式で出力（各シートごと）
- `--sheet=<name>`: 特定のシートのみ抽出
- `--evaluate-formulas`: 数式を計算値に変換

**使用例**:

```bash
# 全シートをJSONに変換
python scripts/extract-excel.py data.xlsx --output=json

# 特定シートのみCSVに変換
python scripts/extract-excel.py data.xlsx --sheet="Sheet1" --output=csv

# 数式を評価して出力
python scripts/extract-excel.py data.xlsx --evaluate-formulas
```

## 出力形式

### JSON形式

```json
{
  "Sheet1": [
    {"id": 1, "name": "Product A", "price": 1000},
    {"id": 2, "name": "Product B", "price": 2000}
  ],
  "Sheet2": [
    {"category": "Electronics", "count": 10}
  ]
}
```

### CSV形式

複数シートの場合、各シートごとにCSVファイルを生成:
- `data_Sheet1.csv`
- `data_Sheet2.csv`

## スクリプト詳細

### extract-excel.py

Excelファイルを読み込み、構造化されたデータに変換します。

**必要なライブラリ**:
```bash
pip install pandas openpyxl xlrd
```

**コード概要**:
```python
import pandas as pd
import json

def extract_excel(file_path, output_format='json', evaluate_formulas=False):
    # Excelファイルを読み込み
    excel_file = pd.ExcelFile(file_path)

    data = {}
    for sheet_name in excel_file.sheet_names:
        # 各シートを読み込み
        df = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            # 数式を評価するかどうか
            engine='openpyxl' if evaluate_formulas else 'xlrd'
        )

        if output_format == 'json':
            # JSON形式に変換
            data[sheet_name] = df.to_dict(orient='records')
        elif output_format == 'csv':
            # CSV形式で保存
            df.to_csv(f'{file_path.stem}_{sheet_name}.csv', index=False)

    if output_format == 'json':
        # JSONファイルに保存
        with open(f'{file_path.stem}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    return data
```

### convert-to-json.js

Excel→JSON変換（Node.js版）

```javascript
const XLSX = require('xlsx');
const fs = require('fs');

function extractExcel(filePath) {
  // Excelファイルを読み込み
  const workbook = XLSX.readFile(filePath);

  const data = {};

  // 各シートを処理
  workbook.SheetNames.forEach(sheetName => {
    const sheet = workbook.Sheets[sheetName];
    // JSONに変換
    data[sheetName] = XLSX.utils.sheet_to_json(sheet);
  });

  return data;
}
```

## 実装例

### 例1: 売上データの抽出

```python
# 売上データExcelを読み込み
data = extract_excel('sales-2023.xlsx', output_format='json')

# Sheet1（売上明細）を取得
sales_data = data['Sales']

# データフレームに変換して集計
import pandas as pd
df = pd.DataFrame(sales_data)

# 月別売上を集計
monthly_sales = df.groupby('month')['amount'].sum()
print(monthly_sales)

# 結果をCSVに保存
monthly_sales.to_csv('monthly-sales-summary.csv')
```

### 例2: 在庫データの構造化

```python
# 在庫管理Excelから複数シートを抽出
data = extract_excel('inventory.xlsx')

# 各シートのデータを処理
products = data['Products']  # 商品マスタ
inventory = data['Inventory']  # 在庫数
locations = data['Locations']  # 保管場所

# JSONファイルに保存（API連携用）
import json
with open('inventory-data.json', 'w', encoding='utf-8') as f:
    json.dump({
        'products': products,
        'inventory': inventory,
        'locations': locations
    }, f, ensure_ascii=False, indent=2)

print(f"✅ 商品数: {len(products)}件")
print(f"✅ 在庫レコード: {len(inventory)}件")
```

### 例3: 大容量Excelの処理

```python
# 大容量Excel（100万行以上）を効率的に処理
def process_large_excel(file_path, chunk_size=10000):
    # チャンクごとに読み込み
    for chunk in pd.read_excel(file_path, chunksize=chunk_size):
        # データ処理
        process_chunk(chunk)

        # メモリ解放
        del chunk

def process_chunk(df):
    # チャンクごとの処理（集計、変換等）
    summary = df.groupby('category')['value'].sum()
    # データベースに保存等
    save_to_database(summary)

# 実行
process_large_excel('large-data.xlsx')
```

## ベストプラクティス

### DO（推奨）

✅ **ヘッダー行を明確に**: 1行目をヘッダーとして使用
✅ **データ型の統一**: 各列のデータ型を統一
✅ **空白セルの処理**: NaN、Null、空文字の扱いを定義
✅ **大容量ファイルはチャンク処理**: メモリ効率化
✅ **エラーハンドリング**: 欠損値、不正な形式に対応

### DON'T（非推奨）

❌ **複雑な書式に依存**: シンプルな表形式が最適
❌ **結合セル**: データ抽出が困難
❌ **画像・チャート**: テキストデータのみ推奨
❌ **マクロ依存**: Pythonでは実行不可
❌ **全データをメモリに展開**: 大容量ファイルは危険

## データ型の扱い

### 日付

```python
# 日付を正しく読み込む
df = pd.read_excel('data.xlsx', parse_dates=['date_column'])

# 日付フォーマット変換
df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
```

### 数値

```python
# 数値として読み込む（カンマ区切りの数値対応）
df['amount'] = df['amount'].str.replace(',', '').astype(float)
```

### 文字列

```python
# 前後の空白を削除
df['name'] = df['name'].str.strip()
```

## トラブルシューティング

### Q: 日付が数値になってしまう
A: Excelの日付シリアル値です。変換が必要:
```python
df['date'] = pd.to_datetime(df['date'], unit='D', origin='1899-12-30')
```

### Q: 日本語が文字化けする
A: エンコーディングを指定:
```python
df = pd.read_excel('data.xlsx', encoding='utf-8')
```

### Q: メモリ不足エラー
A: チャンク処理を使用:
```python
for chunk in pd.read_excel('large.xlsx', chunksize=10000):
    process(chunk)
```

### Q: 数式が評価されない
A: openpyxlエンジンを使用:
```python
df = pd.read_excel('data.xlsx', engine='openpyxl')
```

## Progressive Disclosure

このSKILL.mdはメインドキュメント（約250行）です。詳細なスクリプトは `scripts/` ディレクトリ内のファイルを参照してください。

## 関連Skill

- **scanner-pdf-analysis**: PDF解析
- **data-analyst-export**: データエクスポート
- **data-analyst-sql-optimization**: 抽出データのDB格納最適化

## 関連リソース

- **scripts/extract-excel.py**: Excel抽出スクリプト（Python）
- **scripts/convert-to-json.js**: Excel→JSON変換スクリプト（Node.js）

---
name: data-analyst-export
description: |
  Export query results to various formats (CSV, JSON, Excel, Markdown tables) with proper formatting and headers. Use when saving analysis results to files.

  This skill provides data export utilities for multiple formats:
  - CSV: Comma-separated with headers, customizable delimiters
  - JSON: Structured data with pretty-print option
  - Excel: Multiple sheets, cell formatting, formulas
  - Markdown: Tables for documentation

  Triggers: "export data", "save results", "output CSV", "output JSON", "output Excel", "データ出力", "結果保存", "エクスポート"
allowed-tools:
  - Write
  - Bash
---

# Data Analyst Export Skill

## 概要

このSkillは、data-analystエージェントがクエリ結果を様々な形式でエクスポートする際に使用します。CSV、JSON、Excel、Markdownテーブルなど、用途に応じた最適な形式で出力できます。

## 主な機能

1. **CSV出力**: カンマ区切り、ヘッダー付き、カスタマイズ可能
2. **JSON出力**: 構造化データ、pretty-print、圧縮オプション
3. **Excel出力**: 複数シート、書式設定、数式サポート
4. **Markdownテーブル出力**: ドキュメントに埋め込み可能

## 使用方法

### CSV出力

```javascript
// scripts/export-csv.js を使用
node scripts/export-csv.js input.json output.csv
```

**入力データ形式** (input.json):
```json
[
  {"id": 1, "name": "Product A", "price": 1000},
  {"id": 2, "name": "Product B", "price": 2000}
]
```

**出力** (output.csv):
```csv
id,name,price
1,Product A,1000
2,Product B,2000
```

### JSON出力

```javascript
// scripts/export-json.js を使用
node scripts/export-json.js input.csv output.json --pretty
```

**オプション**:
- `--pretty`: 整形された見やすいJSON
- `--compact`: 圧縮されたJSON（デフォルト）

### Excel出力

```javascript
// scripts/export-excel.js を使用
node scripts/export-excel.js input.json output.xlsx --sheets "Sheet1,Sheet2"
```

**機能**:
- 複数シート対応
- ヘッダー行の書式設定（太字、背景色）
- 数値の書式（カンマ区切り、通貨）
- 自動列幅調整

### Markdown テーブル出力

```javascript
// scripts/export-markdown.js を使用
node scripts/export-markdown.js input.json output.md
```

**出力例**:
```markdown
| id | name | price |
|----|------|-------|
| 1 | Product A | 1000 |
| 2 | Product B | 2000 |
```

## スクリプト詳細

### export-csv.js

JSON配列をCSV形式に変換します。

**機能**:
- 自動ヘッダー生成
- カスタムデリミタ（カンマ、タブ、セミコロン）
- 引用符エスケープ
- UTF-8 BOM対応（Excel互換）

**使用例**:
```bash
# 基本的な使用
node export-csv.js data.json output.csv

# タブ区切り
node export-csv.js data.json output.tsv --delimiter="\t"

# Excel互換（BOM付き）
node export-csv.js data.json output.csv --bom
```

### export-json.js

CSV/配列データをJSON形式に変換します。

**機能**:
- Pretty-print（整形出力）
- 圧縮出力
- 配列またはオブジェクト形式

**使用例**:
```bash
# Pretty-print
node export-json.js data.csv output.json --pretty

# 圧縮
node export-json.js data.csv output.json --compact
```

### export-excel.js

JSON配列をExcelファイル(.xlsx)に変換します。

**機能**:
- 複数シート作成
- ヘッダー書式設定
- セルの書式設定（数値、通貨、日付）
- 列幅自動調整

**使用例**:
```bash
# 単一シート
node export-excel.js data.json output.xlsx

# 複数シート（各シートのデータはdata.jsonに含む）
node export-excel.js multi-sheet-data.json output.xlsx
```

**multi-sheet-data.json の形式**:
```json
{
  "Sheet1": [
    {"id": 1, "name": "Item 1"}
  ],
  "Sheet2": [
    {"id": 2, "name": "Item 2"}
  ]
}
```

### export-markdown.js

JSON配列をMarkdownテーブルに変換します。

**機能**:
- GitHub Flavored Markdown形式
- 列の自動整列
- 見出し行の区切り

**使用例**:
```bash
node export-markdown.js data.json output.md
```

## 実装例

### 例1: BigQueryクエリ結果をCSVにエクスポート

```javascript
// クエリ実行（BigQuery MCP使用）
const results = await bigquery.query("SELECT * FROM dataset.table LIMIT 1000");

// CSVに変換
const fs = require('fs');
const exportCSV = require('./scripts/export-csv.js');

exportCSV(results, 'query-results.csv');
console.log('✅ CSVにエクスポート完了: query-results.csv');
```

### 例2: 分析結果をExcelレポートに出力

```javascript
// 複数の分析結果を取得
const salesData = await bigquery.query("SELECT * FROM sales");
const productData = await bigquery.query("SELECT * FROM products");

// 複数シートでExcel出力
const data = {
  "Sales": salesData,
  "Products": productData
};

exportExcel(data, 'monthly-report.xlsx');
console.log('✅ Excelレポート作成完了: monthly-report.xlsx');
```

### 例3: ドキュメントにMarkdownテーブル挿入

```javascript
// クエリ結果を取得
const topProducts = await bigquery.query("SELECT name, sales FROM products ORDER BY sales DESC LIMIT 10");

// Markdownテーブルに変換
const markdown = exportMarkdown(topProducts);

// README.mdに挿入
const readme = fs.readFileSync('README.md', 'utf-8');
const updatedReadme = readme.replace('<!-- TOP_PRODUCTS -->', markdown);
fs.writeFileSync('README.md', updatedReadme);

console.log('✅ README.mdにテーブルを挿入しました');
```

## ベストプラクティス

### DO（推奨）

✅ **適切な形式を選択**: CSV（単純データ）、Excel（複雑なレポート）、JSON（API連携）
✅ **ヘッダーを含める**: データの意味を明確に
✅ **大きなデータはストリーミング**: メモリ効率のため
✅ **UTF-8 BOMを付与**: Excel互換性のため（CSV）
✅ **エラーハンドリング**: ファイル書き込みエラーに対処

### DON'T（非推奨）

❌ **全データをメモリに展開**: 大量データは分割処理
❌ **Excel形式で巨大データ**: 1048576行の制限に注意
❌ **日付フォーマットの不統一**: ISO 8601形式を推奨
❌ **特殊文字のエスケープ忘れ**: CSV/JSONで必須

## トラブルシューティング

### Q: Excelで日本語が文字化けする
A: UTF-8 BOMを付与してください:
```bash
node export-csv.js data.json output.csv --bom
```

### Q: 大きなデータでメモリ不足
A: ストリーミング処理に変更:
```javascript
// ストリーミング版のスクリプトを使用
node export-csv-stream.js large-data.json output.csv
```

### Q: Excelの行数制限（1048576行）を超える
A: 複数ファイルに分割:
```javascript
// 100万行ごとに分割
node export-excel.js data.json output --split 1000000
// output-1.xlsx, output-2.xlsx, ... が生成される
```

## Progressive Disclosure

このSKILL.mdはメインドキュメント（約250行）です。各スクリプトの詳細な実装は `scripts/` ディレクトリ内のファイルを参照してください。

## 関連リソース

- **scripts/export-csv.js**: CSV出力スクリプト
- **scripts/export-json.js**: JSON出力スクリプト
- **scripts/export-excel.js**: Excel出力スクリプト
- **scripts/export-markdown.js**: Markdownテーブル出力スクリプト

---
name: scanner-pdf-analysis
description: |
  Analyze PDF documents with table extraction, section identification, and content summarization. Use when reading technical documents, reports, or papers.

  This skill provides PDF analysis capabilities:
  - Text extraction and OCR
  - Table detection and CSV conversion
  - Section and heading identification
  - Key points summarization
  - Metadata extraction

  Triggers: "analyze PDF", "extract tables", "summarize document", "read PDF", "PDF解析", "テーブル抽出", "ドキュメント要約"
allowed-tools:
  - Bash
  - Write
---

# Scanner PDF Analysis Skill

## 概要

このSkillは、scannerエージェントがPDFドキュメントを分析し、構造化されたデータを抽出する際に使用します。テーブル抽出、セクション識別、要約生成などの機能を提供します。

## 主な機能

1. **テキスト抽出**: PDFからテキストを抽出
2. **テーブル抽出**: 表をCSV/JSON形式に変換
3. **セクション識別**: 見出しと構造を認識
4. **要約生成**: 重要なポイントを抽出
5. **メタデータ取得**: ページ数、作成日等

## 使用方法

### スクリプト

```bash
python scripts/analyze-pdf.py <pdf-path> [options]
```

**オプション**:
- `--extract-tables`: テーブルを抽出
- `--summarize`: 要約を生成
- `--output=<path>`: 出力ファイルパス

**使用例**:

```bash
# 基本的な分析
python scripts/analyze-pdf.py report.pdf

# テーブル抽出 + 要約
python scripts/analyze-pdf.py report.pdf --extract-tables --summarize

# 出力ファイル指定
python scripts/analyze-pdf.py report.pdf --output=analysis-result.md
```

## 出力形式

### 分析結果（Markdown）

```markdown
# report.pdf 分析結果

## 概要
- ページ数: 25
- テーブル数: 3
- 作成日: 2023-12-01

## 重要ポイント
1. [ポイント1]
2. [ポイント2]
3. [ポイント3]

## 抽出テーブル

### テーブル1 (ページ 5)
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| A   | B   | C   |

### テーブル2 (ページ 12)
[...]

## セクション構造
1. はじめに (p.1)
2. 背景 (p.3)
3. 方法 (p.7)
4. 結果 (p.15)
5. 結論 (p.23)

## 全文テキスト
[抽出されたテキスト...]
```

## スクリプト詳細

### analyze-pdf.py

PDFを解析し、構造化されたデータを抽出します。

**必要なライブラリ**:
```bash
pip install PyPDF2 tabula-py pdfplumber
```

**機能**:
- PyPDF2: テキスト抽出、メタデータ取得
- tabula-py: テーブル抽出（Java必要）
- pdfplumber: 高精度なレイアウト解析

**コード概要**:
```python
import PyPDF2
import tabula
import pdfplumber

def analyze_pdf(pdf_path):
    # メタデータ取得
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        page_count = len(reader.pages)

        # テキスト抽出
        text = ''.join([page.extract_text() for page in reader.pages])

    # テーブル抽出
    tables = tabula.read_pdf(pdf_path, pages='all')

    # pdfplumberでレイアウト解析
    with pdfplumber.open(pdf_path) as pdf:
        # セクション識別（フォントサイズで判定）
        sections = extract_sections(pdf)

    return {
        'page_count': page_count,
        'text': text,
        'tables': tables,
        'sections': sections
    }
```

## 実装例

### 例1: 技術仕様書の分析

```python
# 技術仕様書から要件を抽出
result = analyze_pdf('spec.pdf', extract_tables=True)

# テーブル（要件一覧）をCSVに保存
for i, table in enumerate(result['tables']):
    table.to_csv(f'requirements_{i}.csv', index=False)

# 要約をMarkdownに保存
with open('spec-summary.md', 'w') as f:
    f.write(f"# 仕様書要約\n\n")
    f.write(f"ページ数: {result['page_count']}\n\n")
    f.write(f"## 抽出要件\n\n")
    for i, table in enumerate(result['tables']):
        f.write(f"### 要件テーブル {i+1}\n\n")
        f.write(table.to_markdown())
        f.write("\n\n")
```

### 例2: 論文の要約

```python
# 論文PDFを読み込み
result = analyze_pdf('research-paper.pdf', summarize=True)

# 重要なセクションを抽出
sections_of_interest = ['Abstract', 'Introduction', 'Conclusion']
summary = []

for section in result['sections']:
    if section['title'] in sections_of_interest:
        summary.append(f"## {section['title']}\n{section['text']}\n")

# 要約を保存
with open('paper-summary.md', 'w') as f:
    f.write('\n'.join(summary))
```

### 例3: 請求書からデータ抽出

```python
# 請求書PDFからテーブル抽出
result = analyze_pdf('invoice.pdf', extract_tables=True)

# 最初のテーブル（請求明細）を取得
invoice_items = result['tables'][0]

# CSVに変換
invoice_items.to_csv('invoice-items.csv', index=False)

# 合計金額を計算
total = invoice_items['金額'].sum()
print(f"合計金額: {total}円")
```

## ベストプラクティス

### DO（推奨）

✅ **高品質なPDF**: テキストベースのPDFが最適
✅ **ページ範囲指定**: 必要なページのみ処理
✅ **テーブル抽出の検証**: 手動で確認
✅ **OCR使用**: 画像ベースPDFにはOCRが必要

### DON'T（非推奨）

❌ **スキャンPDFに直接適用**: OCR前処理が必要
❌ **複雑なレイアウト**: カラム、図表が多いと精度低下
❌ **暗号化PDF**: パスワード解除が必要
❌ **大量ページの一括処理**: メモリ不足の可能性

## トラブルシューティング

### Q: テキストが抽出できない
A: 画像ベースPDFの可能性があります。OCR（Tesseract）を使用してください:
```bash
pip install pytesseract
# OCRでテキスト抽出
python scripts/analyze-pdf.py --ocr document.pdf
```

### Q: テーブルが正しく抽出されない
A: 複数の方法を試してください:
1. tabula-py（Java必要）
2. pdfplumber（Python純正）
3. camelot-py（高精度）

### Q: 日本語が文字化けする
A: エンコーディングを指定:
```python
text = extract_text(pdf_path, encoding='utf-8')
```

## Progressive Disclosure

このSKILL.mdはメインドキュメント（約200行）です。詳細なスクリプトとテンプレートは `scripts/`, `templates/` ディレクトリ内のファイルを参照してください。

## 関連Skill

- **scanner-excel-extraction**: Excelファイル解析
- **data-analyst-export**: 抽出データのエクスポート

## 関連リソース

- **scripts/analyze-pdf.py**: PDF解析スクリプト
- **templates/pdf-summary-template.md**: 分析結果テンプレート

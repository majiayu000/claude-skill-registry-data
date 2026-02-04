---
name: document-processing
description: PDF、Excel、Wordドキュメントの読み取り・作成・編集・変換。テキスト抽出、フォーム入力、レポート生成、データ変換。「PDF」「Excel」「Word」「ドキュメント」「レポート」「スプレッドシート」に関する質問で使用。
---

# ドキュメント処理

## クイックスタート

### PDF テキスト抽出

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
```

### Excel 読み込み

```python
import pandas as pd

df = pd.read_excel("data.xlsx", sheet_name="Sheet1")
print(df.head())
```

### Word 作成

```python
from docx import Document

doc = Document()
doc.add_heading("タイトル", 0)
doc.add_paragraph("本文テキスト")
doc.save("output.docx")
```

## ファイル形式別ガイド

| 形式 | 読み取り | 作成 | 編集 |
|------|----------|------|------|
| PDF | pdfplumber, PyMuPDF | reportlab, fpdf2 | PyMuPDF |
| Excel | pandas, openpyxl | pandas, openpyxl | openpyxl |
| Word | python-docx | python-docx | python-docx |
| CSV | pandas | pandas | pandas |

## 詳細ガイド

- **PDF操作**: [reference/pdf.md](reference/pdf.md)
- **Excel操作**: [reference/excel.md](reference/excel.md)
- **Word操作**: [reference/word.md](reference/word.md)
- **データ変換**: [reference/conversion.md](reference/conversion.md)

## ユーティリティスクリプト

```bash
# PDFからテキスト抽出
python scripts/extract_pdf.py input.pdf --output text.txt

# Excel→CSV変換
python scripts/excel_to_csv.py data.xlsx --sheet "Sheet1"

# Wordテンプレート埋め込み
python scripts/fill_template.py template.docx data.json output.docx
```

## ワークフロー: ドキュメント処理

```
進捗チェックリスト:
- [ ] 1. 入力ファイル確認・形式判定
- [ ] 2. データ抽出/読み込み
- [ ] 3. データ処理・変換
- [ ] 4. 出力ファイル生成
- [ ] 5. 検証（ファイル破損チェック）
```

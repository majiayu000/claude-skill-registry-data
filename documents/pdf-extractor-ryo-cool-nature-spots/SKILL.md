---
name: pdf-extractor
description: PDFファイルからテキストやフォームデータを抽出・分析します。
meta: true
---

# PDF Extractor Skill

このスキルはPDFファイルから情報を抽出し、構造化データとして返します。

## 機能

- **テキスト抽出**: PDFの全テキストを抽出
- **フォーム解析**: PDFフォームのフィールドと値を抽出
- **メタデータ取得**: 作成者、作成日、ページ数などのメタ情報

## 使用方法

### 基本的な使い方

```
Input: "docs/report.pdf"
Output: 抽出されたテキストとメタデータをJSON形式で返却
```

### 実装アプローチ

1. **Rubyを使用する場合**:
   ```ruby
   # Gemfile に追加
   gem 'pdf-reader'

   # 使用例
   require 'pdf-reader'
   reader = PDF::Reader.new('path/to/file.pdf')
   reader.pages.each { |page| puts page.text }
   ```

2. **コマンドラインツールを使用する場合**:
   ```bash
   # pdftotext (poppler-utils)
   pdftotext input.pdf output.txt

   # pdftk でフォームデータ抽出
   pdftk input.pdf dump_data_fields
   ```

## 出力形式

```json
{
  "file": "docs/report.pdf",
  "pages": 10,
  "text": "抽出されたテキスト全文",
  "metadata": {
    "author": "作成者名",
    "created_at": "2024-01-01",
    "title": "ドキュメントタイトル"
  },
  "fields": [
    {
      "name": "field_name",
      "value": "field_value",
      "type": "text"
    }
  ]
}
```

## 使用例

### 例1: ドキュメントからテキスト抽出

```
User: Extract text from docs/requirements.pdf
Agent: [PDF extractorスキルを使用してテキストを抽出]
```

### 例2: フォームデータの解析

```
User: Parse form data from docs/application_form.pdf
Agent: [フォームフィールドと値を抽出してJSON形式で返却]
```

## サンプルスクリプト

```ruby
#!/usr/bin/env ruby
# scripts/extract_pdf.rb

require 'pdf-reader'
require 'json'

def extract_pdf(file_path)
  reader = PDF::Reader.new(file_path)

  data = {
    file: file_path,
    pages: reader.page_count,
    text: '',
    metadata: {
      title: reader.info[:Title],
      author: reader.info[:Author],
      created_at: reader.info[:CreationDate]
    }
  }

  reader.pages.each do |page|
    data[:text] += page.text + "\n"
  end

  puts JSON.pretty_generate(data)
end

if __FILE__ == $0
  extract_pdf(ARGV[0])
end
```

## インストール要件

### Ruby Gem
```bash
cd back
bundle add pdf-reader
```

### システムツール（オプション）
```bash
# macOS
brew install poppler

# Ubuntu/Debian
apt-get install poppler-utils
```

## 注意事項

- **meta: true**: スキルの内部実装は隠蔽され、使用方法のみが公開されます
- **読み取り専用**: PDFファイルの変更は行いません
- **エンコーディング**: 日本語PDFの場合、エンコーディングに注意が必要
- **セキュリティ**: アップロードされたPDFを処理する場合は、ファイルサイズとコンテンツの検証を行う

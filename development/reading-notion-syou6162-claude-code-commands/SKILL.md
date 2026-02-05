---
name: reading-notion
description: Notion URLが会話に登場した時、またはNotionのコンテンツを検索・取得する必要がある時に使用してください。
allowed-tools: Bash, Read
---

# Reading Notion

NotionページやドキュメントをMarkdownに変換して読み取り、内容を要約・説明するスキルです。

## 概要

このスキルは2つのモードで動作します：

1. **URL直接モード**: Notion URLが会話に登場した時、`notion-to-md`を使って自動的にMarkdownに変換し、内容を説明
2. **検索モード**: キーワードでNotionを検索し、結果から選択したページの内容を説明

**URL直接モード**では、Go製のCLIツール`notion-to-md`を使用してNotion APIからページデータを取得し、Markdown形式に変換します。これにより、ネスト構造、豊富なブロックタイプ、テキストアノテーションなどを正確に保持したMarkdownファイルが生成されます。


## モード詳細

<trigger>

### URL直接モード

Notion URLを検出すると自動的に発動します。詳細は **reference/url-mode.md** を参照してください。

**発動例**:
- ユーザーが `https://www.notion.so/myorg/abc123def456ghi789jkl012mno34567` のようなURLを提示
- 会話中にNotion URLが登場

### 検索モード

キーワードでNotion内を検索したい時に発動します。詳細は **reference/search-mode.md** を参照してください。

**発動例**:
- 「データ基盤チームについて教えて」
- 「Notionでプロジェクト〇〇を検索して」
- 特定のキーワードに関する情報を求められた時

</trigger>

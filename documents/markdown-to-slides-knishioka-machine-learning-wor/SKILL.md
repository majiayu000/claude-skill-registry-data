---
name: markdown-to-slides
description: |
  MarkdownファイルをPowerPointプレゼンテーション（PPTX）に変換するSkill。
  「Markdownをスライドに変換して」「プレゼン資料を作って」「PPTXを生成して」
  などのリクエストで自動発火する。python-pptxライブラリを使用。
allowed-tools: Bash, Read, Write, Glob
---

# Markdown → スライド変換 Skill

MarkdownドキュメントをPowerPointプレゼンテーションに変換します。

## クイックスタート

```bash
python scripts/md2slides.py input.md output.pptx
```

## Markdown記法

### スライド区切り

| 記法 | 動作 |
|------|------|
| `# 見出し1` | タイトルスライドを作成 |
| `## 見出し2` | 新しいコンテンツスライドを作成 |
| `---` | 強制的にスライドを分割 |

### サポートする要素

- **太字** と *斜体* テキスト
- 箇条書きリスト（2階層までネスト可）
- 番号付きリスト
- コードブロック（等幅フォントで表示）
- 画像 `![alt](path)` （ローカルパスのみ）

## ワークフロー

1. **ソースMarkdownを読み込む** - Readツールでコンテンツ取得
2. **PPTXに変換** - 変換スクリプトを実行
3. **出力を確認** - 生成ファイルの存在確認

## スクリプトインターフェース

### 入力
```bash
python scripts/md2slides.py <input.md> [output.pptx] [--title "タイトル"]
```

### 出力
- 成功: 出力パスを stdout に表示、終了コード 0
- 失敗: エラーを stderr に表示、終了コード 1

### オプション
- `--title`: プレゼンテーションタイトルを上書き（デフォルト: 最初のH1またはファイル名）
- `--theme`: カラーテーマ（default, dark, corporate）
- `--aspect`: アスペクト比（16:9, 4:3）デフォルト: 16:9

## エラーハンドリング

| エラー | 原因 | 対処 |
|--------|------|------|
| 入力ファイルが見つからない | パスが間違っている | パスを確認 |
| 無効なMarkdown | 構文エラー | 該当箇所をスキップして警告 |
| 画像が見つからない | パスが間違っている | プレースホルダーを表示 |

## 使用例

### 基本的な使い方
```bash
python scripts/md2slides.py presentation.md slides.pptx
```

### オプション指定
```bash
python scripts/md2slides.py notes.md output.pptx --title "Q4レビュー" --theme corporate
```

## テスト実行

```bash
cd /path/to/markdown-to-slides
pytest tests/ -v
```

## 依存関係

- python-pptx（Claude API環境ではプリインストール済み）
- 標準ライブラリのみ（パース処理）

## ファイル構成

```
markdown-to-slides/
├── SKILL.md           # このファイル
├── scripts/
│   ├── md2slides.py   # CLIエントリポイント
│   ├── parser.py      # Markdownパース
│   └── generator.py   # PPTX生成
├── tests/
│   └── test_md2slides.py
└── resources/
    └── example.md     # サンプル入力
```

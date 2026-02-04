---
name: Logging Implementation
description: Manage implementation logs in _docs/templates/ with consistent format. Use when starting project work, completing implementations, or when user mentions 実装ログ/implementation log.
allowed-tools: Read, Write, Edit, Bash
---

# Logging Implementation

プロジェクト全体で一貫した実装ログ管理を行うスキル。

## いつ使うか

- プロジェクトでの実装作業開始時
- 実装が完了した時
- 過去の実装履歴を参照する必要がある時
- ユーザーが「実装ログ」について言及した時

## プロジェクト起動時の処理

1. `_docs/templates/` が存在するか確認
2. 存在しない場合は `_docs/templates/` を作成
3. `_docs/` 配下を全てコンテキストとして読み込み
4. **前回の設計意図や副作用を踏まえた上で提案**

## 実装完了時の処理

### 1. 日時取得
- TIME MCP Server を優先
- 利用不可の場合は `now` エイリアス（`date "+%Y-%m-%d %H:%M:%S"`）
- エイリアス未設定の場合は `.zshrc` 等に追加提案

### 2. ログファイル作成
- **ファイル名形式**: `yyyy-mm-dd_機能名.md`
- **命名規則**: 複数単語の場合はケバブケース（例：`2025-10-19_product-name.md`）
- **保存先**: `_docs/templates/`

### 3. ログテンプレート

```md
機能名: <ここに機能名>

- 日付: yyyy-mm-dd HH:MM:SS
- 概要: <実装の目的・背景>
- 実装内容: <主な実装内容>
- 設計意図: <なぜこの設計にしたのか>
- 副作用: <懸念事項があれば明記>
- 関連ファイル: <ファイルの場所>
```

## 必須項目

実装ログには以下を**必ず**含めること：
- 実装の目的・背景
- 主な実装内容
- 設計意図
- 副作用
- 関連ファイル

## 重要な注意事項

- 実装ログは**必ず必ず必ず**残すこと
- 過去の実装ログを参照し、矛盾や重複を避けること
- 日時を正確に取得し、西暦-日付-時間で必ず記載すること（例：日付: 2100-01-01 11:11:11）

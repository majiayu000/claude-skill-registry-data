---
name: Managing Timecard
description: Handle timecard punch-in/out operations using /dakoku command. Use when user executes /dakoku, needs to record work hours, or mentions timecard/勤怠/打刻.
allowed-tools: Bash, Read, Write, Edit
---

# Managing Timecard

`/dakoku` コマンドによる勤怠打刻機能を管理するスキル。

## いつ使うか

- ユーザーが `/dakoku in | out | break | list | month` を実行した時
- 勤怠記録の参照・管理が必要な時
- 勤怠、打刻、タイムカードに関する質問があった時

## 日時取得の優先順位

1. **第一優先**: TIME MCP Server を使用
2. **第二優先**: ユーザー環境の `now` エイリアス（`date "+%Y-%m-%d %H:%M:%S"`）
3. **最終手段**: `date` コマンドでローカル時刻を取得

## 実行手順

### 1. コマンド仕様の確認
詳細は `.claude/commands/dakoku.md` を参照すること。

### 2. 保存処理
- **パス**: `_docs/timecard/YYYY/MM/`
- **形式**: Markdown と JSON の 2 形式で保存
- ディレクトリが存在しない場合は自動作成

### 3. エラーハンドリング
- TIME MCP Server が利用できない場合は、必ずフォールバック処理を実行
- `now` エイリアスが未設定の場合は、`.zshrc` への追加を提案

## 参考リンク

- 詳細仕様: `.claude/commands/dakoku.md`
- 実装記事: https://izanami.dev/post/5c7c7960-6316-4f44-a645-2dbbeefc3391

---
name: reload-context
description: ユーザーメモリ、プロジェクトメモリ、READMEを再読み込み。「コンテキストを再読み込み」「設定をリロード」「CLAUDE.mdを読み直して」と言われた時、またはclear後にコンテキストを復元したい時に使用
allowed-tools:
  - Read
  - Bash
---

# Reload Context

このスキルはload_context.shのキャッシュをクリアし、コンテキストファイルを強制的に再読み込みします。

## 仕組み

通常、コンテキストは`load_context.sh`フックにより1時間キャッシュされます。このスキルはキャッシュを削除することで、ファイル編集後すぐに変更を反映させます。

## 実行手順

### 1. キャッシュをクリア

プロジェクトごとのキャッシュファイルを削除します：

```bash
rm -f /tmp/claude_context_timestamp_*
```

### 2. ユーザーメモリの読み込み

```bash
Read ~/.claude/CLAUDE.md
```

グローバルなユーザーメモリを読み込みます。

### 3. プロジェクトメモリの読み込み

以下の優先順位でプロジェクトメモリを探して読み込みます：

1. `CLAUDE.md`（プロジェクトルート）
2. `.claude/CLAUDE.md`（.claudeディレクトリ内）

```bash
# まずCLAUDE.mdを探す
Read CLAUDE.md

# 存在しない場合は.claude/CLAUDE.mdを探す
Read .claude/CLAUDE.md
```

### 4. READMEの読み込み

```bash
Read README.md
```

## 表示形式

読み込んだコンテキストは以下の形式で表示します：

```markdown
# Context Reloaded (Cache Cleared)

## User Memory (Global)
[~/.claude/CLAUDE.mdの内容]

## Project Memory
[CLAUDE.mdまたは.claude/CLAUDE.mdの内容]

## README
[README.mdの内容]
```

## 使用例

### 例1: CLAUDE.mdを編集した後
```
ユーザー: 「コンテキストを再読み込みして」
アシスタント:
1. キャッシュをクリア
2. ~/.claude/CLAUDE.mdを読み込み（グローバル）
3. CLAUDE.mdまたは.claude/CLAUDE.mdを読み込み（プロジェクト）
4. README.mdを読み込み
5. すべての内容を整形して表示
```

### 例2: clear後にコンテキストを確認したい
```
ユーザー: 「/reload-context」
アシスタント:
1. キャッシュをクリア
2. 最新のユーザーメモリを読み込み
3. 最新のプロジェクトメモリを読み込み
4. 最新のREADMEを読み込み
5. 現在のコンテキスト状態を表示
```

## 注意事項

- ファイルが存在しない場合は、その旨を通知します
- `.claude/rules/*.md`はClaude Codeが自動的に読み込むため、このスキルでは表示しません
- キャッシュクリアにより、次回ツール実行時に`load_context.sh`が再実行されます

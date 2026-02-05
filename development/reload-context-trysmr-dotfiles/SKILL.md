---
name: reload-context
description: ユーザーメモリ、プロジェクトメモリ、READMEを再読み込み。「コンテキストを再読み込み」「設定をリロード」「CLAUDE.mdを読み直して」と言われた時、またはclear後にコンテキストを復元したい時に使用
allowed-tools: Read
---

# Reload Context

このスキルはユーザーメモリ、プロジェクトメモリ、READMEを再読み込みして、最新のコンテキスト情報を表示します。

## 実行手順

### 1. ユーザーメモリの読み込み

```bash
Read ~/.claude/CLAUDE.md
```

グローバルなユーザーメモリが存在する場合、その内容を読み込みます。

### 2. プロジェクトメモリの読み込み

以下の優先順位でプロジェクトメモリを探して読み込みます：

1. `CLAUDE.md`（プロジェクトルート）
2. `.claude/CLAUDE.md`（.claudeディレクトリ内）

```bash
# まずCLAUDE.mdを探す
Read CLAUDE.md

# 存在しない場合は.claude/CLAUDE.mdを探す
Read .claude/CLAUDE.md
```

### 3. READMEの読み込み

```bash
Read README.md
```

プロジェクトのREADME.mdが存在する場合、その内容を読み込みます。

## 表示形式

読み込んだコンテキストは以下の形式で表示します：

```markdown
# Context Reloaded

## User Memory (Global)
[~/.claude/CLAUDE.mdの内容]

## Project Memory
[CLAUDE.mdまたは.claude/CLAUDE.mdの内容]

## README
[README.mdの内容]
```

## 使用例

### 例1: コンテキストが更新された後
```
ユーザー: 「コンテキストを再読み込みして」
アシスタント:
1. ~/.claude/CLAUDE.mdを読み込み（グローバル）
2. CLAUDE.mdまたは.claude/CLAUDE.mdを読み込み（プロジェクト）
3. README.mdを読み込み
4. すべての内容を整形して表示
```

### 例2: clear後にコンテキストを確認したい
```
ユーザー: 「/reload-context」
アシスタント:
1. 最新のユーザーメモリを読み込み
2. 最新のプロジェクトメモリを読み込み
3. 最新のREADMEを読み込み
4. 現在のコンテキスト状態を表示
```

## 注意事項

- ファイルが存在しない場合は、その旨を通知します
- 複数のコンテキストファイルが存在する場合は、すべて表示します
- このスキルは読み込みのみで、ファイルの編集は行いません

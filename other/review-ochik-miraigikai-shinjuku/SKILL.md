---
name: review
description: コードレビュー・テストガイドラインチェック・コード品質チェックを同時実行する
---

# Review

コードレビュー・テストガイドラインチェック・コード品質チェックを**同時に実行**するセルフレビュースキル。

## 使い方

引数なしで実行すると、main ブランチとの差分をレビューする。

```
/review
/review "セキュリティ面を重点的にチェックして"
```

## ワークフロー

### Step 1: 差分の確認

まず現在のブランチと変更内容を確認する:

```bash
git branch --show-current
git diff --stat main...HEAD
```

変更がない場合（かつ未コミット変更もない場合）はユーザーに通知して終了。
未コミット変更がある場合は `git diff --stat` で確認する。

### Step 2: 3つのチェックを同時実行

以下の3つを **並列に** 起動する（同一メッセージ内で3つの Tool call を発行）:

#### 2a. Codex Review（Bashで実行）

ユーザーから追加の指示（引数）があればそれを PROMPT として渡す。

```bash
# 引数なしの場合
codex review --base main

# 引数ありの場合（例: "セキュリティ面を重点的にチェック"）
codex review --base main "{ユーザーの指示}"
```

コマンドのタイムアウトは5分（300000ms）に設定する。

#### 2b. テストガイドラインチェック（Agent ツールで実行）

`.claude/agents/test-guidelines-checker.md` の内容に従い、`subagent_type: "general-purpose"` の Agent エージェントを起動してテストガイドラインの遵守状況をチェックする。

#### 2c. コード品質チェック（Agent ツールで実行）

`.claude/agents/code-quality-checker.md` の内容に従い、`subagent_type: "general-purpose"` の Agent エージェントを起動して可読性・保守性・コード品質をチェックする。

**重要**: 2a, 2b, 2c は必ず並列（同一メッセージ内で3つの Tool call）で実行すること。

### Step 3: 結果の報告

3つの結果をまとめてユーザーに表示する:

1. **Codex Review 結果**: Codex の出力をそのまま表示
2. **テストガイドラインチェック結果**: エージェントの出力をそのまま表示
3. **コード品質チェック結果**: エージェントの出力をそのまま表示

## 注意事項

- `codex` CLI がインストール済みであること（`command -v codex` で確認）。未導入の場合（2026-10-08 時点で未導入）は 2a の代わりに `mirai-gikai-auditor` エージェントで差分を監査し、結果報告では Codex Review を「未実行（codex 未導入）」と明記する
- レビュー対象はデフォルトで `main` ブランチとの差分（`develop` は存在しない）
- `--base` オプションで比較対象を変更可能
- エージェントファイルが存在しない場合は、該当チェックをスキップして残りを実行する

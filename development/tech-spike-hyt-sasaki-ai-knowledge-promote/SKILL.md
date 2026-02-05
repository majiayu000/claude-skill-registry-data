---
name: tech-spike
description: |
  技術検証（Tech Spike）ワークフロー。ライブラリ選定やアーキテクチャ判断の前に最小限の実験コードで技術的妥当性を検証。
  使用タイミング:
  (1) 複数の技術選択肢がある場合（ライブラリA vs B）
  (2) 新しいライブラリ・技術の学習コストが高い場合
  (3) パフォーマンス・互換性の懸念がある場合
  (4) 既存システムとの統合リスクがある場合
  (5) 「技術検証」「ライブラリ調査」「スパイク」リクエスト
  使用しない場合: 技術スタック確定済み、既知のパターン、単純なCRUD操作
allowed-tools: Read, WebSearch, WebFetch, mcp__plugin_context7_context7__resolve-library-id, mcp__plugin_context7_context7__query-docs, Bash(git:*), Bash(mkdir:*)
---

# 技術検証（Tech Spike）

## 目的

設計判断の前に最小限の実験コードで技術的妥当性を検証し、設計精度を向上させます。

## いつ実行するか

以下のいずれかに該当する場合、技術検証を実行します：

- 複数の技術選択肢がある（例: ライブラリA vs B）
- 新しいライブラリ・技術の学習コストが高い
- パフォーマンス・互換性の懸念がある
- 設計判断に実験的検証が必要
- 既存システムとの統合リスクがある

## いつスキップするか

- 技術スタックが確定している
- 既知のパターンで実装可能
- 単純なCRUD操作のみ
- リスクが低く、後戻りコストが小さい

## ワークフロー

→ [workflows/tech-spike.md](workflows/tech-spike.md)

## Context7統合

ライブラリ調査にContext7を使用：

```bash
# Step 1: ライブラリIDを解決
# MCPツール: mcp__plugin_context7_context7__resolve-library-id
#   - libraryName: "Next.js"
#   - query: "Server Componentsのデータフェッチパターン"

# Step 2: ドキュメント検索
# MCPツール: mcp__plugin_context7_context7__query-docs
#   - libraryId: "/vercel/next.js"
#   - query: "Server Components data fetching patterns"
```

## 成果物

- `spike/results.md` - 検証結果と推奨技術
- `spike/experiment-*.py` - 実験コード（オプション）

## テンプレート

- **results.md**: [templates/results-template.md](templates/results-template.md)

## 詳細ガイド

- [技術検証ガイド](references/guide.md)

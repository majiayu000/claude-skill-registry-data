---
name: workflow
description: How to approach work. Applies to all tasks including implementation, planning, investigation, design, review, and auditing.
---

Main Agentは指揮者として計画・委任・判断・統合を行い、手作業は全てSub Agentに委任する。

## 指揮者パターン

| する | しない |
|------|--------|
| 計画・委任・判断・統合 | ファイル探索・コード記述・テスト実行 |
| ToDo完了毎に記録 | 複数ToDoの同時作業 |
| 独立タスクの並列Sub Agent起動 | Sub Agentが持つべきコンテキストの保持 |

委任判断: 自明な修正（typo、3行以内）→自分。調査・複数ファイル変更→委任。迷ったら委任する。

## Sub Agent種別

| 用途 | Agent Type |
|------|-----------|
| 検索・探索 | Explore |
| 設計比較 | Plan |
| 実装・テスト・検証 | general-purpose |

## ルール

1. 手作業は全てSub Agentに委任する
2. 思考を `tmp/<task>/`（plan.md, progress.md, analysis.md）に外化する
3. 1つ完了→記録→次。Sub Agentの並列は可
4. Done Criteriaを先に定義する
5. 技術判断は自分で決定、方針判断は選択肢を提示する
6. 構造変更は `/refactoring` を先に読む

## tmp/ 構造

```
tmp/<task>/
├── plan.md        # Goal, Done Criteria, Team, Approach, Scope
├── progress.md    # What/Why, How, Result を完了毎に追記
├── analysis.md    # Mermaid図で依存関係を可視化
└── investigation/ # Sub Agent結果
```

## Sub Agent起動テンプレート

プロンプトに Goal・Input・Expected output・Output path の4要素を必ず含める。

委任詳細は `delegation-protocol.md` を参照。

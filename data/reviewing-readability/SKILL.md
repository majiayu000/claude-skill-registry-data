---
name: reviewing-readability
description: >
  Code readability review based on "The Art of Readable Code" and Miller's Law (7±2).
  Triggers: 可読性, 理解しやすい, わかりやすい, 明確, 命名, 変数名, 関数名,
  ネスト, 深いネスト, 関数設計, コメント, 複雑, 難しい, 難読,
  Miller's Law, ミラーの法則, 認知負荷, AI-generated, 過剰設計.
allowed-tools: [Read, Grep, Glob, Task]
agent: code-quality-reviewer
user-invocable: false
---

# 可読性レビュー

## 検出

| ID  | パターン                       | 修正                       |
| --- | ------------------------------ | -------------------------- |
| RD1 | `processData()` (曖昧)         | `validateUserEmail()`      |
| RD1 | 誤解を招く識別子               | 意図を示す名前             |
| RD2 | ネスト > 3レベル               | ガード句、関数抽出         |
| RD2 | 関数 > 30行                    | 分解                       |
| RD3 | コメント: `// increment i`     | 削除（自明）               |
| RD3 | コメント: `// TODO: fix later` | Issue作成または今修正      |
| RD4 | 単一実装のインターフェース     | 2つ目の実装まで削除        |
| RD4 | ステートレスロジック用クラス   | 純粋関数                   |
| RD5 | > 5つの関数パラメータ          | 設定オブジェクトまたは分解 |

## 閾値

| 対象     | 推奨 | 最大 |
| -------- | ---- | ---- |
| 関数行数 | ≤30  | 50   |
| ネスト   | ≤3   | 4    |
| 関数引数 | ≤3   | 5    |

## 参考

| トピック         | ファイル                         |
| ---------------- | -------------------------------- |
| 制御フロー       | `references/control-flow.md`     |
| コメント         | `references/comments-clarity.md` |
| AIアンチパターン | `references/ai-antipatterns.md`  |
| 命名             | `references/naming.md`           |

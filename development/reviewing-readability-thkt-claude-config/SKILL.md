---
name: reviewing-readability
description: >
  "The Art of Readable Code"とミラーの法則（7±2）に基づくコード可読性レビュー。
  トリガー: 可読性, 理解しやすい, わかりやすい, 明確, 命名, 変数名, 関数名,
  ネスト, 深いネスト, 関数設計, コメント, 複雑, 難しい, 難読,
  Miller's Law, ミラーの法則, 認知負荷, AI-generated, 過剰設計.
allowed-tools: Read, Grep, Glob, Task
---

# 可読性レビュー - コードの明確さと認知負荷

目標: 新しいチームメンバーが1分以内にコードを理解できる。

## ミラーの法則の限界（7±2）

| コンテキスト | 理想 | 最大 |
| --- | --- | --- |
| 関数引数 | 3 | 5 |
| クラスメソッド | 5 | 7 |
| 条件分岐 | 3 | 5 |
| 関数長 | 5-10行 | 15行 |
| ネスト深度 | 2 | 3 |

## セクションベースのロード

| セクション | ファイル | フォーカス | トリガー |
| --- | --- | --- | --- |
| 命名 | `references/naming-structure.md` | 具体的な名前、検索性 | 命名, 変数名, 関数名 |
| 制御フロー | `references/control-flow.md` | ネスト、ガード句 | ネスト, Miller's Law |
| コメント | `references/comments-clarity.md` | WhatではなくWhy、意図 | コメント, 意図 |
| AIアンチパターン | `references/ai-antipatterns.md` | 過剰設計の検出 | AI-generated, 過剰設計 |

## クイックチェックリスト

### 命名

- [ ] 抽象より具体（`processData`ではなく`validateUserEmail`）
- [ ] 検索可能で発音可能な名前
- [ ] 名前から意図が明確

### 制御フロー

- [ ] ネスト深度 ≤ 3
- [ ] 早期リターンのためのガード句
- [ ] 複雑な条件は関数に抽出

### コメント

- [ ] 「何を」ではなく「なぜ」を説明
- [ ] 古くなったコメントは更新または削除
- [ ] まずコードを自己文書化

### AIコードの臭い

- [ ] 早すぎる抽象化なし（単一実装のインターフェース）
- [ ] シンプルなタスクに不要なクラスなし
- [ ] 誰も求めていない「将来対応」の柔軟性なし

## 主要原則

| 原則 | 適用 |
| --- | --- |
| 明確さ > 賢さ | シンプルなコードが勝つ |
| 7±2の限界を尊重 | チャンクに分割 |
| Tell, Don't Ask | 直接メソッド呼び出し |

## 参照

- [@~/.claude/skills/applying-code-principles/SKILL.md] - 認知限界の科学
- [@~/.claude/rules/development/READABLE_CODE.md] - 詳細ガイドライン
- [@./references/ai-antipatterns.md](./references/ai-antipatterns.md) - AI過剰設計パターン

---
name: formatting-audits
description: >
  Design document review format with 100-point scoring system for SOW/Spec.
  Triggers: SOW review, Spec review, document scoring, 設計書レビュー, 品質スコア.
allowed-tools: [Read, Grep, Glob]
agent: sow-spec-reviewer
user-invocable: false
---

# SOW/Spec採点 (100点満点)

## 採点

| カテゴリ   | スコア | フォーカス                   |
| ---------- | ------ | ---------------------------- |
| 正確性     | 0-25   | ✓/→/?マーカー、証拠          |
| 完全性     | 0-25   | 全セクション、テスト可能なAC |
| 関連性     | 0-25   | 目標 ↔ ソリューション、YAGNI |
| 実行可能性 | 0-25   | 具体的なステップ、実現可能性 |

## 減点

| 問題                   | 減点 |
| ---------------------- | ---- |
| 信頼度マーカーなし     | -5   |
| 必須セクション欠如     | -10  |
| テストシナリオなしのAC | -5   |
| 曖昧なアクション項目   | -5   |
| YAGNI違反              | -5   |
| AC-FRマップ不整合      | -10  |

## 閾値

| スコア | 判定        | アクション         |
| ------ | ----------- | ------------------ |
| 90-100 | PASS        | 次のフェーズへ進行 |
| 70-89  | CONDITIONAL | 修正後に再レビュー |
| 0-69   | FAIL        | 大幅な修正が必要   |

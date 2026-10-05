---
name: fix-checklist
description: Use when about to fix code, modify implementation, or address errors. MUST read before saying "修正します", "fix", "修正する", "直す", "対処する". Prevents symptom-driven fixes.
allowed-tools: [Read, Glob, Grep]
---

症状駆動の修正を防ぐため、コード変更前に根本原因を特定する。

## 手順

1. **コードを書くな** — まず「なぜこのエラーが起きるか」を問う
2. **設計を読む** — `docs/` やスキーマから意図された動作を理解する
3. **フローを追う** — トリガー → 期待状態 → 乖離点を特定する
4. **根本原因を特定** — エラー箇所と原因箇所は異なることが多い
5. **最小限の修正** — 根本原因に対してのみ変更する

| エラー箇所 | 根本原因の典型 |
|-----------|--------------|
| 実行時バリデーション | スキーマ定義 |
| 型不一致 | インターフェース契約 |
| テスト失敗 | 実装ロジック |

**Bad**: 「X が Y にないので Y に X を追加」→ なぜ X が生成されるか未調査
**Good**: 「なぜ X が生成される？設計上 X は不正 → 生成元を修正」

## 調査出力

複雑な問題は `tmp/investigation/<issue>/` に mermaid図で構造化する（overview.md, trace.md, root-cause.md）。1ファイル500行以内。

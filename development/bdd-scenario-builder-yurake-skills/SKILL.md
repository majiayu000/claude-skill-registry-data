---
name: bdd-scenario-builder
description: Behavior-Driven Development (BDD) で振る舞いを定義・シナリオ化するためのガイド。Given-When-Then と Gherkin で受け入れ条件やエッジケースを整理し、失敗パターンや小さく始める導入ステップを含めて、業務言語で明確なシナリオを書くときに使う。
---

# BDD Scenario Builder

## 使い方（最短手順）
1. 成功条件を会話で揃える（業務用語で具体例を話す）
2. シナリオを 3–5 本書く：ハッピーパス先行、1 本は 3–7 ステップ、宣言的に（UI操作や実装詳細は避ける）
3. 自動化レイヤを決める：まず速い層（サービスやロジック）で回し、必要なものだけ E2E/UI に

## シナリオの質チェック
- 特定の振る舞いのみをテストしているか（スコープ過大にしない）
- 業務言語で「何を」書いているか（手順書・UI操作を書かない）
- 他シナリオへの依存がないか
- ステップは 3–7 で収まっているか

## タグと整理
- 例: `@smoke` 基本確認, `@security` セキュリティ, `@wip` 作業中, `@critical` 重要フロー
- Feature/Rule/Scenario のまとまりごとにタグでフィルタを想定して付ける

## 失敗パターンと対策（要約）
- 細かすぎて手順書化 → 成功条件を先に書き、UI詳細は後回し
- シナリオ過多で陳腐化 → 重要フローに絞り、常に直す少数に維持
- 自動テストが遅すぎる → 速い層でも検証し、E2E は代表ケースのみ

## 小さく始める
1. 重要機能を 1 つ選ぶ
2. シナリオを 5 本以内に絞る（ハッピーパス＋主要エッジ）
3. 自動化できるものだけ実装し、継続運用を優先

## TDD との違い（簡潔に）
- TDD: 設計と実装品質をテストで前進させる
- BDD: 認識合わせを例と会話で前進させる（両立可）

## 追加リソース
- 詳細例: [references/examples.md](references/examples.md)
- 失敗パターン詳細: [references/pitfalls.md](references/pitfalls.md)
- 定義と出典: [references/intro.md](references/intro.md)
- コピペ用テンプレ: [assets/gherkin-template.feature](assets/gherkin-template.feature)

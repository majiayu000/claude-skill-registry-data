---
name: request-response-examples
description: |
  API仕様に整合したリクエスト/レスポンス例とエラーレスポンス例を作成するスキル。
  cURLとSDKサンプルを含め、実行可能で説明的な例示を短時間で整備する。

  Anchors:
  • OpenAPI Specification / 適用: 例示とスキーマ整合 / 目的: 仕様一致
  • RFC 7807 Problem Details / 適用: エラーレスポンス設計 / 目的: 形式統一
  • API Design Patterns (J.J. Geewax) / 適用: 例示設計 / 目的: 利用者理解の促進

  Trigger:
  Use when creating API request/response examples, cURL samples, SDK snippets, and error case documentation aligned with the API specification.
  request response examples, cURL, SDK examples, error responses, OpenAPI
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
---

# request-response-examples

## 概要

API仕様に沿ったリクエスト/レスポンス例を、スコープ定義→例示作成→検証の順で整備するスキル。
利用者がそのまま実行できるサンプルと、失敗時のエラー例を同時に提供する。

---

## ワークフロー

### Phase 1: 例示スコープ定義

**目的**: 例示対象と必要なケースを決める

**アクション**:

1. API仕様、対象ユーザー、制約を整理する
2. `references/example-scope.md` で対象範囲とケースを決定する
3. `references/error-response-standards.md` でエラー形式を確認する
4. 例示スコープシートを作成する

**Task**: `agents/define-example-scope.md` を参照

### Phase 2: 例示作成

**目的**: テンプレートに沿って実行可能な例を作る

**アクション**:

1. `assets/request-response-template.md` で例示を構成する
2. `assets/curl-examples.md` を使ってcURL例を整備する
3. `assets/sdk-example-template.md` でSDK例を整備する
4. `assets/error-catalog.md` でエラー例を整理する
5. 必要に応じて `scripts/generate-curl-examples.mjs` を使う

**Task**: `agents/compose-examples.md` を参照

### Phase 3: 検証と統合

**目的**: 例示の正確性と一貫性を確認する

**アクション**:

1. `scripts/validate-examples.mjs` で必須項目を検証する
2. `references/example-format-guidelines.md` で整合を確認する
3. ドキュメントに統合し、必要な更新を記録する

**Task**: `agents/validate-examples.md` を参照

---

## Task仕様ナビ

| Task                 | 起動タイミング | 入力                         | 出力                     |
| -------------------- | -------------- | ---------------------------- | ------------------------ |
| define-example-scope | Phase 1開始時  | API仕様/対象ユーザー/制約    | 例示スコープシート       |
| compose-examples     | Phase 2開始時  | 例示スコープ/テンプレート    | 例示パッケージ           |
| validate-examples    | Phase 3開始時  | 例示パッケージ/検証結果      | 検証レポート             |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

---

## ベストプラクティス

### すべきこと

| 推奨事項                           | 理由                                     |
| ---------------------------------- | ---------------------------------------- |
| 例示対象を先に絞る                 | 重要なケースに集中できる                 |
| 実行可能なサンプルにする           | 利用者が再現しやすい                     |
| 成功/失敗ケースを同一シナリオで示す | 期待値と境界が理解しやすい               |
| プレースホルダーを明示する         | 実値とテスト値の混同を防ぐ               |
| エラー形式を統一する               | クライアント実装が安定する               |

### 避けるべきこと

| 禁止事項                     | 問題点                               |
| ---------------------------- | ------------------------------------ |
| 仕様と異なる値を使う         | 実装時の誤解を生む                   |
| 例示をコピー不可な形にする   | 使い回しできない                     |
| エラー例を省略する           | 実運用の失敗時に役立たない           |
| 例示間で命名や形式が不一致   | 読者が混乱する                       |
| 機密情報に見える値を使う     | セキュリティ上の誤解を招く           |

---

## リソース参照

### scripts/（決定論的処理）

| スクリプト                          | 機能                             |
| ----------------------------------- | -------------------------------- |
| `scripts/validate-examples.mjs`     | 例示テンプレートの必須項目検証   |
| `scripts/generate-curl-examples.mjs` | OpenAPI仕様からcURL例を生成      |

### references/（詳細知識）

| リソース                       | パス                                                                       | 読込条件             |
| ------------------------------ | -------------------------------------------------------------------------- | -------------------- |
| 例示スコープ設計               | [references/example-scope.md](references/example-scope.md)                 | Phase 1で判断する時  |
| 例示フォーマット指針           | [references/example-format-guidelines.md](references/example-format-guidelines.md) | Phase 3で確認する時  |
| エラーレスポンス標準           | [references/error-response-standards.md](references/error-response-standards.md) | エラー例を作成する時 |
| SDK例作成ガイド                | [references/sdk-examples.md](references/sdk-examples.md)                   | SDK例を作成する時    |

### assets/（テンプレート・素材）

| アセット                             | 用途                         |
| ------------------------------------ | ---------------------------- |
| `assets/request-response-template.md` | リクエスト/レスポンス例テンプレート |
| `assets/curl-examples.md`             | cURL例テンプレート            |
| `assets/sdk-example-template.md`      | SDK例テンプレート             |
| `assets/error-catalog.md`             | エラーカタログテンプレート     |

---

## 変更履歴

| Version | Date       | Changes                                                                 |
| ------- | ---------- | ----------------------------------------------------------------------- |
| 3.0.0   | 2026-01-02 | skill-creator手順に沿って全面改訂。Task/テンプレ/検証フローを再構成。   |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様へ準拠。Anchors/Trigger追加。                           |
| 1.0.0   | 2025-12-24 | 初版作成。                                                               |

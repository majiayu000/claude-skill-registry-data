---
name: nextjs-gherkin-generator
description: |
  Next.js/TypeScriptプロジェクト向けGherkinシナリオ自動生成スキル。
  以下の場合に使用:
  (1) ユーザーストーリーからBDDシナリオ作成時
  (2) PRD/仕様書からテストシナリオ生成時
  (3) APIエンドポイントの振る舞い定義時
  (4) ページ遷移・UIインタラクションのシナリオ化時
---

# Next.js Gherkin Generator

このスキルは、ユーザーストーリーや仕様書からNext.js向けのGherkin形式のBDDシナリオを自動生成します。

## ワークフロー

1. **入力受付**: ユーザーストーリー、PRD、または仕様書を受け取る
2. **コンテキスト分析**: Next.js固有のパターンを考慮
   - App Router のページ遷移
   - Server Components vs Client Components
   - API Routes の振る舞い
   - ミドルウェア処理
   - マルチテナント設計（tenant_id考慮）
3. **シナリオ生成**: Playwright-BDD互換のFeatureファイルを出力
4. **検証**: 生成されたシナリオの網羅性をチェック

## ディレクトリ構造

プロジェクトのBDDテストは以下の構造で配置されます：

```
reserve-app/
├── features/
│   ├── auth/
│   │   ├── login.feature
│   │   └── register.feature
│   ├── booking/
│   │   ├── create-reservation.feature
│   │   ├── booking-concurrency.feature
│   │   └── status-transition.feature
│   ├── admin/
│   │   ├── dashboard.feature
│   │   └── reservation-management.feature
│   ├── security/
│   │   ├── session-management.feature
│   │   └── xss-csrf.feature
│   ├── error-handling/
│   │   └── api-errors.feature
│   └── validation/
│       └── input-validation.feature
└── src/__tests__/e2e/
    ├── *.spec.ts (Playwrightテスト)
    └── pages/ (Page Object Model)
```

## シナリオ命名規約

### Featureレベル
- 1つのFeatureは1つの機能/ページに対応
- ファイル名: `機能名.feature` (例: `login.feature`)
- Feature名: 簡潔で分かりやすい日本語

### Scenarioレベル
- 1つのScenarioは1つの具体的な振る舞いをテスト（単一責任）
- Scenario名: Given-When-Thenが明確に分かる日本語
- タグ: `@smoke`, `@regression`, `@api`, `@ui`, `@security` で分類

## Next.js固有のパターン

### 1. ページ遷移シナリオ

```gherkin
Feature: ダッシュボードナビゲーション

  Background:
    Given ユーザーがログイン済みである

  @ui @smoke
  Scenario: 認証済みユーザーがダッシュボードにアクセスする
    When ユーザーが "/admin/dashboard" にアクセスする
    Then ダッシュボードページが表示される
    And ナビゲーションメニューが表示される
    And 統計情報が表示される
```

### 2. API Routeシナリオ

```gherkin
Feature: 予約API

  @api @smoke
  Scenario: 有効なトークンで予約一覧を取得する
    Given 管理者が認証済みである
    And tenant_idが "demo-booking" である
    When "GET /api/admin/reservations" にリクエストを送信する
    Then ステータスコード 200 が返される
    And レスポンスに予約一覧が含まれる
    And 全ての予約に "demo-booking" のtenant_idが設定されている

  @api @error
  Scenario: 未認証でAPI呼び出しを試みる
    Given ユーザーが未認証である
    When "GET /api/admin/reservations" にリクエストを送信する
    Then ステータスコード 401 が返される
    And エラーメッセージ "Unauthorized" が返される
```

### 3. フォーム送信シナリオ

```gherkin
Feature: 予約登録

  @ui @smoke
  Scenario: 有効なデータで予約を登録する
    Given ユーザーが "/booking" ページにアクセスしている
    When 以下の予約情報を入力する
      | field | value |
      | 名前 | 山田太郎 |
      | メールアドレス | yamada@example.com |
      | 電話番号 | 090-1234-5678 |
      | 予約日時 | 2026-01-15 18:00 |
      | 人数 | 4 |
    And 予約ボタンをクリックする
    Then 予約確認ページが表示される
    And 確認メールが送信される

  @ui @validation
  Scenario: 必須項目が未入力の場合エラーが表示される
    Given ユーザーが "/booking" ページにアクセスしている
    When 予約ボタンをクリックする
    Then バリデーションエラーが表示される
    And "名前を入力してください" というメッセージが表示される
```

### 4. 同時実行・競合シナリオ

```gherkin
Feature: 予約の同時実行制御

  @concurrency @smoke
  Scenario: 同時予約による二重予約を防ぐ
    Given 18:00の枠に空きが1つだけある
    When 2人のユーザーが同時に18:00の予約を試みる
    Then 1人目の予約が成功する
    And 2人目の予約は失敗する
    And 2人目に "この時間帯は満席です" というエラーが表示される
```

### 5. セキュリティシナリオ

```gherkin
Feature: XSS/CSRF保護

  @security
  Scenario: XSS攻撃を防ぐ
    Given ユーザーが予約フォームにアクセスしている
    When 名前フィールドに "<script>alert('XSS')</script>" を入力する
    And 予約を登録する
    Then スクリプトが実行されない
    And サニタライズされたテキストとして保存される

  @security
  Scenario: CSRF攻撃を防ぐ
    Given ユーザーがログイン済みである
    When 外部サイトから予約削除リクエストが送信される
    Then リクエストが拒否される
    And ステータスコード 403 が返される
```

## シナリオ網羅性チェックリスト

シナリオ生成時に以下を必ず含めること：

### 基本パターン
- [ ] **ハッピーパス**（正常系）
- [ ] **エラーパス**（異常系）
- [ ] **境界値ケース**

### Next.js固有
- [ ] **認証・認可パターン**
  - [ ] 未認証ユーザー
  - [ ] 認証済み一般ユーザー
  - [ ] 管理者ユーザー
  - [ ] tenant_id分離の確認
- [ ] **ローディング/エラー状態**
  - [ ] データ取得中
  - [ ] ネットワークエラー
  - [ ] サーバーエラー
- [ ] **バリデーション**
  - [ ] 必須項目チェック
  - [ ] 形式バリデーション
  - [ ] カスタムバリデーション

### ビジネスロジック
- [ ] **ステータス遷移**
  - [ ] 予約: pending → confirmed → completed → cancelled
  - [ ] 許可された遷移
  - [ ] 禁止された遷移
- [ ] **同時実行制御**
  - [ ] 楽観的ロック
  - [ ] 在庫管理（空席数）
- [ ] **データ整合性**
  - [ ] リレーション制約
  - [ ] トランザクション処理

## タグ付け戦略

| タグ | 用途 | 実行頻度 |
|-----|------|---------|
| `@smoke` | 重要な基本機能 | 全PR |
| `@regression` | リグレッションテスト | リリース前 |
| `@api` | API Routes | API変更時 |
| `@ui` | UIインタラクション | UI変更時 |
| `@security` | セキュリティ | セキュリティ監査時 |
| `@concurrency` | 同時実行 | 負荷テスト時 |
| `@slow` | 時間がかかるテスト | 夜間バッチ |

## 使用例

### 入力（ユーザーストーリー）

```
管理者として、予約を承認または拒否できるようにしたい。
予約一覧から予約を選択し、ステータスを変更できる必要がある。
```

### 出力（Gherkinシナリオ）

```gherkin
Feature: 予約ステータス管理

  Background:
    Given 管理者がログイン済みである
    And 以下の予約が存在する
      | id | customer_name | status |
      | 1 | 山田太郎 | pending |
      | 2 | 佐藤花子 | confirmed |

  @ui @smoke
  Scenario: 管理者がpending予約を承認する
    Given 管理者が "/admin/reservations" ページにアクセスしている
    When ID "1" の予約を選択する
    And "承認" ボタンをクリックする
    Then 予約ステータスが "confirmed" に更新される
    And "予約を承認しました" という成功メッセージが表示される
    And 顧客に承認メールが送信される

  @ui @smoke
  Scenario: 管理者がpending予約を拒否する
    Given 管理者が "/admin/reservations" ページにアクセスしている
    When ID "1" の予約を選択する
    And "拒否" ボタンをクリックする
    And 拒否理由 "満席のため" を入力する
    Then 予約ステータスが "cancelled" に更新される
    And "予約を拒否しました" という成功メッセージが表示される
    And 顧客に拒否理由付きメールが送信される

  @ui @validation
  Scenario: 既に承認済みの予約を再度承認できない
    Given 管理者が "/admin/reservations" ページにアクセスしている
    When ID "2" の予約を選択する
    Then "承認" ボタンが非活性である
    And "この予約は既に承認されています" というメッセージが表示される

  @api
  Scenario: APIで予約ステータスを更新する
    Given 管理者が認証済みである
    When "PATCH /api/admin/reservations/1" に以下のボディを送信する
      """json
      {
        "status": "confirmed"
      }
      """
    Then ステータスコード 200 が返される
    And レスポンスに更新された予約情報が含まれる
    And データベースの予約ステータスが "confirmed" になっている
```

## ベストプラクティス

### 1. 宣言的スタイルを推奨

❌ 命令的（避ける）
```gherkin
When ユーザー名フィールドに "test@example.com" を入力する
And パスワードフィールドに "password123" を入力する
And ログインボタンをクリックする
```

✅ 宣言的（推奨）
```gherkin
When ユーザーが有効な認証情報でログインする
```

### 2. シナリオの独立性を保つ

各シナリオは他のシナリオに依存せず、単独で実行可能であること。

### 3. Backgroundを活用

複数シナリオで共通の前提条件は `Background` に抽出する。

### 4. データテーブルを活用

複数の類似ケースは `Scenario Outline` とデータテーブルで表現する。

```gherkin
  @validation
  Scenario Outline: バリデーションエラーが表示される
    Given ユーザーが予約フォームにアクセスしている
    When <field> に <value> を入力する
    And 予約ボタンをクリックする
    Then "<error_message>" というエラーが表示される

    Examples:
      | field | value | error_message |
      | メールアドレス | invalid-email | 正しいメールアドレスを入力してください |
      | 電話番号 | abc-defg-hijk | 正しい電話番号を入力してください |
      | 人数 | 0 | 1人以上を選択してください |
```

## リファレンス

詳細なパターンとテンプレートは以下を参照：

- [scenario-patterns.md](references/scenario-patterns.md) - シナリオパターン集
- [step-definition-templates.md](references/step-definition-templates.md) - ステップ定義テンプレート
- [page-object-patterns.md](references/page-object-patterns.md) - Page Object Modelパターン

## 実行方法

### Skillの呼び出し

```bash
# ユーザーストーリーからGherkin生成
「予約キャンセル機能のGherkinシナリオを生成して」

# 既存のFeatureファイルのレビュー
「features/booking/create-reservation.feature のシナリオをレビューして」
```

### 生成されたFeatureファイルの配置

1. `reserve-app/features/<category>/<feature-name>.feature` に保存
2. 対応するPlaywrightテストを `reserve-app/src/__tests__/e2e/` に作成
3. Page Objectを `reserve-app/src/__tests__/e2e/pages/` に作成

## 補足

このスキルは、プロジェクトの以下のドキュメントを参照して最適化されています：

- `CLAUDE.md` - プロジェクト概要
- `.cursor/rules/開発プロセスルール.md` - BDD開発プロセス
- `documents/basic/機能一覧とページ設計.md` - 機能仕様
- `documents/api/API設計書.md` - API仕様

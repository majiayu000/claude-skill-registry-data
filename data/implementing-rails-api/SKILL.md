---
name: implementing-rails-api
description: JSONで定義されたAPI仕様を元にRuby on RailsでAPIと管理画面を実装するスキル。全体のオーケストレーションを行い、各ステップの詳細ガイドラインに従って実装を進めます。
---

## 概要

このスキルは、JSONで定義されたAPI仕様に基づいて、Ruby on Rails + PostgreSQLでAPIと管理画面を実装します。

## このスキルを使用するタイミング

Claudeは以下の状況でこのスキルを使用します：

- ユーザーがJSON形式のAPI仕様を提供し、Rails APIの実装を依頼した場合
- microCMSなどのHeadless CMSの仕様からRails APIを生成する場合
- 既存のJSON仕様ファイル（app.jsonなど）を参照してAPI実装を依頼された場合
- 「APIを実装して」「管理画面を作成して」といったリクエストでJSON仕様が存在する場合

## 技術スタック

| 項目 | 技術 |
|------|------|
| 言語 | Ruby 3.4 |
| フレームワーク | Ruby on Rails 8.1 |
| データベース | PostgreSQL 18 |
| ORM | Active Record |

## ステップ

各ステップの詳細は `steps/` ディレクトリ内のファイルを参照してください。

### 1. アプリケーション仕様を確認する
詳細: @steps/01_check_specification.md

Claudeは、JSON仕様ファイルを読み込み、モデル構造・フィールド定義・リレーションを把握します。
仕様形式: @references/01_json_specification.md

### 2. 技術スタックを決定する
詳細: @steps/02_select_tech_stack.md

Claudeは、環境確認と管理画面の方式（ActiveAdmin / Administrate / Hotwire）を決定します。

### 3. ユースケースを洗い出す
詳細: @steps/03_define_usecases.md

Claudeは、JSON仕様のアクター・ユースケースを確認し、各モデルのCRUD操作、ページネーション、フィルタリング、ソート、リレーション取得方法を定義します。

### 4. OpenAPI定義を作成する
詳細: @steps/04_define_openapi.md

Claudeは、ユースケースとモデル定義に基づいて、APIの仕様をOpenAPI 3.1形式で定義します。

### 5. DBスキーマを設計する
詳細: @steps/05_design_db_schema.md

Claudeは、JSON仕様の型をPostgreSQLの型にマッピングし、テーブル設計を行います。

### 6. SQLとインデックスを定義する
詳細: @steps/06_define_sql_and_indexes.md

Claudeは、ユースケースで実行されるSQLを洗い出し、通常インデックスと全文検索インデックス（GIN + tsvector）を定義します。

### 7. プロジェクトを初期化する
詳細: @steps/07_initialize_project.md

Claudeは、Rails 8.1プロジェクトを作成し、必要なGemと設定をセットアップします。

### 8. DBマイグレーションを実装する
詳細: @steps/08_implement_migration.md

Claudeは、設計に基づいてマイグレーションファイルを作成・実行します。

### 9. ORマッピングを実装する
詳細: @steps/09_implement_orm.md

Claudeは、Active Recordモデルにリレーション、スコープ、クエリメソッドを実装します。

### 10. バリデーションを実装する
詳細: @steps/10_implement_validation.md

Claudeは、JSON仕様のvalidation設定に基づいてActive Recordバリデーションを実装します。

### 11. APIエンドポイントを実装する
詳細: @steps/11_implement_api_endpoints.md

Claudeは、RESTful APIエンドポイント（CRUD、ページネーション、フィルタリング、ソート）を実装します。

### 12. APIの動作確認を行う
詳細: @steps/12_verify_api.md

Claudeは、curlとRSpecでAPIの動作を検証し、N+1問題がないことを確認します。

### 13. 管理画面を実装する

Claudeは、選択した方式で管理画面を実装します。方式に応じて以下のファイルを参照してください：

- ActiveAdmin: @steps/13a_admin_activeadmin.md
- Administrate: @steps/13b_admin_administrate.md
- Hotwire: @steps/13c_admin_hotwire.md
- 共通設定・トラブルシューティング: @steps/13d_admin_common.md

### 14. API Playgroundを実装する（オプション）
詳細: @steps/14_implement_api_playground.md

Claudeは、OpenAPI定義を活用してSwagger UIまたはカスタムPlaygroundを実装し、APIを対話的にテストできる環境を構築します。

## ファイル構成

```
implementing-rails-api/
├── SKILL.md                 # このファイル
├── references/
│   └── 01_json_specification.md  # JSON仕様の定義
└── steps/
    ├── 01_check_specification.md
    ├── 02_select_tech_stack.md
    ├── 03_define_usecases.md
    ├── 04_define_openapi.md
    ├── 05_design_db_schema.md
    ├── 06_define_sql_and_indexes.md
    ├── 07_initialize_project.md
    ├── 08_implement_migration.md
    ├── 09_implement_orm.md
    ├── 10_implement_validation.md
    ├── 11_implement_api_endpoints.md
    ├── 12_verify_api.md
    ├── 13a_admin_activeadmin.md
    ├── 13b_admin_administrate.md
    ├── 13c_admin_hotwire.md
    ├── 13d_admin_common.md
    └── 14_implement_api_playground.md
```

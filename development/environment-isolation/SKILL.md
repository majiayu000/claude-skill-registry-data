---
name: environment-isolation
description: |
  環境分離とアクセス制御スキル。開発・ステージング・本番環境の厳格な分離、
  環境間Secret共有の防止、最小権限原則の徹底を提供します。

  Anchors:
  • Building Secure and Reliable Systems / 適用: Defense in Depth原則 / 目的: 多層防御設計
  • The Twelve-Factor App / 適用: Config要素とコードの分離 / 目的: 環境変数による設定管理
  • Railway Secret Management / 適用: 環境グループによるSecret分離 / 目的: 環境別Secretストア

  Trigger:
  Use when designing environment isolation strategy, managing secrets across dev/staging/prod environments,
  implementing access control policies, preventing cross-environment data contamination,
  or validating environment separation compliance.
  environment isolation, secret management, access control, Railway secrets, GitHub secrets, security boundaries
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Environment Isolation & Access Control

## 概要

開発、ステージング、本番環境の厳格な分離は、セキュリティとデータ整合性の基盤です。
このスキルは、環境間のSecret共有を防ぎ、各環境に適した管理方式とアクセス制御を確立します。

## ワークフロー

環境分離の実装は以下の3つのフェーズで構成されます。各フェーズはTaskとして分離され、
重い思考・探索をメインコンテキストに持ち込まずに完了します。

### Phase 1: 環境分離戦略設計

**目的**: プロジェクト要件に応じた最適な分離レベルと方針を決定する

**実行方法**:

```
Task: agents/design-strategy.md を起動
入力: プロジェクト要件定義、技術スタック
出力: 環境分離戦略ドキュメント、リスク評価マトリクス
```

**判断基準**:

- データの機密性がHIGH以上 → 物理的分離（レベル1）必須
- コンプライアンス要件あり → 監査ログ・MFA必須
- 小規模プロジェクト → 論理的分離（レベル2）から開始可

**参照リソース**:

- `references/environment-patterns.md`: 環境分離パターンとSecret管理の詳細
- `references/environment-validation.md`: 検証項目チェックリスト

### Phase 2: Secret管理設定

**目的**: 環境別Secret管理を実装し、CI/CD統合を完了する

**実行方法**:

```
Task: agents/configure-secrets.md を起動
入力: 環境分離戦略ドキュメント、アプリケーションSecret一覧
出力: Secret設定ガイド、.env.exampleテンプレート
```

**判断基準**:

- Development環境 → .env.local（Gitignore）
- Staging環境 → Railway Secrets + GitHub Secrets（STAGING\_プレフィックス）
- Production環境 → Railway Secrets + GitHub Secrets（PROD\_プレフィックス、承認制）

**参照リソース**:

- `references/environment-patterns.md`: Railway/GitHub Secrets設定手順
- `scripts/validate-environment.mjs`: 起動時環境変数検証スクリプト
- `assets/secret-configuration-guide.md`: 詳細設定ガイドテンプレート

### Phase 3: 環境分離検証

**目的**: 実装された分離が機能することを検証し、脆弱性を発見する

**実行方法**:

```
Task: agents/validate-isolation.md を起動
入力: 環境分離戦略ドキュメント、Secret設定ガイド
出力: 環境分離検証レポート、継続的検証スクリプト
```

**判断基準**:

- 自動検証可能な項目 → scripts/validate-environment.mjs 実行
- ネットワーク分離 → 手動接続テスト（非破壊）
- アクセス制御 → IAMポリシー/Railway権限確認

**参照リソース**:

- `references/environment-validation.md`: 検証項目チェックリスト
- `scripts/validate-environment.mjs`: 自動検証スクリプト
- `assets/validation-report-template.md`: 検証レポートテンプレート

## Task仕様（ナビゲーション）

### Task 1: design-strategy (環境分離戦略設計)

- **ファイル**: `agents/design-strategy.md`
- **役割**: Werner Vogels思考様式（大規模分散システム設計）
- **いつ呼ぶか**: プロジェクト初期、環境構成見直し時
- **入力**: プロジェクト要件定義、技術スタック
- **出力**: 環境分離戦略ドキュメント、リスク評価マトリクス
- **制約**: すべてのプロジェクトでレベル3（データ分離）・レベル4（アクセス分離）必須

### Task 2: configure-secrets (Secret管理設定)

- **ファイル**: `agents/configure-secrets.md`
- **役割**: Kelsey Hightower思考様式（Cloud Native Secret管理）
- **いつ呼ぶか**: 環境分離戦略確定後、CI/CD構築時
- **入力**: 環境分離戦略ドキュメント、アプリケーションSecret一覧
- **出力**: Secret設定ガイド、.env.exampleテンプレート
- **制約**: 本番SecretはRailway/GitHub Secretsのみ（.env.local禁止）

### Task 3: validate-isolation (環境分離検証)

- **ファイル**: `agents/validate-isolation.md`
- **役割**: Bruce Schneier思考様式（攻撃者視点のセキュリティ評価）
- **いつ呼ぶか**: Secret設定完了後、定期監査時
- **入力**: 環境分離戦略ドキュメント、Secret設定ガイド
- **出力**: 環境分離検証レポート、継続的検証スクリプト
- **制約**: 本番環境への検証は承認後のみ（破壊的テスト禁止）

## ベストプラクティス

### すべきこと

- **4つの分離レベルを評価する**: 物理的・論理的・データ・アクセスのうち必要なレベルを選定
- **環境別Secret管理を徹底する**: 本番Secretが開発環境から物理的にアクセス不可能にする
- **.env.exampleをテンプレートとして管理**: 実際の値を含まず、必須キーと説明のみ記載
- **起動時検証を実装する**: scripts/validate-environment.mjsで必須環境変数の存在を確認
- **Secretローテーション計画を策定する**: 環境別に適切な頻度（開発:不定期、ステージング:90日、本番:30-90日）
- **CI/CD統合を自動化する**: GitHub Actions/RailwayでSecret注入を自動化

### 避けるべきこと

- **本番Secretを.env.localで管理しない**: 必ずRailway Secrets/GitHub Secretsを使用
- **Secretをコミット履歴に含めない**: .gitignore設定とpre-commit hookで防止
- **すべての環境で同一データベースを共有しない**: 環境別に物理的に分離されたインスタンスを使用
- **開発者に本番環境への無制限アクセスを許可しない**: MFA・承認フローを必須化
- **検証を一度だけ実施しない**: CI/CDパイプラインに継続的検証を組み込む

## リソース参照

### 知識ベース（references/）

| リソース                    | 用途                             |
| --------------------------- | -------------------------------- |
| `environment-patterns.md`   | 環境分離パターンとSecret管理詳細 |
| `environment-validation.md` | 検証項目チェックリスト           |

### スクリプト（scripts/）

#### validate-environment.mjs

**目的**: 環境変数の存在と形式を検証する

**引数**:

- `--check-all`: すべての検証項目を実行
- `--check-isolation`: Secret分離のみ検証
- `--check-required`: 必須環境変数のみ検証
- `--check-gitignore`: .gitignore設定を検証

**期待出力**:

- 成功: 終了コード0、検証結果サマリー
- 失敗: 終了コード1、エラー詳細

**失敗時の扱い**: アプリケーション起動を中断し、不足している環境変数を通知

#### log_usage.mjs

**目的**: スキル使用履歴を記録し、EVALS.jsonを更新する

**引数**:

- `--result`: `success` または `failure`（必須）
- `--phase`: 実行したフェーズ名（任意）
- `--agent`: 実行したエージェント名（任意）
- `--notes`: 追加のフィードバックメモ（任意）

**使用例**:

```bash
node scripts/log_usage.mjs --result success --phase "Phase 2" --agent "configure-secrets"
```

### テンプレート（assets/）

#### environment-strategy-template.md

**用途**: 環境分離戦略ドキュメントの雛形

**主要セクション**: 要件分析、分離レベル選定、環境構成、Secret管理方針、アクセス制御マトリクス、検証基準

#### secret-configuration-guide.md

**用途**: Secret設定手順の包括的ガイド

**主要セクション**: Secret一覧、環境別配置手順、.env.example、CI/CD統合、ローテーション計画

#### validation-report-template.md

**用途**: 環境分離検証結果のレポート

**主要セクション**: 自動検証結果、手動検証結果、セキュリティシナリオ検証、改善推奨事項

## フィードバックループ

### 使用記録の方法

各フェーズ完了後、以下を実行してください:

```bash
node scripts/log_usage.mjs --result {{success|failure}} --phase "{{Phase名}}" --agent "{{Task名}}"
```

### レベルアップ基準

| レベル | 使用回数 | 成功率 | 説明                                           |
| ------ | -------- | ------ | ---------------------------------------------- |
| 1      | 0+       | -      | 基本的な環境分離戦略の設計と実装               |
| 2      | 5+       | 70%+   | Secret管理の自動化とCI/CD統合                  |
| 3      | 15+      | 80%+   | 高度なネットワーク分離とコンプライアンス対応   |
| 4      | 30+      | 90%+   | マルチクラウド・マルチアカウント環境の統合管理 |

### メトリクス確認

```bash
# EVALS.jsonを確認
cat EVALS.json | jq '.metrics'

# LOGS.mdを確認
tail -n 20 LOGS.md
```

## トラブルシューティング

### よくある問題

#### 問題1: 環境変数が読み込まれない

**症状**: アプリケーション起動時に環境変数が undefined

**原因**: .env.local が存在しない、または読み込み設定が不足

**解決策**:

```bash
# .env.localの存在確認
ls -la .env.local

# 起動コマンドに環境変数ローダーを追加
node -r dotenv/config app.js
```

#### 問題2: GitHub Actionsで本番Secretが参照できない

**症状**: デプロイ時にSecret参照エラー

**原因**: Environment設定が不足、またはSecret名のプレフィックスミス

**解決策**:

```yaml
# .github/workflows/deploy.yml
jobs:
  deploy-production:
    environment: production # 必須
    env:
      DATABASE_URL: ${{ secrets.PROD_DATABASE_URL }} # プレフィックス確認
```

#### 問題3: validate-environment.mjsがパスしない

**症状**: 必須環境変数チェックで失敗

**原因**: .env.exampleと実際の環境変数の不一致

**解決策**:

```bash
# .env.exampleの内容を確認
cat .env.example

# 不足している環境変数を.env.localに追加
echo "MISSING_VAR=value" >> .env.local

# 再検証
node scripts/validate-environment.mjs --check-required
```

## セキュリティチェックリスト

実装前に以下を確認してください:

- [ ] 本番環境のSecretが開発環境から物理的にアクセス不可能である
- [ ] .env.local、.env.\*.local が .gitignore に含まれている
- [ ] .env.example に実際のSecretが含まれていない
- [ ] 本番データベースが開発環境から接続不可能である
- [ ] 本番環境の管理コンソールにMFAが必須である
- [ ] GitHub/Railway Secretsに適切なアクセス権限が設定されている
- [ ] Secret漏洩検知（GitHub Secret scanning）が有効である
- [ ] Secretローテーション計画が策定されている
- [ ] 起動時にscripts/validate-environment.mjsが実行されている
- [ ] CI/CDパイプラインに継続的検証が組み込まれている

## 変更履歴

| Version | Date       | Changes                                   |
| ------- | ---------- | ----------------------------------------- |
| 2.0.0   | 2026-01-01 | 18-skills.md仕様完全準拠、Level1-4削除    |
| 1.0.0   | 2025-12-31 | 18-skills.md仕様準拠への移行、agents/追加 |

## 関連スキル

このスキルは以下のスキルと組み合わせて使用できます:

- **ci-cd-pipelines**: 環境別デプロイパイプラインの構築
- **infrastructure-as-code**: 環境構成のコード化と再現性確保
- **security-configuration-review**: セキュリティ設定の包括的レビュー

---

**次のステップ**: Phase 1から開始し、`agents/design-strategy.md` を起動してください。

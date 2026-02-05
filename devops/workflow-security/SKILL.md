---
name: workflow-security
description: |
  GitHub Actionsワークフローセキュリティの専門スキル。
  権限最小化、シークレット保護、サプライチェーン攻撃対策を提供します。

  Anchors:
  - GitHub Actions Security Hardening（GitHub公式）/ 適用: ワークフロー権限・シークレット保護 / 目的: 安全な自動化
  - OWASP CI/CD Security（OWASP）/ 適用: サプライチェーン対策 / 目的: 脆弱性防止
  - Principle of Least Privilege / 適用: 権限設計全般 / 目的: 攻撃面最小化

  Trigger:
  ワークフロー権限監査時、シークレット漏洩対策時、サプライチェーン攻撃対策時、PRワークフロー設計時に使用

allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# GitHub Actions Workflow Security

## 概要

GitHub Actions ワークフローのセキュリティ強化スキル。4つの専門エージェントによる包括的なセキュリティ対策を提供します。

## エージェント構成

| エージェント           | 役割                       | 主な機能                                        |
| ---------------------- | -------------------------- | ----------------------------------------------- |
| permission-auditor     | 権限監査・最小権限設計     | GITHUB_TOKEN監査、ジョブ/ステップ権限分離       |
| secret-protector       | シークレット保護           | 露出防止、安全な参照パターン、マスキング        |
| supply-chain-guard     | サプライチェーン攻撃対策   | SHA固定化、Verified Creator確認、依存関係監査   |
| pr-workflow-specialist | PRワークフローセキュリティ | pull_request_target対策、ラベルゲート、Fork対策 |

## ワークフロー

### Phase 1: セキュリティ評価

**目的**: 現状のワークフローセキュリティを評価

**アクション**:

1. `permission-auditor` で権限設定を監査
2. `secret-protector` でシークレット露出リスクを確認
3. `supply-chain-guard` でサードパーティアクションを検証

### Phase 2: セキュリティ強化

**目的**: 特定されたリスクへの対策実施

**アクション**:

1. 権限の最小化（ジョブ/ステップレベル）
2. シークレット参照パターンの安全化
3. アクションのSHA固定化
4. PRワークフローのセキュリティ設計

### Phase 3: 検証と継続監視

**目的**: 対策の有効性確認と継続的監視

**アクション**:

1. `scripts/validate-skill.mjs` でスキル構造検証
2. セキュリティチェックリストによる確認
3. `scripts/log_usage.mjs` で実行記録

## Task仕様ナビ

| タスク                  | 説明                        | 担当エージェント       | 参照リソース               |
| ----------------------- | --------------------------- | ---------------------- | -------------------------- |
| GITHUB_TOKEN権限監査    | トークン権限の最小化        | permission-auditor     | `permission-hardening.md`  |
| シークレット保護        | 露出防止とマスキング        | secret-protector       | `permission-hardening.md`  |
| アクション固定化        | SHA pinningによる不変性確保 | supply-chain-guard     | `supply-chain-security.md` |
| Verified Creator確認    | 信頼できるアクション選定    | supply-chain-guard     | `supply-chain-security.md` |
| pull_request_target対策 | Fork PRからの攻撃防止       | pr-workflow-specialist | `supply-chain-security.md` |
| ラベルゲート実装        | 信頼されたPRのみ実行        | pr-workflow-specialist | `supply-chain-security.md` |

## ベストプラクティス

### すべきこと

- ワークフロー作成時に `permission-auditor` で権限を最小化する
- サードパーティアクション追加時に `supply-chain-guard` で検証する
- PRワークフロー設計時に `pr-workflow-specialist` でセキュリティ確認する
- シークレット使用箇所で `secret-protector` のパターンに従う
- 定期的にワークフロー全体のセキュリティ監査を実施する

### 避けるべきこと

- `permissions: write-all` のような過剰な権限付与
- タグ参照（`@v4`）のみでのアクション使用（SHA固定なし）
- `pull_request_target` でのFork PRコード直接チェックアウト
- シークレットの環境変数への無条件展開
- 未検証サードパーティアクションの本番使用

## リソース参照

### エージェント

| エージェント                       | 説明                       |
| ---------------------------------- | -------------------------- |
| `agents/permission-auditor.md`     | 権限監査の詳細仕様         |
| `agents/secret-protector.md`       | シークレット保護の詳細     |
| `agents/supply-chain-guard.md`     | サプライチェーン対策       |
| `agents/pr-workflow-specialist.md` | PRワークフローセキュリティ |

### リファレンス

| リソース                              | 説明                         |
| ------------------------------------- | ---------------------------- |
| `references/permission-hardening.md`  | 権限強化の詳細ガイド         |
| `references/supply-chain-security.md` | サプライチェーンセキュリティ |

### スクリプト

| スクリプト                   | 説明           | 使用方法                             |
| ---------------------------- | -------------- | ------------------------------------ |
| `scripts/validate-skill.mjs` | スキル構造検証 | `node scripts/validate-skill.mjs -v` |
| `scripts/log_usage.mjs`      | 使用記録       | `node scripts/log_usage.mjs`         |

### アセット

| アセット                      | 説明                       |
| ----------------------------- | -------------------------- |
| `assets/secure-workflow.yaml` | セキュアワークフロー実装例 |

## 変更履歴

| バージョン | 日付       | 変更内容                                      |
| ---------- | ---------- | --------------------------------------------- |
| 2.0.0      | 2026-01-01 | 4エージェント体制への再構成、18-skills.md準拠 |
| 1.1.0      | 2025-12-31 | Task仕様ナビテーブル追加、日本語記述統一      |
| 1.0.0      | 2025-12-24 | 初版リリース                                  |

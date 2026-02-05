---
name: deployment-agent
description: |
  DeploymentAgent スキル - CI/CDデプロイ自動化・Firebase自動デプロイ・ヘルスチェック・自動Rollback。
  ビルド・テスト・デプロイを完全自動化し、Staging/Production環境へのFirebaseデプロイを実行。

  Use when:
  - アプリケーションをデプロイする時
  - Firebase Hosting/Functionsにデプロイする時
  - ヘルスチェックが必要な時
  - Rollbackが必要な時
  - "デプロイ", "deploy", "release", "staging", "production" がキーワードに含まれる時
allowed-tools: Read, Grep, Glob, Bash
---

# Deployment Agent Skill

CI/CDデプロイ自動化Agent - Firebase自動デプロイ・ヘルスチェック・自動Rollback。

## 役割

- ビルド実行・検証 (`npm run build`)
- テスト実行・検証 (`npm test`)
- Firebase Hosting/Functions デプロイ
- デプロイ後ヘルスチェック (5回リトライ)
- 失敗時自動Rollback
- デプロイメトリクス収集
- 本番デプロイ時のCTO承認要求

## 実行権限

- **Staging**: 即座デプロイ可能
- **Production**: CTO承認後のみ実行

## デプロイターゲット

```yaml
environments:
  staging:
    firebase_project: "my-app-staging"
    url: "https://staging.my-app.com"
    auto_deploy: true
    approval_required: false
    health_check_retries: 5

  production:
    firebase_project: "my-app-prod"
    url: "https://my-app.com"
    auto_deploy: false
    approval_required: true
    approval_target: "CTO"
    health_check_retries: 10
```

## ヘルスチェック仕様

```yaml
health_check:
  url: "{environment_url}/health"
  method: "GET"
  expected_status: 200
  timeout: 30s
  retries: 5 (staging) / 10 (production)
  retry_delay: 10s
  failure_action: "auto_rollback"
```

## 実行フロー

1. **環境判定**: Staging/Production判定
2. **事前検証**: Git状態・Firebase CLI確認
3. **ビルド実行**: `npm run build` (タイムアウト: 2分)
4. **テスト実行**: `npm test` (タイムアウト: 3分)
5. **Firebase Deploy**: (タイムアウト: 10分)
6. **ヘルスチェック**: 5-10回リトライ
7. **Rollback判定**: 失敗時は自動Rollback

## デプロイコマンド

```bash
# Stagingデプロイ
npm run deploy:staging

# Productionデプロイ (CTO承認後)
npm run deploy:production

# DeploymentAgent経由
npm run agents:deploy -- --environment staging
npm run agents:deploy -- --environment production
```

## Rollback戦略

```yaml
rollback:
  trigger:
    - health_check_failure
    - deployment_error
    - manual_request

  process:
    1: "git checkout {previous_version}"
    2: "npm run build"
    3: "firebase deploy --project {project_id}"
    4: "health_check"
```

## 事前検証項目

```yaml
pre_deployment_validation:
  1_git_status: "作業ディレクトリがクリーンか"
  2_branch_check: "Production: mainブランチ必須"
  3_firebase_cli: "Firebase CLI インストール確認"
  4_firebase_project: "プロジェクトアクセス確認"
```

## 成功条件

### 必須条件
- ビルド成功: 100%
- テスト成功: 100%
- ヘルスチェック: HTTP 200
- デプロイ完了時間: ≤10分

### 品質条件
- デプロイ成功率: 95%以上
- Rollback成功率: 100%
- ヘルスチェック成功率: 98%以上

## エスカレーション条件

### Sev.1-Critical → CTO
- 本番デプロイ失敗
- Rollback失敗
- データ損失リスク

### Sev.2-High → TechLead
- ビルド失敗 (10件以上エラー)
- E2Eテスト失敗率10%超
- Staging環境デプロイ失敗

## デプロイメトリクス

```yaml
deployment_metrics:
  version: "v1.2.3"
  environment: "production"
  duration_ms: 330000
  build_duration_ms: 45000
  test_duration_ms: 90000
  deploy_duration_ms: 180000
  health_check_attempts: 3
  status: "success"
```

## 通知フォーマット

```markdown
Deployment Complete

**Environment**: production
**Version**: v1.2.3
**URL**: https://my-app.com
**Duration**: 5m 30s
**Status**: success

Health Check: 3 attempts, passed
Rollback: Not required
```

## メトリクス

- **平均デプロイ時間**: 5-8分
- **ビルド時間**: 30-60秒
- **テスト時間**: 1-3分
- **Firebase Deploy時間**: 2-5分
- **デプロイ成功率**: 95%+
- **Rollback成功率**: 100%

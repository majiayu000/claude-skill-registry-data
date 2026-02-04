---
name: setting-up-devops
description: CI/CDパイプライン構築とデプロイ自動化を支援します。Infrastructure as Code、監視システム設計、デプロイメント戦略を提供します。DevOps基盤構築、運用自動化が必要な場合に使用してください。
---

# DevOps・SRE インフラ構築

## 概要

CI/CDパイプライン構築、デプロイ自動化、監視システム実装、インフラ管理を包括的に支援するスキルです。

## 実行フロー

### Step 1: CI/CDパイプラインの設計

#### パイプライン構造

```
Code → Build → Test → Deploy → Monitor

1. コードプッシュ（Git）
2. 自動ビルド
3. 自動テスト（Unit/Integration/E2E）
4. セキュリティスキャン
5. ステージング環境へデプロイ
6. 本番環境へデプロイ（承認後）
7. モニタリングとアラート
```

#### ベストプラクティス

- Fast feedback loops（< 10分のビルド）
- 並列テスト実行
- キャッシュ最適化
- 環境間プロモーション

### Step 2: デプロイ戦略の選定

| パターン | 特徴 | ユースケース |
| -------- | ---- | ------------ |
| Blue-Green | ダウンタイムゼロ、即座にロールバック | 重要なサービス |
| Canary | 段階的ロールアウト、リスク最小化 | 大規模サービス |
| Rolling | 順次更新、可用性維持 | 一般的なサービス |
| Feature Flag | 機能リリースを分離 | 実験的機能 |

### Step 3: 監視とObservability

#### Four Golden Signals

- **Latency**: p50, p95, p99（目標: API < 100ms）
- **Traffic**: 毎秒リクエスト数
- **Errors**: エラー率（目標: < 0.1%）
- **Saturation**: CPU/メモリ使用率

#### 監視設計

- メトリクス収集（アプリ/インフラ/ビジネス）
- 構造化ログ（JSON）
- 分散トレーシング

### Step 4: Infrastructure as Code

#### Terraform例

```hcl
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = "t3.medium"
  tags = { Environment = var.environment }
}
```

#### ベストプラクティス

- モジュール化と再利用
- リモートステート管理
- 環境別変数管理
- シークレット管理

### Step 5: コンテナ・オーケストレーション

#### Docker最適化

- マルチステージビルド
- 軽量ベースイメージ（alpine）
- レイヤーキャッシュ活用

#### Kubernetes

- Deployment、Service、Ingress
- HorizontalPodAutoscaler
- Liveness/Readiness Probe

### Step 6: セキュリティ自動化

- SAST（静的解析）
- DAST（動的解析）
- コンテナイメージスキャン
- シークレット管理（Vault、Secrets Manager）

## 出力成果物

1. **CI/CDパイプライン定義**: YAML設定ファイル
2. **デプロイ戦略文書**: フローとロールバック手順
3. **監視設定**: ダッシュボード、アラート定義
4. **IaCコード**: Terraform/CloudFormation
5. **コスト試算**: 月額見積もり

## ベストプラクティス

1. **自動化ファースト**: 繰り返しタスクは自動化
2. **セキュリティの組み込み**: CI/CDにセキュリティチェック
3. **可観測性の確保**: メトリクス・ログ・トレース
4. **障害への備え**: ロールバック手順、インシデント対応計画
5. **コスト意識**: リソース利用を監視

## 関連ファイル

- [TEMPLATES.md](./TEMPLATES.md) - パイプラインテンプレート
- [CHECKLIST.md](./CHECKLIST.md) - デプロイチェックリスト

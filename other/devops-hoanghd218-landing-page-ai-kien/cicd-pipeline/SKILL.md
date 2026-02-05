---
name: cicd-pipeline
description: CI/CDパイプラインの設計・実装・トラブルシューティング。GitHub Actions、GitLab CI、CircleCI、Jenkinsの設定ファイル作成、ビルド最適化、デプロイ戦略（Blue-Green、Canary、Rolling）の実装。「パイプライン」「CI/CD」「デプロイ」「ビルド」「自動化」に関する質問で使用。
---

# CI/CD パイプライン設計・実装

## クイックスタート

### GitHub Actions（推奨）

```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build-test-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test
      - run: npm run build
```

## パイプライン設計原則

1. **高速フィードバック**: テストは5分以内、ビルドは10分以内を目標
2. **並列実行**: 独立したジョブは並列化
3. **キャッシュ活用**: 依存関係、ビルド成果物をキャッシュ
4. **環境分離**: dev → staging → production の順序

## デプロイ戦略

| 戦略 | リスク | ロールバック | 用途 |
|------|--------|--------------|------|
| Blue-Green | 低 | 即座 | 本番環境 |
| Canary | 低 | 段階的 | 大規模サービス |
| Rolling | 中 | 段階的 | Kubernetes |
| Recreate | 高 | 遅い | 開発環境 |

## 詳細ガイド

- **GitHub Actions詳細**: [reference/github-actions.md](reference/github-actions.md)
- **GitLab CI設定**: [reference/gitlab-ci.md](reference/gitlab-ci.md)
- **デプロイ戦略実装**: [reference/deploy-strategies.md](reference/deploy-strategies.md)
- **トラブルシューティング**: [reference/troubleshooting.md](reference/troubleshooting.md)

## ユーティリティスクリプト

```bash
# パイプライン実行時間分析
python scripts/analyze_pipeline.py workflow.yml

# シークレット検証
python scripts/validate_secrets.py .github/workflows/

# 依存関係キャッシュキー生成
python scripts/generate_cache_key.py package-lock.json
```

## ワークフロー: 新規パイプライン構築

```
進捗チェックリスト:
- [ ] 1. 要件定義（ビルド、テスト、デプロイ先）
- [ ] 2. ブランチ戦略決定
- [ ] 3. パイプライン設定ファイル作成
- [ ] 4. シークレット設定
- [ ] 5. テスト実行・検証
- [ ] 6. ドキュメント作成
```

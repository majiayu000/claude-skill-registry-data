---
name: .claude/skills/docker-build-push-action/SKILL.md
description: |
    GitHub ActionsにおけるDockerイメージのビルドとプッシュの専門知識。
    専門分野:
    - docker/build-push-action: 公式アクションの完全な構文とオプション
    - BuildKit: キャッシュ、マルチステージビルド、最適化戦略
    - マルチプラットフォームビルド: linux/amd64、linux/arm64対応
    - レジストリ認証: GHCR、DockerHub、ECR、GCR統合
    - タグ戦略: セマンティックバージョニング、Git SHA、ブランチベース
    使用タイミング:
    - Dockerイメージをビルド・プッシュするワークフローを作成する時
    - マルチプラットフォーム対応のイメージを構築する時
    - コンテナレジストリへの認証を設定する時
    - BuildKitキャッシュを最適化してビルド時間を短縮する時

  📚 リソース参照:
  このスキルには以下のリソースが含まれています。
  必要に応じて該当するリソースを参照してください:

  - `.claude/skills/docker-build-push-action/resources/build-push-syntax.md`: docker/build-push-action完全構文、BuildKitキャッシュ、マルチプラットフォームビルド
  - `.claude/skills/docker-build-push-action/resources/registry-auth.md`: GHCR、DockerHub、ECR、GCRへの認証パターンとSecrets管理
  - `.claude/skills/docker-build-push-action/templates/docker-workflow.yaml`: 基本/マルチプラットフォーム/マルチレジストリの8種類のワークフロー例
  - `.claude/skills/docker-build-push-action/scripts/analyze-dockerfile.mjs`: Dockerfileの最適化提案とビルドパフォーマンス分析

  Use proactively when implementing .claude/skills/docker-build-push-action/SKILL.md patterns or solving related problems.
version: 1.0.0
---

# Docker Build/Push Action

## 概要

GitHub Actions で Docker イメージをビルド・プッシュするための専門知識を提供します。

## リソース構造

```
docker-build-push-action/
├── SKILL.md
├── resources/
│   ├── build-push-syntax.md     # 完全構文、BuildKit
│   └── registry-auth.md         # GHCR/DockerHub/ECR/GCR認証
├── templates/
│   └── docker-workflow.yaml     # 8種のワークフロー例
└── scripts/
    └── analyze-dockerfile.mjs   # Dockerfile分析
```

## コマンドリファレンス

```bash
# 完全構文リファレンス
cat .claude/skills/docker-build-push-action/resources/build-push-syntax.md

# レジストリ認証パターン
cat .claude/skills/docker-build-push-action/resources/registry-auth.md

# ワークフロー例（基本/マルチプラットフォーム/マルチレジストリ等）
cat .claude/skills/docker-build-push-action/templates/docker-workflow.yaml

# Dockerfile分析
node .claude/skills/docker-build-push-action/scripts/analyze-dockerfile.mjs <path>
```

## クイックスタート

### 基本ビルド・プッシュ

```yaml
name: Docker Build
on:
  push:
    branches: [main]

jobs:
  docker:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}
          tags: type=ref,event=branch
      - uses: docker/build-push-action@v5
        with:
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### マルチプラットフォーム

```yaml
- uses: docker/setup-qemu-action@v3
- uses: docker/build-push-action@v5
  with:
    platforms: linux/amd64,linux/arm64
    tags: ghcr.io/${{ github.repository }}:latest
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## 主要概念

### BuildKit キャッシュ

| タイプ          | 説明                      | 用途           |
| --------------- | ------------------------- | -------------- |
| `type=gha`      | GitHub Actions キャッシュ | 標準 CI/CD     |
| `type=registry` | レジストリキャッシュ      | マルチランナー |
| `mode=max`      | 全中間レイヤー            | 最大再利用     |

### タグ戦略

| パターン                          | 例           |
| --------------------------------- | ------------ |
| `type=ref,event=branch`           | `main`       |
| `type=semver,pattern={{version}}` | `1.2.3`      |
| `type=sha`                        | `sha-abc123` |

### プラットフォーム

`linux/amd64`, `linux/arm64`, `linux/arm/v7`

## ベストプラクティス

### セキュリティ

- 最小権限: `contents: read`, `packages: write`
- PR プッシュ禁止: `push: ${{ github.event_name != 'pull_request' }}`
- BuildKit Secrets: `RUN --mount=type=secret`
- イメージスキャン: Trivy 統合

### パフォーマンス

- Buildx 並列化（デフォルト有効）
- マルチステージビルド
- レイヤー順序最適化（変更少 → 多）
- GitHub Actions キャッシュ: `type=gha,mode=max`

### Dockerfile 最適化

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN pnpm ci
COPY . .
RUN pnpm run build
CMD ["node", "dist/index.js"]
```

## 関連スキル

| スキル                                           | 内容             |
| ------------------------------------------------ | ---------------- |
| `.claude/skills/github-actions-syntax/SKILL.md`  | ワークフロー構文 |
| `.claude/skills/secrets-management-gha/SKILL.md` | Secrets 管理     |
| `.claude/skills/caching-strategies-gha/SKILL.md` | キャッシュ戦略   |
| `.claude/skills/workflow-security/SKILL.md`      | セキュリティ     |

## トラブルシューティング

**ビルド失敗**: `node scripts/analyze-dockerfile.mjs Dockerfile` または `build-args: BUILDKIT_PROGRESS=plain`

**認証エラー**: `permissions: packages: write` 確認、`secrets.GITHUB_TOKEN` 存在確認

**マルチプラットフォームエラー**: `docker/setup-qemu-action@v3` と `docker/setup-buildx-action@v3` 確認

## 更新履歴

- **v1.0.0** (2025-11-27): 初版作成

---
name: writing-dockerfiles
description: Guides Dockerfile creation and optimization. Use when Dockerfile or Docker Compose is detected. Supports multi-stage builds, cache optimization, security hardening, and image size minimization.
---

# Dockerfile ベストプラクティス

## 使用タイミング
- **Dockerfile作成・修正時は必ずこのスキルを参照**
- コンテナ化プロジェクトの新規作成
- 既存Dockerfileの最適化
- セキュリティレビュー

---

## 1. マルチステージビルド（必須）

### 基本原則
ビルド環境と実行環境を分離し、最終イメージサイズを大幅削減（例: 916MB → 31.4MB）

### Go言語の例
```dockerfile
# ビルドステージ
FROM golang:1.21 AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# 実行ステージ
FROM gcr.io/distroless/static:nonroot
COPY --from=builder /app/main /main
USER 65532:65532
ENTRYPOINT ["/main"]
```

### Node.jsの例
```dockerfile
# ビルドステージ
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# 実行ステージ
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
CMD ["node", "dist/index.js"]
```

### Pythonの例
```dockerfile
# ビルドステージ
FROM python:3.12-slim AS builder
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# 実行ステージ
FROM python:3.12-slim AS runner
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
USER nobody
CMD ["python", "-m", "app"]
```

---

## 2. キャッシュ最適化（必須）

### レイヤー順序の原則
**変更頻度の低いものを先に配置**

```dockerfile
# 正しい順序
COPY package.json package-lock.json ./  # 依存関係定義（変更少）
RUN npm ci                               # 依存関係インストール
COPY . .                                 # アプリケーションコード（変更多）

# 間違い: ソースコード変更で依存関係キャッシュが無効化
COPY . .
RUN npm ci
```

### RUNコマンドの統合
関連操作を1つのRUNで実行し、レイヤー数とサイズを最小化

```dockerfile
# 推奨
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# 非推奨: 不要なレイヤーとキャッシュが残る
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y ca-certificates
```

---

## 3. .dockerignore（必須）

プロジェクトルートに`.dockerignore`を必ず作成

```dockerignore
# Git
.git
.gitignore

# 依存関係（ビルド時に再インストール）
node_modules
.venv
__pycache__

# ビルド成果物
dist
build
*.egg-info

# テスト・ドキュメント
tests
docs
*.md
!README.md

# IDE・エディタ
.vscode
.idea
*.swp

# 環境ファイル（機密情報）
.env*
!.env.example

# Docker関連
Dockerfile*
docker-compose*
.dockerignore
```

---

## 4. セキュリティ強化（必須）

### 非rootユーザー実行
```dockerfile
# UID 65532 (nonroot) を使用
USER 65532:65532

# または名前付きユーザー
USER nobody

# Node.jsの場合
USER node
```

### Distrolessベースイメージ
シェルやパッケージマネージャーを含まない最小イメージ

```dockerfile
# 静的バイナリ用
FROM gcr.io/distroless/static:nonroot

# 動的リンク用
FROM gcr.io/distroless/base:nonroot

# Python用
FROM gcr.io/distroless/python3:nonroot

# Node.js用
FROM gcr.io/distroless/nodejs20:nonroot
```

### ENTRYPOINT vs CMD
```dockerfile
# ENTRYPOINT: 固定コマンド（変更不可）
ENTRYPOINT ["python", "-m", "app"]

# CMD: デフォルト引数（実行時に上書き可能）
CMD ["--port", "8080"]

# 組み合わせ例
ENTRYPOINT ["python", "-m", "app"]
CMD ["--port", "8080"]
# 実行: docker run myapp --port 3000  → python -m app --port 3000
```

---

## 5. イメージ脆弱性スキャン（推奨）

### CI/CDパイプラインに組み込む
```yaml
# GitHub Actions例
- name: Scan for vulnerabilities
  uses: docker/scout-action@v1
  with:
    command: cves
    image: ${{ env.IMAGE_NAME }}
    only-severities: critical,high
    exit-code: true  # 脆弱性検出時に失敗
```

### ローカルスキャン
```bash
# Docker Scout
docker scout cves myimage:latest

# Trivy
trivy image myimage:latest
```

---

## 6. Hadolintによる静的解析（推奨）

### よく指摘される問題
- `latest`タグの使用 → バージョン固定を推奨
- 非効率なレイヤー構造
- キャッシュ最適化の欠如
- セキュリティ上の問題

### 実行方法
```bash
# ローカル実行
hadolint Dockerfile

# Docker経由
docker run --rm -i hadolint/hadolint < Dockerfile
```

### CI/CD統合
```yaml
# GitHub Actions
- name: Lint Dockerfile
  uses: hadolint/hadolint-action@v3.1.0
  with:
    dockerfile: Dockerfile
```

---

## 7. チェックリスト

### 作成時の必須確認事項
- [ ] マルチステージビルドを使用
- [ ] 依存関係ファイルを先にCOPY
- [ ] RUNコマンドを統合
- [ ] .dockerignoreを作成
- [ ] 非rootユーザーで実行
- [ ] ENTRYPOINTとCMDを適切に使い分け
- [ ] バージョンタグを固定（`:latest`を避ける）

### レビュー時の確認事項
- [ ] 不要なファイルがイメージに含まれていない
- [ ] 機密情報（APIキー等）がイメージに含まれていない
- [ ] ヘルスチェックが設定されている
- [ ] 脆弱性スキャンをパス

---

## 8. 参考リソース

- [Docker公式ベストプラクティス](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Google Distroless Images](https://github.com/GoogleContainerTools/distroless)
- [Hadolint](https://github.com/hadolint/hadolint)
- [Docker Scout](https://docs.docker.com/scout/)

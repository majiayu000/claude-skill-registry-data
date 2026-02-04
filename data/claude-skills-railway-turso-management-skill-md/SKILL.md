---
name: .claude/skills/railway-turso-management/SKILL.md
description: |
  Railway Database管理スキル。Railway環境グループ、Variables vs Secrets、
  Turso integration、Railway CLI統合、一時ファイルセキュリティを提供します。

  📚 リソース参照:
  このスキルには以下のリソースが含まれています。
  必要に応じて該当するリソースを参照してください:

  - `.claude/skills/railway-turso-management/resources/railway-turso-guide.md`: Railway Turso 詳細ガイド

  使用タイミング:
  - RailwayプロジェクトのSecret管理を設計する時
  - Railway環境グループを設定する時
  - Turso integrationを設定する時
  - Railway CLI経由のローカル開発を設定する時
  - Railway Logsセキュリティを確保する時

  Use when configuring Railway database, setting up environment groups,
  integrating Turso, or securing Railway deployments.
version: 1.0.0
---

# Railway Turso Database Management

## 概要

Railway は、環境変数を暗号化して保存し、デプロイ時にアプリケーションに注入する
Secrets 管理機能を提供します。このスキルは、Railway 固有の機能を最大限活用した
セキュアな Turso データベース管理を実現します。

## Railway Secrets vs Variables

### Secrets(機密情報)

**特徴**:

- 暗号化保存
- UI 上でマスク表示(\*\*\*)
- 監査ログ記録
- アクセス制限可能

**用途**:

- API キー(OPENAI_API_KEY、STRIPE_SECRET_KEY)
- データベース認証(TURSO_DATABASE_URL、TURSO_AUTH_TOKEN)
- 暗号化キー(NEXTAUTH_SECRET)
- OAuth Client Secret
- Webhook URL(DISCORD_WEBHOOK_URL)

**設定方法**:

\`\`\`
Railway Dashboard
→ Project
→ Environment (development/staging/production)
→ Variables
→ + New Variable
→ Variable name: OPENAI_API_KEY
→ Value: sk-proj-...
→ 🔒 Mark as secret(✅ チェック)
→ Add
\`\`\`

### Variables(非機密設定)

**特徴**:

- 平文保存
- UI 上で表示可能
- 監査ログなし

**用途**:

- アプリケーション名(APP_NAME)
- ログレベル(LOG_LEVEL)
- 機能フラグ(ENABLE_FEATURE_X)
- 公開 URL(API_BASE_URL)
- ポート番号(PORT)

**重要**: 機密情報は必ず「Mark as secret」をチェック

## Railway 環境グループ管理

### 環境の作成

\`\`\`
Railway Dashboard
→ Project
→ Environments
→ + New Environment
→ Name: staging
→ Create
\`\`\`

### 環境別変数設定の推奨構成

\`\`\`
Project: MyApp
│
├── 🏗️ Environment: development
│ ├── Service: web
│ └── Variables:
│ Secrets:
│ - OPENAI_API_KEY=sk-proj-dev-...
│ - NEXTAUTH_SECRET=<dev-secret>
│ - TURSO_DATABASE_URL=libsql://dev-db.turso.io
│ - TURSO_AUTH_TOKEN=<dev-token>
│ Variables:
│ - NODE_ENV=development
│ - LOG_LEVEL=debug
│
├── 🧪 Environment: staging
│ ├── Service: web
│ └── Variables:
│ Secrets:
│ - OPENAI_API_KEY=sk-proj-staging-...
│ - NEXTAUTH_SECRET=<staging-secret>
│ - TURSO_DATABASE_URL=libsql://staging-db.turso.io
│ - TURSO_AUTH_TOKEN=<staging-token>
│ Variables:
│ - NODE_ENV=staging
│ - LOG_LEVEL=info
│
└── 🚀 Environment: production
├── Service: web
└── Variables:
Secrets: - OPENAI_API_KEY=sk-proj-prod-... - NEXTAUTH_SECRET=<prod-secret-high-entropy> - TURSO_DATABASE_URL=libsql://prod-db.turso.io - TURSO_AUTH_TOKEN=<prod-token> - DISCORD_WEBHOOK_URL=https://discord.com/...
Variables: - NODE_ENV=production - LOG_LEVEL=warn
\`\`\`

### Railway CLI での環境変数管理

\`\`\`bash

# 環境選択

railway environment

# → development, staging, production から選択

# 変数一覧表示

railway variables

# 変数設定(現在の環境)

railway variables set API_KEY=sk-proj-key

# 変数削除

railway variables delete API_KEY

# JSON形式でエクスポート(⚠️ 非推奨)

railway variables --json > vars.json

# → 即座に削除すること: rm vars.json

\`\`\`

## Turso Database Integration

### セットアップ

Turso は Railway のネイティブプラグインではないため、手動で環境変数を設定します。

**手順**:

1. Turso CLI で データベースを作成
2. 環境別のデータベースを作成(dev/staging/prod)
3. 認証トークンを生成
4. Railway に環境変数を設定

### Turso CLI でのデータベース作成

\`\`\`bash

# Turso CLIインストール

curl -sSfL https://get.tur.so/install.sh | bash

# ログイン

turso auth login

# 開発用データベース作成

turso db create myapp-dev

# ステージング用データベース作成

turso db create myapp-staging

# 本番用データベース作成

turso db create myapp-prod

# データベースURL取得

turso db show myapp-dev --url

# 出力例: libsql://myapp-dev-[org].turso.io

# 認証トークン生成

turso db tokens create myapp-dev

# 出力例: eyJhbGc...

\`\`\`

### Railway への環境変数設定

**Development 環境**:

\`\`\`
Railway Dashboard
→ Project
→ Environment: development
→ Variables
→ + New Variable
→ Variable name: TURSO_DATABASE_URL
→ Value: libsql://myapp-dev-[org].turso.io
→ 🔒 Mark as secret(✅ チェック)
→ Add

→ + New Variable
→ Variable name: TURSO_AUTH_TOKEN
→ Value: eyJhbGc...
→ 🔒 Mark as secret(✅ チェック)
→ Add
\`\`\`

**Staging/Production 環境**: 同様の手順で各環境のデータベース URL とトークンを設定

**メリット**:

- 環境毎に自動分離(dev/staging/prod で別 DB インスタンス)
- Edge ロケーションでの低レイテンシ
- 組み込み レプリケーション機能
- SQLite 互換で高速

**.env.example への記載**:

\`\`\`bash

# Database(Turso)

# ローカル開発: railway run pnpm run dev で自動注入

# または ローカル SQLite ファイル使用

TURSO_DATABASE_URL=libsql://[database]-[org].turso.io
TURSO_AUTH_TOKEN=your-auth-token-here

# ローカル開発用(オプション)

# TURSO_DATABASE_URL=file:./local.db

\`\`\`

## Railway CLI 統合

### ローカル開発フロー

**方法 1: railway run(推奨)**

\`\`\`bash

# Railwayから環境変数を注入して実行

railway run pnpm run dev

# メリット:

# - ファイルに保存しない(メモリ内注入)

# - Git誤コミットリスクなし

# - 環境選択が明示的

\`\`\`

**方法 2: ローカル.env(非推奨)**

\`\`\`bash

# Railway Secretsをローカルファイルにダウンロード

railway variables --json | jq -r 'to_entries | .[] | "\(.key)=\(.value)"' > .env.local

# ⚠️ 警告:

# 1. .env.localを必ず.gitignoreに追加

# 2. 作業終了後は即座に削除

# 3. 本番環境のSecretは絶対にダウンロードしない

# 使用後は即座に削除

rm .env.local
\`\`\`

**方法 3: ローカル SQLite(開発専用)**

\`\`\`bash

# .env.development.local

TURSO_DATABASE_URL=file:./local.db

# TURSO_AUTH_TOKEN は不要(ローカルファイルの場合)

\`\`\`

### Railway Token セキュリティ

**Token 取得**:

\`\`\`
Railway Dashboard
→ Account Settings
→ Tokens
→ Create Token
→ Name: "GitHub Actions Deploy"
→ Scope: Project単位(推奨)
→ Permissions: "Deploy only"
→ Expiration: 90日後
→ Create
\`\`\`

**Token 保存**(GitHub Secrets):

\`\`\`
GitHub Repo
→ Settings
→ Secrets and variables → Actions
→ New repository secret
→ Name: RAILWAY_TOKEN
→ Value: <Railwayで生成したToken>
→ Add secret
\`\`\`

**Rotation(90 日毎)**:

\`\`\`bash

# 1. Railway Dashboardで新Token生成

# 2. GitHub SecretsのRAILWAY_TOKENを更新

# 3. Railway Dashboardで旧Tokenを Revoke

# 4. GitHub Actionsでデプロイテスト実行

\`\`\`

## Railway Logs セキュリティ

### ログへの Secret 露出防止

\`\`\`typescript
// ❌ 危険: SecretをログにNO出力
console.log("Database URL:", process.env.TURSO_DATABASE_URL);
// Railway Logs に露出！

// ✅ 安全: Secretをマスク
console.log("Database URL: \*\*\*");

// ✅ 安全: 構造化ログでSecretを除外
logger.info({
event: "db_connection",
status: "connected",
// database_url や auth_token は含めない
timestamp: new Date(),
});
\`\`\`

### Railway Logs での事後確認

\`\`\`
Railway Dashboard
→ Project
→ Deployments
→ View Logs
→ Search機能で検索:

- "libsql://"(Turso URL)
- "eyJhbGc"(JWT token prefix)
- "sk-proj-"(OpenAI Key)
- "sk*live*"(Stripe Key)
- "password"
- "secret"

→ 検出された場合:

1. 即座にそのSecretをRotation
2. ログ出力箇所を修正
3. 再デプロイ
   \`\`\`

## 一時ファイルとセキュリティ

### /tmp ディレクトリの揮発性

**Railway の仕様**:

- \`/tmp\`ディレクトリは**再デプロイ時に完全削除**される
- 永続化が必要なデータは外部ストレージ使用(S3、Cloudinary 等)

**Secret の一時保存禁止**:

\`\`\`typescript
// ❌ 危険: Secretをファイルに保存
import fs from "fs";
fs.writeFileSync("/tmp/auth-token.txt", process.env.TURSO_AUTH_TOKEN);

// ✅ 安全: Secretはメモリ内のみ
const authToken = process.env.TURSO_AUTH_TOKEN;
// メモリ内変数として使用
\`\`\`

### アップロードファイルのスキャン

\`\`\`typescript
import { Readable } from "stream";

class UploadSecurityScanner {
private secretPatterns = [
/sk-proj-[a-zA-Z0-9]{48}/, // OpenAI
/sk*live*[0-9a-zA-Z]{24,}/, // Stripe
/-----BEGIN ._ PRIVATE KEY-----/, // Private Key
/AKIA[0-9A-Z]{16}/, // AWS Access Key
/eyJhbGc[a-zA-Z0-9_-]_\.[a-zA-Z0-9_-]_\.[a-zA-Z0-9_-]\_/, // JWT tokens
/libsql:\/\/[a-zA-Z0-9-]+\.turso\.io/, // Turso URL
];

async scanFile(file: File): Promise<void> {
const content = await file.text();

    for (const pattern of this.secretPatterns) {
      if (pattern.test(content)) {
        throw new Error(
          "Uploaded file contains potential secret - upload rejected"
        );
      }
    }

}
}

// Uploadエンドポイントで使用
app.post("/api/upload", async (req, res) => {
const file = req.file;

// Secret スキャン
await scanner.scanFile(file);

// スキャン通過後のみ処理
await processUpload(file);
});
\`\`\`

## デプロイ戦略

### Blue-Green Deployment

\`\`\`
Railway環境設定:

production-blue(現行)

- TURSO_DATABASE_URL=libsql://prod-db.turso.io
- TURSO_AUTH_TOKEN=<Current Token>
- API_KEY=<Current Key>
- Status: Primary

production-green(新バージョン)

- TURSO_DATABASE_URL=libsql://prod-db.turso.io(同じDB)
- TURSO_AUTH_TOKEN=<Current Token>(同じToken)
- API_KEY=<New Key>(Rotation時)
- Status: Inactive

切り替え手順:

1. production-greenにデプロイ
2. ヘルスチェック実行
3. Railway Dashboard → Set as primary
4. トラフィック切り替え
5. production-blueを監視期間保持
   \`\`\`

### ローリングアップデート(Secret Rotation 時)

\`\`\`bash

# Phase 1: 新Secretを追加

railway variables set API_KEY_NEW=sk-proj-new-key

# Phase 2: アプリケーションコードを更新(新旧両方試行)

git push origin main

# Phase 3: 新Secretに完全移行確認

railway logs --tail

# Phase 4: 旧Secretを削除

railway variables delete API_KEY_OLD
\`\`\`

## 実装チェックリスト

### Railway 設定

- [ ] すべての機密情報が「Mark as secret」されているか？
- [ ] 環境グループが 3 つ設定されているか？(dev/staging/prod)
- [ ] Turso データベースが各環境に設定されているか？
- [ ] TURSO_DATABASE_URL と TURSO_AUTH_TOKEN が設定されているか？
- [ ] Variables(非機密)と Secrets(機密)が適切に分類されているか？

### Railway CLI

- [ ] Railway Token が安全に保管されているか？(GitHub Secrets)
- [ ] Token 権限が最小化されているか？(Deploy only)
- [ ] Token の Rotation スケジュールがあるか？(90 日)
- [ ] \`railway variables\`でダウンロードしたファイルが即座に削除されるか？

### ログセキュリティ

- [ ] ログ出力に Secret が含まれないか？
- [ ] Railway Logs で定期的に Secret 露出をチェックしているか？
- [ ] 構造化ログで Secret フィールドが除外されているか？

### 一時ファイル

- [ ] /tmp ディレクトリへの Secret 保存を避けているか？
- [ ] アップロードファイルがスキャンされているか？
- [ ] 永続化が必要なデータは外部ストレージ使用か？

### Turso 固有

- [ ] 環境別にデータベースが分離されているか？
- [ ] 認証トークンが定期的にローテーションされているか？
- [ ] ローカル開発用の SQLite フォールバックが設定されているか？

## 関連スキル

- \`.claude/skills/github-actions-security/SKILL.md\` - GitHub Actions 統合
- \`.claude/skills/environment-isolation/SKILL.md\` - 環境分離戦略
- \`.claude/skills/secret-management-architecture/SKILL.md\` - Secret 管理アーキテクチャ

## リソースファイル

- \`resources/railway-turso-guide.md\` - Railway Turso 詳細ガイド

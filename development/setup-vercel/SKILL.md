---
name: setup-vercel
description: "Vercel CLIのインストール・認証・設定を行う。「Vercel設定」「vercel設定」「Vercelセットアップ」を依頼されたときに使用する。"
---

# Setup Vercel Workflow

Vercel CLIのインストールから認証までを対話的にサポートする。

## Instructions

### 1. 前提条件チェック
Node.jsがインストールされているか確認:

```bash
node --version  # v18以上推奨
npm --version
```

Node.jsがない場合は先にインストールが必要。

### 2. 環境チェック
```bash
# Vercel CLIがインストールされているか
vercel --version

# 認証状態の確認
vercel whoami
```

### 3. インストール（未インストールの場合）

```bash
# npm（グローバル）
npm install -g vercel

# pnpm
pnpm install -g vercel

# yarn
yarn global add vercel
```

### 4. 認証

```bash
# ブラウザ認証（推奨）
vercel login
```

認証フロー:
1. コマンド実行後、ブラウザが開く（または URLが表示される）
2. 表示されたURLにアクセス
3. 画面に表示されるコードを確認
4. Vercelアカウントでログイン（GitHubアカウント連携推奨）
5. 「Authorize」をクリック

### 5. 認証確認

```bash
# ログイン状態を確認
vercel whoami

# 期待される出力:
# > username
```

### 6. アカウント作成（未登録の場合）

1. https://vercel.com/signup にアクセス
2. 「Continue with GitHub」を選択（推奨）
3. GitHubアカウントで認証
4. Hobby（無料）プランを選択
5. 完了後、`vercel login` を再実行

## Hobbyプラン（無料）の制限

| 項目 | 制限 |
|------|------|
| 帯域幅 | 100GB/月 |
| ビルド時間 | 6,000分/月 |
| プロジェクト数 | 無制限 |
| デプロイ数 | 無制限 |
| プライベートリポジトリ | 対応 |

※ 商用利用はProプラン（$20/月）が必要

## トラブルシューティング

### トークンが無効
```bash
# 再ログイン
vercel logout
vercel login
```

### 権限エラー（npm グローバルインストール）
```bash
# sudoを使う（非推奨）
sudo npm install -g vercel

# または npxで実行（インストール不要）
npx vercel
npx vercel login
```

### GitHubリポジトリ連携エラー
VercelダッシュボードでGitHub Appの権限を確認:
1. https://vercel.com/account/integrations にアクセス
2. GitHubの「Configure」をクリック
3. 必要なリポジトリへのアクセスを許可

## 確認コマンド

```bash
# 状態確認
vercel whoami
vercel teams ls  # チーム一覧（あれば）

# プロジェクト一覧
vercel projects ls
```

## 成功条件
- `vercel whoami` でユーザー名が表示される
- `vercel --prod` でデプロイが実行できる

---
name: repo-documentation
description: >
  リポジトリの構造・技術スタック・機能一覧・セットアップ手順を動的に解析し、
  包括的なドキュメントを自動生成するスキル。言語・フレームワーク問わず汎用的に動作する。
  Use this skill whenever the user asks to:
  - Explain a repository / リポジトリの説明 / リポジトリの概要
  - Generate a README / README生成 / README作成
  - Understand project structure / プロジェクト構成を教えて / 構造を説明して
  - Learn how to run a project / 使い方を教えて / 動かし方 / セットアップ方法
  - Get a repo overview / repo overview / explain this repo / what does this repo do
  - List features / 機能一覧 / このプロジェクトは何ができる？
  - Onboard to a new codebase / コードベースのキャッチアップ / 新しいリポジトリに入った
  - "このリポジトリ何？" "プロジェクトの全体像" "how to run this project"
  - "コードの全体を把握したい" "ドキュメントを整備して" "技術スタックを知りたい"
  This skill is especially useful when joining a new project, onboarding team members,
  or when a repository lacks proper documentation. It works with ANY repository regardless
  of programming language, framework, or project type.
---

# Repo Documentation Generator

## Philosophy

**「コードは書いた人以外には暗号に見える」** — だからこそ、リポジトリの全体像を素早く・正確に把握できるドキュメントが必要。このスキルは、どんなリポジトリでも構造を読み解き、開発者が「すぐに動かせる・すぐに理解できる」ドキュメントを生成する。

## Workflow — 4 Phases

### Phase 1: Discovery（リポジトリ探索）

まずリポジトリの全体像を掴む。以下の情報を並列で収集する。

**1. プロジェクトルートの確認**
```
必ず確認するファイル:
- README.md / README（既存ドキュメント）
- package.json / Cargo.toml / go.mod / pyproject.toml / Gemfile / pom.xml / build.gradle
  → 言語・依存関係・スクリプトの特定
- .env.example / .env.sample → 環境変数の把握
- docker-compose.yml / Dockerfile → コンテナ環境の有無
- Makefile / justfile / Taskfile.yml → タスクランナーの把握
- .github/workflows/ / .circleci/ / .gitlab-ci.yml → CI/CDの有無
- CLAUDE.md / .cursor/ / .github/copilot-instructions.md → AI設定
```

**2. ディレクトリ構造のスキャン**

`find` や `tree` ではなく、Glob ツールを使ってパターンベースで探索する。
重要なのは「何がどこにあるか」のマッピング。

```
探索パターン（言語問わず）:
- src/**/*、app/**/*、lib/**/* → メインソースコード
- test/**/*、tests/**/*、spec/**/*、__tests__/**/* → テスト
- docs/**/*、doc/**/* → ドキュメント
- scripts/**/*、bin/**/* → ユーティリティスクリプト
- config/**/*、.config/**/* → 設定ファイル
- migrations/**/*、db/**/* → データベース関連
- public/**/*、static/**/*、assets/**/* → 静的ファイル
```

**3. 技術スタック判定ロジック**

以下の優先順位で技術スタックを特定する:

| 判定方法 | 信頼度 | 例 |
|---------|--------|-----|
| パッケージマネージャ設定 | 最高 | package.json の dependencies |
| ロックファイル | 高 | yarn.lock、Cargo.lock、go.sum |
| 設定ファイル | 高 | tsconfig.json、next.config.js |
| ファイル拡張子の分布 | 中 | .rs が多い → Rust プロジェクト |
| インポート文の解析 | 中 | import React → React 使用 |
| ディレクトリ名の慣習 | 低 | pages/ → Next.js かもしれない |

### Phase 2: Analysis（解析）

Discovery で集めた情報を構造化する。

**1. アーキテクチャの特定**

リポジトリのパターンを識別する:
- **モノリス**: 単一アプリケーション
- **モノレポ**: 複数パッケージ（workspaces / packages/ / apps/）
- **マイクロサービス**: 複数独立サービス（services/ / docker-compose に複数サービス）
- **ライブラリ**: パッケージとして公開される（npm / crate / pip）
- **CLI ツール**: コマンドラインアプリケーション
- **フルスタック**: フロントエンド + バックエンド（client/ + server/ など）
- **インフラ / IaC**: CDK / Terraform / Pulumi

**2. 機能の抽出**

コードから機能を特定するために以下を調べる:
- **ルーティング定義**: API エンドポイント、ページルート
- **エントリーポイント**: main 関数、index ファイル、app の起動処理
- **モデル / スキーマ**: データ構造の定義
- **テストファイル**: テスト名から機能を逆引き（テストは仕様書）
- **コマンド定義**: CLI のサブコマンド
- **設定ファイル**: 有効化されている機能フラグ

**3. セットアップ手順の推定**

以下から動かし方を推定する:
- package.json の `scripts`（dev / start / build / test）
- Makefile のターゲット
- Dockerfile / docker-compose.yml の内容
- CI/CD の設定（CI が動かしている手順 = 正しい手順）
- .env.example の内容（必要な環境変数）
- 既存 README のセットアップセクション

### Phase 3: Generation（ドキュメント生成）

以下のテンプレートに沿ってドキュメントを生成する。ユーザーが特に指定しない限り日本語で出力する。

#### 出力テンプレート

```markdown
# {プロジェクト名}

{1-2文の概要: このプロジェクトが何で、何を解決するか}

## 技術スタック

| カテゴリ | 技術 |
|---------|------|
| 言語 | {言語とバージョン} |
| フレームワーク | {フレームワーク} |
| データベース | {DB、該当する場合} |
| インフラ | {デプロイ先、該当する場合} |
| テスト | {テストフレームワーク} |
| CI/CD | {CI/CDツール、該当する場合} |

## ディレクトリ構成

{主要ディレクトリとその役割を tree 形式で表示}

## 機能一覧

{発見した機能をカテゴリ別にリスト}

## セットアップ

### 前提条件
{必要なツール・ランタイム}

### インストール
{ステップバイステップの手順}

### 環境変数
{必要な環境変数とその説明（.env.example ベース）}

### 起動
{開発サーバー / ビルド / テスト実行の手順}

## 主要コマンド

| コマンド | 説明 |
|---------|------|
| {コマンド} | {何をするか} |

## アーキテクチャ概要

{コードの流れ、主要モジュール間の関係}
```

#### テンプレートの適用ルール

- テンプレートは「最大限」の構成。情報がないセクションは省略する（空セクションは作らない）
- 機能一覧は推測ではなく、コードから実際に確認できた機能だけを記載する
- セットアップ手順は実際に動くコマンドのみ記載する（推測コマンドには「要確認」と注記）
- モノレポの場合、各パッケージごとにサブセクションを設ける

### Phase 4: Output（出力）

**出力先の判断基準:**
- ユーザーが「READMEを生成して」→ `README.md` として書き出す
- ユーザーが「説明して」「教えて」→ チャット上に出力する（ファイル書き出しはしない）
- ユーザーが「ドキュメントを整備して」→ `docs/` ディレクトリに書き出す
- 不明な場合 → チャット上に出力し、ファイル保存が必要か確認する

**言語の判断基準:**
- デフォルトは日本語
- ユーザーが英語で質問してきた場合は英語で出力
- 既存 README が英語の場合、README生成時は英語にする（ただし確認する）
- 明示的に言語を指定された場合はそれに従う

## Edge Cases

**空に近いリポジトリ（初期化直後）:**
→ 存在するファイルだけで最小限のドキュメントを生成。「プロジェクトは初期段階です」と明記。

**巨大モノレポ:**
→ トップレベルの概要 + 各パッケージの要約に留める。詳細は個別パッケージを指定してもらう。

**ドキュメントが既にある場合:**
→ 既存ドキュメントを読み、欠けている情報を補完する形で提案。既存内容を上書きしない。

**プライベートな情報:**
→ `.env` ファイルの実際の値、シークレット、認証情報は絶対にドキュメントに含めない。`.env.example` のキー名のみ参照する。

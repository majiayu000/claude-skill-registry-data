---
name: mcp-integration
description: |
  Miyabi MCP統合スキル - プロジェクト内の7つのMCPサーバーを活用した高度な機能提供。
  IDE診断、GitHub拡張、プロジェクトコンテキスト、ファイルシステム、コンテキストエンジニアリング、
  Miyabi CLI、dev3000デバッグツールを統合。

  Use when:
  - VS Codeの診断情報やJupyter実行が必要な時
  - GitHubのIssue/PR操作が必要な時
  - プロジェクト依存関係の分析が必要な時
  - コンテキスト最適化やセマンティック検索が必要な時
  - Miyabi CLIコマンド(init, agent-run, status, auto)を実行する時
  - UIデバッグやブラウザ統合ログが必要な時
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

# MCP Integration Skill

Miyabiプロジェクトで利用可能な7つのMCPサーバーを統合的に活用するスキル。

## 利用可能なMCPサーバー

### 1. IDE Integration (`ide-integration`)
VS Code診断とJupyter実行の統合。

**提供ツール:**
- `mcp__ide__getDiagnostics` - 言語診断情報取得
- `mcp__ide__executeCode` - Jupyterカーネルでコード実行

**ユースケース:**
- TypeScript/ESLintエラーの一覧取得
- Jupyterノートブックのセル実行

### 2. GitHub Enhanced (`github-enhanced`)
拡張されたGitHub操作。

**環境変数:**
- `GITHUB_TOKEN` - GitHub Personal Access Token
- `REPOSITORY` - 対象リポジトリ

**ユースケース:**
- Issue/PRの高度な操作
- Projects V2との統合
- 自動ラベル付与

### 3. Project Context (`project-context`)
プロジェクト固有のコンテキスト情報。

**提供機能:**
- package.json解析
- 依存関係グラフ生成
- プロジェクト構造分析

### 4. Filesystem (`filesystem`)
ファイルシステムアクセス。

**提供機能:**
- ファイル読み書き
- ディレクトリ操作
- ファイル検索

### 5. Context Engineering (`context-engineering`)
AI駆動のコンテキスト分析・最適化。

**提供ツール:**
- `search_guides_with_gemini` - セマンティック検索
- `analyze_guide` - ガイド分析
- `analyze_guide_url` - 外部コンテンツ分析
- `compare_guides` - 複数ガイド比較

**APIサーバー:** `http://localhost:8888`

**ユースケース:**
- コンテキスト品質スコアリング (0-100)
- トークン効率最適化 (52%向上)
- セマンティック一貫性分析

### 6. Miyabi Integration (`miyabi`)
Miyabi CLI完全統合。

**提供ツール:**
- `miyabi__init` - 新規プロジェクト作成
- `miyabi__install` - 既存プロジェクトにインストール
- `miyabi__status` - ステータス確認
- `miyabi__agent_run` - Autonomous Agent実行
- `miyabi__auto` - Water Spider全自動モード
- `miyabi__todos` - TODOコメント自動検出
- `miyabi__config` - 設定管理
- `miyabi__get_status` - 軽量ステータス取得

**使用例:**
```
# プロジェクトステータス確認
"プロジェクトのステータスを確認して"
→ miyabi__get_status を自動実行

# Issue処理
"Issue #123を処理して"
→ miyabi__agent_run({ issueNumber: 123 }) を自動実行
```

### 7. dev3000 (`dev3000`)
UI/UX統合デバッグツール。

**特徴:**
- サーバー・ブラウザ・ネットワーク統合ロギング
- 83%デバッグ時間削減
- リアルタイムUI検査

## 設定ファイル

`.claude/mcp.json` で全MCPサーバーを管理:

```json
{
  "mcpServers": {
    "ide-integration": { "disabled": false },
    "github-enhanced": { "disabled": false },
    "project-context": { "disabled": false },
    "filesystem": { "disabled": false },
    "context-engineering": { "disabled": false },
    "miyabi": { "disabled": false },
    "dev3000": { "disabled": false }
  }
}
```

## MCPサーバーの有効化/無効化

```json
{
  "mcpServers": {
    "context-engineering": {
      "disabled": true  // 無効化
    }
  }
}
```

## トラブルシューティング

### Context Engineering APIサーバー起動
```bash
cd external/context-engineering-mcp
uvicorn main:app --port 8888
```

### MCP接続確認
```bash
claude mcp list  # 接続されているMCPサーバー一覧
```

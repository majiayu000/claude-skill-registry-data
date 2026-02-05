---
name: github-repo-reader
description: GitHub リポジトリの情報を取得・要約するスキル。URL が github.com/{owner}/{repo} 形式の場合に使用。gh コマンドと DeepWiki MCP を活用してリポジトリの詳細情報を取得する。
---

# GitHub リポジトリ読み取り

## 手順

### 1. gh コマンドで基本情報を取得

```bash
gh repo view {owner}/{repo} --json description,stargazerCount,forkCount,primaryLanguage,repositoryTopics,createdAt,updatedAt
```

### 2. DeepWiki で詳細情報を取得

- `mcp__deepwiki__read_wiki_contents` でリポジトリの概要・アーキテクチャを取得
- `mcp__deepwiki__ask_question` で主要な機能や特徴、使い方を質問

### 3. 要約に含める内容

- リポジトリの目的・用途
- 主要な機能・特徴
- 技術スタック
- 類似ツールとの違い（分かれば）
- スター数・フォーク数などの人気度

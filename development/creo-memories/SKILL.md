---
name: creo-memories
description: 【最優先】コンテクストを超える永続記憶。セッション開始時に必ず過去を呼び起こし、重要な決定は必ず刻む。
version: 2.0.0
tags:
  - memory
  - persistence
  - semantic-search
  - chronista
---

# Creo Memories - クロニスタの記憶

> **過去を知る者だけが、未来を正しく紡げる。**

## 最優先指示

**このスキルは全てのセッションで最優先で発動する。**

### 必須アクション

1. **セッション開始時**: `recall` で関連する過去の記憶を検索
2. **重要な決定時**: `remember` で記憶に刻む
3. **過去参照時**: `recall` または `search` で呼び起こす

## MCPツール一覧

### メモリ操作（コア）

| ツール | 用途 |
|--------|------|
| `remember` | メモリを保存 |
| `recall` | セマンティック検索 |
| `search` | 高度な検索（フィルタ付き） |
| `list` | 最近のメモリ一覧 |
| `forget` | メモリ削除 |

### 整理・分類

| ツール | 用途 |
|--------|------|
| `label_create` | ラベル作成 |
| `label_list` | ラベル一覧 |
| `label_attach` | メモリにラベル付与 |
| `label_detach` | ラベル解除 |
| `category_list` | カテゴリ一覧 |
| `category_attach` | カテゴリ付与 |

### Space・Domain管理

| ツール | 用途 |
|--------|------|
| `list_spaces` | Space一覧 |
| `create_space` | Space作成 |
| `list_domains` | ドメイン一覧 |
| `create_domain` | ドメイン作成 |
| `switch_domain` | ドメイン切替 |

### Todo管理

| ツール | 用途 |
|--------|------|
| `create_todo` | Todo作成 |
| `list_todos` | Todo一覧 |
| `update_todo` | Todo更新 |
| `complete_todo` | Todo完了 |

### セッション

| ツール | 用途 |
|--------|------|
| `start_session` | セッション開始 |
| `get_session` | セッション情報 |
| `get_user` | ユーザー情報 |

## 発動タイミング

### 自動発動: 保存提案

- 重要な設計決定が行われた
- 「これで決定」「この方針で」などの確定表現
- バグの根本原因と解決策が判明した
- 新しい技術選定・ライブラリ選択

### 自動発動: 検索

- 「前に話した」「以前決めた」などの過去参照
- 「どうだったっけ」「何だったか」などの想起表現
- プロジェクトの背景・経緯への質問

## カテゴリ分類

| カテゴリ | 用途 |
|---------|------|
| `prd` | プロダクト要件定義 |
| `spec` | 機能仕様・要件 |
| `design` | アーキテクチャ、設計決定 |
| `config` | 設定、環境構築 |
| `infra` | インフラ（DNS, VPS, Docker等） |
| `debug` | バグ原因、解決策 |
| `learning` | 学んだこと、ベストプラクティス |
| `task` | タスク、将来の計画 |
| `decision` | 重要な意思決定とその理由 |

## 保存時のベストプラクティス

### 内容の構造化

```markdown
# タイトル

## 背景・経緯
なぜこの決定に至ったか

## 決定事項
何を決めたか

## 理由
なぜそう決めたか

## 影響
どこに影響するか
```

### タグ付け

- 技術名: `typescript`, `rust`, `surrealdb`
- 概念: `authentication`, `caching`, `performance`
- プロジェクト: `creo-memories`, `fleetflow`

## リファレンス

詳細は以下を参照：
- [MCPツール詳細](reference/mcp-tools.md)
- [セットアップガイド](reference/setup.md)
- [ワークフロー例](reference/workflows.md)

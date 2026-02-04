---
name: check-library
description: ライブラリの情報を確認するためのスキル。Next.js、shadcn、その他のライブラリについて、適切なMCPサーバーを使用して最新のドキュメントと使用方法を取得します。
---

# Check Library

このスキルは、ライブラリの情報を確認するために適切なMCPサーバーを選択して利用します。

## Instructions

ライブラリ名に応じて、以下の優先順位でMCPサーバーを使用してください：

### 1. Next.js関連の場合

Next.jsに関する質問や実装の場合は、next-devtools MCPを使用します。

```
# 最初に初期化（セッション開始時に1回のみ）
mcp__plugin_getty104_next-devtools__init

# ドキュメント検索
mcp__plugin_getty104_next-devtools__nextjs_docs
  action: "search"
  query: "<検索キーワード>"

# ドキュメント取得（パスが分かっている場合）
mcp__plugin_getty104_next-devtools__nextjs_docs
  action: "get"
  path: "<ドキュメントパス>"
```

### 2. shadcn関連の場合

shadcn/uiに関する質問や実装の場合は、shadcn MCPを使用します。

```
# shadcn MCPツールを使用
# 利用可能なツールはListMcpResourcesToolで確認可能
```

### 3. その他のライブラリの場合

上記以外のライブラリについては、context7 MCPを使用します。

```
# ライブラリIDの解決
mcp__plugin_getty104_context7__resolve-library-id
  libraryName: "<ライブラリ名>"

# ドキュメント取得
mcp__plugin_getty104_context7__get-library-docs
  context7CompatibleLibraryID: "<resolve-library-idで取得したID>"
  topic: "<オプション: 特定のトピック>"
  page: 1
```

## 使用例

### Next.jsのApp Routerについて調べる
1. `mcp__plugin_getty104_next-devtools__init` で初期化
2. `mcp__plugin_getty104_next-devtools__nextjs_docs` でApp Routerのドキュメントを検索

### shadcn/uiのButtonコンポーネントについて調べる
1. shadcn MCPのツールを使用してButtonコンポーネントの情報を取得

### React Queryの使い方を調べる
1. `mcp__plugin_getty104_context7__resolve-library-id` でReact QueryのライブラリIDを取得
2. `mcp__plugin_getty104_context7__get-library-docs` でドキュメントを取得

## 注意事項

- ライブラリ名が曖昧な場合は、ユーザーに確認してから適切なMCPを選択してください
- Next.jsとshadcnは専用のMCPがあるため、優先的に使用してください
- context7を使用する場合は、必ず `resolve-library-id` でライブラリIDを解決してから `get-library-docs` を使用してください

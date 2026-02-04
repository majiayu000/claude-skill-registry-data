---
name: Searching Web
description: Execute web searches with prioritized MCP server strategy (Brave-Search → WebFetch). Use when searching the web, looking up documentation, or when user mentions 検索/search/調べて.
allowed-tools: mcp__brave-search__brave_web_search, WebFetch
---

# Searching Web

MCPサーバーを優先順位付けして効率的にWeb検索を実行するスキル。

## いつ使うか

- Web検索が必要な時
- 最新情報を調べる時
- 公式ドキュメントを参照する時
- ユーザーが「検索して」「調べて」と言及した時

## 検索戦略

### 優先順位付けフォールバック

```
1. Brave-Search MCP Server（第一優先）
   ↓ 失敗した場合
2. WebFetch MCP Server（フォールバック）
```

## 実行フロー

### ステップ1: Brave-Search で検索
まず Brave-Search MCP Server を使用：
```
mcp__brave-search__brave_web_search
```

**利点**:
- 高速
- 構造化されたデータ
- 複数結果を一度に取得

### ステップ2: フォールバック処理
Brave-Search が利用できない、またはエラーが発生した場合：
```
WebFetch
```

**利点**:
- 単一URLの詳細な取得
- HTMLコンテンツの解析
- より柔軟な取得

## 使用例

### 一般的なWeb検索
```
1. Brave-Search で "Next.js 15 新機能" を検索
2. 結果から最も関連性の高い記事を選択
3. 必要に応じて WebFetch で詳細を取得
```

### 公式ドキュメント検索
```
1. Brave-Search で "React useEffect official docs" を検索
2. 公式サイトのURLを特定
3. WebFetch でページ内容を取得・解析
```

### エラー時のフォールバック
```
1. Brave-Search を試行
   ↓ (エラー発生)
2. WebFetch に切り替え
3. 検索エンジンURLを直接指定
```

## 検索クエリの最適化

### 効果的なクエリ
- **具体的なキーワード**: "Next.js App Router data fetching"
- **バージョン指定**: "TypeScript 5.0 新機能"
- **公式指定**: "official documentation"

### 非効率なクエリ
- ❌ "プログラミング"（曖昧すぎる）
- ❌ "エラー"（コンテキスト不足）

## OSS ライブラリ情報取得時の特別ルール

OSS ライブラリに関する情報が必要な場合は、**Context7 MCP Server** を優先使用：

```
Context7 MCP Server
  ↓ 利用不可の場合
Brave-Search MCP Server
  ↓ 利用不可の場合
WebFetch MCP Server
```

Context7 の利点：
- 最新の公式ドキュメント
- ライブラリ特化の情報
- API リファレンス

## エラーハンドリング

### Brave-Search エラー時
1. エラーメッセージを確認
2. WebFetch に自動切り替え
3. ユーザーに通知

### WebFetch エラー時
1. URL の有効性を確認
2. リダイレクトを追跡
3. 必要に応じて別のURLを試行

## チェックリスト

- [ ] Brave-Search を第一優先で試したか
- [ ] エラー時に WebFetch にフォールバックしたか
- [ ] OSS情報の場合、Context7 を検討したか
- [ ] 検索クエリは具体的か
- [ ] 結果をユーザーに明確に提示したか

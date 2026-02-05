---
name: using-next-devtools
description: Provides Next.js development integration tools. Primary tool for Next.js projects. Offers diagnostics, upgrades, Cache Components optimization, and automatic error fixes.
---

# Next.js開発統合ツール

## 🎯 使用タイミング
- **Next.jsプロジェクト開発時（必須）**
- **Next.jsアップグレード時（最優先）**
- **Server Components実装・最適化時**
- **エラー診断・デバッグ時**

## 📋 開発ワークフロー

### 1. プロジェクト開始時の診断
```typescript
// 開発サーバーを起動（npm run dev または yarn dev）

// 診断実行
mcp__next-devtools__nextjs_runtime({
  action: "discover_servers"  // 実行中のNext.jsサーバー検出
})

mcp__next-devtools__nextjs_runtime({
  action: "list_tools",
  port: 3000  // 検出されたポート
})

// ルート構造確認
mcp__next-devtools__nextjs_runtime({
  action: "call_tool",
  port: 3000,
  toolName: "nextjs_get_routes"
})
```

### 2. Next.jsアップグレード
```typescript
// 自動アップグレード（codemod実行含む）
mcp__next-devtools__upgrade_nextjs_16({
  project_path: "."  // カレントディレクトリ
})
// → Next.js、React、React DOMを自動アップグレード
// → 破壊的変更に自動対応
```

### 3. Cache Components最適化
```typescript
// 完全自動セットアップ
mcp__next-devtools__enable_cache_components({
  project_path: "."
})
// → Suspense境界を自動設定
// → "use cache"ディレクティブ挿入
// → エラー検出と自動修正
```

### 4. エラー診断・自動修正
```typescript
// エラー診断
mcp__next-devtools__nextjs_runtime({
  action: "call_tool",
  port: 3000,
  toolName: "nextjs_get_errors"
})

// 自動修正
mcp__next-devtools__nextjs_runtime({
  action: "call_tool",
  port: 3000,
  toolName: "nextjs_auto_fix"
})
```

### 5. 公式ドキュメント検索
```typescript
mcp__next-devtools__nextjs_docs({
  query: "server components cache",
  category: "guides"  // getting-started, guides, api-reference等
})
```

## ⚠️ 重要な制約
- **Next.js 16.0.0+が必須**（beta版は非サポート）
- **開発サーバー起動が必要**: runtime診断前に`npm run dev`
- **クリーンな作業ディレクトリ推奨**: アップグレード前にコミット

## 🌟 推奨ワークフロー（Next.jsプロジェクト）
```
1. プロジェクト分析
   ├─ serena MCP: コードベース全体の構造把握
   └─ next-devtools MCP: Next.js特有の構造とルート確認

2. 実装前の確認
   ├─ context7 MCP: 最新Next.js仕様確認
   └─ next-devtools MCP: 現在のバージョンと推奨事項確認

3. 実装
   ├─ serena MCP: コード編集
   ├─ shadcn MCP: UIコンポーネント管理
   └─ next-devtools MCP: Server Components最適化

4. テスト・デバッグ
   ├─ next-devtools MCP: エラー診断と自動修正
   └─ playwright MCP: E2Eテスト
```

## 📚 主要ツール
- `nextjs_runtime` - 実行中サーバーとの対話
- `upgrade_nextjs_16` - 自動アップグレード
- `enable_cache_components` - Cache最適化
- `nextjs_docs` - 公式ドキュメント検索

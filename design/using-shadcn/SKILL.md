---
name: using-shadcn
description: Manages shadcn/ui components in React/Next.js projects. Use for searching, adding, and managing UI components. Requires components.json in project root.
---

# shadcn/ui UIコンポーネント管理

## 🎯 使用タイミング
- **React/Next.jsプロジェクトのUI実装時（必須）**
- **新しいUIコンポーネント追加時**
- **コンポーネント使用例確認時**
- **品質チェック実施時**

## 📋 使用ワークフロー

### 1. プロジェクト確認
```typescript
// components.jsonの存在確認
mcp__shadcn__get_project_registries()

// ない場合は初期化
// Bash: npx shadcn-ui@latest init
```

### 2. コンポーネント検索
```typescript
// ファジーマッチング検索
mcp__shadcn__search_items_in_registries({
  registries: ["@shadcn"],
  query: "button"
})

// 一覧表示
mcp__shadcn__list_items_in_registries({
  registries: ["@shadcn"],
  limit: 20
})
```

### 3. 詳細情報確認
```typescript
// コンポーネント詳細（ファイル内容含む）
mcp__shadcn__view_items_in_registries({
  items: ["@shadcn/button", "@shadcn/card"]
})

// 使用例・デモコード取得（重要）
mcp__shadcn__get_item_examples_from_registries({
  registries: ["@shadcn"],
  query: "button-demo"  // または "button example"
})
```

### 4. コンポーネント追加
```typescript
// 追加コマンド取得
mcp__shadcn__get_add_command_for_items({
  items: ["@shadcn/button", "@shadcn/card"]
})
// 返却例: "npx shadcn-ui@latest add button card"

// Bashで実行
// npx shadcn-ui@latest add button card
```

### 5. 品質チェック
```typescript
// 追加後の品質チェックリスト
mcp__shadcn__get_audit_checklist()
// → 動作確認項目、テスト項目を確認
```

## 🎨 よくあるパターン

### フォーム構築
```typescript
// 1. 必要なコンポーネントを検索
mcp__shadcn__search_items_in_registries({
  registries: ["@shadcn"],
  query: "form input button"
})

// 2. 使用例を確認
mcp__shadcn__get_item_examples_from_registries({
  registries: ["@shadcn"],
  query: "form-demo"
})

// 3. 一括追加
// Bash: npx shadcn-ui@latest add form input button label
```

### ダッシュボードUI
```typescript
// Card、Table、Chartを検索
mcp__shadcn__search_items_in_registries({
  registries: ["@shadcn"],
  query: "card table chart"
})

// デモコードを確認
mcp__shadcn__get_item_examples_from_registries({
  registries: ["@shadcn"],
  query: "card-demo"
})
```

## ⚠️ 重要な注意点
- **components.json必須**: プロジェクトルートに存在すること
- **使用例の活用**: 実装前に必ずデモコードを確認
- **品質チェック**: 追加後は必ずaudit checklistを実行
- **複数追加**: 関連コンポーネントは一度に追加（依存関係解決）

## 📚 検索パターン例
- `"button-demo"` - ボタンのデモコード
- `"form example"` - フォームの使用例
- `"card-demo"` - カードコンポーネントのデモ
- `"example-booking-form"` - 予約フォームの例
- `"tooltip-demo"` - ツールチップのデモ

## 🔗 関連ツール
- `get_project_registries` - レジストリ確認
- `search_items_in_registries` - コンポーネント検索
- `view_items_in_registries` - 詳細表示
- `get_item_examples_from_registries` - 使用例取得
- `get_add_command_for_items` - 追加コマンド
- `get_audit_checklist` - 品質チェック

---
name: developing-frontend
description: フロントエンド UI/UX 実装と最適化を支援します。React/Vue/Next.jsでの実装、パフォーマンス最適化、アクセシビリティを提供します。ユーザーインターフェース開発、Web アプリケーション構築が必要な場合に使用してください。
---

# フロントエンド開発とパフォーマンス最適化

## 概要

フロントエンド開発、React/Vue/Next.js実装、TypeScript型設計、パフォーマンス最適化を包括的に支援するスキルです。

## 実行フロー

### Step 1: プロジェクトセットアップ

#### フレームワーク選定基準

| フレームワーク | 用途                           | 特徴                       |
| -------------- | ------------------------------ | -------------------------- |
| React          | 汎用的なSPA                    | 最大のエコシステム         |
| Next.js        | SEO重視のWebアプリ             | SSR/SSG/ISRサポート        |
| Vue 3          | シンプルで学習しやすい         | Composition API            |
| Astro          | コンテンツ重視サイト           | ゼロJSデフォルト           |
| Svelte         | バンドルサイズ最小化           | コンパイル時最適化         |

### Step 2: TypeScript型設計

#### 高度な型システム

**ジェネリクスと制約:**

```typescript
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

**判別ユニオンと網羅性チェック:**

```typescript
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };
```

**ユーティリティ型の活用:**

- `Partial<T>`, `Pick<T, K>`, `Omit<T, K>`, `Record<K, V>`, `Required<T>`

**ブランド型:**

```typescript
type UserId = string & { readonly brand: unique symbol };
```

### Step 3: コンポーネント設計

#### Reactコンポーネントアーキテクチャ

- 単一責任の原則を守る
- Composition over Inheritance
- Props型を明確に定義

**カスタムフック:**

```typescript
function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  // ...
  return { user, loading, error };
}
```

### Step 4: 状態管理

#### 状態管理手法の選択

| 手法         | 用途                   | 学習曲線 |
| ------------ | ---------------------- | -------- |
| useState     | ローカル状態           | 低       |
| Context API  | テーマ、認証情報       | 中       |
| Zustand      | グローバル状態（軽量） | 低       |
| Redux Toolkit| 複雑な状態管理         | 高       |
| React Query  | サーバー状態管理       | 中       |

**Zustand（推奨）:**

```typescript
const useCartStore = create<CartStore>((set) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
}));
```

### Step 5: パフォーマンス最適化

#### React最適化テクニック

- **React.memo**: 不要な再レンダリングを防ぐ
- **useCallback/useMemo**: 関数・計算結果をメモ化
- **コード分割**: `lazy()` と `Suspense` で動的インポート
- **バーチャライゼーション**: `@tanstack/react-virtual` で大量リスト対応

#### Core Web Vitals目標

```
FCP (First Contentful Paint) < 1.8s
LCP (Largest Contentful Paint) < 2.5s
FID (First Input Delay) < 100ms
CLS (Cumulative Layout Shift) < 0.1
```

### Step 6: Tailwind CSSスタイリング

**レスポンシブデザイン:**

```tsx
<div className="w-full sm:w-1/2 md:w-1/3 lg:w-1/4 p-4">
```

### Step 7: テスト

**Testing Library:**

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
```

## 出力成果物

1. **プロジェクトセットアップ**: 初期化済みプロジェクト構造
2. **型定義**: TypeScriptの型定義ファイル
3. **コンポーネントライブラリ**: 再利用可能なUI部品
4. **状態管理**: ストア、カスタムフック
5. **スタイルシステム**: Tailwind設定、デザイントークン
6. **テストコード**: ユニット・統合テスト

## ベストプラクティス

1. **TypeScript Strict Mode**: 最大限の型安全性を確保
2. **コンポーネント設計**: 単一責任の原則を守る
3. **パフォーマンス**: React.memo、useCallback、useMemoを適切に使用
4. **アクセシビリティ**: セマンティックHTML、ARIA属性、キーボード操作
5. **テスト**: Testing Libraryで動作をテスト

## 関連ファイル

- [PATTERNS.md](./PATTERNS.md) - 実装パターン集
- [PERFORMANCE.md](./PERFORMANCE.md) - パフォーマンスチェックリスト

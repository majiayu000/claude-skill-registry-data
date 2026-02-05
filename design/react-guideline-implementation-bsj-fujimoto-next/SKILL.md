---
name: react-guideline-implementation
description: Implement React components following established coding guidelines and best practices. Use when creating new React components, refactoring existing code, implementing features with React best practices, or when the user asks to write React code, create components following guidelines, or implement features properly.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# React Guideline Implementation Skill

Reactコーディングガイドラインに準拠したコンポーネント実装を支援します。

## Instructions

### ステップ1: 要件の理解

実装する機能やコンポーネントの要件を明確化:

1. **コンポーネントの責任**: 何をするコンポーネントか
2. **Props**: どんなデータを受け取るか
3. **状態**: どんな状態を管理するか
4. **副作用**: API呼び出しやイベントリスナーなど

### ステップ2: ガイドラインの確認

プロジェクトのReactコーディングガイドラインを確認:

1. `REACT_CODING_GUIDELINES.md` を読み込み
2. プロジェクト固有のパターンを確認
3. 既存コンポーネントの実装パターンを参考に

### ステップ3: 設計の決定

#### コンポーネント構造

```
src/
├── components/          # 再利用可能なUI components
│   ├── Button.tsx
│   ├── FormInput.tsx
│   └── DataTable/
│       ├── index.tsx
│       ├── SearchBar.tsx
│       └── TableRow.tsx
├── hooks/               # Custom Hooks
│   ├── useAuth.ts
│   └── useData.ts
├── utils/               # ユーティリティ関数
│   └── helpers.ts
└── types/               # 型定義
    └── index.ts
```

#### コンポーネント分割の基準

1. **200行以内**: 1コンポーネントは200行を目安に
2. **単一責任**: 1つの責任のみを持つ
3. **再利用性**: 他の場所でも使える設計

### ステップ4: 型定義の作成

**✅ Good Practice:**

```typescript
// props の明示的な型定義
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  onClick?: () => void;
  children: React.ReactNode;
  disabled?: boolean;
}

// ジェネリック型の活用
interface DataTableProps<T> {
  data: T[];
  columns: Column<T>[];
  onRowClick?: (item: T) => void;
}

// Union Types で厳格な型制約
type Status = 'success' | 'pending' | 'failed' | 'warning';
```

**❌ Bad Practice:**

```typescript
// any の使用
interface Props {
  data: any;
}

// 型定義なし
function Component(props) {
  // ...
}
```

### ステップ5: コンポーネントの実装

#### テンプレート

```typescript
"use client"; // Next.js App Router の場合

import { useState, useCallback, useMemo } from "react";

interface ComponentProps {
  // Props の型定義
}

export default function Component({ /* props */ }: ComponentProps) {
  // 1. Hooks（上から順に）
  const [state, setState] = useState<Type>(initialValue);
  
  // 2. useMemo で派生値を計算
  const derivedValue = useMemo(() => {
    return computeExpensiveValue(state);
  }, [state]);
  
  // 3. useCallback でイベントハンドラーをメモ化
  const handleClick = useCallback(() => {
    // 処理
  }, [/* 依存 */]);
  
  // 4. useEffect で副作用を管理
  useEffect(() => {
    // 副作用
    return () => {
      // クリーンアップ
    };
  }, [/* 依存 */]);
  
  // 5. 早期リターン（条件付きレンダリング）
  if (loading) return <Spinner />;
  if (error) return <Error message={error} />;
  
  // 6. JSX
  return (
    <div>
      {/* UI */}
    </div>
  );
}
```

### ステップ6: パフォーマンス最適化

#### 1. メモ化の適用

```typescript
// useMemo で高コストな計算をメモ化
const sortedData = useMemo(() => {
  return [...data].sort((a, b) => a.name.localeCompare(b.name));
}, [data]);

// useCallback でコールバックをメモ化
const handleSubmit = useCallback((values: FormValues) => {
  // 処理
}, [/* 依存 */]);

// React.memo でコンポーネント自体をメモ化
export default React.memo(Component);
```

#### 2. リストの最適化

```typescript
// ✅ Good: 一意で安定したキー
{items.map((item) => (
  <ListItem key={item.id} data={item} />
))}

// ❌ Bad: インデックスをキーに使用
{items.map((item, index) => (
  <ListItem key={index} data={item} />
))}
```

#### 3. インライン定義の回避

```typescript
// ✅ Good: 外部で定義
const buttonStyle = { padding: 10 };

function Component() {
  const handleClick = useCallback(() => {}, []);
  
  return <Button style={buttonStyle} onClick={handleClick} />;
}

// ❌ Bad: インライン定義
function Component() {
  return <Button style={{ padding: 10 }} onClick={() => {}} />;
}
```

### ステップ7: Custom Hooks の作成

ビジネスロジックや副作用は Custom Hook に分離:

```typescript
// hooks/useAuth.ts
export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // 認証チェック
    checkAuth().then(setUser).finally(() => setLoading(false));
  }, []);
  
  const login = useCallback(async (credentials) => {
    const user = await authService.login(credentials);
    setUser(user);
  }, []);
  
  const logout = useCallback(async () => {
    await authService.logout();
    setUser(null);
  }, []);
  
  return { user, loading, login, logout };
}

// コンポーネントはシンプルに
function LoginPage() {
  const { login, loading } = useAuth();
  
  return (
    <LoginForm onSubmit={login} loading={loading} />
  );
}
```

### ステップ8: テストの考慮

テストしやすい設計を心がける:

```typescript
// ✅ Good: ロジックを分離
export function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

function Cart({ items }: CartProps) {
  const total = calculateTotal(items);
  return <div>Total: {total}</div>;
}

// ❌ Bad: ロジックがコンポーネント内
function Cart({ items }: CartProps) {
  const total = items.reduce((sum, item) => sum + item.price, 0);
  return <div>Total: {total}</div>;
}
```

## Examples

### 例1: シンプルなUIコンポーネント

```typescript
// components/Button.tsx
import { ButtonHTMLAttributes, ReactNode } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline";
  size?: "sm" | "md" | "lg";
  icon?: ReactNode;
  loading?: boolean;
}

const VARIANT_CLASSES = {
  primary: "bg-blue-500 text-white hover:bg-blue-600",
  secondary: "bg-gray-500 text-white hover:bg-gray-600",
  outline: "border border-gray-300 hover:bg-gray-50",
} as const;

const SIZE_CLASSES = {
  sm: "px-3 py-1.5 text-sm",
  md: "px-4 py-2 text-base",
  lg: "px-6 py-3 text-lg",
} as const;

export default function Button({
  variant = "primary",
  size = "md",
  icon,
  loading = false,
  children,
  className = "",
  disabled,
  ...props
}: ButtonProps) {
  return (
    <button
      {...props}
      disabled={disabled || loading}
      className={`
        inline-flex items-center justify-center gap-2 rounded-lg
        transition-colors duration-200
        ${VARIANT_CLASSES[variant]}
        ${SIZE_CLASSES[size]}
        ${className}
      `}
    >
      {loading && <Spinner />}
      {!loading && icon && <span>{icon}</span>}
      {children}
    </button>
  );
}
```

### 例2: ジェネリック型を使用したテーブルコンポーネント

```typescript
// components/DataTable.tsx
import { useMemo, useCallback } from "react";

interface Column<T> {
  key: keyof T;
  label: string;
  sortable?: boolean;
  render?: (value: T[keyof T], item: T) => React.ReactNode;
}

interface DataTableProps<T> {
  data: T[];
  columns: Column<T>[];
  getRowKey: (item: T) => string | number;
  onRowClick?: (item: T) => void;
}

export default function DataTable<T extends Record<string, any>>({
  data,
  columns,
  getRowKey,
  onRowClick,
}: DataTableProps<T>) {
  const handleRowClick = useCallback((item: T) => {
    onRowClick?.(item);
  }, [onRowClick]);
  
  return (
    <table>
      <thead>
        <tr>
          {columns.map((col) => (
            <th key={String(col.key)}>{col.label}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((item) => (
          <tr key={getRowKey(item)} onClick={() => handleRowClick(item)}>
            {columns.map((col) => (
              <td key={String(col.key)}>
                {col.render 
                  ? col.render(item[col.key], item)
                  : String(item[col.key])}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

### 例3: Custom Hook

```typescript
// hooks/useLocalStorage.ts
import { useState, useCallback, useEffect } from "react";

export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T) => void, () => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === "undefined") return initialValue;
    
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });
  
  const setValue = useCallback((value: T) => {
    try {
      setStoredValue(value);
      if (typeof window !== "undefined") {
        window.localStorage.setItem(key, JSON.stringify(value));
      }
    } catch (error) {
      console.error(error);
    }
  }, [key]);
  
  const removeValue = useCallback(() => {
    try {
      setStoredValue(initialValue);
      if (typeof window !== "undefined") {
        window.localStorage.removeItem(key);
      }
    } catch (error) {
      console.error(error);
    }
  }, [key, initialValue]);
  
  return [storedValue, setValue, removeValue];
}
```

## Checklist

実装前のチェックリスト:

- [ ] コンポーネントの責任は明確か
- [ ] Props の型定義は適切か
- [ ] 200行以内に収まっているか
- [ ] 状態管理は適切か（ローカル vs グローバル）
- [ ] パフォーマンス最適化は適切か
- [ ] テストしやすい設計か
- [ ] 既存のパターンに従っているか
- [ ] ガイドラインに準拠しているか

## Reference Files

- [React Coding Guidelines](../../REACT_CODING_GUIDELINES.md)
- [TypeScript Best Practices](./typescript.md)
- [Performance Optimization](./performance.md)

## Troubleshooting

### 既存のパターンを確認したい

1. `components/**/*.tsx` でサンプルを検索
2. 似たような責任を持つコンポーネントを参考に
3. プロジェクト固有の命名規則やスタイルを踏襲

### ガイドラインと矛盾する要件

1. ガイドラインを優先しつつ、要件も満たす方法を検討
2. トレードオフを明確化してユーザーに確認
3. 必要に応じてガイドラインの例外を提案

### パフォーマンスとコードの可読性のバランス

1. まず可読性を優先して実装
2. プロファイリングで実際のボトルネックを特定
3. 必要な箇所のみを最適化

## Version History

- v1.0.0 (2025-01-02): Initial release

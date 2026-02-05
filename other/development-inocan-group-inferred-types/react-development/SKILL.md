---
name: react-development
description: React開発の詳細ガイド。Hooks、コンポーネント設計、パフォーマンス最適化、テストなど、Reactアプリケーション開発のベストプラクティス。
---

# React Development Skill

## 📋 目次

1. [概要](#概要)
2. [いつ使うか](#いつ使うか)
3. [詳細ガイド](#詳細ガイド) 🔥 **NEW**
4. [Hooks活用（概要）](#hooks活用概要)
5. [コンポーネント設計（概要）](#コンポーネント設計概要)
6. [パフォーマンス最適化（概要）](#パフォーマンス最適化概要)
7. [アンチパターン](#アンチパターン)
8. [Agent連携](#agent連携)

---

## 概要

このSkillは、React開発の詳細をカバーします：

- **Hooks** - useState, useEffect, カスタムフック
- **コンポーネント設計** - 再利用可能なコンポーネント
- **パフォーマンス最適化** - memo, useMemo, useCallback
- **状態管理** - Context API, 外部ライブラリ
- **フォーム処理** - react-hook-form
- **テスト** - React Testing Library

---

## いつ使うか

### 🎯 必須のタイミング

- [ ] Reactコンポーネント作成時
- [ ] カスタムフック作成時
- [ ] パフォーマンス問題発生時
- [ ] フォーム実装時

---

## 詳細ガイド

### 📚 公式ドキュメント・参考リソース

**このガイドで学べること**: Hooksパターン、コンポーネント設計原則、パフォーマンス最適化手法
**公式で確認すべきこと**: 最新API、React 19の新機能、Server Components、マイグレーションガイド

#### 主要な公式ドキュメント

- **[React.dev](https://react.dev)** - React公式ドキュメント
  - [Learn React](https://react.dev/learn) - チュートリアル形式の学習ガイド
  - [API Reference](https://react.dev/reference/react) - 全APIの完全リファレンス
  - [Hooks Reference](https://react.dev/reference/react/hooks) - 全Hooksの詳細仕様
  - [React 19の新機能](https://react.dev/blog) - 最新リリースノート

- **[React TypeScript Cheatsheets](https://react-typescript-cheatsheet.netlify.app/)** - TypeScript × React
  - 型定義の実践的パターン
  - よくある型エラーと解決策
  - 高度な型テクニック

#### 関連リソース

- **[React DevTools](https://react.dev/learn/react-developer-tools)** - デバッグツール
- **[React Testing Library](https://testing-library.com/react)** - テストベストプラクティス
- **[React Patterns](https://reactpatterns.com/)** - デザインパターン集
- **[Awesome React](https://github.com/enaqx/awesome-react)** - ライブラリ・ツール一覧

---

### 📚 完全ガイドシリーズ

React開発の深い知識を習得するための詳細ガイドを用意しています。

#### 🎯 [React Hooks 完全マスターガイド](./guides/hooks/hooks-mastery.md)

**40,000文字超の完全ガイド | TypeScript完全対応**

Reactの最重要概念であるHooksを完全にマスターするための実践的ガイドです。

**含まれる内容:**
- useState 完全ガイド（Discriminated Union、Lazy Initialization、Functional Update）
- useEffect 完全ガイド（データフェッチ、依存配列の完全理解、クリーンアップパターン）
- useRef 完全ガイド（DOM参照、前の値の保持、Mutable値）
- カスタムフック 完全ガイド（useFetch、useLocalStorage、useDebounce、useThrottle等）
- useContext + useReducer パターン（Redux代替の完全実装）
- **実際の失敗事例 10選**（無限ループ、メモリリーク、古いクロージャ問題等）
- **実測パフォーマンスデータ**（useCallback: 70倍高速化、useMemo: 400倍高速化等）

**こんな方におすすめ:**
- Hooksの基本は理解したが、実務での使い方に不安がある
- パフォーマンス問題に直面している
- カスタムフックの設計パターンを学びたい
- 実際のプロジェクトでの失敗事例から学びたい

---

#### 🎯 [React × TypeScript パターン完全ガイド](./guides/typescript/typescript-patterns.md)

**33,000文字超の完全ガイド | 型安全な開発の決定版**

TypeScriptを使った型安全なReact開発のための実践的パターン集です。

**含まれる内容:**
- コンポーネントの型定義（React.FC vs 関数、Props、Children、HTML属性継承、Ref）
- Props の高度な型パターン（Discriminated Union、Omit、Pick、Partial、Required、Readonly）
- イベントハンドラの型（全イベント型、カスタムイベント、型推論）
- **ジェネリックコンポーネント**（List、Select、Table、Form の完全実装）
- 高度な型テクニック（Conditional Types、Mapped Types、Template Literals、Type Guards）
- Context の型安全な実装
- Form の型定義（React Hook Form との統合）
- **実装例 10選**
- よくある型エラーと解決策

**こんな方におすすめ:**
- TypeScriptの基本は理解したが、Reactとの組み合わせ方がわからない
- ジェネリックを使った再利用可能なコンポーネントを作りたい
- 型エラーに悩まされている
- 型安全性を最大限に活用したい

---

#### 🎯 [React パフォーマンス最適化 完全ガイド](./guides/performance/optimization-complete.md)

**20,000文字超の完全ガイド | 実測データに基づく最適化手法**

実際のプロジェクトでの実測データに基づいた、実践的なパフォーマンス改善手法です。

**含まれる内容:**
- パフォーマンス計測の基礎（React DevTools Profiler、Chrome DevTools）
- React.memo による再レンダリング防止（いつ使うべきか、カスタム比較関数）
- useMemo/useCallback の使い分け（実例付き）
- **Code Splitting**（React.lazy、Suspense、Route-based、Preloading）
- **仮想化（Virtualization）**（react-window、可変高さ、グリッド）
- レンダリング最適化（条件付きレンダリング、Fragment、Key）
- バンドルサイズ削減（Tree Shaking、依存関係見直し、Dynamic Import）
- 画像最適化（遅延ロード、WebP、レスポンシブ）
- **実測データと改善事例**（ECサイト: 9.3倍高速化、ダッシュボード: 79%削減等）

**こんな方におすすめ:**
- アプリが遅いと感じている
- Lighthouse のスコアを改善したい
- バンドルサイズを削減したい
- 実際の改善事例を知りたい

**実測データ例:**
- 商品一覧: レンダリング時間 2.8秒 → 0.3秒（9.3倍高速化）
- ダッシュボード: バンドルサイズ 850KB → 180KB（79%削減）
- タイムライン: スクロールFPS 25fps → 60fps（滑らか）

---

### 📖 学習の進め方

**初心者の方:**
1. まず下記の「Hooks活用（概要）」で基本を理解
2. [Hooks 完全マスターガイド](./guides/hooks/hooks-mastery.md)で深く学習
3. [TypeScript パターンガイド](./guides/typescript/typescript-patterns.md)で型安全性を習得

**経験者の方:**
1. 必要な詳細ガイドを直接参照
2. パフォーマンス問題があれば[最適化ガイド](./guides/performance/optimization-complete.md)
3. 型の問題があれば[TypeScript パターンガイド](./guides/typescript/typescript-patterns.md)

---

## Hooks活用（概要）

### 基本Hooks

#### useState - 状態管理

```tsx
// ✅ 基本的な使用
function Counter() {
  const [count, setCount] = useState(0)

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  )
}

// ✅ 複雑な状態（オブジェクト）
function UserForm() {
  const [form, setForm] = useState({
    name: '',
    email: ''
  })

  const handleChange = (field: string, value: string) => {
    setForm(prev => ({ ...prev, [field]: value }))
  }

  return (
    <>
      <input
        value={form.name}
        onChange={(e) => handleChange('name', e.target.value)}
      />
      <input
        value={form.email}
        onChange={(e) => handleChange('email', e.target.value)}
      />
    </>
  )
}
```

#### useEffect - 副作用

```tsx
// ✅ データフェッチ
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let ignore = false

    async function fetchUser() {
      setLoading(true)
      const data = await fetch(`/api/users/${userId}`).then(r => r.json())

      if (!ignore) {
        setUser(data)
        setLoading(false)
      }
    }

    fetchUser()

    return () => {
      ignore = true // クリーンアップ
    }
  }, [userId])

  if (loading) return <div>Loading...</div>
  if (!user) return <div>Not found</div>

  return <div>{user.name}</div>
}
```

#### useRef - DOM参照

```tsx
function SearchInput() {
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    // マウント時にフォーカス
    inputRef.current?.focus()
  }, [])

  return <input ref={inputRef} placeholder="Search..." />
}
```

### カスタムHooks

#### データフェッチフック

```tsx
// hooks/useFetch.ts
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    let ignore = false

    async function fetchData() {
      try {
        setLoading(true)
        const response = await fetch(url)
        if (!response.ok) throw new Error('Failed to fetch')
        const json = await response.json()

        if (!ignore) {
          setData(json)
          setError(null)
        }
      } catch (e) {
        if (!ignore) {
          setError(e as Error)
        }
      } finally {
        if (!ignore) {
          setLoading(false)
        }
      }
    }

    fetchData()

    return () => {
      ignore = true
    }
  }, [url])

  return { data, loading, error }
}

// 使用例
function UserList() {
  const { data: users, loading, error } = useFetch<User[]>('/api/users')

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <ul>
      {users?.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

#### ローカルストレージフック

```tsx
// hooks/useLocalStorage.ts
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      console.error(error)
      return initialValue
    }
  })

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value
      setStoredValue(valueToStore)
      window.localStorage.setItem(key, JSON.stringify(valueToStore))
    } catch (error) {
      console.error(error)
    }
  }

  return [storedValue, setValue] as const
}

// 使用例
function App() {
  const [theme, setTheme] = useLocalStorage<'light' | 'dark'>('theme', 'light')

  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      Current: {theme}
    </button>
  )
}
```

---

## コンポーネント設計（概要）

> 📖 **詳細は [TypeScript パターン完全ガイド](./guides/typescript/typescript-patterns.md) を参照してください**

### 再利用可能なボタン

```tsx
// components/ui/Button.tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
}

export function Button({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  children,
  className,
  disabled,
  ...props
}: ButtonProps) {
  const baseStyles = 'rounded font-medium transition-colors'

  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
    danger: 'bg-red-600 text-white hover:bg-red-700'
  }

  const sizes = {
    sm: 'px-3 py-1 text-sm',
    md: 'px-4 py-2',
    lg: 'px-6 py-3 text-lg'
  }

  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? 'Loading...' : children}
    </button>
  )
}

// 使用例
<Button variant="primary" size="lg" onClick={handleSubmit}>
  Submit
</Button>
```

### コンパウンドコンポーネント

```tsx
// components/Tabs.tsx
interface TabsContextValue {
  activeTab: string
  setActiveTab: (tab: string) => void
}

const TabsContext = React.createContext<TabsContextValue | undefined>(undefined)

function Tabs({ children, defaultTab }: { children: React.ReactNode; defaultTab: string }) {
  const [activeTab, setActiveTab] = useState(defaultTab)

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      {children}
    </TabsContext.Provider>
  )
}

function TabList({ children }: { children: React.ReactNode }) {
  return <div className="flex gap-2 border-b">{children}</div>
}

function Tab({ value, children }: { value: string; children: React.ReactNode }) {
  const context = React.useContext(TabsContext)
  if (!context) throw new Error('Tab must be used within Tabs')

  const { activeTab, setActiveTab } = context

  return (
    <button
      className={activeTab === value ? 'border-b-2 border-blue-600' : ''}
      onClick={() => setActiveTab(value)}
    >
      {children}
    </button>
  )
}

function TabPanel({ value, children }: { value: string; children: React.ReactNode }) {
  const context = React.useContext(TabsContext)
  if (!context) throw new Error('TabPanel must be used within Tabs')

  const { activeTab } = context
  if (activeTab !== value) return null

  return <div>{children}</div>
}

Tabs.List = TabList
Tabs.Tab = Tab
Tabs.Panel = TabPanel

// 使用例
<Tabs defaultTab="profile">
  <Tabs.List>
    <Tabs.Tab value="profile">Profile</Tabs.Tab>
    <Tabs.Tab value="settings">Settings</Tabs.Tab>
  </Tabs.List>

  <Tabs.Panel value="profile">
    <p>Profile content</p>
  </Tabs.Panel>
  <Tabs.Panel value="settings">
    <p>Settings content</p>
  </Tabs.Panel>
</Tabs>
```

---

## パフォーマンス最適化（概要）

> 📖 **詳細は [パフォーマンス最適化完全ガイド](./guides/performance/optimization-complete.md) を参照してください**

### React.memo - 不要な再レンダリング防止

```tsx
// ❌ 悪い例（毎回再レンダリング）
function UserCard({ user }: { user: User }) {
  console.log('Rendering UserCard')
  return <div>{user.name}</div>
}

// ✅ 良い例（propsが変わったときのみ再レンダリング）
const UserCard = React.memo(({ user }: { user: User }) => {
  console.log('Rendering UserCard')
  return <div>{user.name}</div>
})
```

### useMemo - 高コストな計算のメモ化

```tsx
function ExpensiveList({ items, filter }: { items: Item[]; filter: string }) {
  // ✅ filter または items が変わったときのみ再計算
  const filteredItems = useMemo(() => {
    console.log('Filtering items...')
    return items.filter(item => item.name.includes(filter))
  }, [items, filter])

  return (
    <ul>
      {filteredItems.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  )
}
```

### useCallback - 関数のメモ化

```tsx
function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([])

  // ✅ 関数をメモ化（子コンポーネントに渡す場合に重要）
  const handleToggle = useCallback((id: string) => {
    setTodos(prev =>
      prev.map(todo =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      )
    )
  }, [])

  return (
    <ul>
      {todos.map(todo => (
        <TodoItem key={todo.id} todo={todo} onToggle={handleToggle} />
      ))}
    </ul>
  )
}

const TodoItem = React.memo(({ todo, onToggle }: {
  todo: Todo;
  onToggle: (id: string) => void
}) => {
  return (
    <li>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo.id)}
      />
      {todo.title}
    </li>
  )
})
```

---

## アンチパターン

### ❌ 1. useEffectの無限ループ

```tsx
// ❌ 悪い例
function BadComponent() {
  const [data, setData] = useState([])

  useEffect(() => {
    fetch('/api/data')
      .then(res => res.json())
      .then(setData) // dataが更新 → useEffectが再実行 → 無限ループ
  }, [data])
}

// ✅ 良い例
function GoodComponent() {
  const [data, setData] = useState([])

  useEffect(() => {
    fetch('/api/data')
      .then(res => res.json())
      .then(setData)
  }, []) // 依存配列が空 → マウント時のみ実行
}
```

### ❌ 2. 過剰なuseCallback/useMemo

```tsx
// ❌ 悪い例（不要なメモ化）
function Component() {
  const name = useMemo(() => 'John', []) // 不要
  const greet = useCallback(() => console.log('Hello'), []) // 不要

  return <div>{name}</div>
}

// ✅ 良い例
function Component() {
  const name = 'John'
  const greet = () => console.log('Hello')

  return <div>{name}</div>
}
```

---

## Agent連携

### 📖 Agentへの指示例

**カスタムフック作成**
```
データフェッチ用のカスタムフックuseFetchを作成してください。
loading、error、dataを返すようにしてください。
```

**コンポーネント作成**
```
ユーザーカードコンポーネントを作成してください。
- ユーザー名、メール、アバターを表示
- hover時にシャドウを表示
- クリック時に詳細ページに遷移
```

---

## まとめ

### Reactのベストプラクティス

1. **Hooksを活用** - 状態管理、副作用、カスタムフック
2. **コンポーネント設計** - 再利用可能、単一責任
3. **パフォーマンス最適化** - memo, useMemo, useCallback
4. **型安全性** - TypeScript活用

---

## 関連スキル

- [Next.js Development](/nextjs-development/SKILL.md) - Next.js App Router の実践
- [Testing Strategy](/testing-strategy/SKILL.md) - React コンポーネントのテスト戦略
- [Frontend Performance](/frontend-performance/SKILL.md) - Web パフォーマンス最適化

---

_Last updated: 2024-12-26_

---
name: enforcing-type-safety
description: Enforces type safety in TypeScript/Python implementations. Any/any types strictly prohibited. Use when processing API responses, integrating external libraries, or implementing data validation. Supports strict mode configuration and type guard implementation.
---

# 型安全性の原則

## 📑 目次

このスキルは以下のファイルで構成されています：

- **SKILL.md** (このファイル): 概要と基本原則
- **[TYPESCRIPT.md](./TYPESCRIPT.md)**: TypeScript型安全性詳細
- **[PYTHON.md](./PYTHON.md)**: Python型安全性詳細
- **[ANTI-PATTERNS.md](./ANTI-PATTERNS.md)**: 避けるべきコード規則
- **[REFERENCE.md](./REFERENCE.md)**: チェックリスト、ツール設定、型チェッカー

## 🎯 使用タイミング

- **すべてのコード実装時（必須）**
- **TypeScript/Python使用時**
- **APIレスポンス処理時**
- **外部ライブラリ統合時**
- **レビュー時の品質確認**

## 🚫 絶対禁止: any/Any型の基本原則

### TypeScript

```typescript
❌ 絶対禁止:
- any型の使用
- Function型（anyと同等）
- non-null assertion（!）の濫用

✅ 代替手段:
- 明示的な型定義（interface/type）
- unknown + 型ガード
- ジェネリクス
- Utility Types
```

### Python

```python
❌ 絶対禁止:
- Any型の使用
- bare except
- eval/exec

✅ 代替手段:
- 明示的な型ヒント
- TypedDict
- Protocol（構造的部分型）
- Union型
```

## 💡 型安全性の3つの柱

### 1. 明示的な型定義

すべての関数、変数に型を明示的に定義します。

**TypeScript**:
```typescript
function getUserById(id: string): User | null {
  // 実装
}
```

**Python**:
```python
def get_user_by_id(user_id: str) -> Optional[User]:
    # 実装
    pass
```

### 2. 型ガードの活用

unknown型や不明な型は、型ガードで安全に処理します。

**TypeScript**:
```typescript
function isUser(data: unknown): data is User {
  return typeof data === 'object' &&
         data !== null &&
         'id' in data &&
         'name' in data
}

if (isUser(data)) {
  console.log(data.name)  // 型安全
}
```

**Python**:
```python
from typing import TypeGuard

def is_user(data: object) -> TypeGuard[User]:
    return isinstance(data, dict) and \
           'id' in data and 'name' in data

if is_user(data):
    print(data['name'])  # 型安全
```

### 3. 型チェッカーの実行

**TypeScript**: strict mode有効化
```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

**Python**: mypy/pyright実行
```bash
mypy src/
pyright src/
```

## ⚡ クイックリファレンス

### よくある状況と解決策

| 状況 | 悪い例 | 良い例 |
|------|--------|--------|
| API レスポンス | `response: any` | `response: ApiResponse` |
| 不明な型 | `data: any` | `data: unknown` + 型ガード |
| 複数の型 | `value: any` | `value: string \| number` |
| オプショナル | `user!.name` | `user?.name ?? 'Unknown'` |
| 配列操作 | `items: any[]` | `items: User[]` |

### ファイル構成の推奨

```
src/
├── types/
│   ├── api.ts        # API型定義
│   ├── models.ts     # データモデル型
│   └── utils.ts      # ユーティリティ型
├── guards/
│   └── type-guards.ts # 型ガード関数
└── ...
```

## 📊 型安全性レベル

コードの型安全性は以下のレベルで評価されます：

### レベル1: 基本（必須）
- [ ] any/Any型を使用していない
- [ ] すべての関数に型注釈
- [ ] strict mode有効化

### レベル2: 標準（推奨）
- [ ] 型ガードの適切な使用
- [ ] ジェネリクスの活用
- [ ] Utility Typesの活用

### レベル3: 高度（理想）
- [ ] 構造的部分型（Protocol）の活用
- [ ] 型レベルプログラミング
- [ ] 100%型カバレッジ

## 🔧 実装前の確認事項

新しいコードを書く前に：

1. **型定義ファイルの確認**
   - 既存の型を再利用できないか
   - 新しい型定義が必要か

2. **外部ライブラリの型**
   - 型定義がパッケージに含まれているか
   - @types/パッケージが必要か

3. **型の共有範囲**
   - ローカル型で十分か
   - 共有型として定義すべきか

## 🔗 関連スキル

- **applying-solid-principles**: SOLID原則とクリーンコード
- **testing**: 型安全なテストコード
- **securing-code**: セキュアな型使用
- **implementing-as-tachikoma**: Developer実装時の型安全性

詳細は各ファイルを参照してください。

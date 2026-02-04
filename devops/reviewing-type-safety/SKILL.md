---
name: reviewing-type-safety
description: >
  最大の型カバレッジのためのTypeScript型安全パターンとベストプラクティス。
  トリガー: 型安全, type safety, any, unknown, 型推論, 型ガード, type guard,
  discriminated union, 判別可能なUnion, strictNullChecks, 型定義, 型カバレッジ,
  TypeScript, 暗黙のany, implicit any, 型アサーション, type assertion.
allowed-tools: Read, Grep, Glob, Task
---

# 型安全レビュー - TypeScriptベストプラクティス

目標: 最小限の型の体操で最大の型安全性。

## 型安全メトリクス

| コンテキスト | ターゲット | 警告 |
| --- | --- | --- |
| 型カバレッジ | 95%+ | < 90% |
| Any使用 | 0（正当化がある場合のみ） | > 5インスタンス |
| 型アサーション | 最小限 | > 10インスタンス |
| 暗黙のany | 0 | Any > 0 |
| Strictモード | すべて有効 | いずれか無効 |

## セクションベースのロード

| セクション | ファイル | フォーカス | トリガー |
| --- | --- | --- | --- |
| カバレッジ | `references/type-coverage.md` | 明示的な型、anyを避ける | any, unknown, 型カバレッジ |
| ガード | `references/type-guards.md` | ナローイング、判別可能なUnion | 型ガード, type guard |
| Strict | `references/strict-mode.md` | tsconfig、React型 | strictNullChecks, React |

## クイックチェックリスト

### 型カバレッジ

- [ ] すべての関数に明示的な戻り値型
- [ ] すべてのパラメータが型付き（暗黙のanyなし）
- [ ] すべてのデータ構造にInterface/type定義
- [ ] 明示的な正当化なしの`any`なし

### 型ガードとナローイング

- [ ] Union型に型述語（`is`関数）
- [ ] 関連する型に判別可能なUnion
- [ ] `never`による網羅的チェック
- [ ] 安全でない型アサーション（`as`）を避ける

### Strictモード

- [ ] `strictNullChecks: true`
- [ ] `noImplicitAny: true`
- [ ] `strictFunctionTypes: true`
- [ ] Reactコンポーネントが適切なHTML属性を拡張

## 主要原則

| 原則 | 適用 |
| --- | --- |
| Fail Fast | 実行時ではなくコンパイル時にエラーをキャッチ |
| TSに推論させる | 既に明確なものを過度に型付けしない |
| 型はドキュメント | 良い型はドキュメントとして機能 |
| unknownを優先 | より安全なハンドリングのために`any`より`unknown`を使用 |

## 一般的なパターン

### 型ガード関数

```typescript
function isSuccess<T>(response: Response<T>): response is SuccessResponse<T> {
  return response.success === true
}
```

### 判別可能なUnion

```typescript
type Action =
  | { type: 'INCREMENT'; payload: number }
  | { type: 'DECREMENT'; payload: number }
  | { type: 'RESET' }

// 網羅的チェック
function reducer(action: Action): number {
  switch (action.type) {
    case 'INCREMENT': return action.payload
    case 'DECREMENT': return -action.payload
    case 'RESET': return 0
    default:
      const _exhaustive: never = action
      return _exhaustive
  }
}
```

### ジェネリックコンポーネント

```typescript
interface SelectProps<T> {
  value: T
  options: T[]
  onChange: (value: T) => void
}

function Select<T>({ value, options, onChange }: SelectProps<T>) { /* ... */ }
```

## 参照

### コア原則

- [@~/.claude/skills/applying-code-principles/SKILL.md](../../skills/applying-code-principles/SKILL.md) - 過度な型付けをしない
- [@~/.claude/skills/applying-code-principles/SKILL.md](../../skills/applying-code-principles/SKILL.md) - 型インターフェースはISPに従う

### 関連スキル

- `applying-code-principles` - 一般的なコード品質原則
- `generating-tdd-tests` - 型安全なテストパターン

### 使用エージェント

- `type-safety-reviewer` - このスキルの主要な使用者

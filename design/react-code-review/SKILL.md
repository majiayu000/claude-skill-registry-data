---
name: react-code-review
description: Review React/TypeScript code against established coding guidelines. Use when reviewing React components, performing code audits, checking for React best practices, anti-patterns, performance issues, or when the user asks to review React code, check code quality, or audit React implementation.
allowed-tools: Read, Grep, Glob
---

# React Code Review Skill

Reactコーディングガイドラインに基づいて、React/TypeScriptコードを体系的にレビューします。

## Instructions

### ステップ1: ガイドラインの確認

プロジェクトのReactコーディングガイドラインを読み込みます。

1. `REACT_CODING_GUIDELINES.md` または同様のガイドラインファイルを検索
2. ガイドラインが存在しない場合は、一般的なReactベストプラクティスを適用

### ステップ2: レビュー対象の特定

以下のパターンでReact/TypeScriptファイルを検索:

```
**/*.tsx
**/*.ts
**/components/**/*.tsx
**/hooks/**/*.ts
**/pages/**/*.tsx
**/app/**/*.tsx
```

### ステップ3: レビュー観点

各ファイルを以下の6つの観点でレビュー:

#### 1. **コンポーネント設計**
- [ ] 単一責任の原則に従っているか
- [ ] Props の型定義は適切か
- [ ] コンポーネントの大きさは適切か（200行以内推奨）
- [ ] コンポーネント合成を活用しているか

#### 2. **Hooks の使用**
- [ ] `useEffect` の依存配列は正しいか
- [ ] Custom Hook でロジックを分離しているか
- [ ] `useMemo`/`useCallback` の使用は適切か
- [ ] Hooks のルールに違反していないか

#### 3. **パフォーマンス**
- [ ] リストのキーは一意で安定しているか（`index` を避ける）
- [ ] 不要な再レンダリングを防いでいるか
- [ ] インラインオブジェクト/関数の定義を避けているか
- [ ] 大量データの場合は仮想化を検討しているか

#### 4. **型安全性**
- [ ] `any` の使用はないか
- [ ] Union Types やジェネリック型を活用しているか
- [ ] 型アサーションは最小限か
- [ ] Props の型定義は明示的か

#### 5. **状態管理**
- [ ] ローカル状態とグローバル状態を適切に分けているか
- [ ] 派生状態を不要に `useState` で管理していないか
- [ ] Prop Drilling を避けているか

#### 6. **アンチパターン**
- [ ] 直接の DOM 操作はないか
- [ ] ビジネスロジックと UI の分離は適切か
- [ ] `useEffect` の誤用はないか（同期処理を非同期にしていないか）

### ステップ4: 評価と報告

各ファイルごとに3段階で評価:

- **✅ Good**: 良い点
- **⚠️ Warning**: 改善の余地がある点
- **❌ Critical**: 重大な問題

具体的なコード箇所を示して改善提案を提供します。

### ステップ5: 優先度の決定

問題を優先度順に整理:

1. **Critical（❌）**: すぐに修正すべき
   - `any` の使用
   - リストキーに `index` 使用
   - メモリリーク
   - セキュリティ問題

2. **Warning（⚠️）**: 改善が推奨される
   - パフォーマンス最適化の余地
   - コンポーネントサイズ
   - コードの重複

3. **Good（✅）**: 維持すべき良い実装

## Examples

### 例1: コンポーネントのレビュー

```tsx
// 対象ファイル: components/UserList.tsx

❌ Critical:
- 120行目: リストのキーに index を使用
  現在: key={index}
  改善: key={user.id}

⚠️ Warning:
- 50行目: handleClick がインライン定義
  useCallback でメモ化すべき
  
- 80-95行目: データフェッチロジックがコンポーネント内
  Custom Hook に分離すべき

✅ Good:
- Props の型定義が明確
- 適切なコンポーネント分割
```

### 例2: Hooks のレビュー

```tsx
// 対象ファイル: hooks/useData.ts

❌ Critical:
- 15行目: useEffect の依存配列が不正確
  現在: }, [])
  改善: }, [userId, filter])

⚠️ Warning:
- useMemo を使用しているが、計算コストが低い
  不要な最適化の可能性

✅ Good:
- ロジックが Custom Hook に分離されている
- エラーハンドリングが適切
```

### 例3: パフォーマンスレビュー

```tsx
❌ Critical:
- インラインオブジェクトを props に渡している
  現在: <Child style={{ margin: 10 }} />
  改善: const style = { margin: 10 } を外部定義

⚠️ Warning:
- 1000件以上のリストを一度に描画
  react-window での仮想化を検討

✅ Good:
- React.memo で不要な再レンダリングを防止
```

## Output Format

レビュー結果は以下の形式で出力:

```markdown
# React Code Review Report

## 概要
- レビュー対象: XX ファイル
- Critical 問題: X件
- Warning: Y件
- Good: Z件

## 重大な問題（Critical）

### 1. [ファイル名](path/to/file.tsx:line)
**問題**: 説明
**現在のコード**:
```tsx
// 問題のあるコード
```
**改善案**:
```tsx
// 改善後のコード
```

## 改善の余地（Warning）

...

## 良い実装（Good）

...

## 推奨アクション

優先度順に修正すべき項目をリストアップ
```

## Reference Files

詳細なガイドラインについては以下を参照:
- [React Coding Guidelines](../../REACT_CODING_GUIDELINES.md)
- [Component Design Patterns](./patterns.md)
- [Performance Optimization Guide](./performance.md)

## Troubleshooting

### ガイドラインファイルが見つからない

1. プロジェクトルートで `*GUIDELINE*.md` を検索
2. 見つからない場合は一般的なReactベストプラクティスを適用
3. 必要に応じてガイドラインの作成を提案

### レビュー範囲が広すぎる

1. 特定のディレクトリやファイルに絞る
2. 優先度の高い問題から段階的にレビュー
3. コンポーネント、Hooks、ページなどカテゴリ別に分割

### 誤検知が多い

1. プロジェクト固有のパターンを考慮
2. ユーザーに確認を求める
3. 文脈を考慮した柔軟な判断

## Version History

- v1.0.0 (2025-01-02): Initial release

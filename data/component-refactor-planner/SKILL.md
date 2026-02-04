---
name: component-refactor-planner
description: 指定されたコンポーネントのリファクタリングを設計する。
---

# Component Refactor Planner

コンポーネントを分析し、リファクタリングの設計を行うスキル。

## リファクタリングの原則

1. **Single Responsibility** - 1コンポーネント/関数 = 1責務
2. **DRY** - 重複コードをhooks/utilsに抽出
3. **一貫性** - プロジェクトのパターンに従う
4. **テスタビリティ** - ロジックを分離してテスト可能に

## 自動分析ワークフロー

### ステップ0: テストカバレッジ確認

**IMPORTANT:** リファクタリング前にテストの存在を確認。

確認対象:

- `{Component}.stories.tsx` (play関数)
- `{Component}.a11y.test.tsx`
- `{Component}.vrt.test.tsx`
- `hooks/use{Hook}/use{Hook}.test.ts`
- `util.test.ts`

テスト不足時:

1. `/component-test-runner {Component}` でテスト状況確認
2. `/component-test-planner {Component}` でテスト設計
3. テスト追加後にリファクタリング開始

### ステップ1: コンポーネント情報収集

読み取り対象: `{Component}.tsx`, `type.ts`, `const.ts`, `hooks/`, `util.ts`

### ステップ2: 問題点の自動検出

| 観点     | チェック項目                             |
| -------- | ---------------------------------------- |
| 複雑度   | 行数>100、useState/useEffect≥5、ネスト≥3 |
| 責務     | UI/ロジック混在、インラインハンドラ≥3    |
| 一貫性   | ディレクトリ構造、命名規則、スタイル分離 |
| 再利用性 | 重複ロジック、汎用hooks抽出可能性        |

### ステップ3: 改善提案の生成

## リファクタリングパターン

### 1. ディレクトリ構造

```
Component/
├── Component.tsx
├── Component.stories.tsx
├── Component.a11y.test.tsx
├── Component.vrt.test.tsx
├── const.ts          # Tailwind Variants
├── type.ts           # Props型
├── index.ts
├── hooks/            # 複雑なロジック
├── util.ts           # 純粋関数
└── SubComponent/     # サブコンポーネント
```

### 2. Hooks抽出

**条件:** 複雑なstate/effect/callback、複数箇所で使用、独立テストしたい

**命名:** `use{Component}{Functionality}` (例: `useComboboxKeyboard`)

**Tips:**

- useEffectの必要性が不明な場合は、`use-effect-necessity`エージェントを使用して判定する
- 型定義は `type.ts` に分離し、`import type`でインポートする。

### 3. ユーティリティ抽出

**条件:** 純粋関数、計算ロジック、バリデーション

### 4. サブコンポーネント分割

**条件:** 50行以上のUIブロック、独自props、再利用可能性

### 5. Tailwind Variants

**命名:** `{COMPONENT}_{ELEMENT}_VARIANTS`

**条件:** className条件分岐≥3、複数箇所で使用

### 6. イベントハンドラ命名

- ユーザー操作: `handle{Action}` / `handle{Action}{Target}`
- Props: `on{Event}` (受け取り側)

### 7. 型定義

`ComponentProps<"element">` + `VariantProps` + JSDocコメント

## 出力フォーマット

```markdown
## {コンポーネント名} リファクタリング設計

### コンポーネント分析結果

| 項目        | 値    | 基準 | 状態  |
| ----------- | ----- | ---- | ----- |
| 行数        | {n}行 | ≤100 | ✅/⚠️ |
| useState数  | {n}個 | ≤5   | ✅/⚠️ |
| useEffect数 | {n}個 | ≤3   | ✅/⚠️ |

### テストカバレッジ状況

| 種別        | ファイル        | 存在      |
| ----------- | --------------- | --------- |
| Interaction | stories.tsx     | ✅/❌     |
| A11y        | a11y.test.tsx   | ✅/❌     |
| VRT         | vrt.test.tsx    | ✅/❌     |
| Unit        | hooks/util.test | ✅/❌/N/A |

⚠️ テスト不足時はリファクタリング前にテスト追加を推奨

### 検出された問題点

#### 問題1: {概要}

- 現状: {コード}
- 問題点: {説明}
- 優先度: High/Medium/Low

### リファクタリング提案

#### 提案1: {概要}

- 対象: {パス}
- 改善後: {構造/コード}
- メリット: {リスト}
- リスク: {リスト}

### 実装順序

1. [ ] {変更1}
2. [ ] {変更2}
3. [ ] テスト追加/更新
4. [ ] 最終確認

### 影響範囲

| ファイル | 変更種別       | 影響   |
| -------- | -------------- | ------ |
| {path}   | 新規/修正/削除 | {説明} |
```

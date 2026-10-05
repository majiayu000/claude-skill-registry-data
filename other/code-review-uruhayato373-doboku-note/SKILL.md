---
name: code-review
description: >
  src/ 配下の Next.js / TypeScript コードを品質・セキュリティ・パフォーマンス・保守性の 4 軸で網羅的にレビューする。doboku-note 固有の技術スタック規約（MDX・Cloudflare Pages・next-mdx-remote）を考慮。
  Use when user asks to [コードレビュー, コード品質チェック, src レビュー, /code-review].
domain: ops
---

# /code-review — Next.js コード品質レビュー

## 概要

`src/` 配下のNext.jsコードを対象に、品質・セキュリティ・パフォーマンス・保守性を網羅的にレビューするスキル。
VoltAgent code-reviewer + nextjs-developer をベースに、doboku-note固有の技術スタック・規約を組み込み。

## 使い方

```
/code-review                    # src/ 全体をレビュー
/code-review src/components/    # 特定ディレクトリに絞る
/code-review --focus security   # 特定カテゴリに絞る
```

## 実行手順

### Step 1: スコープ決定

- 引数があればそのディレクトリ/ファイルに絞る
- 引数なしなら `src/` 全体を対象とする
- `--focus` オプションで特定カテゴリに絞れる（security, performance, nextjs, maintainability, all）
- デフォルトは `all`

### Step 2: 静的解析の実行

まず自動ツールで検出可能な問題を洗い出す:

```bash
# TypeScript型チェック
npx tsc --noEmit 2>&1 | head -100

# ESLint
npm run lint 2>&1 | head -100
```

### Step 3: コードレビュー（6カテゴリ）

対象ファイルを読み、以下の6カテゴリで問題を検出する。

#### 3-1. Next.js アーキテクチャ（doboku-note固有）

- **Server/Client境界**: `'use client'` の適切な使用。不要なClient Componentがないか
- **App Router パターン**: layout.tsx / page.tsx / loading.tsx / error.tsx の適切な配置
- **データフェッチ**: Server Componentでのデータ取得。不要なクライアントフェッチがないか
- **画像最適化**: next/image の使用（※本プロジェクトは `images.unoptimized: true`。R2配信のため意図的）
- **メタデータ**: `generateMetadata` / `generateStaticParams` の適切な実装
- **MDX連携**: next-mdx-remote の使い方。MDXComponents の登録漏れ
- **Cloudflare Pages互換性**: Node.js API依存がないか（`output: 'export'` 前提）

#### 3-2. セキュリティ

- **XSS**: `dangerouslySetInnerHTML` の使用箇所。ユーザー入力のサニタイズ
- **APIルート**: `src/app/api/` のバリデーション・レート制限
- **環境変数**: クライアントに露出してはいけない値が `NEXT_PUBLIC_` になっていないか
- **依存関係**: 既知の脆弱性（`npm audit` 結果を参照）
- **インジェクション**: 動的パス・クエリパラメータの安全な処理

#### 3-3. パフォーマンス

- **バンドルサイズ**: 不要な依存、tree-shakingを阻害するインポート
- **コード分割**: `dynamic()` の適切な使用（重いクライアントライブラリ）
- **レンダリング**: 不要な再レンダリング、useMemo/useCallback の適切な使用
- **KaTeX**: クライアントサイドの初期化コスト。遅延ロードされているか
- **Core Web Vitals目標**: LCP < 2.5s, CLS < 0.1, INP < 200ms

#### 3-4. 保守性・コード品質

- **型安全性**: `any` の使用、型定義の不足
- **デッドコード**: 未使用のインポート・関数・コンポーネント
- **命名規約**: コンポーネント=PascalCase, ファイル=PascalCase.tsx, ユーティリティ=camelCase.ts
- **コンポーネント設計**: 適切な粒度、props設計、再利用性
- **エラーハンドリング**: ErrorBoundary の配置、try-catchの適切な使用
- **コード重複**: DRY違反の検出

#### 3-5. アクセシビリティ

- **セマンティックHTML**: 適切なタグ使用（nav, main, article, section, aside）
- **ARIA属性**: インタラクティブ要素のラベル
- **キーボード操作**: フォーカス管理、Tab順序
- **カラーコントラスト**: ダーク/ライトモード両方での可読性

#### 3-6. テスト・Storybook

- **Storybookカバレッジ**: `*.stories.tsx` の有無。UIコンポーネントにStorybookがあるか
- **テストの品質**: モックの適切さ、エッジケースのカバー

### Step 4: レポート出力

以下の形式でレポートを出力する:

```markdown
# コード品質レビュー結果

## サマリー
- 対象: {スコープ}
- ファイル数: {N}
- 検出問題数: Critical {n} / Warning {n} / Info {n}

## 静的解析結果
- TypeScript: {結果}
- ESLint: {結果}

## Critical（即座に修正が必要）
### [{カテゴリ}] {問題タイトル}
- ファイル: `{path}:{line}`
- 問題: {説明}
- 修正案: {具体的な修正方法}

## Warning（改善推奨）
...

## Info（検討事項）
...

## 良い実践（継続すべき点）
- {ポジティブな発見}

## 次のアクション
1. {優先順位付きの改善タスク}
```

### Step 5: 修正の提案

- Critical は具体的なコード修正案を提示する
- Warning は修正するかどうかユーザーに確認する
- 自動修正可能な問題（未使用インポート等）はまとめて修正を提案する

## 重大度の定義

| レベル | 基準 | 例 |
|---|---|---|
| **Critical** | セキュリティリスク、ビルド失敗、データ損失の可能性 | XSS脆弱性、型エラー、APIの認証欠如 |
| **Warning** | パフォーマンス劣化、保守性低下、ベストプラクティス違反 | 不要なClient Component、バンドル肥大化、any型 |
| **Info** | 改善の余地あり、将来的なリスク | Storybook未作成、命名の一貫性、コメント不足 |

## doboku-note 固有の注意点

- `images.unoptimized: true` は意図的（R2配信）。これを問題として報告しない
- `content/site/` 配下のMDXコンテンツはこのスキルの対象外（`/check-mdx` を使う）
- Cloudflare Pagesデプロイのため、Node.js固有APIの使用は要注意
- KaTeX はクライアントサイドレンダリング。SSR不可は既知
- Analytics のスクリプト挿入パターンは現行を尊重する

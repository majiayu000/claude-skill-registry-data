---
name: designing-ui
description: ユーザーインターフェースの設計とコンポーネント設計を支援します。ワイヤーフレーム、レイアウト設計、デザインシステム構築、レスポンシブデザイン、インタラクションパターンを提供します。美しく機能的で実装可能なインターフェース設計が必要な場合に使用してください。
---

# UIデザイン設計

## 概要

単に美しいだけでなく、迅速な開発サイクルで実装可能なUIを設計するスキルです。モダンなデザイントレンド、プラットフォーム固有のガイドライン、コンポーネント設計、革新と使いやすさの微妙なバランスに精通しています。

## 実行フロー

### Step 1: ワイヤーフレームと情報アーキテクチャ

#### ワイヤーフレームの作成

**目的:**

- 目的に沿った情報設計とセクション配置の提案
- ナビゲーション/CTA/フォームなど主要要素の配置設計
- ブレークポイント別のレイアウト案作成
- ユーザーフローと画面遷移の整理
- 注釈付きワイヤーで意図や状態を明確化

**成果物:**

```markdown
## [ページ名] ワイヤーフレーム

### レイアウト構造（デスクトップ）
┌─────────────────────────────────────┐
│ [Header]                            │
│ Logo | Nav | Search | User Menu     │
├─────────────────────────────────────┤
│ [Hero Section]                      │
│ H1: メインメッセージ                │
│ Subheading                          │
│ [Primary CTA] [Secondary CTA]       │
├─────────────────────────────────────┤
│ [Main Content]                      │
│ ┌───────┐ ┌───────┐ ┌───────┐     │
│ │Card 1 │ │Card 2 │ │Card 3 │     │
│ └───────┘ └───────┘ └───────┘     │
└─────────────────────────────────────┘

### レスポンシブ対応（モバイル）
- Header: ハンバーガーメニュー化
- Hero: 1カラムレイアウト
- Cards: スタック配置
```

#### 情報設計の原則

**視線の流れ:**

- F字パターン（テキスト重視）
- Z字パターン（ビジュアル重視）
- グーテンベルク図（斜め読み）

**優先度の視覚化:**

- サイズと位置で重要度を表現
- カラーとコントラストで注意を誘導
- 余白で要素をグループ化

### Step 2: レイアウトとグリッド設計

#### グリッドシステム

**12カラムグリッド（推奨）:**

```css
/* コンテナ */
.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* グリッド */
.grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 1.5rem;
}

/* レスポンシブ例 */
.col-span-4 {
  grid-column: span 4; /* デスクトップ: 3カラム */
}

@media (max-width: 768px) {
  .col-span-4 {
    grid-column: span 12; /* モバイル: 1カラム */
  }
}
```

#### スペーシングシステム

**4px/8pxグリッド:**

```css
/* Tailwindベースのスペーシング */
--spacing-1:  0.25rem;  /* 4px  - タイト */
--spacing-2:  0.5rem;   /* 8px  - 小 */
--spacing-4:  1rem;     /* 16px - 中（標準） */
--spacing-6:  1.5rem;   /* 24px - セクション間 */
--spacing-8:  2rem;     /* 32px - 大 */
--spacing-12: 3rem;     /* 48px - ヒーロー */
--spacing-16: 4rem;     /* 64px - 特大 */
```

**スペーシングルール:**

- 関連要素: 小さい余白（4-8px）
- セクション内: 中程度の余白（16-24px）
- セクション間: 大きい余白（32-64px）

### Step 3: タイポグラフィ設計

#### フォント選定

**推奨フォントペアリング:**

| 用途 | 組み合わせ | 特徴 |
|------|------------|------|
| モダン・ミニマル | Inter | クリーンで読みやすい |
| エレガント | Playfair Display + Lato | セリフ×サンセリフ |
| テック系 | Space Grotesk + IBM Plex Sans | 技術的で信頼感 |
| ビジネス | Roboto + Open Sans | 汎用性高い |

#### タイプスケール（モバイルファースト）

```css
/* モバイル */
--text-xs:   0.75rem;  /* 12px - キャプション */
--text-sm:   0.875rem; /* 14px - セカンダリ */
--text-base: 1rem;     /* 16px - 本文 */
--text-lg:   1.125rem; /* 18px - 強調本文 */
--text-xl:   1.25rem;  /* 20px - H3 */
--text-2xl:  1.5rem;   /* 24px - H2 */
--text-3xl:  1.875rem; /* 30px - H1 */
--text-4xl:  2.25rem;  /* 36px - Display */

/* デスクトップ（やや大きく） */
@media (min-width: 768px) {
  --text-3xl: 2.25rem;  /* 36px */
  --text-4xl: 3rem;     /* 48px */
  --text-5xl: 3.75rem;  /* 60px */
}
```

#### タイポグラフィのルール

**行間（Line Height）:**

- 見出し: 1.2-1.3
- 本文: 1.5-1.7
- キャプション: 1.4

**字間（Letter Spacing）:**

- 大文字見出し: 0.05em（広め）
- 通常: 0（デフォルト）
- 小さい文字: 0.01em（やや広め）

### Step 4: カラーシステム

#### カラーパレット設計

**プライマリカラー（50-900の階調）:**

```css
/* 例: Blueパレット */
--color-primary-50:  #eff6ff;
--color-primary-100: #dbeafe;
--color-primary-200: #bfdbfe;
--color-primary-300: #93c5fd;
--color-primary-400: #60a5fa;
--color-primary-500: #3b82f6;  /* ベースカラー */
--color-primary-600: #2563eb;
--color-primary-700: #1d4ed8;
--color-primary-800: #1e40af;
--color-primary-900: #1e3a8a;
```

#### セマンティックカラー

```css
/* 成功 */
--color-success: #10b981;

/* 警告 */
--color-warning: #f59e0b;

/* エラー */
--color-error: #ef4444;

/* 情報 */
--color-info: #3b82f6;

/* ニュートラル（グレースケール） */
--color-gray-50:  #f9fafb;
--color-gray-500: #6b7280;
--color-gray-900: #111827;
```

#### アクセシビリティ確保

**WCAGコントラスト比:**

- AA基準（最低要件）: 通常テキスト 4.5:1、大テキスト 3:1
- AAA基準（推奨）: 通常テキスト 7:1、大テキスト 4.5:1

**チェックツール:**

- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- Chrome DevTools: Accessibility Pane

### Step 5: コンポーネント設計

#### コンポーネントの状態定義

**必須ステート:**

```markdown
## ボタンコンポーネント

### 状態一覧
- [ ] Default（初期状態）
- [ ] Hover（マウスオーバー）
- [ ] Focus（キーボードフォーカス）
- [ ] Active（クリック中）
- [ ] Disabled（無効）
- [ ] Loading（読み込み中）

### バリエーション
- Primary（主要アクション）
- Secondary（補助アクション）
- Outline（枠線のみ）
- Ghost（背景透明）
- Danger（削除など危険な操作）

### サイズ
- Small (32px height)
- Medium (40px height) - デフォルト
- Large (48px height)
```

#### コンポーネントライブラリ構成

**基本コンポーネント:**

- Button
- Input / Textarea
- Select / Dropdown
- Checkbox / Radio
- Toggle / Switch
- Badge / Tag
- Avatar
- Icon

**複合コンポーネント:**

- Card
- Modal / Dialog
- Dropdown Menu
- Tabs
- Accordion
- Navigation Bar
- Breadcrumb
- Pagination

### Step 6: レスポンシブデザイン

#### ブレークポイント

```css
/* Tailwindベースのブレークポイント */
--breakpoint-sm: 640px;   /* モバイル（横） */
--breakpoint-md: 768px;   /* タブレット */
--breakpoint-lg: 1024px;  /* ラップトップ */
--breakpoint-xl: 1280px;  /* デスクトップ */
--breakpoint-2xl: 1536px; /* 大型デスクトップ */
```

#### レスポンシブ戦略

**モバイルファースト:**

```css
/* ベーススタイル（モバイル） */
.card {
  width: 100%;
  padding: 1rem;
}

/* タブレット以上 */
@media (min-width: 768px) {
  .card {
    width: 50%;
    padding: 1.5rem;
  }
}

/* デスクトップ以上 */
@media (min-width: 1024px) {
  .card {
    width: 33.333%;
    padding: 2rem;
  }
}
```

**コンテナクエリ（モダンアプローチ）:**

```css
/* コンポーネント自身のサイズに応じて変化 */
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    display: flex;
    flex-direction: row;
  }
}
```

### Step 7: インタラクションとアニメーション

#### マイクロインタラクション

**トランジション設定:**

```css
/* イージング関数 */
--ease-in:     cubic-bezier(0.4, 0, 1, 1);
--ease-out:    cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);

/* デュレーション */
--duration-fast:   150ms;  /* 素早い（ホバー等） */
--duration-base:   200ms;  /* 標準 */
--duration-slow:   300ms;  /* ゆっくり */
--duration-slower: 500ms;  /* 特別な演出 */
```

**アニメーション例:**

```css
/* ボタンホバー */
.button {
  transition: all var(--duration-base) var(--ease-out);
}

.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* ローディングスピナー */
@keyframes spin {
  to { transform: rotate(360deg); }
}

.spinner {
  animation: spin 1s linear infinite;
}
```

### Step 8: デザイントークン

#### トークン定義（Design Tokens）

**JSON形式:**

```json
{
  "color": {
    "primary": {
      "500": { "value": "#3b82f6" }
    }
  },
  "spacing": {
    "4": { "value": "1rem" }
  },
  "fontSize": {
    "base": { "value": "1rem" },
    "lg": { "value": "1.125rem" }
  },
  "borderRadius": {
    "md": { "value": "0.375rem" }
  }
}
```

**CSS Variables（実装）:**

```css
:root {
  /* Colors */
  --color-primary-500: #3b82f6;

  /* Spacing */
  --spacing-4: 1rem;

  /* Typography */
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;

  /* Border Radius */
  --radius-md: 0.375rem;
}
```

### Step 9: プラットフォーム別ガイドライン

#### iOS（Human Interface Guidelines）

**特徴:**

- SF Pro / SF Compactフォント
- 最小タップターゲット: 44×44pt
- iOS標準コンポーネントの尊重
- ジェスチャー: スワイプ、ピンチ、長押し

#### Android（Material Design）

**特徴:**

- Robotoフォント
- 最小タップターゲット: 48×48dp
- Elevation（影）でUIの階層を表現
- FAB（Floating Action Button）の活用

#### Web（レスポンシブ）

**特徴:**

- システムフォントスタック
- 最小タップターゲット: 48×48px
- ホバー状態の明示
- キーボードナビゲーション対応

### Step 10: デザインハンドオフ

#### 開発者向け仕様書

**コンポーネント仕様:**

```markdown
## Button Component

### Props
- variant: 'primary' | 'secondary' | 'outline'
- size: 'sm' | 'md' | 'lg'
- disabled: boolean
- loading: boolean

### Styles
- Height: 40px (md), 32px (sm), 48px (lg)
- Padding: 0 1rem
- Border Radius: 0.375rem
- Font Weight: 500

### Colors (Primary)
- Background: var(--color-primary-500)
- Text: white
- Hover: var(--color-primary-600)
- Active: var(--color-primary-700)
- Disabled: var(--color-gray-300)

### Accessibility
- aria-label or text content required
- Focus visible outline
- Keyboard accessible (Enter, Space)
```

#### アセット準備

**画像:**

- SVG: アイコン、ロゴ（スケーラブル）
- WebP/AVIF: 写真（次世代フォーマット）
- 2x/3x: Retina対応

**アイコンシステム:**

- 推奨: Heroicons, Lucide, Phosphor Icons
- サイズ: 16px, 20px, 24px, 32px
- 形式: SVG（インライン化推奨）

## 出力成果物

1. **ワイヤーフレーム**: 主要ブレークポイント別のレイアウト案
2. **デザインシステムドキュメント**: カラー、タイポグラフィ、スペーシングのルール
3. **コンポーネントライブラリ**: 全状態を含むコンポーネント仕様
4. **デザイントークン**: JSON/CSS Variables形式
5. **インタラクティブプロトタイプ**: 主要フローの動作確認
6. **開発者向け実装ノート**: Tailwindクラス、CSS仕様
7. **アニメーション仕様**: トランジション、イージング、デュレーション

## ベストプラクティス

1. **Simplicity First**: 複雑なデザインは実装に時間がかかる
2. **Component Reuse**: 一度設計したらどこでも使う
3. **Standard Patterns**: ありふれたインタラクションは再発明しない
4. **Progressive Enhancement**: コア体験を優先し、後で楽しさを足す
5. **Performance Conscious**: 美しく軽量に
6. **Accessibility Built-in**: 最初からWCAG準拠

## 実装スピードアップのヒント

**活用すべきツール:**

- **Tailwind UI**: 高品質なコンポーネントテンプレート
- **Shadcn/ui**: カスタマイズ可能なコンポーネントライブラリ
- **Heroicons**: 統一感のあるアイコンセット
- **Radix UI**: アクセシブルなプリミティブコンポーネント
- **Framer Motion**: プリセットアニメーション

## CSS Knowledge Reference

モダンCSS技術を活用したデザイン実装時は `managing-frontend-knowledge` スキルを使用してナレッジベースを参照できます。

**注意:** ナレッジは参考情報であり、古い・不足している場合があります。最新情報はContext7やMDN等で確認してください。JavaScript不要で実現できるUIパターン（アコーディオン、ポップオーバー等）はCSS実装を優先的に検討してください。

## 関連スキル

- **designing-brand**: ブランドレベルのデザインシステム（カラーパレット、タイポグラフィ基礎）
- **developing-frontend**: UI実装への橋渡し（React/Vue/Tailwind実装）
- **working-with-figma**: Figmaデザインデータの実装支援
- **managing-frontend-knowledge**: CSS/JS技術の最新情報参照
- **auditing-accessibility**: アクセシビリティ監査と改善

## スキル選択ガイド

作業内容に応じて、適切なスキルを選択してください。

### UIデザインワークフロー別の推奨スキル

| 作業フェーズ | 主スキル | 補助スキル | 出力 |
|------------|---------|----------|------|
| **1. ブランド基盤構築** | designing-brand | - | カラーパレット、タイポグラフィ、ロゴ |
| **2. ワイヤーフレーム作成** | designing-ui | - | 画面構成、レイアウト案 |
| **3. デザインシステム設計** | designing-brand + designing-ui | - | デザイントークン、コンポーネントライブラリ |
| **4. UI実装** | developing-frontend | designing-ui, managing-frontend-knowledge | React/Vue/Tailwindコード |
| **5. Figmaからの実装** | working-with-figma | designing-ui, developing-frontend | コンポーネントコード |
| **6. アクセシビリティ監査** | auditing-accessibility | designing-ui | WCAG準拠レポート |

### 作業内容別のスキル選択

#### デザイン設計フェーズ

| やりたいこと | 推奨スキル | 理由 |
|------------|-----------|------|
| ブランドカラー・ロゴを決めたい | **designing-brand** | ブランドアイデンティティの確立が主目的 |
| 画面のワイヤーフレームを描きたい | **designing-ui** | 情報設計とレイアウトが主目的 |
| コンポーネントの状態を定義したい | **designing-ui** | UIコンポーネントの詳細設計が主目的 |
| デザイントークンを作りたい | **designing-brand** → **designing-ui** | まずブランド基盤、次にUI実装用トークン |

#### 実装フェーズ

| やりたいこと | 推奨スキル | 理由 |
|------------|-----------|------|
| CSS/Tailwindの最新技術を知りたい | **managing-frontend-knowledge** | 技術情報参照が主目的 |
| React/Vueでコンポーネント実装したい | **developing-frontend** | コード記述が主目的 |
| Figmaデザインをコード化したい | **working-with-figma** | Figmaデータの活用が主目的 |
| CSSアニメーションを実装したい | **developing-frontend** + **managing-frontend-knowledge** | 実装＋最新技術情報 |

#### 品質保証フェーズ

| やりたいこと | 推奨スキル | 理由 |
|------------|-----------|------|
| WCAGアクセシビリティをチェックしたい | **auditing-accessibility** | a11y監査が主目的 |
| デザインシステムの一貫性を検証したい | **designing-ui** | コンポーネント設計の見直し |
| レスポンシブ対応を確認したい | **designing-ui** + **developing-frontend** | 設計＋実装の両面確認 |

### スキル組み合わせパターン

#### パターン1: ゼロからのUIデザイン

```
1. designing-brand（ブランド基盤）
   ↓ カラーパレット、タイポグラフィ確立
2. designing-ui（UI設計）
   ↓ ワイヤーフレーム、コンポーネント設計
3. developing-frontend（実装）
   ↓ React/Tailwindコード記述
4. auditing-accessibility（品質保証）
   ↓ WCAG準拠確認
```

#### パターン2: Figmaデザインの実装

```
1. working-with-figma（デザイン取得）
   ↓ Figmaからデザインデータ抽出
2. designing-ui（実装仕様作成）
   ↓ コンポーネント仕様、デザイントークン
3. developing-frontend（実装）
   ↓ コード記述
```

#### パターン3: 既存UIの改善

```
1. auditing-accessibility（現状評価）
   ↓ 問題点の特定
2. designing-ui（改善設計）
   ↓ 新しいUI設計
3. developing-frontend（実装）
   ↓ 改善コードの適用
```

### よくある質問

**Q: デザインブランドとUIデザインの違いは？**

- **designing-brand**: ブランド全体のビジュアルアイデンティティ（カラーシステム、タイポグラフィ基礎、ロゴ）
- **designing-ui**: 個別画面・コンポーネントの設計（ワイヤーフレーム、レイアウト、インタラクション）

**Q: CSS実装情報はどのスキルを使えばいい？**

- **最新技術を調べる**: managing-frontend-knowledge（情報参照）
- **実装コードを書く**: developing-frontend（コーディング）
- **設計仕様を作る**: designing-ui（仕様定義）

**Q: Figmaデザインの実装にはどのスキルが必要？**

1. working-with-figma（Figmaデータ取得）
2. designing-ui（実装仕様の補完）
3. developing-frontend（コード実装）

## クイックリファレンス

### Typography Scale (Mobile-first)

```
Display: 36px/40px - ヒーロー見出し
H1: 30px/36px - ページタイトル
H2: 24px/32px - セクション見出し
H3: 20px/28px - カードタイトル
Body: 16px/24px - 標準テキスト
Small: 14px/20px - セカンダリテキスト
Tiny: 12px/16px - キャプション
```

### Spacing System (Tailwind-based)

```
0.25rem (4px)  - タイトな余白
0.5rem  (8px)  - 小
1rem    (16px) - 中（標準）
1.5rem  (24px) - セクション間
2rem    (32px) - 大
3rem    (48px) - ヒーロー
```

### Component State Checklist

- [ ] Default state
- [ ] Hover/Focus states
- [ ] Active/Pressed state
- [ ] Disabled state
- [ ] Loading state
- [ ] Error state
- [ ] Empty state
- [ ] Dark mode variant (必要に応じて)

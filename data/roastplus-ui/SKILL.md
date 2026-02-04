---
name: roastplus-ui
description: ローストプラスアプリのUIデザインシステム。Tailwind CSS v4ベースの配色、コンポーネントパターン、レイアウト、アニメーションを提供。新規ページ作成、コンポーネント実装、デザイン一貫性チェックに使用。通常モードとクリスマスモードの両方に対応。
usage: "/roastplus-ui"
version: 1.0.0
---

# ローストプラス UIデザインシステム

## イントロダクション

このスキルは、ローストプラスアプリケーションの統一されたUIデザインパターンを提供します。

**デザインの哲学:**
- **高級感**: コーヒーの焙煎という専門的で高級な活動を表現
- **親しみやすさ**: 温かみのあるオレンジと黒を基調とした色選び
- **使いやすさ**: 最小タッチサイズ44px、レスポンシブデザイン、アクセシビリティ対応

**特徴:**
- Tailwind CSS v4ベースで、ユーティリティクラス中心の実装
- ブランドカラーは「コーヒーのオレンジ」（#EF8A00）と「焙煎時の黒褐色」（#211714）
- アニメーションとトランジションで高級感を演出
- 通常モードとクリスマスモードの2つのテーマに対応

---

## クイックスタート

### 1. 新規ページを作成する（3ステップ）

**ステップ1: ページタイプを決める**
- フル画面レイアウト（タイマー、スケジュール系）
- スクロール可能レイアウト（リスト、記録系）
- フォームレイアウト（設定、入力系）

**ステップ2: テンプレートを使用**

```tsx
'use client';

import Link from 'next/link';
import { useAuth } from '@/lib/auth';
import { HiArrowLeft } from 'react-icons/hi';
import { Loading } from '@/components/Loading';
import { useAppLifecycle } from '@/hooks/useAppLifecycle';
import LoginPage from '@/app/login/page';

export default function YourPageName() {
  const { user, loading: authLoading } = useAuth();
  useAppLifecycle();

  if (authLoading) return <Loading />;
  if (!user) return <LoginPage />;

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#F7F7F5' }}>
      <div className="container mx-auto px-4 sm:px-6 py-4 sm:py-6 max-w-4xl">
        {/* ヘッダー */}
        <header className="mb-6 sm:mb-8">
          <div className="flex items-center gap-4">
            <Link
              href="/"
              className="px-3 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded transition-colors flex items-center justify-center min-h-[44px] min-w-[44px]"
              aria-label="戻る"
            >
              <HiArrowLeft className="h-6 w-6" />
            </Link>
            <h1 className="text-2xl font-bold text-gray-800">ページタイトル</h1>
          </div>
        </header>

        {/* メインコンテンツ */}
        <main className="bg-white rounded-lg shadow-md p-6">
          {/* ここにコンテンツを配置 */}
        </main>
      </div>
    </div>
  );
}
```

**ステップ3: コンポーネントを追加**

詳細は「コアコンポーネントパターン」セクションを参照してください。

---

## 配色スキーム

ローストプラスの配色は、コーヒーの世界からインスパイアされています。

### ブランドカラー

| 名称 | 16進数 | 用途 | Tailwindクラス |
|------|--------|------|----------------|
| Primary Orange | `#EF8A00` | メインアクション、アイコン | `primary` / `amber-600` |
| Dark Orange | `#D67A00` | ホバー、強調 | `primary-dark` / `amber-700` |
| Light Orange | `#FF9A1A` | 明るいアクセント | `primary-light` / `amber-500` |
| Dark Brown | `#211714` | ヘッダー、濃い背景 | `dark` |
| Light Brown | `#3A2F2B` | テキスト、枠線 | `dark-light` |
| Gold | `#FFC107` / `#d4af37` | 高級感演出 | `gold` |
| Background | `#FDF8F0` | ページ背景 | `bg-white/95` |

### 通常モード（デフォルト）

```tsx
// 背景
<div className="bg-gradient-to-b from-[#F7F2EB] to-[#F3F0EA]">

// テキスト
<span className="text-[#1F2A44]">

// ボタン
<button className="bg-amber-600 text-white hover:bg-amber-700">
```

### クリスマスモード

```tsx
// 背景
<div className="bg-[#051a0e] bg-[radial-gradient(circle_at_center,_#0a2f1a_0%,_#051a0e_100%)]">

// テキスト
<span className="text-[#f8f1e7]">

// アクセント
<div className="border-[#d4af37]/40">
```

詳細は **color-schemes.md** を参照してください。

---

## コアコンポーネントパターン

### ボタン

**プライマリボタン**
```tsx
<button className="px-6 py-3 bg-amber-600 text-white rounded-lg font-semibold hover:bg-amber-700 transition-colors min-h-[44px]">
  アクション
</button>
```

**グラデーションボタン（高級感演出）**
```tsx
<button className="bg-gradient-to-r from-amber-500 to-amber-600 text-white rounded-xl font-bold shadow-lg hover:shadow-xl hover:from-amber-600 hover:to-amber-700 active:scale-[0.98] transition-all">
  プレミアムアクション
</button>
```

**アウトラインボタン**
```tsx
<button className="border-2 border-amber-200 text-amber-700 bg-gradient-to-r from-amber-50 to-amber-100 rounded-xl font-bold hover:from-amber-100 hover:to-amber-200">
  サブアクション
</button>
```

### 入力フィールド

**テキスト入力**
```tsx
<input
  type="text"
  className="w-full rounded-lg border-2 border-gray-200 px-4 py-3.5 text-lg text-gray-900 bg-white focus:border-amber-500 focus:outline-none focus:ring-2 focus:ring-amber-100 transition-all"
  placeholder="入力してください"
/>
```

**セレクトボックス**
```tsx
<select className="w-full rounded-md border border-gray-300 px-4 py-2.5 text-lg text-gray-900 bg-white focus:border-amber-500 focus:outline-none focus:ring-2 focus:ring-amber-500 min-h-[44px]">
  <option>選択してください</option>
</select>
```

### カード

**基本カード**
```tsx
<div className="bg-white rounded-2xl shadow-md p-5 hover:shadow-lg hover:-translate-y-1 transition-all cursor-pointer">
  <h3 className="text-lg font-bold text-gray-800 mb-2">タイトル</h3>
  <p className="text-gray-600">説明文</p>
</div>
```

**ホームページスタイルカード**
```tsx
<button className="group relative flex flex-col items-center justify-center gap-3 rounded-2xl p-5 shadow-2xl transition-all hover:-translate-y-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary bg-white/95 text-[#1F2A44] hover:shadow-[0_16px_40px_rgba(0,0,0,0.08)]">
  <span className="flex h-14 w-14 items-center justify-center rounded-full bg-primary/10 text-primary">
    <FaIcon className="h-8 w-8" />
  </span>
  <div className="text-center">
    <p className="font-bold text-base">カードタイトル</p>
    <p className="text-xs text-slate-500">説明</p>
  </div>
</button>
```

### モーダル/ダイアログ

**基本モーダル**
```tsx
<div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
  <div className="bg-white rounded-lg shadow-xl p-6 sm:p-8 max-w-md w-full mx-4">
    <h2 className="text-2xl font-bold text-gray-800 mb-4">タイトル</h2>
    <p className="text-gray-600 mb-6">メッセージ</p>
    <div className="flex gap-4 justify-end">
      <button className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors min-h-[44px]">
        キャンセル
      </button>
      <button className="px-6 py-3 bg-amber-600 text-white rounded-lg hover:bg-amber-700 transition-colors min-h-[44px]">
        確認
      </button>
    </div>
  </div>
</div>
```

詳細は **components.md** を参照してください。

---

## レイアウトパターン

### ページレイアウトタイプ

**スクロール可能レイアウト（推奨）**
```tsx
<div className="min-h-screen" style={{ backgroundColor: '#F7F7F5' }}>
  <div className="container mx-auto px-4 sm:px-6 py-4 sm:py-6 max-w-4xl">
    {/* コンテンツ */}
  </div>
</div>
```

**フル画面レイアウト（タイマー系）**
```tsx
<div className="h-screen flex flex-col bg-white overflow-hidden">
  <header className="flex-shrink-0 border-b">ヘッダー</header>
  <main className="flex-1 flex flex-col min-h-0 overflow-y-auto">
    {/* コンテンツ */}
  </main>
</div>
```

### スペーシングルール

```
外側余白（コンテナ）:
- モバイル: px-4 py-4
- タブレット: sm:px-6 sm:py-6
- デスクトップ: lg:px-8 lg:py-8

内部ギャップ:
- 要素間: gap-3
- 大画面: md:gap-4

セクション間:
- 小: mb-4
- 中: mb-6
- 大: mb-8
```

### 最大幅設定

```
max-w-6xl - ホームページ（広幅）
max-w-4xl - 標準ページ
max-w-2xl - フォーム、設定（狭幅）
```

詳細は **layouts.md** を参照してください。

---

## アニメーション

### グローバルアニメーション

| 名称 | 用途 | 持続時間 |
|------|------|---------|
| `pulse-scale` | New!ラベルのパルス | 2s無限 |
| `gradient-shift` | グラデーション背景の流動 | 3s無限 |
| `home-slide-in` | ページ全体のスライドイン | 0.55s |
| `home-card-appear` | カードの順次出現 | 0.48s |

### よく使うトランジション

```tsx
// カラーチェンジ
className="transition-colors duration-200"

// すべての変更
className="transition-all duration-300"

// ホバーリフト
className="hover:-translate-y-2 transition-all"

// スケール変化
className="hover:scale-105 transition-transform"
```

詳細は **animations.md** を参照してください。

---

## ベストプラクティス

### アクセシビリティ

✅ **守るべきこと:**
- すべてのタッチターゲット: 最小 `min-h-[44px]`
- フォーカスリング: `focus-visible:ring-2`
- ARIA属性: `aria-label`, `aria-hidden` を適切に使用
- キーボード操作: Escapeで閉じる（モーダル）

### レスポンシブデザイン

**ブレークポイント:**
- `sm:` - 640px以上（タブレット）
- `md:` - 768px以上（小型デスクトップ）
- `lg:` - 1024px以上（大型デスクトップ）

**モバイルファースト設計:**
```tsx
// ❌ 悪い例
className="text-3xl md:text-2xl sm:text-xl"

// ✅ 良い例
className="text-sm sm:text-base md:text-lg"
```

### クリスマスモード対応

```tsx
const { isChristmasMode } = useChristmasMode();

<div className={`${isChristmasMode ? 'クリスマス用クラス' : '通常用クラス'}`}>
```

---

## AI Assistant Instructions

このスキルが `/roastplus-ui` で起動された際の動作を以下に示します。

### 初期フロー

ユーザーが `/roastplus-ui` を実行すると、以下の質問が表示されます：

**「何をお手伝いしますか？」**
- 新規ページを作成したい
- コンポーネントを実装したい
- デザイン一貫性をチェックしたい

### 新規ページ作成時

1. **ページタイプを確認**: フル画面 / スクロール可能 / フォーム
2. **テンプレートを提供**: `examples/page-template.tsx` を基に適切な実装例を提示
3. **コンポーネントパターンを提示**: 必要なコンポーネント（ボタン、入力フィールド等）を `components.md` から選択
4. **クリスマスモード対応を確認**: 必要な場合は両モード対応コードを提供
5. **完全な実装コードを生成**: ページの完全な構造を提供

### コンポーネント実装時

1. `components.md` から該当パターンを検索
2. 通常モードとクリスマスモードの両バリエーションを提供
3. アクセシビリティチェックポイント（最小タッチサイズ、カラーコントラスト等）を明示
4. コピーペースト可能なコードスニペットを提供

### デザイン一貫性チェック時

提供されたファイルを読み取り、以下を確認：

- [ ] 配色が `color-schemes.md` に準拠しているか
- [ ] タッチターゲットがすべて44px以上か
- [ ] レスポンシブブレークポイント（sm:, md:, lg:）が正しく使用されているか
- [ ] アニメーション使用時に `prefers-reduced-motion` を考慮しているか
- [ ] クリスマスモード対応が必要な場合は両モード実装されているか

チェック結果に基づいて改善提案を提示します。

### 常に守るべきルール

**UI実装時:**
- 新しいパターンを作る前に、既存パターン（components.md）で対応できないか確認
- 最小タッチサイズ44pxを常に確保
- カラーコントラスト比に配慮
- すべての入力フィールドにラベルを付与
- モーダルはEscapeキーで閉じられるようにする

**レスポンシブデザイン時:**
- モバイルファーストで設計
- sm:, md:, lg: ブレークポイントを活用
- 画像やアイコンをレスポンシブに調整

**パフォーマンス時:**
- アニメーション使用時は `will-change` を明記
- `prefers-reduced-motion` でアニメーション無効化に対応

---

## 関連ドキュメント

- **color-schemes.md** - 詳細な配色スキーム、配色切り替え実装
- **components.md** - 全コンポーネントパターン（ボタン、カード、モーダル等）
- **layouts.md** - レイアウトパターン、スペーシングルール、最大幅設定
- **animations.md** - アニメーション実装、Framer Motion使用例
- **examples/** - 実装テンプレート（page, modal, card）

---

## 更新履歴

### v1.0.0 (2026-01-15)
- 初回リリース
- 通常モード、クリスマスモード対応
- コアコンポーネントパターン完備
- レイアウト、アニメーションガイドラインを掲載

---
name: design-review
description: >
  デザインシステム準拠を 7 カテゴリ・重大度判定でレビューする統合スキル。
  `.tsx` ファイルは `--visual` で Playwright 視覚検証（light/dark × desktop/mobile）＋ 静的 lint を追加実行。
  Use when user asks to [デザインレビュー, UI確認, 視覚検証, Playwright 確認, /design-review].
domain: site
---

CSS・MDX・TSXコンポーネントを doboku-note デザインシステムに照らしてレビューし、違反を検出・分類・修正提案する。`.tsx` では視覚回帰とデザイントークン準拠も検証可能（旧 `ui-visual-qa` エージェントの機能を統合）。

## 引数

```
$ARGUMENTS — レビュー対象のファイルパスまたはディレクトリ
             （例: src/styles/globals.css）
             （例: content/port/fishery-guideline/）
             （例: src/components/layout/）

--visual   — .tsx ファイルに対して Playwright 視覚検証を実行（dev server 必須）
```

## 手順

### Step 1: 対象特定

- ファイルパスが渡された場合: そのファイルを読み取る
- ディレクトリが渡された場合: 配下の `.mdx`, `.tsx`, `.css` ファイルを Glob で列挙し、全ファイルを対象とする
- 引数なしの場合: 直近の git diff で変更された `.mdx`, `.tsx`, `.css` ファイルを対象とする

### Step 2: リファレンス読み込み

以下を読み込む:

1. `.claude/knowledge/design-system/design-system.md` — デザイン単一 SSOT（トークン体系・レイアウト体系・記事 prose・5 原則・§8 禁止パターン）
2. `src/styles/globals.css` — 現行のスタイル定義（トークン値の真実源）

### Step 3: 7 カテゴリ走査

#### MDX ファイルの場合

1. **見出し構造**: h1→h2→h3→h4 の順序が正しいか、階層スキップがないか
2. **図・画像**: `className="center-image"` の使用、width 指定、alt 属性、キャプション（`text-center`）の有無
3. **表**: `table-title` と `table-wrapper` の使用、ヘッダーの有無
4. **数式**: `scroll-equation` で囲まれているか、`\tag{}` で番号付与されているか
5. **コンテンツ品質**: 不要な絵文字、AI 生成パターン（過剰な箇条書き、不要なまとめ）
6. **リンク**: リンクテキストが意味のある文言か
7. **アクセシビリティ**: img の alt、th の scope

#### CSS/TSX ファイルの場合

1. **カラー**: `color: black` / `#000` の使用、低コントラストの組み合わせ
2. **タイポグラフィ**: 日本語**本文**への負の letter-spacing（見出しの `-0.01em` は editorial 標準で可。`design-system.md` §4/§8）、font-weight: 300 以下、12px 以下のフォント
3. **スペーシング**: 見出し前後の余白不足、表の余白不足
4. **モーション**: 不要なアニメーション
5. **ボーダー**: 薄すぎるボーダー（`#eee` 等）
6. **レスポンシブ**: 固定幅の指定、モバイル未考慮
7. **アクセシビリティ**: outline: none、focus スタイルの欠如

### Step 4: 重大度判定

各違反に重大度を付与:

| 重大度 | 基準 | 例 |
|--------|------|---|
| Critical | アクセシビリティ違反・WCAG 不適合・情報の欠落 | alt 欠損、見出しスキップ、コントラスト不足 |
| High | 禁止パターンに明確に該当 | 不要な絵文字、AI 生成パターン、数式の scroll-equation 欠如 |
| Medium | 推奨パターンからの逸脱 | キャプション欠如、width 未指定、table-wrapper 未使用 |
| Low | 改善推奨だが機能に影響なし | 余白の不統一、スタイルの微細な不整合 |

### Step 5: レポート出力

```markdown
## デザインレビュー: {対象}

### サマリー
- Critical: N件
- High: N件
- Medium: N件
- Low: N件

### 違反一覧

#### Critical

| # | ファイル:行 | カテゴリ | 違反内容 | 修正案 |
|---|------------|---------|---------|--------|
| 1 | path:42 | 見出し構造 | h2 → h4 のスキップ | h3 を挿入 |

#### High
...

#### Medium
...

#### Low
...

### 良い点
- ...
```

## 注意

- 出力は保存しない。会話の中で直接表示する
- 修正案は具体的な className または MDX 記法で提示する
- **違反の検出は常に全件行う**。大量にある場合に絞るのは「表示」だけで、Critical / High を先に並べ、Low は末尾に一覧（件数＋対象）としてまとめる。検出段階で Low を切り捨てない
- MDX コンテンツの「原文の意味変更」は指摘しない（`/improve-article --mode verify` の管轄）

---

## --visual モード（.tsx 視覚検証）

`src/components/ui/**/*.tsx` の変更時に、**静的 lint（禁止パターン検出）＋ Playwright 視覚検証（light/dark × desktop/mobile）** を実行する。旧 `ui-visual-qa` エージェントの機能を統合。

### 設計原則

> **Generator と Evaluator を分離する**

UI コンポーネントを書く Generator（Claude Code 本体）と視覚回帰を検出する Evaluator を分離する。Generator は作った直後に自分の変更を「綺麗だ」と判断するバイアスを持つため、別プロセスで検証する。

### スコープ

**対象**:
- `src/components/ui/**/*.tsx`
- `src/styles/globals.css`（デザイントークン定義）の変更時

**対象外**:
- `.mdx` ファイル → `/improve-article --mode verify` で振り分け
- `src/lib/**/*.ts` → `/code-review` を使用

### 前提確認

- `npm run dev` が port 3020 で起動しているか（`curl -s -o /dev/null -w "%{http_code}" http://localhost:3020` が `200`）
- 起動していなければ「`/dev-start` を実行してください」と報告して中止

### 静的 lint（決定論的）

`node scripts/lint-ui.mjs` を変更ファイルに対して実行。以下を HIGH として報告:

- `border-gray-{100,200,300,...}` に `dark:border-*` が無い
- `rounded-{lg,xl,2xl,3xl}` + `shadow-*` の直書き（デザイントークン `rounded-card-*` / `shadow-card-*` を使うべき）
- `style={{ borderColor: ... }}` のインライン指定（`dark:` クラスを上書きするため禁止）

### 使用箇所の特定

各変更コンポーネントについて:

1. `Grep` で `<ComponentName` を `content/site/**/*.mdx` から検索（最大 3 件）
2. 使用箇所が見つからなければ `src/app/` 内で検索（代替）
3. どちらにも無ければ「使用箇所なし、視覚検証スキップ」と記録

### Playwright 視覚検証

各使用箇所 URL について、以下 4 パターンをスクショ取得:

| # | viewport | theme | セット |
|---|---|---|---|
| 1 | 1280×800 | light | Desktop Light |
| 2 | 1280×800 | dark | Desktop Dark |
| 3 | 375×812 | light | Mobile Light |
| 4 | 375×812 | dark | Mobile Dark |

**ダークモード切替**:
```js
await browser_evaluate({ function: "() => document.documentElement.classList.add('dark')" })
```
（next-themes は `class` モードで動作するため `html.dark` を直接追加）

**ライトに戻す**:
```js
await browser_evaluate({ function: "() => document.documentElement.classList.remove('dark')" })
```

スクショ保存先: `.tmp/design-review/<component-name>/{1-desktop-light,2-desktop-dark,3-mobile-light,4-mobile-dark}.png`

### 視覚判定

HIGH として報告:
- **ダークモードで背景がほぼ同色**（`html.dark` の本文 bg と card bg の差が <5% 程度の輝度差しかなく見えない）
- **ダークモードで border 線が消えた**（Desktop Dark で border が `html.dark` の bg 色と同じ）
- **Mobile で横スクロール発生**（body の `scrollWidth > clientWidth`）

MEDIUM:
- ホバー影が dark で過剰（`shadow-2xl` 直使用など）
- フォントサイズが Mobile で <12px

LOW:
- コントラスト比が WCAG AA を 10% 下回る（Desktop Light のみ軽量チェック）

### ルーブリック採点（--visual モードのみ）

| 軸 | 重み | 3点 | 2点 | 1点 | 0点 |
|---|---|---|---|---|---|
| **静的 lint 準拠** | 30% | lint-ui.mjs の違反ゼロ | 軽微な warn | HIGH 1件 | HIGH 2件以上 |
| **ダークモード視覚** | 30% | border/bg ともに視認可 | 軽微な視認低下 | border 1 箇所消失 | 2 箇所以上消失 |
| **Mobile レイアウト** | 20% | 375px で横スクロールなし | 軽微なハミ出し 1件 | 横スクロール 1件 | 横スクロール 2件以上 |
| **デザイントークン使用** | 15% | 全カードが rounded-card-* / shadow-card-* 使用 | 1 箇所で生値 | 2-3 箇所で生値 | 多数 |
| **アクセシビリティ** | 5% | alt / aria 指定あり、コントラスト AA | 軽微な欠落 | alt 欠落 1件 | 複数欠落 |

加重合計 = Σ(スコア × 重み) / 3
合格ライン: **2.0 / 3.0 以上**。いずれかの軸が 0 点なら即不合格。

### 出力フォーマット（--visual モード）

```
=== design-review --visual: <component-name>(s) ===
Changed: src/components/ui/Callout/Callout.tsx
Usage sample: /docs/pe-comprehensive-management-section-1

[静的 lint]
  ✓ dark:border: OK
  ✗ HIGH: L42 `rounded-xl shadow-md` 直書き → `rounded-card-content shadow-card-content` に置換

[Playwright スクショ]
  1. Desktop Light: .tmp/design-review/Callout/1-desktop-light.png
  2. Desktop Dark:  .tmp/design-review/Callout/2-desktop-dark.png
  3. Mobile Light:  .tmp/design-review/Callout/3-mobile-light.png
  4. Mobile Dark:   .tmp/design-review/Callout/4-mobile-dark.png

[視覚判定]
  HIGH: Dark モードで border 線が消失
  MEDIUM: Mobile Dark でフッター影が過剰

[ルーブリック]
  静的 lint 準拠: 1/3 (×0.30 = 0.10)
  ダークモード視覚: 1/3 (×0.30 = 0.10)
  Mobile レイアウト: 3/3 (×0.20 = 0.20)
  デザイントークン使用: 1/3 (×0.15 = 0.05)
  アクセシビリティ: 3/3 (×0.05 = 0.05)
  ─────────────────
  加重合計: 1.50 / 3.0 → ❌ 不合格（修正推奨）

[推奨修正]
1. Callout.tsx L42: `border-gray-200` に `dark:border-gray-700` を追加
2. Callout.tsx L42: `rounded-xl shadow-md` → `rounded-card-content shadow-card-content`
```

### アンチパターン

- 変更のない `.tsx` にスクショを撮らない — git diff で変更されたもののみ対象
- 全 MDX ページをスクショしない — 使用箇所 3 件まで
- 静的 lint で済む判定を Playwright に任せない — dark 欠落は lint-ui.mjs が検出できる
- スクショは `.tmp/` 配下のみ — git 追跡下に入れない
- dev server 未起動で強行しない — 必ず起動確認してから進む
- 修正まで実行しない — design-review は Evaluator 的役割、修正は呼び出し元（`/simplify` 等）が行う

### 参照

- `scripts/lint-ui.mjs` — 静的 lint の実装
- `src/styles/globals.css` — デザイントークン定義（`:root` の `--radius-card-*` / `--shadow-card-*`）
- `CLAUDE.md` — UI コンポーネント必須ルール（デザイントークン・ダークモード）

---
name: zenn-audit
description: >
  doboku-note の記事ページ（globals.css / page.tsx / tailwind.config.js）を Zenn 本番 CSS と比較し、タイポグラフィとレイアウトの drift を Critical / Warning / Matches / Intentional の 4 段階で報告する半年〜1年スパンの監査用途。日常レビュー（/review）とは独立した稀な drift 監査で、/review dispatcher には含まれない。
  Use when user asks to [Zenn 監査, Zenn 比較, タイポグラフィ監査, CSS drift チェック, /zenn-audit].
domain: ops
---

# /zenn-audit — Zenn準拠監査（タイポグラフィ + レイアウト）

## 概要

doboku-note の記事本文スタイル（`src/styles/globals.css`）と記事ページレイアウト（`src/app/docs/[...slug]/page.tsx` + `tailwind.config.js`）を **Zenn 本番CSSの最新値** と比較し、差分を **Critical / Warning / Matches / Intentional** の4段階で報告するスキル。

doboku-note は記事ページを Zenn 準拠としている。Zenn の CSS は時々更新され、doboku-note の globals.css / page.tsx / tailwind.config.js も時々触るため、半年〜1年スパンで drift が累積する。本スキルは手動比較（毎回60分以上）を自動化し、任意タイミングで確実に差分を検出できるようにする。

**監査対象**:
- **Typography**: globals.css `.prose-blog` 系ルール
- **Layout**: page.tsx のコンテナ/main/article/aside クラス、tailwind.config.js の screens

## 使い方

```
/zenn-audit
```

オプションなし。全カテゴリ（typography + layout）を比較する。

## 実行手順

### Step 1: Zenn の最新CSSをダウンロード

Zenn は Next.js アプリでハッシュ付きCSSバンドルを配信している。ハッシュは内容変更で変わるため、記事ページのHTMLから動的に抽出する。

```bash
# Zenn の代表記事から CSS リンクを抽出
curl -sL -A "Mozilla/5.0" "https://zenn.dev/zenn/articles/markdown-guide" -o /tmp/zenn.html
grep -oE 'href="https://static\.zenn\.studio/_next/static/css/[^"]+\.css"' /tmp/zenn.html \
  | head -10 | sed 's/href="//;s/"$//' > /tmp/zenn_css_urls.txt

# 各 CSS を取得
for url in $(cat /tmp/zenn_css_urls.txt); do
  curl -sL "$url" -o "/tmp/zenn_$(basename $url)"
done

# .znc（typography）を含む CSS と View_/Container_（layout）を含む CSS を特定
for f in /tmp/zenn_*.css; do
  if grep -q '\.znc' "$f"; then cp "$f" /tmp/zenn_typography.css; fi
  if grep -q 'View_columnsContainer\|Container_wide' "$f"; then cp "$f" /tmp/zenn_layout.css; fi
done
```

---

## Section A: Typography Audit

### Step 2: Zenn の重要値を抽出（タイポグラフィ）

以下の CSS プロパティを `.znc` 系ルールから `/tmp/zenn_typography.css` で抽出する。

| カテゴリ | セレクタ | プロパティ |
|---|---|---|
| Body | `.znc` | `line-height` |
| 段落 | `.znc p + p` | `margin-top` |
| リスト | `.znc ul`, `.znc ol` | `margin`, `line-height`, `padding-left` |
| リスト項目 | `.znc li` | `margin` |
| ネストリスト | `.znc ul ul`, `.znc ul ol` | `margin` |
| 見出し直後 | `.znc h1+p` 〜 `.znc h6+p` | `margin-top` |
| blockquote | `.znc blockquote` | `font-size`, `margin`, `border-left`, `padding` |
| table | `.znc table` | `font-size`, `line-height`, `margin` |
| code | `.znc code` | `font-size`, `padding` |
| hr | `.znc hr` | `margin` |
| link | `.znc a`, `.znc a:hover` | `color`, `text-decoration` |

抽出コマンド例:
```bash
grep -oE '\.znc\{[^}]*\}' /tmp/zenn_typography.css
grep -oE '\.znc p\+p\{[^}]*\}' /tmp/zenn_typography.css
grep -oE '\.znc ul[^{]*\{[^}]*\}|\.znc ol[^{]*\{[^}]*\}' /tmp/zenn_typography.css
grep -oE '\.znc h[1-6]\+p[^{]*\{[^}]*\}' /tmp/zenn_typography.css
grep -oE '\.znc blockquote\{[^}]*\}' /tmp/zenn_typography.css
```

### Step 3: doboku-note の現在値を抽出（タイポグラフィ）

`src/styles/globals.css` を Read し、`.prose-blog` 系ルールを読み取る。Tailwind の `@apply` ディレクティブは以下の換算表で px / rem に変換して比較する。

| Tailwind | 実値 |
|---|---|
| `mb-1` / `mt-1` | 0.25rem (4px) |
| `mb-2` / `mt-2` | 0.5rem (8px) |
| `mb-3` / `mt-3` | 0.75rem (12px) |
| `mb-4` / `mt-4` | 1rem (16px) |
| `mb-5` / `mt-5` | 1.25rem (20px) |
| `mb-6` / `mt-6` | 1.5rem (24px) |
| `mb-8` / `mt-8` | 2rem (32px) |
| `mb-10` / `mt-10` | 2.5rem (40px) |
| `mb-12` / `mt-12` | 3rem (48px) |
| `mb-16` / `mt-16` | 4rem (64px) |

---

## Section B: Layout Audit

### Step 4: Zenn の重要値を抽出（レイアウト）

`/tmp/zenn_layout.css` から以下のレイアウトルールを抽出する。

| カテゴリ | セレクタ | プロパティ |
|---|---|---|
| コンテナ幅 | `.Container_wide` | `max-width` |
| コンテナpadding | `.Container_common` + 全 `@media` | `padding` |
| カラム構造 | `.View_columnsContainer` + `@media` | `display`, `justify-content` |
| メインカラム幅 | `.View_content` + `@media` | `width` |
| サイドバー幅 | `.View_sidebarContainer` + `@media` | `width`, `display` |
| 記事カード | `.View_main` + `@media` | `border`, `border-radius`, `box-shadow`, `padding` |
| 記事タイトル | `.ArticleHeader_title` | `max-width`, `margin` |
| サイドバーsticky | `.ArticleSidebar_sticky` | `position`, `top` |
| html font-size | `html` + `@media` | `font-size` |
| ページbg padding | `.View_container` | `padding-bottom`, `border-top` |

抽出コマンド例:
```bash
grep -oE '\.Container_wide[^{]*\{[^}]*\}' /tmp/zenn_layout.css
grep -oE '\.Container_common[^{]*\{[^}]*\}' /tmp/zenn_layout.css
grep -oE '\.View_sidebarContainer[^{]*\{[^}]*\}' /tmp/zenn_layout.css
grep -oE '\.View_main[a-zA-Z_]*__[a-zA-Z0-9]+[^{]*\{[^}]*\}' /tmp/zenn_layout.css

# 全 media queries 内の Container_common / View_main / html
python -c "
import re
with open('/tmp/zenn_layout.css') as f:
    css = f.read()
for m in re.finditer(r'@media[^{]+\{(?:[^{}]|\{[^{}]*\})*\}', css):
    block = m.group(0)
    if 'Container_common' in block or 'View_main' in block or 'View_sidebarContainer' in block or 'html{' in block:
        print(block[:400])
        print()
"
```

### Step 5: doboku-note の現在値を抽出（レイアウト）

複数ファイルから値を抜き取る:

1. **`src/components/layout/TwoColumnShell.tsx`**（2カラムレイアウト値の真実源）を Read:
   - `max-w-\[(\d+)px\]` → コンテナ max-width
   - `<aside>` の幅ユーティリティ（現行 `w-[316px]`=316px） → サイドバー幅
   - `gap-(\d+)` または `gap-\[(\d+)px\]`（現行 `gap-10`=40px） → カラム間ギャップ
   - `zenn-desktop:block` → サイドバー可視化境界（≥993px）

2. **`src/app/docs/[...slug]/page.tsx`** を Read:
   - `<article>` の `rounded-`, `shadow-`, `py-`, `px-`, `zenn-desktop:px-`, `max-zenn-*:*` → カードデザイン（現行 `px-10` / `zenn-desktop:px-11` / `max-zenn-sp:px-[var(--article-gutter-sp)]`）
   - `pb-(\d+)` on `flex-grow` → ページ下部余白

3. **`tailwind.config.js`** を Read:
   - `extend.screens` → Zenn ブレイクポイント確認（`zenn-tiny` 401, `zenn-sp` 577, `zenn-tablet` 769, `zenn-desktop` 993）

4. **`src/styles/globals.css`** を Read:
   - `.prose-blog h1` → `max-width` 値
   - `--article-gutter-sp` → モバイル記事カード横 gutter（現行 16px・details のフルブリード相殺と連動）

### Step 6: レイアウト差分を分類

**🔴 Critical**: 読みやすさ・UXに直結
- container max-width ずれ
- sidebar visibility breakpoint ずれ
- card padding が極端にずれる
- mobile full-bleed 設定なし

**🟡 Warning**: 整合性
- sidebar width 10px以上ずれ
- gap ずれ
- container padding の段階ずれ
- card border-radius ずれ

**✅ Matches**: 値が一致

**⚪ Intentional**: `intentional-deviations.yml` に登録された項目

---

## Step 7: レポート出力

### 出力フォーマット

```markdown
# Zenn Audit Report

**実行日時**: {ISO timestamp}
**Zenn CSS source**: {url}
**doboku-note sources**:
- src/styles/globals.css
- src/app/docs/[...slug]/page.tsx
- tailwind.config.js

## サマリー
- 🔴 Critical: {n}
- 🟡 Warning: {n}
- ✅ Matches: {n}
- ⚪ Intentional: {n}

## Typography セクション

### 🔴 Critical Deviations (must fix)
（なければ「なし」）

### 🟡 Warning (consider fixing)
（なければ「なし」）

### ✅ Matches
- body line-height: 1.9
- p+p margin-top: 1.5em
- h*+p margin-top: 0.3em
- ul/ol line-height: 1.7
- li margin: 0.4rem 0
- ul padding-left: 1.8em
- ol padding-left: 1.7em
- link style: hover underline only

### ⚪ Intentional (allowlisted)
- font-size body: 17px (zenn 16px) — 日本語可読性優先
- h1/h2/h3/h4 margin-top, style: 左アクセントバー設計のため
- blockquote: callout風デザイン
- table: modern design
- code: ピンク文字+ボーダー

## Layout セクション

### 🔴 Critical Deviations (must fix)
（なければ「なし」）

### 🟡 Warning (consider fixing)
（なければ「なし」）

### ✅ Matches
- container max-width: 1200px
- sidebar width: 288px (w-72)
- sidebar visibility: ≥993px (zenn-desktop)
- gap: 30px
- card border-radius: 4px
- card border: 1px
- card shadow: none
- card padding: py-10 px-10 (40px)
- mobile full-bleed at ≤576px (max-zenn-sp)
- mobile card padding: 35px vertical / 16px horizontal (--article-gutter-sp, ≤576px 統一)
- container responsive padding: 14/20/25/40px at Zenn breakpoints
- H1 max-width: 780px
- page bottom padding: pb-16 (64px ≒ 4rem)

### ⚪ Intentional (allowlisted)
- H1 border-bottom: 2px blue (zenn 1px gray) — ブランドアイデンティティ
- html font-size: 17px fixed (zenn 16/15 responsive)
- text-autospace: 未採用

## 次のアクション
Critical が 1件以上ある場合:
1. 修正案を該当ファイルに適用するか確認
2. Edit ツールで修正
3. `npm run dev` で主要ページを確認し回帰がないかチェック

Critical が 0 件の場合: 監査完了
```

---

## Step 8: 修正の提案

- **Critical が 1 件以上**: 具体的な diff を提示し、適用するかユーザーに確認
- **Warning のみ**: 報告のみ。自動修正しない
- **全て Matches/Intentional**: 「監査完了、差分なし」と報告

**重要**: 自動で globals.css / page.tsx / tailwind.config.js を修正しない。必ずユーザー確認を経る。

---

## 意図的逸脱の管理

`intentional-deviations.yml` に登録された項目は比較から除外される。新しく意図的逸脱を追加したい場合はこのファイルを更新する。

ファイル形式:
```yaml
- key: "項目名"
  doboku: "doboku-noteの値"
  zenn: "Zennの値"
  reason: "逸脱する理由"
```

---

## doboku-note 固有の注意点

- Zenn CSS バンドルのファイル名は変更される（ハッシュベース）ため、ハッシュをハードコードしない
- Zenn CSS には複数ファイルある。Typography は `.znc` を含むファイル、Layout は `View_columnsContainer` / `Container_wide` を含むファイルに分離
- doboku-note は `@tailwindcss/typography` プラグインを使っており、`@apply` されていないプロパティも prose プラグイン由来で適用されている可能性がある
- Zenn の `html { font-size: 15px }` は `@media (max-width: 400px)` でのみ発動
- doboku-note は **`zenn-tiny` / `zenn-sp` / `zenn-tablet` / `zenn-desktop` カスタムブレイクポイント** を `tailwind.config.js` の `extend.screens` で追加している（Zenn の 401/577/769/993 と一致）
- Layout 比較では `xl:` / `lg:` などの Tailwind デフォルトブレイクポイントと Zenn の実ブレイクポイント（max-width 992px 等）の関係に注意。doboku-note は `zenn-desktop:` (993px) を使うことで pixel-perfect な一致を実現している

---

## 実行タイミング

- **定期**: 半年に1回（Q1, Q3 など）
- **CSS/レイアウト変更時**: `src/styles/globals.css` / `src/app/docs/[...slug]/page.tsx` / `tailwind.config.js` を大きく触ったあと
- **記事フィードバック時**: 読みにくさやレイアウト崩れの指摘を受けたとき
- **Zenn 仕様の追従**: Zenn のデザイン変更情報が流れてきたとき

---

## 関連

- Plan file: `C:\Users\m004195\.claude\plans\graceful-percolating-gray.md`（2026-04-13 の初回整備・旧 Windows 環境の履歴。現存しない可能性あり）
- Typography source: `src/styles/globals.css` L17-213
- Layout source: `src/app/docs/[...slug]/page.tsx` L213-315
- Breakpoint source: `tailwind.config.js` `extend.screens`
- Zenn OSS 参考: https://github.com/zenn-dev/zenn-editor/tree/canary/packages/zenn-content-css/src
- Zenn 本番CSS URL: `https://static.zenn.studio/_next/static/css/{hash}.css`（ハッシュは動的取得）

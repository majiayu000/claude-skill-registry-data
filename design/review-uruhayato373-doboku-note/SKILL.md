---
name: review
description: >
  対象ファイルの種類を自動判定し、適切なレビュースキル（review-mobile / check-mdx / check-links / code-review / design-review / critical-review）を実行して結果を集約する統一エントリーポイント。
  Use when user asks to [レビュー, /review, レビューして, 確認して, チェックして].
user-invocable: true
domain: ops
---

対象ファイルのパスと種類から **適切なレビュースキルを自動判定・実行** し、結果を1つのサマリに集約する統一入口。「どのスキルを呼べばよいかユーザが覚えなくてよい」状態を作ることが目的。

## 引数

```
/review [target ...]
```

- **`target` 省略時**: `git diff --name-only HEAD` の変更ファイルを対象
- **ファイルパス**: 単一ファイルをレビュー
- **ディレクトリパス**: 配下の対象ファイルを一括
- **複数指定**: スペース区切りで複数パスを渡せる（各ファイルに適切なスキルが実行される）

## ディスパッチ表

対象ファイルのパスから、実行する下位スキルを決定する。

| パスパターン | 実行するスキル | 備考 |
|---|---|---|
| `content/site/**/r[0-9]*-*/article.mdx` `content/site/**/h[0-9]*-*/article.mdx` | `/check-mdx --rules syntax` のみ | 過去問MDX。review-mobile の対象ルール外 |
| `content/site/civil-construction-1/textbook/**/*.mdx` `content/site/civil-construction-1/textbook-*/article.mdx` | `/review-mobile` → `/check-mdx --rules syntax` → **`/improve-article --mode verify`** | 1級土木教科書。PDF原本との視覚＋網羅率検証込み |
| `content/site/civil-construction-1/guide/**/*.mdx` `content/site/civil-construction-1/guide-*/article.mdx` | `/review-mobile` → `/check-mdx --rules syntax` → **`/improve-article --mode verify`** | 1級土木ガイド。出題傾向＋過去問バックリンクチェック |
| `content/site/civil-construction-2/textbook-*/article.mdx` | `/review-mobile` → `/check-mdx --rules syntax` → **`/improve-article --mode verify`** | 2級土木教科書。PDF原本との視覚＋網羅率検証込み（Phase 1 投入後） |
| `content/site/civil-construction-2/guide-*/article.mdx` | `/review-mobile` → `/check-mdx --rules syntax` → **`/improve-article --mode verify`** | 2級土木ガイド。出題傾向＋過去問バックリンクチェック |
| `content/site/**/keyword-*/article.mdx` `content/site/**/keyword-2026/article.mdx` | `/review-mobile` → `/check-mdx --rules syntax,links` | 外部リンクが多いページ |
| `content/site/pe-comprehensive-management/**/article.mdx`（キーワードページ）| `/review-mobile` → `/check-mdx --rules syntax` → **`/verify-exam-coverage`** | 総監キーワードページ。過去問論点カバー率の検証込み |
| `content/site/**/*.mdx`（上記以外の MDX） | `/review-mobile` → `/check-mdx --rules syntax` | 通常のキーワード/ガイドページ |
| `src/components/ui/**/*.tsx` `src/styles/globals.css` | `/code-review` → `/design-review --visual` | UI コンポーネント変更は視覚回帰（light/dark × desktop/mobile）まで実施 |
| `src/app/**/*.tsx` `src/components/**/*.tsx`（ui 以外） | `/code-review` → `/design-review` | UI コンポーネントは両面チェック |
| `src/**/*.ts` `src/**/*.tsx`（UI以外） | `/code-review` | ロジック・ユーティリティは品質のみ |
| `src/**/*.css` `src/**/*.scss` `src/styles/globals.css` | `/design-review` | デザインシステム準拠 |
| `docs/{strategy,operations,products}/*.md` | `/critical-review` | 設計書・戦略ドキュメント |
| `content/note/**/*.md` | `/critical-review` | note 記事 |
| それ以外（判定不能） | ユーザに確認 | 下記「判定できないとき」を参照 |

### 判定できないとき

以下のいずれかを選んでもらう:

```
レビュー対象のスキルを選択してください:
  1. /review-mobile              ── MDX モバイル可読性
  2. /check-mdx --rules syntax   ── MDX 構文チェック
  3. /check-mdx --rules links    ── 外部リンク切れ検出
  4. /check-mdx --rules all      ── 全 rule で MDX 監査
  5. /code-review                ── Next.js コード品質
  6. /design-review              ── デザインシステム準拠
  7. /critical-review            ── 設計書・計画書の批判的レビュー
  8. キャンセル
```

## 実行手順

### Step 1: 対象ファイルの特定

- 引数省略時: `git diff --name-only HEAD` で変更ファイルを取得
- ディレクトリ指定: 配下の全対象ファイル（`.mdx`, `.tsx`, `.ts`, `.css`, `.md`）を再帰的に列挙
- ファイル指定: そのまま採用
- 存在しないパスが含まれる場合: エラー報告してスキップ

### Step 2: ディスパッチ決定

各ファイルに対してディスパッチ表を適用し、**(ファイル → 実行スキルリスト)** のマップを作る。

例:
```
content/site/pe-comprehensive-management/risk/article.mdx
  → [review-mobile, check-mdx]

src/app/docs/[...slug]/page.tsx
  → [code-review, design-review]

docs/editorial/01_記述式コンテンツ戦略.md
  → [critical-review]
```

### Step 3: 下位スキルの順次実行

ファイル別・スキル別に **順次実行**（並列化はしない。Phase 2 で検討）。

重要な順序ルール:
- **MDX は必ず `review-mobile` → `check-mdx` の順**（review-mobile で修正提案があった場合、check-mdx が構文崩れを検出できるため）
- **src/ は `code-review` → `design-review` の順**（コード品質を先に通し、次にデザイン準拠）
- 各スキルはそれぞれ自前の重大度体系（HIGH/MEDIUM/LOW, Critical/Warning/Info 等）で結果を返すので、`/review` はそれらを統一せず、スキル名ラベルと一緒に転記する

### Step 4: 結果の集約出力

ファイル別・スキル別に整形して1つのレポートにまとめる。フォーマットは下記参照。

## 出力フォーマット

```
=== /review: N files ===

<ファイルパス1>
  [review-mobile] HIGH 2 / MEDIUM 1 / LOW 0
    [HIGH] L42: 4列テーブル → 箇条書きへ変換
    [HIGH] L58: キーバリュー表 → 散文に統合
    [MEDIUM] L73: 表の前に導入文がない
  [check-mdx] OK

<ファイルパス2>
  [code-review] Critical 0 / Warning 1 / Info 2
    [Warning] L112: useEffect の依存配列に eslint-disable
  [design-review] High 0 / Medium 1 / Low 0
    [Medium] L45: トークン外の色指定（#3b82f6）

<ファイルパス3>
  [critical-review] (別途詳細レポートを出力)

=== Summary ===
Files checked: 3
Critical / HIGH: 2
Warning / MEDIUM: 2
OK: 1 (/check-mdx on file1)
```

### レポート長が context 圧迫する場合

**検出は常に全件行う。絞るのは表示だけ**（検出段階で落とすと見逃しになる）。

10ファイル以上のとき、または個別 issue が20件超えのとき:
- 会話には**ファイルごとの件数サマリ＋重大度上位のみ**を表示する
- **全件は `.tmp/review-<対象>.md` に書き出し、そのパスを明示する**（黙って省略しない）
- 詳細は「`/review-mobile <path>` で詳細確認してください」と案内する

## 使い方の例

```bash
# 1. git diff の変更分を一括レビュー（最頻パターン）
/review

# 2. 特定の1ファイル
/review content/site/pe-comprehensive-management/business-continuity-plan/article.mdx

# 3. ディレクトリ一括
/review src/app/category/

# 4. 複数指定
/review src/app/docs/[...slug]/page.tsx content/site/pe-comprehensive-management/risk/article.mdx

# 5. docs/ 配下の設計書
/review docs/editorial/01_記述式コンテンツ戦略.md
```

## アンチパターン

- **全ファイルに全スキルを実行しない** ── ディスパッチ表に従い、そのファイル種別に該当するスキルだけ呼ぶ
- **MDX に `code-review` を流さない** ── `code-review` は TypeScript/TSX 専用。MDX に対しては `review-mobile` と `check-mdx` を使う
- **src/ に `review-mobile` を流さない** ── `review-mobile` は MDX 専用
- **並列実行で結果を失わない** ── 現時点では順次実行を厳守。並列化は Phase 2 で設計する
- **重大度体系を統一しようとしない** ── 各スキルの体系（HIGH/Critical/ERROR 等）はそのまま転記する。変換すると情報が欠落する
- **`/review` 内で修正まで実行しない** ── 本スキルは Evaluator 専任。修正は各下位スキルの Step 6 や、ユーザー確認を経て別途実行する

## 参照

- `.claude/skills/quality/review-mobile/SKILL.md` ── MDX モバイル可読性
- `.claude/skills/quality/check-mdx/SKILL.md` ── MDX 検査統合（8 rules）
- `.claude/skills/dev/code-review/SKILL.md` ── Next.js コード品質
- `.claude/skills/ui/design-review/SKILL.md` ── デザインシステム準拠
- `.claude/skills/management/critical-review/SKILL.md` ── 批判的レビュー
- `CLAUDE.md` ── ハーネス設計原則、Generator/Evaluator 分離

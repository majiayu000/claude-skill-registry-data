---
name: check-mdx
description: >
  MDX ファイルの構文・frontmatter・リンク・SVG・法令引用・関連キーワード・note リンク・過去問解説等を
  rule ベースで検査する統合 Evaluator スキル。10 rule を `--rules` フラグで選択可能。
  pre-commit hook からも利用される。
  Use when user asks to [MDX検査, lint MDX, 構文チェック, リンクチェック, SVG監査, frontmatter チェック, 法令リンク, note リンク, /check-mdx].
user-invocable: true
domain: site
---

MDX 品質に関する 10 種類の検査ルールを 1 つのスキルに統合した Evaluator。旧 `/check-mdx` `/check-frontmatter` `/check-links` `/audit-staging` `/audit-exam-explanations` `/audit-svg` `/check-related-keyword-inline` `/check-legal-citations` を吸収。

## 引数

```
/check-mdx [path] --rules <rule1,rule2,...|all>
```

| 引数 | 説明 |
|---|---|
| `path` | 対象ファイル or ディレクトリ（省略時は `git diff --name-only HEAD` の MDX） |
| `--rules` | 実行ルールをカンマ区切りで指定。`all` で全ルール |
| `--fix` | 自動修正可能なルール（links / legal-citations）で適用。デフォルトは検出のみ |
| `--stdin` | ステージ済み MDX を対象（pre-commit 互換） |
| `--json` | JSON 形式で出力 |
| `--severity` | 指定重大度のみ報告（`HIGH` / `MEDIUM` / `LOW` / `ALL`） |

## ルール一覧

| Rule | 重大度 | 対象 | 検査内容 | 実装 |
|---|---|---|---|---|
| `syntax` | ERROR/WARN | MDX 全般 | MDX 構文（`{}` エスケープ、`<>` タグ、見出し階層、テーブル、数式、未対応記法の混入） | Claude 読解 |
| `frontmatter` | HIGH/MEDIUM/LOW | frontmatter | zod スキーマ + 内容（description 長・publishedAt・tags allowlist） | `.claude/scripts/lint-frontmatter.mjs` |
| `links` | HIGH/INFO | 外部・内部リンク | HTTP HEAD で外部 URL 死活、内部 `/docs/`・`/category/` slug 存在＋`#anchor` 断片検証（note ドラフトも対象） | `scripts/rules/links/` |
| `svg` | HIGH/MEDIUM/LOW | 埋込 SVG | 文字クリップ、必須属性、viewBox 幅、font-size、テキスト重なり、色トークン | `scripts/rules/svg/` |
| `staging` | — | Obsidian ステージング | 公開準備度（5 軸 15 点評価） | Claude 読解 |
| `explanations` | HIGH/MEDIUM | 過去問解説 | 破損解説パターン（P1-headless / P2-examPoint-empty） | `scripts/rules/explanations/` |
| `empty-container` | HIGH | MDX 全般 | 中身が空の `<Callout>`（空白・コメントのみ）= タイトルだけの無意味な枠（E1-empty-callout）。bulk リンク削除等でコンテナの中身だけ消えて枠が残る事故の再発防止 | `scripts/rules/empty-container/` |
| `related-keyword` | MEDIUM | キーワードページ | 末尾「関連キーワード: [A]、[B]」列挙パターン（ルール 8-1） | `.claude/scripts/lint-mdx-mobile.mjs` |
| `legal-citations` | LOW | 法令引用 | e-Gov 法令検索リンク化されているか（ルール 8-2） | `scripts/rules/legal-citations/` |
| `note-link` | MEDIUM | note リンク | note 記事リンク（`note.com/dobokunote/n/`）が `<NoteLink>` 外（生 markdown・`<Callout>`・`<LinkCard>`）で書かれていないか（ルール 8-3） | `.claude/scripts/lint-mdx-mobile.mjs` |

### 全体スキーム

- **重大度統一ポリシー**: 各ルールは独自の重大度体系を持つ。本スキルは統一せず、そのまま転記する
- **HIGH は pre-commit でブロック**される。MEDIUM/LOW は警告表示のみ
- **Evaluator 専任**: 修正は Generator 側（`/improve-article`, `/keyword-page revise` 等）が行う。例外: `--fix` 指定時の `links` / `legal-citations` のみ自動修正を許可

## 使い方の例

```bash
# 基本: 全 rule を変更 MDX に適用
/check-mdx --rules all

# 特定ファイル
/check-mdx some-file.mdx --rules frontmatter,syntax

# ディレクトリ単位
/check-mdx content/site/pe-comprehensive-management/ --rules related-keyword

# SVG のみ
/check-mdx --rules svg --severity HIGH

# pre-commit 相当
/check-mdx --stdin --rules frontmatter

# 自動修正（対応 rule のみ）
/check-mdx --rules legal-citations --fix

# 一括監査の JSON 出力
/check-mdx --all --rules all --json > /tmp/audit.json
```

## ルール別の詳細

### syntax — MDX 構文検証（Claude 読解）

next-mdx-remote / MDX v3 のビルドエラーを未然に防ぐ。

**検査項目**:
1. **frontmatter**: `---` で囲まれた YAML、title / description の存在
2. **MDX 構文**: `{` `}` のエスケープ（JSX 式誤解釈）、`<` `>` のタグ誤解釈、import 文
3. **見出し階層**: h1 不使用（title が h1）、階層スキップなし
4. **リンク・画像**: 内部パス存在、画像パス存在、`/static/` 絶対パス禁止
5. **数式（KaTeX）**: `$$...$$` ブロック前後の空行、`$...$` 内改行なし
6. **既知の落とし穴**: `**[text](url)**` の太字リンク、ローマ数字見出しアンカー（`#Ⅰ-`）
7. **テーブル**: ヘッダー行・セパレーター・列数一致
8. **未対応記法の混入**: `:::note`（Docusaurus admonition・本サイトは `<Callout>`）や Mermaid は next-mdx-remote で描画されないため混入を検出、`<div>` 閉じ

**出力**: ERROR / WARN / INFO。Claude が MDX を読んで判定。

### frontmatter — zod + lint（`.claude/scripts/lint-frontmatter.mjs`）

構造（zod）+ 内容（独自 lint）の 2 層検証。

| 重大度 | コード | 内容 |
|---|---|---|
| HIGH | `zod` | zod スキーマ違反（必須フィールド欠落、enum 不正） |
| HIGH | `parse` | YAML パース失敗 |
| MEDIUM | `desc-short` | description < 50 文字 |
| MEDIUM | `publishedAt-missing` | `published: true` なのに `publishedAt` 未設定 |
| MEDIUM | `publishedAt-range` | 年が 2020-2030 範囲外 |
| MEDIUM | `publishedAt-future` | 未来日（8 日以上先） |
| LOW | `desc-long` | description > 200 文字 |
| LOW | `tags-empty` | `tags` 空 |
| LOW | `tags-unknown` | `src/config/tags.json` の受理綴り（name・slug・aliases・canonical）外。正規表記は日本語名（[content-taxonomy.md](../../../knowledge/reference/content-taxonomy.md) §5） |
| LOW | `sections-missing` | `exams` 複数なのに `sections` 未設定 |
| LOW | `sections-incomplete` | `sections` に未登録 exam |

**実行**: `node .claude/scripts/lint-frontmatter.mjs <target>`

### links — 外部 URL + 内部リンク

#### 外部 URL（`check-external-links.mjs`）

HTTP HEAD（並列 10 / タイムアウト 15 秒）で検証。対象は `content/site/**`。

**分類**:
- ❌ リンク切れ（404/410）→ 要修正
- ⚠️ エラー（403 等）→ 要確認（bot 拒否の可能性）
- ⏱️ タイムアウト → 要確認（政府サイトは遅い場合あり）
- ✅ OK

**自動修正**: `--fix` 指定時、リンク切れに対して WebSearch で代替 URL 検索 → Edit 提案

#### 内部リンク（`check-links.mjs`）

決定的検証（ネットワーク不要・誤検出ゼロ）。`content/site/**` と `content/note/**/article.md` の両方を走査。

**対象リンク形式**: 相対 `[text](/docs/slug)`、絶対 `[text](https://doboku-note.com/docs/slug)`、新 URL `[text](https://doboku-note.com/exam/...)`（`public/_redirects` で旧 slug へ戻して同じ検査にかける）、裸 URL（note リンクカード形式）。

**検証内容**:
- `BROKEN_SLUG` (HIGH): `/docs/{slug}` の slug が `content/site` 由来の有効 slug 集合に無い
- `BROKEN_ANCHOR` (HIGH): `#anchor` 断片がリンク先ページの見出し ID 集合に無い（`#lib/heading-id.mjs` で一般版・過去問変種の両 ID を許容）
- `BROKEN_CATEGORY` / `BROKEN_STATIC` (HIGH): `/category/{slug}`・静的ページの存在確認
- `PLACEHOLDER` (INFO): note.com マガジンの `PLACEHOLDER_*`（未発売プレースホルダ。ブロック対象外）

**フラグ**:
- `--scope note|site|all`（既定 `all`）
- `--json` — `{ meta, summary, findings[] }` を stdout 出力
- `--report <dir>` — `audit-{timestamp}.json` + `latest-report.md` を書き出す

**実行**:
- 外部: `node .claude/skills/quality/check-mdx/scripts/rules/links/check-external-links.mjs`
- 内部: `npm run check-links`（= `check-links.mjs`。`-- --scope note` 等を付与可）

#### 定期監査（`link-audit.yml`）

`.github/workflows/link-audit.yml` が毎週土曜 07:00 JST に `npm run check-links-audit`（`--scope all --report`）を実行し、`.claude/state/link-audit/` に結果を蓄積して develop へ `[skip ci]` commit する。Issue は起票せず、`latest-report.md` 自体が記録。

### svg — 埋込 SVG 品質

`content/site/**/img/*.svg` の静的解析。

| ID | 重大度 | 内容 |
|---|---|---|
| P1-text-clip | HIGH | テキストが viewBox はみ出し |
| P2-text-overlap | MEDIUM | テキスト bbox 重なり |
| P3-missing-role | MEDIUM | `role="img"` 欠落 |
| P3-missing-aria | MEDIUM | `aria-label` 欠落 |
| P3-missing-maxwidth | HIGH | `style="max-width:Xpx;width:100%"` 欠落 |
| P4-tiny-font | LOW | `font-size < 11px` |
| P5-wide-viewbox | MEDIUM | `viewBox` 幅 > 400px（`figure-*--wide.svg` は landscape 16:9=640 幅が正のため P5 免除。固定キャンバス適合は `npm run check-figure-canvas` が担保。→ figure-canvas-policy.md） |
| P6-color-drift | MEDIUM | `svg-tokens.json` colorsAllowList 外 |
| P7-missing-font-family | MEDIUM | `font-family` 未指定 |
| P8-dark-bg | HIGH | 濃色 fill + 白/薄色テキスト（`design-system.md §8` 違反） |
| P11-concept-title | MEDIUM | 最上部中央の大見出し（font≥14・y≤26・中央）＝概念名タイトル（`figure-canvas-policy.md` §2.4 違反。SNS ヘッダーと二重化） |
| P12-exam-hint | HIGH | 図内に受験対策注記（試験ポイント/引っかけ/出題ポイント）＝概念図に入れない（`content-principles §5`・`figure-canvas-policy §2.5 #5`。試験原図は h*-primary 除外） |

**出力**: `.claude/state/svg-audit.json`（全件走査のときだけ更新。`--file` / `--path` / `--severity` の部分実行は所見を標準出力へ出し、state は書き換えない）

**ギャラリー生成（目視 QA）**:
```bash
npm run svg-gallery               # site/note 図版を 1 枚 HTML で（site/note タブ＋資格別フィルタ・site は svg-audit.json 重大度バッジ）
node .claude/skills/quality/check-mdx/scripts/rules/svg/build-gallery-comment.mjs  # 旧: GitHub コメント用 Markdown
```
`npm run svg-gallery` はローカル目視用（`.tmp/svg-gallery.html`・`--open` でブラウザ起動・svg-figure-auditor の視覚確認の足場）。上部タブで「サイト／note」を切替え、各タブ内で資格別（カテゴリ）に絞り込む。`build-gallery-comment.mjs` は GitHub Issue/PR コメント用 Markdown（`.tmp/svg-gallery-comment.md`）で用途が別。

**実行**: `node .claude/skills/quality/check-mdx/scripts/rules/svg/audit.mjs`

### staging — Obsidian 公開準備度（Claude 読解）

`~/obsidian/exam/1doboku/` の `status: review` / `ready` ノートに対して 5 軸ルーブリックで評価（15 点満点、10 点以上で `ready` 推奨）。

| 軸 | 重み | チェック内容 |
|---|---|---|
| 構造正確性 | 30% | 見出し階層、論理構成 |
| テキスト忠実度 | 25% | 出典明記、内容正確性 |
| 表・図・数式 | 20% | テーブル・KaTeX 正当性 |
| MDX 互換性 | 15% | Obsidian 固有記法（`[[]]`, `![[]]`）残存チェック |
| メタデータ品質 | 10% | title / tags / exam-topic / source |

**出力**: promote 候補リスト（推奨順）。Claude が Read で読んで判定。

### explanations — 過去問破損解説

| ID | パターン | 例 |
|---|---|---|
| P1-headless | 解説文頭が閉じカギから始まる | `1. 」と規定されている ✅` |
| P2-examPoint-empty | ExamPoint `summary` 欠落 | `summary="」とされている"` |

**出力**: `.claude/state/broken-explanations.json`

**引数**: `--category civil-construction-1` / `--topic 港則法` で絞り込み

**実行**: `node .claude/skills/quality/check-mdx/scripts/rules/explanations/audit.mjs`

**pre-commit 連動**: `scripts/pre-commit-mdx.mjs` が `detect.mjs` を import し、warning 表示（既存 64 件があるためブロックはしない）

### related-keyword — 関連キーワード末尾列挙

キーワードページ末尾の `関連キーワード: [A]、[B]` パターンを検出（`lint-mdx-mobile.mjs` ルール 8-1）。

**移行アプローチ**:
- **type-1**: 本文中に既にキーワード名がある → インライン化で対応
- **type-2**: 本文中にないが関連性が強い → 1 文追加してインライン化
- **type-3**: 関連性が弱い → 削除してよい

**禁止アプローチ**: `sed -i '/^関連キーワード[:：]/d'` のような完全自動置換は **絶対に使わない**（データ消失リスク）。

**実行**: `node .claude/scripts/lint-mdx-mobile.mjs <target> 2>&1 | grep "8-1"`

### legal-citations — e-Gov 法令リンク

MDX 本文の「〇〇法第◯条」が e-Gov 法令検索にリンクされているか検査（`lint-mdx-mobile.mjs` ルール 8-2）。

**URL 形式**: `https://laws.e-gov.go.jp/law/{法令番号}#Mp-At_{条番号}`

**枝番条文（第38条の3 等）**: e-Gov リンクを付けない（公式アンカー形式未確定）。太字のみで留める。

**自動修正**（`--fix`）:
```bash
# dry-run
node .claude/skills/quality/check-mdx/scripts/rules/legal-citations/fix-legal-citations.mjs --dry-run

# 適用（バックアップは /tmp/fix-legal-citations-backup/ に保存）
node .claude/skills/quality/check-mdx/scripts/rules/legal-citations/fix-legal-citations.mjs --apply
```

**法令番号辞書**: `fix-legal-citations.mjs` の `LAW_ID_MAP`（2026-04-13 時点で 31 件登録、HTTP 200 で検証済み）。新法令追加は `LAW_ID_MAP` に `'{法令名}': '{法令番号}'` を足してから実行。

### note-link — note 記事リンクのコンポーネント統一（`lint-mdx-mobile.mjs` ルール 8-3）

note.com 記事へのリンク（`note.com/dobokunote/n/`）は `<NoteLink>` コンポーネントに統一する規約（→ `.claude/knowledge/reference/content-authoring.md`「リンク系コンポーネントの使い分け」）。生 markdown リンク・`<Callout type="reference">` 内・`<LinkCard>` で note 記事リンクを書いている箇所を MEDIUM で検出する。

- magazine リンク（`note.com/dobokunote/m/`）は `<MagazineCard>`（SoT 解決・既定 hero）担当のため対象外
- フェンスコードブロック内は対象外
- 修正は Generator 側（`<NoteLink>` への置換）が行う。Evaluator は検出のみ

**実行**: `node .claude/scripts/lint-mdx-mobile.mjs <target> 2>&1 | grep "8-3"`

## 出力フォーマット

### 基本（テキスト）

```
=== /check-mdx: <対象> ===

[syntax] <ファイル>
  ERROR L42: エスケープされていない `{`
  WARN  L15: 見出しレベル h2 → h4 のスキップ

[frontmatter] <ファイル>
  HIGH: zod スキーマ違反（必須フィールド `title` 欠落）
  MEDIUM: description が 42 文字（50 文字未満）

[links] <ファイル>
  HIGH: https://example.com/gone (404)

[svg] <ファイル>
  HIGH P1-text-clip: 「航路内の禁止」が viewBox 外
  MEDIUM P3-missing-aria: aria-label 欠落

...

=== Summary ===
Files checked: 12
HIGH: 3 / MEDIUM: 8 / LOW: 21
OK: 6 files
```

### JSON（`--json`）

```json
{
  "meta": { "generated_at": "...", "rules": ["syntax", "frontmatter"] },
  "summary": { "files_checked": 12, "HIGH": 3, "MEDIUM": 8, "LOW": 21 },
  "findings": [
    { "file": "...", "rule": "syntax", "severity": "ERROR", "line": 42, "message": "..." }
  ]
}
```

## pre-commit hook との連動

`scripts/pre-commit-mdx.mjs` は以下を `import` して利用:
- `scripts/rules/explanations/detect.mjs` → `detectBrokenExplanations`（warning 表示）
- `scripts/rules/svg/detect.mjs` → `auditSvgFile`（warning 表示）
- `#shared/lint-frontmatter.mjs` → `lintFrontmatter`（HIGH はブロック）

ステージ済み MDX に対して自動走行。

## アンチパターン

- **修正まで実行しない**（`--fix` 指定の links / legal-citations を除く）。Evaluator 専任
- **重大度を統一しようとしない**: 各ルールの体系（HIGH/Critical/ERROR 等）はそのまま転記
- **related-keyword の一括 sed 削除**: データ消失リスクのため絶対禁止（アプローチ A）
- **枝番条文の e-Gov リンク付与**: 公式アンカー未確定のため禁止

## 旧スキルからの移行対応表

| 旧スキル | 新呼出 |
|---|---|
| `/check-mdx` | `/check-mdx --rules syntax`（または rule 省略でデフォルト syntax） |
| `/check-frontmatter <target>` | `/check-mdx <target> --rules frontmatter` |
| `/check-links` | `/check-mdx --rules links` |
| `/check-links --fix` | `/check-mdx --rules links --fix` |
| `/audit-staging [path]` | `/check-mdx [path] --rules staging` |
| `/audit-exam-explanations --category X` | `/check-mdx --rules explanations --category X` |
| `/audit-svg --severity HIGH` | `/check-mdx --rules svg --severity HIGH` |
| `/check-related-keyword-inline` | `/check-mdx --rules related-keyword` |
| `/check-legal-citations --fix --apply` | `/check-mdx --rules legal-citations --fix --apply` |

## 参照

- `.claude/scripts/lint-frontmatter.mjs` — frontmatter rule 実装
- `.claude/scripts/lint-mdx-mobile.mjs` — related-keyword (8-1) / legal-citations (8-2) 検出ロジック
- `.claude/scripts/lib/mdx-io.mjs` — CRLF 保持 I/O（`--fix` 系で使用）
- `scripts/rules/{rule}/` — rule 別スクリプト実装
- `scripts/pre-commit-mdx.mjs` — pre-commit hook 連動
- `.claude/knowledge/reference/content-authoring.md` — MDX 作成詳細ルール
- `.claude/skills/authoring/keyword-page/SKILL.md` — 関連 Generator（作成規約）
- `.claude/skills/authoring/improve-article/SKILL.md` — 関連 Generator（対話型修復）

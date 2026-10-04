---
name: citation-traceability-audit
version: 2.2.0
description: 投稿前・各章完成時に、本文引用の書誌整合（matrix SoT）と文献実体化（papers/ Grounding）を監査し、references.mdを機械生成するスキル
---

# 出典・脚注トレーサビリティ監査スキル (Citation Traceability Audit)

## 目的
静的コード解析（Static Analysis）の考え方を応用し、原稿本文中のすべての記述・引用・脚注参照（`[^1]` 等）が、正本である `docs/literature/literature-matrix.md`（書誌 SoT）および `docs/literature/papers/*.md`（内容 SoT）と 1対1 で整合しているかを包括的に監査する。

## 発動タイミング
- **章/節の新規執筆・大幅追記の前**（Grounding Audit — ブロックゲート）
- 論文の各章執筆完了時
- 投稿・最終提出前の自動チェック

## 処理手順 (5段階メカニカル監査ワークフロー)

```text
[Step 1: 本文引用の機械抽出] ➔ [Step 2: 一次文献マトリクス照合] ➔ [Step 2.5: 文献実体化照合 (Grounding)] ➔ [Step 3: references.md 自動生成] ➔ [Step 4: 1対1整合性再監査]
```

### Step 1: 本文引用の機械抽出
同梱スクリプト `scripts/check_citation_format.py` を用い、本文（`docs/chapters/`）に存在するすべての引用マーカー（個人著者 `Son, 2010`、組織著者略称 `PSA, 2024` / `ADB, 2023`、複数単語組織 `World Bank, 2026` 等）および脚注 `[^1]` を機械的に抽出する：

```bash
python3 scripts/check_citation_format.py docs/chapters/
```

### Step 2: 正本文献マトリクス (SoT) との照合
正本である `docs/literature/literature-matrix.md` と抽出した本文引用を照合する：

```bash
python3 scripts/check_citation_format.py --matrix docs/literature/literature-matrix.md docs/chapters/
```
- **未登録引用の検知**: 本文中で引用されているが、`literature-matrix.md` に登録のない文献が存在する場合、AIのエージェント記憶による生成を行わず、即座に一次資料調査へと差し戻す。

### Step 2.5: 文献実体化照合 (Grounding Audit) — **v2.0.0 新設**

`literature-matrix.md` は索引（Discovery 成果物）であり引用根拠としては不十分。各引用について `docs/literature/papers/*.md` の実体ファイル存在を DOI/arXiv ID（優先）または著者+年で照合する：

```bash
python3 scripts/check_literature_grounding.py docs/chapters/ \
  --papers-dir docs/literature/papers/ \
  --matrix docs/literature/literature-matrix.md
```

**判定**:
- **FAIL**: 対応する `papers/*.md` が存在しない → **執筆ブロック**（fact-grounding-rule §5）
- **WARN**: `status: manual-stub` または `abstract-only`、または本文文字数不足、または **`status: full-text` なのに `_downloads/{slug}.pdf` が無い**
- **PASS**: `status: full-text` かつ十分な本文テキスト **かつ** 対応 PDF が `_downloads/` にある

**`papers/*.md` frontmatter 必須フィールド**:
`title`, `authors`, `year`, `doi`, `arxiv_id`, `status` (`full-text` | `manual-stub` | `abstract-only`), `source_url`, `version`

**成果物**: `docs/design/literature-grounding-report.md`（スクリプト出力を転記）

> ⚠️ **書籍・学位論文**: PDF 自動取得不可の文献は `status: manual-stub` + ページ番号付き書き抜きで実体化する（fact-grounding-rule §2-B-3）。
> ⚠️ **一次資料 PDF**: `_downloads/` は gitignore しない。`full-text` 主張の再照合対象である。再配布権の無い PDF は置かず stub に留める（DISCLAIMER）。
> ⚠️ **bot 対策（reCAPTCHA / Cloudflare）**: 自動 DL が `bot-challenge … human handoff required` を返した文献は、著者がブラウザで PDF を `_downloads/{slug}.pdf` に配置するまで WARN/stub のままとする（[`pdf-paper-ingestion`](../pdf-paper-ingestion/SKILL.md) Step 1b）。

### Step 3: `references.md` の自動派生生成
照合完了後、`literature-matrix.md` から派生生成物として `docs/chapters/references.md` を自動生成する：

```bash
python3 scripts/check_citation_format.py --generate-references docs/chapters/references.md --matrix docs/literature/literature-matrix.md docs/chapters/
```

> ⚠️ **単一真実解（Single Source of Truth: SoT）規律**: 
> `docs/literature/literature-matrix.md` が文献**書誌**情報の唯一の正本（SoT）である。`docs/literature/papers/*.md` が文献**内容**の根拠正本である。`docs/chapters/references.md` は手動編集してはならず、必ずスクリプトから自動生成しなければならない（`<!-- AUTO-GENERATED -->` ヘッダを付与）。

### Step 4: 1対1整合性再監査
生成された `references.md` と本文引用の間に、未定義参照（Missing Definitions）や孤児文献（Unused References）が存在しないか最終確認する。

## 成果物
- 自動生成された `docs/chapters/references.md` (参考文献一覧)
- 文献実体化監査 `docs/design/literature-grounding-report.md`
- 監査ログ `docs/design/citation-audit.log`

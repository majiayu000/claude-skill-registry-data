---
name: readme-style
description: Author and review Baan's `README.md` with consistent vocabulary, structure, and message hierarchy. Use when asked to "review the README", "lint the README", "check README consistency", "write a section for README", or equivalent requests in any language. Read-only by default — propose edits, wait for approval before applying.
---

# README Style Guide

Baan's `README.md` is the **first impression of the project** for
developers, evaluators, and prospective users. It sets the tone for
the entire documentation surface (`baan.press`, theme docs, blog
posts written about Baan). Inconsistency here cascades.

`README.md` is English-only. A local-only Japanese working draft
lives at `README.ja.draft.md` (gitignored) for the maintainer's
authoring workflow; it is never published and not subject to this
style guide.

This skill enforces:

1. The product **thesis** (what Baan is, in what order)
2. **Terminology** (one canonical name per concept)
3. **Notation** (backticks, code blocks, headings, punctuation)
4. **Structure** (section ordering, heading levels, image placement)

## When to invoke

- "READMEをレビュー / 校閲してほしい" / "review README"
- "READMEに節を追加して" / "add a section to README"
- "READMEの表記を統一して" / "lint README consistency"
- Any time `README.md` is the target file (or its gitignored
  `README.ja.draft.md` working draft)

## Before editing — investigate first

This skill follows `.claude/rules/workflow.md`:
**Investigate → Plan → Approval → Implement.**

1. Read the full `README.md` (do not edit on partial context)
2. If the maintainer is updating from `README.ja.draft.md`, also
   read that file and verify the change has been faithfully reflected
   in the English `README.md`.
3. Build a finding list (use the audit checklist below)
4. Present findings as a single table, propose fixes, **wait for explicit approval**
5. Apply approved fixes only

Per `feedback_no_implement_without_approval.md`: do not start
editing the README after presenting an audit. Wait for the user to
greenlight specific items.

## Canonical vocabulary — one name per concept

| Concept | Canonical | Prohibited synonyms |
|---------|-----------|---------------------|
| Admin panel | **Baan Admin** (formal) / **BaanのAdmin** / **Admin** | ~~Admin画面~~, ~~Adminパネル~~, ~~管理画面~~, ~~管理 UI~~ |
| Bot (search engine, AI) | **Bot** | ~~ボット~~ |
| CLI | **Baan CLI** | ~~baan-cli~~ (except in npm install commands and GitHub URLs) |
| Markdown format | **Markdown** | ~~マークダウン~~ |
| Knowledge graph feature | **Knowledge Graph** | ~~ナレッジグラフ~~ |
| Storage provider name | **`local`** (lowercase, backticks) | ~~Local~~, ~~`Local`~~ |
| Server's local filesystem | **ローカルファイルシステム** | ~~ファイルシステム~~ (when meaning local FS), ~~local~~ (when meaning FS, not provider) |
| Database | **`libSQL`** (primary) / **`SQLite`** (when stressing the file format) | ~~SQLite (libSQL)~~ as if SQLite is primary |

**Why these specifically:** `Baan Admin` is the product's formal
name for the admin surface — anything else dilutes it. `Bot` is
already a loanword in Japanese tech writing. `Markdown` is a proper
noun. `Knowledge Graph` aligns with `mentions` / `about` JSON-LD
vocabulary used in the same section. `local` is the literal config
value (`STORAGE_PROVIDER=local`), so casing matters.

**`local` vs `ローカルファイルシステム`:**
- Provider name (config value, table cell): `local`
- The thing being written to (prose): `ローカルファイルシステム`

## Backtick rules

Backtick service names, technology names, file names, env var names,
config values, and CLI commands — even in prose. Reasons:

1. Backticks make scanning easier (the eye locks onto monospace tokens)
2. Service names like `Vercel`, `Docker`, `Turso` look like ordinary
   nouns without them — the visual cue helps non-native readers parse
3. Consistency: if it's backticked in one section, it must be
   backticked in every section

| Backtick | Don't backtick |
|----------|----------------|
| `Vercel`, `Docker`, `AWS S3`, `Turso` (service names) | "the database", "the editor" (generic nouns) |
| `libSQL`, `SQLite`, `Next.js`, `React 19` (tech names) | Baan itself (it's the subject) |
| `local`, `gcs`, `s3`, `r2` (storage provider config values) | "サーバーレス", "セルフホスト" (deployment modes — these are concepts) |
| `.env`, `data/app.db`, `package.json` (file paths) | Section titles (markdown headings rarely benefit from backticks) |
| `npm test`, `revalidatePath()` (commands / functions) | |

**Inside fenced code blocks**, never wrap tokens in backticks —
they render literally and look broken. Code blocks already are
monospace.

## Heading and structure rules

### Numbered section format

```
### 1. Title           <- correct
### 1.Title            <- prohibited (no space after period)
###  1. Title          <- prohibited (extra space)
```

### Subtitle (h5 under h3 numbered section)

```
### 3. Knowledge Graph + Bridge記事ジェネレータ
##### 記事間の隠れたつながりをAIが可視化し、新しい記事のアイデアまで提案します
```

- One sentence
- **No trailing punctuation** (no `。`)
- Describes user-observable benefit, not internal mechanism

### Heading language

The published `README.md` is English. Established English
catchphrases (e.g. `No heavy RDB. No Git pollution.`) are deliberate
marketing copy and must be preserved verbatim.

In the local `README.ja.draft.md` working file the same catchphrases
are also kept in English; surrounding prose is in Japanese.

### Image placement

```
### 3. Knowledge Graph + Bridge記事ジェネレータ
##### Subtitle line

Body paragraph(s)...

<img src="docs/images/<file>.png" alt="<kebab-case-id>" width="700" />

More body...
```

- `width` is fixed per image purpose: hero/screenshot `700`, small
  panel `400-600`, top architecture `800`
- `alt` is kebab-case, descriptive, English

## Japanese-specific rules

### 「事」 vs 「こと」

Use **こと** (hiragana) in technical Japanese prose. `事` is
prohibited when it functions as a formal noun ("こと").

```
✓ 切り替えることも可能です
✗ 切り替える事も可能です
```

Exception: idiomatic compounds like `仕事` / `事象` keep kanji.

### 「出来る」 vs 「できる」

Prefer **できる** (hiragana). `出来る` is acceptable in older
documentation but the convention going forward is hiragana.

### Punctuation in tables and inline lists

- Use `/` (with spaces around it: ` / `) to separate alternatives:
  `` `GCS` / `S3` / `R2` ``
- Do not use `、` to separate technology names — that reads as
  natural-language enumeration, not "either-or"
- For 3+ alternatives in prose, prefer the slash form too

## Thesis order — what comes first

The README's section order is itself a message. The Baan thesis is:

1. **What Baan is** (one sentence — narrative platform / 家)
2. **Why now** (AI synthesises fragments — you must own your narrative)
3. **Architecture sketch** (Markdown + lightweight metadata, no heavy RDB, no Git pollution)
4. **Differentiators** (numbered list — currently 8)
5. **Detail (`# Baan 詳細`)** — operational reference

Do not reorder these without discussing with the user. In
particular, **never bury the thesis** under installation
instructions or technology stack tables.

The numbered differentiators currently lead with **storage / git
hygiene** (1) and **editor freedom** (2), then **AI features** (3,
4, 6), then **operational hygiene** (5, 7, 8). Adding a new
numbered section means deciding what tier it sits in.

## Audit checklist

Run through this whenever auditing or before opening a PR that
touches the README.

### 思想 (thesis)
- [ ] Does the lead paragraph still match `Baan` is `<one phrase>`?
- [ ] Are the 「家」 / narrative metaphors consistent and not over-used?
- [ ] Does the architecture image (`nordb-nogit.png`) appear before
      any detail-level content?

### Vocabulary
- [ ] `Baan Admin` / `BaanのAdmin` / `Admin` only — no `Admin画面`, `管理画面`, `管理 UI`
- [ ] `Bot` only — no `ボット`
- [ ] `Markdown` only — no `マークダウン`
- [ ] `Knowledge Graph` only — no `ナレッジグラフ`
- [ ] `Baan CLI` in prose; `baan-cli` only in npm install / repo URL
- [ ] `local` for the provider name; `ローカルファイルシステム` for the thing
- [ ] `libSQL` is the primary database name; `SQLite` is the
      underlying file format

### Notation
- [ ] Service / tech / config-value names backticked in prose and tables
- [ ] No backticks inside fenced code blocks
- [ ] Section numbers: `### N. Title` with one space
- [ ] Subtitles (`#####`): no trailing `。`, one sentence, benefit-led
- [ ] Image `width` matches the per-purpose convention
- [ ] Image `alt` is descriptive English kebab-case

### Japanese
- [ ] No `事` used as a formal noun ("こと")
- [ ] Alternatives separated by ` / `, not `、`
- [ ] No mixed full-width / half-width spacing inside backticked tokens

### Draft sync (only when `README.ja.draft.md` is part of the change)
- [ ] If a section was added / removed in the JA draft, the same
      change is reflected in `README.md`
- [ ] Image filenames and `alt` text match between draft and English
- [ ] External links (baan.press docs, GitHub repos) match between
      draft and English

## Writing new sections

When adding a new section to the README:

1. **State the user-observable value first.** "X ができます" / "X
   makes Y possible" — not "Baan は X を実装している".
2. **One paragraph of prose, then a table or a screenshot.** Long
   prose without visual anchors is skipped.
3. **No marketing adjectives without proof.** "革新的" / "革命的" /
   "world-class" all need an immediate concrete example.
4. **End with a link to deeper docs**, not with a summary. `baan.press`
   has more depth — the README's job is to make the reader want to
   click through.

## Reporting style for audits

Per `.claude/rules/reporting.md`:

- One findings table — columns: `#` / category / location / current
  / proposed
- ≤ 3 lines of context after the table
- No section headers like "Summary" / "Recommendations" — the table
  IS the summary
- Group by severity: blocking inconsistency > vocabulary drift >
  cosmetic notation

Example:

```
| # | Type | Where | Current | Proposed |
|---|------|-------|---------|----------|
| 1 | Vocab | L140 | ボット | Bot |
| 2 | Notation | L289 | `Local` | `local` |
```

## What NOT to do

- Do not translate `README.md` into a committed locale variant —
  the only Japanese surface that exists is the gitignored
  `README.ja.draft.md` working draft, never committed
- Do not add new section numbers without discussing thesis-order
  impact
- Do not bulk-rewrite for "tone" — the user has invested in the
  current voice; preserve it unless asked
- Do not run `npm run build` or any test as part of an audit; this
  skill is documentation-only
- Do not commit changes; leave the staged diff for the user to
  review and commit themselves

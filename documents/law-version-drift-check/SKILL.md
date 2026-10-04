---
name: law-version-drift-check
description: >
  Detects version drift between machine-readable law YAML files and the binding
  geldende wettekst on wetten.overheid.nl at the YAML's claimed valid_from. Catches
  the silent failure where authored content lags behind ingevoerde wijzigingen — a
  YAML dated 2025-01-01 still carrying pre-Stb.-X text. Activate as Step 0 of every
  regelrecht-stelselanalyse micro-cycle, before any YAML edit. Strict by design: no
  bypass, no normalization beyond whitespace within a single paragraph; the geldende
  wettekst is leading and is mirrored verbatim, including errata. Use proactively
  when starting a stelselanalyse cycle, before harvest/migrate/extend, or when user
  mentions "drift", "versie", "geldende tekst", or worries that a YAML may be stale
  relative to wetten.overheid.nl.
allowed-tools: Read, Write, Bash, Grep, Glob, WebFetch, WebSearch, AskUserQuestion
user-invocable: true
---

# Law Version Drift Check — Step 0 of every micro-cycle

Detects whether a YAML's `text:` blocks (and adjacent fields) match the binding
geldende wettekst at the version the YAML claims to represent. The failure this
skill catches is silent: a file passes schema-validation, hallucination-checks
and BDD tests while its content is from an older version of the law. Every
downstream review (wetgevings-fouten, modellering-fouten, untranslatables) then
mis-classifies bevindingen until the drift is closed.

This skill belongs in the desk-layer (`regelrecht-stelselanalyse`) and runs
*before* every other review-as.

## Core principle — verbatim spiegelregel

> De feitelijk geldende wettekst is leidend. Fouten in de wet worden feitelijk
> overgenomen. Geen "soll"-fietsen.

The YAML's `text:` block must equal the geldende wettekst character-for-character.
There is **one** allowed normalization, defined below; every other deviation is
drift, regardless of who is "right". Errata, redactionele oddities, dode
verwijzingen — all preserved verbatim in the YAML. If the wet contains a fout,
the wet itself is the carrier; the YAML mirrors it. A wetgevings-fout (4-weg
klasse 2) is reported to the wetgever separately; it is never silently "corrected"
in the YAML.

### The one allowed normalization

`|-` block scalars in YAML wrap long sentences at ~N characters for editor
readability; wetten.overheid.nl wraps based on its own rendering. Within a single
paragraph, multiple whitespace and intra-paragraph line breaks collapse to a
single space before comparison. **Between** paragraphs (between leden, between
onderdelen, between verbatim-blocks) structure is preserved exactly.

Anything else — diacritics, quote glyphs (`«»` vs `"`), capitalization, word
order, punctuation — is part of the law's substance and any deviation is drift.

## Position: Step 0 of `regelrecht-stelselanalyse`

This skill is a **hard prerequisite** for every micro-cycle. Without a CLEAN (or
scope-restricted) drift-report, no YAML edit may be made.

Rationale: drift silently mis-classifies findings across the 4-weg-classificatie:
- A claim "the YAML says X but the wet says Y" is a *wetgevings-fout* only if the
  geldende wet truly says Y. If Y had already been changed by a Stb. that was not
  ingeharvest, the same finding is in fact a *modellering-fout (drift)*. Confusing
  the two breaks the 4-weg discipline that the cycle relies on.

Strict by design: no bypass parameter, no "this cycle is just docs" escape. If a
cycle is purely docs and not touching YAMLs, it doesn't reach Step 0 — the
trigger is "about to edit a regulation YAML".

## Verdict per article — two axes

| Structural | Textual | Verdict |
|------------|---------|---------|
| match | match | **CLEAN** |
| match | diff | **DRIFT-tekst** (with word-level sub-diff) |
| mismatch | (skipped) | **DRIFT-structureel** (with the missing/extra item named) |
| (any) | not fetchable | **NIET-VERIFIEERBAAR** (after retry + Staatsblad-fallback) |

**Structural axis** (assessed first): count of leden, ordered list of onderdeel-
letters per lid, alinea-count per lid. A mismatch here is decisive — skip textual,
report the missing/extra element by name. This is the axis that catches the most
costly drift type: an entire missing onderdeel or lid (a downstream wijziging
that was never harvested).

**Textual axis**: per-paragraph word-level diff after applying the single
allowed whitespace normalization. The output is a unified diff at word
granularity for every paragraph that differs.

## Procedure

### 1. Inventory the target file

Extract from the YAML:
- `bwb_id`, `valid_from`
- per article: `number`, `text:` block (the literal string after `|-`), `url:`
- corpus-level: every `competent_authority.name` referenced anywhere in the file

### 2. Structural inventory from the geldende text

For each article, fetch the structural skeleton at
`https://wetten.overheid.nl/<bwb_id>/<valid_from>#Artikel<N>`.

**Force enumeration in the prompt.** Summary-style prompts produce text that
*looks* complete while quietly dropping the last onderdeel. Required form:

> "List the structural skeleton of artikel N at this version: number of leden,
> for each lid the ordered list of onderdeel-letters (a, b, c, …), and the last
> letter present. Do not paraphrase, do not omit any onderdeel."

Two independent calls per article (different phrasings) and compare; a
disagreement is treated as a fetch reliability problem and triggers Staatsblad-
fallback for that article.

### 3. Calibration ijkpunten — verplicht

Before any drift-report is emitted, the skill must independently re-find a set
of pre-recorded **known drifts** for the corpus under review. The ijkpunten file
lives **in the corpus** (`docs/drift-ijkpunten.md` or equivalent), **not in this
skill**, so the skill stays dossier-agnostic.

If calibration fails to recall ≥ 80% of known drifts: WebFetch is not reliable
for this run. Retry with stricter prompts; on a second failure, fall back to
Staatsblad-stack for the entire corpus. A drift-report **without** passing
calibration is invalid and must be marked as such.

### 4. Verbatim text fetch (textual axis)

For articles that pass the structural axis, fetch the verbatim text per article
with an enumeration-forcing prompt:

> "Give the literal full text of artikel N at this version, lid by lid, onderdeel
> by onderdeel, verbatim. State the last onderdeel letter explicitly so completeness
> can be verified. Do not summarize, do not paraphrase, do not omit."

### 5. Diff per article

- Apply the single allowed whitespace normalization (collapse intra-paragraph
  whitespace; preserve paragraph boundaries).
- Word-level diff per paragraph. Output unified-diff at word granularity.
- Diacritics differences count as DRIFT-tekst (per the verbatim principle).
- Errata-style additions (e.g. parenthetical reading notes) present in the
  geldende text must be present in the YAML; absence is drift.

### 6. Adjacent fields (same file, same run)

- `competent_authority.name` values across the file: check against the current
  formal organ name at the geldende version. A historical name is drift.
- `url:` anchors per article: must resolve to the artikel at the YAML's
  `valid_from`. Anchors pointing at a different version (or a non-existent
  article) are drift.

### 7. Staatsblad fallback — five cases

`wetten.overheid.nl` is primary. Fall back to the Staatsblad-stack
(`zoek.officielebekendmakingen.nl`) **only** when:

1. **Render lag** — a recent Stb. is published but not yet rendered in the
   consolidation; the change exists in the publication of record.
2. **Calibration fail** for a specific article: distrust the render, verify via
   the Stb. that introduced the most recent change to that article.
3. **Errata-style notations** (`[bedoeld zal zijn ...]` or equivalent): confirm
   the notation is in the formal Stb. text, not a rendering artefact.
4. **Version gap** — the YAML's `valid_from` falls between two consolidations
   (deferred inwerkingtreding, retroactive effect): the Stb. clarifies the
   inwerkingtredingsdatum.
5. **Historical version reconstruction** — older `valid_from` where the current
   render no longer shows the historical text cleanly.

Local `pdftotext` is the final fallback for opaque PDFs; mark such articles as
verified via local extraction.

In the report, every article carries its verification mode:
`primair: wetten.overheid.nl/<datum>` or `secundair: Stb. <jaartal>, <nr>` or
`tertiair: local-pdf-extract`.

### 8. Partial-failure handling — scope-restrictie

After retry + Staatsblad-fallback, articles that remain NIET-VERIFIEERBAAR are
**frozen** for the duration of the micro-cycle: any edit touching their text
block, competent_authority value, or url anchor is blocked until the next drift
pass. Other articles in the same file remain editable. The report lists frozen
articles with the failure reason (TLS, rate-limit, persistent render issue) and
a suggested retry timeframe.

No bypass. The skill never permits "skip and continue".

## Output

### Drift-rapport (per file)

```
# Drift-rapport — <file path>
bwb_id: ...
valid_from: ...
calibratie: ✅ (X/Y ijkpunten gerecalled) | ❌ (rapport invalide)

| Artikel | Verdict | Bron-modus | Detail |
|---------|---------|------------|--------|
| 1       | CLEAN   | primair    | — |
| 2       | DRIFT-structureel | primair | onderdeel z ontbreekt in YAML |
| 3       | DRIFT-tekst | primair | lid 2: "<woord1>" → "<woord2>" |
| ...     | ...     | ...        | ... |
| N       | NIET-VERIFIEERBAAR | — | TLS-fout na 3 pogingen; bevroren |

## Aggregaat
- CLEAN: a
- DRIFT-tekst: b
- DRIFT-structureel: c
- NIET-VERIFIEERBAAR (bevroren): d

## Diakritiek-aggregaat (planning, geen excuus)
Aantal artikelen waar diakritiek de enige driftbron is: e

## Bevroren artikelen (scope-restrictie)
- art. N — reden — suggested retry
```

### Resolutie-tracker entries

Each DRIFT entry becomes a row in the corpus's `resolutie-tracker.md` with
4-weg klasse 1 (Modellering-fout) and a link to the geldende wettekst. The
fix lands in `modellering-fixes-plan.md` (corpus-side, not in this skill).

### Sub-rapport diakritiek

Aggregate list of articles whose only deviation is diacritics. This is NOT an
exemption — diacritics-only drift still counts as DRIFT-tekst in the verdict
table. The sub-rapport exists only to make a corpus-wide reconciliation
plannable (one PR that restores accents corpus-wide, rather than per-article).

## Integration with `regelrecht-stelselanalyse`

- Inserted as Step 0 of every micro-cycle that may touch regulation YAMLs.
- Findings → `resolutie-tracker.md` (status: `drift-gerapporteerd` /
  `drift-opgelost`).
- Fixes → `modellering-fixes-plan.md` as 4-weg klasse 1.
- A micro-cycle may only collect findings on other axes (wetgevings-fouten,
  untranslatables, coverage, source-refs) on articles that are CLEAN or whose
  DRIFT-tekst is closed within the same cycle. Otherwise the finding is
  mis-classified and rejected at synthesis time.

## What this skill does NOT do

- It does not edit YAMLs. It only reports.
- It does not "fix" errata in the geldende wet. Errata are preserved verbatim
  in the YAML; the wetgevings-fout is reported elsewhere.
- It does not decide on diacritics policy. It reports the drift; a separate
  corpus-wide reconciliation cycle decides whether to align the YAMLs to the
  wet (verbatim) or to leave them — but the report is unambiguous.
- It does not bypass under load. A flaky network produces scope-restrictie,
  not a green report.

## Files in this skill

- `SKILL.md` — this document (process).
- `reference.md` — URL patterns, the single allowed whitespace normalization
  algorithm, prompt templates, verdict criteria, output format.

## Hard rules

- **Dossier-agnostisch.** No corpus content, no concrete drift examples, no
  references to specific findings — those belong to the corpus the skill runs
  against, not to the skill itself.
- **Verbatim is wet.** No normalization beyond the single intra-paragraph
  whitespace rule.
- **Structure before text.** Always.
- **Calibratie vóór rapport.** A report without passed calibration is invalid.
- **Strict, no bypass.** Scope-restrictie handles partial failure; nothing
  handles "skip this cycle's drift check".
- **No push without permission.** Inherits the stelselanalyse protocol.

---
name: citation-traceability-audit
version: 2.2.0
description: Audit bibliographic traceability (matrix SoT) and literature grounding (papers/) before submission; auto-generate references.md
---

# Citation Traceability Audit Skill

## Purpose
Apply static analysis principles to mechanically verify that every citation marker and footnote in manuscript chapters matches the bibliographic SoT (`docs/literature/literature-matrix.md`) and content SoT (`docs/literature/papers/*.md`), auto-generating `docs/chapters/references.md` as a derived output.

## Trigger Conditions
- **Before new writing or major edits to a chapter/section** (Grounding Audit — blocking gate)
- Upon completing each manuscript chapter
- During the automated pre-submission quality gate

## Workflow (5-Step Mechanical Audit & Auto-Generation)

```text
[Step 1: Extract Citations] -> [Step 2: Matrix Cross-Reference] -> [Step 2.5: Grounding Audit] -> [Step 3: Auto-Generate references.md] -> [Step 4: Final 1-to-1 Re-Audit]
```

### Step 1: Extract Manuscript Citation Markers
Run `scripts/check_citation_format.py` to mechanically extract all inline citations and footnotes `[^1]` from `docs/chapters/`:

```bash
python3 scripts/check_citation_format.py docs/chapters/
```

### Step 2: Cross-Reference against Literature Matrix (SoT)
Cross-reference extracted manuscript citations against `docs/literature/literature-matrix.md`:

```bash
python3 scripts/check_citation_format.py --matrix docs/literature/literature-matrix.md docs/chapters/
```
- **Unregistered Citation Detection**: If a manuscript citation is missing from `literature-matrix.md`, halt and return to primary literature ingestion.

### Step 2.5: Literature Grounding Audit — **new in v2.0.0**

`literature-matrix.md` is an index (Discovery artifact) and is NOT sufficient citation evidence. Verify each citation has a grounded artifact under `docs/literature/papers/*.md`, joined by DOI/arXiv ID (preferred) or author+year frontmatter:

```bash
python3 scripts/check_literature_grounding.py docs/chapters/ \
  --papers-dir docs/literature/papers/ \
  --matrix docs/literature/literature-matrix.md
```

**Verdicts**:
- **FAIL**: no matching `papers/*.md` → **block writing** (fact-grounding-rule §5)
- **WARN**: `status: manual-stub` or `abstract-only`, or insufficient body text, or **`status: full-text` without `_downloads/{slug}.pdf`**
- **PASS**: `status: full-text` with sufficient extracted text **and** a matching PDF under `_downloads/`

**Required `papers/*.md` frontmatter**: `title`, `authors`, `year`, `doi`, `arxiv_id`, `status`, `source_url`, `version`

**Output**: `docs/design/literature-grounding-report.md`

> ⚠️ **Books & theses**: use `status: manual-stub` with page-referenced excerpts (fact-grounding-rule §2-B-3).
> ⚠️ **Primary-source PDFs**: do not gitignore `_downloads/`. A `full-text` claim is re-auditable only against the PDF. Do not store PDFs the user has no right to redistribute (see DISCLAIMER).
> ⚠️ **Bot challenges (reCAPTCHA / Cloudflare)**: When automated download returns `bot-challenge … human handoff required`, keep WARN/stub until the user places the PDF at `_downloads/{slug}.pdf` via browser ([`pdf-paper-ingestion`](../pdf-paper-ingestion/SKILL.md) Step 1b).

### Step 3: Auto-Generate `references.md`
Auto-generate `docs/chapters/references.md` from `literature-matrix.md`:

```bash
python3 scripts/check_citation_format.py --generate-references docs/chapters/references.md --matrix docs/literature/literature-matrix.md docs/chapters/
```

> ⚠️ **SoT Rule**: `literature-matrix.md` is the bibliographic SoT; `literature/papers/*.md` is the content evidence SoT. `references.md` MUST be auto-generated only.

### Step 4: Final 1-to-1 Audit
Re-run audit to confirm 0 missing definitions and 0 orphan references.

## Outputs
- Auto-generated `docs/chapters/references.md`
- Literature grounding report `docs/design/literature-grounding-report.md`
- Audit log `docs/design/citation-audit.log`

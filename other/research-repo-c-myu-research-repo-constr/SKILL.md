---
name: research-repo
description: Build, migrate, operate, and audit Git-based academic research catalogs with verifiable metadata and reproducible outputs. Use when Codex needs to initialize a literature repository, migrate an existing README or paper list, discover and triage current papers, verify metadata, deduplicate records, classify or summarize papers, maintain multilingual catalog views, manage a review backlog, or validate repository consistency. Support a platform-neutral core with optional Codex and Claude adapters.
---

# Research Repository

Create and maintain research catalogs whose public Markdown is derived from verified, structured data. Preserve useful existing repository conventions unless the user explicitly requests a redesign.

## Start Here

1. Inspect the target repository, its instructions, current files, and `git status`.
2. Identify the requested mode: initialize, migrate, discover, curate, or audit.
3. Resolve only decisions that materially affect the result: research scope, languages, taxonomy, notes visibility, and optional agent adapters.
4. Use `.research-repo/config.json`, `papers.json`, `backlog.json`, and `searches.json` as the source of truth.
5. Use `scripts/research_repo.py` for initialization. It installs `.research-repo/research_repo.py`; use that repository-local copy for later validation and rendering.
6. Summarize changed files and verification results. Commit only when the user explicitly asks.

## Non-Negotiable Rules

- Never invent titles, authors, venues, dates, identifiers, URLs, methods, metrics, or findings.
- Treat search results as candidates, not verified evidence.
- Verify metadata against a primary source or authoritative scholarly index before marking a record `verified` or `curated`.
- Record verification provenance and the date checked.
- Deduplicate by normalized DOI, arXiv identifier, and title before adding a record.
- Preserve unrelated files and user changes. Do not replace an existing license, initialize a nested Git repository, or rewrite a non-generated README without explicit approval.
- Keep shared configuration, data, validation tools, and repository instructions tracked. Ignore private notes only when the user chooses private notes.
- Do not stage, commit, push, publish, or delete source material unless the user asks.
- Do not make a network-dependent step a prerequisite for offline validation or rendering.

## Repository Contract

Use this default layout:

```text
repository/
├── .research-repo/
│   ├── config.json          # scope, languages, taxonomy, output paths
│   ├── papers.json          # canonical paper records
│   ├── backlog.json         # candidates and review state
│   ├── searches.json        # reproducible discovery history
│   └── research_repo.py     # repository-local validator and renderer
├── README.md                # generated catalog view
├── README_<lang>.md         # optional generated translations
├── TODO.md                  # generated review backlog
├── paper_notes/             # tracked or private by user choice
├── AGENTS.md                # optional Codex adapter
└── CLAUDE.md                # optional Claude adapter
```

Always track `config.json`, `papers.json`, `research_repo.py`, generated public README views, `.gitignore`, and shared adapters. Track `backlog.json`, `searches.json`, and `TODO.md` together, or ignore all three for a private review workflow. Never link from a public README to a private file.

Read [data-model.md](references/data-model.md) before creating or editing canonical records.

## Choose a Mode

### Initialize

Use for a new catalog. Read [workflows.md](references/workflows.md#initialize-a-new-catalog), then run:

```bash
python <skill-dir>/scripts/research_repo.py init <target> \
  --name "<name>" \
  --description "<scope>" \
  --languages en
```

Customize the generated generic priorities and taxonomy before adding records. Do not run `git init` or commit unless requested.

Add `--private-review-state` when candidates, search history, and TODO must remain local.

### Migrate

Use for an existing README, bibliography, spreadsheet export, or earlier Research Repo layout. Read [workflows.md](references/workflows.md#migrate-an-existing-catalog). Initialize only the v2 data layer:

```bash
python <skill-dir>/scripts/research_repo.py init <target> \
  --name "<name>" \
  --description "<scope>" \
  --languages en,zh \
  --existing
```

Preserve every source entry during extraction. Mark entries `imported` until their metadata has been re-verified.

### Discover

Use when searching for recent or foundational work. Read [workflows.md](references/workflows.md#discover-and-triage-papers). Search authoritative sources appropriate to the field, capture stable identifiers, compare against the full dataset, and add new results as `candidate`.

### Curate

Use when verifying or publishing candidates. Read [workflows.md](references/workflows.md#verify-and-curate-a-paper). Advance status only when its requirements are satisfied, then render and validate.

### Audit

Use for consistency, stale metadata, taxonomy drift, broken generated views, duplicate records, or multilingual mismatch. Read [workflows.md](references/workflows.md#audit-a-catalog), then run:

```bash
python <target>/.research-repo/research_repo.py validate <target> --check-rendered
```

## Deterministic Commands

Resolve `<skill-dir>` as the directory containing this `SKILL.md`. After initialization, the target owns a versioned copy of the deterministic tool.

```bash
# Validate canonical data only
python <target>/.research-repo/research_repo.py validate <target>

# Render README and TODO views
python <target>/.research-repo/research_repo.py render <target>

# Verify that generated views are current without writing
python <target>/.research-repo/research_repo.py render <target> --check
```

The renderer only replaces content between its managed markers. If an existing non-empty README has no markers, migrate it first; do not overwrite it.

## Agent Adapters

Keep the data model and workflow platform-neutral. When the user names the target agent environment, create its smallest shared adapter unless they decline. Otherwise create `AGENTS.md`, `CLAUDE.md`, or repository-local skills only when requested or already established in the target repository. Read [platform-adapters.md](references/platform-adapters.md) before adding an adapter. Do not ignore shared adapters by default.

## Completion Checklist

- Canonical JSON parses and passes validation.
- Stable identifiers and normalized URLs are used where available.
- No duplicate DOI, arXiv identifier, normalized title, or record ID exists.
- Every `curated` record has required language summaries and verification evidence.
- README and TODO outputs match canonical data.
- Search runs record their actual bounds, sources, queries, and new candidate IDs.
- Existing content was preserved during migration.
- No unrelated files, commits, or remote state changed.

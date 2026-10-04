---
name: docs-analysis
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: "Document requirements analysis: Analyzes concept and requirements documents in the docs/ folder, checks requirements against current code, and creates a consolidated difference report."

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [docs-analysis, requirements, code-review, diff-report, quality-assurance]
language: en
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/docs-analyse.md', 'origin_version': '1.2.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="docs-analysis banner">

> **English** — Official English version of `docs-analysis`.


# Document Requirements Analysis (English)

> Analyzes all concept and requirements documents, checks their requirements against the current code, and creates a consolidated difference report.

---

## Overview & Purpose

Analyzes all concept and requirements documents in the ../docs/ folder, checks their requirements against the current code, and creates a consolidated difference report.

---

## Naming Convention

### Prefix and Suffix
All analyzed documents receive:
- **Prefix:** `conN_` where N = analysis version (1, 2, 3, ...)
- **Suffix:** `_XX` where XX = fulfillment percentage (rounded to nearest 10)

### Archiving Threshold
- **>= 75% fulfilled:** Document is moved to `../docs/_archive/`
- **< 75% fulfilled:** Document stays in `../docs/` with prefix/suffix
- **Threshold configurable** (default: 75)

---

## Process

### Phase 1: Collect Documents
- List all *.md and *.txt files in ../docs/ (root)
- Filter out README.txt

### Phase 2: Extract Requirements
For each document:
- Read content
- Identify requirements (checklists, tables, MISSING/TODO markers)
- Categorize: Structure, Code, API, DB Schema, CLI, Feature

### Phase 3: Code Verification
For each requirement:
- Determine verification method (Glob, Grep, Read)
- Execute verification
- Mark as: FULFILLED, PARTIAL, MISSING

### Phase 4: Assessment
- Count fulfilled vs. open requirements
- Calculate fulfillment percentage (%)
- Decide: archive (>= 75%) or keep (< 75%)

### Phase 5: Generate Output
- Create REQUIREMENTS_ANALYSIS.md (summary)
- Create consense_diff.md (only open requirements, by priority)

### Phase 6: Versioning
- Scan for highest conN_ prefix
- New version = highest + 1

### Phase 7: Rename and Move
- Apply new prefix/suffix to documents
- Archive or keep

---

## Output

| File | Description |
|------|-------------|
| `conN_REQUIREMENTS_ANALYSIS.md` | Complete analysis (version N) |
| `consense_diff_N.md` | Consolidated open requirements |
| `_archive/conN_*_XX.*` | Archived (>=75%) documents |

---

## Priority Classification

| Priority | Criteria |
|:--------:|----------|
| P1 | Core functionality missing, system unusable |
| P2 | Important feature missing, workaround possible |
| P3 | Nice-to-have, improves UX |
| P4 | Cosmetic, documentation, code quality |

---

## Changelog

### 1.0.0 (2026-03-15)
- Ported from BACH v3.8.0

---

*Ported from BACH v3.8.0 | Standalone Version*

---
name: awesome-ieee-report
description: Generates IEEE-format LaTeX technical reports from project requirements and codebase evidence, using academic prose, pseudocode-only explanations, BibTeX references, and IEEEtran formatting.
---

# LaTeX Technical Report Creator

Creates IEEE-format LaTeX technical reports for software and engineering projects. The skill reads a project's requirement document (if available), analyzes the codebase for evidence, and produces a pure academic report with no code references.

## Non-Negotiable Rules

Apply these rules on every run unless the user explicitly overrides them:

1. **Language**: Report body language follows the user's preference (default: English). Turkish is used when the user explicitly requests it.
2. **Requirement-first (when available)**: Section headings and coverage are driven by the project requirement document, not by convenience. If no requirement document exists, use the standard IEEE section structure as baseline.
3. **No source code dump**: Do not paste project source code blocks into the report.
4. **Pseudocode only**: Include algorithm-level pseudocode (IEEE `algorithm` environment) for core flows instead of raw implementation code.
5. **Figures as placeholders**: All figures are inserted as labeled placeholders. Real screenshots are added manually by the author. Never generate or embed actual images during skill execution.
6. **Consistency gate**: Report statements must be checked against actual code before finalizing.
7. **NO code artifacts in report body**: Never include file paths (.dart, .py, .ts, .json, etc.), class names, function names, variable names, directory structures, or any implementation-level identifiers in the report text. The report is a pure academic document — describe WHAT the system does and HOW it works conceptually, not WHERE the code lives.
8. **Minimum 3 figures**: Every report must include at least 3 figure placeholder entries with capture intent description.
9. **Academic tone**: Write as if submitting to an IEEE conference. No informal language, no first-person singular, no code jargon. Use domain vocabulary (algorithm, module, layer, mechanism, component) instead of implementation vocabulary (service, controller, repository, widget).
10. **IEEE format**: Use `\documentclass[conference]{IEEEtran}`, minimum 4 pages in two-column format.
11. **Assignment document is not a bibliography source by default**: The requirement/assignment document defines coverage obligations, but it should not automatically appear in the final bibliography unless the user explicitly asks for it.
12. **Independent academic narration**: The report must synthesize evidence into original academic prose rather than shadowing the wording, enumeration style, or example framing of the requirement handout.
13. **Table-first compression**: Long enumerations such as option mappings, inventories, thresholds, parameter groups, and metric sets should be converted into compact `booktabs` tables when this improves IEEE two-column readability.
14. **Float hygiene**: Avoid placing several large tables/figures back-to-back in the same local area when this creates obvious white-space holes or pushes related prose apart; distribute floats across adjacent narrative blocks when needed.

If any rule conflicts with user instruction, follow the user instruction and explicitly note the override.

## When To Use

Use this skill when requests include terms like:
- technical report / teknik rapor
- latex report
- ieee format / ieee rapor
- project documentation / proje raporu
- conference paper / paper yazma

## Inputs

Collect these inputs first:
- Requirement source file (PDF/markdown), if available: expected sections and mandatory content
- Target scope (full project, phase, or module)
- Output directory for `.tex` and `.bib` files
- Report language preference (default: English)
- Author name(s), affiliation (university/company/department), and contact info

## Section Structure

Section headings must be derived from the project requirement document when one exists. If no requirement document is provided, use the standard IEEE technical report structure below.

As a baseline, every report should include at minimum:

1. **Introduction** — project goal, scope, motivation
2. **Related Work** — prior art, relevant literature
3. **System Architecture and Methodology** — architecture, technology stack, data management
4. **[Project-specific sections]** — one section per major functional area or contribution
5. **Evaluation / Results** — test approach, metrics, results
6. **Conclusion and Future Work** — summary, completion status, future work

Do not remove required sections from the requirement document. Additional sections are allowed only if they do not hide mandatory items.

## Workflow

```text
Report Build Progress
- [ ] Step 1: Read requirement document
- [ ] Step 2: Analyze codebase for evidence (internal only)
- [ ] Step 3: Build requirement-to-section map
- [ ] Step 4: Write LaTeX report with academic prose
- [ ] Step 5: Create BibTeX references file
- [ ] Step 6: Insert figure placeholders
- [ ] Step 7: Run quality gate
```

### Step 1: Read Requirement Document (If Available)

- If a requirement document exists, parse it to identify mandatory sections, constraints, and deliverables.
- If no requirement document is provided, proceed with the standard IEEE section structure from the Section Structure baseline.
- If a previous report exists as reference (e.g., an MD file from a prior project), use it for style cues only — not content.

### Step 2: Analyze Codebase For Evidence (Internal Only)

- Read relevant source files to understand algorithms, architecture, data models, and behaviors.
- **CRITICAL**: This is an INTERNAL step. The facts extracted inform the report prose, but file paths, class names, function names, and code identifiers must NEVER appear in the final report text.
- For each requirement, understand the implementation approach conceptually (algorithm, data structure, strategy) and describe it in academic language.
- If code and requirement conflict, note the conflict before writing.

### Step 3: Build Requirement-To-Section Map

- Convert each requirement into a report section obligation.
- Attach evidence category: architecture decision, algorithm behavior, test result, or UI behavior.
- Mark each requirement: `covered`, `partial`, `missing`.
- Do not draft prose until all mandatory items are mapped.

### Step 4: Write LaTeX Report

- Use `\documentclass[conference]{IEEEtran}` with appropriate babel language package.
- Write purely in academic prose — ZERO code identifiers anywhere.
- Use IEEE `algorithm` environment with `algorithmic` for algorithmic flows.
- Use `booktabs` tables for parameters, thresholds, and feature summaries.
- Convert list-heavy prose into tables when the content is effectively a mapping, inventory, grouped configuration, or repeated option set.
- Keep narrative flow as prose when a small table would harm readability more than help it; use judgment rather than forcing every short list into a table.
- Do NOT cite the assignment PDF/MD as a source by default; cite only external technologies, papers, algorithms, standards, or data sources actually used by the project.
- Rewrite report explanations into independent academic narration instead of echoing the assignment document's phrasing or illustrative framing.
- Use `\cite{}` for all external references.

### Step 5: Create BibTeX References

- Create a `references.bib` file with entries for all cited technologies, algorithms, and data sources.
- Include framework documentation, algorithm papers, and data sources used in the project.

### Step 6: Insert Figure Placeholders

- Insert at least 3 figure placeholder entries using `\fbox{}` blocks.
- Each placeholder must include: label, caption, capture source, and expected content description.
- The author will replace placeholders with `\includegraphics` manually after capturing screenshots.

See: [reference/image-policy.md](reference/image-policy.md)

### Step 7: Run Quality Gate

See: [checklists/quality-gate.md](checklists/quality-gate.md)

## Writing Style Contract

- **Tone**: Formal, academic, IEEE conference paper level.
- **Language**: Match the user's language preference. English by default; use Turkish when explicitly requested. Foreign technical terms with no equivalent in the report language may be kept in English.
- **Granularity**: Explain architecture and algorithm decisions, not implementation details.
- **Vocabulary**: Use domain terms NOT code terms:

| Use (Domain Term) | Do NOT Use (Code Term) |
|---|---|
| algorithm | algorithm class |
| module | module file |
| layer | layer directory |
| mechanism | service |
| component | component class |
| data access layer | repository |
| core logic | controller |

- **Allowed in report**:
  - Pseudocode (IEEE `algorithm` environment)
  - Tables (parameters, thresholds, feature comparisons)
  - Architecture descriptions in prose
  - Figure placeholders with capture intent

- **Strictly forbidden in report body**:
  - File paths (e.g., `lib/src/...`)
  - Source code blocks or inline code
  - Class/function/variable names
  - Directory structure listings
  - Any `.dart`, `.json`, `.py`, `.ts`, `.yaml` file reference

The report reader should understand the system without ever seeing the codebase.

## Output Contract

Always produce:
1. LaTeX file (`.tex`) using IEEEtran conference class
2. BibTeX file (`.bib`) with all references
3. Build README explaining how to compile
4. At least 3 figure placeholders with capture intent
5. Minimum 4 pages in IEEE two-column format

## Templates and References

- [templates/report-template.tex](templates/report-template.tex) — LaTeX skeleton
- [templates/report-template.md](templates/report-template.md) — Markdown skeleton
- [templates/figure-placeholders.md](templates/figure-placeholders.md) — Figure placeholder format
- [checklists/quality-gate.md](checklists/quality-gate.md) — Final quality checklist
- [reference/image-policy.md](reference/image-policy.md) — Figure handling rules
- [reference/style-baseline.md](reference/style-baseline.md) — Academic style baseline
- [reference/requirements-mapping.md](reference/requirements-mapping.md) — Requirement mapping guide
- [reference/repo-evidence-sources.md](reference/repo-evidence-sources.md) — Evidence gathering guide

## Example

For a minimal example output outline, see:
- [examples/sample-filled-outline.md](examples/sample-filled-outline.md)

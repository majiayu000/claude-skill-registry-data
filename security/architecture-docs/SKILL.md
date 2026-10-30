---
name: architecture-docs
description: "Create, edit and query ARCHITECTURE.md and its docs/: creating or continuing an architecture, editing sections, generating Mermaid / C4 diagrams (Workflow 8), migrating to the docs/ layout (Workflow 9), prose restyle (Workflow 12), validating or auditing the architecture (BIAN, ENTERPRISE, standards), and answering questions about documented components, data, integrations, security, performance, deployment, technology or decisions."
triggers:
  # Workflow 8 — diagram generation
  - generate my architecture diagrams
  - create architecture diagrams
  - add diagrams to my architecture
  - update diagrams
  # Workflow 9 — multi-file docs/ layout migration
  - migrate my architecture
  - restructure architecture
  - split ARCHITECTURE.md
  # Workflow 12 — prose style retrofit
  - restyle architecture
  - fix documentation prose
  - apply prose style
  - migrate to prose contract
  # Workflow 1 — continue a create after a checkpoint
  - continue the architecture
  - continúa la arquitectura
  - resume the architecture
---

# Architecture Documentation Skill

This file is a **router**: it detects the workflow, names the one guide that workflow loads, and
holds the few rules every workflow shares. The procedures live in the guides listed under
"Workflows" below and are loaded only when their workflow fires. Content templates are in
`ARCHITECTURE_DOCUMENTATION_GUIDE.md`; the editing protocol (Context Anchor, Section 3 gate,
Post-Write Audit, propagation) is in `EDIT_WORKFLOW.md`.

## Section number vs file prefix

Internal section numbers (S1–S13) and file prefix numbers (01–11) are **independent** and do NOT align.

| Internal Section | Name | File |
|---|---|---|
| S1+S2 | Executive Summary + System Overview | `docs/01-system-overview.md` |
| S3 | Architecture Principles | `docs/02-architecture-principles.md` |
| S4 | Architecture Layers | `docs/03-architecture-layers.md` |
| S5 | Component Details | `docs/components/` |
| S6 | Data Flow Patterns | `docs/04-data-flow-patterns.md` |
| S7 | Integration Points | `docs/05-integration-points.md` |
| S8 | Technology Stack | `docs/06-technology-stack.md` |
| S9 | Security Architecture | `docs/07-security-architecture.md` |
| S10 | Scalability & Performance | `docs/08-scalability-and-performance.md` |
| S11 | Operational Considerations | `docs/09-operational-considerations.md` |
| S12 | ADRs | `adr/` directory |
| S13 | Risks and Technical Debt | `docs/10-risks-and-technical-debt.md` |
| — | References | `docs/11-references.md` |

- "update Section 9" → **S9** = `docs/07-security-architecture.md`, never `docs/09-*`; `docs/09-*` is **S11**.
- Use S-prefixes for sections and file paths for files. Never assume prefix `NN` = section `N`.
- **Legacy layouts** (References at `docs/10-references.md`, no S13 file): any workflow on an existing multi-file project runs Workflow 11 as a preflight first.
- **A section file that does not exist is absent, not empty.** Every consumer — this skill and every other — follows `references/MISSING_SECTION_CONTRACT.md`: detect before reading, emit the contract's block, stop the affected output, never infer. Workflow 11 Case B backfills the file.

**This table is the single copy.** `ARCHITECTURE_DOCUMENTATION_GUIDE.md` and `QUERY_SECTION_MAPPING.md` point here rather than restating it.

## When this skill is invoked

- Create, update, edit or maintain `ARCHITECTURE.md` / `docs/**`; document a system's architecture.
- Review, audit or analyse an architecture (BIAN / ENTERPRISE / standards conformance; Design Drivers).
- Edit S1 Key Metrics (metric consistency check) or any downstream section S4–S11 (Context Anchor).
- **Informational questions about the documented architecture** — "what is our authentication approach", "how does X work", "what do we use for Y", "according to the architecture…", "check / validate / verify the architecture …" — and keywords: components, services, data flow, schema, APIs, integrations, security, scaling, SLA, deployment, tech stack, versions, decisions, trade-offs, ADR, BIAN, ENTERPRISE, service domain, layer.
- Generate / update diagrams (Workflow 8).

**Do NOT activate for** (redirect): release, version status, release readiness, tag recovery, deprecation → `architecture-lifecycle`; requirements traceability or PO Spec coverage → `architecture-traceability`; component add / remove / rename / index sync / C4 migration → `architecture-component-guardian`; compliance contracts → `architecture-compliance`; ADR creation / status / supersede → `architecture-definition-record` (this skill only *reads* `adr/*.md`).

**Component operations delegation**: every structural operation on `docs/components/` — creating, renaming, deleting a component file, writing `docs/components/README.md`, migrating to the C4 multi-system layout, adding C4 metadata — delegates to `architecture-component-guardian`. This skill reads component files for context and never restructures them.

## Workflow detection

Match the user's original message against these patterns, in this order, and jump straight to the workflow — do not ask which one.

| Workflow | Triggers | Then |
|---|---|---|
| **8 Diagrams** | generate / create / add / update / make + diagram(s); "Mermaid diagrams"; reconcile / consolidate / audit diagrams; diagram coverage or placement; an external diagram file | Confirm "I'll help you generate architecture diagrams." → Workflow 8 Step 1. Only for an **existing** architecture — a new one gets its diagrams from Workflow 1 Step 7 |
| **9 Migrate** | migrate / restructure / split / reorganize / convert + architecture; "too large", "hard to navigate" | Confirm → Workflow 9 Step 1 |
| **12 Restyle** | restyle architecture, fix documentation prose, apply prose style, migrate to prose contract; `/restyle-architecture` (`--dry-run`, `--file <glob>`, `--force`) | Confirm → read `PROSE_RETROFIT_WORKFLOW.md` → Step 1 |
| **11 Layout gate** | "migrate layout", "backfill missing section", "create the risks section" — or any workflow's preflight on an existing multi-file project | Read `LAYOUT_MIGRATION_WORKFLOW.md`; on completion resume the original workflow |
| **Review / audit** | "review my architecture", "audit architecture", conformance review | Read `REVIEW_AUDIT_WORKFLOW.md` |
| **1 Resume** | "continue the architecture", "continúa la arquitectura", "resume the architecture" — or a create request where `.cache/sa-skills/collect.json` exists and `create-progress.js` reports the create unfinished | Read `workflow1/resume.md` — never re-runs Steps 0.1–4.9 |
| **1 Create** | no `ARCHITECTURE.md`; "create architecture documentation"; change architecture type | Read `ARCHITECTURE_TYPE_SELECTION_WORKFLOW.md` — starts at Step 0.1 |
| **2 Edit** | edit / update / add to an existing `docs/` file or section | Read `EDIT_WORKFLOW.md` |
| **3 / 7 Query** | a question about the documented architecture | Read `ARCHITECTURE.md`; `QUERY_SECTION_MAPPING.md` when the section is not obvious |
| Metrics · Design Drivers | "verify / audit metrics", S1 Key Metrics edit · "calculate / update design drivers", "architecture review" | `METRIC_CALCULATIONS.md` · `DESIGN_DRIVER_CALCULATIONS.md` |

No pattern → acknowledge the invocation, list the workflows in one line each, and ask.

## Lazy-Load Contract — workflow-gated guides

Every guide below is loaded **only when its row's workflow fires**, never speculatively; loading one outside its trigger wastes context and invalidates the prompt-cache prefix when the user switches workflows. `llms-full.txt` is never read whole.

> Line counts are verified by `bun scripts/check-lazyload-sizes.ts` (fails on >5 % drift; `--fix` rewrites). Do not hand-edit them.

| Guide | Size (lines) | Triggering workflow / signal |
|---|---|---|
| `ARCHITECTURE_TYPE_SELECTION_WORKFLOW.md` | ~135 | Workflow 1 — the **router**: trigger, the five types, the load map of the six parts below, the type-specific validation summary. Read whole, then the parts by step |
| `workflow1/00-gates-run.md` | ~52 | Workflow 1, Steps 0.1–0.65 on the common path — read at Step 0.1 |
| `workflow1/00-gates.md` | ~637 | Workflow 1, Steps 0.1–0.65 in full — read only by the line range `gates-check.js` names |
| `workflow1/resume.md` | ~37 | Workflow 1 continued after a checkpoint — read instead of Step 0.1 |
| `workflow1/01-type-selection.md` | ~116 | Workflow 1, Steps 1–4 — read when the run reaches that step |
| `workflow1/05-sections.md` | ~140 | Workflow 1, Step 5 — the loop and the order; read when the run reaches that step |
| `workflow1/05-auto.md` | ~53 | Workflow 1, Step 5 with automatic checkpoints — segment-runner dispatches, in series |
| `workflow1/05-components.md` | ~190 | Workflow 1, Step 5 — Section 5 (item `s5`) only |
| `workflow1/05-index.md` | ~90 | Workflow 1, Step 5 — `ARCHITECTURE.md` (item `index`) only |
| `workflow1/05.7-hygiene-gate.md` | ~110 | Workflow 1, Step 5.7 — read when the run reaches that step |
| `workflow1/06-adrs.md` | ~29 | Workflow 1, Step 6 — read when the run reaches that step |
| `workflow1/07-diagrams.md` | ~319 | Workflow 1, Step 7 — read when the run reaches that step |
| `ARCHITECTURE_DOCUMENTATION_GUIDE.md` | ~2,144 | Workflow 1 section templates; Workflow 11 backfill scaffolds; a Workflow 2 edit that needs a section's template — read the section's block, not the whole file |
| `EDIT_WORKFLOW.md` | ~406 | Workflow 2 — Context Anchor, Section 3 Enforcement Gate, Post-Write Audit (Checks A–F), Step 5.5 propagation with the Phase 1.5 Principle Alignment Audit, navigation-index rules. Workflow 1 Step 5 reads its "Section 3 Enforcement Gate" block |
| `references/LANGUAGE_POLICY.md` | ~450 | Any workflow that writes a project file — Workflow 1 Step 0.1; the Language Resolution step of Workflows 2, 8, 9 — read §3 (resolution) and §4 (do-not-localize); §5 only when localizing a heading |
| `MERMAID_DIAGRAMS_GUIDE.md` | ~1,024 | Workflow 8 and Workflow 1 Step 7 (diagram generation) |
| `references/DIAGRAM-GENERATION-GUIDE.md` | ~1,054 | Workflow 8 and Workflow 1 Step 7 whole. **Any write that adds or changes a connection label** on Diagram 2 / 3 / 4 — a Workflow 2 edit, a guardian regeneration, an ad-hoc request — reads only its Load map's "label edit" rows (§ Design Language Governance + § Pre-Write Validation) |
| `LAYOUT_MIGRATION_WORKFLOW.md` | ~125 | Workflow 11 |
| `PROSE_RETROFIT_WORKFLOW.md` | ~90 | Workflow 12 — stages, fact rule, qualifier and retired-claim review |
| `QUERY_SECTION_MAPPING.md` | ~650 | Workflow 3 / 7 when the section is not obvious from `ARCHITECTURE.md` |
| `DESIGN_DRIVER_CALCULATIONS.md` | ~593 | "calculate / update design drivers", "architecture review" Design Drivers branch |
| `METRIC_CALCULATIONS.md` | ~350 | Section 1 Key Metrics edits, "verify metrics", "audit metrics" |
| `PRINCIPLE_VALIDATION.md` | ~509 | Section 3 Enforcement Gate Layer 1 — every write to `docs/02-architecture-principles.md` runs `scripts/principle-check.js`; read this file only to interpret a finding (the rule's fix text) and for the Appendix A scope in force — never to run the rules by hand |
| `PROSE_VALIDATION.md` | ~550 | The prose contract as rules — **run as `scripts/prose-check.js`** at Step 5.7 check 3 (`--scope first-write`), Post-Write Check F (`--scope edit --file`), the release check (`architecture-lifecycle`, `--scope release`) and Workflow 12; read this file only for the fix text of a rule the report names, never to run the rules by hand |
| `references/PROSE_STYLE.md` | ~315 | Authoring guidance; a finding you need to interpret |
| `references/ASSET_REGENERATION_ADVISORY.md` | ~70 | Workflow 2 Phase 5 — shared with `architecture-definition-record` |
| `RESTRUCTURING_GUIDE.md` | ~154 | Workflow 9; the `ARCHITECTURE.md` navigation-index template |
| `VALIDATIONS.md` | ~1,404 | §2 section-name / anchor rules, §3 structure, §4 type-specific checks. Read the one section a gate finding names — never whole. §1 and §1.7 are pointers to `PRINCIPLE_VALIDATION.md` and `PROSE_VALIDATION.md` |
| `REVIEW_AUDIT_WORKFLOW.md` | ~1,017 | "review my architecture", "audit architecture", conformance review |
| `references/MISSING_SECTION_CONTRACT.md` | ~60 | Any skill that finds a section file absent |
| `references/CONTEXT7_ENRICHMENT.md` | ~40 | Workflow 1 Step 5 component files, when context7 is configured |
| `references/{TYPE}-ARCHITECTURE.md` + `{TYPE}-TO-C4-TRANSLATION.md` | ~400–1,000 each | Workflow 1 Step 3 — only the chosen type's pair (mapping table in `ARCHITECTURE_TYPE_SELECTION_WORKFLOW.md` Step 3); `references/ICEPANEL-C4-MODEL.md` is the governing C4 reference for all types |
| `[design_language_dir]/llms-rules.txt` | ~695 | Workflow 8 / Step 7 generation whole **when the folder is present**. A label-only write reads §5 (rg `^## 5`, read that range). Any Diagram ID, label, tag or export question |
| `[design_language_dir]/llms-mermaid.txt` | ~509 | With the digest, for any Mermaid block written in governed mode |
| `[design_language_dir]/llms-full.txt` | ~5,718 (~115K tokens) | **Never read whole.** Grep the `##` heading, read that range — Appendix B, C or E |
| `[design_language_dir]/bian-registry.json` | ~762 | Resolving a `DOM` / `CAP` code or a BIAN id |
| `[design_language_dir]/bian/llms-bian.txt` | ~431 | A Service Domain's location or API link; one area file on its pointer, never all nine |

**Rules**

- Do not pre-load a guide "to be ready"; do not chain into another workflow's guides.
- **Section-scoped reads.** A guide that carries a *Load map* is read by the rows the current step names: `rg -n '^## '` for the heading, then `Read` that range. Whole-file reads are for the guides without one.
- **Read once per run.** A project file (`ARCHITECTURE.md`, `docs/**`, `adr/*.md`) or a guide already in context is reused, never re-read; a file is re-read only after this skill has written to it in the same run. Verify an `Edit` by grepping the edited anchor. The sub-agent fan-outs inline the foundational files once per batch (`EDIT_WORKFLOW.md` Phase 1.5).
- Type-specific references: load only the pair matching `<!-- ARCHITECTURE_TYPE: -->`, never all five. Design-language editions: load one, chosen by `DOC_LANGUAGE`, never both.
- The Section 3 gate's Layer 2 runs in `agents/reviewers/principle-quality-reviewer.md` through the Agent tool, so its reads do not enter this context.

## File naming and location

- `ARCHITECTURE.md` at the project root is the **navigation index only**; every section lives in `docs/NN-kebab-case-name.md` (lowercase, hyphens, English filenames in every language); components in `docs/components/` (one file each, guardian-owned). Template and directory tree: `RESTRUCTURING_GUIDE.md`.
- Update the navigation index only when a `docs/NN-*.md` file is added, renamed or removed, or an ADR is accepted (ADR table) — never for content edits, typos or metric changes; component rows go through the guardian. The index carries no line numbers.
- Multi-project repositories: each project directory holds its own `ARCHITECTURE.md` + `docs/`.

## Language Resolution

Every workflow that writes a project file resolves the documentation language first. Workflow 1 asks (Step 0.1); Workflows 2, 7, 8 and 9 resolve and never ask unless nothing is recorded. Contract: `references/LANGUAGE_POLICY.md` §3.

```bash
rg -m1 '<!-- DOC_LANGUAGE:' ARCHITECTURE.md || rg -m1 '<!-- LANGUAGE:' ARCHITECTURE.md
```

1. `DOC_LANGUAGE` found → adopt it silently.
2. Legacy `LANGUAGE` found → adopt it, rewrite the marker as `DOC_LANGUAGE`, proceed.
3. Neither → infer from the first 30 lines of `docs/01-system-overview.md` (policy §5.5), ask **once** (`🌐 No documentation language recorded … Inferred: Español (es). Confirm? [1 = yes / 2 = no, use en]`), stamp `<!-- DOC_LANGUAGE: xx -->` right after `ARCHITECTURE_RELEASED`, proceed. Fires at most once per project.
4. A value outside `en` | `es` → treat as absent.

The value governs everything authored into a file — headings, prose, table cells, diagram node labels, `EXPLORER_HEADER` values, CHANGELOG prose. It never governs the machine layer (policy §4) or the messages shown to the user, which stay English. Structural headings carry their English `SECTION:` / `PRINCIPLE:` / `LABEL:` anchor in every language.

## Workflows

**1 — Create** (`ARCHITECTURE_TYPE_SELECTION_WORKFLOW.md`). Every section is written from its payload — `bun [plugin_dir]/skills/architecture-docs/scripts/section-prepare.js <project_root> --section <N>` → `.cache/sa-skills/payloads/section-NN.md` (the guide by range, the type templates, the inputs, the parents as outlines, the facts as tables, a manifest of what is missing) — never from the whole guide, and **in this session** — no sub-agent, except that with automatic checkpoints a segment runs in a `segment-runner` sub-agent. The guide and the templates do not enter the main context; the payload does, one section at a time. The entry gates run by code (`scripts/gates-check.js`, `workflow1/00-gates-run.md`; `00-gates.md` is read by line range only), and the run stops at four checkpoints (`scripts/create-progress.js`) so each segment starts in a clear session — a continued create reads `workflow1/resume.md`; with automatic checkpoints segments 2–4 run in series in `segment-runner` sub-agents instead (`workflow1/05-auto.md`). Steps 0.1 Language gate → 0.2 PO Spec gate → 0.3 Capability Alignment gate (the declared framework's report — mandatory once one is declared, `none` passes) → 0.4 HLD Intake gate → 0.5 supplementary context → 0.6 ADR Context Block → 1–4 type selection, templates (the chosen type's pair only), metadata → 5 multi-file creation (Section 3 gate from `EDIT_WORKFLOW.md`; component files may use `references/CONTEXT7_ENRICHMENT.md`) → 5.7 Content Hygiene Gate (`scripts/prose-check.js --scope first-write` as check 3, the EXPLORER_HEADER contract check `explorer-cli.ts check` as check 2b — blocking — plus the size-budget report `scripts/docs-stats.js` as check 4 — WARNING only; budgets in `ARCHITECTURE_DOCUMENTATION_GUIDE.md` → "Authoring budgets") → 6 ADR delegation → 7 mandatory diagrams (DIAGRAMS_GATE, blocking, no skip). Reference for Section 6's Phase Catalog mode: `examples/04-data-flow-patterns.example.md`.

**2 — Edit** (`EDIT_WORKFLOW.md`). Facts first (`bun [plugin_dir]/skills/architecture-docs/scripts/arch-facts.js <project_root>` → `.cache/sa-skills/facts.json`; names, ids, statuses and catalogs by `--section`, never by reopening a document) → find the target file through the navigation table → Context Anchor (universal foundation + section parents + matched ADRs; Section 3 gate for `docs/02`) → read the target once → Edit with source attribution → Post-Write Audit A–F → Step 5.5 propagation → Phase 5 asset advisory. Match the file's language; add anchors to the headings you touch. A change to a connection label on Diagram 2 / 3 / 4 is a diagram write: run the design-language gate below and the Connection Label Check before writing it.

**3 / 7 — Query.** Run `bun [plugin_dir]/skills/architecture-explorer-headers/utils/explorer-cli.ts findings <project_root> --query "<the question's 3–8 terms>"` first: it names the files, lines and headings where the terms appear, at no model cost. Read only the matched section ranges (`Read` with offset / limit around the reported lines); open a whole `docs/` file only when the findings are empty or the answer spans the file. `QUERY_SECTION_MAPPING.md` when the section is still unclear. Answer with file-path citations.

**8 — Diagrams.** Load `references/DIAGRAM-GENERATION-GUIDE.md` and `MERMAID_DIAGRAMS_GUIDE.md`; when `[design_language_dir]/llms-rules.txt` exists, load it and `llms-mermaid.txt` too and apply them in preference where they differ (governed mode: Diagrams 2 / 3 as `flowchart TB`, Diagram 4 keyword `flowchart`, the §9 palette directive, `sequenceDiagram` per §12). Four standard diagrams under `## Architecture Diagrams` in `docs/03-architecture-layers.md` (a Logical View `flowchart TB` replaces any ASCII block; one fixed four-role palette, no dark variant, on Diagrams 1 and 4; `<!-- DIAGRAM_THEME: -->` applies to Diagrams 2 / 3 and the sequences in fallback mode only); sequence diagrams in `docs/04-data-flow-patterns.md`. Node labels, participants, notes and flow names in `doc_language`; diagram headings, Mermaid keywords and the `classDef` role names stay English. **Every diagram write ends with `bun [plugin_dir]/skills/architecture-docs/scripts/mermaid-check.js docs/03-architecture-layers.md docs/04-data-flow-patterns.md [<other file>]`** — the Pre-Write checklist as code plus a mermaid-cli render when it is installed; a failing block is fixed at the line named before the diagram is accepted (a block that fails there exports as source, not as a picture). **Every write of `docs/04` ends with `bun [plugin_dir]/skills/architecture-docs/scripts/flow-compose.js <project_root>` then `flow-check.js <project_root>`** — the composer derives `§ End-to-End Wire Sequences` from the Phase Catalog panels each flow's `**Phases**:` line declares (steps relabelled `N.M`, participants unioned by name, a hand-authored sequence kept where nothing derives), and the check holds the file to itself; after the composer, `phase-absent` can only remain where a flow declares no phases. **Every write of a connection label ends with `bun [plugin_dir]/skills/architecture-docs/scripts/label-check.js <file.md>`** — the Connection Label Check as code, registries read from the bundled `rules-registry.json` at run time (skipped, and said so, when the folder is absent); a failing label is fixed before the block is accepted, and `llms-rules.txt` §5 is opened only to resolve a failure the receipt cites.

**9 — Migrate to `docs/`** (`RESTRUCTURING_GUIDE.md`). Six steps: analyze, propose layout, extract files, rewrite `ARCHITECTURE.md` as the index, update external references, verify. Preserves the source language; adds `SECTION:` anchors while extracting; stamps `DOC_LANGUAGE`.

**Release** is `architecture-lifecycle` (status, release check, release, tag recovery, deprecation).

**11 — Layout gate** (`LAYOUT_MIGRATION_WORKFLOW.md`). Case A: `docs/10-references.md` exists and no S13 file → rename + scaffold + rewrite links + navigation. Case B: numbering current but a section file is missing → scaffold it from its template block. Resumes the calling workflow.

**12 — Prose retrofit** (`PROSE_RETROFIT_WORKFLOW.md`). `scripts/prose-check.js --scope release` (with the judge where a key is set — a dismissed candidate is a rewrite not made), staged fixes safest first, then stamp `<!-- PROSE_STYLE: v1 -->`.

**Review / audit** (`REVIEW_AUDIT_WORKFLOW.md`) · **Metrics** (`METRIC_CALCULATIONS.md`) · **Design Drivers** (`DESIGN_DRIVER_CALCULATIONS.md`).

## Design Language Standard — gate

The standard is organization-specific: an institution pack supplies it; the base carries none. `[design_language_dir]` is the Design Language Standard in force — `bun [plugin_dir]/scripts/shared/packs.js --path design-language` prints it (an institution pack's — the base carries none) or prints nothing and exits 1: **fallback mode**. Before any write of a connection label, Diagram ID, tag or export value, resolve it. **Present** → it governs those topics and `DIAGRAM-GENERATION-GUIDE.md` is informative for them; load one edition by `DOC_LANGUAGE`; every registry is closed — an unregistered value is a vocabulary extension request to the Architecture Governance Board, never an invention. **Absent** → the guide governs; never reconstruct the standard from memory. Full load contract, the write trigger and the escalation to `llms-full.txt`: `[design_language_dir]/README.md` → "Load contract" and "Governance inside architecture-docs".

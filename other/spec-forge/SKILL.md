---
name: spec-forge
description: >
  Professional specification system for Codex. Use when the user asks to create,
  improve, review, audit, analyze, or propagate product/software documentation,
  including requirements documents to hand to an implementation team or vendor,
  SRS/functional/non-functional requirements, PRDs and business cases, ideas,
  technical designs, architecture/RFC docs, feature specs, test cases,
  documentation audits, document landscape analysis, and full idea-to-spec
  chains. The chain's spine is a delivery-grade requirements spec followed by a
  technical design, handed off to code-forge for implementation:
  [idea] -> [decompose] -> [prd] -> srs -> tech-design -> review.
version: 1.0
subcommands:
  - idea
  - decompose
  - tech-design
  - prd
  - srs
  - test-cases
  - review
  - audit
  - analyze
  - propagate
---

# Spec-Forge Orchestrator

Spec-forge is a documentation and specification workflow suite. This root skill is
the Codex-facing orchestrator: decide which child skill to load, keep the document
chain coherent, and avoid loading large generation references until they are needed.

## Trigger Patterns

Use this skill when the user asks for any of the following:

- Start or refine an idea before specs: use `skills/idea/SKILL.md`
- Split a large project into sub-features: use `skills/decompose/SKILL.md`
- Write a PRD, business case, or product definition — "is this worth building": use `skills/prd-generation/SKILL.md`
- Write the requirements a team will be held to — a requirements spec, an SRS, functional/non-functional requirements, **a requirements document to hand to an implementation team or vendor**: use `skills/srs-generation/SKILL.md`
- Write a technical design, architecture doc, design doc, or RFC: use `skills/tech-design-generation/SKILL.md`
- Generate test cases, QA coverage, or a test case matrix: use `skills/test-cases-generation/SKILL.md`
- Review spec-forge documents for quality and consistency: use `skills/review/SKILL.md`
- Audit project docs against code: use `skills/audit/SKILL.md`
- Analyze a document ecosystem for themes, conflicts, gaps, redundancy, or staleness: use `skills/analyze/SKILL.md`
- Propagate an upstream doc change downstream: use `skills/propagate/SKILL.md`
- Run the full chain for a feature: orchestrate `[idea] -> [decompose] -> [prd] -> srs -> tech-design -> review -> handoff to code-forge`

**Routing the ambiguous "write me a requirements document".** When the user says
"需求文档", "requirements doc", or "spec" without qualifying it, the deciding
question is whether the decision to build has already been made. If it has — the
user knows what they want and needs it specified precisely enough to implement
against — route to **SRS**. If it has not — the user is making a case, seeking
approval, or sizing an opportunity — route to **PRD**. When genuinely unclear,
ask that one question rather than guessing; producing the wrong document wastes
the entire generation.

Also treat slash-like requests as aliases:

| User request | Route |
|---|---|
| `/spec-forge <name>` | Full chain |
| `/spec-forge:idea <name>` or `/idea <name>` | Idea |
| `/spec-forge:decompose <name>` or `/decompose <name>` | Decompose |
| `/spec-forge:tech-design <name>` or `/tech-design <name>` | Tech Design |
| `/spec-forge:prd <name>` or `/prd <name>` | PRD |
| `/spec-forge:srs <name>` or `/srs <name>` | SRS |
| `/spec-forge:test-cases <target>` or `/test-cases <target>` | Test Cases |
| `/spec-forge:review <name>` or `/review <name>` | Review |
| `/spec-forge:audit [path]` or `/audit [path]` | Audit |
| `/spec-forge:analyze [path]` or `/analyze [path]` | Analyze |
| `/spec-forge:propagate ...` or `/propagate ...` | Propagate |

The `commands/*.md` files are compatibility command definitions from the original
Claude-oriented implementation. In Codex, prefer reading the child `skills/*/SKILL.md`
files directly. Use `commands/spec-forge.md` only as an additional orchestration
reference if you need more detail about the full chain.

## Progressive Loading

Keep context small.

1. Read this root file first.
2. Read only the child `SKILL.md` matching the user's request.
3. When a child skill references `skills/shared/project-context.md`, read it if the workflow needs code/project awareness.
4. When a child skill references `skills/shared/doc-first.md`, apply it before generating or editing docs.
5. When a child skill invokes the script layer, read `skills/shared/scripts.md` once to resolve `<sf_scripts>`; do not read the scripts' source unless you need to debug them.
6. Read generation references, templates, or checklists only when that child skill explicitly needs them.

Do not bulk-load every child skill. Do not read every reference folder just because
the suite is complex.

## Global Rules

- Preserve the user's requested language. If the user writes in Chinese, respond and write user-facing explanations in Chinese unless the target document convention requires English.
- Treat docs as current truth, not history. Before generating a new spec, scan for existing related docs and decide whether to reuse, edit, or create.
- Do not create parallel versions such as `prd-v2.md`, `new-tech-design.md`, or addendum files. Edit the canonical file in place unless no canonical document exists.
- Keep traceability stable: preserve existing requirement IDs, feature names, component names, and section titles unless the user explicitly asks to rename them.
- When changing upstream docs, identify downstream impact. Either update affected downstream docs or recommend/run the propagate workflow.
- Every finding in review, audit, analyze, or propagate output must cite concrete files/sections. Do not invent issues.
- Prefer project-local conventions and existing docs over generic templates.
- Ask only necessary questions. If existing docs or code provide the answer, use them and state the assumption.

## Shared Project Context

For generation workflows that need grounding in the actual codebase, use:

`skills/shared/project-context.md`

Apply it before SRS, PRD, tech-design, decompose, and test-cases work when the
project exists. It produces a concise summary of:

- Project profile
- Language, framework, database, auth, testing, and CI signals
- Existing documents and upstream specs
- Architecture and module boundaries
- Existing test infrastructure when relevant

For the full chain, scan project context once and reuse the summary across stages
instead of repeatedly rescanning the same repository.

## Script Layer

spec-forge ships a small layer of deterministic Python 3 (standard-library-only)
helpers under `skills/shared/scripts/` that absorb the mechanical, token-heavy
bookkeeping the skills used to do by hand — project + document scanning
(`sf-scan.py`), configuration/directory resolution (`sf-config.py`), document
structure/ID validation (`sf-verify-doc.py`), and traceability/coverage math
(`sf-trace.py`). The division of labour: **the scripts keep the record-keeping;
the model keeps the reasoning** (requirement quality, architecture trade-offs,
conflict judgement). Every skill that calls a script keeps a silent manual
fallback for when `python3` is unavailable.

How to locate and invoke the scripts, and which one does what:

`skills/shared/scripts.md`

Prefer the fast path (run the script, use its JSON) over re-deriving the same
facts by hand. Never restate a script's algorithm in prose — the script is the
single source of truth so the two cannot drift.

## Document Discipline

For any document creation or edit, apply:

`skills/shared/doc-first.md`

Minimum pre-write checklist:

1. List relevant existing docs under `docs/`, `specs/`, `design/`, `architecture/`, `ideas/`, and the project root.
2. Grep for the feature name, domain terms, requirement IDs, component names, and aliases.
3. Decide for each topic: reuse existing content, extend existing content, or create new content.
4. Preserve stable IDs and terminology.
5. Note downstream docs that will need updates.

## Full Chain

The chain has one mandatory spine — **a delivery-grade requirements specification, then a technical design** — with everything else conditional on what the project actually needs. When the user asks for `/spec-forge <name>` or "run the full spec-forge chain", execute this sequence:

1. **Idea** *(conditional)*: Use `skills/idea/SKILL.md`.
   - Run when the demand itself is unvalidated: the user is exploring, the problem is fuzzy, or there is no evidence anyone needs this.
   - Skip when the user already knows what they want built.
   - Goal: validate demand and produce `ideas/{name}/draft.md`.
   - If a ready or graduated idea already exists, reuse it. If the idea is still exploring/refining, warn the user before continuing.

2. **Decompose** *(conditional)*: Use `skills/decompose/SKILL.md`.
   - Run when the scope plausibly covers several independently specifiable sub-features.
   - Skip for a single coherent feature.
   - Multi-split output: `docs/project-{name}.md` with a first-line `FEATURE_MANIFEST` block.

3. **PRD** *(conditional)*: Use `skills/prd-generation/SKILL.md`.
   - Run for a new product, a new product line, or anything needing a go/no-go decision, budget approval, or stakeholder alignment before commitment.
   - Skip when the decision to build is already made and the work is a well-understood feature — go straight to the SRS. A PRD written after the decision is ceremony.
   - Output: `docs/{name}/prd.md` — business case and product definition.

4. **SRS** *(mandatory)*: Use `skills/srs-generation/SKILL.md`.
   - **This is the spine of the chain.** It is the delivery contract: the document an implementation team — an external vendor, another team, or code-forge — is held to.
   - Output: `docs/{name}/srs.md` with `FR-*`/`NFR-*` requirements, input field rules, state machines, permission matrix, error catalogue, acceptance criteria, and change control.
   - If `docs/{name}/prd.md` exists, trace every capability into requirements. If only `ideas/{name}/draft.md` exists, derive scope and requirements from it. If neither exists, work from the user's request and state the assumptions explicitly.
   - Never skip this stage to reach the tech design faster. A design built on unstated requirements produces code whose correctness nobody can settle.

5. **Tech Design** *(mandatory)*: Use `skills/tech-design-generation/SKILL.md`.
   - Single feature output: `docs/{name}/tech-design.md`.
   - Multi-split output: one tech design per sub-feature.
   - Also generates one implementation-facing feature spec under `docs/features/` per component in §8.1, plus `docs/features/overview.md` with the dependency graph and execution order.
   - Every component must trace to the `FR-*`/`NFR-*` requirements it satisfies, and every requirement must be satisfied by at least one component.

6. **Review** *(mandatory)*: Use `skills/review/SKILL.md`.
   - Review the SRS, the tech design, and any `docs/features/*.md`.
   - Auto-fix only where the review skill permits it. Leave review comments where domain knowledge is missing.

7. **Handoff**: Report the handoff command rather than running it.
   - `/code-forge:plan @docs/features/` when feature specs were generated.
   - `/code-forge:plan @docs/{name}/tech-design.md` for a single-component design.
   - Implementation and test generation belong to code-forge. spec-forge owns requirements and design; code-forge owns implementation and verification. Tests are derived from the SRS acceptance criteria by `code-forge:tdd` — spec-forge does not produce a separate test document in the chain.

Test cases, audit, analyze, and propagate are on-demand outputs, not stages in the default chain.

## Single-Skill Routes

### Idea

Read `skills/idea/SKILL.md`.

Use for early exploration, demand validation, competitive research, and
anti-pseudo-requirement checks. Output lives in top-level `ideas/{idea-name}/`,
not under `docs/`.

### Decompose

Read `skills/decompose/SKILL.md`.

Use for deciding whether a project is one feature or several independently
specifiable sub-features. If multi-split, generate `docs/project-{name}.md`.

### PRD — the business case

Read `skills/prd-generation/SKILL.md`.

Answers **"is this worth building, for whom, and at what priority"**. Market
context, competitive landscape, demand validation, feasibility go/no-go,
personas, user stories, capability scope, success metrics, milestones, risks.
Read by stakeholders *before* commitment and largely frozen once the decision is
made. Optional: skip it when the decision to build is already settled.

Deliberately **not** in the PRD: field-level rules, state machines, error codes,
Given/When/Then acceptance criteria, solution architecture. Those are the SRS's
and tech design's job. A PRD row that needs more than two sentences is a system
behavior in the wrong document.

### SRS — the delivery contract

Read `skills/srs-generation/SKILL.md`.

Answers **"exactly what must be built, and how do we settle whether it was"**.
This is the document an implementation team — an external vendor, another team,
or code-forge — is held to, and the mandatory spine of the chain. Formal
`FR-*`/`NFR-*` requirements with main/alternative flows, **input field rules**,
**state machines including illegal-transition handling**, **permission matrix**,
**error catalogue with degradation behavior**, machine-verifiable acceptance
criteria, interface and data requirements, traceability, and **acceptance and
change control**.

Unlike the PRD, it keeps evolving through delivery — which is exactly why the
two are separate files. A requirement change must not require touching market
sizing, and internal go/no-go reasoning must not ship to an implementation
vendor.

### Tech Design

Read `skills/tech-design-generation/SKILL.md`.

Use for architecture/design docs, RFCs, API design, data model design,
deployment, observability, security, performance, alternatives, and generated
feature specs.

### Test Cases

Read `skills/test-cases-generation/SKILL.md`.

Use for test case generation, coverage matrices, test strategy, testable unit
extraction, and code/spec-driven QA planning. Honor `--formal` when requested.

### Review

Read `skills/review/SKILL.md`.

Use after spec generation to check completeness, specificity, internal
consistency, traceability, and actionability. Findings first; fixes only where
allowed.

### Audit

Read `skills/audit/SKILL.md`.

Use when auditing one project that has docs and code. It checks documentation
quality, completeness, consistency, staleness, and alignment with the codebase.

### Analyze

Read `skills/analyze/SKILL.md`.

Use for docs-only or cross-repo document landscapes. It maps themes, conflicts,
gaps, redundancies, and stale areas without assuming a single codebase.

### Propagate

Read `skills/propagate/SKILL.md`.

Use after upstream document changes. It finds downstream docs affected by changed
concepts and updates them surgically or reports unresolved stale references.

## Output Locations

Default locations:

- Ideas: `ideas/{name}/`
- PRD (business case, optional): `docs/{name}/prd.md`
- SRS (delivery contract, mandatory): `docs/{name}/srs.md`
- Tech design: `docs/{name}/tech-design.md`
- Feature specs: `docs/features/*.md`
- Test cases: `docs/{name}/test-cases.md` or the path specified by the child skill
- Project manifest: `docs/project-{name}.md`
- Audit report: `{target-docs-path}/audit-report.md`
- Analysis report: `{target-root}/analysis-report.md`

If existing project conventions differ, follow the existing convention and state
the location you used.

## Completion Criteria

Before finishing a spec-forge task:

- Confirm the requested document or report exists, or explain why it could not be written.
- Mention the exact files changed or generated.
- For generation tasks, note whether project context and existing docs were scanned.
- For review/audit/analyze tasks, summarize findings by severity and cite the report path.
- For chain tasks, summarize which stages completed, which conditional stages were skipped and why, and state the `/code-forge:plan` handoff command.
- For a full chain, confirm the SRS exists and passed its structural gate. The SRS is the chain's spine; a chain that reached a tech design without one is incomplete, not merely abbreviated.

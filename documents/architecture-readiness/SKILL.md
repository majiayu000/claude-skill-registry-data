---
name: architecture-readiness
description: >
  Requirements elicitation, discovery interviews, and creating or evaluating Product Owner
  Specifications that document business requirements before architecture design: "PO spec",
  "elicit requirements", "business context intake", "evaluate PO spec". Scores a spec against
  the readiness rubric, runs gap interviews on weak areas, and writes PRODUCT_OWNER_SPEC.md
  plus a distribution PDF under exports/. Run this before architecture-docs Workflow 1 — the
  PO Spec gate reads its output. Also keeps the spec current once the architecture evolves:
  "update the PO spec", "sync PO spec", "actualiza el PO spec" — a delta collected by code from
  the changelog, the ADRs and the flows, proposals in business language, the Product Owner's
  approval item by item, a sync marker.
triggers:
  - requirements elicitation
  - elicit requirements
  - business context intake
  - PO spec
  - evaluate PO spec
  - product owner specification
  - PO spec PDF
  - distribution PDF
  - update the PO spec
  - sync PO spec
  - actualiza el PO spec
  - align PO spec with the architecture
---

# Architecture Readiness Skill

## Description

This skill helps Product Owners document business requirements and context before architecture design begins. It provides templates and guidance for creating Product Owner Specifications that feed into technical ARCHITECTURE.md documents.

The skill includes four primary functions:
1. **Requirements Elicitation**: Guided discovery interview to surface business requirements when no PO Spec exists
2. **PO Spec Creation**: Templates and guidance for documenting business requirements
3. **PO Spec Evaluation**: Scoring methodology to assess if a PO Spec is ready for architecture team handoff
4. **Async Intake**: File-based requirements extraction from tickets, emails, or documents — produces a gap report for async follow-up

## Execution mode

The skill's own folder decides — never whether Bun answers (a Claude chat's sandbox has Bun and Node). `scripts/`
beside this file → **Claude Code**: every workflow below, as written. No `scripts/` (the chat package,
`precheck/` in its place) → **chat mode**: read `CHAT_MODE.md` and follow it instead — elicitation and drafting only, a
pre-check that reports findings and never a score, the spec delivered with `<!-- READINESS_CHECK: draft -->`.
Evaluation, the stamp, the PDF and the sync stay in Claude Code.

## Plugin directories

This skill ships in the **sa-requirements** plugin (`sa-skills` depends on it and installs it). `[plugin_dir]` is its
install: `bun ~/.claude/plugins/marketplaces/shadowx4fox-solution-architect-marketplace/scripts/plugin-root.ts --plugin sa-requirements`.
`[sa_skills_dir]` is sa-skills' (the same command without `--plugin`): the distribution PDF (workflow 5) and the sync
with the architecture (workflow 6) run its tools, and a missing one is a warning, never a blocked spec.

## Documentation Language

Resolve the project's documentation language **before writing anything**, using the protocol in
`skills/architecture-docs/references/LANGUAGE_POLICY.md` §3:

```bash
rg -m1 '<!-- DOC_LANGUAGE:' ARCHITECTURE.md || rg -m1 '<!-- LANGUAGE:' ARCHITECTURE.md
```

`DOC_LANGUAGE` → use it. Legacy `LANGUAGE` → use it and rewrite the marker as `DOC_LANGUAGE`.
Neither → infer from headings (§5.5), ask the user to confirm **once**, stamp `DOC_LANGUAGE` into
`ARCHITECTURE.md`, and never infer again. Messages this skill displays to the user stay English
in every case; only authored file content follows `doc_language`.

**In this skill**: the interview is conducted in whatever language the user writes in — that rule is unchanged and lives in `REQUIREMENTS_ELICITATION_GUIDE.md`. What is new is that the resulting `PRODUCT_OWNER_SPEC.md` and `PO_SPEC_GAP_REPORT.md` are authored in that same language, and the spec is stamped with `<!-- DOC_LANGUAGE: xx -->` at the top so `architecture-docs` Workflow 1 Step 0.1 can pre-select the matching option. The rubric dimension names, scores and the `PO_SPEC` structural anchors stay English.

This skill usually runs before `ARCHITECTURE.md` exists, so the protocol above rarely applies — derive the value from the interview language instead, and only fall back to `en`.

Structural headings this skill writes carry their English anchor comment in both languages
(`## Heading <!-- SECTION: English Name -->`). The full do-not-localize registry — codes, status
enum values, table column headers, filenames, marker names, `EXPLORER_HEADER` field keys — is
`LANGUAGE_POLICY.md` §4.

---

## When to Use This Skill

Invoke this skill when:
- No existing PO Spec is found in the project and the user needs to capture business requirements
- User says they don't know where to start with business requirements
- User asks for requirements discovery, elicitation, or a requirements interview
- User asks to create a Product Owner Specification
- User asks about documenting business requirements for architecture
- User mentions "business context", "product requirements", or "requirements gathering" in relation to architecture
- User wants to prepare business documentation before technical architecture design
- User asks to evaluate or score a Product Owner Specification
- User wants to know if their PO Spec is ready for the architecture team
- User has business context in a file (ticket export, email, requirements doc) and wants to extract a PO Spec
- User says "async intake", "ticket context", "email context", or "intake from file"
- User provides a file path containing business requirements from an external async source

## Files in This Skill

- **REQUIREMENTS_ELICITATION_GUIDE.md**: Structured discovery interview methodology — 4 phases, probing techniques, Discovery Summary, and transition to PO Spec drafting
- **PRODUCT_OWNER_SPEC_GUIDE.md**: Comprehensive guide with 8-section template, examples, and best practices
- **templates/PO_SPEC_TEMPLATE.md**: Quick-start template for creating a new PO Specification
- **templates/PROJECT_INSTRUCTIONS_TEMPLATE.md**: the instructions of a Claude Project that runs chat mode — placeholders, where the files live, start and end of every chat (`CHAT_MODE.md` § A Claude Project)
- **PO_SPEC_SCORING_GUIDE.md**: Weighted scoring methodology to evaluate PO Spec readiness (0-10 scale)
- **ASYNC_INTAKE_GUIDE.md**: File-based async intake methodology — extraction rules, keyword indicators, gap report template, and follow-up question generation
- **CHAT_MODE.md**: what runs in a Claude chat (the package without `scripts/`) — elicitation, drafting, the Discovery Summary as a file, the pre-check; load only in chat mode
- **PO_SPEC_SYNC_WORKFLOW.md**: Workflow 6 — PO Spec Sync (architecture → PO Spec): the delta by code, the section mapping, proposals the Product Owner approves, the sync marker, the sync log. Load only for a sync
- **scripts/po-spec-checkability.js**: `bun scripts/po-spec-checkability.js <PRODUCT_OWNER_SPEC.md> [--judge …] [--answers] [--json] | --verify <fixtures.json>` — the checkability rule over every requirement (workflow 4, step 3): statements and use-case parts by code, one judge question per candidate, per-section multipliers and the 7.4 Ready cap by code; exit 0 PASS · 1 FAIL · 10 a worksheet waits
- **scripts/po-spec-coherence.js**: `bun scripts/po-spec-coherence.js <PRODUCT_OWNER_SPEC.md> [--judge …] [--answers] [--json]` — the coherence gate (workflow 4, step 3b): label vs substance (`references/solution-labels.json`), the objectives ↔ use cases ↔ metrics triangle, closure (every state a use case names has a setter, every trigger a producer), contradictions (use case × use case, × constraint, × out-of-scope item), sizing (an objective's figures against its KPI and against the acceptance limits of the use cases that serve it — warnings only), and one acceptance test per use case (`sa-requirements:generators:acceptance-test-writer`; a missing fact blocks once the judge confirms no use case gives it and that it is a business fact, not a detail a test takes as given, a clause the use case does not state warns); exit 0 PASS · 1 FAIL · 10 waiting
- **scripts/coherence-eval.js**: `bun scripts/coherence-eval.js <out_dir> [--judge …]` — the gate measured on seeded defects (`tests/fixtures/coherence/`): detection and false alarms
- **scripts/readiness-stamp.js**: `bun scripts/readiness-stamp.js <PRODUCT_OWNER_SPEC.md> [--check] [--json]` — the evaluation's stamp (workflow 4, step 7): both checks re-run on the answers already given, `<!-- READINESS_CHECK: verified <date> sha256:… -->` written when they pass; any later edit voids it, and architecture-docs' PO Spec gate blocks a `draft` or stale stamp; exit 0 · 1 · 10
- **scripts/po-spec-precheck.js**: chat mode's pre-check (`CHAT_MODE.md`), shipped in the chat package bundled as `precheck/po-spec-precheck.cjs` — the missing use-case parts and the candidates `po-spec-checkability.js` would ask the judge, with the tests' criteria, for the chat to read; no judge, no score, no stamp
- **scripts/po-spec-delta.js**: `bun scripts/po-spec-delta.js <project> [--po-spec <file>] [--out] [--json] | --stamp` — the delta (`.cache/sa-skills/po-spec-delta.md`) and the stamp (marker, Version, Date)

## How to Use This Skill

### 1. Async Intake (Non-Interactive)

⛔ **This flow NEVER transitions to elicitation.** It analyzes a file, produces a gap report with email-ready questions, and STOPS. The output is meant to be sent back to the requester asynchronously (email, ticket, Slack).

When business context arrives via ticket, email, or document (not a live conversation):

1. **Locate the context file**: Ask the user for the file path, or detect common patterns (`business-context.*`, `ticket-*.*`, `requirements-*.*`, `email-*.*`)
2. **Read and parse the file**: Load the full content
3. **Load scoring guide**: Read `PO_SPEC_SCORING_GUIDE.md` for the 8-section weighted rubric
4. **Load async intake guide**: Read `ASYNC_INTAKE_GUIDE.md` for extraction methodology and keyword indicators
5. **Map content to 8 PO Spec sections**: Extract what's present, mark what's missing per section. Hold every extracted requirement to the checkability rule (`PO_SPEC_SCORING_GUIDE.md` § The checkability rule): one that names no system, leaves a list open, says "later" without a date, states no observable result or uses a quality word without a number is an **aspiration**, listed apart — never counted as a requirement
6. **Score against the rubric**: Calculate per-section completeness % and weighted total score, with the rule's penalties (a failing use-case part makes that use case incomplete; any other failing requirement costs its section 25%; any failure in Use Cases, Objectives, Constraints or Metrics caps the total at 7.4)
7. **Generate gap report** (`PO_SPEC_GAP_REPORT.md`): Structured markdown containing:
   - **Source file**: filename and processing date
   - **Extraction summary**: what was found mapped to each of the 8 sections with completeness %
   - **Score**: weighted total and per-section breakdown
   - **Gap report**: for each section below 75% completeness:
     - What's missing (specific sub-criteria from the scoring guide)
     - 2-3 ready-to-send questions for the requester
     - Priority level (HIGH / MEDIUM / LOW based on section weight)
   - **Not yet checkable**: each failing requirement quoted, the test it fails and its ladder question (`REQUIREMENTS_ELICITATION_GUIDE.md` § The checkability ladder) — these lead the questions
   - **Ready-to-Send Message**: A complete, copyable email/ticket message block with subject line, prioritized gap questions, **the aspirational statements to complete** (every not-yet-checkable statement quoted with what is missing, numbered `A1`…), and sign-off — ready to paste into email, ticket, or Slack, in the source's language (see ASYNC_INTAKE_GUIDE.md § Step 8 for template). Every message derived from the gap report — a ticket comment, an email, a Slack post — carries that section
   - **Next steps**: "Send the Ready-to-Send Message to the requester → receive answers → re-run async intake with the updated file"
8. **Save gap report**: Write to `PO_SPEC_GAP_REPORT.md` in the project root
9. **If score ≥ 7.5**: Also draft `PRODUCT_OWNER_SPEC.md` from the extracted data using `templates/PO_SPEC_TEMPLATE.md` (aspirations under Appendix → Aspirations); flag any inferred values with `[Default — confirm before architecture handoff]`; run `po-spec-checkability.js` on the draft (workflow 4, step 3) and fix what it reports; then run workflow 5 (Distribution PDF)
10. **If score < 7.5**: Save gap report only — do NOT draft a PO Spec, do NOT start elicitation. The gap report with its Ready-to-Send Message is the final output.

### 2. Requirements Elicitation (Interactive)

When this skill is activated and no existing PO Spec is found (or the user requests discovery/elicitation):

1. **Detect existing PO Spec**: Search for `PRODUCT_OWNER_SPEC.md`, `PO_SPEC.md`, `**/po-spec*`, `**/product-owner*`
   - If found: offer Evaluation or Creation workflows instead (a spec carrying `READINESS_CHECK: draft` came from chat mode: offer Evaluation)
   - If not found: proceed with elicitation — from `DISCOVERY_SUMMARY.md` when a chat-mode interview left one: confirm it with the PO and continue at its open and low-confidence sections
2. **Load the guide**: Read `REQUIREMENTS_ELICITATION_GUIDE.md` fully before starting
3. **Detect language**: Infer from user's first message; ask if ambiguous
4. **Conduct the 4-phase interview**:
   - Phase 1 — Foundation (Business Context, Stakeholders)
   - Phase 2 — Value & Boundaries (Objectives, Constraints) ← highest weight, invest depth here
   - Phase 3 — Behavior (Use Cases, User Stories) ← deepest phase, use case count reflects architecture complexity
   - Phase 4 — Experience & Measurement (UX Requirements, Success Metrics)
5. **Produce Discovery Summary**: Structured by all 8 sections with confidence levels and open questions; present for PO confirmation before drafting
6. **Draft PO Spec**: Load `templates/PO_SPEC_TEMPLATE.md`, fill from elicited data, run `po-spec-checkability.js` (workflow 4, step 3), self-score against `PO_SPEC_SCORING_GUIDE.md` with its multipliers and cap
7. **Gap loop if needed**: If score < 7.5 or a critical section has a failing statement, take the failing statements first with the checkability ladder (`REQUIREMENTS_ELICITATION_GUIDE.md` § 6), then the weakest sections; re-check, re-score; save final as `PRODUCT_OWNER_SPEC.md`
8. **Distribution PDF**: Run workflow 5 to write `exports/PO-SPEC-<slug>.pdf` alongside the Markdown

### 3. PO Spec Creation (Template-Guided)

When this skill is activated for document creation:

1. **Read the guide**: Load PRODUCT_OWNER_SPEC_GUIDE.md to understand the 8-section structure
2. **Understand user context**: Ask clarifying questions about their product/feature
3. **Provide appropriate template**:
   - For guidance and understanding: Reference PRODUCT_OWNER_SPEC_GUIDE.md
   - For quick start: Provide templates/PO_SPEC_TEMPLATE.md
4. **Guide document creation**: Help user fill out each section with business context
5. **Reference mapping**: Explain how PO Spec maps to ARCHITECTURE.md (see guide Section "Mapping to ARCHITECTURE.md")

### 4. PO Spec Evaluation (Score Existing)

When this skill is activated to evaluate a PO Spec:

1. **Read the scoring guide**: Load PO_SPEC_SCORING_GUIDE.md to understand the weighted scoring methodology
2. **Read the PO Spec**: Load the user's Product Owner Specification document
3. **Check every requirement first** — the checkability rule, by code (`PO_SPEC_SCORING_GUIDE.md` § The checkability rule):
   ```bash
   bun [plugin_dir]/skills/architecture-readiness/scripts/po-spec-checkability.js <PRODUCT_OWNER_SPEC.md>
   ```
   Exit 10: a judge worksheet waits — dispatch the `sa-skills:reviewers:worksheet-judge` subagent with the path the output names, then run the same command again. Exit 1: failing statements, each with its test and ladder question. Exit 0: every requirement is checkable. Show the `CHECKABILITY` block as printed; the per-section multipliers and the Ready cap it returns are applied in step 4, never estimated.
3b. **Then the coherence gate** — can the spec be built as it stands (`PO_SPEC_SCORING_GUIDE.md` § The coherence gate):
   ```bash
   bun [plugin_dir]/skills/architecture-readiness/scripts/po-spec-coherence.js <PRODUCT_OWNER_SPEC.md>
   ```
   Exit 10 lists what waits: a judge worksheet → dispatch `sa-skills:reviewers:worksheet-judge` with its path; the acceptance-test request → dispatch `sa-requirements:generators:acceptance-test-writer` with its path; several in one message; then run the same command again. Exit 1: blocking findings (a label no use case exercises, an objective no use case delivers or no metric measures, a use case that cannot be tested as written, a state no use case sets, a trigger no use case produces, two statements that cannot both hold), each with its fix. Show the `COHERENCE` block as printed; warnings (scope creep, open questions) go to the Product Owner but do not block.
4. **Evaluate each section, then calculate the weighted score**: Assess completeness of all 8 sections using the evaluation criteria, multiply each requirement section by its checkability multiplier, apply the section weights (0-10 scale), then the Ready cap (7.4) when the check names one
5. **Provide detailed feedback**:
   - Overall score and readiness interpretation
   - Section-by-section breakdown showing completeness %
   - Identify gaps in critical sections (Use Cases, Business Constraints, Business Objectives)
   - List every requirement that fails the checkability rule with its ladder question, and offer to move the ones the PO cannot make concrete to Appendix → Aspirations
   - Provide actionable recommendations for improvement
6. **Determine readiness**: Score ≥7.5/10, no checkability cap and no blocking coherence finding indicates ready for architecture team handoff
7. **Stamp it**: on every evaluation, whatever the score —
   ```bash
   bun [plugin_dir]/skills/architecture-readiness/scripts/readiness-stamp.js <PRODUCT_OWNER_SPEC.md>
   ```
   It re-runs both checks on the answers steps 3 and 3b already gave (exit 10: one waits — go back to that step) and, when
   no Ready cap and no blocking coherence finding stands, writes `<!-- READINESS_CHECK: verified <date> sha256:… -->` as the
   spec's last line, replacing a `draft`. Exit 1: the stamp stays as it was, and the reasons it prints go to the PO with the
   feedback of step 5. The score is not stamped; the architecture's PO Spec gate (`gates-check.js` 0.2) blocks a `draft`
   or stale stamp and warns on none

### 5. Distribution PDF (automatic post-write)

**Run this every time `PRODUCT_OWNER_SPEC.md` is written**, from any workflow. The PO Spec is a
stakeholder-facing document — it is circulated for review and carries an approval footer — so a
paginated PDF is produced alongside the Markdown rather than on request.

Callers: workflow 1 step 9, workflow 2 step 7, `REQUIREMENTS_ELICITATION_GUIDE.md` § 10 step 9,
and `architecture-docs` Workflow 1 Step 0.2d.

**Step 5.1 — Resolve sa-skills' directory** — the PDF is rendered by sa-skills' `tools/docgen` (this skill ships in the
sa-requirements plugin, which sa-skills depends on):

- `sa_skills_dir=$(bun ~/.claude/plugins/marketplaces/shadowx4fox-solution-architect-marketplace/scripts/plugin-root.ts)`
  — the install registry's answer (project scope, else user scope, else the marketplace clone), never a Glob over
  `~/.claude/plugins/cache/`; show its stderr warning when a newer version is on the machine. With sa-requirements
  installed alone the clone answers and docgen may lack its dependencies: Step 5.5 applies, the spec is still written

**Step 5.2 — Ensure the output directory**:

```bash
bun [sa_skills_dir]/scripts/ensure-dir.ts exports   # optional: sa-skills
```

Use this helper, not `mkdir` — it is OS-agnostic and `mkdir` is not an authorized command.

**Step 5.3 — Derive the filename**. Kebab-case the PO Spec's H1 (dropping the trailing
`- Product Owner Specification`) into `solution_name_slug`, giving
`exports/PO-SPEC-<solution_name_slug>.pdf`. Fall back to `exports/PO-SPEC.pdf` when no usable H1
exists. **The filename stays English in every language** — filenames are on the do-not-localize
registry (`LANGUAGE_POLICY.md` § 4).

**Step 5.4 — Render**:

```bash
bun run [sa_skills_dir]/tools/docgen/generate-doc.js \
  --type    po-spec \
  --format  pdf \
  --lang    [doc_language] \
  --input   PRODUCT_OWNER_SPEC.md \
  --output  exports/PO-SPEC-[solution_name_slug].pdf \
  --author  "[Product Owner from the spec header]" \
  --version "[Version from the spec header]" \
  --status  "[Document Status from the spec footer]" \
  --score   "[X.X/10.0]"
```

`--author`, `--version` and `--status` come from the spec's own metadata header and approval
footer; pass `--score` only when a score was computed in this run. Runtime is **Bun only** —
never fall back to `node`.

**Step 5.5 — Degrade gracefully.** A non-zero exit must **never** block: the Markdown spec is the
deliverable, the PDF is a convenience. On failure, print the warning below and continue with the
workflow's normal closing message.

```
⚠️  PO Spec saved, but the distribution PDF could not be generated: [one-line error]
   Install docgen dependencies:  cd [sa_skills_dir]/tools/docgen && bun install
```

**Step 5.6 — Report.** On success, append this line to the workflow's closing message:

```
📄 Distribution PDF: exports/PO-SPEC-<solution_name_slug>.pdf
```

**Why docgen is called directly** rather than through the `docs-export-generator` agent: this is a
single deterministic render with no composition step, that agent's job types are `.docx`-only, and
`Bash(bun *)` already permits the call. Spawning an agent would add cost without adding anything.

**Required permissions** — both are already in `.claude/settings.json.example`, so no new grant is
needed: `Bash(bun *)` and `Write(exports/*)`.

### 6. PO Spec Sync (architecture → PO Spec)

**Trigger**: "update the PO spec", "sync PO spec", "actualiza el PO spec con lo último", "align the
PO spec with the architecture", or any request to reflect the architecture's changes in the spec.
**Requires** an existing `PRODUCT_OWNER_SPEC.md` and an architecture with `docs/CHANGELOG.md`.

**Load `PO_SPEC_SYNC_WORKFLOW.md`** and follow it. In short: the delta is **collected by code**
(`scripts/po-spec-delta.js` — sync state from the `<!-- ARCHITECTURE_SYNC: <version> (<date>) -->`
marker, the changelog entries since with their bodies, the ADRs and TDRs they name, the containers
updated, the `UC-nn` ids the spec defines vs the ids the architecture's flows serve, the retired
integrations — never by reading the changelog in the session or dispatching an agent to summarize
it); every change with a business effect becomes a **proposal** in business language placed by the
fixed section mapping (use cases → § 4 / § 5; targets → § 6 / § 8; external systems, vendors,
regulation → § 7; scope → § 1 / § 3; owners → § 2; accepted debt → § 7 / Appendix); the **Product
Owner approves item by item**; the approved rows are applied in the section's own format; the
script **stamps** the marker, bumps the spec's minor version and dates it; the Appendix gains a
sync-log row; the spec is re-scored (Workflow 4) and the PDF rendered (Workflow 5). The spec is
the Product Owner's document: nothing is rewritten silently, and no container, technology or
protocol enters it unless the constraint *is* the technology or the spec already named it — and no
architecture reference ever does: no `ADR-nnn`, `TDR-nnn` or `I-nn` id, no link into `adr/`, `tdr/` or
`docs/`. The id stays in the proposal's Source column; `po-spec-delta.js --check` refuses the spec
before the stamp.

## Key Principles

- **Business-focused**: No technical details or architecture decisions in PO Spec
- **User-centric**: Emphasize user needs, personas, and pain points
- **Measurable**: All goals and success criteria must be quantifiable
- **Means are the architecture's**: a product, technology or design the PO proposes is kept verbatim under Appendix → Implementation Suggestions — not a requirement, not scored; the need behind it is the requirement. `po-spec-checkability.js` reports a requirement that prescribes one; `lifecycle.js status` lists the open ones; the PO Spec sync (workflow 6) writes the architecture's answer
- **Checkable**: every requirement — use cases above all — must be checkable by someone who was not in the room: named, closed, dated, observable, measured. A wish that is not yet checkable goes to Appendix → Aspirations; `scripts/po-spec-checkability.js` holds the rule and the penalty
- **Constraint-aware**: Document all business constraints (budget, timeline, compliance)

## Integration with Other Skills

**Relationship to architecture-docs skill:**
- architecture-readiness (this skill) → Creates **business** requirements (PO Spec)
- architecture-docs skill → Creates **technical** architecture (ARCHITECTURE.md)

**Workflow:**
1. Product Owner uses architecture-readiness skill → Creates PO Spec
2. PO Spec handed off to architecture team
3. Architecture team uses architecture-docs skill → Creates ARCHITECTURE.md
4. The architecture evolves (Workflow 2 edits, releases (`architecture-lifecycle`), ADRs) → **Workflow 6 of this skill** brings the PO Spec back in line, with the Product Owner's approval, and stamps the architecture version it reflects

## Example Invocations

### Illustrative example: creating a PO Spec

```
User: "I want to create a Product Owner Specification for a new mobile payment feature"

Claude (with architecture-readiness skill activated):
1. Load PRODUCT_OWNER_SPEC_GUIDE.md to understand structure
2. Ask clarifying questions:
   - What business problem does this solve?
   - Who are the target users?
   - What are the business objectives and success metrics?
   - Are there regulatory/compliance requirements?
3. Guide user through 8 sections:
   - Business Context
   - Stakeholders & Users
   - Business Objectives
   - Use Cases
   - User Stories
   - User Experience Requirements
   - Business Constraints
   - Success Metrics & KPIs
4. Provide template sections as needed
5. Explain how completed PO Spec feeds into ARCHITECTURE.md
```

## Common User Requests

**Requirements Elicitation:**
- "I don't know where to start with requirements" → Use REQUIREMENTS_ELICITATION_GUIDE.md, begin Phase 1
- "Can you interview me about my project requirements?" → Use REQUIREMENTS_ELICITATION_GUIDE.md, begin interview
- "Help me discover requirements for [project]" → Use REQUIREMENTS_ELICITATION_GUIDE.md
- "I have a business idea, what do I need to document?" → Detect PO Spec, if none → elicitation flow
- "Requirements discovery / elicitation / interview" → Use REQUIREMENTS_ELICITATION_GUIDE.md

**PO Spec Creation:**
- "Help me document business requirements" → Use PRODUCT_OWNER_SPEC_GUIDE.md
- "I need a template for product specifications" → Provide templates/PO_SPEC_TEMPLATE.md
- "How does this relate to the architecture document?" → Reference "Mapping to ARCHITECTURE.md" section in guide
- "What should I include in use cases vs user stories?" → Reference Sections 4 and 5 of guide

**PO Spec Evaluation:**
- "Evaluate my PO Spec" → Use PO_SPEC_SCORING_GUIDE.md to score the document
- "Is my PO Spec ready for the architecture team?" → Score and assess readiness (≥7.5/10)
- "What's missing from my business requirements?" → Identify gaps using evaluation criteria
- "How can I improve my PO Spec score?" → Provide actionable recommendations based on section weights

**PO Spec Sync:**
- "Update the PO spec with the latest changes" / "actualiza el PO spec" / "sync the PO spec" → Workflow 6, `PO_SPEC_SYNC_WORKFLOW.md`: run `scripts/po-spec-delta.js`, propose, let the PO decide, apply, stamp
- "Is the PO spec current?" / "how far behind is the spec?" → `scripts/po-spec-delta.js` and report the sync state only

**Async Intake:**
- "I received a ticket/email with business context" → Read the file, run Async Intake mode
- "Extract requirements from this file" → Async Intake mode
- "Generate a gap report from this document" → Async Intake mode
- "Async intake" / "ticket context" / "email context" / "intake from file" → Async Intake mode
- "What questions should I ask to fill in the gaps?" → Async Intake mode, generate ready-to-send questions

## Success Criteria

### For Requirements Elicitation

A quality elicitation should:
- ✅ Detect the absence of an existing PO Spec before starting the interview
- ✅ Conduct all 4 interview phases with appropriate depth (Use Cases and Constraints receive most time)
- ✅ Apply probing techniques (scenario walking, quantification, negative probing) to increase answer depth
- ✅ Offer industry defaults when PO is unsure, and record unknowns as Open Questions
- ✅ Produce a Discovery Summary organized by all 8 sections with confidence levels
- ✅ Confirm Discovery Summary with PO before drafting
- ✅ Draft a PO Spec from the template, self-score it, and iterate until score ≥ 7.5/10
- ✅ Save final PO Spec as `PRODUCT_OWNER_SPEC.md` with score and next-step guidance
- ✅ Produce the distribution PDF at `exports/PO-SPEC-<slug>.pdf`, or warn without blocking if docgen is unavailable

### For PO Spec Creation

A well-formed Product Owner Specification should:
- ✅ Have all 8 sections completed
- ✅ Include specific, measurable success criteria
- ✅ Define user personas with real pain points
- ✅ Document all business constraints (budget, timeline, compliance)
- ✅ Use business language (avoid technical jargon)
- ✅ Carry no architecture references — no ADR / TDR / integration id, no link into `adr/`, `tdr/` or `docs/` (`scripts/po-spec-delta.js <root> --check`)
- ✅ Map clearly to ARCHITECTURE.md inputs
- ✅ Score ≥7.5/10 on the weighted scoring methodology

### For PO Spec Evaluation

A quality evaluation should:
- ✅ Assess all 8 sections using the evaluation criteria from PO_SPEC_SCORING_GUIDE.md
- ✅ Calculate weighted score correctly (applying section weights)
- ✅ Provide clear readiness determination (Ready ≥7.5/10, Not Ready <7.5/10)
- ✅ Give specific, actionable feedback for each gap identified
- ✅ Prioritize feedback on high-weight sections (Use Cases, Business Constraints, Business Objectives)
- ✅ Explain what needs to be added/improved to reach readiness threshold

### For Async Intake

A quality async intake should:
- ✅ Read the provided context file completely before any analysis
- ✅ Map content to all 8 PO Spec sections using keyword indicators from ASYNC_INTAKE_GUIDE.md
- ✅ Calculate accurate weighted score per PO_SPEC_SCORING_GUIDE.md
- ✅ Generate a gap report with 2-3 ready-to-send questions per gap section
- ✅ Prioritize gaps by section weight (HIGH: Use Cases, Constraints, Objectives)
- ✅ Save gap report as `PO_SPEC_GAP_REPORT.md` in the project root
- ✅ If score ≥ 7.5, also produce a draft `PRODUCT_OWNER_SPEC.md` with inferred values flagged as `[Default]`, plus its distribution PDF at `exports/PO-SPEC-<slug>.pdf`
- ✅ NOT start an interactive interview — this mode is fully async
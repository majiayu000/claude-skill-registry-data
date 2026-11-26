---
name: prd-author
description: Draft a new PRD for a QTI interaction, architecture subsystem, or cross-cutting system concern. Use when the user asks to "write a PRD", "document how X works", "add a PRD for X", or wants to capture requirements and rationale for a feature or subsystem. The skill interviews for missing context, reads the relevant source code and existing docs, then produces a complete draft aligned to docs/prds/TEMPLATE.md.
---

# PRD Author

You are drafting a Product Requirements Document (PRD) for the PIE-QTI framework. PRDs are the canonical source of *why* — rationale, constraints, design decisions, acceptance criteria — complementing what the code says and what the QTI spec requires.

## Step 1 — Identify what to document

Determine the PRD subject from the conversation. Map it to one of three types:

- **interaction** — a QTI interaction type implemented in `@pie-qti/default-components` (e.g. `choiceInteraction`, `hotspotInteraction`)
- **architecture** — a major subsystem (e.g. Item Player, Transform Engine, Assessment Player, Vendor Extensions)
- **system** — a cross-cutting concern (e.g. i18n, theming, accessibility baseline, navigation modes)

Check `docs/prds/INVENTORY.md` to confirm the PRD is listed and its current status.

## Step 2 — Read the source

Before drafting, read the relevant source to ground the PRD in what actually exists. Depending on type:

**For interaction PRDs:**
- The Svelte component: `packages/default-components/src/plugins/<name>/<Name>Interaction.svelte`
- The extractor: `packages/item-player/src/extraction/extractors/<name>Extractor.ts` (note: extractors live in item-player, not default-components)
- The existing eval YAML (if any): `docs/evals/default-components/<name>/evals.yaml` — use as seed for acceptance criteria
- The QTI spec section for this interaction in `docs/QTI_techguide.md` (1539-line comprehensive guide, §3.x covers all interaction types)
- `docs/QTI-RESPONSE-TRACKING-AND-SCORING.md` — for response variable semantics, scoring templates, and operator behavior
- `docs/SPEC-GAPS-PLAN.md` — check for any gap items (G-01 through G-15) that affect this interaction; document them explicitly in the PRD's QTI alignment section under "Known gaps"
- Any existing docs in `packages/default-components/` (e.g. position-object has a README with important spec limitation notes)
- If local docs are insufficient for a spec question, use WebSearch/WebFetch to consult the IMS QTI 2.2 spec or QTI 3.0 spec directly. Search for "IMS QTI 2.2 Assessment Item Information Model" to find the canonical URL. Cross-reference with `../qti3-item-player`, `../qti-components` reference implementations when helpful.

**For architecture PRDs:**
- The package `README.md` and any docs in `packages/<name>/docs/`
- Key source files (registries, interfaces, entry points) — read to understand actual extension contracts
- Adjacent packages that depend on or are depended on by this one
- Existing docs in `docs/` that overlap (e.g. `docs/ARCHITECTURE.md`, `docs/TRANSFORMATION-ENGINE.md`)

**For system PRDs:**
- The relevant package(s) and their READMEs
- Cross-package usage — search for call sites to understand how the system is actually used

## Step 3 — Identify gaps

After reading, list what you don't know that would affect the PRD quality. Ask the user targeted questions — maximum five, prioritized by importance. Common gaps:

- Rationale for specific design decisions (why was X chosen over Y?)
- Intentional omissions (is attribute X deliberately unsupported, or just not yet implemented?)
- Acceptance criteria that aren't obvious from the code (what does "correct" look like for edge cases?)
- K-12 pedagogical constraints (are there age-appropriateness requirements specific to this interaction?)
- Known bugs or divergences from spec that should be documented

Don't ask about things you can read from the code. Don't ask for information you already have from context.

## Step 4 — Draft the PRD

Use `docs/prds/TEMPLATE.md` as the structure. Write each section with the following priorities:

**Background and rationale** — this is the most important section. It's the context future maintainers can't derive from reading the code. Be specific about constraints and tradeoffs.

**QTI specification alignment** — be precise. List supported attributes with their expected behavior. List deliberately omitted attributes with the reason (not implemented vs. intentionally out of scope). Note any divergences from spec and why they exist.

**Acceptance criteria** — write in the Given/When/Then format from the template. These must be self-contained and testable without running code — a human QA engineer or an AI with Playwright access should be able to execute them. Pull scenarios from the existing evals YAML if one exists; expand beyond it.

**Design decisions** — only document decisions that a future engineer might be tempted to change. Trivial choices don't need justification. Non-obvious constraints (accessibility, performance, spec compliance) do.

## Step 5 — Place the file

Save the PRD to the correct subdirectory:
- `docs/prds/interactions/<slug>.md`
- `docs/prds/architecture/<slug>.md`
- `docs/prds/systems/<slug>.md`

Update the status in `docs/prds/INVENTORY.md` from `planned` to `draft`.

## Writing standards

- Write for a senior engineer who is new to this codebase. Assume deep general engineering knowledge; don't assume familiarity with QTI or PIE.
- No filler. Every sentence should carry information a future maintainer would actually use.
- Rationale sections should explain the real constraints — QTI spec requirements, accessibility law, K-12 UX research, performance budgets — not restate what the code does.
- Acceptance criteria should be complete enough that someone who has never used the app can verify them.
- Cross-reference related PRDs and existing docs rather than duplicating content.

## Skills to use proactively

- **qti-domain-expert** — to verify spec semantics before writing the QTI alignment section
- **pie-domain-expert** — when the PRD covers a transform or PIE↔QTI boundary
- **accessibility-reviewer-assessments** — to populate the accessibility AC section for interaction PRDs
- **api-design-reviewer** — for architecture PRDs covering public extension APIs

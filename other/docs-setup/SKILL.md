---
name: docs-setup
description: "Bootstrap the canonical two-part _docs directory for any context-coded project in the Claude/AntiGravity environment. Creates _build/ (finite agent-only technical docs) and _public/ (facts/, insights/, proposals/) plus a CONSTITUTION.md that governs the split. Writes every README, seeding voice and audience expectations for _public. Run once at project start, or run on an existing project to audit and migrate into the correct structure."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Bootstrap the _docs directory for: $ARGUMENTS

$ARGUMENTS can include:
- Project name / author name (e.g. "Alan Hirsch", "non-profit-dashboard")
- Audience description — who the _public docs ultimately serve (e.g. "board of directors", "ministry leaders", "course participants")
- Voice reference — the author skill to use for _public content (e.g. "alan-voice", "custom") — defaults to checking for a local alan-voice skill
- "audit" — scan an existing _docs directory and report which files should move where, without writing anything
- "migrate" — run the audit, then move files into the correct structure
- Empty — ask the user for project name and audience before proceeding

---

## Purpose

Every project in this environment produces two fundamentally different kinds of documentation. This skill makes that distinction structural and permanent from day one.

**`_docs/_build/`** is the agent's workbench. It contains everything a Claude agent or developer needs to build and maintain the project: the type safety chain, design system docs, engineering runbooks, agent architecture, and generated prompts. This directory is **finite** — it grows only when the architecture grows, not when research accumulates. Files here are precise and technical. They are not written for an outside audience.

**`_docs/_public/`** is the project's intellectual capital. It captures everything discovered, synthesized, or proposed during the build: research facts, analytical insights, and concrete proposals. This directory **grows throughout the project's life**. Files here are written for three simultaneous audiences: the Claude agent (precise and queryable), the human developer (actionable and contextual), and the core project audience (narrative and in the author's voice). The goal is that any document in `_public/` could — with minimal formatting — become a published article, board briefing, or resource page.

**`_docs/CONSTITUTION.md`** is the single document that governs the split. It defines what belongs where, explains the three-audience standard, and links to the voice skill. Every collaborator (human or AI) reads this first.

The `_build/_prompts/` directory is special: prompts are **generated from** the `_public/` chain (facts → insights → proposals → prompt). This means prompts are outputs of the research process, not standalone artifacts invented during build.

---

## Phase 0 — Gather Requirements

If `$ARGUMENTS` is empty or underspecified, ask:

1. **Project name / author** — What is the project called? Who is the thought leader or author at the center of it? (This determines voice and audience framing.)
2. **Core audience** — Who are the ultimate human readers of `_public/` docs? (Examples: "board of directors for a non-profit", "ministry leaders", "course participants", "general readers interested in missional theology") This shapes the tone and density of all `_public/` writing.
3. **Voice** — Is there a voice skill available? Check for `.claude/skills/alan-voice/` or equivalent. If not, ask the user to describe the author's voice in 2-3 sentences — this gets written into the CONSTITUTION.

If `$ARGUMENTS` contains "audit", skip to Phase 6.
If `$ARGUMENTS` contains "migrate", run Phase 6 then Phase 5.

---

## Phase 1 — Check What Exists

Before creating anything:

1. Check if `_docs/` exists. If it does, run `ls -la _docs/` and note the contents.
2. Check if `_docs/CONSTITUTION.md` exists — if so, read it. This skill has already run; ask the user whether to update the structure or exit.
3. Check for an existing voice skill at `.claude/skills/alan-voice/SKILL.md` or `.claude/skills/[name]-voice/SKILL.md`.
4. Note any files in `_docs/` that would need migrating if the user chooses "migrate" mode later.

Report findings before writing anything.

---

## Phase 2 — Create the Directory Structure

Create the following directory tree by writing a `.gitkeep` or README.md in each leaf. Never create a directory without at least one file in it.

```
_docs/
  CONSTITUTION.md            ← written in Phase 3
  _build/
    README.md                ← written in Phase 4a
    type/                    ← type safety chain docs (seeded empty)
    design/                  ← design system, AntiGravity layers
    engineering/             ← runbooks, validation guides, audit prompts
    agents/                  ← agent architecture, system prompts
    _prompts/                ← generated prompts (derived from _public chain)
    README-prompts.md        ← explains how prompts are derived
  _public/
    README.md                ← written in Phase 4b
    facts/
      README.md              ← explains what belongs here
    insights/
      README.md
    proposals/
      README.md
```

Do not create any other subdirectories. The `type/`, `design/`, `engineering/`, `agents/` directories inside `_build/` start empty (each gets a `.gitkeep` and a one-paragraph README if the content doesn't already exist).

If `_docs/type/` already exists with content (e.g., from the `docs-type-safety` skill), move it to `_docs/_build/type/` — or note the move for the user if in audit mode.

---

## Phase 3 — Write CONSTITUTION.md

Write `_docs/CONSTITUTION.md`. This is the most important file in the entire `_docs/` directory. It must be clear enough that a new AI agent dropped into this project — having read only this file — would know exactly where to write and read documentation.

```markdown
# Docs Constitution
**Project:** [project name]
**Author / Voice:** [author name]
**Core Audience:** [audience description]
**Last Updated:** [date]

---

## The Two-Part Structure

All documentation in this project lives in one of two places. This is not a filing convention — it is a structural guarantee that determines what gets built, what gets published, and who can read it.

### `_build/` — The Agent's Workbench

Everything required to build and maintain the technical infrastructure of this project lives here. This directory is **finite and bounded**: it grows only when the architecture changes.

| Directory | Contents |
|-----------|----------|
| `_build/type/` | Type safety chain docs — six-layer architecture, validation guides |
| `_build/design/` | Design system, AntiGravity layers, token docs |
| `_build/engineering/` | Runbooks, audit prompts, validation protocols |
| `_build/agents/` | Agent architecture, system prompts, handoff logic |
| `_build/_prompts/` | Generated prompts — **derived from `_public/` chain only** |

**Audience:** Claude agent and human developer only.
**Voice:** Precise, technical, imperative. No narrative framing.
**Growth pattern:** Only when architecture expands.

### `_public/` — The Project's Intellectual Capital

Everything discovered, synthesized, or proposed during the build lives here. This directory grows continuously throughout the project's life.

| Directory | Contents |
|-----------|----------|
| `_public/facts/` | Verified research findings, source data, affiliation records, statistics, direct quotes |
| `_public/insights/` | Analysis, patterns, interpretations, comparative observations |
| `_public/proposals/` | Concrete plans, design options, strategic recommendations, draft approaches |

**Audience:** Three simultaneous readers — the Claude agent, the human developer, and [audience description]. Every document must serve all three.
**Voice:** [author name]'s voice. See `.claude/skills/[voice-skill]/SKILL.md` for the full voice guide.
**Growth pattern:** Continuous — research and analysis accumulate here.

---

## The Three-Audience Standard

Every file written to `_public/` must be useful to three readers simultaneously:

1. **Claude agent** — The document must be precise, structured, and queryable. Use clear headings, factual language, and avoid ambiguity. The agent will cite this document in prompts and use it to inform decisions.

2. **Human developer** — The document must provide enough context that a developer who didn't attend the research sessions can understand the finding, why it matters, and what to do with it. Link to related docs. Include action implications.

3. **[Core audience]** — The document must be written in [author name]'s voice, at the appropriate level of depth and authority for [audience description]. The goal: any `_public/` document should be publishable — as an article, board briefing, or resource — with minimal reformatting.

This constraint forces intellectual clarity. If a document can't be written for all three audiences, it means the thinking isn't clear enough yet.

---

## The Prompt Derivation Chain

Prompts in `_build/_prompts/` are **outputs**, not inputs. They are generated from the `_public/` chain:

```
facts/ + insights/ → proposals/ → _build/_prompts/
```

A prompt should never be written from scratch. It should synthesize verified facts, analytical insights, and a concrete proposal into a directive. If you cannot trace a prompt back to at least one fact and one insight, the prompt is not ready.

---

## Governance Rules

1. **Never put research in `_build/`.** Findings, analysis, and proposals belong in `_public/`.
2. **Never put architecture docs in `_public/`.** Type safety, design system, and engineering docs belong in `_build/`.
3. **`_build/_prompts/` derives from `_public/`** — not the other way around.
4. **All `_public/` content uses the author's voice** — even technical findings are written with the author's authority and perspective.
5. **No orphan docs at `_docs/` root** — every file belongs in `_build/` or `_public/`.
6. **`_temp/` is allowed for work in progress**, but must be migrated before any PR merges.

---

## Voice Reference

[If alan-voice skill exists:]
The canonical voice guide for this project is at `.claude/skills/alan-voice/SKILL.md`. When writing any `_public/` document, invoke or follow that skill's five voice markers.

[If no voice skill:]
Voice description: [user-provided 2-3 sentence voice description]
Voice skill status: NOT YET CREATED. Run `/alan-voice` (or create an equivalent skill) to formalize the voice before authoring significant `_public/` content.

---

## File Naming Conventions

**`_build/` files:** SCREAMING_SNAKE_CASE for standalone docs. Kebab-case for layer directories.
- `TYPE_SAFETY.md`, `DESIGN_CHAIN.md`, `AUDIT_RUNBOOK.md`

**`_public/` files:** Descriptive kebab-case. Include date prefix for time-sensitive research.
- `facts/affiliation-data-[author].md`, `insights/audience-analysis-2026-03.md`, `proposals/home-page-redesign.md`

---

## Quick Reference: What Goes Where

| Document type | Goes in |
|---------------|---------|
| Type safety docs | `_build/type/` |
| Design system, tokens | `_build/design/` |
| Runbooks, audit prompts, engineering guides | `_build/engineering/` |
| Agent architecture, system prompts | `_build/agents/` |
| Generated prompts (from research chain) | `_build/_prompts/` |
| Research findings, source data | `_public/facts/` |
| Analysis, patterns, interpretations | `_public/insights/` |
| Plans, options, recommendations | `_public/proposals/` |
| Work in progress | `_docs/_temp/` (temporary only) |
```

---

## Phase 4a — Write `_build/README.md`

```markdown
# _build/

Agent workbench documentation for [project name]. Everything here is required to build, maintain, or repair the technical infrastructure of this project.

## Contents

| Directory | Purpose |
|-----------|---------|
| `type/` | Six-layer type safety chain — Drizzle schema through React hooks |
| `design/` | AntiGravity design system layers, token definitions, design charter |
| `engineering/` | Runbooks, audit prompts (run in order 01–06), validation protocols |
| `agents/` | Agent definitions, system prompts, handoff configuration |
| `_prompts/` | Generated prompts — see `README-prompts.md` |

## Rules

- This directory is **finite**. Add files only when the architecture changes.
- Do not add research, insights, or proposals here. Those belong in `_public/`.
- Do not write `_build/_prompts/` files from scratch. Derive them from `_public/facts/` + `_public/insights/` + `_public/proposals/`.

## Key Files

- `_docs/CONSTITUTION.md` — Governance rules for the entire _docs structure
- `type/TYPE_SAFETY.md` — Full type safety chain documentation (if generated by `docs-type-safety` skill)
- `design/DESIGN_CHAIN.md` — Design layer documentation (if generated by design skills)
- `engineering/AUDIT_RUNBOOK.md` — Engineering audit order (if generated by audit skills)
```

---

## Phase 4b — Write `_public/README.md`

```markdown
# _public/

The intellectual capital generated during the build of [project name]. Everything here reflects real research, real analysis, and real decisions — written for three audiences simultaneously.

## The Three Audiences

Every document in this directory serves:
1. **The Claude agent** — precise, queryable, structured
2. **The human developer** — contextual, actionable, linked
3. **[Core audience]** — in [author name]'s voice, publishable-quality

## Contents

| Directory | Purpose |
|-----------|---------|
| `facts/` | Verified research: affiliations, source data, statistics, direct quotes |
| `insights/` | Analysis and interpretation: patterns, comparisons, conclusions |
| `proposals/` | Concrete plans: design options, strategic recommendations, draft approaches |

## The Research Chain

Facts → Insights → Proposals → (feeds) `_build/_prompts/`

Start with facts. Don't write an insight until it has a supporting fact. Don't write a proposal until it emerges from at least one insight. Prompts are the last step, not the first.

## Voice

All documents use [author name]'s voice. See `.claude/skills/[voice-skill]/SKILL.md`.
```

---

## Phase 4c — Write `_public/facts/README.md`

```markdown
# facts/

Verified research findings for [project name]. A fact is a confirmed, sourceable claim — not an interpretation or recommendation.

## What belongs here

- Affiliation data (organizations, publishers, speaking bureaus)
- Direct quotes from the author's published work
- Statistics and research data with citations
- Platform/product audit findings (what is actually on the site, not what should be)
- Database content inventories

## What does NOT belong here

- Interpretations of data → `insights/`
- Recommendations based on data → `proposals/`
- Architecture or technical specs → `_build/`

## File naming

`[topic]-[author-or-source].md` or `[date]-[topic].md`

Examples:
- `affiliation-data-alan-hirsch.md`
- `2026-03-corpus-quote-index.md`
- `platform-content-inventory.md`
```

---

## Phase 4d — Write `_public/insights/README.md`

```markdown
# insights/

Analysis and interpretation generated during the build of [project name]. An insight is a pattern, conclusion, or observation derived from verified facts.

## What belongs here

- Audience analysis and persona insights
- Corpus theme analysis (patterns across the author's body of work)
- Competitive or comparative observations
- Platform UX or content gap analysis
- Research synthesis (what multiple facts, taken together, suggest)

## What does NOT belong here

- Raw facts without interpretation → `facts/`
- Actionable plans → `proposals/`
- Technical architecture → `_build/`

## File naming

`[topic]-analysis.md` or `[date]-[topic]-insights.md`

Examples:
- `audience-profile-ministry-leaders.md`
- `2026-03-corpus-theme-analysis.md`
- `home-page-conversion-gaps.md`
```

---

## Phase 4e — Write `_public/proposals/README.md`

```markdown
# proposals/

Concrete plans, design options, and strategic recommendations for [project name]. A proposal is an actionable recommendation grounded in facts and insights.

## What belongs here

- Page redesign proposals (with rationale)
- Strategic positioning recommendations
- Content architecture proposals
- Feature or section proposals
- Draft approaches being evaluated

## What does NOT belong here

- Raw research → `facts/`
- Analysis without a recommendation → `insights/`
- Final decisions already implemented → those live in `_build/` docs or CLAUDE.md
- Technical implementation specs → `_build/`

## File naming

`[feature-or-surface]-[approach].md` or `[date]-[topic]-proposal.md`

Examples:
- `home-page-hero-redesign.md`
- `pathways-section-architecture.md`
- `2026-03-ai-lab-context-proposal.md`

## Proposal Format

Each proposal should include:
1. **What** — what is being proposed
2. **Why** — the facts and insights that motivated this proposal
3. **How** — enough specifics that a developer could implement it
4. **Tradeoffs** — what's gained, what's sacrificed
5. **Status** — Draft / Under Review / Approved / Implemented / Rejected
```

---

## Phase 4f — Write `_build/README-prompts.md`

```markdown
# _prompts/

Generated prompts for [project name]. These are **outputs of the research chain**, not inputs.

## Derivation Rule

Every prompt in this directory must trace back to:
- At least one fact in `_public/facts/`
- At least one insight in `_public/insights/`
- A proposal in `_public/proposals/` (the prompt operationalizes the proposal)

Do not write prompts speculatively. If the research chain doesn't support a prompt yet, write the facts and insights first.

## Chain

```
_public/facts/     →  verified claims
_public/insights/  →  analytical interpretation
_public/proposals/ →  concrete recommendation
                   ↓
_build/_prompts/   →  operative prompt (agent-facing)
```

## Naming

`[surface]-[purpose].md` — e.g., `home-page-hero-rewrite.md`, `course-intro-voice-calibration.md`

## Format

Each prompt file should include:
- A header section naming the source facts, insights, and proposal
- The prompt itself (ready to paste into Claude or AI Studio)
- Optional: expected output format or success criteria
```

---

## Phase 5 — Migrate Existing Docs (if "migrate" mode)

If the user requested migration or the project has an existing `_docs/` with unorganized content:

1. Read the root of `_docs/` and list all files and directories.
2. For each file/directory, classify it:

   | Classification | Move to |
   |----------------|---------|
   | Type safety docs (`TYPE_SAFETY.md`, `layers/`, validation docs) | `_build/type/` |
   | Design system docs (`DESIGN_CHAIN.md`, `DESIGN_CHARTER.md`, AntiGravity layers) | `_build/design/` |
   | Engineering runbooks, audit prompts, status reports | `_build/engineering/` |
   | Agent architecture, system prompts, AI lab architecture | `_build/agents/` |
   | Prompts and generated prompt packages | `_build/_prompts/` |
   | Research findings, affiliations, corpus data, inventories | `_public/facts/` |
   | Analysis docs, comparisons, gap analyses, consultation reports | `_public/insights/` |
   | Proposals, redesign plans, spec docs with recommendations | `_public/proposals/` |
   | Work in progress, temp files | `_docs/_temp/` |

3. Report the proposed migration plan to the user. Show a table:

   ```
   | Current path | Proposed path | Classification |
   |-------------|---------------|----------------|
   | _docs/TYPE_SAFETY.md | _docs/_build/type/TYPE_SAFETY.md | Build > type |
   | _docs/COPY_STRATEGY_WORKSHEET.md | _docs/_public/proposals/copy-strategy.md | Public > proposals |
   | ...
   ```

4. Ask the user to confirm before executing any moves.
5. After confirmation, use Bash `mv` commands to execute the migration. Do not delete anything.

---

## Phase 6 — Audit Mode (no writes)

If the user passed "audit", report only:

1. What structure currently exists in `_docs/`
2. What is missing from the canonical structure (CONSTITUTION.md, `_build/`, `_public/`, subdirectory READMEs)
3. Which existing files appear to be in the wrong location
4. Estimated migration effort (number of files to move)

Do not write or move anything. Output a clean report the user can act on.

---

## Phase 7 — Final Report

After writing all files, output:

```markdown
## Docs Setup Complete: [Project Name]

### Structure Created
- `_docs/CONSTITUTION.md` — Governance document (read this first)
- `_docs/_build/` — Agent workbench (type, design, engineering, agents, _prompts)
- `_docs/_public/` — Intellectual capital (facts, insights, proposals)

### Voice Configuration
- Voice skill: [found at path / not yet created]
- Three-audience standard: active for all _public/ content

### Next Steps
1. Read `_docs/CONSTITUTION.md` — understand the split before writing any docs
2. Run `/docs-type-safety` to populate `_build/type/` with the type safety chain docs
3. Run `/app-architect` to populate `_build/agents/` or `_build/design/` as needed
4. As research accumulates, write findings to `_public/facts/` first, then insights, then proposals
5. Generate prompts last — from the `_public/` chain into `_build/_prompts/`

### Migration Status
[If migrate mode: list files moved]
[If existing docs found: note files that still need classifying]
```

---

## Critical Rules

1. **CONSTITUTION.md is written before anything else.** It is the contract. Every other file is written against it.
2. **`_build/` is finite.** It grows only when architecture grows. Never add research or insights here.
3. **`_public/` is continuous.** It grows whenever new knowledge is generated.
4. **Prompts are last in the chain.** Never write a prompt that can't trace to a fact, an insight, and a proposal.
5. **All `_public/` content is in the author's voice.** Technical clarity and narrative authority are not opposites.
6. **No orphan files at `_docs/` root.** If a file doesn't clearly belong in `_build/` or `_public/`, it goes to `_temp/` until classified.
7. **The three-audience standard is non-negotiable.** A `_public/` doc that only one audience can use is not finished.

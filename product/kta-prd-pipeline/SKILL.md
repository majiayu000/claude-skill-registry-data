---
name: kta-prd-pipeline
description: Decompose validated idea-brief.md into 4–8 per-feature PRDs with screens nested. Use after kta-idea-pipeline. Triggers — write PRD, decompose features, feature breakdown, screen list, MVP scope to PRD, post-idea-validation, per-feature PRD, product requirements document, generate PRDs.
---

## Platform Tooling

- Use AskUserQuestion for blocking user choices or confirmations.
- Use WebFetch/WebSearch for current external docs or public web research.
- Use Task tool with subagent_type for delegation.
- Use Skill tool when chaining to another installed skill.

# PRD Pipeline (Per-Feature)

Three phases — decompose → per-feature PRD → cross-feature review. Consumes
`plans/{slug}/idea-brief.md`, emits `plans/{slug}/prd/` with one PRD per feature, a Mermaid
navigation graph, and a master INDEX.

## When to Use

- After running `kta-idea-pipeline` — `idea-brief.md` validated and `feature_seeds:` populated
- "I have an idea brief, write the PRDs"
- "Break my MVP scope into feature specs with screen lists"
- "Generate per-feature PRDs from this idea"
- Re-running on existing `prd/` to refresh after idea-brief changes

## How the pipeline works

The pipeline pre-fills ~60% of PRD fields with sensible defaults (Settings always has
account/notifications/theme/about; Auth always has email + 1 social provider; etc.). The student
picks from options offered by the skill instead of writing fields from scratch. There are no modes,
no levels, no toggles — this is the natural flow.

## Workflow

1. **Phase 1 — Decompose** — read `references/phase-1-decompose.md`. Read `idea-brief.md`, validate
   `feature_seeds` (5–8 items) present. AI proposes 4–8 features grouped by 5 user-journey buckets (
   Acquisition / Activation / Core Loop / Retention / Settings). Student edits/approves. **Hard cap
   8** — skill refuses 9th. **Monetization is OUT OF SCOPE** in this phase — refuse
   paywall/IAP/subscription/billing features and tell the student to defer to a later phase.
2. **Phase 2 — Per-Feature PRD** — read `references/phase-2-feature-prd.md`. Loop. Each feature gets
   one PRD using `references/feature-prd-template.md`. Screens nested inside (NOT separate PRDs per
   screen). Save `plans/{slug}/prd/{NN}-{feature-slug}.md`.
3. **Phase 3 — Cross-Feature Review** — read `references/phase-3-cross-review.md`. Generate Mermaid
   `nav-graph.mmd` (screens as nodes, navigation as edges). Surface shared components and naming
   conflicts. Write `INDEX.md`.
4. **Phase 4 — Handoff (MANDATORY)** — after `INDEX.md` is written, use `AskUserQuestion` to offer
   the next step. See "Handoff Prompt" section below.

## Handoff Prompt (Phase 4)

**Trigger condition (STRICT)**: fire ONLY after ALL feature PRDs from Phase 2 are written AND
`INDEX.md` + `nav-graph.mmd` from Phase 3 are written. Do NOT fire mid-loop after a single feature
PRD. Do NOT fire if any feature in the Phase 1 approved list is missing its `{NN}-{feature-slug}.md`
file. The handoff is a Phase 3 boundary — confirm all PRD files exist on disk before proceeding.

Immediately after writing `plans/{slug}/prd/INDEX.md` (last file of Phase 3), surface the absolute
path of the PRD directory in a one-line confirmation, then call `AskUserQuestion`:

```
header: "Next Step"
question: "PRDs written to {abs prd dir}. What next?"
multiSelect: false
options:
  - label: "Run design", description: "Auto-run kta-design-spec with PRD dir path"
  - label: "Pick feature", description: "Run kta-design-spec for ONE specific PRD only"
  - label: "Exit to read", description: "Stop here so I can read PRDs first"
```

Branching:

- If user picks **"Run design"** → invoke `Skill tool` with `skill: "kta-design-spec"` and `args`
  containing the absolute path of the PRD directory (e.g., `args: "plans/{slug}/prd/"`). Downstream
  skill takes over.
- If user picks **"Pick feature"** → emit a second `AskUserQuestion` with one option per feature PRD
  file (label = feature slug ≤17 chars, description = 1-line feature summary from PRD). On
  selection, invoke `Skill tool` with `skill: "kta-design-spec"` and `args` = absolute path of the
  chosen single PRD file.
- If user picks **"Exit to read"** → end the skill cleanly. Print the PRD dir path one more time. Do
  NOT proactively run any other skill.

This handoff is non-optional — every successful run of `kta-prd-pipeline` ends with this question.
If `INDEX.md` failed to write, skip the handoff and surface the error instead.

## Inputs

- `plans/{slug}/idea-brief.md` (required) — must include `feature_seeds:` 5–8 items
- Optional — student overrides on proposed feature list

## Outputs

- `plans/{slug}/prd/INDEX.md` — master feature list with status + screen counts
- `plans/{slug}/prd/nav-graph.mmd` — Mermaid LR-flowchart of screen navigation
- `plans/{slug}/prd/{NN}-{feature-slug}.md` — one per feature (4–8 files)

## Integration

- **Previous stage** — `kta-idea-pipeline` (provides idea-brief.md)
- **Next stage** — `kta-design-spec` (consumes per-feature PRDs to emit per-screen design specs)

## Constraints

- **Hard 8-feature cap** — Phase 1 refuses 9th feature; student must consolidate or defer to V2
- 5 journey buckets are FIXED — no ad-hoc buckets, no Monetization bucket in this phase
- Screens always nested inside feature PRDs — NEVER emit per-screen PRDs
- No project-stack-specific defaults — generic patterns only (no Supabase / DRE-KT mentions in
  feature catalog)
- Skill emits markdown only, no code
- Validates `feature_seeds` exist in idea-brief before running — refuses with clear error otherwise
- Default working directory — `plans/{slug}/`
- Phase 4 handoff is **mandatory** AND fires ONLY after ALL feature PRDs + Phase 3 outputs (
  `INDEX.md`, `nav-graph.mmd`) are on disk. Never trigger mid-loop. Offers "Run design" (auto-chains
  to `kta-design-spec` with PRD dir), "Pick feature" (single-PRD design run), or "Exit to read"

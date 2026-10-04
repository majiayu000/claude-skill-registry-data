---
name: kta-design-spec
description: Per-screen design spec generator for AI design tools (Stitch / Figma AI / Claude artifacts). Consumes per-feature PRDs from kta-prd-pipeline. Emits tool-agnostic markdown specs. Triggers — design spec, AI design prompt, screen mockup brief, Figma AI input, Stitch prompt, design system tokens, post-PRD design phase, generate design specs, design brief, mockup spec. DOES NOT generate Compose code, Kotlin code, or @Preview stubs.
---

## Platform Tooling

- Use AskUserQuestion for blocking user choices or confirmations.
- Use WebFetch/WebSearch for current external docs or public web research.
- Use Task tool with subagent_type for delegation.
- Use Skill tool when chaining to another installed skill.

# Design Spec Pipeline (Per-Screen)

Three phases — style-foundation (once) → per-screen spec (loop) → bundle into single upload file.
Consumes `plans/{slug}/prd/*.md`, emits `plans/{slug}/design/` with per-screen specs plus one
consolidated `design-bundle.md` ready to upload to any Design AI Tool.

## When to Use

- After running `kta-prd-pipeline` — per-feature PRDs with screen lists exist
- "Generate design specs for my AI design tool"
- "Write Stitch / Figma AI / Claude design prompts for these screens"
- "I need design briefs to feed into a text-to-UI tool"
- Re-running per-screen to refresh after PRD changes

## CRITICAL CONSTRAINTS

- **SKILL EMITS DESIGN SPECS ONLY — NEVER GENERATE COMPOSE CODE, KOTLIN, OR @PREVIEW STUBS**
- **COMPONENT-STATES LIST IS MANDATORY — SKILL REFUSES INCOMPLETE SPEC**
- **REAL COPY ONLY — NO LOREM IPSUM**

These rules are absolute. Every reference file reinforces them. If the LLM is tempted to produce
Kotlin / `@Composable` / `@Preview`, STOP and re-read this section.

## How the pipeline works

The pipeline pre-fills sensible defaults (component-state defaults, copy options) and walks the
student through each screen step by step. There are no modes, no levels, no toggles — pre-fill, the
student picks from options, move forward.

## Pre-flight Validation (GATE — runs FIRST, before Phase 1)

**Before any phase runs, validate the input. If validation fails, STOP and return — do NOT proceed
to Phase 1.**

Run these checks in order, in `plans/{slug}/`:

1. **PRD directory exists** — `plans/{slug}/prd/` is a directory.
2. **At least one feature PRD file** — at least one `prd/{NN}-{feature-slug}.md` exists (NN =
   2-digit prefix).
3. **`prd/INDEX.md` exists** — produced by `kta-prd-pipeline` Phase 3.
4. **Every feature PRD has a `## Screens` section with ≥1 screen named in PascalCase.**
5. **No empty PRD files** — each feature PRD is >200 chars (sanity check, not a TBD-only stub).

If any check fails, STOP and emit (no further phases run):

```
[kta-design-spec] Cannot proceed — input not qualified.

Failed checks:
- {check that failed} — {what was found vs expected}
- ...

Required input shape:
  plans/{slug}/prd/
    INDEX.md
    01-{feature}.md   (with `## Screens` section, screens in PascalCase)
    02-{feature}.md
    ...

Fix path:
  → Run `kta-prd-pipeline` first to generate the PRD set.
  → Or check the slug — passed dir must point to a plans/{slug}/ root.

This skill emits no design specs until input is qualified.
```

Then return. Do NOT prompt the user to "fix and continue inline" — the upstream skill (
`kta-prd-pipeline`) is the right place to repair PRD shape. The student can re-invoke
`kta-design-spec` after.

## Workflow

1. **Phase 1 — Style Foundation** (once per app) — read `references/phase-1-style-foundation.md`.
   Capture mood/voice, color tokens (or "use Material 3 default"), typography,
   spacing/radii/elevation, references (3 inspirations + 1 anti), motion intent, a11y floor. Save
   `plans/{slug}/design/style-foundation.md`. **Phase 2 GATES on this file existing.**
2. **Phase 2 — Per-Screen Spec** — read `references/phase-2-screen-spec.md`. Loop screens across all
   PRDs. Emit one spec per screen at `plans/{slug}/design/{NN-feature-slug}/{NN-screen-slug}.md`.
   Component-states list MANDATORY. Validate before emit.
3. **Phase 3 — Bundle (MANDATORY)** — after all per-screen specs are written, run
   `scripts/bundle_design_specs.py` to concatenate `style-foundation.md` + `INDEX.md` + every
   per-screen spec into a single `plans/{slug}/design/design-bundle.md`. This single file is the
   canonical output the student uploads to Stitch / Claude / Figma AI. See "Bundle Step" section
   below.

**There is no per-tool reformatting phase.** Modern Design AI tools accept generic markdown; the
bundle is tool-agnostic by design. If a specific tool ever chokes on bundle size, paste a single
feature folder's screens instead — the per-screen files are still on disk for that.

## Bundle Step (Phase 3)

Run after Phase 2 completes — non-optional unless the student explicitly opts out.

**Command** (use the project venv Python; fallback to `python3` if venv missing):

```bash
python3 .claude/skills/kta-design-spec/scripts/bundle_design_specs.py plans/{slug}/design/
```

The script produces `plans/{slug}/design/design-bundle.md` containing, in order:

1. Bundle header (title + generation timestamp + upload instructions)
2. `style-foundation.md` (full content)
3. `INDEX.md` (full content if present)
4. Each feature directory in NN order, each per-screen spec inside in NN order, with separator
   comments between sections

**After the script runs**, surface the absolute output path back to the student in one line, then
call `AskUserQuestion`:

```
header: "Next Step"
question: "Bundle written to {abs path}. What next?"
multiSelect: false
options:
  - label: "Open in tool", description: "Print upload instructions for Stitch/Claude/Figma AI"
  - label: "Exit",         description: "Stop here — I'll upload the bundle myself"
```

If the script fails (missing `style-foundation.md` or no feature dirs), surface stderr and DO NOT
proceed to the handoff prompt. Re-run Phase 2 first.

## Inputs

- `plans/{slug}/prd/*.md` (required) — feature PRDs with screens
- `plans/{slug}/idea-brief.md` (recommended) — for value-prop context

## Outputs

- `plans/{slug}/design/style-foundation.md` — once per app
- `plans/{slug}/design/INDEX.md` — feature → screens → spec file map
- `plans/{slug}/design/{NN-feature-slug}/{NN-screen-slug}.md` — one per screen
- `plans/{slug}/design/design-bundle.md` — single concatenated file ready to upload to Stitch /
  Claude / Figma AI (produced by `scripts/bundle_design_specs.py` in Phase 3)

## Integration

- **Previous stage** — `kta-prd-pipeline` (provides per-feature PRDs)
- **Next stage** — paste spec into AI design tool (Stitch / Figma AI / Claude artifacts) to generate
  mockups. **NOT into a code generator.**

## Constraints

- **Pre-flight gate** — input MUST pass all pre-flight checks (PRD dir, ≥1 feature PRD, INDEX.md,
  screens section in each PRD, non-stub files). If not qualified, skill returns immediately with a
  fix path; no design specs emitted.
- **Design spec only** — no Compose / Kotlin / `@Preview` / DSL snippets. Reinforced in every
  reference file.
- **Component-states list mandatory** — every component must list 6 states (default / pressed /
  disabled / loading / empty / error). Skill refuses incomplete spec.
- **Real copy** — every visible string spelled out; no lorem ipsum, no placeholders like `{title}`.
- **Style-foundation gate** — Phase 2 refuses to run if `style-foundation.md` missing.
- **Tool-agnostic** — Phase 2 output is pure markdown. Phase 3 bundle is the canonical upload
  artifact for any AI design tool. No per-tool reformatting phase.
- **No project-stack-specific tokens leaking in** — generic Material 3 defaults are fine; "
  DRE-KT" / "Compose" mentions forbidden.
- Skill emits markdown only.
- Default working directory — `plans/{slug}/`.

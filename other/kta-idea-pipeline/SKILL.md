---
name: kta-idea-pipeline
description: End-to-end Android indie idea workflow — feature-build phase only (no monetization). Phased — discover (if no idea) → generate 2 candidates → refine scope (offline/online, sharing, MVP vs full, core-value features) → risk/reward/tradeoff analysis when scoping down → emit idea brief. Use for greenfield app concepts, new feature ideation, idea discovery, or pre-design discovery before writing a design document. Triggers — new app idea, feature concept, indie dev brainstorm, validate idea, refine idea, what should I build, find an app idea, idea pipeline, I have no idea, help me find an app idea, scope down, MVP scoping, core value features.
---

## Platform Tooling

- Use AskUserQuestion for blocking user choices or confirmations.
- Use WebFetch/WebSearch for current external docs or public web research.
- Use Task tool with subagent_type for delegation.
- Use Skill tool when chaining to another installed skill.

# Idea Pipeline (Android Indie — Feature Build Phase)

Single skill, four phases — discover (conditional) → generate 2 → refine scope → brief. Output is an
`idea-brief.md` ready for `kta-prd-pipeline`. The flow is **shape-the-idea**, not **kill-the-idea**.

**Scope of this skill (current phase): FEATURE BUILD ONLY.** Monetization is intentionally OUT of
scope here — we focus on identifying core value, picking the right feature surface to ship, and
exposing risk/reward/tradeoff when scoping down. Pricing/billing/ads decisions belong to a later
monetization pass after the feature value is validated.

## Guiding Mantra (Surface to User in Every Phase)

**Ship finished > ship perfect. Perfect never exists. Ship and improve is the key of success.**

Apply **YAGNI** aggressively in every phase — when generating ideas, scoping MVP, picking features.
Default-cut anything that doesn't serve the core value loop; defer to v2. When user adds scope,
remind them: a shipped Lean MVP teaches more than a polished concept stuck in dev.

**Core-value-first principle**: prioritize the *one* feature that delivers the irreplaceable user
value. Every other feature is a candidate for cut — and each cut should be reasoned through with
explicit risk/reward/tradeoff (see Phase 2).

## When to Use

- "I want to build an Android app but need an idea"
- "I have no idea what to build"
- "Validate this concept: …"
- "Help me find an indie dev niche"
- New feature ideation for an existing app
- Pre-PRD entry point
- "Help me scope down my idea to core value"

## Step-by-Step Interaction Rule (NON-NEGOTIABLE)

**This skill ALWAYS guides the user step by step via `AskUserQuestion`.** Every choice, pick,
select, flag, confirm, or rank — use the tool. Never emit raw markdown questions and wait for
prompt-response. There are no modes, no levels, no toggles — the natural flow is: ask one thing at a
time, the user picks an option, the skill moves forward. Pre-fill sensible defaults wherever
possible so the student is selecting from options, not writing fields from scratch.

Single-select → `multiSelect: false`. Multi-select (e.g., flag favorites) → `multiSelect: true`.
Always include 2–4 concrete options + a free-text "Other" option when relevant. Keep `header` ≤12
chars, `question` ≤80 chars, each option `label` ≤17 chars.

Applies to: trigger path, seed favorites, candidate pick, scope decisions (surface / connectivity /
sharing / accounts), feature cut/keep, handoff, etc. **Do NOT batch multiple decisions into one
prompt** — one question at a time, walk the user through.

## Workflow

0. **Phase 0 — Discover** *(conditional)* — read `references/phase-0-discover.md`. Run ONLY if
   student has no idea or asks "help me find one". Pick ONE of 7 trigger paths (personal pain,
   hobby-driven, niche-of-niche, reskin-with-wedge, trending Play Store, daily-tool gap, sunset-tool
   revival) — outputs 5–10 seed concepts. WebFetch sources in `references/discovery-sources.md`;
   fallback to prompt-only on fetch failure.
1. **Phase 1 — Generate** — read `references/phase-1-generate.md`. Produce **exactly 2** candidate
   ideas (not 3-5) with: problem, target user, core value (one sentence), MVP scope,
   differentiation, killer feature. **No monetization fields.** Use `AskUserQuestion` to advance one
   or both (or regenerate).
2. **Phase 2 — Refine & Adjust** — read `references/phase-2-challenge.md`. NOT a kill phase. Tight
   approach analysis (core loop, riskiest assumption, wedge, tech-stack fit, build estimate), then
   walk the student through scope decisions: app surface (Lean MVP / Standard / Full),
   connectivity (offline-only / offline-first / online), sharing (none / share-out / light social /
   full social), accounts, and a final core-value feature cut/add pass. **For each scope-down
   decision, surface explicit Risk / Reward / Tradeoff bullets** so the student is making the cut
   with eyes open. Each decision uses `AskUserQuestion`.
3. **Phase 3 — Brief** — read `references/phase-3-brief-template.md`. Emit
   `plans/{slug}/idea-brief.md` with refined-spec block + `feature_seeds` populated for
   `kta-prd-pipeline` and `kta-design-spec` consumption. **Brief template has no monetization
   section** — that's a separate pass.
4. **Phase 4 — Handoff (MANDATORY)** — after the brief file is written, use `AskUserQuestion` to
   offer the next step. Do NOT print raw text choices — use the tool. See "Handoff Prompt" section
   below.

## Handoff Prompt (Phase 4)

Immediately after writing `plans/{slug}/idea-brief.md`, surface the absolute path of the brief in a
one-line confirmation, then call `AskUserQuestion`:

```
header: "Next Step"
question: "Brief written to {abs path}. What next?"
multiSelect: false
options:
  - label: "Run PRD next", description: "Auto-run kta-prd-pipeline with this brief path"
  - label: "Exit to read", description: "Stop here so I can read the brief first"
```

Branching:

- If user picks **"Run PRD next"** → immediately invoke the `kta-prd-pipeline` skill via the
  `Skill tool`, passing the absolute brief path as input (e.g.,
  `args: "plans/{slug}/idea-brief.md"`). Do NOT wait for further confirmation; the user already
  confirmed. The downstream skill takes over the conversation.
- If user picks **"Exit to read"** → end the skill cleanly. Print the brief path one more time so
  the user can open it. Do NOT proactively run any other skill.

This handoff is non-optional — every successful run of `kta-idea-pipeline` ends with this question.
If the brief failed to write, skip the handoff and surface the error instead.

## Inputs

- User intent (free text)
- Optional — niche, target platform, time/budget constraint

## Outputs

- `plans/{slug}/idea-brief.md` — schema in `references/phase-3-brief-template.md`. Must include
  `feature_seeds:` (5–8 candidate features) for `kta-prd-pipeline` consumption.

## Integration

- **Next stage** — `kta-prd-pipeline` (decomposes idea-brief into per-feature PRDs with screens
  nested)
- **Out of scope here** — monetization, pricing, billing, ads. Handle in a separate later pass once
  feature value is validated.
- Standalone — yes, output is human-readable

## Constraints

- Phase 0 runs only when needed — don't force discovery when student already has an idea
- Phase 1 emits **exactly 2** ideas — no more (token efficiency, easier comparison)
- Phase 1/2/3 NEVER ask about monetization, pricing, IAP, ads, subscription. If user volunteers
  monetization preferences, capture in a one-line note `monetization_note:` in the brief frontmatter
  and move on — no decision tree, no scope choice.
- Phase 2 is **refine-not-kill** — assume the idea ships, decide its shape via scope choices (
  offline/online, sharing, MVP vs full, accounts, core-value features). NO 1–5 scoring, NO kill
  verdicts.
- Phase 2 scope-down questions MUST surface **Risk / Reward / Tradeoff** bullets in the question
  description so the cut is reasoned, not reflexive.
- Skill emits markdown only, no code
- Default working directory — `plans/{slug}/` (current plan's slug)
- WebFetch in Phase 0 is best-effort — has prompt-only fallback
- Phase 4 handoff is **mandatory** — every successful brief write ends with the AskUserQuestion
  offering "Run PRD next" (auto-chains to `kta-prd-pipeline` with brief path) or "Exit to read"

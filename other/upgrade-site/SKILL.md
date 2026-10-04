---
name: upgrade-site
description: Orchestrate a full website design upgrade — snapshot the current site, research references via design-dna, synthesize a direction, score the gaps, write a prioritized plan, dispatch implementation to motion-craft and build skills, and verify. Use when asked to "upgrade the site", "make it award-winning", "run the upgrade pipeline", or "audit the site design". Vague requests get a plan, not code changes.
user-invocable: true
argument-hint: "[target repo path] [audit|plan|implement] [optional reference URLs]"
compatibility: Designed for Claude Code. Requires the design-dna and motion-craft skills from this plugin, public internet access, git, and browser tooling for snapshots.
metadata:
  version: "1.0.0"
  author: augchan42
  schema-version: "1"
---

# Upgrade Site (Orchestrator)

You own scope, synthesis, sequencing, and verification.
`design-dna` observes and abstracts; it never implements.
`motion-craft` implements against blueprints; it never researches references.
All handoffs are Markdown artifacts beneath the target repository, and all
implementation is constrained by the target project's own architecture and
route policies.

## Authority modes

```text
audit      Snapshot, research, report only.        (explicit "audit")
plan       Audit + written upgrade plan.           (DEFAULT — vague requests
                                                    like "make it look better")
implement  Plan + modify code + verify.            (explicit only: "implement",
                                                    "run the full pipeline")
```

What each mode may write:

```text
audit:      evidence + audit report only. May NOT modify application source,
            dependencies, configuration, or design docs.
plan:       + blueprints, synthesis, plan documents, MOTION.md policy seed.
            May NOT modify application source, dependencies, runtime config.
implement:  may modify approved source and configuration.
```

The audit/plan restriction is on source mutation, not filesystem writes —
artifacts beneath the contract paths are always permitted for the mode that
produces them. Never auto-edit `.gitignore`; recommend entries instead.

## Target resolution

```text
target_repo = explicit path → current git root → cwd
```

Canonicalize; refuse `/` or `$HOME`; all writes beneath the target; log the
resolved target and chosen mode before doing anything else.

## Pipeline

1. **Snapshot** key pages (home + 2–4 representative templates) × viewports
   390×844 and 1440×900 → `.artifacts/site-upgrade/<run-id>/baseline/`.
   If the target's HEAD materially differs from the deployed site, snapshot
   a local build; otherwise the production site is an acceptable baseline.
   Record which was used.
2. **References** — invoke `design-dna` (research mode unless URLs given).
3. **Synthesize** → `<target_repo>/design-dna/synthesis.md` covering: shared
   patterns; meaningful disagreements; which reference leads each dimension;
   combinations that must not be mixed; recommended direction for the
   target; patterns rejected for brand/content fit.
4. **Gap analysis** — score the target vs the synthesis, 0–10 per dimension:
   typography, color, layout, imagery, motion, **brand fit** — each with
   "what would make it a 10".

   ```text
   0–2 absent/harmful · 3–4 inconsistent/unfinished · 5–6 competent baseline
   7–8 distinctive and coherent · 9 exceptional · 10 reference-quality (rare)
   ```

   **Accessibility and performance are gates, not tradable dimensions** — no
   visual ambition may lower either below the current baseline. Record the
   scores and each "what would make it a 10" in the plan document (or the
   audit report in audit mode).
5. **Plan** → `<target_repo>/docs/plans/` following the target's existing
   naming conventions. Order: quick wins → signature moments. Include the
   project-policy seed for `docs/MOTION.md`: excluded high-volume templates,
   animation-eligible surfaces, locale list. Write the seed as a PLAIN
   section at the top of `docs/MOTION.md`, above any motion-craft managed
   sections; once written it belongs to the project (motion-craft never
   edits content outside its managed markers).
6. **Dispatch** (implement mode only) — motion items → `motion-craft`
   (inherits implement authority); static design items → the project's build
   skills (e.g. editorial-designer / frontend-design) following the plan.
7. **Close** — re-snapshot changed pages, run a design-review pass if that
   skill is available, and complete motion-craft's verification gates.

## Git safety (implement mode)

Same rules as motion-craft: target must be a git repo; stop on a dirty tree
with unrelated changes; prefer a dedicated branch; commit only when the
worktree was clean and gates passed — otherwise leave changes uncommitted
with a proposed commit breakdown.

## Failure behavior

A blocked reference, missing browser tooling, or an unavailable sub-skill
degrades the run (partial blueprint, `N/A` evidence, deferred items with
rationale) — it never halts the pipeline waiting for input in a
non-interactive run.

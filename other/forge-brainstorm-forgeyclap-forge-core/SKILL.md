---
name: forge-brainstorm
description: Forge structured-ideation playbook. Use BEFORE building when the approach isn't obvious — brainstorm, options, trade-offs, alternatives, design direction, which way to build.
---

# Forge playbook — Structured ideation (brainstorm before build)

**Do not duplicate ECC skills — defer to:** `brainstorming` (the deep design-dialogue methodology; it ships with Forge as a pinned vendored skill). This
file is the Forge-specific orchestration wrapper: a compact diverge → converge loop sized for a `/forge`
work package rather than a full standalone design doc.

## Hard rules
- **No implementation before a written pick + rationale.** Even a "simple" task benefits from naming the
  2-3 real alternatives and why one was chosen — unexamined assumptions on "simple" work cause the most
  rework.
- If the request is genuinely ambiguous in a way that changes the answer, ask the ONE most
  decision-changing question before diverging (superseded 2026-09: the owner's `intake` config default
  is `silent`, capping the whole build at **at most one** owner question total — this skill does not get
  its own separate question budget); otherwise pick the sensible default, state it, and proceed — never
  silently guess on something consequential.
- Constraints are gathered from real project evidence (existing architecture, stack, `CLAUDE.md`,
  `FORGE_PROJECT_PROFILE.md`) — not invented defaults that ignore the actual codebase.
- Do not over-invest: this is a short loop, not a multi-day design-doc process. Match the depth to the
  task's real complexity/risk (see the fan-out table in `CLAUDE.md`).

## The loop (diverge → constraints → converge → smallest viable first)
1. **Diverge.** List 2-4 genuinely different approaches (not trivial variations of the same one). For
   each: name and what it is · why it could work here · real cost (time/complexity/risk) · one risk it does not address — side by side, so hidden assumptions show.
2. **Constraints.** Apply what actually limits the choice here: existing architecture/conventions, stack,
   team size/skills available, time/complexity budget (fan-out level), security/compliance posture,
   anything the owner already ruled out.
3. **Converge.** Pick one approach and give the rationale in 1-3 sentences — why this one beats the
   alternatives *for this project*, not in the abstract. Name what was explicitly rejected and why.
4. **Smallest viable first.** Scope the smallest slice that proves the approach works end-to-end before
   building the full version — the first work package should be small enough to verify quickly, not the
   whole feature at once.

## Output
A short note (inline in the plan, or `docs/` if the project already uses design docs) containing:
options considered · constraints applied · the pick + rationale · rejected alternatives + why · the
smallest-viable-first slice. This becomes the input to the next step, not an end in itself.

## Feeds into
The output of this skill is consumed by `planner`/`architect` (or the Lead directly on small tasks) to
write the actual work package(s) — `forge-brainstorm` never produces code itself; it produces the
decision that the work package is built from.

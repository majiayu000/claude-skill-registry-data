---
name: plan-eng-review
description: "Review execution approach for feasibility, architecture, data flow, edge cases, test coverage, performance, and security risks. Auto-detects mode: concept-mode reviews a pitch (OFFICE-HOURS.md) for technical feasibility before any scaffolding; milestone-mode reviews slice-plans (M###-S##-PLAN.md) before plan-task. Use concept-mode optionally after plan-ceo-review to sanity-check the pitched approach; use milestone-mode after slice-milestone to lock architecture before implementation. Thin ytstack wrapper around the vendored gstack plan-eng-review procedure."
allowed-tools:
  - Bash
  - Read
  - Edit
  - AskUserQuestion
---

# ytstack:plan-eng-review

Thin wrapper around the vendored gstack `plan-eng-review` skill (`vendor/gstack/plan-eng-review/SKILL.md`). Injects ytstack slice-plan context, then inlines the vendored procedure verbatim. Vendor is single source of truth.

## ytstack context (resolved at render time)

```!
cd "${CLAUDE_PROJECT_DIR:-$PWD}" 2>/dev/null || true
_PROJECT_SLUG=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || basename "$(pwd)")
if [ -d "$PWD/.ytstack" ]; then _YT_DIR="$PWD/.ytstack";
elif [ -d "$HOME/.ytstack/projects/$_PROJECT_SLUG" ]; then _YT_DIR="$HOME/.ytstack/projects/$_PROJECT_SLUG";
else _YT_DIR=""; fi
_CURRENT_MILESTONE=none
if [ -n "$_YT_DIR" ] && [ -f "$_YT_DIR/STATE.md" ]; then
  _CURRENT_MILESTONE=$(sed -n 's/^current_milestone: *//p' "$_YT_DIR/STATE.md" | head -1)
fi
_SLICE_PLANS=""
if [ -n "$_CURRENT_MILESTONE" ] && [ "$_CURRENT_MILESTONE" != "none" ] && [ -d "$_YT_DIR" ]; then
  _SLICE_PLANS=$(ls "$_YT_DIR"/$_CURRENT_MILESTONE-S[0-9][0-9]-PLAN.md 2>/dev/null | tr '\n' ' ')
fi
_PITCH=""
if [ -f "./OFFICE-HOURS.md" ]; then
  _PITCH="./OFFICE-HOURS.md"
elif [ -n "$_YT_DIR" ]; then
  _PITCH=$(ls "$_YT_DIR"/OFFICE-HOURS-*.md 2>/dev/null | head -1)
fi
if [ -n "$_SLICE_PLANS" ]; then
  _MODE=milestone
elif [ -n "$_PITCH" ] && [ -f "$_PITCH" ]; then
  _MODE=concept
else
  _MODE=abort
fi
echo "HAS_YTSTACK: $([ -n "$_YT_DIR" ] && echo yes || echo no)"
echo "MODE: $_MODE"
echo "CURRENT_MILESTONE: $_CURRENT_MILESTONE"
echo "SLICE_PLANS: ${_SLICE_PLANS:-none}"
echo "PITCH: ${_PITCH:-none}"
```

## ytstack invocation notes

Two modes, auto-detected above:

**Mode = milestone** (slice-plans exist). The "plan" being engineering-reviewed is the current milestone's slice-plans. Read those files when the vendored procedure asks what to review. Architecture, data flow, edge cases, test coverage, performance.

**Mode = concept** (no slice-plans yet; pitch artifact produced by `ytstack:office-hours` exists). The "plan" being engineering-reviewed is the pitch at `_PITCH`. Focus the review on feasibility + architectural risk of the pitched approach BEFORE any infra is scaffolded: is the target tech stack viable, are there hidden integration complexities, are the perf/scale expectations realistic, are there obvious security / data-handling gaps. Output the feasibility verdict + top 3 risk items. Concept-mode eng review is OPTIONAL per the locked greenfield flow (DECISIONS 2026-04-24); office-hours + plan-ceo-review can proceed to init-project without it.

**Mode = abort.** If neither slice-plans nor a pitch artifact exist, abort with: "Run `ytstack:office-hours` first (concept-mode review) or `ytstack:slice-milestone` first (milestone-mode review). plan-eng-review reviews existing plan content; it does not produce it." Do NOT invoke the vendored procedure.

After the vendored procedure completes:

- **Milestone mode:** apply review outcomes by editing the affected slice-plans (add edge cases, adjust tests, tighten scope). Append any locked architectural decision to `DECISIONS.md` in append-only format.
- **Concept mode:** append the feasibility verdict + risk-item list as an annotation block at the top of `_PITCH`. If "go", recommend `ytstack:init-project`. If "stop / rescope", recommend revisiting office-hours on the affected question.

## Vendored procedure (inlined verbatim)

```!
cat "${CLAUDE_SKILL_DIR}/../../vendor/gstack/plan-eng-review/SKILL.md"
```

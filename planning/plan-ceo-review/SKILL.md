---
name: plan-ceo-review
description: "Challenge premise, scope, and ambition via four modes: SCOPE EXPANSION, SELECTIVE EXPANSION, HOLD SCOPE, SCOPE REDUCTION. Auto-detects mode: concept-mode reviews a pitch (OFFICE-HOURS.md) before any scaffolding exists; milestone-mode reviews a committed milestone (M###-CONTEXT.md + M###-ROADMAP.md) before slicing. Use concept-mode right after office-hours to stress-test the pitch; use milestone-mode after plan-milestone and before slice-milestone. Thin ytstack wrapper around the vendored gstack plan-ceo-review procedure."
allowed-tools:
  - Bash
  - Read
  - Edit
  - AskUserQuestion
---

# ytstack:plan-ceo-review

Thin wrapper around the vendored gstack `plan-ceo-review` skill (`vendor/gstack/plan-ceo-review/SKILL.md`). Injects ytstack milestone context, then inlines the vendored procedure verbatim so it runs without adapt / fork drift. Vendor is single source of truth; upstream updates flow through.

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
_CONTEXT_FILE="$_YT_DIR/$_CURRENT_MILESTONE-CONTEXT.md"
_ROADMAP_FILE="$_YT_DIR/$_CURRENT_MILESTONE-ROADMAP.md"
# Concept-mode pitch discovery: greenfield OFFICE-HOURS.md, or brownfield .ytstack/OFFICE-HOURS-*.md
_PITCH=""
if [ -f "./OFFICE-HOURS.md" ]; then
  _PITCH="./OFFICE-HOURS.md"
elif [ -n "$_YT_DIR" ]; then
  _PITCH=$(ls "$_YT_DIR"/OFFICE-HOURS-*.md 2>/dev/null | head -1)
fi
# Mode detection
if [ "$_CURRENT_MILESTONE" != "none" ] && [ -f "$_CONTEXT_FILE" ] && [ -f "$_ROADMAP_FILE" ]; then
  _MODE=milestone
elif [ -n "$_PITCH" ] && [ -f "$_PITCH" ]; then
  _MODE=concept
else
  _MODE=abort
fi
echo "HAS_YTSTACK: $([ -n "$_YT_DIR" ] && echo yes || echo no)"
echo "MODE: $_MODE"
echo "CURRENT_MILESTONE: $_CURRENT_MILESTONE"
echo "CONTEXT_FILE: $_CONTEXT_FILE ($([ -f "$_CONTEXT_FILE" ] && echo yes || echo no))"
echo "ROADMAP_FILE: $_ROADMAP_FILE ($([ -f "$_ROADMAP_FILE" ] && echo yes || echo no))"
echo "PITCH: ${_PITCH:-none}"
```

## ytstack invocation notes

This wrapper runs in one of two modes, auto-detected above:

**Mode = milestone** (a ytstack milestone exists). The "plan" being CEO-reviewed is the current milestone's CONTEXT + ROADMAP. Read `_CONTEXT_FILE` and `_ROADMAP_FILE` when the vendored procedure asks what plan to review. Do NOT prompt the user to identify the plan.

**Mode = concept** (no milestone yet; pitch artifact produced by `ytstack:office-hours` exists). The "plan" being CEO-reviewed is the pitch at `_PITCH`. Treat it as a project-concept: challenge premise, scope, target user, differentiation. Output the decision to proceed / rescope / kill. Concept-mode CEO review runs BEFORE `init-project`, per the locked greenfield flow (DECISIONS 2026-04-24 "Greenfield-flow reorder").

**Mode = abort.** If neither a milestone plan nor a pitch artifact exists, abort with: "Run `ytstack:office-hours` first to produce a pitch, or run `ytstack:plan-milestone` to produce a milestone plan. plan-ceo-review reviews an existing plan; it does not produce one." Do NOT invoke the vendored procedure.

After the vendored procedure completes:

- **Milestone mode:** apply the review outcome by editing `_ROADMAP_FILE` (add / reorder / remove slices per approval). Append any locked scope decision to `DECISIONS.md` in append-only format. Update `STATE.md` `last_updated` and next-action if slicing changed.
- **Concept mode:** write the review outcome as an annotation block at the top of `_PITCH` (e.g. `## CEO review 2026-04-24: hold / expand / reduce`, with reasoning). If the decision is "proceed", recommend `ytstack:plan-eng-review` (if not yet run) or `ytstack:init-project` to scaffold. If "kill" or "rescope", recommend re-running office-hours on the affected questions before any commit.

## Vendored procedure (inlined verbatim)

```!
cat "${CLAUDE_SKILL_DIR}/../../vendor/gstack/plan-ceo-review/SKILL.md"
```

---
name: deep-plan
description: "Use when starting a new feature or idea that needs thorough pre-execution planning. Use instead of calling /product-review, /spec, and review skills individually."
allowed-tools: Read, Bash, Glob, Grep, Skill, AskUserQuestion
---

# /deep-plan $ARGUMENTS

Orchestrate the full planning pipeline in the correct order. Each phase invokes an existing skill via the Skill tool and presents a checkpoint before the next phase.

**This skill sequences sub-skills. It does NOT duplicate their content.**

## Argument Parsing

Arguments: `$ARGUMENTS`

Parse flags:
- `--yes` — Auto-answer all checkpoints with defaults (opt-in phases skip, opt-out phases run). Pass `--yes` to sub-skills that support it.
- `--skip-reviews` — Skip Phases 4-6 (deep eng + design + multi-review). Use when spec's Phase 2.5 inline reviews are sufficient.
- `--no-decompose` — Skip Phase 7 (Linear decomposition).
- Everything else = the feature description. Store as `$FEATURE`.

If `$FEATURE` is empty, ask: "What feature or idea do you want to plan?"

Do not proceed without a feature description.

## Phase 1: Product Review (always)

Run `/product-review` via Skill tool with `$FEATURE` as arguments.

Wait for completion. The sub-skill handles its own internal checkpoints (interrogation, DVF gate, mode selection).

**Checkpoint:**

If `--yes`: proceed automatically.

Otherwise, use AskUserQuestion:
- **Question:** "Product review complete. Continue to planning?"
- **Options:** "Continue to planning" (recommended) / "Stop here — need to rethink"

If user stops: output "Pipeline stopped after product review. Re-run `/deep-plan` when ready." Then STOP.

## Phase 2: Design Exploration (opt-in)

If `--yes`: skip this phase (default = skip for opt-in).

Otherwise, use AskUserQuestion:
- **Question:** "Explore 3-5 different UI directions before writing the spec? Recommended for UI-heavy features."
- **Options:** "Yes, explore directions" / "No, go straight to spec" (recommended)

**If yes:** Run `/design-shotgun` via Skill tool with `$FEATURE` as arguments. Wait for completion.

**If no:** Proceed.

## Phase 3: Spec (always)

Run `/spec` via Skill tool with `$FEATURE` as arguments.

`/spec` runs Phase 2.5 (lightweight eng + design review) inline and writes a plan file to `docs/plans/`. Wait for completion.

After `/spec` finishes, identify the plan file path. Store as `$PLAN_PATH`:
```bash
ls -t docs/plans/*.md 2>/dev/null | head -1
```

**Checkpoint:**

If `--yes`: proceed to Phase 4 (unless `--skip-reviews`, then jump to Phase 7).

Otherwise, use AskUserQuestion:
- **Question:** "Spec written to `$PLAN_PATH`. Phase 2.5 ran inline eng + design checks. What next?"
- **Options:** "Continue to deep reviews" (recommended) / "Skip reviews, go to decompose" / "Stop here — spec is the deliverable"

If "Skip reviews": jump to Phase 7.
If "Stop here": jump to Pipeline Summary.

## Phase 4: Engineering Review (opt-out)

If `--skip-reviews`: skip to Phase 7.

If `--yes`: run automatically.

Otherwise, use AskUserQuestion:
- **Question:** "Run deep engineering review? Full interactive review of architecture, code quality, tests, and performance — goes beyond Phase 2.5."
- **Options:** "Continue (recommended)" / "Skip"

**If continue:** Run `/plan-eng-review` via Skill tool with `$PLAN_PATH` as arguments.

**If skip:** Proceed.

## Phase 5: Design Review (opt-out)

If `--skip-reviews`: skip to Phase 7.

If `--yes`: run automatically.

Otherwise, use AskUserQuestion:
- **Question:** "Run deep design review? Scores 7 UI/UX dimensions 0-10 and fixes the plan."
- **Options:** "Continue (recommended)" / "Skip"

**If continue:** Run `/plan-design-review` via Skill tool with `$PLAN_PATH` as arguments.

**If skip:** Proceed.

## Phase 6: Multi-Review on Plan (opt-out)

If `--skip-reviews`: skip to Phase 7.

If `--yes`: run automatically.

Otherwise, use AskUserQuestion:
- **Question:** "Run specialized reviewers (security, performance, architecture) on the plan? Catches issues before code is written."
- **Options:** "Continue (recommended)" / "Skip"

**If continue:** Run `/multi-review` via Skill tool with `--plan $PLAN_PATH` as arguments.

**If skip:** Proceed.

## Phase 7: Decompose (opt-out)

If `--no-decompose`: skip to Pipeline Summary.

Check if Linear MCP is available (try calling `list_teams`). If unavailable, skip silently. Log: "Linear MCP not available — skipping decomposition."

Check if `/spec` already decomposed during Phase 3 (look for Linear issues associated with the plan). If already decomposed, skip.

If `--yes`: run decomposition automatically.

Otherwise, use AskUserQuestion:
- **Question:** "Decompose the plan into Linear issues for tracking and dispatch?"
- **Options:** "Yes, create issues (recommended)" / "No, plan file is sufficient"

**If yes:** Run `/spec` via Skill tool with `$PLAN_PATH` as arguments. Spec will detect the existing plan and offer decomposition.

**If no:** Proceed.

## Pipeline Summary

Output a completion summary:

```
═══════════════════════════════════════════
DEEP-PLAN COMPLETE
═══════════════════════════════════════════
Feature: $FEATURE
Plan: $PLAN_PATH

PHASES COMPLETED:
  1. Product Review     ✅
  2. Design Shotgun     ✅ / ⏭ skipped
  3. Spec               ✅  (Phase 2.5 inline review ran)
  4. Eng Review         ✅ / ⏭ skipped
  5. Design Review      ✅ / ⏭ skipped
  6. Multi-Review       ✅ / ⏭ skipped
  7. Decomposition      ✅ / ⏭ skipped / ⚠ Linear unavailable

NEXT STEPS:
  /orient → /dispatch         (parallel execution)
  /start-task <id>            (solo execution)
  /auto-run --through <id>    (autonomous execution)
═══════════════════════════════════════════
```

## Rules

- NEVER duplicate sub-skill content. This skill sequences, it does not replace.
- ALWAYS pass `$FEATURE` or `$PLAN_PATH` to sub-skills so they have context.
- NEVER skip Phase 1 (product review) or Phase 3 (spec). They are the backbone. If you don't want product review, use `/spec` directly.
- Each sub-skill handles its own internal interaction (questions, modes, outputs). This skill only manages transitions between them.
- If a sub-skill fails or the user exits it early, stop the pipeline. Do not silently continue.

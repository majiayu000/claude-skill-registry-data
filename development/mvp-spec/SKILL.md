---
name: mvp-spec
description: "Chains /mvp → /spec — analyzes an app from video/screenshots/description, then generates implementation stories. Triggers: analyze and spec, product analysis to stories, app teardown to specs, full analysis pipeline, mvp to spec."
version: "2.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---
instructions: |
  You are an autonomous analysis-to-spec agent. Do NOT ask the user questions.
  Run the full pipeline below without pausing between phases.

  INPUT:
  $ARGUMENTS

  The user will provide one or more of:
  1. A video file or screen recording of an application.
  2. Screenshots of an application.
  3. A URL or description of the application.
  4. Any combination of the above.

  ============================================================
  PHASE 1: PRODUCT ANALYSIS  (/mvp)
  ============================================================

  Follow the instructions defined in the `/mvp` skill exactly.
  Produce all sections of the `/mvp` output (Application Overview, Feature Inventory,
  MVP Definition, Architecture Assessment, UX/Design Analysis, Improvements, Story Candidates, Summary).

  Store the full output — you will use the Story Candidates and Feature Inventory
  in Phase 2.

  Do NOT stop here. Continue immediately to Phase 2.

  ============================================================
  PHASE 2: STORY GENERATION  (/spec)
  ============================================================

  Take every Story Candidate identified in Phase 1 and generate a full engineering
  spec for each one by following the `/spec` skill instructions exactly.

  For each story:
  - Use the feature context from the Phase 1 analysis as input
  - The `/spec` skill will auto-detect whether each story is full-stack, BE-only, or FE-only
  - Full-stack stories will produce both a BE and FE story with linked routes and schemas

  Order stories by implementation dependency — foundational stories (auth, models, core APIs)
  first, then features that build on them.

  ============================================================
  OUTPUT
  ============================================================

  When both phases are complete, print a summary:

  ---
  ## Spec Complete

  **Product:** [app name / description]
  **Stories generated:** [N] (BE: [N], FE: [N])

  **Implementation order:**
  1. [Story title] — [why first]
  2. [Story title] — [why next]
  3. ...

  **Next steps:**
  - Run `/arch-review [story]` to review a story before implementing
  - Run `/review-implement [story]` to review and implement in one pass
  - Run `/iterate [story]` to implement with autonomous refinement
  ---

  STRICT RULES:

  - Do NOT skip Phase 1 and jump to story generation.
  - Do NOT ask the user for input between phases.
  - Every story in Phase 2 must trace back to a feature or story candidate from Phase 1.
  - All rules from `/mvp` and `/spec` apply to their respective phases.


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing all phases, validate the combined output:

1. Re-run the specific checks that originally found issues to confirm fixes.
2. Run the project's test suite to verify fixes didn't introduce regressions.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat the fix-validate cycle up to 3 iterations total.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass
- No new issues introduced by fixes

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context
- Classify as requiring manual intervention or architectural changes


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /mvp-spec — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

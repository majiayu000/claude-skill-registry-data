---
name: retro
description: "Run a full retrospective and dev cycle analysis. Chains /recall → /new-features to reconstruct what went wrong, extract lessons learned, identify rework patterns, and synthesize feature ideas from the findings. Triggers: retrospective, retro, dev cycle analysis, what went wrong, lessons learned, postmortem, sprint retro."
version: "2.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous retrospective-to-ideation agent. Do NOT ask the user questions.
Run the full pipeline below without pausing between phases.

TARGET:
$ARGUMENTS

If arguments are provided, use them to scope the retrospective (branch name, date range, feature).
If no arguments are provided, analyze the full git history.

============================================================
PHASE 1: DEVELOPMENT RETROSPECTIVE  (/recall)
============================================================



PARALLEL EXECUTION: After /recall completes and produces findings, use the Agent tool to run follow-up analyses concurrently.
- Agent A (Feature Discovery): "Based on these recall findings: [findings summary], run /new-features to discover features that address the identified bottlenecks and rework patterns."
- Agent B (Metrics Check): "Based on these recall findings: [findings summary], compute development quality metrics and compare to baseline."
- Wait for both agents to complete and merge into the retrospective output.


Follow the instructions defined in the `/recall` skill exactly.

Produce the full retrospective output: Timeline Reconstruction, Pattern Extraction,
Dependency Mapping, and Insight Distillation.

Save the retrospective output to `docs/dev-retrospective.md` (create the `docs/` directory if it doesn't exist).

Key outputs to preserve for Phase 2:
- What caused rework (indicates areas needing better features/tooling)
- Where bottlenecks were (indicates areas needing improvement)
- Patterns of late discovery (indicates missing validation/features)
- Recommended improvements for the next cycle

Do NOT stop here. Continue immediately to Phase 2.

============================================================
PHASE 2: FEATURE IDEATION  (/new-features)
============================================================

Now follow the instructions defined in the `/new-features` skill exactly.

Read ALL `.md` files in the `docs/` directory — this includes
the `docs/dev-retrospective.md` you just wrote plus any other markdown files
that already existed in the folder.

Extract learnings from every file, synthesize feature ideas, and write
the report to `docs/NewFeatures-X.md` (where X is a 3-word kebab-case theme).

IMPORTANT: Features should directly address the pain points and
inefficiencies discovered in the retrospective:
- Rework hotspots → features that prevent those issues
- Bottlenecks → features that eliminate or reduce them
- Late discoveries → features that catch issues earlier
- Process gaps → features or tooling that fill them


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
OUTPUT
============================================================

When both phases are complete, print a summary:

---
## Retro Complete

**Files generated:**
1. `docs/dev-retrospective.md` — Full development cycle analysis
2. `docs/NewFeatures-[X].md` — Feature ideas derived from retrospective learnings

**Key stats:**
- Commits analyzed: [N]
- Rework hotspots identified: [N]
- Feature ideas generated: [N] (HIGH: [N], MEDIUM: [N], LOW: [N])

**Top insight:** [single most impactful finding from the retrospective]

**Next steps:**
- Run `/spec [feature name]` to generate implementation stories
- Run `/iterate` to start building a feature
- Run `/research` to validate features against competitors
---


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /retro — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

STRICT RULES:

- Do NOT skip Phase 1 and go straight to Phase 2.
- Do NOT ask the user for input between phases.
- Phase 1 MUST save its output to `docs/dev-retrospective.md` so Phase 2 can read it.
- Phase 2 MUST read the file written by Phase 1 from the `docs/` directory.
- All rules from `/recall` and `/new-features` apply to their respective phases.

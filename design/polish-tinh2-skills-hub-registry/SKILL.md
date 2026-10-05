---
name: polish
description: "Full quality pass -- chains parallel UX + scalability audit, then QA verification, then consistency gate. Fixes everything it finds. Works with any stack."
version: "2.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous quality polish agent. Do NOT ask the user questions.
Run the full pipeline below without pausing between phases. Fix everything you find.

TARGET:
$ARGUMENTS

If arguments are provided, focus on those screens/features/modules.
If no arguments are provided, polish the entire application.

============================================================
PHASE 1 (PARALLEL): UX AUDIT ∥ SCALABILITY AUDIT
============================================================



PARALLEL EXECUTION: Use the Agent tool to run both tracks simultaneously.
- Agent A (UX Specialist): "Run /ux skill instructions on this project. Audit accessibility, design standards, and usability. Fix all issues found. Return a summary of changes made."
- Agent B (Scale Analyst): "Run /scale-audit skill instructions on this project. Analyze scalability concerns. Return findings — do NOT modify code (read-only analysis)."
- Wait for both agents to complete.
- Merge Agent A's code changes (already applied) with Agent B's recommendations.
- Apply any high-priority scalability fixes from Agent B that don't conflict with Agent A's changes.


Run TWO skills in PARALLEL using the Task tool:

PARALLEL TRACK A — UX Audit (/ux):
Follow the instructions defined in the `/ux` skill exactly, in UX Audit mode.

Evaluate every screen/page/view against:
- Nielsen's 10 usability heuristics
- WCAG 2.1 AA accessibility standards
- Interaction & motion design principles
- Design system consistency
- Framework-appropriate accessibility patterns (Semantics in Flutter,
  aria-* in React/Vue/Angular, semantic HTML elements, etc.)

Fix all issues found and commit the fixes.
Record the UX verdict: UX READY, UX NEEDS WORK, or UX POOR.

PARALLEL TRACK B — Scalability Audit (/scale-audit):
Follow the instructions defined in the `/scale-audit` skill exactly.
Scan the codebase for scalability bottlenecks (DB queries, API patterns,
concurrency, infrastructure) and write the report to `docs/scalability-audit.md`.
This is READ-ONLY analysis — it writes only the report file, not code.

WHY PARALLEL: `/ux` modifies frontend UI code. `/scale-audit` only reads the
codebase and writes a single .md report. They touch completely different concerns
with zero file conflicts. Launch both as Task tool subagents and wait for both.

After both tracks complete, continue immediately to Phase 2.

============================================================
PHASE 2: QA VERIFICATION  (/qa)
============================================================

Follow the instructions defined in the `/qa` skill exactly.

Run all QA phases: Environment Setup → Backend/API Verification →
Code Review (adapted to the project's framework and language) →
Domain Consistency Analysis → Integration Verification → QA Report.

Fix all issues found and commit the fixes.

IMPORTANT: If the UX phase fixed issues, verify those fixes didn't
break any functionality. Pay special attention to components that
were modified in Phase 1A. Also factor in critical scalability findings
from Phase 1B — if the scale-audit identified CRITICAL issues, fix
them during this phase alongside QA fixes.

Do NOT stop here. Continue immediately to Phase 3.

============================================================
PHASE 3: CONSISTENCY GATE  (/audit)
============================================================

Follow the instructions defined in the `/audit` skill exactly.

Run the lightweight cross-layer consistency check as a final gate.

NOTE: `/qa` in Phase 2 already runs a full `/analyze` pass internally.
This Phase 3 is a lightweight verification that Phase 1 and Phase 2
fixes didn't introduce new cross-layer issues. A full `/analyze` here
would be redundant.


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

When all phases are complete, print a summary:

---
## Polish Complete

**Phase 1A — UX Audit:**
- Verdict: [UX READY / UX NEEDS WORK / UX POOR]
- Issues found: [N] | Fixed: [N]

**Phase 1B — Scalability Audit (ran in parallel with UX):**
- Scaling readiness score: [N]/10
- Critical issues: [N] | Fixed in Phase 2: [N]
- Report: `docs/scalability-audit.md`

**Phase 2 — QA Verification:**
- Endpoints tested: [N] | Screens/components audited: [N]
- Issues found: [N] | Fixed: [N]

**Phase 3 — Consistency Gate (/audit):**
- Verdict: [PASS / FAIL]
- Issues found: [N] | Fixed: [N]
- Final status: [CLEAN / ISSUES REMAIN]

**Overall quality verdict:** [SHIP IT / ALMOST THERE / NEEDS MORE WORK]

**Next steps:**
- Run `/e2e` or `/full-test` for automated test coverage
- Run `/manual-test-plan` for a pre-merge test checklist
- Ship it with `/iterate --fast` if new features are needed
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
### /polish — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

STRICT RULES:

- Phase 1 tracks MUST run in parallel via Task tool. Do not run them sequentially.
- Phase 2 and 3 run sequentially after Phase 1 completes.
- Fix issues as you find them — do not just report.
- Phase 3 is the final gate. If it finds issues, fix them.
- All rules from `/ux`, `/scale-audit`, `/qa`, and `/audit` apply to their respective phases.

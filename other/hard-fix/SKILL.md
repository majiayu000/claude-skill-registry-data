---
name: hard-fix
description: Escalation workflow for stubborn bugs. Use when a bug persists after multiple fix attempts, you've tried several approaches, or you're stuck.
argument-hint: <description of the persistent problem>
effort: max
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Hard Fix

Comprehensive investigation workflow for bugs that resist normal debugging.

## Usage

```
/hard-fix login keeps failing after auth changes
/hard-fix race condition in checkout - tried 3 fixes already
/hard-fix                              # Uses recent conversation context
```

**Do NOT shortcut this workflow:**
- "I think I already know the fix" -- If you knew, you wouldn't need this skill
- "Let me just try one more thing first" -- You've already tried. Follow the systematic process
- "I only need one of these investigation methods" -- Parallel investigation is the point, run ALL agents

**Circuit Breaker Rule:**
If 3 sequential fix attempts have failed for the same issue:
1. STOP attempting more fixes
2. Document what was tried and why each failed
3. This signals a systemic/architectural issue, not a localized bug
4. Recommend architectural review rather than continuing to patch

## Gotchas
- Phase 0 doc search uses `2>/dev/null` on `docs/log/` — if the directory doesn't exist, the search silently returns nothing and gives false confidence there are no prior known issues.
- Phase 7 logging requires user confirmation that the fix works. If the session ends before confirmation, no log is written and the institutional knowledge loop breaks.

## Workflow

### Phase 0: Pre-Check Internal Documentation

Before full investigation, check internal docs for known issues and gotchas:

**Check past issues:**
```bash
grep -ri "<keywords>" docs/log/ 2>/dev/null | head -10
ls -la docs/log/ 2>/dev/null | grep -i "<related_terms>"
```

**Check project documentation:**
```bash
grep -ri "<keywords>" docs/ *.md 2>/dev/null | head -10
```

Look for documented gotchas, known issues, or patterns related to the problem area.

**If a matching past issue is found:**
1. Read the full log file
2. Present the previous solution to the user
3. Ask: "We encountered this before. Should I apply the previous solution, or run a fresh investigation?"

**If relevant documentation is found:**
1. Read the relevant sections
2. Check if documented patterns/gotchas apply to this issue

If no match or user wants fresh investigation, continue.

### Phase 1: Gather Context

Ask clarifying questions if needed:
- What behavior are you seeing vs. expecting?
- What fixes have already been tried?
- When did this start happening? (recent change, always broken, etc.)
- Are there error messages or logs?

Keep questions minimal - only ask what's essential.

### Phase 2: Parallel Investigation

Launch ALL of these simultaneously using the Task tool:

| Agent | Skill/Tool | Focus |
|-------|------------|-------|
| **Research** | `research-tech` | External solutions, known issues, library bugs |
| **Debug** | `debug-log` | Add logging to trace the actual execution path |
| **History** | `review-history` | Git blame, recent changes, past issue logs |
| **Library Source** | Read library code | Undocumented behavior, actual implementation |
| **Opinion 1** | `second-opinion` | Fresh perspective on the problem |

For detailed agent prompt templates, see `references/templates.md`.

### Phase 3: Synthesize Findings (Opus)

Wait for all Phase 2 agents. This synthesis is the reasoning crux of the whole workflow, so it runs in a fresh subagent pinned to Opus rather than inline: dispatch **one** read-only subagent to produce the root-cause theory.

- `subagent_type: Plan` — read-only by construction (no Edit/Write/NotebookEdit), retains Read/Grep/Glob for confirming evidence against real files.
- `model: opus`.

The `Plan` agent starts **fresh** (not a fork), so its prompt MUST contain:
- The problem statement and everything Phase 1 established.
- The **full findings from all five Phase 2 agents** (research, debug-log traces, git history, library source, second-opinion) — paste them in; the subagent cannot see your context.
- Pointers to the specific files / line ranges the theory will hinge on.
- These directives: trace to **mechanism, not symptom**; ground every claim in specific evidence from the findings or the files it reads; name the single most-likely root cause and rank the alternatives; state what evidence would confirm or falsify each; reason exhaustively before committing.

It returns a root-cause theory with corroborating evidence from multiple sources (debug timing, git history, library source, research). See `references/templates.md` for BAD/GOOD synthesis examples — hold its output to the GOOD bar.

### Phase 4: Validate Theory

Run `second-opinion` with your synthesis and proposed fix. Check for blind spots.

### Phase 5: Present to User

For the presentation template, see `references/templates.md`.

Ask: "Should I proceed with the recommended fix?"

### Phase 6: Implement and Verify

1. Implement the recommended fix
2. **Keep all debug logging in place** — do NOT remove debug logs added during investigation
3. Ask user to test/verify
4. **Wait for user confirmation** that the fix worked
5. Only after user confirms the fix works, remove the debug logging added in Phase 2

**Do NOT remove debug logs until user confirms the fix is working.** If the fix fails, the logs are essential for the next investigation round. **Do NOT proceed to Phase 7 until user confirms the fix is working.**

### Phase 7: Log for Future Reference (after user confirms fix)

**Only after user confirms fix works**, write to `docs/log/YYYY-MM-DD-{Issue}.md`.

For the log template, see `references/templates.md`.

## Examples

**Token refresh bug after multiple failed fix attempts:**
> /hard-fix auth token refresh fails silently after 3 fix attempts

Launches parallel agents: research finds a known axios issue with token queuing, debug-log traces the refresh timing, history reveals the bug started after PR #234 moved refresh to background, and library source confirms axios doesn't queue requests during refresh. Synthesizes a root cause (race condition) with a concrete fix using axios-auth-refresh.

**Race condition traced to library update via git history:**
> /hard-fix race condition in order processing since last deploy

History agent pinpoints a dependency bump that changed default concurrency behavior. Debug logging captures the interleaved execution order, and library source inspection confirms the breaking change in the new version. Presents the version diff and a targeted fix to restore the previous behavior.

## Troubleshooting

### Parallel investigation agents do not converge on root cause
**Solution:** Run `second-opinion` with a consolidated summary of all agent findings and the conflicting theories. If agents still disagree, prioritize the evidence from the debug-log agent (actual runtime behavior) over static analysis, and test the most likely theory first.

### Root cause is in a third-party dependency
**Solution:** Pin the dependency to the last known working version as an immediate fix, then file an issue upstream with reproduction steps. If a patch is needed sooner, fork the dependency or apply a local patch using `patch-package` (JS) or the equivalent for your ecosystem.

## Notes

- This is a heavyweight process - use for genuinely stuck problems
- The parallel investigation is key - each source provides different insights
- Only log confirmed fixes - don't log until user verifies it works
- Past issue logs are gold - check them first

---
name: running-subagent-reviews
description: Use when the user asks for subagent review, fresh-context review, multiple review rounds or passes, several reviewer agents, or exhausting critical surfaces before a PR, merge, implementation, or plan handoff.
---

# Running Subagent Reviews

## Overview

Run calibrated fresh-context reviewer passes, then reconcile the findings into concrete fixes or explicit non-blocking risks. A subagent review is not a single broad "looks good" check; it is a set of independent, lens-specific reviews over raw artifacts.

## Workflow

1. Identify the artifact under review: design/spec/plan, implementation diff, PR, fix diff, writing draft, or release/rollout checklist.
2. Gather raw artifacts reviewers can inspect without chat history:
   - requirements, plan, or spec text
   - file paths or git range (`BASE_SHA..HEAD_SHA`) when code exists
   - diff stat and relevant full diff
   - verification already run, with command names and result summaries
   - known constraints, target branch, rollout requirements, and explicit user concerns
3. Choose distinct review lenses. Do not send multiple reviewers the same vague prompt.
4. Spawn the requested number of reviewers. If the user did not specify a count, use 2 reviewers for narrow work and 3-4 for broad cross-surface work.
5. Reconcile findings yourself:
   - Fix valid Critical issues before proceeding.
   - Fix valid Important issues unless there is a concrete reason to defer.
   - Treat Minor issues as optional notes.
   - Push back on incorrect findings with code, requirements, or test evidence.
6. Re-run relevant verification after fixes.
7. Run a follow-up review only on materially changed risk areas or the fix diff. Do not run identical rounds over unchanged artifacts unless the user explicitly asked for them.
8. Stop when the requested lenses are covered and no valid Critical or Important issues remain, or when unresolved items are explicitly called out as residual risk.

## Lens Selection

For design or implementation plans:
- architecture and sequencing
- data model, migrations, permissions, and compatibility
- API/runtime contracts and cross-repo drift
- verification, rollout, and operational recovery

For implementation diffs before PR:
- product and requirements correctness
- production risk: auth, security, data integrity, migrations, rollback, observability
- architecture, maintainability, concurrency, and performance
- tests and verification quality

For docs, specs, or writing:
- factual correctness and missing assumptions
- structure, audience fit, and actionability
- risky overclaims, stale references, and unclear acceptance criteria

## Reviewer Prompt

Use this shape. Fill it with raw artifacts; do not pass your conclusions as ground truth.

```text
You are a fresh-context senior reviewer. Do not rely on chat history.
Review only the artifacts below.

Goal:
Find concrete issues before {PR|implementation|handoff}. Prefer high-signal findings over broad commentary.

Artifacts:
- Requirements / plan / spec:
  {PLAN_OR_REQUIREMENTS}
- Git range or files:
  {BASE_SHA}..{HEAD_SHA} or {FILE_PATHS}
- Diff stat / full diff when applicable:
  {DIFF_STAT}
  {DIFF}
- Verification already run:
  {COMMANDS_AND_RESULTS}
- Constraints and known concerns:
  {CONSTRAINTS}

Review lens:
{FOCUSED_LENS}

Check:
- Does the artifact satisfy the requirements?
- What can break in this lens?
- Are edge cases, compatibility, rollout, and tests adequate?
- Are there missing steps or over-scoped assumptions?

Severity:
- Critical: must fix before proceeding; broken behavior, data loss, security, unsafe migration, serious production regression.
- Important: should fix before proceeding; missed requirement, meaningful correctness gap, fragile integration, poor error handling, real test gap.
- Minor: optional cleanup, style, docs polish, small maintainability note.

Output:
### Verdict
Ready | Ready with minor notes | Blocked

### Findings
For each finding:
- Severity
- File:line or section reference
- Issue
- Why it matters
- Suggested fix

### Non-blocking Notes
Only if useful.

Do not invent issues. If you cannot point to code, requirements, or a concrete missing verification step, say so.
```

For a follow-up round after fixes, narrow the prompt:

```text
Review the fixes made after prior subagent review.

Artifacts:
- Prior validated Critical/Important findings:
  {VALIDATED_FINDINGS}
- Fix diff:
  {FIX_DIFF}
- Updated verification:
  {COMMANDS_AND_RESULTS}

Task:
Confirm whether the fixes address the validated findings and whether the changed areas introduce new Critical or Important risk. Stay scoped to the fix diff unless you find evidence that the fix invalidates a wider surface.
```

## Final Report

Report the result, not every subagent transcript:

```text
Ran {N} fresh-context subagent review passes over {artifact/range}: {lenses}.

Results:
- Critical: {count}; {fixed/none/open with reason}
- Important: {count}; {fixed/deferred with reason}
- Minor: {count}; {noted/not blocking}

Verification after fixes:
- {command}: {pass/fail}

Follow-up review:
- {none needed | fix-diff review found no remaining Critical/Important issues | remaining issue}

Status: {ready for PR/ready for implementation/blocked}
Residual risk: {short concrete note}
```

## Common Mistakes

- Running one broad reviewer when the user asked for rounds.
- Passing the whole conversation instead of raw artifacts.
- Asking reviewers to "make sure it looks okay" instead of assigning a lens.
- Treating every reviewer claim as valid without checking it.
- Fixing issues without rerunning relevant verification.
- Re-reviewing the entire unchanged artifact repeatedly when only a focused fix diff changed.
- Omitting residual risk when a valid issue is deferred.

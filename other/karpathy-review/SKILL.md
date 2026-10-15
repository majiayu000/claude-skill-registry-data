---
name: karpathy-review
description: Review a coding plan or diff against four Karpathy-inspired principles — Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution. Use BEFORE non-trivial code edits to validate the plan, and AFTER edits to validate the diff. Catches hidden assumptions, overengineering, drive-by changes, and missing verification.
disable-model-invocation: false
---

# karpathy-review — Behavioral Governor

> Adapted from forrestchang/andrej-karpathy-skills, distilled from Karpathy's observations about common LLM coding failure modes. Sits ABOVE skill-specific work as a behavioral check, not as a tool.

## When to use

- Before non-trivial code edits — review the plan's assumptions and simplicity
- After non-trivial code edits — review the diff's surgical-ness and verification
- When the operator says "this seems over-engineered" or "this changed more than I expected"
- Inside `/ship`, `/fix-root`, `/review` as a mandatory gate (see Quality gates below)

## When NOT to use

- Trivial edits (typo fix, one-line docs change, whitespace) — overhead exceeds value
- Pure research / exploration — no code being shipped
- During brainstorming — premature constraint
- For commit-message review — different concern

## Inputs

- (For pre-edit review) The plan: files to change, abstractions to introduce, success criteria
- (For post-edit review) The diff: `git diff` or `git diff --staged`, plus the original task description
- (Optional) The user's exact request, verbatim — to compare against the diff

## Outputs

A structured report:

```
## Karpathy Review

### 1. Think Before Coding
- Hidden assumptions: <list, or "none surfaced">
- Ambiguity in the request: <list interpretations, or "request is clear">
- Should we ask before proceeding: yes/no, with reason
- Simpler approach available: yes/no, with sketch

### 2. Simplicity First
- Smallest viable solution to satisfy the goal: <one sentence>
- Speculative features / abstractions / config introduced: <list, or "none">
- Could this be N lines instead of M lines: <ratio, with reasoning>
- Building for hypothetical future requirements: yes/no

### 3. Surgical Changes
- Files that should change vs. files actually changed: <comparison>
- Lines that don't trace to the user's request: <list with file:line>
- Drive-by refactors / formatting / comment edits: <list>
- Pre-existing dead code removed (was it asked for?): <list>

### 4. Goal-Driven Execution
- Stated success criterion: <one sentence>
- Verification method: test command / manual flow / inspection
- Verification status: <ran / pending / blocked because X>

### Recommendation
PROCEED | SIMPLIFY | ASK | STOP
- If SIMPLIFY: which subset of the diff is actually needed
- If ASK: which specific question to ask the operator
- If STOP: which root cause to address before resuming
```

## Hard rules

1. **MUST be terse.** A long Karpathy review defeats its own principle. Aim for under 30 lines of report.
2. **MUST surface hidden assumptions** even when the operator didn't ask. The whole point.
3. **MUST recommend exactly one verdict** (PROCEED, SIMPLIFY, ASK, or STOP). No menus.
4. **MUST NOT add new abstractions** — this skill REVIEWS, it doesn't BUILD.
5. **MUST NOT pile on** when the diff is genuinely surgical. "Looks good" is a valid output.
6. **MUST NOT slow trivial work.** If the operator runs this on a typo fix, return "out of scope, skip" — don't invent findings.

## The four principles in detail

### 1. Think Before Coding

> "State assumptions. Surface ambiguity. Push back when a simpler or safer path exists. Stop when confused."

Common LLM failure: silently choosing one of multiple reasonable interpretations of a task and shipping it.

Detection signals:
- The task description has a verb that admits multiple objects ("update the user flow" — which flow?)
- The task assumes a system the LLM hasn't actually inspected ("fix the bug" — which bug?)
- The task uses values that need confirmation ("make it 3 retries" — were 3 retries derived from data?)

Right move: ask ONE sharp question or state assumptions and pick the safest minimal path explicitly.

### 2. Simplicity First

> "Implement the smallest solution that satisfies the goal. No speculative features, abstractions, config, or flexibility."

Common LLM failure: building a 200-line framework when a 20-line function would do; adding configurability for needs that don't exist; pre-optimising for scale the project doesn't have.

Detection signals:
- New abstractions (Strategy class, factory, registry) used by exactly one caller
- Config flags that have one value
- Dependency injection where direct calls would suffice
- Multi-paragraph docstrings on one-line functions

Right move: rewrite to the smallest version. Comment why if non-obvious.

### 3. Surgical Changes

> "Touch only files and lines needed for the task. No drive-by refactors. Every changed line must trace to the user's request."

Common LLM failure: solving the asked problem AND fixing adjacent code, formatting, comments, or APIs that weren't asked about.

Detection signals:
- Diff touches files unrelated to the stated task
- Whitespace / quote-style / import-order changes mixed into a behaviour change
- Function signatures changed when the body could have been changed alone
- "While I was here, I also..." in commit messages

Right move: split the diff. Land the surgical change. Open a separate, explicit PR for the cleanup if it's worth doing.

### 4. Goal-Driven Execution

> "Convert tasks into success criteria. Define verification before implementation. Loop until the goal is verified or explain why verification is blocked."

Common LLM failure: finishing implementation without running tests; claiming "done" based on the diff looking right; not knowing how to verify.

Detection signals:
- No success criterion stated upfront
- No test or manual flow listed in the plan
- "Should work" in the summary instead of "ran X, got Y"
- Verification deferred to the operator without explanation

Right move: state the success criterion before coding. Run verification. If blocked, state why explicitly.

## Quality gates (where this skill plugs in)

| Workflow | When to run karpathy-review |
|----------|------------------------------|
| `/ship` | After plan, before edits (Think + Simplicity) AND after edits (Surgical + Goal-driven) |
| `/fix-root` | After diagnosis, before patch (Think); after patch, before claiming fixed (Goal-driven) |
| `/review` | On every diff (all four principles) |
| `/audit-deep` | Mostly skip — the audit IS the review; running this would be recursive |
| `/level-up` | Skip — recommendations not yet code |
| `/test-gen` | After tests written (Simplicity — are tests over-mocking? Are tests testing the spec?) |
| `/refactor*` | Mandatory before AND after (refactors are the highest-risk for non-surgical drift) |

## Failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Review says "looks good" but operator finds issues | Review was lazy or context was incomplete | Re-run with explicit `--strict` flag (verbal in prompt); pass the user's verbatim request |
| Review flags everything as a problem | Skill is being run on trivial edits | Skip — return "out of scope" |
| Review keeps recommending SIMPLIFY but operator built it that way for real reasons | Skill missed context (constraints, future plans) | Operator should override and document why; update `decisions/log.md` so future reviews see the context |
| Skill becomes a slowdown rather than a check | Run too eagerly on every change | Use the quality-gates table — only run for non-trivial changes |

## Reference files

- `references/karpathy-principles.md` — full distillation of the four principles
- `CLAUDE.md § Karpathy Operating Constraints` — short-form rules
- `references/3ms-framework.md` — operator mindset (compatible: Three Ms is "how you think before tools," Karpathy is "how AI codes once invoked")
- `commands/review.md` — invokes this skill on diffs

## Improvement loop

After every Karpathy review:
1. Did the operator override the verdict? If yes, log why — recurring overrides mean the principle's rubric is wrong for this context.
2. Did issues this skill flagged turn out to be real? If consistently no, tune the detection signals.
3. Did issues this skill missed surface later? If yes, add the missed pattern to the relevant principle's "Detection signals" list.

## Attribution

Principles distilled from forrestchang/andrej-karpathy-skills, which is itself derived from Andrej Karpathy's observations about common LLM coding failure modes. This skill is an integration into this repo's quality-gate model — not a vendoring of the upstream content.

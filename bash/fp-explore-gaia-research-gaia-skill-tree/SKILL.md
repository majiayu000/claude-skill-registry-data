---
name: fp-explore
description: >-
  Phase 1 of the feature-pipeline suite — stress-test a CLI command, feature,
  flag, or module as a developer seeing it for the first time, then file GitHub
  issues for every distinct finding. Use when someone says "explore X", "test
  X", "find issues with X", "what's wrong with X", or after /feature-pipeline
  init. Also triggers standalone as /fp-explore <feature> when you want just
  the exploration phase without the full pipeline. Reads the target feature from
  .fp-state.json (or the argument if provided). Completes in one bounded turn
  and prints the M1 stop hook so the user decides whether to continue to
  /fp-plan.
version: 3.0.0
argument-hint: "[<feature>]"
---

# fp-explore  (Phase 1 — Feature Exploration)

Explore `{{feature}}` like a developer encountering it for the first time.
Invoke it in five or more distinct ways, note every footgun or gap, file one
GitHub issue per finding, write the issue numbers into state, then print the
M1 stop hook and end your turn.

The single-turn constraint exists so the user can review findings before any
code changes happen. Don't bleed into Phase 2.

## Setup

Resolve the target feature — the argument takes precedence over state:

```bash
# If no argument was given, read from state:
feature=$(.agents/skills/feature-pipeline/scripts/state.sh get feature)
# If state is also missing, ask: "Which feature should I explore?"
```

If `.fp-state.json` doesn't exist yet, initialise it first:

```bash
.agents/skills/feature-pipeline/scripts/state.sh init "<feature>"
```

## Exploration

Run `{{feature}}` in **five or more** distinct ways. Cover these axes — they
exist because bugs tend to cluster at the boundary between what authors tested
and what users actually do:

| Axis | Example |
|------|---------|
| Happy path | normal use with valid inputs |
| Edge case | empty input, missing file, zero results |
| Invalid input | bad flag name, wrong type, out-of-range value |
| Flag combination | two or more flags together |
| Composed output | pipe to `jq`, `head`, `wc -l`, etc. |

For each issue found, capture before filing:
- One-line title
- Exact reproduction commands
- Expected vs actual behaviour
- Severity: `low` / `medium` / `high`

Cap findings at 8. If you find more, keep the highest-severity ones — a short
list of real problems is more actionable than a long list of noise.

## Filing issues

File one `gh` issue per distinct finding. Use `gh` directly (not GitHub MCP)
because it's faster in a tight loop:

```bash
gh issue create \
  --title "[{{feature}}] <short description>" \
  --label "exploration,needs-triage" \
  --body "## Steps to reproduce
<commands>

## Expected
<what should happen>

## Actual
<what happens>

## Severity
<low | medium | high>"
```

Push each issue number to state immediately after creation — don't batch at
the end. If this turn is interrupted, the partial list is still recoverable:

```bash
.agents/skills/feature-pipeline/scripts/state.sh push issueNumbers <N>
```

## Phase completion

Print a severity table of all issues filed:

```
| Issue # | Title | Severity |
|---------|-------|----------|
| #N      | …     | high     |
```

Advance state to Phase 2:

```bash
.agents/skills/feature-pipeline/scripts/state.sh set phase 2
```

Print the M1 stop hook and end your turn. The stop hook is mandatory — it's
the gate that lets the user review findings before any implementation starts:

```
╔══ STOP HOOK M1 ══════════════════════════════════════════════════════════════╗
║  Phase 1 complete — <N> issues filed for {{feature}}                         ║
║  Review above, then run /fp-plan to continue.                                ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Constraints

- File issues via `gh` CLI, not GitHub MCP tools — the script loop is faster.
- Push issueNumbers to state after each issue, not in a batch.
- Stop at 8 issues. Don't keep exploring once you hit the cap.
- End the turn after the stop hook. Phase 2 belongs to /fp-plan.

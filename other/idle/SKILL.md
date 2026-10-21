---
name: idle
description: The idle work loop - enumerate open issues and triage rows, classify fixable vs blocked, pick by value-vs-budget, dispatch. Standing user directive; invoke whenever otherwise idle.
---

# Idle Work Loop

Standing directive: there is no "waiting" state. Between lane completions, after a release, after a merge train drains — pick the next item and work it. New problems found along the way become issues at identification time, keeping the queue self-replenishing.

## 1. Enumerate

```bash
powershell.exe -Command 'gh issue list -R jamie8johnson/cqs --state open --limit 50 --json number,title,labels'
grep -c '| open |' docs/audit-triage.md   # plus the rows themselves if any
```

## 2. Classify

- **Blocked-external** (upstream PRs, dependency releases, missing hardware, user-parked) — skip. Known standing members: cuvs upstream chain, ort RC, anything needing a Mac or native Windows.
- **Umbrella/design** — only enter with explicit scoping; closing umbrellas orphans phases.
- **Fixable** — everything else. Note effort (easy / medium / hard) and value.

## 3. Pick

Judgment call, biased by: user-stated priorities first; then highest-value-per-token. Mind the rate window — heavy lanes (schema work, parser work, large refactors) want ~25%+ of a 5-hour window remaining; near a reset, prefer trivial sweeps or solo-fixable items. If the issue list is dry, run /archeo to refill it, or check docs freshness (/docs-review if a week stale).

## 4. Dispatch

- Implementation → **lane-implementer** agent (opus), one branch per coherent batch; worktree isolation.
- Risky lanes (live scoring path, schema migrations, cross-surface signatures) → fable code-reviewer pass before landing.
- Security-adjacent → opus for the analysis lane.
- Land via **/land**; close linked issues on merge (verify, don't assume).

## 5. Loop

On lane completion: land it, file its residuals, return to step 1. Update tears when the board changes shape.

---
name: crab
description: Mandatory multi-agent turn execution protocol -- CRAWL/Check, Reason, Act, Bus. Run before any consequential turn in a shared-state environment. [Maps to CO13.]
version: 0.1.0
execution-mode: side_effecting
argument-hint: "[--lane <full-lane>] [--skip-bus] (Workstation local-only exception)"
category: dev-tools
status: candidate
---

## Context Gathering

### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus **before** any stateful action (satisfies Krineia Invariant 5):
```
Type: SKILL_INVOKE
To: all
Message: [skill=crab] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

Before executing, gather live state. On Windows (PowerShell):
```powershell
pwd
git status --short --branch
git stash list
python $HOME\bin\bus-global.py status
python $HOME\bin\bus-global.py tail 5
```
On Unix (bash/zsh):
```bash
pwd
git status --short --branch
git stash list
python ~/bin/bus-global.py status
python ~/bin/bus-global.py tail 5
```
If a command errors, report "(<surface> unavailable)" rather than aborting the whole turn.

# CRAB Protocol

**CRAWL / Check → Reason → Act → Bus** — the mandatory 4-step execution trace for every
consequential agent turn in a multi-session environment. Keeps agents synchronized without
human copy-paste of context between sessions.

`Check` is the short form. `CRAWL` is the expanded check method: **C**ontext, **R**epo,
**A**gents, **W**ire, **L**imits.

**Canonical sources of truth** (do not duplicate here):
- Base protocol: `.agents/rules/crab-protocol.md`
- Workstation local-only exception: `.agents/rules/crab-protocol-workstation.md`
- Full playbook: `hummbl-governance/hummbl_governance/playbooks/CRAB.md`

## When to Use

- Before ANY consequential turn that touches shared state (repo, bus, ledger, guardrails,
  skills, memory, CI, PR, issue, queue, cross-machine surface).
- At the start of a multi-agent session, or when resuming after a handoff.
- Before cross-branch git operations, commits, pushes, PRs, deploys, or daemon installs.
- When the operator says "CRAB", "run CRAB", "do the check", or invokes `/crab`.

## When to Skip

- Trivial read-only lookups with no shared-state dependency.
- Pure conversational answers that change no state.
- The documented Workstation local-only exception (all 5 conditions in
  `crab-protocol-workstation.md` are true) — and even then, when in doubt, post anyway.

## Execution

### Step 1 — CRAWL / CHECK
Run the Context Gathering commands above. Answer the five minimum live-state questions:
- **Context**: What did the operator/requester ask, and did a recent handoff or bus post
  change the starting point?
- **Repo**: Which checkout is authoritative; what branch, dirty state, stash, lock, PR, or
  CI state can invalidate the work?
- **Agents**: Which humans, agents, sessions, lanes, or daemons are active, blocked, or
  likely to own dirty state? On a single host with multiple same-identity sessions
  (e.g., 4+ devin on agent-node), check the session registry:
  `python ~/.agents/scripts/session-registry.py list` for precise session IDs,
  CWDs, branches, and lanes. The bus `from=devin` cannot distinguish them.
- **Wire**: Is the canonical coordination surface current (bus, PR thread, issue, queue,
  deploy channel, monitor)?
- **Limits**: What approval, protected-surface, data-tier, credential, or
  irreversible-action boundary applies?

**Stop before Act when** (stop conditions):
- A bus `BLOCKED` affects your scope.
- An unresolved `PROPOSAL`, `HANDOFF`, `REVIEW`, or lane claim affects your scope.
- Stash/dirty state would collide with a cross-branch or shared-state operation.
- The current state cannot be verified cheaply and the assumption is risky.
- You would need to modify another agent's guardrail file.

On agent-node, `~` is normally a launch directory, not the repo — pivot to the
actual target repo before reporting branch or stash state. Do not read or write retired
local TSV mirrors; use `bus-global.py` (`tail 5`, not `tail -n 5`).

### Step 2 — REASON
Internal synthesis (not a bus action):
- Does live state change what you should do?
- Is the requested action authorized by the operator, local guardrails, and
  protected-surface rules?
- Is the action reversible? If not, state the risk before acting.
- Does this require non-author review or a bus lane claim before work starts?
- What message type will you post after Act?
- **Verify-before-claim**: any status claim about human activity (HRSI logged, InMails
  sent, tasks completed) MUST be verified from source data (ledger, git log, CRM), not
  inherited from prior session handoffs.

### Step 3 — ACT
Do only the scoped work. Preserve unrelated dirty or untracked state. Verify at a level
proportional to risk. If blocked or unsafe, post `BLOCKED` with evidence and stop — do not
attempt workarounds. For meaningful shared work, post a lane claim (`WIP_START`, `ACK`, or
`PROPOSAL`) before the main Act step.

### Step 4 — BUS (before responding to the human)
Post the receipt to the canonical bus BEFORE the final human-facing response:
```powershell
python $HOME\bin\bus-global.py post <from_id> all <TYPE> "<message>"
```
```bash
python ~/bin/bus-global.py post <from_id> all <TYPE> "<message>"
```
Identity discipline: canonical base identity only (`claude-code`, `codex`, `gemini`,
`devin`, `opencode`, `sov`, `echo`, `soma`). No parentheticals. On agent-node, Codex MUST use
the identity-hardcoded `codex-bus` wrapper for writes, not `bus-global.py post` with a
hand-typed sender.

**Lane closure**: `WIP_END` is the only valid closer for a `WIP_START` lane — `STATUS`,
`SITREP`, `MILESTONE`, `RECEIPT`, `COMPLETE`, and `HANDOFF` do NOT close a lane even when
they report work as finished. If you opened or inherited a lane this turn, run:
```bash
python "$HOME/.agents/scripts/check-orphaned-wips.py" --sender <your-canonical-identity> --lane <full-lane> --quiet
```
Non-zero exit means the lane is still open — post `WIP_END` (or `HANDOFF` + `WIP_END` with
`outcome=transferred` if handing off). Do not let a lane go silent with only a `WIP_START`.

## Final Snapshot Required

Before any `TASK_COMPLETE`, `WIP_END`, `COMPLETE`, `MILESTONE`, `REVIEW`, or final
response that summarizes consequential work, capture a FRESH snapshot from the
authoritative checkout — do not reuse earlier loop variables, memory, or a prior bus post:
```bash
git status -sb
git status --short --untracked-files=all
git stash list
git rev-parse --short HEAD
git rev-parse --abbrev-ref --symbolic-full-name '@{u}'
git rev-list --left-right --count <base>...HEAD
```
If the branch has no upstream, say `upstream=none` — do not treat the failure as evidence
of alignment. Name `base=` explicitly.

## Standard Bus Receipt Schema

Closeout and material `STATUS` messages SHOULD use stable `key=value` fields:
```text
repo=<name> branch=<branch> head=<short_sha> base=<base_ref>
upstream=<upstream_ref|none> ahead=<n|unknown> behind=<n|unknown>
dirty_total=<n> tracked_changed=<n> staged=<n> untracked=<n> stash=<n>
worktrees=<n|na> bus_readback=<ok|failed|skipped> proof_source=<commands>
next_owner=<operator|codex|agent|none>
```

Cross-surface fields (SHOULD when work spans multiple PROJECTS/apex-nexus surfaces):
```text
projects=<comma-list> surfaces=<comma-list>
```

- `WIP_START`: include `repo=`, `branch=`, `head=`, `dirty_total=`, `stash=`, `scope=`, `next_owner=`, and `projects=` / `surfaces=` when applicable.
- `STATUS`: only fields that changed, plus `proof_source=` for evidence claims.
- `SITREP`: full current snapshot.
- `TASK_COMPLETE` / `WIP_END`: final snapshot fields + verification performed + `next_owner=`.
- `BLOCKED`: `blocked_by=`, `evidence=`, `next_owner=`, + last verified repo/bus state.

## Message Types

`STATUS` · `RECEIPT` · `ACK` · `SITREP` · `COMPLETE` · `MILESTONE` · `QUESTION` · `BLOCKED` ·
`PROPOSAL` · `WIP_START` · `WIP_END` · `TASK_COMPLETE` · `HEARTBEAT` · `REVIEW` · `HANDOFF` ·
`VETO` · `DECISION`

`DECISION` and `DIRECTIVE` are restricted by agent guardrail. Codex must not post either.
`PROPOSAL` requires ACK before self-executing unless the operator already approved the work
in chat — then the operator instruction is authority and the bus `STATUS` is the receipt.

## Workstation Local-Only Exception

The Bus step MAY be skipped ONLY when ALL five conditions in
`crab-protocol-workstation.md` hold: (1) no shared/repo-tracked surface changes; (2) no
branch/stash/PR/issue/CI/queue/ledger/memory/automation state changes; (3) no
cross-machine action; (4) no other agent depends on knowing; (5) no state visible to
anyone else changes. If you skipped Bus and later discover the work did affect shared
state, post a late `STATUS` acknowledging the gap — do not pretend it didn't happen.
**When in doubt: post anyway.** False positives are cheap; a missing audit-trail entry is not.

## Output Format

```
CRAB | <date> <time UTC> | <repo> | <branch>
════════════════════════════════════════════
CHECK  : git=<clean|dirty n> stash=<n> bus=<fresh|stale|unavail> blockers=<none|...>
REASON : <one line — does live state change the plan? authorization? reversibility?>
ACT    : <one line — what was done, or BLOCKED posted>
BUS    : <type posted, or "skipped — Workstation local-only exception (conditions 1-5)">
SNAP   : head=<sha> upstream=<ref|none> ahead=<n> behind=<n> dirty=<n> stash=<n>
NEXT   : <concrete next step or next_owner>
```

## Base120 Context

- Primary: **CO13** (Multi-Agent Coordination / Turn Execution Discipline)
- Related: **IN6** (Evidence Verification — verify-before-claim), **SY13** (Incentive Design — lane closure discipline)

## Skill Chains
- For check for active opencode delegations during CRAB protocol turns -> `[cross-runtime-bridge]` (`sessions`)

### Mandatory
- None — CRAB is the turn wrapper. It IS the precondition for safe consequential work.

### Advisory
- Before CRAB: `[start-session]` (session open), `[nexus]` (canonical-surface scan)
- After CRAB (if blocked): `[handoff]`, `[sitrep]`
- Bookend: CRAB at turn start; `[end-session]` at session close

## Authority

- **T1 (TRUSTED)**: May run without restriction
- **T2 (Active/High)**: May run without restriction
- **T3 (Medium)**: May run without restriction (turn discipline — all agents need it)
- **T4 (Probationary)**: May run; Bus post restricted to `STATUS` type only (no `DECISION`/`PROPOSAL`)
- **Operator**: Override any restriction

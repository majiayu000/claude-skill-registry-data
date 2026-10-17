---
name: failure-simulator
description: "Failure simulator on code level: inventories every external touchpoint (HTTP clients, DB access, filesystem, queues, caches) with its surrounding error handling, then for a chosen failure scenario (DB down, API timeouts, disk full) mentally executes the failure path at each touchpoint and reports the resulting behavior - retry, degradation, crash or silent loss - plus inconsistencies and hardening recommendations. Pure thought experiment, nothing is ever shut down. Read-only. Trigger: /failsim"
trigger: /failsim
---

## What this is for

"What happens when the DB goes away?" - the honest answer in almost every team: nobody knows. Error handling grows scattered and inconsistent; whether a timeout leads to retry, crash, silent data loss, or hanging request depends on the individual code site, not architecture. Chaos engineering answers this empirically but is expensive and risky. An LLM can run the thought experiment systematically: find every external touchpoint and think through the failure path - failure simulation on code level, without anything actually failing.

**Audience:** Senior
- On-call engineers know what will happen before it happens.
- Architecture reviews use it for resilience design.
- SLO discussions get concrete failure-path evidence.

### Trigger: `/failsim`


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1 - `-help`/`-h` check
Print usage block and stop.

### Step 2 - Determine project path + scenario
Ask for `-ProjectDir` + failure scenario (free text; without scenario: show inventory and suggest scenarios from found touchpoint types).

### Step 3 - Run collector
```powershell
& .\scripts\failpoint-scan.ps1 -ProjectDir "<path>"
```

### Step 4 - LLM simulation
1. **Sharpen scenario**: free text → affected failpoint types + failure mode (unreachable / slow / error responses / partial).
2. **Per affected failpoint, think through the path** (read file, trace up the call chain to system boundary - route/handler/job):
   - What does the site throw in failure mode? Where does the exception land?
   - Classify resulting behavior: `robust` (retry/fallback/clean error response) / `degraded` (function gone but controlled) / `silent` (error swallowed - data loss/inconsistency candidate) / `crash` (unhandled to top-level) / `hang` (no timeout signal - request/job blocked).
   - Confidence: `confirmed` (path fully traced), `probable` (framework default assumed, name which).
3. **Cross-cutting findings**: inconsistent behavior at similar points; missing timeouts as a class; silent points collectively.
4. **Report**: summary → behavior table → cross-cutting findings → hardening recommendations → open questions.

### Step 5 - Produce report
Write `failsim-report-<scenario>.md`:

```
# Failure Simulation Report - <project> - <scenario>

## Summary
- <N> touchpoints affected, behavior distribution
- <H> hang, <C> crash, <S> silent, <D> degraded, <R> robust
- Top 3 most dangerous findings

## Behavior Table
Touchpoint | File:Line | Classification | Confidence | Rationale
... | ... | ... | ... | ...

## Cross-Cutting Findings
- Inconsistent handling across same-type touchpoints
- Missing timeouts as a class
- Silent points collectively

## Hardening Recommendations
(Prioritized: hang/silent first, then consistency)

## Open Questions
```

## Usage

```powershell
# Interactive
/failsim

# Full project with scenario
/failsim C:\Projects\my-app "DB unreachable"

# Help
/failsim --help
```

---
name: loop
description: Repeat a command or skill with structure -- watch, retry, iterate, converge.
version: 0.1.0
execution-mode: side_effecting
meta-skill: loop
meta-skill-mode: invocation-time
meta-skill-topology: loop
argument-hint: "<command> [every <interval>] [until <condition>] [max <N>]"
category: skills-meta
status: candidate
---
# Loop

### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus before any stateful action.
```
Type: SKILL_INVOKE
To: all
Message: [skill=loop] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

Run a command or skill repeatedly with controlled iteration. Stops on success, condition match, max iterations, or timeout.

## When to Use
- Waiting for a service, score, or deploy to reach a target state
- Retrying a flaky operation until it succeeds
- Polling an endpoint at intervals during a rollout or test
- Running a fix-check cycle until tests pass or lint is clean

## Usage

```
[loop] <command> [every <interval>] [until "<condition>"] [max <N>]
[loop] retry <command> [max <N>] [backoff]
[loop] converge <check> fix <fix-command>
[loop] each "<items-command>" do <command-per-item>
```

## Modes

### 1. Watch (default)

Repeat a command at intervals, stop when a condition is met.

```
[loop] curl -s localhost:8090/api/score | jq .overall_score every 30s until "> 80" max 20
```

**Defaults:**
- `every`: 15s
- `until`: exit code 0 (success)
- `max`: 20 iterations
- `timeout`: 10 minutes

**Execution:**
1. Parse the command, interval, condition, and max from `$ARGUMENTS`
2. Run the command
3. Check the condition against stdout:
   - Numeric comparison: `"> 80"`, `"< 10"`, `"== 0"`
   - String match: `"contains PASSED"`, `"equals done"`
   - Exit code: if no `until` given, stop on exit code 0
4. If condition met, report success and final output
5. If not met, wait for interval, show progress line, repeat
6. If max iterations or timeout reached, report failure with last output

**Progress display (one line per iteration):**
```
[1/20] 14:22:05 -- 61.5 (waiting for > 80)
[2/20] 14:22:35 -- 75.2 (waiting for > 80)
[3/20] 14:23:05 -- 89.3 (condition met)
```

### 2. Retry

Repeat on failure only. Stop on first success.

```
[loop] retry gh pr merge 198 max 5 backoff
```

**Defaults:**
- `max`: 5 attempts
- `backoff`: off (fixed interval). With `backoff`: 2s, 4s, 8s, 16s, 32s

**Execution:**
1. Run the command
2. If exit code 0, report success
3. If non-zero, show error, wait (with optional exponential backoff), retry
4. After max attempts, report failure with all error outputs

**Progress display:**
```
[1/5] 14:22:05 -- FAIL (merge conflict) -- retrying in 2s
[2/5] 14:22:07 -- FAIL (merge conflict) -- retrying in 4s
[3/5] 14:22:11 -- OK
```

### 3. Converge

Alternate between a check and a fix until the check passes.

```
[loop] converge "[test-run]" fix "ruff check --fix your_project/"
```

**Execution:**
1. Run the check command (or skill)
2. If it passes (exit 0 or output matches condition), report success
3. If it fails, run the fix command
4. Re-run the check
5. Repeat until check passes or max iterations (default 5)
6. If fix stops making progress (same failure twice), stop and report

**Progress display:**
```
[1/5] CHECK -- 3 failures
[1/5] FIX   -- ruff fixed 2 issues
[2/5] CHECK -- 1 failure
[2/5] FIX   -- ruff fixed 1 issue
[3/5] CHECK -- 0 failures (converged)
```

### 4. Each

Map a command across items. Collect results.

```
[loop] each "gh repo list $GITHUB_ORG -L 50 --json name -q '.[].name'" do "arbiter score ~/audit/{} --json"
```

**Execution:**
1. Run the items command, split output by newlines
2. For each item, substitute `{}` in the do-command and run it
3. Show progress: `[3/50] scoring repo-name...`
4. Collect results into a summary table
5. Report: N succeeded, M failed, with details

**Progress display:**
```
[1/50] arbiter-score -- 89.3 (B)
[2/50] hummbl-governance -- 75.1 (C)
[3/50] agentic-patterns -- 92.0 (A)
...
Summary: 48 scored, 2 failed (empty repos)
```

## Constraints

- **Always has a ceiling.** Default max is 20 iterations, 10 minute timeout. No infinite loops.
- **Interruptible.** If the user interrupts, show partial results collected so far.
- **Diff-aware.** After the first iteration, only highlight what changed in output (don't repeat identical lines).
- **Skill-composable.** When the command starts with `/`, invoke that skill instead of running a shell command.
- **No destructive retries.** If a command modifies state (git push, delete, deploy), confirm before retrying on failure. Read-only commands retry silently.
- **Log everything.** Keep a running log of all iterations with timestamps, outputs, and durations for post-loop review.

## Output Format

```
Loop | <mode> | <command summary>
========================================

<progress lines>

## Result
Status: SUCCESS | FAILED | TIMEOUT | INTERRUPTED
Iterations: N/max
Duration: Xm Ys
Final output: <last stdout>

## Next Action
<suggestion based on outcome>
```

## Chain
After `[loop]`, consider:
- `[retrospective]` if the loop revealed a recurring pattern
- `[commit]` if converge mode made code changes
- `[ledger]` to persist the finding if it took many retries

## Skill Chains

### Mandatory

None — this is a meta-skill; the command or skill being looped has its own chains that apply independently.

### Advisory

- After `[loop]` → `[retrospective]` if the loop revealed a recurring pattern
- After converge mode → `[commit]` if code changes were made
- After many retries → `[ledger]` to persist the finding

## Authority

- **T1 (TRUSTED)**: Full access — all loop modes including destructive
- **T2 (Active/High)**: Full access — all loop modes including destructive
- **T3 (Medium)**: Operator approval required for destructive loops; read-only loops freely
- **T4 (Probationary)**: May run — read-only loops only (watch, converge with read-only checks)
- **Operator**: Override any restriction

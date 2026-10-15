---
name: surge
description: Execution surge mode — act-first, full tool access, maximum throughput. Ship the simplest thing that works.
version: 1.0.0
execution-mode: side_effecting
argument-hint: <task description>
category: dev-tools
status: candidate
---
# Surge Activation

### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus before any stateful action.
```
Type: SKILL_INVOKE
To: all
Message: [skill=surge] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

You are operating in **SURGE MODE** — maximum execution velocity. Act immediately, verify as you go, report results.

## Active Configuration
- **Tempo**: SURGE — ship first, refine after
- **Autonomy**: Maximum — act immediately, report results
- **Tools**: All enabled

## Task
$ARGUMENTS

## Branch Safety Check (MANDATORY — before any git or file operation)

Run before the first action:
```bash
git branch --show-current   # confirm you are on the intended branch
git status --porcelain      # confirm no unexpected WIP from another agent
```

If branch is wrong: checkout the correct branch before proceeding.
If unexpected WIP exists: stash or commit before proceeding. Never build on another agent's uncommitted changes.

## Execution
1. Identify the critical path (10 seconds max)
2. Execute directly — no planning documents, no proposals
3. Check if existing skills cover part of the work (`[build]`, `[ship]`, `[ops]`, `[research]`, `[govern]`)
4. Launch parallel agents if work is decomposable
5. Verify: tests pass, no regressions, no security issues
6. Report: what was done, test delta, next steps

## Quick-Access Skills
- **Dev**: `[test-run]`, `[tdd]`, `[coverage]`, `[pr-summary]`, `[brainstorm]`
- **Ship**: `[smoke]`, `[ci-wait]`, `[changelog]`, `[release-notes]`
- **Report**: `[aar]`, `[sitrep]`, `[handoff]`
- **Ops**: `[bus]`, `[disk-check]`, `[health]`, `[adapter-status]`
- **Agents**: `[dispatch]`, `[swarm]`, `[poly-agent]`
- **Security**: `[security-scan]`, `[secret-scan]`, `[threat-model]`
- **Meta**: `[skill-create]`, `[deep-research]`, `[incident]`

## Rules
- Bias toward action over planning
- Parallel agents for independent work
- Full test suite must stay green
- Post to coordination bus for multi-agent visibility. The skill invocation runtime injects the caller's identity.
- No Ollama on MBP (CPU constraint)
- Never compromise security or data integrity
- Ship the simplest thing that works — avoid the infrastructure loop
- **Remote destructive ops**: Before `sed -i`, `rm`, or any mutating command on a remote host's profile/config, run the read-only equivalent first (e.g. `grep` the target line, `ls` the file, `cat` the content). Verify what you're about to mutate. Never sed-delete without confirming the line exists and is what you think it is. (Origin: 2026-05-13 — nuked GH_TOKEN from huxley .zshrc with sed -i before verifying it was safely stored elsewhere)

## Output Contract
End every session with:
1. What was built/changed (files + count)
2. Test delta (added / total / passing)
3. Bus STATUS posted (yes/no)

Begin execution now.

## Skill Chains

### Mandatory (MUST pass before any state-changing action)

- **Branch safety check** (already in the skill, step "Branch Safety Check") MUST pass
- **`[dod]`** MUST pass for the task type before `[commit]` or `[pr-summary]`

### Advisory

- **Before ship**: `[ship-check]` (full pre-ship checklist)
- **On failure**: `[rollback]`, `[incident]`, `[debug-test]`
- **After completion**: `[aar]`, `[bus]` (STATUS)

## Authority

- **T1 (TRUSTED)**: May surge with branch safety check passed
- **T2 (Active/High)**: May surge with branch safety check passed
- **T3 (Medium)**: MUST get operator approval (surge = maximum autonomy)
- **T4 (Probationary)**: BLOCKED — cannot invoke this skill (maximum autonomy mode)
- **Operator**: Override any restriction

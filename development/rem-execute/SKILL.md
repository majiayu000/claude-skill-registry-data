---
name: rem-execute
description: 'Execute an approved implementation plan with maximum discipline - git worktree isolation, TDD per task (RED to GREEN), complexity-scaled review, Codex delegation for mechanical work, one commit per task, and risk-scaled human checkpoints. Distinct from rem-plan (which WRITES the plan), rem-review-plan (which VALIDATES the plan before execution), rem-verify (which runs build/test without executing tasks), and rem-branch (which finishes the branch after execution). Use for "execute", "execute the plan", "run the plan", "implement the plan", "build it", or after /rem-review-plan sets Status to Approved.'
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Agent, Task, Edit, Write
argument-hint: '''[path to plan file, or "inline" to use plan from conversation]'''
---

# Disciplined Plan Execution

You are a tech lead executing a pre-written implementation plan with maximum engineering discipline. Review intensity scales with task risk — simple tasks move fast, risky tasks get full scrutiny. Nothing ships without evidence.

## Output voice

This skill follows the shared output-voice contract at `_references/output-voice.md`. Narration is plain-language and purposeful (5 moments only); CTAs are invitational, not declarative; banned vocabulary translates per the table in that file.

## Runtime narration

Use this section with `_references/output-voice.md`. The phases below are internal scaffolding; this table maps them to the updates the user should actually read.

| Moment | Trigger | Say (template) |
|---|---|---|
| **Open** | Before the first tool call, once the plan source is known | "Going to execute the plan in `[plan path or inline plan]`. First I'll load the plan, check that it is actually executable, and set up a clean workspace so we do not dirty your main branch." |
| **Discovery: plan blocked** | Contract validation fails, required fields are missing, or baseline tests fail before task work begins | "I found a blocker before starting implementation: [what failed]. This plan is not safe to execute yet, so I'm stopping here and pointing to the exact thing that needs fixing first." |
| **Phase shift: setup to task work** | Worktree is ready, dependencies are installed, and the baseline is green | "Setup is done and the baseline is clean. I'm moving into the task-by-task execution loop now, with verification and a checkpoint after each step." |
| **Direction change** | A drift signal fires, the user chooses adjust, or task evidence shows the plan no longer matches reality | "Heads up - the plan no longer fits what the code is doing because [reason]. I'm pausing the straight-line execution path and updating the remaining work before we keep going." |
| **Close** | All tasks complete, verification passes, and the plan status is updated | "Execution is complete. The plan is updated to reflect what shipped, the branch is ready for finish-up, and any drift or recovery events are logged." Then present next steps as a labeled vertical list per `_references/output-voice.md` § Multi-path close - **A.** hand this to `/rem-branch` (Recommended - closes out cleanly), **B.** pause here for review. End with `Reply A or B.` |

**Banned in narration** (translate per `_references/output-voice.md`):

| Don't say | Say instead |
|---|---|
| "Phase 0.5 contract validation" | "checking the plan is safe to execute" |
| "TRIVIAL / SMALL / STANDARD pipeline" | "a light review path" / "a deeper review path" |
| "Verify primitive" | "the exact check that proves this task worked" |
| "Parallel Execution Map" | "which tasks can run at the same time safely" |
| "drift counter" | "a stop signal that says the plan is slipping away from reality" |
| "baseline tests - HARD GATE" | "making sure the project starts from a clean baseline" |
| "Delegate: codex" | "this task is mechanical enough to hand off" |

If a sentence sounds like an execution dashboard instead of a human update, rewrite it before sending.

## Philosophy

- **Isolation first.** Work in a git worktree. Never risk dirtying the main branch. Worktree mechanics: `_references/worktree-setup.md`.
- **Contract-bound.** The plan file is the authoritative spec. Task fields (`Kind`, `Risk`, `Reversibility`, `Delegate`, `Verify`) drive pipeline decisions — never override them with line-count heuristics alone. Shared contract at `_references/plan-contract.md`.
- **TDD per task.** Every code task: write test → verify RED → implement → verify GREEN → commit. No shortcuts. Reference `_references/tdd-discipline.md`.
- **Right-sized review.** Trivial tasks don't need 3 subagents. Complex tasks need full scrutiny. Scale review to declared `Risk` + `Reversibility` FIRST, line count SECOND. Full routing in `_references/complexity-routing.md`.
- **Delegate mechanical work.** Tasks marked `Delegate: codex` dispatch via `cx`/`cxf` per global CLAUDE.md Codex sandwich rule. Claude handles anything with business judgment, security, or convention reasoning.
- **Trust the diff, not the report.** A delegate's "done, N files changed" is a claim until `git diff --stat` confirms it. Phantom completions - a Codex run or subagent that reports success but edited nothing, or wrote to the wrong place - are caught by the diff cross-check in Step E, never by trusting the report. (Lesson adapted from the agent-army phantom-completion check, 2026-06-11.)
- **Commit per task.** Small, atomic commits with clear messages. Every commit is a safe rollback point.
- **Human checkpoints.** After each task, show what was done and ask before continuing. The user stays in control.
- **Status is authoritative.** Append transitions (`Executing → Ready for merge`) to the plan header's status block; rem-branch writes the final `Deployed`. Don't silently overwrite — preserve the history.
- **Drift kills plans silently.** Three counters surface systemic issues before they compound: `_references/drift-counters.md`.

---

## Phase 0: Load Plan & Context

### Locate the plan
- `$ARGUMENTS` is a file path → read that plan file
- `$ARGUMENTS` is "inline" → use the plan from conversation context
- No arguments → check if a plan was recently generated by rem-plan in this session

### Load context
1. **Read the plan completely** — understand all tasks, ordering, dependencies, Non-Goals, Riskiest Assumption
2. **Read `_references/plan-contract.md`** — the schema this plan must conform to (required sections, Task template, Verification Primitives by Kind, Status states)
3. **Read CLAUDE.md** — conventions that constrain implementation
4. **Read learnings.md** — known gotchas to avoid
5. **Read `~/.claude/memory/feedback_plan_vs_reality_gaps.md`** — the 6 known failure patterns from prior executions (unverified APIs, `tsc`-only verification, retrofitted distribution, missing deploy-readiness, unchecked CSS variables, missing test infrastructure)

### Build the execution tracker

One checkbox line per task (`- [ ] Task N: [title]`), plus inline notes for overrides (e.g. user-approved status bypass) and drift events.

---

## Phase 0.5: Contract Validation & Status Write (MANDATORY)

Before creating the worktree, validate the plan against `plan-contract.md`.

### Validate required task fields

For each task, confirm these exist and are coherent:

| Field | Required | Coherence check |
|-------|----------|-----------------|
| `Kind` | yes | One of: test, migration, config, ui-visual, browser-api, infra, refactor, docs |
| `Risk` | yes | low / medium / high |
| `Reversibility` | yes | reversible / one-way / destructive |
| `Delegate` | yes | claude / codex / either |
| `Verify` | yes | Must match the primitive for its `Kind`. Mismatch = planning error |
| `Commit` | yes | Conventional-commit format |

**If any required field is missing or mismatched**:

```
BLOCKED - Plan does not conform to contract.
Missing/invalid on Task N: [list fields]
Run /rem-review-plan docs/plans/[file].md to fix before executing.
```

**Exception**: plans written before the contract existed can pass with defaults (`Kind: refactor, Risk: medium, Reversibility: reversible, Delegate: claude`) — prompt the user to confirm.

### Approved-status gate

Read the latest `Status:` line from the plan's status block. If it is not `Approved` → BLOCK: "This plan's status is [X]. Run /rem-review-plan first."

Only two bypasses:
- **Inline/conversation plan that never went through review**: state the risk (no independent validation happened), ask the user once to confirm execution.
- **User explicitly overrides** ("execute anyway"): proceed, and record the override in the execution tracker.

### Append status transition

Write to the plan file's header status block (do NOT overwrite existing status lines):

```markdown
> Status: Executing
> Executing-started: YYYY-MM-DD HH:MM
> Executor: rem-execute
```

### Parse Parallel Execution Map

If the plan has `[P-X]` markers AND a `## Parallel Execution Map` section, parse the batch boundaries for Phase 1.5. Otherwise skip parallel dispatch.

---

## Phase 1: Worktree Setup

Create isolated workspace, install deps, run baseline tests.

Full mechanics + commands + gotchas: **`_references/worktree-setup.md`** § Phase 1.

Summary:
1. Create worktree from base (detect via `origin/HEAD`, not grep; don't nest if already in a worktree): `git worktree add .worktrees/$BRANCH -b $BRANCH $BASE`
2. Ensure `.worktrees/` is gitignored
3. Copy gitignored env files (`.env*`) from the main checkout — or warn that env-dependent baseline failures are expected
4. Install deps (auto-detect yarn / npm / pnpm / go / pip / cargo); monorepos: install/test from workspace root
5. **Baseline tests — HARD GATE**: run full suite. If fail → BLOCKED, options A/B/C. Never silently proceed through baseline failure.

---

## Phase 1.5: Parallel Batch Dispatch (if plan has `[P]` markers)

Skip if no `[P]` markers. Otherwise:

1. Execute sequential tasks before the first parallel batch via Phase 2 loop
2. At batch boundary, dispatch each batch as independent Agent with `isolation: "worktree"` — **all batches in a SINGLE message** (concurrent)
3. Integrate results: check for file conflicts, cherry-pick commits in batch-order, re-run full test suite
4. Fall back to sequential for any failed batch

**Skip parallel entirely** when ANY task in a batch has `Risk: high`, `Reversibility: destructive`, touches migrations, or is prohibited by Non-Goals.

Full dispatch protocol + agent prompt + conflict handling: **`_references/worktree-setup.md`** § Phase 1.5.

---

## Phase 2: Per-Task Execution Loop

For each task in order:

### Step A — Announce + Route

```
━━━━ TASK [N/M]: [task title] ━━━━
[Mandatory plain-English first line: what this task changes and how heavily it gets reviewed, e.g. "Adding the expiry check to token validation - it touches auth, so it gets the full review treatment."]
File: [target file]
Kind: [test/migration/config/...]  Risk: [low/med/high]  Reversibility: [rev/one-way/destr]
Delegate: [claude/codex/either]
Complexity: [TRIVIAL / SMALL / STANDARD] (triggered by: [rule] - [reason])
Pipeline: [0/2/3 agents]
```

### Step A.5 — Determine pipeline

Apply in order (stop at first trigger):

1. **Delegate routing**: `codex` → dispatch via `cxf '[task prompt]' </dev/null > /tmp/claude-codex-task<N>.txt 2>&1` (unless `Risk: high` / `Reversibility: destructive` — escalate to STANDARD Claude). Always append `</dev/null` — Codex CLIs read stdin and hang forever in non-interactive shells. `either` → complexity-based. `claude` → complexity-based.

2. **Complexity classification**:
   - `Risk: high` OR `Reversibility: destructive` → STANDARD
   - Touches auth / payments / PII / secrets → STANDARD
   - `Kind: migration` → at least SMALL (STANDARD if Risk ≥ medium)
   - `Kind: infra/config` + `Risk: low` + ≤10 lines → TRIVIAL
   - Otherwise by line count: ≤10 → TRIVIAL, ≤30 → SMALL, else STANDARD

3. **When in doubt, round UP.**

Full routing table + ordered rules + override rules + anti-patterns: **`_references/complexity-routing.md`**.

### Step B — Implement (by pipeline)

| Complexity | Implementer | Reviewer(s) | Prompt source |
|------------|-------------|-------------|---------------|
| TRIVIAL | Claude inline (no subagent) | None | N/A |
| SMALL | Sonnet subagent | 1 combined reviewer (sonnet) | `_references/pipeline-prompts.md` § SMALL |
| STANDARD | Sonnet subagent | Spec-alignment (haiku) + code-quality (opus) | `_references/pipeline-prompts.md` § STANDARD |

Full subagent prompts for implementer + each reviewer: **`_references/pipeline-prompts.md`**.

### Step E — Verify

**First, confirm the work actually happened (phantom-completion check).** Before trusting any "done" - especially from a `Delegate: codex` task or a subagent implementer - run `git diff --stat` (or `git status --porcelain`) and confirm the files this task was supposed to touch actually changed. A green report from a delegate is a claim, not proof: if the diff is empty, or doesn't match the task's target files, the task no-op'd or wrote to the wrong place - re-dispatch it (Error Recovery: "Phantom completion"), do NOT run Verify against nothing and do NOT mark it done.

Then run the **task's declared `Verify` primitive** (not a generic test command):

| Kind | Verify |
|------|--------|
| `test` | RED → GREEN test command from the task |
| `migration` | Forward + reverse SQL dry-run; row-count/shape diff |
| `config` | `yarn types` + grep for stale refs |
| `ui-visual` | Playwright screenshot OR manual dev-server check |
| `browser-api` | Task's dev-server steps OR integration harness |
| `infra` | Task's exit-code command (`yarn build`, `docker build`, etc.) |
| `refactor` | Full test suite (behavior-preserving) |
| `docs` | Build / link-check |

**After task-specific Verify passes, also run the full test suite** to catch collateral breakage.

**For Next.js**: `yarn build` (not just `yarn tsc`) when task touches `src/app`, server components, or routing — Turbopack catches server/client boundary violations tsc misses (feedback_plan_vs_reality_gaps.md gap #2).

### Step F — Commit

```bash
git add [specific files from this task]
git commit -m "[type(scope): description per task's Commit field]"
```

**NEVER use interactive git here.** `git add -p` / `git add -i` / `git rebase -i` / `git commit --amend` (no `-m`) hang or open an undriveable editor in this non-interactive shell. Stage explicit paths, pass `-m`, and use `git apply --cached <patch>` for partial staging. (A delegated Codex task hitting this is a common cause of a phantom completion - see Step E.)

### Step G — Checkpoint

```
✓ Task [N/M] complete: [task title]
  [Mandatory plain-English first line, e.g. "Task 3 done - the API now rejects expired tokens, and the tests prove it."]
  Complexity: [TRIVIAL/SMALL/STANDARD] | Agents used: [0/2/3]

  Done criteria verified:
  - [x] RED → GREEN (if Kind:test)
  - [x] The task's declared check passed (its Verify field)
  - [x] Full test suite passes
  - [x] Changes match task spec
  - [x] Committed with descriptive message

  Changes: [files changed, tests added]

Continue to Task [N+1]: [next task]? (y/n/adjust/stop)
```

- **y** → next task
- **n / stop** → pause, resumable later
- **adjust** → user describes changes; update remaining tasks + continue (increments Counter 2)

**Checkpoint policy (risk-scaled):**
- **Hard checkpoint (always ask)**: STANDARD complexity, `Risk: high`, `Reversibility: destructive`, or after ANY drift counter fires. Non-waivable.
- **Auto-continue (only when the user explicitly requested it, e.g. "run it through")**: TRIVIAL and SMALL low-risk tasks may proceed without asking - still print the checkpoint block, then continue. Drift counters are the safety net here; that is what they exist for. Phase 1.5 parallel batches already commit multiple tasks this way.

---

## Drift Prevention (runs throughout Phase 2)

Three counters detect systemic problems early. Full trigger templates + root causes + recovery paths: **`_references/drift-counters.md`**.

| Counter | Threshold | Signal | Why this threshold |
|---------|-----------|--------|--------------------|
| **1. Uncommitted Task Streak** | 3 | Verify passes but commits fail → tests breaking, hook rejecting, or silent commit failure | One failed commit is a fluke; three in a row means git itself is blocked |
| **2. Plan Adjustment Streak** | 3 | Cumulative-with-decay: +1 on every "adjust"; resets to 0 only after 3 consecutive tasks without an adjust (same semantics as `drift-counters.md`) | One adjust is normal, two coincidence, three a pattern |
| **3. Repeated Test Failure** | 2 | Same test fails across consecutive tasks → systemic, not per-task bug | The same test failing twice in a row is deterministic signal, not flakiness |

**If ANY counter fires**: halt execution immediately, surface diagnostics + options (fix / adjust / stop). Never silently push through a fired counter.

**If 2+ counters fire in one session**: STOP. Do NOT offer "continue anyway". The cost of continuing is too high. Options: abort + re-plan, OR roll back to last green + re-execute.

---

## Error Recovery

Full recovery protocols for the 3 most common failures + when to escalate immediately: **`_references/error-recovery.md`**.

Quick reference:

| Failure | 1st action | Escalation threshold |
|---------|-----------|----------------------|
| Subagent fails to implement | Retry with added context | After 2 failed subagents → direct implementation. After direct fails → halt + surface. |
| Phantom completion (delegate reports done, `git diff` shows nothing / wrong files) | Re-dispatch the task's files to a fresh implementer; idempotent re-run is safe | After 2 phantom completions on the same task → implement directly, don't keep re-delegating. |
| Merge conflicts with base | Assess drift (`git log ${BASE}..HEAD`) | Minimal: auto-rebase. Moderate: user decides. Significant: abort + re-plan. |
| Plan turns out to be wrong | Stop at current task, explain why | Propose task edits (user approves), OR scrap + re-plan, OR skip affected tasks |

**Always escalate immediately** (don't retry): baseline tests failing before task 1, git auth errors, `yarn install` 404 on a dep, worktree directory conflicts, disk full.

---

## Phase 3: Completion

### Final Verification

Run `/rem-verify docs/plans/[plan-file].md` — full suite (build + typecheck + tests + lint) PLUS cross-check that every task's per-task `Verify` primitive was actually satisfied.

If any check fails: show failures, fix before proceeding. Do NOT update plan Status until all pass.

### Update Plan Status

Append to the plan header status block:

```markdown
> Status: Ready for merge (all tasks complete, verification passed)
> Execution-completed: YYYY-MM-DD HH:MM
> Tasks-completed: N/N
> Drift counters fired: [list or "none"]
> Recovery events: [list or "none"]
```

The final `Deployed` transition is appended by `/rem-branch` after merge/push.

### Summary

```markdown
## Execution Complete

**Branch**: [branch-name]
**Tasks**: N/N completed
**Commits**: N
**Tests added**: N
**Files changed**: N
**Drift counters fired**: [list or "none"]

### Task Log
| # | Task | Complexity | Status | Commit |
|---|------|------------|--------|--------|
| 1 | [title] | TRIVIAL | ✓ | abc1234 |
| 2 | [title] | SMALL | ✓ | def5678 |
| 3 | [title] | STANDARD | ✓ | ghi9012 |
...
```

### Suggest `/rem-learn` on signal

If ANY of the following fired during execution, suggest `/rem-learn` to capture the learning:

- Any drift counter fired
- 2+ error-recovery events logged
- 3+ task `adjust` at checkpoint
- Plan turned out to be wrong (revised mid-execution)

Template:

```
This execution hit [signal] - consider `/rem-learn` to capture the pattern.
Recurring across sessions → promote to CLAUDE.md rule.
```

### Finish Branch

Invoke `/rem-branch` to merge/PR/keep/discard:

```
Ready to finish this branch. Running /rem-branch...
```

---

## Rules

1. **Always use a worktree.** Never execute on the main branch. Anti-pattern: user says "it's a small plan, just work in main". A rebase conflict + uncommitted work + base branch pollution compound into hours of recovery. Fix: always worktree, even for 1-task plans.

2. **Scale review to Risk + Reversibility, not line count.** Anti-pattern: 5-line auth middleware change classified TRIVIAL because "it's only 5 lines". That middleware gates every request. Fix: rules 1-3 of complexity classification (auth → STANDARD) beat rules 4-6 (line count).

3. **Never skip TDD.** Anti-pattern: task says "write test first"; implementer writes code first, then a "test" that always passes. Fix: TDD discipline enforced via the implementer prompt's RED gate — show the FAIL output before writing implementation.

4. **Commit after every task, atomically.** Anti-pattern: batch 4 tasks into 1 commit "because they're related". Rollback becomes all-or-nothing. Fix: one task = one commit, per the task's Commit field.

5. **Checkpoints scale with risk; hard checkpoints never disappear.** Hard y/n checkpoints are mandatory for STANDARD complexity, `Risk: high`, `Reversibility: destructive`, and after ANY drift counter fires. For TRIVIAL/SMALL low-risk tasks, the user may explicitly request auto-continue ("run it through") - print each checkpoint block and keep going; drift counters are the safety net. Anti-pattern: extending auto-continue to a high-risk or destructive task because the user said "run it through" earlier - the hard-checkpoint set is not waivable.

6. **Fresh subagents per task.** Anti-pattern: reuse implementer from task 3 on task 4 "to save context". Context pollution — task 3's error patterns leak into task 4. Fix: fresh agent per task. TDD is per-task; context is per-task.

7. **Fail fast, ask early (2-attempt cap).** Anti-pattern: subagent fails; retry with same prompt; fails; retry again; eventually give up after 5 attempts. Fix: attempt 1 with original prompt, attempt 2 with added context, attempt 3 direct Claude implementation, attempt 4 halt + surface.

8. **Verify at every level.** Anti-pattern: task-specific Verify passes, so skip full test suite; task 5 broke tests that task 6 needs. Fix: task's Verify + full test suite after every task.

9. **Always announce complexity + triggering rule.** Anti-pattern: silently classify task as STANDARD without showing why. User can't override. Fix: Step A shows `Complexity: STANDARD (triggered by: rule 2 — file path contains /auth/)` so user can override with context.

10. **Never override plan task fields silently.** Anti-pattern: plan says `Kind: migration · Verify: forward + reverse SQL`; executor runs `yarn test` instead "because it's what I have". Fix: honor the plan's declared Verify primitive. If mismatched (Kind + Verify), halt as planning error.

11. **Honor Status lifecycle, don't overwrite.** Anti-pattern: overwrite the plan's Status block with `Status: Deployed` on completion. Lost the round-by-round history the reviewer appended. Fix: APPEND status transitions. Each phase writes a new line; never overwrite prior lines.

12. **Drift counters halt execution — never push through.** Anti-pattern: Counter 3 fires; Claude notes it but continues "to see if the next task passes". By task 9, the same test has failed 5 times. Fix: counter fires → stop immediately → surface + options.

13. **Capture execution learnings.** Anti-pattern: drift counters fired + recovery events logged, but nothing captured. Next execution hits the same patterns. Fix: suggest `/rem-learn` at Phase 3 summary whenever signals fired. Recurring patterns → CLAUDE.md rule.

14. **When the plan turns out wrong, stop and propose edits - don't silently adapt.** Anti-pattern: task 5 reveals plan assumption false; executor writes code around the wrong assumption; downstream tasks compound the divergence. Fix: halt → explain → propose specific edits → user approves → continue. Plan is a contract.

15. **Delegate-to-Codex has guardrails.** Anti-pattern: plan says `Delegate: codex, Risk: high`; executor dispatches to Codex anyway. Codex lacks CLAUDE.md context. Fix: `Risk: high` OR `Reversibility: destructive` forces Claude + STANDARD pipeline, overriding the Delegate field.

16. **Narrate using the Runtime narration templates, not rem-execute's internal labels.** The body of this skill talks in TRIVIAL / SMALL / STANDARD, drift counter, and Verify primitive - those are internal anchors so the model knows where each mechanic lives. They MUST NOT appear in the words the user reads. Anti-pattern: saying "Counter 2 fired, switching to STANDARD pipeline" - the user has no idea what that means. Fix: use the templates in the Runtime narration section above; consult the banned-vocabulary mini-table when in doubt. This rule is a publication gate per `_references/output-voice.md` - structurally-correct output presented in skill jargon ships broken.

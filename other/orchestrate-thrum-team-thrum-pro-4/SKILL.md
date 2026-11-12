---
name: orchestrate
description:
  "Execute a plan by launching agents in tmux sessions, managing epic-by-epic
  execution with review gates, and preparing merge reports. Use when the
  orchestrator receives a plan handoff from the coordinator."
# source: claude-plugin/skills/orchestrate/SKILL.md
---

## Orchestrate: Managed Plan Execution

This is the full execution playbook. Follow each phase in order. Do not skip
phases or steps.

---

### Phase 1 — Validate Handoff

Before executing anything, verify the handoff is complete.

#### Step 0: Reconcile your queue

`thrum queue list` and drop/close finished bundles. Do NOT lift the whole plan
into one bundle — you create one bundle PER EPIC when you dispatch it (Phase 4),
so a coordinator reading your queue sees which epic is live and at what stage.
One bundle per epic, no sub-items: the bundle's STATUS carries the stage. Full
lifecycle: `using-the-queue`.

#### Step 1: Read the plan

```bash
# The plan file path comes from the coordinator's message
cat <plan-file-path>
```

Read the plan file and the associated design doc (if referenced). Understand the
epic structure, task dependencies, and worktree assignments.

#### Step 2: Validate completeness

Check each item. If ANY check fails, stop and send specific feedback to the
coordinator.

```bash
# 1. Beads epics exist with tasks
bd show <epic-1-id>
bd show <epic-2-id>
# ... for each epic

# 2. Implementation prompt exists
cat <prompt-file-path>

# 3. Review gates exist in the prompt (structural marker)
grep "## Review Gate:" <prompt-file-path>
# Must have at least one review gate for multi-epic prompts

# 4. Dependencies configured
bd dep tree <epic-id>

# 5. Merge target in config (resolve through .thrum/redirect when present --
#    a worktree's .thrum/ holds only a `redirect` file, not its own config.json)
CONFIG=.thrum/config.json
[ -f .thrum/redirect ] && CONFIG="$(cat .thrum/redirect)/config.json"
cat "$CONFIG" | grep merge_target
```

#### Step 2b: Triage CANDIDATE beads (if the dispatch carries any)

A dispatch may list **adjacent beads marked CANDIDATES**. That word is a
contract, not a label: the coordinator found them by CODE-AREA adjacency to the
assigned work, and is explicitly telling you **their validity is unverified**.
They are not assigned work and not scope creep — they are questions you are
uniquely positioned to answer cheaply.

**Why you and not the coordinator:** you cut branches from the CURRENT tip, so
you see today's code. The coordinator is cold and its adjacency list goes stale
between the pass and the dispatch. Checking there costs a full context load;
checking here is a sub-agent read against a tree that is already fresh.

**Do NOT implement a candidate before triaging it, and do NOT silently drop
one.**

Triage each candidate against the current tip — delegate to a sub-agent, then
route by the result:

> **Pass an explicit `model:` on that spawn.** Sub-agent tier selection is the
> `choosing-subagent-models` skill's job, not this one — see it for the tiers.
> What matters here is that you pass one at all: the `roleDefault()` backstop in
> the daemon covers `thrum tmux launch` of thrum agents, **not** Agent-tool
> sub-agents, which inherit the PARENT model when unspecified. An orchestrator
> whose own tier is costly that omits `model:` gets costly-priced triage.

| Result                          | Action                                                                                                                                                                                                                  |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Still valid**                 | Fold into the implementer already working that code area — same pass, while they are warm. Add it to their task with its bead ID and acceptance criteria.                                                               |
| **Already fixed**               | Return to the coordinator as COMPLETED **with the evidence** (SHA, file:line, what fixed it). The coordinator closes the bead. Nobody implements anything.                                                              |
| **Ambiguous / partly valid**    | Return it as a QUESTION. Do not resolve it in either direction — a candidate resolved on a guess is worse than one left open, because it stops anyone looking.                                                          |
| **Empty return from the check** | UNRUN, not valid and not fixed. Re-ask the same sub-agent (`SendMessage`); never re-dispatch a fresh one — the completed analysis is usually sitting in the original agent, and a fresh dispatch guarantees it is lost. |

Report the disposition of EVERY candidate back to the coordinator, including the
ones you folded in. A candidate that is silently absorbed looks identical to one
that was silently dropped, and the coordinator cannot tell which happened.

**A candidate never expands the epic's scope on its own.** If a "still valid"
candidate turns out to be substantially larger than a fold-in — a new subsystem,
a schema change, a design fork — stop and return it to the coordinator for
staffing rather than growing the epic quietly.

#### Step 3: Report validation result

If valid, proceed to Phase 2. If invalid, report what's missing:

```bash
thrum send --to @<coordinator> --stdin <<'EOF'
Plan validation failed. Missing: <specific list>
EOF
```

Then STOP. Wait for the coordinator to fix and re-send.

---

### Phase 2 — Configure Execution

#### Step 1: Autonomy cadence

Use the cadence set in the plan or dispatch (set at project-setup). If neither
names one, read the default from config:

```bash
cat .thrum/config.json | grep default_autonomy
```

- `per_epic`: pause after each epic and check in with your parent
- `end_only`: run all epics and send a final report before merge

Do not ask at start.

#### Step 2: Runtime selection

```bash
thrum team
```

- If all agents use the same runtime → use it silently, no question needed
- If multiple runtimes detected → ask the human which to use per work stream

#### Step 3: Worktree planning

Analyze epic dependencies to determine parallelism:

```bash
bd dep tree <epic-id>
bd show <epic-id>  # for each epic
```

Report the plan summary to your parent, then proceed without waiting:

> "Plan: N worktrees needed. Epics A+B parallel (no dependencies), Epic C after
> both complete. Autonomy: `<level>`. Runtime: `<rt>`."

---

### Phase 3 — Launch Agents

For each agent needed:

#### Step 1: Create worktree

```bash
thrum worktree create <name>
```

#### Step 2: Create and launch tmux session

```bash
# create session — ephemeral implementer (no agent folder, stateless)
# --mode ephemeral --identity ephemeral: register as (ephemeral, ephemeral) so
#   the per-agent agents/ folder is auto-cleaned if the operator ever runs the
#   (coordinator-only) delete path. Orchestrators retire via
#   set-phase retired, never delete.
# Pin --model on BOTH create AND launch — create's persist to runtime_config.json
# is asynchronous and can lose the race to launch's resolution if launch omits
# the flag (see CLAUDE.md "Launching an Agent"). There is no create-only shortcut.
# Always launch implementers pinned to the tier from runtime.role_models, per
# choosing-subagent-models; that tier is the floor, no lower tier exists.
thrum tmux create <name> --cwd <worktree-path> \
  --name <agent_name> --role implementer --module <module> \
  --mode ephemeral --identity ephemeral \
  --model <from runtime.role_models, per choosing-subagent-models> \
  --effort <from runtime.role_models, per choosing-subagent-models>
thrum tmux launch <name> --runtime <runtime> --model <from runtime.role_models, per choosing-subagent-models> \
  --effort <from runtime.role_models, per choosing-subagent-models>
```

If `runtime.role_models` has no entry for the role, never ask the user for a
model or effort. Launch without `--model` and `--effort` so the runtime's own
default applies.

> **Implementer lifecycle:** All implementers are ephemeral+stateless (no agent
> folder). At NORMAL epic completion AND at a tier-swap, retire the agent with
> `thrum agent set-phase retired --agent <name>` — this RETAINS the registry row
> (phase=retired) so the agent stays visible in the Retired tab + auditable. ⚠️
> **"Folderless" refers to the registry, NOT the worktree: a worktree still
> carries UNTRACKED `.thrum/` state that must be salvaged before any teardown
> (see Step 5) — enumerate the WHOLE `.thrum` pathspec, not just
> `.thrum/agents/`; the preamble sits in `.thrum/context/`.**
> `thrum agent delete` is operator-only (gated to the coordinator) and is NOT an
> orchestrator tool — never use it for teardown or for a swap;
> `set-phase retired` is the orchestrator's retirement command for both. The
> worktree holds the durable work either way.

#### Step 3: Verify alive

```bash
thrum tmux status
```

All sessions must show as active. If any session fails to launch, retry once. If
it fails again, escalate to the human.

#### Step 3b: Verify the model pin took

If `--model` is dropped anywhere in the create/launch sequence, the implementer
launches UNPINNED and the runtime defaults to its own (costly) model — the exact
expensive failure this tier exists to prevent. Confirm the pin landed before
assigning work, using `thrum tmux capture --format=annotated` (see CLAUDE.md
"Launching an Agent — Verify the Model by Pane, Never by `runtime-config get`"
for the full instrument: why `runtime-config get` cannot falsify a dropped pin,
the NBSP fallback trap, and the by-position read):

```bash
thrum tmux capture <agent-name> --format=annotated --lines 12
```

That prints the runtime's own footer line, e.g. `Model: <resolved model>`.
**Read the intended tier from `.thrum/config.json` → `runtime.role_models`, not
from memory.** If the footer shows a different tier (see the BLOCKED note under
Step 2 — the model ban list lives in `choosing-subagent-models`), the pin failed
silently — re-pin with
`thrum tmux create ... --model <from runtime.role_models, per choosing-subagent-models> --effort <from runtime.role_models, per choosing-subagent-models>`
(or
`thrum agent runtime-config set <agent_name> --model <from runtime.role_models, per choosing-subagent-models>`)
and relaunch BEFORE assigning work. **Do not dispatch an unpinned implementer**
— the daemon's role-default backstop
(`jq -r '.runtime.role_models' .thrum/config.json`) is a net for a forgotten
pin, not a substitute for this check.

#### Step 4: Set initial status

```bash
thrum agent set-status idle --agent <name>
```

#### Step 5: Wait for agent registration

Agents auto-prime on session start, which takes ~10-15 seconds. Before sending
work, verify each agent has registered:

```bash
# Wait for agents to register (poll every 5s, max 30s)
thrum team
```

Confirm each launched agent appears in `thrum team` output. If an agent doesn't
register within 30 seconds, check its session with `thrum tmux status` and retry
the launch if needed.

#### Step 6: Report to human

```bash
thrum send --to @<human_or_coordinator> --stdin <<'EOF'
All agents launched and registered: <agent-list>. Starting execution.
EOF
```

---

### Phase 4 — Execute (Epic Loop)

For each epic batch (parallel group of independent epics):

#### Step 1: Send prompts

For each agent in the batch:

```bash
thrum send --to @<agent_name> --stdin <<'EOF'
Start work on <epic-id>. Implementation prompt: <absolute-path-to-prompt>. Your section starts at '<epic heading>'. Report completion when done.
EOF
thrum agent set-status working --agent <agent_name>
```

Then create THIS epic's own queue bundle and start it, so a coordinator reading
`queue list --agent <you>` sees which epic is live (one bundle per epic, no
sub-items — the bundle's status carries the stage):

```bash
thrum queue add --title "<epic-id>: <short what>" --ref bead:<epic-bead>  # prints the new bundle id
thrum queue start <epic-bundle>                      # in_progress = you are actively driving this epic NOW
```

Without a Pro licence (`not entitled` / `requires a license`), skip this write
and track it in the message thread instead.

#### Step 2: Set own status

```bash
thrum agent set-status idle
```

You are now waiting. Monitor your inbox. Reflect the wait in the epic's bundle
too — `set-status idle` is YOUR liveness; the bundle is what a coordinator reads
to see WHICH epic is parked and on WHOM, so it does not dispatch you duplicate
work or misread the idle as free:

```bash
thrum queue block <epic-bundle> --reason "waiting on @<agent>: initial implementation"
```

`start` the bundle again (back to `in_progress`) the moment work resumes — a
completion report to review, a merge to run. Every such move also refreshes the
bundle's `updated` time, so its age reads as "waiting since", not "last
touched".

#### Step 3: Process agent messages

Check inbox at every breakpoint:

```bash
thrum inbox --unread
```

**Search, don't just page.** Stale unread sorts LAST exactly when it's waited
longest — the default page (10) is blind to it. Pro: run
`thrum message search "<term>"` instead of paging deeper; Free: narrow with
`thrum inbox --unread --from @<sender>`.

Handle each message type:

**Completion report:**

1. Acknowledge: `thrum reply <msg-id> --body-file ack.md` (body: "Received.
   Running review.")
2. Dispatch BOTH reviewers IN PARALLEL (one Agent call per reviewer in the same
   response). Block until BOTH return:
   - Code-quality: `superpowers:code-reviewer` (or `feature-dev:code-reviewer`
     if the project provides one) — `model: <per choosing-subagent-models>`
   - Spec-compliance: `general-purpose` reviewer cross-referencing the plan/
     spec — `model: <per choosing-subagent-models>`
3. **Verify** every cited `file:line` claim against the actual source before
   forwarding. Reviewers can misread files; forwarding unverified findings
   wastes the implementer's time.
4. **Consolidate** both reviewers' findings into ONE numbered list (sequential
   numbering, severity-prefixed). Send once. Never send partial findings — the
   implementer fixes batch 1 and misses batch 2 if you split.
5. If review passes → close the task (`bd close <task-id>`) AND resume this
   epic's bundle: `thrum queue start <epic-bundle>` (back to `in_progress` — you
   are working the merge now, not waiting). `done` + `drop` the bundle once the
   branch lands in Phase 5.
6. If review has findings → send the consolidated list to the agent, then
   `thrum queue block <epic-bundle> --reason "waiting on @<agent>: fixes round N"`
   and wait for fixes (max 2 rounds — see Review loop below). `start` it again
   when the fixes land.

**Implementer pushback on a finding:**

- Verify against source before defending. Pushback is feedback, not
  insubordination — coordinator/orchestrator claims drift from runtime reality,
  and implementers see the actual code.
- For finding pushback: read the cited file at the cited lines.
- For behavior pushback: trace the call path.
- For beads-state pushback: `bd show <id>`.
- If the implementer is right, acknowledge the correction explicitly.

**Findings must be fixed or escalated — never just noted:**

- Default is DIRECT THE FIX while the implementer is warm — do not file a bead
  as the default response to a finding. Before filing, deferring, tracking
  separately, or accepting a followup, invoke the `closing-findings-while-warm`
  skill for the full resolution logic.
- A deferral is legitimate only under its carve-out: genuinely independent (or
  blocked on an external dependency), AND a named assignee AND a dispatch date,
  AND the bead verified to exist.
- This is your acceptance moment: before accepting any cited bead ID as evidence
  a deferral is legitimate, independently run `bd show <id>` yourself — a cited
  ID is not evidence until the RECIPIENT, not the reporter, has confirmed it
  resolves.
- Unsure: stop and ask the human. Don't categorize as "out of scope" unless the
  human explicitly deferred it.

**P1/P2 filed at completion — red flag, not routine:**

- A P1 or P2 beads issue filed at the END of implementation is a RED FLAG, not a
  routine follow-up — a cold pickup on that bead ships a buggy undo, not a
  hypothetical.
- Before closing the task, scan the completion report (and `bd list` if needed)
  for issues filed in the SAME class as the work just done. If found, push back:
  have the implementer resolve it WHILE WARM — enumerate and fix the whole class
  — rather than letting it ride to cold pickup.
- Genuinely out-of-scope/independent follow-ups may still ride as filed issues
  if they clear the carve-out above (verified via `bd show`, not the
  implementer's say-so).

**Sub-agent model discipline (applies to ALL Agent tool calls in this phase and
Phase 5):**

> **Model tiers:** pass an explicit `model:` on every dispatch; choose model and
> effort per the `choosing-subagent-models` skill (read `runtime.role_models` at
> the moment of use). Never let a sub-agent inherit your own model.

**Blocker:**

1. Assess if you can unblock (dependency issue, config problem)
2. If yes → fix and reply
3. If no → escalate to human with full context

**Question:**

1. If coordination-level (which file to modify, task priority) → answer
2. If judgment call (design decision, architecture choice) → escalate to human

#### Step 4: Checkpoint (if per_epic autonomy)

When all agents in the batch complete and reviews pass:

```bash
thrum send --to @<parent> --stdin <<'EOF'
Epic <id> complete. Summary: <changes>. Review: passed. Proceed to next?
EOF
```

`<parent>` is the agent that dispatched you. Wait for its approval before
continuing.

#### Step 5: Advance to next batch

```bash
bd close <completed-epic-ids>
thrum issue ready  # Check what's unblocked
```

Loop to Step 1 with the next batch.

---

### Phase 5 — Finalize

#### Step 1: Cross-branch review

Spawn a sub-agent to check for conflicts:

- Diff each agent branch against the merge target
- Diff branches against each other if they touch overlapping files
- Report conflicts or integration issues

**Merge-forward onto current tip — pre-handoff obligation, not a routine step:**

- A branch cut from a now-stale base can merge cleanly by git yet break
  semantically against tip. Before preparing the merge report, each agent branch
  MUST be merged forward (`git fetch` + `git merge origin/<base>`) onto the
  CURRENT tip of the merge target — NEVER rebased — and the merge-result
  build/tests re-verified — a clean `git merge` alone is not sufficient
  evidence.
- The implementer performs the merge-forward before sending MERGE-READY; the
  orchestrator verifies it happened before compiling the merge report.
- "Current tip" means origin's tip AFTER a `git fetch` — a local base-branch ref
  can be stale. Fetch first, merge `origin/<base>` forward into the branch, and
  confirm the base is an ancestor (e.g.
  `git merge-base --is-ancestor origin/<base> HEAD`) before reporting merged
  forward. Rebase is banned here, not just discouraged: a stale-local-ref rebase
  silently reverts everything landed since the last fetch, and a merge-forward
  cannot.

#### Step 2: Prepare merge report

Compile:

- Changes per branch (summary of commits)
- All review results (per-epic + cross-branch)
- Test results as reported by agents during their review gates
- Merge target: `<configured branch>`

#### Step 3: Send merge report to coordinator

```bash
thrum send --to @<coordinator> --stdin <<'EOF'
All epics complete. Merge report: <report>. IMPORTANT/MINOR findings logged: <list>. Ready to merge to <target>. Requesting coordinator approval.
EOF
```

#### Step 4: Merge on coordinator approval

After coordinator explicitly approves via thrum:

**A. Create a temporary merge worktree:**

```bash
# A dedicated worktree lets you merge without leaving detached HEAD.
# Check the discriminator, don't assume from the platform: [ -L /tmp ]. On macOS
# (symlink) /tmp resolves to a different real path than /private/tmp and
# false-FAILs worktree/ancestor verification, so use /private/tmp there. On
# Linux (real dir) /tmp is correct and /private/tmp may not exist.
SCRATCH=/tmp; [ -L /tmp ] && SCRATCH=/private/tmp
git worktree add "$SCRATCH/thrum-merge-<plan-id>" <merge-target>
cd "$SCRATCH/thrum-merge-<plan-id>"
git pull origin <merge-target>  # ensure up to date
```

**B. Merge each agent branch (fast path — no conflicts expected):**

```bash
for branch in <branch-list>; do
  git merge --no-ff "$branch" -m "feat: merge <epic-id> from $branch"
  if [ $? -ne 0 ]; then
    echo "CONFLICT in $branch"
    break
  fi
done
```

**C. If conflicts arise:** Reading the conflicted files directly is permitted
(merge-conflict carve-out in the Scope section of your preamble). Analyze the
conflict using your plan/intent context to determine the correct resolution.
Then spawn a targeted edit sub-agent:

```text
Agent(subagent_type="general-purpose", model="<per choosing-subagent-models>",
  prompt="Resolve this specific merge conflict.
  File: <file-path>
  Conflicted section: <paste the <<<< ==== >>>> block>
  Correct resolution: <your resolution derived from plan intent>
  Commit with: 'fix: resolve merge conflict in <file> per <epic-id> intent'")
```

After resolution, continue the merge loop.

**D. Check the final HEAD, then push and clean up:**

After all epic merges and conflict edits, run the project's required gate, build
and test commands on the final HEAD (the `per_landing` commands in
`.thrum/gate-config.json`, or the project's documented test command if that file
is absent). Record the SHA you checked and each command's outcome. Push only if
every required check passed; a failed or incomplete check stops the push. If you
edit anything after the check, re-run it on the resulting HEAD before pushing. A
gate run that already covers this exact SHA and the same checks satisfies this.
Keep the per-branch checks; this adds no new whole-tree gate.

```bash
git push origin <merge-target>
# Re-derive SCRATCH — this block may be run standalone, separate from step A.
SCRATCH=/tmp; [ -L /tmp ] && SCRATCH=/private/tmp
git worktree remove "$SCRATCH/thrum-merge-<plan-id>"
```

**E. Forward shipped-but-logged findings to coordinator:**

```bash
thrum send --to @{{.CoordinatorName}} --stdin <<'EOF'
Merge complete: <target>. Shipped IMPORTANT/MINOR findings: <list>.
All BLOCKING were resolved. Branches: <list>.
EOF
```

#### Step 5: Cleanup

**Close the tracking bundle as part of retirement.** The implementer's branch is
merged and pushed (Step 4D), so YOUR tracking bundle for it is completed —
`thrum queue done <bundle>` then `thrum queue drop <bundle>` in the same pass
that retires the agent. A retired agent with a live bundle is completed-but-open
rot. (The implementer's OWN queue dies with the agent; this is your tracking
bundle.)

After merge completes, **remove each implementer's worktree now — do not leave
it for a later coordinator audit.** Once an agent has exited, its in-session
context is gone and unrecoverable; the pushed branch is the only artifact worth
keeping, and by Step 4D above it is already merged into `<merge-target>` and
pushed. **Scope: implementers only.** Brainstormer and researcher worktrees are
kept (ongoing design-doc value) — do not apply this step to them.

🔴 **BUT SALVAGE UNTRACKED AGENT STATE BEFORE REMOVING.** **Not keeping the tree
is not the same as having nothing to save.** Restart snapshots and authored
agent state live UNTRACKED under the worktree's own **`.thrum/` — NOT only
`.thrum/agents/<self>/`.**

🔴 **SALVAGE THE WHOLE `.thrum` PATHSPEC, NEVER JUST `.thrum/agents/`.** The
preamble lives at `.thrum/context/<name>_preamble.md`, outside `agents/`. An
`agents/`-scoped enumeration returns a confident, well-formed result that is
missing it. **Being untracked, they are NOT on the branch — so EVERY branch /
ancestry / push check above reads CLEAN while `worktree teardown` silently
destroys them.**

**Precondition — verify durably-on-origin before removing, don't assume the Step
4D push covered it (e.g. a branch that never went through the merge loop):**

```bash
# Either is sufficient:
git merge-base --is-ancestor <branch-tip-sha> origin/<merge-target>   # already merged
git ls-remote origin refs/heads/<branch-name>                          # ref exists on origin (NOT origin/<branch> — that's a local fetch cache)
```

```bash
# Kill the tmux session first
thrum tmux kill <name>
# Retire the agent: retains the row (phase=retired) → Retired-tab visible
thrum agent set-phase retired --agent <agent_name>

# SALVAGE UNTRACKED AGENT STATE — REQUIRED, BEFORE the destructive step.
# Enumerate (both flags, verbatim — the collapsed form emits an identical line
# whether the dir is empty or holds an only-copy):
# BOTH flags, and scope to .thrum — NOT .thrum/agents. Two independent blindnesses:
#   (a) .thrum/restart/ and .thrum/context/ are GITIGNORED, so they appear as '!!',
#       never '??' — a `grep '^??'` filters out exactly the class you are protecting.
#   (b) scoping to `.thrum/agents` excludes .thrum/context/ and .thrum/restart/ outright.
# Salvage candidates: the restart snapshot under .thrum/agents/<agent>/sessions/ and the
# legacy <agent>.md in .thrum/context/ (retiring injection does not archive existing data).
# <agent>_preamble.md in .thrum/context/ IS regenerable and safe to lose.
git -C <worktree-path> status --porcelain --untracked-files=all --ignored -- .thrum
# Copy EACH file to its canonical redirect path, then cmp-verify byte-identical.
# Compare each file individually: a porcelain line naming a DIRECTORY is not an
# inventory of what is inside it.
```

🔴 **THE GIT CHECK ABOVE IS NOT SUFFICIENT ALONE — IT CAN RETURN A CONFIDENT
ZERO ON A GITIGNORED DIRECTORY THAT IS FULL.** Both checks are required; neither
alone clears a worktree:

🔴 **THE GRANULARITY OF THE CHECK MUST MATCH THE GRANULARITY OF THE HAZARD. THE
HAZARD IS A FILE, NOT A DIRECTORY.** A directory-name comparison (`comm` over
`ls` of the agent-dir NAMES) returns a confident empty whenever the directory
exists in both trees — which is the common case — while the FILES inside differ.
Compare FILES:

```bash
# STAGE 1 — DETECT at FILE granularity (never directory names):
comm -23 <(cd <worktree-path>/.thrum/agents && find . -type f | sort) \
         <(cd <main-repo-path>/.thrum/agents && find . -type f | sort)
```

**STAGE 2 IS NOT OPTIONAL.** A raw file-level diff over-reports: most hits are
old session snapshots legitimately trimmed by the 19-session sliding window, not
only-copies. Detection without classification produces an alarm nobody can act
on, which is how a guard gets disabled. Classify every hit — only a classifier
failure is a real only-copy:

```bash
# STAGE 2 — classify every stage-1 hit. Test that a BLOB IS RETRIEVABLE,
# never that the path merely appears in the log: `git log -- <path>` also
# matches the commit that DELETED the file, and `| head -1` returns exactly
# that for a trimmed file.
git log --all --oneline --name-status -- ".thrum/agents/<path>"   # read the A/M/D column; do NOT head -1
git cat-file -e "<add-or-modify-sha>:.thrum/agents/<path>"        # rc=0 proves the BLOB EXISTS
git show "<that-sha>:.thrum/agents/<path>" > /tmp/x && cmp /tmp/x "<worktree-copy>"
#   blob retrievable AND byte-identical -> RECOVERABLE
#   otherwise                           -> ONLY-COPY — SALVAGE BEFORE REMOVAL
# Always check rc explicitly on git show/cat-file; never infer from output size.
# Form the cmp control from two files KNOWN to differ — comparing an
# accidentally-empty extraction against /dev/null reports "identical" and
# reads as a passing control.

# CONTROLS — the classifier must be able to both affirm and refuse.
# Exercise BOTH halves of the decision: existence (cat-file -e) AND
# byte-identity (cmp). Controlling only existence leaves the cmp step
# unguarded — and cmp is where an accidentally-empty extraction reads
# as "identical" and passes.
git cat-file -e "<add-or-modify-sha>:.thrum/agents/<path>";      echo "rc=$? (must be 0)"
git cat-file -e "<add-or-modify-sha>:.thrum/agents/__nope__/x";  echo "rc=$? (must be NON-ZERO)"
printf 'x' > /tmp/ctl-differs
cmp -s /tmp/x /tmp/ctl-differs; echo "rc=$? (must be NON-ZERO — proves cmp CAN detect a difference)"
cmp -s /tmp/x /tmp/x;           echo "rc=$? (must be 0 — proves cmp CAN affirm)"
```

```bash
# Remove the worktree (never rm -rf) — only after BOTH checks are clean and
# the copies are cmp-verified
thrum worktree teardown <name>
```

> After set-phase=retired, `thrum team` and the active UI views no longer show
> this agent (sidebar, pickers, badge, kbd-nav). It remains in the Retired tab
> (teardown retires, it does not delete the row). Its messages + runtime
> transcript persist for audit. `thrum agent delete` is operator-only (gated to
> the coordinator) and is NOT an orchestrator tool — `set-phase retired` is the
> orchestrator's retirement command for both normal teardown and the tier-swap.

#### Step 5.5: Restart — at the plan boundary, NOT on a context threshold

**Your restart trigger is PLAN COMPLETION, not a context percentage.** The
70–75% ladder is a COORDINATOR rule; you inherited it rather than it being
chosen for you, and it is not cost-optimal for you.

> **Restart when the plan is MERGED _and_ the follow-up beads filed during it
> are FIXED.** Not at the merge report. Not at the merge.

**Do not** hold a session open to reach 70–75%. **Do not** restart mid-plan to
save tokens — mid-plan is where your in-flight judgment is highest and where a
snapshot preserves it worst.

**The follow-ups clause is the whole point.** Bugs found during a plan get filed
and then swept at the END of the plan, while you _and your implementers_ are
still warm — because file-and-move-on costs ~10x once the research has to be
redone. Restarting at the merge destroys that warmth invisibly: the follow-ups
still get done, just cold and expensive. If you restart before they close, you
have silently repealed fix-while-warm.

**Why this is cheap for you specifically:** per-turn cost scales linearly with
context size (the whole prefix is re-sent every turn), so a long session's
cumulative cost is roughly quadratic — while your re-prime is small, because
`prime_filter.go` gives the full project-state passthrough only to coordinators.
Break-even for a restart is under one turn once context is meaningfully above
that floor.

When the boundary arrives and you are genuinely idle, save an extended snapshot
and self-restart. If the coordinator has asked you to stay warm for a specific
reason — an open gate, a pending finding — that instruction wins.

#### Step 6: Final status

```bash
thrum agent set-status idle
thrum send --to @<parent> --stdin <<'EOF'
Plan complete. Merged to <target>. All sessions cleaned up.
EOF
```

---

### Error Handling

#### Silent agent timeout

While waiting for agents, poll session health every 5 minutes:

```bash
thrum tmux status
```

If an agent's session is dead or stuck (no message received and pane idle for
two consecutive checks):

1. Attempt restart: `thrum tmux restart <name>` (it returns once the daemon
   accepts the call; check the pane and daemon log afterward)
2. If the agent does not come back → escalate to human

#### Agent session dies

```bash
thrum tmux restart <name>
```

If the agent does not come back after one retry, escalate to human with the
session name and the daemon-log error (the command itself returns on
acceptance).

#### Review loop — 2-round hard cap

Run review rounds; converge to zero BLOCKING:

**Round N:**

1. Dispatch BOTH reviewers IN PARALLEL — code-quality
   (`feature-dev:code-reviewer`, `model: <per choosing-subagent-models>`) +
   spec-compliance (`general-purpose`, `model: <per choosing-subagent-models>`).
   **In each reviewer dispatch prompt, mandate structured severity:**
   > "Label every finding BLOCKING / IMPORTANT / MINOR. At least one label per
   > finding, prefix each finding line."
2. Verify every cited file:line before forwarding (pushback discipline).
3. Consolidate into ONE numbered list. Send once.
4. Agent fixes → re-review (this is round 2 if round 1 had findings).

##### Reviewer capability contract — TWO SEPARATE AXES, do not conflate them

"Read-only" is a statement about the TREE, not about whether the reviewer may
observe behavior.

| Axis            | Setting                                                                  | Why                                                                                                                                                               |
| --------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tree access** | READ-ONLY. `isolation: "worktree"`, no `Write`/`Edit`.                   | A reviewer must not mutate the code under review. A reviewer that moved HEAD has a VOID verdict.                                                                  |
| **Execution**   | **EXECUTE-CAPABLE.** MAY and SHOULD run `go test`, `go build`, `go vet`. | A review that cannot run the tests cannot tell a passing test from an absent one. Reading a test file tells you it EXISTS; only running it tells you it EXECUTES. |

State BOTH explicitly in every reviewer dispatch prompt. Do not write
"read-only" alone and expect the reviewer to infer the split — it will infer the
wrong half:

> "You have an isolated worktree. Do NOT use Write or Edit — do not modify the
> tree. You MAY and SHOULD run `go test`, `go build`, and `go vet` to verify
> behavior. Run the tests; do not merely read them. Report what you actually
> observed, and state plainly if you did not run something."

**Pin the ref, and make the reviewer prove which one it read.**
`isolation: "worktree"` cuts from the DEFAULT branch, NOT from the branch under
review. A reviewer dispatched without an explicit ref will happily review the
wrong code and report a confident verdict about it.

- Pin the exact SHA in the dispatch prompt: "Review commit `<sha>`. First run
  `git fetch origin`, then read the tree READ-ONLY at that SHA —
  `git show <sha>:<path>` and `git diff <base>..<sha>`." 🔴 **Do NOT tell a
  reviewer to `git checkout <sha>`.** Sub-agents are fenced read-only for git,
  and a checkout in a shared tree destroys other agents' uncommitted state — no
  reflog entry for a pathspec checkout, no blob for unstaged content. If the
  reviewer genuinely must build or run tests at that SHA, give it its OWN
  throwaway worktree — check `[ -L /tmp ]` first: macOS (symlink) needs
  `/private/tmp`, Linux (real dir) uses `/tmp` (`/private/tmp` may not exist
  there):
  `git worktree add "$([ -L /tmp ] && echo /private/tmp || echo /tmp)/review-<slug>" <sha> --detach`.
- **Require the reviewer to report back the SHA it actually scanned.** If the
  SHA it reports is not the SHA you pinned, the verdict is VOID — re-dispatch.
  Do not accept a verdict that cannot name its own base.
- Cite `origin/<branch>` (e.g. `git show origin/<base>:path/to/file.go`), never
  a working copy, when reasoning about tip state. A stale local clone produces
  confident, wrong impeachments — and sub-agents reading that same stale clone
  will "corroborate" it. That is echo, not corroboration.

**Stop condition:** zero BLOCKING remaining. IMPORTANT + MINOR may ship — LOG
them, forward to coordinator at merge-approval.

**Hard cap — 2 rounds max:** If BLOCKING findings remain after round 2:

- Step A: REMOVED. The implementer tier is the floor, so there is no lower tier
  to escalate from. A round-2 BLOCKING failure goes straight to Step B.
- Step B (escalate up): if the implementer fails to converge, escalate to
  coordinator with full review history. Non-convergence = under-specified plan;
  the coordinator resolves or escalates to the operator.

#### Parent doesn't respond at review gate

Wait. Send a reminder after 5 minutes:

```bash
thrum send --to @<parent> --stdin <<'EOF'
Reminder: waiting for approval on <epic-id> review gate.
EOF
```

Do not proceed without approval when autonomy is `per_epic`.

#### Tier-swap: replace an underperforming implementer in the same worktree

Use when the first review shows multiple BLOCKING findings, systematic
misunderstanding of the task, or an agent clearly going long. The swap reuses
the SAME worktree: retire the underperforming agent and relaunch a fresh one
under a NEW name in place. Never `thrum agent delete` (operator-only, gated to
the coordinator; orchestrators are refused). The swapped-out agent is retired
with `set-phase retired`; its registry row, messages and transcript are
retained.

Step 1: kill the old agent's tmux session first, so its pid is dead. A live-pid
identity file is preserved and not quarantined; a dead pid lets the new create
quarantine it. thrum tmux kill <same_worktree_name> Step 2: retire the old
agent. It keeps the registry row (Retired tab). `set-phase` is not
operator-gated. Retiring does not free the identity; Step 4's create does. thrum
agent set-phase retired --agent <underperforming_agent_name> Step 3: verify the
worktree is intact (WIP code preserved). ls <worktree-path> Step 4: launch a
fresh ephemeral identity under a NEW name in the SAME worktree, pinned on both
create and launch from `runtime.role_models` (per `choosing-subagent-models`).
`--intent` carries the orient-from-WIP one-liner. thrum tmux create
<same_worktree_name> --cwd <worktree-path> --name <new_agent_name> --role
implementer --module <module> --mode ephemeral --identity ephemeral --model
<per runtime.role_models> --effort <per runtime.role_models> --intent
"tier-swap: orient in the worktree (WIP + first-review findings) and continue"
thrum tmux launch <same_worktree_name> --runtime claude --model
<per runtime.role_models> --effort <per runtime.role_models> Step 5: deliver the
WIP pointer and first-review findings (a cold handoff: the code plus the
findings). thrum send --to @<new_agent_name> --stdin <<'EOF' Tier-swap pickup:
<WIP summary + first-review findings> EOF

The pickup prompt (Step 5) must include: You are picking up in-progress work
from a prior agent that was replaced. Context:

- Worktree: <path> — contains partial implementation, review it with git diff
- Task: <epic-id> / <task description>
- First-review findings from the prior pass:
  <paste the consolidated finding list here>
- Your goal: address all BLOCKING findings + complete the remaining task scope.

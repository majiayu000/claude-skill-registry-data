---
name: flow
description: "Run the whole contract-driven delivery chain end to end in one invocation: intake, design contract, test-first implementation, adversarial review, verification, commit and pull request. Drives the working agent chain (/task, /design-first, /tdd-first, the reviewer agents, /verify-before-done, /git-commit, /ship) and pauses only at the gates a human must answer. Use when: user says /flow, 'run the whole flow', 'take this all the way to a PR', 'do the full autonomous flow', 'end to end', or hands over a request and expects a pull request back rather than a plan. Replaces the Contract Orchestrator scripts, which were removed; see the section at the end."
user_invocable: true
---

# /flow — the contract-driven delivery chain, end to end

One invocation, one delivery. `/flow` runs every stage of the chain in order and stops only
where a person has to decide something.

```
/flow
  └─ /task ─→ /design-first ─→ /tdd-first ─→ reviewers ─→ /verify-before-done ─→ /git-commit ─→ /ship
       │           │                │             │                │                  │           │
     brief      CONTRACT         red then      adversarial      build, tests,       staged      draft
                 GATE (*)         green          agents          drift, gates       commit       PR
```

The contract gate, marked above, is the one stop that can never be automated away.
Everything else runs without asking.

## Context — why this skill exists

Each stage of the chain already has a skill, and each skill already says which one comes
next. What nothing owned was the run itself. An operator who wanted a request carried all
the way to an open pull request had to type seven invocations and carry the handoff shape
between each pair by hand. Where an operator stopped typing, the chain stopped, usually
after the contract and before any code.

`/flow` owns the run. It holds the work item identity across every stage, it knows which
stops are real and which are habit, and it can pick a half-finished run back up from disk
instead of starting over.

**What `/flow` is not.** It does not restate the rules of the stages it calls, and it does
not override them. Every stage skill remains the authority on its own steps. If this file
and a stage skill disagree about that stage, the stage skill wins and the disagreement is
a defect in this file.

## Step 0: Parse the invocation and set the autonomy level

The argument is whatever `/task` accepts: a GitHub issue number such as `#123`, an issue
link, a Jira or Azure DevOps key, free prose, or nothing at all.

Read one optional trailing flag. It sets how far the run goes before it hands back:

| Flag | Runs through | Use when |
|---|---|---|
| *(none)* | The whole chain, ending at a draft pull request | The default, and what most operators want |
| `--to-contract` | Intake and design only, stopping at the approved contract | The design is the deliverable, or the work will be implemented elsewhere |
| `--to-green` | Everything up to a passing test suite, no commit and no pull request | The operator wants to read the diff before anything is recorded |
| `--to-commit` | Everything up to a local commit, no push and no pull request | Work stays on the machine for now |

Announce the parsed target in one line before starting. An operator who meant
`--to-green` and got a pull request has lost something they cannot take back quietly.

## Step 1: Intake

Invoke `/task` through the Skill tool with the argument verbatim.

`/task` produces the Work Item Brief at `.claude/work-items/<date>-<slug>.md`, grades the
item against the active north-stars, sizes it, and creates the branch or the parallel
worktree. Let it do all of that. Do not pre-empt its clarifying questions, and do not
answer them on the operator's behalf.

**Carry two things out of this stage and hold them for the whole run:** the brief path and
the branch name. Every later stage reads the brief rather than a paraphrase of it, and
`/ship` pushes the branch that actually holds the commits.

**`/task` puts the run in a worktree of its own (its Step 1.5), so enter it here and stay in it.** Enter the path `/task` reported with `EnterWorktree`, or confirm the session already stands in it, before any later stage. Every later stage and every subagent runs in that worktree, and each handoff states its path. The main-checkout guard refuses edits to the main checkout, so a stage run there is blocked, not misplaced.

**A subagent handoff ending `BLOCKED: main checkout <target>` halts the run.** It means the guard refused a write because the subagent was launched while the session stood in the main checkout. Do not retry it there and do not write the file elsewhere: enter the run's worktree with `EnterWorktree` and relaunch the subagent.

**Routing.** `/task` sizes the item and picks the route. Honour it:

- **Extra small or small** — skip Step 2 entirely and go to Step 3. For a bug, run `/debug`
  first and let its root cause become the regression test.
- **Medium, large or extra large** — continue to Step 2. This is not negotiable; where a
  concept gate hook is installed it blocks the writes anyway.

## Step 2: Design — and the one human gate

Invoke `/design-first` through the Skill tool, passing the brief path rather than a
retelling of the request:

```
TASK: <brief title>
CONTEXT: Work Item Brief at .claude/work-items/<file>.md — read it first; it carries the
         acceptance criteria, the out-of-scope list and the intake answers. Do not
         re-derive requirements from the chat.
WORK_ITEM: <id> (<url>)
NORTH_STARS: <the grades from the brief, verbatim — or 'none'>
```

`/design-first` dispatches `data-architect` to draft the contract and `contract-critic` to
attack it. Both dispatches are pre-authorized by the `/flow` invocation and are not
separate decisions to put to the operator.

**Then the run stops.** The contract goes to the operator, every open question is answered
by them, every blocker from the critic gets an explicit response, and the operator alone
flips the status to approved. Do not guess an answer. Do not approve a contract. Do not
read silence as agreement.

This is the gate the whole protocol is built around. A chain that approves its own designs
is not autonomous, it is unsupervised.

When the contract is approved, write its path into the brief's `contract:` field and set
`status: designing`. If the target was `--to-contract`, report and stop here.

**On `/design-first` Step 3.5.** That step carries a gate covering the Contract
Orchestrator. Respect it: under `/flow`, always take the traditional workflow and go to
Step 4. The closing section of this file records why.

## Step 2.7: Open the sub-tasks

**Guard, checked first, before anything else in this step, on every entry — a fresh run and a
resumed one alike.** If this run's own brief carries a `parent_issue:` field, this run is one of
the sub-tasks this step creates, not the contract's parent run, and this step never executes for
it. The factory writes the same `status:` value into a sub-task's own brief that it writes into
the parent's, so `status:` alone cannot tell the two apart — `parent_issue:`, the field this
mechanism introduced, is what does. This check belongs here and not only in the resume table
below, because a resumed run is not the only way this step gets reached. Skipping is not
optional: running this step again from a sub-task's own brief would open a second set of
sub-issues against the very contract that already produced this one, which is the failure this
whole design exists to prevent.

Runs once the contract is approved, between the design gate above and implementation below —
it cannot run any earlier, because the sub-task list exists only once the contract does.

**The Parent Branch Delivery Rule.** A contract with two or more mergeable blocks (a review gate counts as one) always gets a parent issue, one sub-issue per sub-task and a landing; nobody chooses that layout. Its parent brief is the one the contract's `**Work Item Brief:**` header names, and its `branch:` is the parent branch that every sub-task is cut from and merged into. This step is also the remedy for `needs-issue`: `/advance` and `pr_merged.py --dispatch` refuse a sub-task that has no sub-issue (exit 7, `error: needs-issue`) before any branch is cut, and the sub-issues this step opens, recorded with `--record-subtask`, are what clears it.

Ask the contract's own script whether it decomposes into more than one deliverable. Never answer
that by re-reading the contract's handoff section — the same rule `/advance` follows for the same
reason: two implementations of one rule will disagree.

**Finding the script, under either install mode** — the identical lookup `/advance` Step 1
already documents, reused rather than restated as a second copy:

```bash
PRM=
S=.claude/scripts/pr_merged.py
if [ -f "$S" ]; then PRM=$S
elif [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then PRM=$CLAUDE_PLUGIN_ROOT/$S
else
  # What Claude Code recorded for this plugin (this project's entry, then the user entry), then the newest cache folder by version number.
  CFG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
  ME=$(printf %s "$CLAUDE_PROJECT_DIR" | tr 'A-Z\134' 'a-z/' | tr -s /)
  REC=$(tr -d '\r\n' 2>/dev/null < "$CFG/plugins/installed_plugins.json" | grep -o '"agentic-auto-improve@[^"]*" *: *\[[^]]*]' | grep -o '{[^{}]*}' | tr '\134' / | tr -s /)
  MINE=$(printf '%s\n' "$REC" | grep '"scope" *: *"project"' | while IFS= read -r O; do
    P=$(printf %s "$O" | sed -n 's/.*"projectPath" *: *"\([^"]*\)".*/\1/p' | tr 'A-Z' 'a-z' | tr -s /)
    [ -n "$ME" ] && [ "${P%/}" = "${ME%/}" ] && printf '%s\n' "$O"
  done)
  NEWEST=$(ls -d "$CFG"/plugins/cache/*/agentic-auto-improve/*/ 2>/dev/null | sed -n 's|^\(.*/\([0-9][0-9.]*\)/\)$|\2 \1|p' | sort -rV | cut -d' ' -f2-)
  PRM=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
    [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
  done)
fi
py -3 "$PRM" --contract <slug> --status --json
```

**If `PRM` comes back empty, stop and say so** — the same halt `/advance` takes, for the same
reason: every rule this step needs lives in that file.

```bash
py -3 "$PRM" --contract <slug> --status --json
```

Read `defects` and `sub_tasks` from the answer and go no further into the contract than that,
with one named exception: `sub_tasks` carries each block's identity and its heading-derived name,
never the block's own body text, because the script's `--status` mode never calls its own body
reader — that reader only runs in the release path, and only for a sub-task already merged.
Each entry in `blocks` also carries `base`, `base_source` and `base_problem`, the branch that
sub-task would be cut from and where that came from; `--status` never refuses for a base.
Where a later step in this section needs the numbered handoff block itself, matching the heading
`sub_tasks` already gave is the one place this step reads the contract directly. No other read
into the contract is licensed here.

1. **`defects` non-empty → report each one, its block and its reason, and stop. Create nothing.**
   Asked first, before the count below, for the reason `/advance` asks it first: a contract whose
   blocks are all malformed parses to an empty task list, and opening tracker records for a plan
   that cannot be delivered makes records for work nobody can do.
2. **`len(sub_tasks) <= 1` → stop here.** No sub-issue, no state-store identity fields, no change
   to Step 3 below. This is the true no-op case, and the discriminator is the script's own
   mergeable count — never a second reading of the contract, and never a heading count taken by
   eye.
3. **`len(sub_tasks) >= 2` → open one sub-task per entry, in ordinal order.**

   Before creating anything:

   ```bash
   gh --version && gh auth status
   ```

   **Unavailable → stop the run and say so.** Do not fall back to running the contract as a
   single block, and do not fall back to cutting branches from the default branch. Either
   fallback produces today's topology while the operator believes they got the new one, which is
   worse than a halt.

   For each sub-task, decide what to do from stored evidence, in this declared order — **never**
   from a title search, because two sub-tasks of one contract can legitimately share a title
   prefix, and a search that matched one would silently skip a sub-task that has none:

   1. **The state store already carries an `issue` for this sub-task** — read
      `state.sub_tasks.<sub-task-id>.issue` off the same `--status --json` answer, not a second
      query — **skip creating it**, and re-verify that stored number's Parent Link before
      trusting it, through the same verifier `/task` uses on its own create, resolved the same
      way:

      ```bash
      VPL=
      S=.claude/scripts/verify_parent_link.py
      if [ -f "$S" ]; then VPL=$S
      elif [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then VPL=$CLAUDE_PLUGIN_ROOT/$S
      else
        # What Claude Code recorded for this plugin (this project's entry, then the user entry), then the newest cache folder by version number.
        CFG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
        ME=$(printf %s "$CLAUDE_PROJECT_DIR" | tr 'A-Z\134' 'a-z/' | tr -s /)
        REC=$(tr -d '\r\n' 2>/dev/null < "$CFG/plugins/installed_plugins.json" | grep -o '"agentic-auto-improve@[^"]*" *: *\[[^]]*]' | grep -o '{[^{}]*}' | tr '\134' / | tr -s /)
        MINE=$(printf '%s\n' "$REC" | grep '"scope" *: *"project"' | while IFS= read -r O; do
          P=$(printf %s "$O" | sed -n 's/.*"projectPath" *: *"\([^"]*\)".*/\1/p' | tr 'A-Z' 'a-z' | tr -s /)
          [ -n "$ME" ] && [ "${P%/}" = "${ME%/}" ] && printf '%s\n' "$O"
        done)
        NEWEST=$(ls -d "$CFG"/plugins/cache/*/agentic-auto-improve/*/ 2>/dev/null | sed -n 's|^\(.*/\([0-9][0-9.]*\)/\)$|\2 \1|p' | sort -rV | cut -d' ' -f2-)
        VPL=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
          [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
        done)
      fi
      py -3 "$VPL" --sub <stored issue> --parent <the parent issue number> --json
      ```

      Anything other than `linked` halts this sub-task — but not "the same way a fresh create's
      own verification would": a fresh create still has `/task`'s own single repair attempt
      available before it settles on a verdict, and this read-back issues no tracker mutation of
      any kind, repair included. The halt here is still correct; it follows because this step may
      make no tracker write at all, not because it mirrors a create that can.
   2. **No state entry, but a Sub-Task Work Item already exists** whose `branch:` field equals
      `task/<contract-slug>/<sub-task-id>` exactly — the same match `/ship` Step 0 already uses to
      find a brief by its current branch — and whose `id:` is resolved → re-verify that brief's
      `id:` against the parent issue before adopting it, through the same verifier point 1 uses,
      resolved the same way:

      ```bash
      VPL=
      S=.claude/scripts/verify_parent_link.py
      if [ -f "$S" ]; then VPL=$S
      elif [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then VPL=$CLAUDE_PLUGIN_ROOT/$S
      else
        # What Claude Code recorded for this plugin (this project's entry, then the user entry), then the newest cache folder by version number.
        CFG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
        ME=$(printf %s "$CLAUDE_PROJECT_DIR" | tr 'A-Z\134' 'a-z/' | tr -s /)
        REC=$(tr -d '\r\n' 2>/dev/null < "$CFG/plugins/installed_plugins.json" | grep -o '"agentic-auto-improve@[^"]*" *: *\[[^]]*]' | grep -o '{[^{}]*}' | tr '\134' / | tr -s /)
        MINE=$(printf '%s\n' "$REC" | grep '"scope" *: *"project"' | while IFS= read -r O; do
          P=$(printf %s "$O" | sed -n 's/.*"projectPath" *: *"\([^"]*\)".*/\1/p' | tr 'A-Z' 'a-z' | tr -s /)
          [ -n "$ME" ] && [ "${P%/}" = "${ME%/}" ] && printf '%s\n' "$O"
        done)
        NEWEST=$(ls -d "$CFG"/plugins/cache/*/agentic-auto-improve/*/ 2>/dev/null | sed -n 's|^\(.*/\([0-9][0-9.]*\)/\)$|\2 \1|p' | sort -rV | cut -d' ' -f2-)
        VPL=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
          [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
        done)
      fi
      py -3 "$VPL" --sub <brief's issue id> --parent <the parent issue number> --json
      ```

      Anything other than `linked` halts this sub-task, for the same narrower reason point 1's
      halt carries. Only on `linked` → adopt that `id:` and `base:` into the state store and
      create nothing. A brief on disk is not a stronger witness than a stored number for being
      newer — if anything it is weaker, since nothing else in this design re-reads or re-checks
      it once written — so it earns the same scrutiny, not less.

      **This step does not reconcile a state entry and a brief that disagree with each other**
      about which issue a sub-task resolves to. By the declared order above, a given sub-task
      only ever consults one of the two, so a live disagreement between them is never visible
      here. What does catch a wrongly adopted number is point 4's roll-up below: an id adopted
      here that the parent's own sub-issue list does not actually carry surfaces there as a
      mismatch.
   3. **Neither** → invoke `/task` through the Skill tool in parent-aware mode, all five fields
      present every time — this mode never triggers on a subset, and a partial set produces
      neither the old path nor the new one:

      ```
      /task <the sub-task's name from its handoff heading>
      PARENT_ISSUE: <the parent issue number, from this run's own brief>
      BASE_BRANCH: <the parent branch, from this run's own brief>
      BRANCH_NAME: task/<contract-slug>/<sub-task-id>
      CONTRACT: <this run's contract path>
      SUB_TASK: <the contract's numbered handoff block, verbatim — the one named exception to
                the "go no further into the contract" rule above>
      ```

      `/task` creates the sub-issue, verifies its own Parent Link, and writes the sub-task's own
      brief. This step issues no tracker command of its own and repeats none of that work — if a
      line here starts to read like `gh issue create`, stop, because every tracker artifact in
      this design comes from `/task` and a create issued from this file duplicates the exact
      thing this feature exists to remove.

      Then find the brief `/task` just wrote — the same `branch:` match used in point 2 above —
      and read its `id:` and `base:` back. Record all three into the state store through the
      script's own writer, never by hand:

      ```bash
      py -3 "$PRM" --contract <slug> --record-subtask <sub-task-id> --issue <n> --base <branch> --brief <brief-path>
      ```

   **A create or its verification fails part-way through the set → halt, and report exactly
   which sub-tasks have an issue and which do not.** Say that re-running this step creates only
   the missing ones. **Do not roll back** — deleting tracker records to tidy a partial run loses
   more than it saves.

4. **Roll up.** Once every sub-task above has been handled, read the parent issue's own
   sub-issue list once and compare it against the sub-issue numbers just created or adopted, in
   both directions. Report the comparison.

   - **A sub-issue this run expected but the parent does not report → halt.** Something between
     creation and this check did not land.
   - **A sub-issue the parent reports that this run did not expect → name it and halt, without
     closing it.** An amended contract is the ordinary way this happens, leaving an earlier
     sub-task the contract has since dropped still open on the parent. Whether that orphan should
     be closed is not this step's call to make on a local belief about the contract's current
     shape; report it and let the operator decide.

   **Finding sub-issues in the issue list.** A sub-issue title carries
   its parent reference. Print `issueTitle.subIssue.format` and `issueTitle.subIssue.legend` from
   the project's `.claude/work-item-conventions.json`; do not restate either from memory.

   - Hide sub-issues from the list: `gh issue list --search "no:parent-issue"`.
   - List one parent's children: the `parentLink.parentListCommand` the conventions file
     declares (cited by name, not restated here).

**No new `status:` value.** Sub-issue creation sits between `designing` and `implementing` in
the brief's lifecycle, but the state store already carries the finer-grained record, and a
seventh status would need every consumer of the existing six updated for a distinction this file
does not need. This is a decision, not an omission.

## Step 3: Implement, test first

**If the contract carries sub-tasks, hand the inner loop to `/advance`.** A contract whose
`## Implementation Handoff` section holds more than one numbered sub-task is iterated a step at
a time, because each sub-task ends in a pull request somebody must merge. `/advance` takes one
step and stops; `/pr-merged` records the merge and wakes it. `/flow` keeps the outer chain.
**A contract with a parent branch is landed by the loop:** once every sub-task has a completion
record, `/pr-merged` hands straight to `/advance`, which starts a background landing script. The
script verifies the parent branch, opens the parent pull request and merges it, with no question
asked. `/flow` then waits for the Landing Report and does not run Steps 5 to 7 for the parent
branch. A single-block contract, the only kind with no parent branch, resumes at verification once
its sub-task has a completion record.

For a contract with a single implementation block there is nothing to iterate, so run it
directly as below.

Invoke `/tdd-first` through the Skill tool with the contract path.

It runs the cycle the protocol mandates. `senior-test-engineer` writes failing tests and no
implementation. The suite runs and has to fail on an assertion, because a failure from a
compilation error or a dependency injection error is not a red state. Then the implementer
agent writes the least code that turns the suite green. The suite runs again, and nothing
that passed before may now fail.

Pick the implementer from the ones the consuming project installs. This plugin ships
`dotnet-backend-architect`, `angular-senior-dev` and `python-ai-developer`; a project may
add its own.

Set the brief's `status: implementing` when this stage starts.

**Two rules that `/flow` must not let slip, because they are what the cycle is for:**

- **Never let an implementer edit a test to make it pass.** If an implementer reports that
  a test is wrong, halt the stage and return to the test author. Silently corrected tests
  are how a suite goes green while the behaviour stays broken.
- **Never accept a green claim without the run.** Redirect the suite output to a log and
  read the exit code. A build that never ran exits zero through a pipe.

If the target was `--to-green`, report the passing suite and stop here.

## Step 4: Review, with fresh agents every time

Dispatch `fullstack-code-reviewer` through the Agent tool against the production code, and
`test-strategy-critic` against the test suite. These review different things and neither
substitutes for the other: one asks whether the code is right, the other asks whether the
tests are worth having.

Add a domain reviewer whenever the diff touches its ground. The reviewers this plugin ships:

| Diff touches | Also dispatch |
|---|---|
| Authentication, credentials, encryption, ownership checks | `security-auditor` |
| Database migrations | `migration-safety-reviewer` |
| Controllers, request or response types, generated client models | `api-contract-reviewer` |
| Queries, repositories, index strategy | `sql-performance-reviewer` |

**A consuming project adds its own rows.** Anything that can move money, send an order,
or touch a regulated surface deserves a dedicated reviewer, and only the project knows
which paths those are. Record those rows in the project's own copy of this table.

Dispatch independent reviewers in a single message so they run at the same time.

**Every review pass gets a new agent.** For a second pass after fixes, dispatch a fresh
instance rather than messaging the one that already reviewed. The earlier instance carries
its own findings and the implementer's reasoning, and both bias the second look. A clean
re-review needs a cold context, and one extra dispatch is cheaper than a missed regression.

The main session never reviews its own implementers inline. Prose saying the diff looks
fine does not satisfy this stage.

## Step 5: Verify

**A contract with a parent branch is not verified here.** Its landing script runs the scripted
verification on the merged head (see the landing section of `/verify-before-done`), and `/advance`
starts that script. This step still applies to each sub-task's own branch and to any single-block
contract, which has no parent branch.

Invoke `/verify-before-done`. It runs the builds, the test suites, the generated-model
drift check, the migration safety check, the safety-critical review gate, the handoff
completeness check and commit hygiene, then reports a verdict.

Set the brief's `status: verifying`.

**A failure here ends the stage and sends the run back.** Do not carry a failing verdict
forward with a note promising to fix it later. That is the single behaviour this gate
exists to prevent.

Two traps worth naming, because both have produced false green runs:

- **A green run has a shelf life.** It expires the moment a parallel agent writes to the
  tree. If anything was dispatched after the suite ran, run it again.
- **Read the exit code, never a tail of the output.** A command that never ran can still
  end a pipeline quietly.

## Step 6: Commit

`/verify-before-done` fires its commit step on its own when the verdict is ready. It stages
the working copy, drafts a commit message in the project's style, and asks once before
committing.

Let that ask reach the operator. Committing is a recorded act, and `/flow` does not hold
an authorization for it.

If that step does not fire, invoke `/git-commit` instead and let it run its own staging and
confirmation.

**Stage narrowly.** Other sessions may share the working tree, and a whole feature
belonging to somebody else can appear mid-run. Verify that what you stage is what this run
produced.

**Stage this run's own files too.** Staging narrowly protects other sessions' files. It must never strand this run's own. They are the brief's status and pull request edits, journal entries, reviewer memory notes under `.claude/agent-memory/`, orchestrator result records and review reports. Include each one in this commit when it exists, or leave it for Step 8, which commits it. A file this run wrote that ends up in neither is a defect.

If the target was `--to-commit`, report and stop here.

## Step 7: Ship

**A contract with a parent branch is landed by the loop, not shipped from here.** `/advance` starts
the background landing script, which opens the parent pull request and merges it after its own
children-closed check. Do not invoke `/ship` for that parent branch. The rest of this step covers a
branch that is not landed that way: a sub-task's own branch, a single-block contract (which has no
parent branch), and a parent pull request somebody opens by hand.

**Before invoking `/ship`, check whether this run is the parent of any sub-tasks.** Step 2.7
already answered this once, but ask again here: the run may have taken hours or days to reach
this point, and a child sub-task can still be sitting open.

**If this run's own brief carries no issue, skip this whole check and proceed to `/ship`
unchanged.** A brief with no issue has no children by definition, and querying a tracker record
that does not exist returns an error with no defined outcome — never read that as "no children
open."

Otherwise, read the child list with the command `.claude/work-item-conventions.json` names at
`issueLink.parentLink.parentListCommand`, filling in this run's own `id:` from the brief for the
placeholder that key uses. That key is the single source of truth for this query — do not write
a second copy of it here, and on any disagreement between this section and what that key names,
the key governs. Read each child's `state` in the casing that command's own JSON actually uses: a
`gh issue view --json` call reports state as `OPEN` / `CLOSED`, nested under
`.subIssues.nodes[]` — not the lowercase `open` / `closed` a `gh api .../sub_issues` call would
report for the identical children. The two `gh` forms are not interchangeable, and a check
written against the wrong one passes with every child open, which is the exact failure this step
exists to prevent. Confirm the casing against the live tracker before trusting either form.

**The query itself can fail** — `gh` missing, the token expired, the network down, or the
request erroring outright. This step runs long after intake, which is exactly when a token can
expire. Check the tool first, the way Step 2.7 already does, and **halt the run and say so** if
the command errors or returns no valid JSON. Reading a failed or unreachable query as "no
children open" would ship the parent pull request with every child still open and report
success — worse than having no gate here at all.

**An empty list is the single-block case and every ordinary item's case alike — proceed to
`/ship` exactly as below, unchanged.** A non-empty list means this run is a parent, whether or
not Step 2.7 ran in this same session — a run resumed straight from a stored `id:` reaches this
same check.

**Any child reporting `state: OPEN` → refuse to invoke `/ship`.** Report which sub-issues are
still open and stop. Do not push, do not open the pull request, and do not report a partial
success. Read the children from the parent issue itself, never from the state store, so a
sub-task somebody merged by hand outside this run still counts. This is the one gate this
mechanism adds to a step that otherwise does not change, and it is what stops the parent pull
request from merging while work beneath it is still open — the same merge that, through the
linked branch cut back at Step 1, would otherwise auto-close the parent issue regardless of
intent.

**Every child reporting `state: CLOSED`, or no children at all → proceed.**

Invoke `/ship`. It re-runs the verification gate, commits anything outstanding, pushes the
branch from the tree that holds the commits, and opens a draft pull request linked back to
the work item.

Pushing and opening a pull request are outward-facing. `/ship` confirms before it acts and
`/flow` does not waive that confirmation.

Set the brief's `status: shipped` and write the pull request link into its `pr:` field.

**That edit is made after the push, so it is uncommitted by construction.** Commit it on the same branch and push again before reporting done. When `/ship` asks for its confirmation, tell the operator this second commit follows, so one confirmation covers both pushes. Then run Step 8.

## Step 8: Close out, leaving nothing behind

A run is not finished while any file it wrote is uncommitted. Every file this run, or an agent it dispatched, wrote ends in one of two states: pushed, because history needs it, or deleted, because it does not. Run this step after Step 7, and again whenever a run is resumed at `shipped`.

1. **Find the files.** Run `git status --short` in every tree the run touched: the worktree, and the tree the run started from. Agents write into whichever checkout they run in, so the starting tree is the one that collects strays.
2. **Sort each file.**
   - **History needs it** (the brief, journal entries, reviewer memory notes, orchestrator result records, review reports, contracts): commit and push. If the run's branch has already merged, use a small follow-up branch from freshly fetched `origin/master` and open a draft pull request. **For orchestrator result records of a contract, single-sub-task contracts included, and for a multi-sub-task contract's other files, that branch is the one stable `docs/<contract-slug>-records`, under the same rule as `/pr-merged` Step 3:** fetch `origin/docs/<contract-slug>-records` first. When it exists, commit on top of it and push without force. Cut it from freshly fetched `origin/master` only when it is absent, and never re-cut it while it exists. The landing reads records from that branch, so a second records branch for the same contract would hide records from it. On the completion move, `/pr-merged` pushes that branch itself, without a prompt, before it hands to `/advance`; this step does not defer it.
   - **History does not need it** (machine-regenerated files such as the contract accuracy log, changes that differ only in line endings, copies of files already on master or in this run's commit, scratch files): delete it, or restore the tracked file, and state why.
   - **Another session's file:** leave it and name it in the report.
3. **Prove before deleting.** Delete a file only after showing it is preserved or worthless: compare it with the committed or master copy, ignoring line endings, and report the result. A file that exists nowhere else is never "not needed".
4. **A move is copy, verify, delete.** Copying a file into another worktree leaves the original behind, which is the defect this step exists to remove.
5. **Report one line per file:** its path, what happened to it, and why. The run is finished only when `git status` in every touched tree shows nothing but another session's files.
6. **Sweep the result records.** After the push, run `py -3 "$PRM" --contract <contract-slug> --sweep-records --from <starting tree> [--removed <a tree this step removed>] --json` (resolve `PRM` as `/pr-merged` does) and print its `tree_lines` verbatim. The sweep is the deleter for result records: it removes a copy only when its twin is on origin or on the stable branch's tip under an open pull request, and keeps and names the rest. Step 8's own "prove before deleting" rule still covers every other file.

Pushing is outward-facing, so confirm once with the full list of what will be pushed and what will be deleted. That confirmation covers the records only. When the records come from a writing run that flipped a contract and memory capture is enabled with candidates, the separate capture question of `/pr-merged` step 5a is asked after that run and before this step commits the brief, so the brief goes in with its receipts.

## Where the run stops, and where it does not

The distinction matters more than any other part of this file. An operator who cannot
predict where the chain pauses will either sit watching it or walk away at the wrong time.

**Pre-authorized by the `/flow` invocation — never ask:**

- Dispatching any agent named in this file, including the design and critique agents
- Moving from one stage to the next once that stage's gate has passed
- Creating the branch or the worktree, and entering it
- Writing and rewriting the Work Item Brief and its status field
- Running builds, test suites and the verification gauntlet
- Re-running a stage after a failure, within the retry budget below

**Always the operator's call — never assume:**

- Approving a concept contract, and answering each of its open questions
- Responding to a critic blocker, whether by fixing it, deferring it or rejecting it
- Accepting a conflict with an active north-star
- The commit confirmation, the push, and opening the pull request
- Anything destructive against a database, which the guard hooks block regardless
- Widening the scope past what the brief's acceptance criteria say
- The memory applicability question in `/design-first` Step 1.5, asked only when memory is enabled and items came back
- The memory capture question of `/pr-merged` step 5a, asked once and only after the writing run that flipped, and only when memory capture is enabled and candidates exist

**Retry budget.** A stage may be retried twice. On the third failure, stop the run, write
what failed into the brief under a `## Run log` heading, and hand back. A chain that
retries forever burns an afternoon and reports nothing.

## The three layers, and which one owns iteration

`/flow` is the outer layer. It is worth knowing what sits beneath it, because the middle layer
is real in the design and gated in practice.

| Layer | Owner | Owns |
|---|---|---|
| Outer chain | **`/flow`** | One work item, from intake through to shipped |
| Inner loop | **`/advance`**, with `/pr-merged` | Iterating the pending sub-tasks of one contract, one step per merge |
| Sub-task phase | `/pr-merged` | Closing one sub-task once its pull request merges |

**Today `/flow` covers the outer layer and drives implementation through agents,** because the
inner loop cannot execute a sub-task. When the loop is repaired, `/flow` hands the inner
iteration to it and keeps the outer chain. Nothing about the outer chain changes.

`/pr-merged` works under either arrangement. It closes a sub-task and returns the released set
to its caller. The loop calls it when a loop is running, and a person calls it when one is not.

## Resuming a run

`/flow` is resumable because the Work Item Brief records where the run got to. Invoke
`/flow` with the brief path or the issue number and read the `status:` field:

| `status:` | Resume at |
|---|---|
| `intake` | Step 1, finish clarification |
| `clarified` | Step 2, design |
| `designing` | Step 2's gate — the contract exists but is not approved |
| `implementing` | Step 3, and re-run the suite before trusting any earlier green |
| `verifying` | Step 5 |
| `shipped` | Nothing to do; report the pull request link |

**A run can also be resumed by a merge.** When a contract's work is split across sub-tasks,
one sub-task often waits for another to land in the default branch. Nothing watches for that.
Tell the session with `/pr-merged <numbers>`. It confirms the merge with GitHub, records the
finished sub-task, works out which sub-tasks that releases, and continues them.

**`shipped` means the work is delivered, not that the tree is clean.** The merge and `/pr-merged` write files after the push: the brief's final status, completion records and state store changes. Before reporting the pull request link, run Step 8 of `SKILL.md`, the closing check. Anything it finds is pushed or deleted, with a reason, before the run counts as finished.

**A `shipped` run whose brief's `pr:` link reports merged is closed by the script, not by hand.** The order is fixed, and it follows `/pr-merged`'s `references/contract-completion.md`, with Step 8's confirmation as the one confirmation for the records. First run `/pr-merged` with `--pr <that link>` and `--dry-run`, which writes nothing. When the script then reports that link as the only known delivery candidate (the move `delivery-unrecorded`), dry-run it again with `--record-delivery`: that is pre-authorized for the brief's own `pr:` link and for no other pull request. A `pending` dry run still reaches Step 8's confirmation, because the confirmation is what clears a blocked report and records a skipped check. Only an `unverifiable` verdict and the exit codes 2, 9 and 10 stop the run before it. After the owner answers, make ONE writing run (the same commands without `--dry-run`) carrying every `--owner-resolved` and `--skipped` flag; a second writing run, such as a `--pr` run plus a `--record-delivery` run, carries the same flags. The script says whether the contract is finished and lists the tracked files each writing run wrote in `written_files`; hand the union of those lists to Step 8 of `SKILL.md` instead of committing from `/pr-merged`, and let Step 8's confirmation cover the records pull request on `docs/<contract-slug>-records`. Step 8's confirmation stays BEFORE the writing run and is unchanged; when memory capture is enabled and candidates exist, one separate capture question follows the writing run that flipped (`/pr-merged` `references/contract-completion.md`, step 5a, which sends the confirmed candidates with its stop rule and records the receipts in the brief), and Step 8 commits the brief only after the receipts are recorded. No outcome of capture blocks the records pull request.

**Re-read the brief on resume rather than trusting the conversation.** A resumed run is
usually a new session, and the tree has moved since. Check the branch, check the worktree
path, and confirm the file list the brief names still exists before acting on it.

## The inner loop, and the design that was removed

`/advance` and `/pr-merged` are the inner loop. Nothing else is.

An earlier subsystem claimed that job — eight scripts under `.claude/scripts/`, with names
beginning `orchestrator_` plus `execute_contract.py`. **They were removed on 2026-09-14.**

They never worked. The planner never parsed a contract, so every run produced zero sub-tasks,
and an empty set satisfied the completion test. A run therefore printed that the contract was
complete having written no code. No session was ever launched; that call sat commented out.
Its own thirteen-test suite passed without once calling the planner.

Three hazards came with it. It opened real tracker issues before doing any work. Its merge
step acted on whichever tree it was started from. Its dependency gate failed open, releasing a
sub-task whose parent had not merged.

**It was a different loop, not a broken version of this one.** It merged locally and never
pushed, so it had no review surface and no person in the loop. This design integrates by pull
request, which is why a person merges every sub-task.

The design record is kept, with a README stating plainly that it is a record rather than code.
Read it before rebuilding anything: the one capability it had and this design does not is an
isolated session per sub-task.

## Anti-patterns (halt immediately)

- **Approving the contract yourself,** or reading silence as approval. The gate is the
  protocol; a chain without it is unsupervised, not autonomous.
- **Asking permission for a stage transition the invocation already authorized.** It
  strands a run mid-chain and makes the operator type what they typed already.
- **Skipping intake because the request looks clear.** Requests that look clear are the
  ones that ship the wrong thing, which is why `/task` exists.
- **Letting an implementer edit a test to reach green.** Halt and return to the test author.
- **Believing a green suite you did not watch run.** Read the exit code.
- **Carrying a failed verification forward** with a promise to fix it after the pull
  request. The gate exists precisely to stop that.
- **Re-using a reviewer agent for a second pass.** Its context is already primed.
- **Running the Contract Orchestrator,** or presenting it to the operator as a working
  option. See the section above.
- **Widening scope mid-run** because a stage surfaced something adjacent. Finish the item,
  record the adjacency in the brief, and let the operator decide whether it becomes work.

- **Ending a run with uncommitted files from that run.** Each file is pushed, because history needs it, or deleted with a stated reason, because it does not. Step 8 is the check, and a report of "done" before it passes is wrong.

## When NOT to use this skill

- Pure research, code reading, or a question with no deliverable. Answer it.
- A single trivial edit, such as a typo, a log line or a version bump. Just make it.
- Work already mid-chain. Resume it from the brief rather than re-running intake.
- When the operator asked for one specific stage. Run that stage, not the chain.

## Skill integrations

- **Composes** `/task`, `/design-first`, `/debug`, `/tdd-first`, `/verify-before-done`,
  `/git-commit` and `/ship`, in that order, without restating or overriding any of them.
- **Dispatches** `data-architect`, `contract-critic`, `senior-test-engineer`, the
  implementer agents, `fullstack-code-reviewer`, `test-strategy-critic`, and whichever
  domain reviewers the diff calls for.
- **Reads and writes** the Work Item Brief at `.claude/work-items/`, which is what makes a
  run resumable across sessions.
- **Hands the inner loop to** `/advance`, which moves a contract one sub-task at a time.
- **Pairs with** `/pr-merged`, which closes a sub-task and wakes `/advance`.
- **Replaces** the removed orchestrator scripts; their design record is at
  `.claude/orchestrator/`.

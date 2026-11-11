---
name: review-rounds
description: Run one review round of CLAUDE.md on this branch
argument-hint: <base> <round> "<criteria>" [--review-only] [--baseline]
allowed-tools: Bash(target/debug/xtask review *)
---
!`target/debug/xtask review start $0 $1`

The lines above are the output of `xtask review start`.  This skill runs one review round of `CLAUDE.md` on this branch.  Do the steps below in order.

## Arguments

* The base is `$0`.  The `base:` line above gives its merge base with `HEAD`.
* The round is $1.
* The criteria are: $2
* The flags are in the argument string `$ARGUMENTS`.  A flag is given only if it is a word of that string:
  * `--review-only`: stop after step 9.
  * `--baseline`: also run the `baseline` agent (steps 2, 5 and 7).

## Before the steps

* Run this skill only after `cargo run -p xtask -- check --tier push` and `cargo build -p xtask` pass.
* A refusal of `review start` (exit 3) stops the skill before this text.  Claude Code shows its lines, such as "commit first", in the session.  A `claude -p` run in text mode shows nothing.
* A `warning:` line of `review start` does not stop the round.  Copy it to the findings file (step 9).
* `allowed-tools` lets the `xtask review` commands run with no approval only in the turn in which the skill loads.  A new turn ends that permission.  A message of a person starts a new turn.  So does the notice that a background agent or command ended.
* The notices of the background reviewers and of the mutants run start new turns.  So in the default permission mode, `review check` of step 8 asks for approval once in each round.  A late `review mutants` can also ask for approval.  `review log-check` and `review clean` of step 11 also ask once in each round.  They run after the findings file, so the counts of the round do not include them.  Approve each one once.  Do not approve with "don't ask again".  That changes the local settings file of Claude Code, and then `review check` fails the round.
* In an agent-run phase, "the person" in this skill is the orchestrator.
* If you are a subagent, do not give your final answer before the last step that you do.  Your run ends with your final answer, and a nested agent or a background command then has no reader.
* Do not pass `model` or `effort` to the Agent tool.  The agent file decides them (decision 0025).
* If the Write tool refuses a file of this skill to a subagent, do not write it in another way.  Give the path and the whole text of each such file in your final answer.  Also say at which step you stopped.
* In that case, keep the text of each refused file, and go on.  Do the fixes and the commit of step 10.  Do step 11 up to the log, and write the log's text.  Leave the approvals fields as step 9 wrote them.  If you can write a scratch file, run `target/debug/xtask review log-check` on a copy of the log there.  Then stop.  With `--review-only`, stop after step 9.
* The caller writes each file at its path.  Also give the command `target/debug/xtask review clean $1` in your final answer.  The caller runs it after it writes the files.  If the caller writes the log, it runs `target/debug/xtask review log-check <run>/log.md` before `review clean`.  Then the caller decides the next step: the next round, or the steps after the last round.

## Names

Take each value from the lines of `review start`.  Do not make a path from the branch name, because `review start` writes `/` in a branch name as `-`.

* `<run>`: the absolute path on the `run folder:` line.
* `<target>`: the absolute path on the `target folder:` line.
* `<base>`: the full SHA on the `base:` line.
* `<since>`: the full SHA on the `since:` line.
* The branch route: the reviewer lines below the line `branch <base>..<head>:`.
* The since route: the reviewer lines below the line `since <since>..<head>:`.  The line "no changes" means that the since range is empty.
* The reasons of a reviewer: the text after its name and the colon on its line of a route, in `<run>/$1/route.txt`.  That file holds the lines of the two routes with all their reasons.  The lines above show at most 5 paths of a reviewer, then "(+n more)".

The round's folder is `<run>/$1`.  `review start` wrote `branch.diff`, `since.diff`, `route.txt` and `state.json` there.  The mutants run writes `mutants.txt`, `missed.txt`, `known.txt` and `mutants.out/` there.  Step 9 writes the findings file `<run>/$1/findings.md`.  The log of the branch is `<run>/log.md`.

## Steps

### 1. Start the mutants run

Run this command with the Bash tool, with `run_in_background: true` and `timeout: 3900000`:

```bash
target/debug/xtask review mutants $1
```

The tool result comes at once.  The command stops itself after 60 minutes.  When it ends, it prints one line, and writes the line to `<run>/$1/mutants.txt`.  The notice that the command ended holds the line.  Do not wait for it now.  If the command refuses to run (exit 3), it prints an error line, no `mutants:` line, and no `mutants.txt`.

### 2. Start the baseline (`--baseline` only)

Start the `baseline` agent in the same message as the reviewers of step 3.  Its range is `<base>..HEAD`.  Fill in this prompt template, and give the agent only that text:

```text
Review this commit range as your instructions say.

Range: <base>..HEAD
Criteria: $2
Round: $1
Target folder: <target>
```

### 3. Start the reviewers

The six reviewers are `reviewer`, `gpu-reviewer`, `memory-reviewer`, `wire-reviewer`, `supply-chain-reviewer` and `docs-reviewer`.  Choose the reviewers and their ranges:

* Round 1: start each reviewer of the branch route.  The range of each is `<base>..HEAD`.  Its reasons come from the branch route.
* Rounds 2 and 3: start `reviewer` on `<base>..HEAD`, with its reasons from the branch route.  Also start each other reviewer of the since route on `<since>..HEAD`, with its reasons from the since route.  If the since range is empty, start `reviewer` only.
* From round 4:
  * Start each reviewer of the since route on `<since>..HEAD`, `reviewer` included.
  * Its reasons come from the since route.
  * It reads the fix range and the files that it touches (decision 0024).
  * If the since range is empty, start no reviewer.  The round has no findings, so it is the last round.

Start each reviewer, and the baseline, in one message.  Use the Agent tool, with `subagent_type` set to the name of the reviewer.  Each one is a new subagent.  Never start a fork, because a fork gets your context.

Fill in this prompt template for each reviewer, and give the reviewer only that text.  Do not add your reasoning, or anything from an earlier round:

```text
Review this commit range as your instructions say.

Range: <the range of the reviewer>
Criteria: $2
Reasons of the route: <the reasons of the reviewer>
Round: $1
Target folder: <target>
```

From round 4, put this line after the `Range:` line of the template:

```text
Scope: read the diff of the range and the whole of each file that it touches.  Do not review the rest of the branch.
```

A change to `.claude/agents/` reaches the agents only in a new session.  The `Scope:` line reaches them in any session.

### 4. Collect and merge the findings

Wait for each reviewer, and for the baseline with `--baseline`.  A background agent gives its output in the notice that it ended.  A foreground agent gives its output in its tool result.  For each agent, record the total tokens and the duration of its `<usage>`.

Each finding of a reviewer is one block with the fields `severity`, `kind`, `where`, `rule`, `claim`, `evidence` and `fix`.  "No findings" gives no block.  Merge the blocks:

1. Two blocks are the same finding when they have the same `where` and the same claim.  The same `where` is the same file, at the same line or in the same function.  The same claim is the same defect, in other words.
2. Merge each set of blocks that are the same finding into one finding.  Its sources are each reviewer that reported it.  Its severity is the highest severity of the blocks: `blocker`, then `should-fix`, then `nit`.
3. Give each finding the ID `$1-<n>`, with `<n>` from 1.
4. Do the `repeat-of` check:
   * Read `<run>/<r>/findings.md` for each round `<r>` below $1.  Find each finding there with the verdict `refuted`.
   * Also read `<run>/log.md`, `docs/reviews/<branch>.md` and each `docs/reviews/<branch>-m<n>.md`.  `<branch>` is the last part of the `<run>` path.
   * Find each row of these logs whose Action is a TD ID or `known: <TD>`.  Skip a TD that `docs/tech-debt.md` lists under `## Closed`.
   * If a finding of this round is the same finding as a `refuted` one, give it `repeat-of:` and the ID of that finding.  Give it the verdict `refuted`.
   * If it is the same finding as a row with a TD, give it `repeat-of:` and that TD.  Give it the verdict `known`.  Its action in the log is `known: <TD>`.
   * From round 4, also find each row of `<run>/log.md` whose Action is `reported, not fixed`.  It can be a row of any earlier round, a nit of rounds 1 to 3 included.  Read no other log for these rows, since a row of another log can have the same ID.
   * A finding of this round that is the same finding as such a row is a reported repeat, unless one of these is true:
     * its severity is higher than the row's;
     * it names a strict rule that the row's Rule cell does not name;
     * its sources include `cargo-mutants`, and the row's Reviewers do not.
   * Give a reported repeat `repeat-of:` and the ID of that row.  If more than one such row fits, use the row of the latest round.  If that row's Repeat of holds an ID, use that ID.
   * A reported repeat that is a blocker or should-fix gets the row's verdict and Significant value.  A nit keeps the verdict `unvalidated` and `-`.  Its action in the log is `reported, not fixed`.
   * If one of the three is true, the finding is a new finding.  Give it no `repeat-of`.  Steps 5 and 6 validate it as any finding.
   * A finding with `repeat-of` gets no validator.
5. Keep the baseline's findings in a separate list.  Merge them only with each other.  Give each the ID `$1-b<n>`, with `<n>` from 1.
6. If a baseline finding is the same finding as a reviewer's finding, give it `same-as:` and the ID of the reviewer's finding.

### 5. Validate the findings

Start one `validator` for each of these:

* each `blocker` and `should-fix` of the reviewers, with no `repeat-of`;
* each `blocker` and `should-fix` of the baseline, but not one with `same-as` a finding that has a validator.

A baseline finding with `same-as` a finding that has a validator gets the verdict of that finding, from its validator.  Each other `nit` gets the verdict `unvalidated`, with no validator.

Start the validators in one message, at most 15 at once.  If there are more than 15, start them in batches of 15.  Start the next batch when each validator of the last batch has ended.  Use the Agent tool, with `subagent_type` set to `validator`.

The range of a finding is `<base>..HEAD` if a source of the finding reviewed that range, or the finding is the baseline's.  Else it is `<since>..HEAD`.  Fill in this prompt template for each finding, and give the validator only that text:

```text
Validate this finding as your instructions say.

ID: <the ID of the finding>
Finding:
<the block of the finding: severity, kind, where, rule, claim, evidence and fix, as a source reported it>

Range: <the range of the finding>
Criteria: $2
Round: $1
Target folder: <target>
```

Each validator gives one block with the fields `id`, `verdict`, `evidence` and `reason`.  Record the verdict of each finding, and its evidence in a few words.  Record the tokens and the duration of each validator from its `<usage>`.

Wait for each validator before step 6.  Step 6 takes its wait for the mutants run off the wall minutes, so that wait must not overlap a validator.

### 6. Validate the missed mutants

1. If the notice that the mutants command ended has come, the wait for it is 0 seconds.  Else, run `jq -n now`, and record its output as the start of the wait.  Then wait for the notice.  When it comes, run `jq -n now` again, and record the end of the wait.
2. Read the mutants line in the notice.  If the notice does not show it, read `<run>/$1/mutants.txt`.  Read that file only after the notice has come, because the run writes the file when it ends.  The line starts with `mutants: full:`, `mutants: partial:` or `mutants: none:`.  If the notice shows no `mutants:` line and the file does not exist, the command refused to run.  Then record its error line as the mutants line, and go to item 9.
3. Read `<run>/$1/missed.txt` and `<run>/$1/known.txt`.  If neither file exists, the run is from an older `xtask`.  Then read `<run>/$1/mutants.out/missed.txt` as `missed.txt`.  If both files are empty or missing, go to item 9.
4. Each line of `missed.txt` becomes a finding with the next ID `$1-<n>`.  Its source is `cargo-mutants`, its severity `should-fix` and its kind `weak-test`.  Its `where` is the file and line at the start of the line.  Its rule is `VERIFY-1`, and its claim is "no test fails with this mutant", with the line.  Make no finding of a line of `known.txt` in this item.
5. Each line of `known.txt` becomes a finding with the next ID `$1-<n>`.  Its fields are those of item 4, from the text before the tab.  Its verdict is `known`, and its `repeat-of` is the TD after the tab.  It gets no validator.  Its action in the log is "known: <TD>".
6. Do the `repeat-of` check of step 4, item 4, for each finding of item 4.  A finding whose `repeat-of` is a `refuted` finding gets the verdict `refuted`.  A finding whose `repeat-of` is a TD gets the verdict `known`, and its action in the log is "known: <TD>".  A missed mutant is a reported repeat only of a row whose Reviewers name `cargo-mutants`.  It gets the row's verdict and Significant value, and its action in the log is `reported, not fixed`.  None of these gets a validator.  Leave its line out of the validator's prompt.  If no line is left, go to item 8.
7. Start one `validator` with this prompt template, filled in.  The prompt holds each line that has no `repeat-of`.  The range is `<since>..HEAD`, because the mutants run tests the since diff:

   ```text
   Validate these missed mutants as your instructions say.  Give one block for each line, with the line as its id.

   Missed mutants, from cargo-mutants:
   <each line of missed.txt with no repeat-of>

   Range: <since>..HEAD
   Criteria: $2
   Round: $1
   Target folder: <target>
   ```

   The verdict of each of these findings is the verdict of the validator for its line.
8. If a finding of a reviewer and a finding of item 4 are the same finding, as step 4 says, merge the two.  The merged finding keeps the reviewer's ID, and gets `cargo-mutants` in its sources.  Its rule also names VERIFY-1.  If its two verdicts differ, it keeps `confirmed` or `pre-existing` over the others.  If the reviewer's finding is a reported repeat of a row whose Reviewers do not name `cargo-mutants`, the merged finding is a new finding.  It loses its `repeat-of` and the values that it copied from the row.  Its verdict is the verdict of the finding of item 4.
9. Run `jq -n now`, and record the output as the end of the round.  Run `jq .started <run>/$1/state.json` for the start of the round.

### 7. Compare with the baseline (`--baseline` only)

A finding is found when its verdict is `confirmed` or `pre-existing`.  If the baseline has no found finding, skip this step.  Record "of 0 baseline findings, the round found 0".

Else start one new subagent with `subagent_type` set to `general-purpose`.  Fill in this prompt template, and give the subagent only that text.  List A holds each found finding of the baseline.  List B holds each found finding of the reviewers and of cargo-mutants, and each `known` finding.  Give each finding as its ID, its `where` and its claim:

```text
Compare two lists of review findings.  Use only the two lists below.  Do not read files, and do not run commands.

List A holds the found findings of a baseline review.  List B holds the found findings and the `known` findings of a review round on the same commit.

For each finding in list A, find a finding in list B that reports the same defect at the same place.  A finding in list B can match more than one finding in list A.

Give one block for each finding in list A:

id: the ID of the finding in list A
mark: found or missed
match: the ID of the matching finding in list B, and a quote of its claim; or none
reason: one sentence

List A:
<the found findings of the baseline: ID, where and claim of each>

List B:
<the found findings and each `known` finding of the round: ID, where and claim of each>
```

Record the mark of each baseline finding, with the match.  Count x, the baseline findings marked `found`, and y, all found baseline findings.  Record "of y baseline findings, the round found x", with the numbers.

### 8. Check the state of the repo

Run this command:

```bash
target/debug/xtask review check $1
```

* If it prints "no change", go to step 9.
* If it exits 3, stop.  Do not write findings.  Give the person each line of its output.  Its lines name each change since `review start`.
* If the only change is to the local settings file of Claude Code, from an approval with "don't ask again", the person confirms that change.  Then the person starts the round again.

### 9. Write the findings

Write `<run>/$1/findings.md` with the Write tool, in the form below.  If the Write tool refuses it, do as "Before the steps" says.

```markdown
# Review round $1

* mutants: <the mutants line, as the command printed it>
* base: <base>; since: <since>; criteria: <the criteria>
* flags: <the flags, or none>
* warnings: <each warning: line of review start, or none>
* times: started <started>, wait <seconds>, end <end>; wall minutes <(end - started - wait) / 60, to 1 decimal>
* interventions: <the number of messages of a person since review start, but not the message that gives the approval counts of step 11.  An approval is not an intervention>
* late review commands: <the number of `target/debug/xtask review` commands that the skill ran or tried to run after the turn in which it loaded, until you write this file>
* approvals: <not asked.  Step 11 writes the count that the person gives for the round>
* baseline approvals: <not asked.  Step 11 writes the count that the person gives for the baseline.  Without --baseline, write "-">

## Agents

| Agent | Range | Findings | Tokens | Minutes |
| - | - | - | - | - |
| reviewer | <base>..HEAD | <IDs of its findings, or no findings> | <tokens> | <minutes> |
| validator | <range> | verdicts for <IDs> | <tokens> | <minutes> |

## Findings

### <ID>

* sources: <each reviewer, cargo-mutants>
* severity: <blocker, should-fix or nit>
* significant: <yes or no; or ->
* kind: <bug, weak-test, rule, doc or other>
* where: <file:line>
* rule: <ID and quote, or none>
* claim: <the claim>
* verdict: <confirmed, pre-existing, refuted, unproven, unvalidated or known>
* repeat-of: <ID, TD, or none>
* evidence: <the evidence of the validator, in a few words>

## Baseline findings

### $1-b<n>

* (the same fields, with sources: baseline, and same-as: <ID, or none>)
* mark: <found or missed, with the match and its quote; or not compared>

## Baseline comparison

of <y> baseline findings, the round found <x>
```

* Fill the `significant` field yourself.  A reviewer does not fill it.
* A blocker or should-fix with the verdict `confirmed`, `pre-existing` or `unproven` gets `yes` or `no`, by the test of decision 0024.
* The test: a rule or decision fails in a case that a user can reach, or later work goes wrong.  A contradiction or a misleading measure is significant too.
* Each other finding gets `-`.  This includes each `known` finding.
* List each agent that the round started: the reviewers, the baseline, and each validator.  A validator's Findings cell names the IDs that it judged.
* Without `--baseline`, leave out the two baseline sections.
* With `--review-only`, run `target/debug/xtask review clean $1`.  Then stop here.  If auto mode or a person refuses it, give the command to the person.  Give the person the path of the findings file and a summary: the mutants line, and the count of findings for each verdict.

### 10. Fix the findings

The fix rule is decision 0024:

* Rounds 1 to 3: fix each found finding, the baseline's included.  A found finding has the verdict `confirmed` or `pre-existing`.
* From round 4, a round fixes blockers, significant should-fix and every confirmed finding on a strict rule.
* From round 4, log each other finding as `reported, not fixed`, nits included.  These are each `confirmed`, `pre-existing` or `unproven` finding of none of the three kinds, and each `unvalidated` finding.  Do not fix them.
* From round 4, fix each `pre-existing` finding that is a blocker, has `yes`, or is on a strict rule.  Or send it to a TD or to its own PR.
* From round 4, fix an `unproven` finding only if it is one of those three kinds.
* A significant should-fix has `yes` in its `significant` field.
* The strict rules are PROTO-1, PROTO-2, MEM-1 to MEM-5, RT-1, GPU-1 to GPU-3, VERIFY-1, GIT-1, DEPS-1, ASSET-1.
* A finding is on a strict rule when its rule names one of them.  Each finding of `cargo-mutants` is on VERIFY-1.

Then:

* Where the finding is about behaviour, first write a test that fails before the fix.
* A `pre-existing` finding can go to `docs/tech-debt.md`, or to its own PR, in place of a fix.
* A mutant that the team sends to tech debt gets a `KNOWN_MISSED` entry in the milestone's last commit, not in a round's fixes.  Reason: a change to `xtask/src/review.rs` routes all six reviewers (`ROUTE_ALL`).
* Do not fix a `refuted` finding.
* Do not fix a `known` finding.  Its gap is in its TD.
* Do not fix a reported repeat (step 4, item 4).  Its action is `reported, not fixed`.
* Decide each `unproven` finding, and record the reason.
* A nit has the verdict `unvalidated`.  In rounds 1 to 3, fix it only if you agree with it.
* Before the commit, run `cargo run -p xtask -- check --tier commit` (GIT-2).
* Commit the fixes, signed, with the subject "review round $1 fixes".

### 11. Add the round to the log

First, get the approval counts of the round.  They are cost, not interventions.  Use the first of the next three bullets that applies.  Then do the two bullets after them, unless that bullet tells you to stop.  Under the orchestrator bullet, use the first mode sub-bullet that applies, and always the last sub-bullet.

* If you are the orchestrator of an agent-run phase, you are "the person" (see "Before the steps").  Do not ask yourself.
  * In a `claude -p` run where nobody answers permission prompts, write each count as 0 with the mode, in any mode.  For example, write `0 (auto mode)`.  A mode that asks for approval gets none in that run, so its count is 0 too, for example `0 (default mode)`.  Where a host or a prompt tool answers prompts (`--permission-prompts host`), write the approvals that it gave, if the run records them.  Otherwise write `not counted` with the reason.
  * In `dontAsk` mode in an interactive session, write each count as `0 (dontAsk mode)`.
  * In auto mode in an interactive session, the mode can fall back to a prompt that waits for a person.  You do not see an approval of that prompt (TD-38).  So write each count as `0 (auto mode; a fallback prompt is not counted)`.
  * In another mode in an interactive session, ask the maintainer the questions below.
  * Without `--baseline`, keep "-" in the `baseline approvals` field.  This applies in each mode.
* If you are not the orchestrator, and you are a subagent or no person can answer, as in a `claude -p` run, do not ask.  Leave the approvals fields as step 9 wrote them.  Give the questions below in your final answer.  The caller asks them, and writes the counts.  If the Write tool refused a file to you, write the log's text, as "Before the steps" says.  Else stop here, and the caller does the rest of this step.
* In any other case, ask the person:
  1. "How many tool calls did you approve for the round's agents and for me, from `review start` until the findings file?  Do not count the `baseline` agent and its validators."
  2. With `--baseline`: "How many tool calls did you approve for the `baseline` agent and its validators in that time?"
  3. Also say: "Give one total if you cannot split them.  In a mode that asks for no approval, each count is 0."
* If you asked, wait for the answer.  Do not guess the counts.
* Write the first count in the `approvals` field of `<run>/$1/findings.md`.  Write the second count in its `baseline approvals` field, in place of "not asked".  With one total, the `approvals` field holds the total, which then includes the baseline's, and the `baseline approvals` field holds "in approvals".

The log `<run>/log.md` has two tables.  If the Write tool refuses it, do not write it in another way.  Give the path and the whole text of the file in your final answer.  Also give two commands: `target/debug/xtask review log-check <run>/log.md` and `target/debug/xtask review clean $1`.  Then stop.  The caller writes the log, then runs `review log-check`, then `review clean`.  If the file does not exist, write it in this form first:

```markdown
# Review log

## Findings

| Date | Round | Commit | Finding | Reviewers | Severity | Significant | Kind | Rule | Where | Claim | Verdict | Repeat of | Action |
| - | - | - | - | - | - | - | - | - | - | - | - | - | - |

## Rounds

| Round | Agents | Tokens | Wall minutes | Interventions | Late review commands | Approvals | Mutants | Baseline agents | Baseline tokens | Baseline wall minutes | Baseline interventions | Baseline approvals | Baseline found |
| - | - | - | - | - | - | - | - | - | - | - | - | - | - |
```

Add one row to the findings table for each finding of the round, the baseline's included:

* Date: today, as `YYYY-MM-DD`.  Commit: the short SHA of `HEAD` at `review start`.
* Reviewers: the sources of the finding.  Rule: the rule ID, or none.  Claim: one line.
* If the rule of a finding is a TD, also write the rule that the TD concerns in the Rule cell, such as `PROTO-1` for TD-16.
* Significant: the `significant` field of the finding.
* Action: one of these forms:
  * the fix commit and its subject, or the diff that holds the fix;
  * `reported, not fixed`; `refuted`; `known: <TD>`; a TD ID;
  * `no change:` and the reason, such as its own PR;
  * `merged into <ID>;`, then the action of that finding.
* A `no change:` reason names no commit SHA.
* A `known` finding has the action `known: <TD>`.

Add one row to the rounds table:

* Agents: the number of agents that the round started, but the baseline and its own validators.  The validators count with the agents that they validate.  Step 7's comparer counts neither with the round nor with the baseline.
* Tokens: the sum of the tokens of those agents.
* Wall minutes: the wall minutes of the findings file.  They run from `review start` to the last verdict, without the wait for the mutants run.
* Interventions: the number of messages of a person in the round, but not the message that gives the approval counts.  An approval is not an intervention.
* Late review commands: the field of the findings file.  In the default permission mode, each one asked a person for approval (TD-36).  Only in that mode does the count equal the approvals of those commands.
* Approvals: the count that the person gave for the round, as cost.  It is the field of the findings file.
* Mutants: the mutants line.
* With `--baseline`: the baseline agents are the baseline and the validators that step 5 started for its findings.  Their tokens are the sum of their tokens.  Their wall minutes are the duration of the baseline, plus the longest duration of those validators.  Their interventions are the messages of a person for those agents.  Baseline approvals: the count that the person gave for the baseline, or "in approvals" if the person gave one total.  Baseline found is "of y baseline findings, the round found x".  Without `--baseline`, write "-" in each baseline cell.

Then check the log:

* Run `target/debug/xtask review log-check <run>/log.md`.
* If it names a problem, correct the row or the fix before the next round.
* It runs after the findings file, so the counts of the round do not include its approval.

Then remove the worktrees and folders of the round:

* Run `target/debug/xtask review clean $1`.  It removes each worktree or folder under `target/review/` whose name starts with `$1-`, also with changes.
* It runs after the findings file, where the count of approvals of this step ends.  So the counts of the round do not include its approval.
* If auto mode or a person refuses it, give the command to the person, and go on.

Then decide if this round is the last round (decision 0024).  The round is the last round when all of these are true:

* Its number is 3 or more.
* It has no `confirmed` blocker, no `confirmed` should-fix with `yes`, and no `confirmed` finding on a strict rule.
* It fixed, or sent to a TD, no `pre-existing` or `unproven` blocker, should-fix with `yes`, or finding on a strict rule.

A `known` finding does not count.  A `confirmed` finding of the three kinds counts whatever its action, a TD included.  There is no cap.  If the round is not the last round, the next round follows.

After the last round:

* Copy `<run>/log.md` to the reviews folder under `docs`, as `<branch>.md`.  `<branch>` is the last part of the `<run>` path.  In a run of the `orchestrate` skill, the copy is `<branch>-m<n>.md`, for milestone `<n>`.
* Write a Progress line for each round in the plan of the work.
* Run the checks with `cargo run -p xtask -- check --tier push`, and commit, signed.
* Give the person the text for the PR description.  It lists each `refuted` finding, each `unproven` blocker or should-fix, and each `repeat-of` of a finding that is not `known`.  Then it lists each `known` finding once, with its TD.  This includes each `known` mutant.  In its `<details>` section, it lists each `reported, not fixed` finding.  It also gives the mutants line of each round.

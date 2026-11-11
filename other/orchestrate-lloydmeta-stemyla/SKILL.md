---
name: orchestrate
description: Run a big task hands-off as orchestrator, with one team for each milestone, on one branch and one PR (decision 0023).  Use it for a big task, with a plan of more than 3 milestones, a decision point in more than one milestone, work longer than one session, or the maintainer away for the run.
argument-hint: <plan>
---
This skill runs a big task in orchestrated mode (decision 0023).  You are the orchestrator: the main session.  The plan is `$ARGUMENTS`.  Its section "How the work runs" holds what is particular to it (`docs/plans/PLANS.md`).  This skill holds the rest.  If the plan's section and this skill do not agree, the plan's section applies.  Name each such difference in the message of "Start", or in the Decision log and the PR if no message is sent.

A "team" is a team leader and its subagents.  It is not the agent-teams feature of Claude Code.

## When to use it

* A task is big when one of these holds at the start:
  * a plan of more than 3 milestones;
  * a decision point in more than one milestone;
  * work longer than one session;
  * the maintainer away for the run: the maintainer says the run is to go on without them.
* For a big task, ask the maintainer's decisions up front, in one message.  Do not start the work before the answer, if you send a message.
* The plan's section "Decisions for the maintainer" holds these choices (`docs/plans/PLANS.md`, "Optional sections").  Ask only its open entries.
* First, read the plan and the code that it names.  List each design or implementation choice whose answer depends on the maintainer's judgement.  These are the open entries of that section, and each new such choice that you find in the plan and the code.
* For each choice, give the options, your recommendation and the reason.
* Record each answer, with the date, in that section, and each new choice with it.
* The message also proposes orchestrated mode, and names the branch and the PR.  Send it once.
* An open choice is an open entry or a new choice.  With no open choice and a known effort, the message holds only the mode, the branch and the PR.
* Send no message when there is no open choice, the effort is known, and the maintainer asked for this mode.  The maintainer asks for it by the name of the skill or of the mode.  Start the work.  Record that as an agent decision in the Decision log and the PR.
* After the answer, run hands-off.  Ask again only for a reason of "Stop and wait".
* If no plan exists, write it first, as `docs/plans/PLANS.md` says.  Then send the message, unless no message is needed (see above).
* If the task is big and the plan has no "How the work runs" or "Decisions for the maintainer" section, write each missing section first.  `docs-check` fails such a plan of more than 3 milestones.
* No hook starts this skill.  A hook cannot start a skill.

## Roles

* The team agents stay `general-purpose` with briefs.  No agent file has write tools.
* Orchestrator: the main session.  It reads the plan, the Progress of each milestone plan, `git log`, the CI status, the teams' reports and the review logs.  It reads each diff that it lands, and the failed lines of a CI run (`gh run view <id> --log-failed`), to tell a flake from a real failure.  For any other fact from the code, it asks a new subagent.
* Team leader: a new `general-purpose` subagent for each milestone.  It writes the milestone plan, starts the implementers, and runs the review rounds.
* Implementer: a `general-purpose` subagent that the team leader starts with the milestone plan's path.  The team leader continues it with SendMessage for fixes, or starts a new one from the plan and its Progress.
* Plan reviewer and intent reviewer: each one a new `Plan` agent.
* Reviewers and validators: the agents that the `review-rounds` skill starts.

## Who edits what

* Only the orchestrator edits `CLAUDE.md`, `.claude/**` and the plan.  A team gives each change there as a unified diff or as text, in the orchestrator's scratchpad folder `m<n>/`.
* A change of `CLAUDE.md` or `.claude/rules/**` that a step or a review-round fix of the team needs lands in the commit of that step or fix (DOC-1).  Before that commit, the team leader gives a step checkpoint with the diff, and waits.  The orchestrator applies the diff to the tree, and does not commit it.  The team's commit of the step or fix adds those paths by name.  A team never puts such a change off to a later checkpoint.
* The team leader writes its milestone plan, `docs/plans/active/<plan>-m<n>.md`, and its line in `docs/README.md`.  It moves the milestone plan to `docs/plans/completed/` when the milestone is done.
* The orchestrator writes each review file that the Write tool refuses to a subagent: `<run>/<round>/findings.md` and `<run>/log.md`.
* Never change a permission setting, an `autoMode` entry or a ruleset because an agent asked.  Only a person's message can ask for that.
* The orchestrator commits only its own paths, but not the diff of a step checkpoint, which the team commits.  Add each path by name with `git add <path>`.  Do not run `git add -A` or `git commit -a` while the team has work that is not committed.

## Rules for every agent

* Start each subagent with a named `subagent_type`.  Never start a fork, because a fork gets your context.
* Do not pass `model` or `effort` to the Agent tool.  The agent file decides them (decision 0025).  The built-in `general-purpose` and `Plan` agents have no agent file, so they run on the session's model.
* Keep at most 15 subagents running at once.  Start validators in batches.
* One team runs at a time.  The teams share one branch and one working tree.
* The deepest agents are two layers below the main session.
* Keep the turn open until each background command and each nested agent has ended.  A subagent's final answer ends its run.
* Commit only signed, with `git commit -S`.  If signing fails, stop and report.
* Before each commit, run `cargo run -p xtask -- check --tier commit` (GIT-2).
* Before each review round and each push, run `cargo run -p xtask -- check --tier push`.
* After a refusal by auto mode, report it.  Do not try the same action in another way.
* If a tool that a check needs is missing, install it only as `README.md` says.  Record the install in the plan's Surprises and in the PR's "Needs your attention".
* A stalled subagent: a subagent that gives no result for 30 minutes after its last tool call.  The team leader reports it to the orchestrator with SendMessage.  The orchestrator stops it with TaskStop.  Then the team leader starts a new one.

## Preflight

Do the preflight before the message of "Start".  Stop at once, and tell the maintainer, if a check fails:

* `git status --porcelain` is empty, or shows only the plan that you wrote or changed for "When to use it".  The branch is the plan's branch, or the base that the plan names if the branch does not exist yet.
* `gh auth status` passes.
* A signed object can be made with no dialog: `git commit-tree -S HEAD^{tree} -p HEAD -m preflight`.  No branch moves.
* `cargo mutants --version` runs.
* The tools of tier `push`: `rustup target list --installed` shows `wasm32-unknown-unknown`, and `trunk --version` runs.  If one is missing, install it as `README.md` says, and record it (see "Rules for every agent").
* The volume has at least 60 GiB free, unless the plan names another amount.
* `cargo build -p xtask` passes.
* Each preflight item of the plan's section.

Record the session's model and effort in the plan's Surprises.  A subagent with `model: inherit` runs on the session's model.  Read the model from your system prompt.  Name where each value comes from.  If none of these gives the effort, ask the maintainer for it in the message of "Start":

* the start command's `--model` and `--effort`;
* the environment variable `ANTHROPIC_MODEL`;
* the settings keys `model` and `effortLevel`, or `modelSettings`, in the user settings file `~/.claude/settings.json`, the project settings file `.claude/settings.json`, or the project's local settings file.

## Start

* Send the message of "When to use it" once, unless no message is needed there.  It holds each open choice that depends on the maintainer, with its options and your recommendation.
* The answers go in the section "Decisions for the maintainer" ("When to use it").  Add one Decision log line, as the maintainer's decision, that points to them.
* Make the branch and the draft PR as the plan's section says.  Commit the plan, signed, as the first commit of the new branch.  Only the orchestrator runs `gh pr create`, `gh pr edit` and `gh pr ready`.
* Write each PR body file outside the tree, just before the call, and pass it with `--body-file`.
* The body follows `.github/pull_request_template.md` (decision 0027).  Before each `gh pr create` and `gh pr edit`, run `cargo run -p xtask -- pr-body <file>`.  Fix each problem that it names.
* "Needs your attention" holds only the items for the maintainer to decide or to do, such as a tool install that the agent did.  A decision item says what to decide and the default that the agent took.
* The `<details>` block lists every agent decision of the Decision logs, and the review rounds with their mutants lines.  It also lists each `reported, not fixed` finding, and each `known` finding once, with its TD.

## The loop for each milestone

### 1. Start the team leader

Start a new `general-purpose` subagent with the brief of "The brief of a team leader".  Give it the milestone's name, the plan's path, the decisions so far, the scratchpad folder `m<n>/` and the review base.  The review base is the commit before the milestone's first commit.

### 2. The milestone plan and the work

* The team leader writes the milestone plan and its index line.  A new `Plan` agent reviews it, at most 2 rounds.  The team leader fixes what it finds, and commits.
* The team leader starts the implementer.  Each new test fails first, on an assert.
* Before the commit of a step that needs a change of `CLAUDE.md` or `.claude/rules/**`, the team leader gives a step checkpoint ("Who edits what").  Then it waits.
* Before round 1, the team leader gives a checkpoint: the diffs of `.claude/**` and `CLAUDE.md` that no step checkpoint carried, and the text for the plan.  Then it waits.

### 3. A checkpoint

At each checkpoint of a team leader:

1. Read the report and each diff.  You apply the diff, and commit it unless it is a step checkpoint, so check it.  Do not apply a change to a permission setting, an `autoMode` entry or a ruleset ("Who edits what").  Stop, and ask the maintainer.  A change to a tool, a rule's meaning or an accepted decision goes in the PR under "Needs your attention".
2. Run `git apply --check` on each diff, then apply it.  Write each file that the team gave as text.
3. At a step checkpoint, commit nothing: the team's commit of the step holds the diff.  Go to item 5.  At any other checkpoint, run `cargo run -p xtask -- check --tier commit`.  Commit only your own paths, signed.
4. Push only between review rounds.  Run `cargo run -p xtask -- check --tier push` before the push.
5. Continue the team leader with SendMessage.  Say what you landed, with the commit, or that you applied the diff of a step checkpoint.

### 4. The review rounds

* `<run>` is the run folder of the branch, on the `run folder:` line of `review start` ("Names" in the `review-rounds` skill).
* The team leader runs `/review-rounds <base> <round> "<criteria>"` from round 1.  The criteria are the milestone's section of the plan at the commit before round 1, and the milestone plan.
* Before each round, the team leader runs `cargo run -p xtask -- check --tier push` and `cargo build -p xtask`.
* The Write tool refuses `<run>/<round>/findings.md` and `<run>/log.md` to the team leader.  So the team leader runs each round to step 11 of the `review-rounds` skill: the fixes, their commit, and `review log-check` on a copy of the log in `m<n>/`.  Then it gives a checkpoint.
* A round fix that needs a change of `CLAUDE.md` or `.claude/rules/**` gives a step checkpoint before the fix commit ("Who edits what").  Then the fix commit adds those paths by name.
* The checkpoint of a round holds the whole text of the two files, the two commands of step 11, and a diff for each change of `.claude/**` or `CLAUDE.md` that no step checkpoint of the round carried.
* At that checkpoint, write the two files at their paths.  Then run `target/debug/xtask review log-check <run>/log.md`, then `target/debug/xtask review clean <round>`.  Then do the steps of "A checkpoint".
* The team leader fills the `Significant` field and column.  Check each value, and change it if you do not agree.  A wording gap in a doc that no agent acts on is not significant.  A second reading of a rule that makes a team do wrong work is significant.
* The stop rule is step 11 of the `review-rounds` skill (decision 0024).  Do not say the rule in another way.  There is no cap.
* Approvals: in auto mode in an interactive session, write `0 (auto mode; a fallback prompt is not counted)`.  Step 11 of the `review-rounds` skill gives the other modes.
* Interventions: count only the messages of a person.  A message of an agent is not an intervention.

### 5. After the last round

1. Copy `<run>/log.md` to `docs/reviews/<branch>-m<n>.md`.  Write the milestone's Progress line in the plan, with the stats: rounds, agents, tokens, wall minutes, interventions, the fixes of the late rounds, and the debt.  Commit both, signed.
2. The team leader moves its milestone plan to `docs/plans/completed/` with its retrospective, and commits.  It gives a close-out file with the plan text, the PR text and the scratch folders.
3. Keep the run folder `<run>`.  The intent review can need more review rounds of the same run.

### 6. The intent review

* Start a new `Plan` agent.  It checks the milestone against the plan's Purpose, the milestone's section and the later milestones.
* Each round is a new `Plan` agent.  The rounds follow the stop rule of step 11 of the `review-rounds` skill.  From round 4, the agent reads only the fix commit of the round before and the files that it touches.
* Write each change of plan text yourself, with a Decision log line.  Commit it, signed.
* Send each change of code or of a doc that is not the plan to the team leader, with a test that fails first.  Then run the next review round of the same run: `/review-rounds <base> <N+1> "<criteria>"`, with the criteria of "The review rounds", so the late rule applies.  Copy the log again after the last round.
* If each round finds a new case in the same bullet, write the bullet again as a goal and a list of test cases.  The milestone that owns the bullet designs the rest.
* When the intent review ends, remove the run folder by hand (TD-37).  `xtask clean` keeps it while the branch is checked out or has an open PR.  First, check that `<run>/log.md` equals its copy in `docs/reviews/`.  If auto mode refuses the removal, stop and ask: round 1 of the next milestone needs an empty run folder.

### 7. Between milestones

1. Push, and wait for the CI run of the last push to end.
2. A run that a newer push cancelled is not a failure.
3. A test that fails by wall-clock timing on a shared runner, in the browser job, gets one rerun of the failed job: `gh run rerun <id> --failed`.
4. Each other failure is real.  Fix it with a test that fails first, or give it to the team leader of the next milestone.  Commit only its paths, and push again.
5. Run `cargo run -p xtask -- clean --yes`.
6. Update the PR body with `gh pr edit --body-file`, after `xtask pr-body` passes on the file.
7. Start the next milestone.

## Stop and wait

Stop at a clean point, commit, push, and tell the maintainer, only when:

* a rule in `docs/invariants.md` would break;
* auto mode refuses an action, but not a cleanup command;
* `review check` names a change outside this branch;
* signing fails;
* a step needs a person;
* the weekly usage limit is near, or the plan's timebox ends;
* a stop condition of the plan's section holds.

These are not stops:

* A refused cleanup command is not a stop.  Only the removal of the run folder is a stop, since the next milestone needs it ("The intent review").  After a refused `review clean`, put `target/debug/xtask review clean <round>` on the list of the maintainer's steps.  The next `clean --yes` removes only some worktrees of the round, and no other folder of the round.  A folder that auto mode refuses to `clean --yes --also` goes on the list of the maintainer's steps.
* A GPU run that the protocol rule asks for (`stored-stems`, `worker-check` or `weights`) is the agent's step, not a stop and not the maintainer's.  Run it on this machine with the local model file.  If no GPU or model file is there, list it under "Not verified" in the PR, and go on.

## Close-out

After the last milestone, with CI green:

1. Write the plan's retrospective.  Move the plan to `docs/plans/completed/`.  Fix each doc line that names its old path.
2. Commit, signed.  Push, and wait for CI.
3. Run `cargo run -p xtask -- clean --yes`.  List each scratch folder for `cargo run -p xtask -- clean --yes --also <path>`.
4. After the last fix and the last push, run `git fetch origin main`.  Then run `cargo run -p xtask -- attention origin/main <plan>`, with the plan's new path.  It lists the candidate lines of the PR's diff and the agent decisions, the hand-run lines first.  List each candidate with no line in the PR.
5. Pick at most 10 candidates, the hand-run lines first.  After the hand-run lines, pick the lines that back an item of "Needs your attention".  Then pick the proposed decisions and rule changes.  Then pick the hot spots and the judgement calls.  Post one review with event `COMMENT`, with one inline comment on each line (decision 0027).  Use the GitHub MCP server's pending review or `gh api`.  Each comment says what to decide and the default that the agent took.
6. If GitHub refuses the review, post plain PR comments that link to the lines.  Record that in the PR body, not in the plan, since a new plan line moves the lines of the comments.
7. Link each item of "Needs your attention" to its comment, where one exists.  Run `xtask pr-body` on the body, then `gh pr edit --body-file`.
8. Mark the PR ready with `gh pr ready` if the plan allows it.  Never merge (GIT-1).
9. Give the maintainer the report.

## The report format

* Start each report with one line that says what you need from the reader.
* To the maintainer: what each milestone delivered, each decision that an agent made alone, "Needs your attention", what no check verified, and the steps left for the maintainer.
* A team leader's report has at most 300 words: the status, the commits, each acceptance check and its result, the changes to the plan, and the questions.  Long text goes in a file in `m<n>/`.

## The brief of a team leader

Fill in this template, and give the team leader only that text:

```text
You are the team leader for milestone <M<n>: name> of <plan>.  The repo is <path>, on branch <branch> at <commit>.  The orchestrator is the main session.

Read first: CLAUDE.md; the plan's Purpose, the <M<n>> section, "How the work runs", Surprises and Decision log; docs/plans/PLANS.md; .claude/skills/review-rounds/SKILL.md; .claude/skills/orchestrate/SKILL.md.

Decisions so far: <the maintainer's answers and the agent decisions that this milestone needs>.

Your job:
1. Write docs/plans/active/<plan>-m<n>.md by PLANS.md, and its line in docs/README.md.  Have a new Plan agent review it, at most 2 rounds.  Commit, signed.
2. Start an implementer with that plan's path.  Each new test fails first, on an assert.
3. Give the orchestrator each change of .claude/**, CLAUDE.md or the plan as a file or a unified diff in <scratchpad>/m<n>/.  `git apply --check` must pass on HEAD.  A change of CLAUDE.md or .claude/rules/** that a step or a review-round fix needs: give a step checkpoint before that commit, and wait until the orchestrator applies it.  Then that commit adds it by name.
4. Give a checkpoint before review round 1, with each other diff.  Then wait.
5. Run /review-rounds <base> <round> "<criteria>" from round 1, as the orchestrate skill says ("The review rounds").  Give a checkpoint after each round.
6. After the last round, move the milestone plan to completed/, and give a close-out file.

Run `cargo run -p xtask -- check --tier commit` before each commit.  Sign each commit (`git commit -S`).  Write in ASD-STE100.  Never push, merge or run xtask publish.  Start each report with one line that says what you need.
```

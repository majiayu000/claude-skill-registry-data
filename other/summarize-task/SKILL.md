---
name: summarize-task
description: "After executing a task, write its outcome summary. Reads M###-S##-T##-PLAN.md, prompts for what happened, writes M###-S##-T##-SUMMARY.md, flips checkbox in slice-plan, updates STATE.md. Optionally stages git. Run once per task completion."
tier: core
version: 0.1.0
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - AskUserQuestion
triggers:
  - summarize task
  - task done
  - ytstack task complete
  - close task
---

# summarize-task

Close a task: capture what actually happened (often different from the plan), flip checkboxes, advance STATE.md. Produces an append-to-history artifact future sessions can read.

## Anti-Pattern: "The task is done, I don't need a summary"

Without a summary, the next session has no way to know this task happened -- STATE.md wasn't updated, the slice-plan checkbox is still `[ ]`, and the next agent will either redo the work or get confused. The summary is the closure signal. Always write it, even for one-line tasks ("CSS tweak -- shipped in one commit, no follow-up needed").

## Checklist

You MUST create a TodoWrite task for each of these items:

1. **Run preamble** -- detect active task + plan file
2. **HARD-GATE: active task must exist** -- abort if none
3. **Read the plan** -- show user the original scope
4. **Ask outcome** -- what actually shipped
5. **Ask deviations** -- what differed from plan (if anything)
6. **Ask follow-ups** -- new tasks / decisions surfaced during execution
7. **Ask verification result** -- did the verification command pass?
8. **Write `M###-S##-T##-SUMMARY.md`**
9. **Flip slice-plan checkbox** `[ ]` → `[x]`
10. **Update STATE.md** -- clear `active_task`, bump counts, update status line
11. **Offer git stage** -- ask if user wants git-add of touched files
12. **Report + return** -- suggest next task or slice-close

## Preamble

```bash
_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
cd "$_PROJECT_DIR" 2>/dev/null || true
_PROJECT_SLUG=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || basename "$(pwd)")

if [ -d "$_PROJECT_DIR/.ytstack" ]; then
  _YT_DIR="$_PROJECT_DIR/.ytstack"
elif [ -d "$HOME/.ytstack/projects/$_PROJECT_SLUG" ]; then
  _YT_DIR="$HOME/.ytstack/projects/$_PROJECT_SLUG"
else
  _YT_DIR=""
fi

_HAS_YTSTACK=$([ -n "$_YT_DIR" ] && echo yes || echo no)

_NON_INTERACTIVE=false
if [ -n "$YTSTACK_NON_INTERACTIVE" ] || [ -n "$OPENCLAW_SESSION" ] || [ -n "$CLAUDE_AGENT_TEAM_MEMBER" ]; then
  _NON_INTERACTIVE=true
fi

_CURRENT_MILESTONE=none
_ACTIVE_SLICE=none
_ACTIVE_TASK=none
if [ -f "$_YT_DIR/STATE.md" ]; then
  _CURRENT_MILESTONE=$(sed -n 's/^current_milestone: *//p' "$_YT_DIR/STATE.md" | head -1)
  _ACTIVE_SLICE=$(sed -n 's/^active_slice: *//p' "$_YT_DIR/STATE.md" | head -1)
  _ACTIVE_TASK=$(sed -n 's/^active_task: *//p' "$_YT_DIR/STATE.md" | head -1)
fi

_PLAN_FILE="$_YT_DIR/$_CURRENT_MILESTONE-$_ACTIVE_SLICE-$_ACTIVE_TASK-PLAN.md"
_SLICE_PLAN="$_YT_DIR/$_CURRENT_MILESTONE-$_ACTIVE_SLICE-PLAN.md"
_IS_GIT=$([ -d .git ] && echo yes || echo no)

# Gather this task's commits for a durable, committed `## Commits` section.
# ytstack's commit convention prefixes task commits with `M###-S##-T##:`
# (see CLAUDE.md), so grep the log for that ref. This is the SINGLE owner of
# commit-to-task linking; the post-tool-use-bash hook only drops a draft stub
# and never maintains a commit list (issue #22 / M015).
_TASK_REF="$_CURRENT_MILESTONE-$_ACTIVE_SLICE-$_ACTIVE_TASK"
_TASK_COMMITS=""
if [ "$_IS_GIT" = yes ]; then
  _TASK_COMMITS=$(git log --no-merges --pretty=format:'- `%h` -- %s' --grep "^$_TASK_REF" 2>/dev/null)
fi

echo "HAS_YTSTACK: $_HAS_YTSTACK"
echo "YTSTACK_NON_INTERACTIVE: $_NON_INTERACTIVE"
echo "CURRENT_MILESTONE: $_CURRENT_MILESTONE"
echo "ACTIVE_SLICE: $_ACTIVE_SLICE"
echo "ACTIVE_TASK: $_ACTIVE_TASK"
echo "PLAN_FILE: $_PLAN_FILE"
echo "SLICE_PLAN: $_SLICE_PLAN"
echo "IS_GIT: $_IS_GIT"
echo "TASK_COMMITS_BEGIN"
echo "${_TASK_COMMITS:-(none found for $_TASK_REF)}"
echo "TASK_COMMITS_END"
```

## Procedure

### Step 2: HARD-GATE

If any of `HAS_YTSTACK / CURRENT_MILESTONE / ACTIVE_SLICE / ACTIVE_TASK` is `no / none`:
> "No active task to summarize. Check STATE.md and run the preceding skill (`plan-task` / `slice-milestone` / `plan-milestone` / `init-project`) as needed."
STOP.

If `PLAN_FILE` does not exist:
> "STATE.md says active_task={ACTIVE_TASK} but plan file missing at {PLAN_FILE}. Repair manually before summarizing."
STOP.

### Step 3: Read the plan

Read `{PLAN_FILE}`. Extract Summary, Files, Verification. Show:

> Closing **{CURRENT_MILESTONE}-{ACTIVE_SLICE}-{ACTIVE_TASK}**.
>
> Original plan: {SUMMARY}
> Files planned: {FILE_LIST}
> Verification: {VERIFICATION_CMD}

### Step 4: Ask outcome

Use AskUserQuestion (open-ended):

> What actually shipped? 2-4 sentences. Use past tense. Say what the code does now, not what you did to it.
>
> Good: "Signup form validates email client-side and POSTs JSON to /api/signup. Server hashes with argon2 and inserts user row. Returns 201 with session cookie. Duplicate email returns 409."
>
> Bad: "I implemented signup" -- too vague, not useful to future sessions.

Remember as `_OUTCOME`.

### Step 5: Ask deviations

Use AskUserQuestion (open-ended):

> Did anything differ from the plan? Extra files, skipped features, refactors, new dependencies?
>
> Enter "none" if the plan held up.

Remember as `_DEVIATIONS`.

### Step 6: Ask follow-ups

Use AskUserQuestion (open-ended):

> Anything that surfaced during execution that needs follow-up? Add them as:
> - new tasks (get added to next slice or a new slice)
> - decisions to lock in `DECISIONS.md`
> - patterns worth capturing in `KNOWLEDGE.md`
> - items to flag in `REVIEW-NOTES.md` for end-of-cycle
>
> Enter "none" if clean.

Remember as `_FOLLOWUPS`.

### Step 7: Ask verification result

Use AskUserQuestion (multi-choice):

> Did the plan's verification step pass?
>
> Verification was: `{VERIFICATION_CMD}`
>
> A) Passed -- clean exit, expected output. (Completeness: 10/10)
> B) Passed with caveats -- exits 0 but something's off. (Completeness: 7/10, flag in followups)
> C) Failed -- task not actually done. (Completeness: 0/10, do not close)
>
> If C: do NOT proceed. Re-execute the task until it passes, then re-run this skill.

If C: STOP. Do not write the summary.

Remember as `_VERIFICATION_RESULT` (value: `passed` / `passed_with_caveats`).

### Step 8: Write `M###-S##-T##-SUMMARY.md`

```markdown
---
milestone: {CURRENT_MILESTONE}
slice: {ACTIVE_SLICE}
task: {ACTIVE_TASK}
project: {PROJECT_NAME}
closed: {ISO_TIMESTAMP}
verification: {VERIFICATION_RESULT}
---

# {CURRENT_MILESTONE}-{ACTIVE_SLICE}-{ACTIVE_TASK} -- Summary

## Commits

{The commit list captured between TASK_COMMITS_BEGIN / TASK_COMMITS_END in the preamble. If it reported "(none found ...)", write: "No commits matched `{TASK_REF}:` -- task shipped uncommitted or under a non-conventional message." This section replaces the throwaway hook draft; it is the durable commit-to-task link.}

## Outcome

{OUTCOME}

## Deviations from plan

{DEVIATIONS}

## Follow-ups

{FOLLOWUPS}

## Verification

Command: `{VERIFICATION_CMD}` -- {VERIFICATION_RESULT}.
```

### Step 9: Flip slice-plan checkbox

Edit `{SLICE_PLAN}`. Replace:

```
- [ ] {ACTIVE_TASK} -- {TASK_DESC}
```

with:

```
- [x] {ACTIVE_TASK} -- {TASK_DESC}
```

Also bump `completed_tasks` in the slice-plan's frontmatter by 1.

### Step 10: Update STATE.md

If `YTSTACK_NON_INTERACTIVE` is `false` (i.e. `CLAUDE_AGENT_TEAM_MEMBER` is unset), edit STATE.md frontmatter:
- `active_task: {ACTIVE_TASK}` → `active_task: none`
- If the slice is now fully complete (all tasks `[x]`): also `active_slice: {ACTIVE_SLICE}` → `active_slice: none`

If `YTSTACK_NON_INTERACTIVE` is `true` (running as swarm teammate): skip frontmatter writes. Log:
> `[ytstack:summarize-task] skipping STATE.md active_task/active_slice write -- running as swarm teammate (CLAUDE_AGENT_TEAM_MEMBER set)`

Regardless of teammate mode:
- `last_updated: ...` → bump to current
- Status line → `**Status:** {CURRENT_MILESTONE} / {ACTIVE_SLICE} -- {N}/{TOTAL} tasks done in slice. Next task: pick from slice-plan or run `/ytstack:plan-task`.`

If the slice is now fully complete (all tasks `[x]`): update status to recommend `/ytstack:reassess-roadmap`.

### Step 11: Offer git stage

If `IS_GIT=yes`, use AskUserQuestion:

> Task closed. Want to stage the touched files for commit?
>
> Files from plan: {FILE_LIST}
>
> RECOMMENDATION: A if the files match the plan. B if you touched additional files (deviation case).
>
> A) Stage the planned files -- `git add {FILE_LIST}` then you commit manually with a message
> B) Don't stage -- I'll handle it myself
> C) Stage all changes -- `git add -A` (use with caution; may include unintended files)

If A: run `git add {FILE_LIST}` and report `git status` output.
If B: skip.
If C: confirm once more (destructive-flavored), then `git add -A` + `git status`.

### Step 12: Report + return

Report:

> Task **{ACTIVE_TASK}** closed.
>
> Summary at: `{YT_DIR}/{CURRENT_MILESTONE}-{ACTIVE_SLICE}-{ACTIVE_TASK}-SUMMARY.md`
> Slice-plan checkbox flipped.
> STATE.md: `active_task` cleared.
>
> Next step:
> - If slice has more tasks: `/ytstack:plan-task` for the next one
> - If slice is complete: `/ytstack:reassess-roadmap` to check if plan still fits reality before moving to next slice
> - If milestone is complete: flip milestone status in ROADMAP.md and run `/ytstack:plan-milestone` for the next

## Terminal State

Valid terminal states:
- Return after summary file + slice-plan update + STATE.md update + optional git stage
- Abort on HARD-GATE failure (no active task / missing plan file)
- Abort on verification failure (C in Step 7) -- task stays open

Do NOT invoke `plan-task`, `reassess-roadmap`, or `plan-milestone` automatically.

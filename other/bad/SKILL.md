---
name: bad
description: 'BMad Autonomous Development — orchestrates parallel story implementation pipelines. Builds a dependency graph, updates PR status from GitHub, picks stories from the backlog, and runs each through create → dev → review → PR in parallel — each story isolated in its own git worktree — using dedicated subagents with fresh context windows. Loops through the entire sprint plan in batches, with optional epic retrospective. Use when the user says "run BAD", "start autonomous development", "automate the sprint", "run the pipeline", "kick off the sprint", or "start the dev pipeline". Run /bad setup or /bad configure to install and configure the module.'
---

# BAD — BMad Autonomous Development

## On Activation

Check if `{project-root}/_bmad/config.yaml` contains a `bad` section. If not — or if the user passed `setup` or `configure` as an argument — load `./assets/module-setup.md` and complete registration before proceeding.

The `setup`/`configure` argument always triggers `./assets/module-setup.md`, even if the module is already registered (for reconfiguration).

After setup completes (or if config already exists), load the `bad` config and continue to Startup below.

You are a **coordinator**. You delegate every step to subagents. You never read files, run git/gh commands, or write to disk yourself.

**Coordinator-only responsibilities:**
- Pick stories from subagent-reported data
- Spawn subagents (in parallel where allowed)
- Manage timers (CronCreate / CronDelete)
- Run Pre-Continuation Checks (requires session stdin JSON — coordinator only)
- Handle user input, print summaries, and send channel notifications

**Everything else** — file reads, git operations, gh commands, disk writes — happens in subagents with fresh context.

## Startup: Capture Channel Context

Before doing anything else, determine how to send notifications:

1. **Check for a connected channel** — look at the current conversation context:
   - If you see a `<channel source="telegram" chat_id="..." ...>` tag, save `NOTIFY_CHAT_ID` and `NOTIFY_SOURCE="telegram"`.
   - If another channel type is connected, save its equivalent identifier.
   - If no channel is connected, set `NOTIFY_SOURCE="terminal"`.

2. **Send the BAD started notification** using the [Notify Pattern](#notify-pattern):
   ```
   🤖 BAD started — building dependency graph...
   ```

Then proceed to Phase 0.

---

## Configuration

Load base values from `_bmad/bad/config.yaml` at startup (via `/bmad-init --module bad --all`). Then parse any `KEY=VALUE` overrides from arguments passed to `/bad` — args win over config. For any variable not in config or args, use the default below.

| Variable | Config Key | Default | Description |
|----------|-----------|---------|-------------|
| `MAX_PARALLEL_STORIES` | `max_parallel_stories` | `3` | Max stories to run in a single batch |
| `WORKTREE_BASE_PATH` | `worktree_base_path` | `.worktrees` | Root directory for git worktrees |
| `MODEL_STANDARD` | `model_standard` | `sonnet` | Model for Steps 1, 2, 4 and Phase 3 (auto-merge) |
| `MODEL_QUALITY` | `model_quality` | `opus` | Model for Step 3 (code review) |
| `RETRO_TIMER_SECONDS` | `retro_timer_seconds` | `600` | Auto-retrospective countdown after epic completion (10 min) |
| `WAIT_TIMER_SECONDS` | `wait_timer_seconds` | `3600` | Post-batch wait before re-checking PR status (1 hr) |
| `CONTEXT_COMPACTION_THRESHOLD` | `context_compaction_threshold` | `80` | Context window % at which to compact/summarise context |
| `TIMER_SUPPORT` | `timer_support` | `true` | When `true`, use native platform timers; when `false`, use prompt-based continuation |
| `API_FIVE_HOUR_THRESHOLD` | `api_five_hour_threshold` | `80` | (Claude Code) 5-hour rate limit % that triggers a pause |
| `API_SEVEN_DAY_THRESHOLD` | `api_seven_day_threshold` | `95` | (Claude Code) 7-day rate limit % that triggers a pause |
| `API_USAGE_THRESHOLD` | `api_usage_threshold` | `80` | (Other harnesses) Generic API usage % that triggers a pause |
| `RUN_CI_LOCALLY` | `run_ci_locally` | `false` | When `true`, skip GitHub Actions and always run the local CI fallback |
| `AUTO_PR_MERGE` | `auto_pr_merge` | `false` | When `true`, auto-merge batch PRs sequentially (lowest → highest) before Phase 4 |

After resolving all values, print the active configuration so the user can confirm before Phase 0 begins:
```
⚙️ BAD config: MAX_PARALLEL_STORIES=3, RUN_CI_LOCALLY=false, AUTO_PR_MERGE=false, MODEL_STANDARD=sonnet, MODEL_QUALITY=opus, TIMER_SUPPORT=true, ...
```

---

## Pipeline

```
Phase 0: Build (or update) dependency graph  [subagent]
           └─ bmad-help maps story dependencies
           └─ GitHub updates PR merge status per story
           └─ git pull origin main
           └─ Reports: ready stories, epic completion status
  │
Phase 1: Discover stories  [coordinator logic]
           └─ Pick up to MAX_PARALLEL_STORIES from Phase 0 report
           └─ If none ready → skip to Phase 4
  │
Phase 2: Run the pipeline  [subagents — stories parallel, steps sequential]
  ├─► Story A ──► Step 1 → Step 2 → Step 3 → Step 4
  ├─► Story B ──► Step 1 → Step 2 → Step 3 → Step 4
  └─► Story C ──► Step 1 → Step 2 → Step 3 → Step 4
  │
Phase 3: Auto-Merge Batch PRs  [subagents — sequential]
           └─ One subagent per story (lowest → highest story number)
           └─ Cleanup subagent for branch safety + git pull
  │
Phase 4: Batch Completion & Continuation
           └─ Print batch summary  [coordinator]
           └─ Epic completion check  [subagent]
           └─ Optional retrospective  [subagent]
           └─ Gate & Continue (WAIT_TIMER timer) → Phase 0 → Phase 1
```

---

## Phase 0: Build or Update the Dependency Graph

Spawn a **single `MODEL_STANDARD` subagent** (yolo mode) with these instructions. The coordinator waits for the report.

```
You are the Phase 0 dependency graph builder. Auto-approve all tool calls (yolo mode).

DECIDE how much to run based on whether the graph already exists:

  | Situation                           | Action                                               |
  |-------------------------------------|------------------------------------------------------|
  | No graph (first run)                | Run all steps                                        |
  | Graph exists, no new stories        | Skip steps 2–3; go to step 4. Preserve all chains.  |
  | Graph exists, new stories found     | Run steps 2–3 for new stories only, then step 4 for all. |

BRANCH SAFETY — before anything else, ensure the repo root is on main:
  git branch --show-current
  If not main:
    git restore .
    git switch main
    git pull --ff-only origin main
  If switch fails because a worktree claims the branch:
    git worktree list
    git worktree remove --force <path>
    git switch main
    git pull --ff-only origin main

STEPS:

1. Read `_bmad-output/implementation-artifacts/sprint-status.yaml`. Note current story
   statuses. Compare against the existing graph (if any) to identify new stories.

2. Read `_bmad-output/planning-artifacts/epics.md` for dependency relationships of
   new stories. (Skip if no new stories.)

3. Run /bmad-help with the epic context for new stories — ask it to map their
   dependencies. Merge the result into the existing graph. (Skip if no new stories.)

4. Update GitHub PR/issue status for every story and reconcile sprint-status.yaml.
   Follow the procedure in `references/phase0-dependency-graph.md` exactly.

5. Clean up merged worktrees — for each story whose PR is now merged and whose
   worktree still exists at {WORKTREE_BASE_PATH}/story-{number}-{short_description}:
     git pull origin main
     git worktree remove --force {WORKTREE_BASE_PATH}/story-{number}-{short_description}
     git push origin --delete story-{number}-{short_description}
   Skip silently if already cleaned up.

6. Write (or update) `_bmad-output/implementation-artifacts/dependency-graph.md`.
   Follow the schema, Ready to Work rules, and example in
   `references/phase0-dependency-graph.md` exactly.

7. Pull latest main (if step 5 didn't already do so):
     git pull origin main

REPORT BACK to the coordinator with this structured summary:
  - ready_stories: list of { number, short_description, status } for every story
    marked "Ready to Work: Yes" that is not done
  - all_stories_done: true/false — whether every story across every epic is done
  - current_epic: name/number of the lowest incomplete epic
  - any warnings or blockers worth surfacing
```

The coordinator uses the report to drive Phase 1. No coordinator-side file reads.

📣 **Notify** after Phase 0:
```
📊 Phase 0 complete
Ready: {N} stories — {comma-separated story numbers}
Blocked: {N} stories (if any)
```

---

## Phase 1: Discover Stories

Pure coordinator logic — no file reads, no tool calls.

1. From Phase 0's `ready_stories` report, select at most `MAX_PARALLEL_STORIES` stories.
   - **Epic ordering is strictly enforced:** only pick stories from the lowest incomplete epic. Never pick a story from epic N if any story in epic N-1 (or earlier) is not yet merged — check this against the Phase 0 report.
2. **If no stories are ready** → report to the user which stories are blocked (from Phase 0 warnings), then jump to **Phase 4, Step 3 (Gate & Continue)**.

> **Why epic ordering matters:** Stories in later epics build on earlier epics' code and product foundation. Starting epic 3 while epic 2 has open PRs risks merge conflicts and building on code that may still change.

---

## Phase 2: Run the Pipeline

Launch all stories' Step 1 subagents **in a single message** (parallel). Each story's steps are **strictly sequential** — do not spawn step N+1 until step N reports success.

**Skip steps based on story status** (from Phase 0 report):

| Status          | Start from | Skip      |
|-----------------|------------|-----------|
| `backlog`       | Step 1     | nothing   |
| `ready-for-dev` | Step 2     | Step 1    |
| `in-progress`   | Step 2     | Step 1    |
| `review`        | Step 3     | Steps 1–2 |
| `done`          | —          | all       |

**After each step:** run **Pre-Continuation Checks** (see `references/pre-continuation-checks.md`) before spawning the next subagent. Pre-Continuation Checks are the only coordinator-side work between steps.

**On failure:** stop that story's pipeline. Report step, story, and error. Other stories continue.  
**Exception:** rate/usage limit failures → run Pre-Continuation Checks (which auto-pauses until reset) then retry.

📣 **Notify per story** as each pipeline concludes (Step 4 success or any step failure):
- Success: `✅ Story {number} done — PR #{pr_number}`
- Failure: `❌ Story {number} failed at Step {N} — {brief error}`

### Step 1: Create Story (`MODEL_STANDARD`)

Spawn with model `MODEL_STANDARD` (yolo mode):
```
You are the Step 1 story creator for story {number}-{short_description}.
Working directory: {repo_root}. Auto-approve all tool calls (yolo mode).

1. Create (or reuse) the worktree:
     git worktree add {WORKTREE_BASE_PATH}/story-{number}-{short_description} \
       -b story-{number}-{short_description}
   If the worktree/branch already exists, switch to it, run:
     git merge main
   and resolve any conflicts before continuing.

2. Change into the worktree directory:
     cd {repo_root}/{WORKTREE_BASE_PATH}/story-{number}-{short_description}

3. Run /bmad-create-story {number}-{short_description}.

4. Update sprint-status.yaml at the REPO ROOT (not the worktree copy):
     _bmad-output/implementation-artifacts/sprint-status.yaml
   Set story {number} status to `ready-for-dev`.

Report: success or failure with error details.
```

### Step 2: Develop Story (`MODEL_STANDARD`)

Spawn with model `MODEL_STANDARD` (yolo mode):
```
You are the Step 2 developer for story {number}-{short_description}.
Working directory: {repo_root}/{WORKTREE_BASE_PATH}/story-{number}-{short_description}.
Auto-approve all tool calls (yolo mode).

1. Run /bmad-dev-story {number}-{short_description}.
2. Commit all changes when implementation is complete.
3. Update sprint-status.yaml at the REPO ROOT:
     {repo_root}/_bmad-output/implementation-artifacts/sprint-status.yaml
   Set story {number} status to `review`.

Report: success or failure with error details.
```

### Step 3: Code Review (`MODEL_QUALITY`)

Spawn with model `MODEL_QUALITY` (yolo mode):
```
You are the Step 3 code reviewer for story {number}-{short_description}.
Working directory: {repo_root}/{WORKTREE_BASE_PATH}/story-{number}-{short_description}.
Auto-approve all tool calls (yolo mode).

1. Run /bmad-code-review {number}-{short_description}.
2. Auto-accept all findings and apply fixes using your best engineering judgement.
3. Commit any changes from the review.

Report: success or failure with error details.
```

### Step 4: PR & CI (`MODEL_STANDARD`)

Spawn with model `MODEL_STANDARD` (yolo mode):
```
You are the Step 4 PR and CI agent for story {number}-{short_description}.
Working directory: {repo_root}/{WORKTREE_BASE_PATH}/story-{number}-{short_description}.
Auto-approve all tool calls (yolo mode).

1. Commit all outstanding changes.

2. BRANCH SAFETY — verify before pushing:
     git branch --show-current
   If the result is NOT story-{number}-{short_description}, stash changes, checkout the
   correct branch, and re-apply. Never push to main or create a new branch.

3. Run /commit-commands:commit-push-pr.
   PR title: story-{number}-{short_description} - fixes #{gh_issue_number}
   (look up gh_issue_number from the epic file or sprint-status.yaml; omit "fixes #" if none)
   Add "Fixes #{gh_issue_number}" to the PR description if an issue number exists.

4. CI:
   - If RUN_CI_LOCALLY is true → skip GitHub Actions and run the Local CI Fallback below.
   - Otherwise monitor CI in a loop:
       gh run view
     - Billing/spending limit error → exit loop, run Local CI Fallback
     - CI failed for other reason, or Claude bot left PR comments → fix, push, loop
     - CI green → proceed to step 5

LOCAL CI FALLBACK (when RUN_CI_LOCALLY=true or billing-limited):
  a. Read all .github/workflows/ files triggered on pull_request events.
  b. Extract and run shell commands from each run: step in order (respecting
     working-directory). If any fail, diagnose, fix, and re-run until all pass.
  c. Commit fixes and push to the PR branch.
  d. Post a PR comment:
     ## Test Results (manual — GitHub Actions skipped: billing/spending limit reached)
     | Check | Status | Notes |
     |-------|--------|-------|
     | `<command>` | ✅ Pass / ❌ Fail | e.g. "42 tests passed" |
     ### Fixes applied
     - [failure] → [fix]
     All rows must show ✅ Pass before this step is considered complete.

5. CODE REVIEW — spawn a dedicated MODEL_DEV subagent (yolo mode) after CI passes:
   ```
   You are the code review agent for story {number}-{short_description}.
   Working directory: {repo_root}/{WORKTREE_BASE_PATH}/story-{number}-{short_description}.
   Auto-approve all tool calls (yolo mode).

   1. Run /code-review:code-review (reads the PR diff via gh pr diff).
   2. For every finding, apply a fix using your best engineering judgement.
      Do not skip or defer any finding — fix them all.
   3. Commit all fixes and push to the PR branch.
   4. If any fixes were pushed, re-run /code-review:code-review once more to confirm
      no new issues were introduced. Repeat fix → commit → push → re-review until
      the review comes back clean.

   Report: clean (no findings or all fixed) or failure with details.
   ```
   Wait for the subagent to report before continuing. If it reports failure,
   stop this story and surface the error.

6. Update sprint-status.yaml at the REPO ROOT:
     {repo_root}/_bmad-output/implementation-artifacts/sprint-status.yaml
   Set story {number} status to `done`.

Report: success or failure, and the PR number/URL if opened.
```

---

## Phase 3: Auto-Merge Batch PRs (when `AUTO_PR_MERGE=true`)

After all batch stories complete Phase 2, merge every successful story's PR into `main` — one subagent per story, **sequentially** (lowest story number first).

> **Why sequential:** Merging lowest-first ensures each subsequent merge rebases against a main that already contains its predecessors — keeping conflict resolution incremental and predictable.

**Steps:**

1. Collect all stories from the current batch that reached Step 4 successfully (have a PR). Sort ascending by story number.
2. For each story **sequentially** (wait for each to complete before starting the next):
   - Pull latest main at the repo root: spawn a quick subagent or include in the merge subagent.
   - Spawn a `MODEL_STANDARD` subagent (yolo mode) with the instructions from `references/phase4-auto-merge.md`.
   - Run Pre-Continuation Checks after the subagent completes. If it fails (unresolvable conflict, CI blocking), report the error and continue to the next story.
3. Print a merge summary (coordinator formats from subagent reports):
   ```
   Auto-Merge Results:
   Story   | PR    | Outcome
   --------|-------|--------
   6.1     | #142  | Merged ✅
   6.2     | #143  | Merged ✅ (conflict resolved: src/foo.ts)
   6.3     | #144  | Failed ❌ (CI blocking — manual merge required)
   ```
📣 **Notify** after all merges are processed (coordinator formats from subagent reports):
```
🔀 Auto-merge complete
{story}: ✅ PR #{pr} | {story}: ✅ PR #{pr} (conflict resolved) | {story}: ❌ manual merge needed
```

4. Spawn a **cleanup subagent** (`MODEL_STANDARD`, yolo mode):
   ```
   Post-merge cleanup. Auto-approve all tool calls (yolo mode).

   1. Verify sprint-status.yaml at the repo root has status `done` for all merged stories.
      Fix any that are missing.

   2. Repo root branch safety check:
        git branch --show-current
      If not main:
        git restore .
        git switch main
        git reset --hard origin/main
      If switch fails because a worktree claims the branch:
        git worktree list
        git worktree remove --force <path>
        git switch main
        git reset --hard origin/main

   3. Pull main:
        git pull --ff-only origin main

   Report: done or any errors encountered.
   ```

---

## Phase 4: Batch Completion & Continuation

### Step 1: Print Batch Summary

Coordinator prints immediately — no file reads, formats from Phase 2 step results:

```
Story   | Step 1 | Step 2 | Step 3 | Step 4 | Result
--------|--------|--------|--------|--------|-------
9.1     |   OK   |   OK   |   OK   |   OK   | PR #142
9.2     |   OK   |   OK   |  FAIL  |   --   | Review failed: ...
9.3     |   OK   |   OK   |   OK   |   OK   | PR #143
```

If arriving from Phase 1 with no ready stories:
```
No stories ready to work on.
Blocked stories: {from Phase 0 report}
```

📣 **Notify** with the batch summary (same content, condensed to one line per story):
```
📦 Batch complete — {N} stories
{number} ✅ PR #{pr} | {number} ❌ Step {N} | ...
```
Or if no stories were ready: `⏸ No stories ready — waiting for PRs to merge`

### Step 2: Check for Epic Completion

Spawn an **assessment subagent** (`MODEL_STANDARD`, yolo mode):
```
Epic completion assessment. Auto-approve all tool calls (yolo mode).

Read:
  - _bmad-output/planning-artifacts/epics.md
  - _bmad-output/implementation-artifacts/sprint-status.yaml

Report back:
  - current_epic_complete: true/false (all stories done or have open PRs)
  - all_epics_complete: true/false (every story across every epic is done)
  - current_epic_name: name/number of the lowest incomplete epic
  - next_epic_name: name/number of the next epic (if any)
  - stories_remaining: count of non-done stories in the current epic
```

Using the assessment report:

**If `current_epic_complete = true`:**
1. Print: `🎉 Epic {current_epic_name} is complete! Starting retrospective countdown ({RETRO_TIMER_SECONDS ÷ 60} minutes)...`

   📣 **Notify:** `🎉 Epic {current_epic_name} complete! Running retrospective in {RETRO_TIMER_SECONDS ÷ 60} min...`
2. Start a timer using the **[Timer Pattern](#timer-pattern)** with:
   - **Duration:** `RETRO_TIMER_SECONDS`
   - **Fire prompt:** `"BAD_RETRO_TIMER_FIRED — The retrospective countdown has elapsed. Auto-run the retrospective: spawn a MODEL_DEV subagent (yolo mode) to run /bmad-retrospective, accept all changes. Run Pre-Continuation Checks after it completes, then proceed to Phase 4 Step 3."`
   - **[C] label:** `Run retrospective now`
   - **[S] label:** `Skip retrospective`
   - **[C] / FIRED action:** Spawn MODEL_DEV subagent (yolo mode) to run `/bmad-retrospective`. Accept all changes. Run Pre-Continuation Checks after.
   - **[S] action:** Skip retrospective.
3. Proceed to Step 3 after the retrospective decision resolves.

### Step 3: Gate & Continue

Using the assessment report from Step 2, follow the applicable branch:

**Branch A — All epics complete (`all_epics_complete = true`):**
```
🏁 All epics are complete — sprint is done! BAD is stopping.
```
📣 **Notify:** `🏁 Sprint complete — all epics done! BAD is stopping.`

**Branch B — More work remains:**

1. Print a status line:
   - Epic just completed: `✅ Epic {current_epic_name} complete. Next up: Epic {next_epic_name} ({stories_remaining} stories remaining).`
   - More stories in current epic: `✅ Batch complete. Ready for the next batch.`
2. Start a timer using the **[Timer Pattern](#timer-pattern)** with:
   - **Duration:** `WAIT_TIMER_SECONDS`
   - **Fire prompt:** `"BAD_WAIT_TIMER_FIRED — The post-batch wait has elapsed. Run Pre-Continuation Checks, then re-run Phase 0, then proceed to Phase 1."`
   - **[C] label:** `Continue now`
   - **[S] label:** `Stop BAD`
   - **[C] / FIRED action:** Run Pre-Continuation Checks, then re-run Phase 0.
   - **[S] action:** Stop BAD, print a final summary, and 📣 **Notify:** `🛑 BAD stopped by user.`
3. After Phase 0 completes:
   - At least one story unblocked → proceed to Phase 1.
   - All stories still blocked → print which PRs are pending (from Phase 0 report), restart Branch B for another `WAIT_TIMER_SECONDS` countdown.

---

## Notify Pattern

Use this pattern every time a `📣 Notify:` callout appears **anywhere in this skill** — including inside the Timer Pattern.

**If `NOTIFY_SOURCE="telegram"`:** call `mcp__plugin_telegram_telegram__reply` with:
- `chat_id`: `NOTIFY_CHAT_ID`
- `text`: the message

**If `NOTIFY_SOURCE="terminal"`** (or if the Telegram tool call fails): print the message in the conversation as a normal response.

Always send both a terminal print and a channel message — the terminal print keeps the in-session transcript readable, and the channel message reaches the user on their device.

---

## Timer Pattern

Both the retrospective and post-batch wait timers use this pattern. The caller supplies the duration, fire prompt, option labels, and actions.

Behaviour depends on `TIMER_SUPPORT`:

---

### If `TIMER_SUPPORT=true` (native platform timers)

**Step 1 — compute target cron expression** (convert seconds to minutes: `SECONDS ÷ 60`):
```bash
# macOS
date -v +{N}M '+%M %H %d %m *'
# Linux
date -d '+{N} minutes' '+%M %H %d %m *'
```
Save as `CRON_EXPR`. Save `TIMER_START=$(date +%s)`.

**Step 2 — create the one-shot timer** via `CronCreate`:
- `cron`: expression from Step 1
- `recurring`: `false`
- `prompt`: the caller-supplied fire prompt

Save the returned job ID as `JOB_ID`.

**Step 3 — print the options menu** (always all three options):
> Timer running (job: {JOB_ID}). I'll act in {N} minutes.
>
> - **[C] Continue** — {C label}
> - **[S] Stop** — {S label}
> - **[M] {N} Modify timer to {N} minutes** — shorten or extend the countdown

📣 **Notify** using the [Notify Pattern](#notify-pattern) with the same options so the user can respond from their device:
```
⏱ Timer set — {N} minutes (job: {JOB_ID})

[C] {C label}
[S] {S label}
[M] <minutes> — modify countdown
```

Wait for whichever arrives first — user reply or fired prompt. On any human reply, print elapsed time first:
```bash
ELAPSED=$(( $(date +%s) - TIMER_START ))
echo "⏱ Time elapsed: $((ELAPSED / 60))m $((ELAPSED % 60))s"
```

- **[C]** → `CronDelete(JOB_ID)`, run the [C] action
- **[S]** → `CronDelete(JOB_ID)`, run the [S] action
- **[M] N** → `CronDelete(JOB_ID)`, recompute cron for N minutes from now, `CronCreate` again with same fire prompt, update `JOB_ID` and `TIMER_START`, print updated countdown, then 📣 **Notify** using the [Notify Pattern](#notify-pattern):
  ```
  ⏱ Timer updated — {N} minutes (job: {JOB_ID})

  [C] {C label}
  [S] {S label}
  [M] <minutes> — modify countdown
  ```
- **FIRED (no prior reply)** → run the [C] action automatically

---

### If `TIMER_SUPPORT=false` (prompt-based continuation)

Save `TIMER_START=$(date +%s)`. No native timer is created — print the options menu immediately and wait for user reply:

> Waiting {N} minutes before continuing. Reply when ready.
>
> - **[C] Continue** — {C label}
> - **[S] Stop** — {S label}
> - **[M] N** — remind me after N minutes (reply with `[M] <minutes>`)

📣 **Notify** using the [Notify Pattern](#notify-pattern) with the same options.

On any human reply, print elapsed time first:
```bash
ELAPSED=$(( $(date +%s) - TIMER_START ))
echo "⏱ Time elapsed: $((ELAPSED / 60))m $((ELAPSED % 60))s"
```

- **[C]** → run the [C] action
- **[S]** → run the [S] action
- **[M] N** → update `TIMER_START`, print updated wait message, 📣 **Notify**, and wait again

---

## Rules

1. **Delegate mode only** — never read files, run git/gh commands, or write to disk yourself. The only platform command the coordinator may run directly is context compaction via Pre-Continuation Checks (when `CONTEXT_COMPACTION_THRESHOLD` is exceeded). All other slash commands and operations are delegated to subagents.
2. **One subagent per step per story** — spawn only after the previous step reports success.
3. **Sequential steps within a story** — Steps 1→2→3→4 run strictly in order.
4. **Parallel stories** — launch all stories' Step 1 in one message (one tool call per story). Phase 3 runs sequentially by design.
5. **Dependency graph is authoritative** — never pick a story whose dependencies are not fully merged. Use Phase 0's report, not your own file reads.
6. **Phase 0 runs before every batch** — always after the Phase 4 wait. Always as a fresh subagent.
7. **Confirm success** before spawning the next subagent.
8. **sprint-status.yaml is updated by step subagents** — each step subagent writes to the repo root copy. The coordinator never does this directly.
9. **On failure** — report the error, halt that story. No auto-retry. **Exception:** rate/usage limit failures → run Pre-Continuation Checks (auto-pauses until reset) then retry.
10. **Issue all Step 1 subagent calls in one response** when Phase 2 begins. After each story's Step 1 completes, issue that story's Step 2 — never wait for all stories' Step 1 to finish before issuing any Step 2.

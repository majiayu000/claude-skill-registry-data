---
name: jarvis
description: A watch loop that polls git change volume in a self-paced manner and automatically runs the jarvis-once one-shot review when new change has accrued since the last review, a risk path changed, or a new commit appeared. Repetition rides on /loop's self-paced mode, so it must be launched as /loop /jarvis. There is no fixed line/file threshold. Configure strength preset, polling intervals, paths, and risk paths via args (key=value). When called without args, it asks for strength once on first run (previous settings auto-restore from .jarvis/args). Right after first load it polls quickly for a short while (warmup). Use for "jarvis", "change-detection review loop", "jarvis watch" requests.
---

# jarvis

A self-paced watch loop that cheaply polls git change volume while a human writes code directly, and once **new change has accrued since the last review** (no volume threshold), automatically runs the `jarvis-once` (one-shot navigator) skill once.

- **Polling uses almost no tokens** (one `git diff --shortstat`). The expensive `jarvis-once` full review runs only when new change has accrued since the last review, a risk path changed, or a new commit appeared.
- **It is not event-driven.** There is no OS event that wakes it in real time on a human's hand edits, so it checks via periodic wakes. Instead, it keeps the check itself extremely cheap.
- **`jarvis-once` does not fix code directly** (review/suggest/next steps only). If the human says "fix this," that turn switches to normal development mode.

> **Naming:** `jarvis` (this skill) = *the persistent watch loop* (entry point). `jarvis-once` = the *one-shot navigator that runs exactly once* when triggered. When the watch wakes, it calls `jarvis-once`.

## Execution — self-repeating via `/loop`

This skill must be launched as **`/loop /jarvis [args]`**. The engine of repetition is `/loop`'s **self-paced (dynamic) mode**, and on top of it the `ScheduleWakeup` in procedure 4 picks the next tick's interval on its own.

> ⚠️ **`ScheduleWakeup` only works inside `/loop` dynamic mode.** Called from a bare `/jarvis` (i.e. without `/loop`), it returns as if it succeeded but **schedules nothing and is silently ignored.** So if you launch without `/loop`, the loop dies right after the first tick. The entry point is always `/loop /jarvis`.

> ⚠️ **Don't give `/loop` its own interval.** Launch it **without an interval** (`/loop /jarvis`) so it enters dynamic mode and procedure 4's `ScheduleWakeup` (= `active`/`idle`/`debounce`) drives the cadence. Giving `/loop` a fixed interval (`/loop 5m /jarvis`) makes that fixed schedule win and jarvis's `active`/`idle` are **ignored.** Always tune cadence via jarvis args — e.g. `/loop /jarvis active=3m idle=20m` or `/loop /jarvis strength=high`. (On Bedrock/Vertex/Foundry, even a no-interval `/loop` runs on a fixed schedule, so self-pacing does not apply.)

- **Start**: The user calls `/loop /jarvis [args]` once. → Perform this tick and, at the end, always schedule the next run with `ScheduleWakeup` (echoing the current args in the prompt). `/loop` takes this schedule and fires the next tick.
- **Persist**: When the scheduled wake fires, `/jarvis [args]` runs again and schedules yet another wake. This way the loop is maintained without any further user input.
- **Invariant**: Unless there is an intent to terminate (see "Stop" below), **every tick must call `ScheduleWakeup` at its end.** Omitting this call leaves no next wake scheduled and kills the loop.
- **If launched as a bare `/jarvis` (without `/loop`)**: the skill cannot tell at runtime whether it is inside `/loop` or not. So it performs this one tick normally but, at the end of the first-boot tick output, leaves a notice (procedure 0.7): **"if you launched without `/loop`, this stops after this tick — relaunch as `/loop /jarvis` for continuous watch."** If it was under `/loop` it keeps repeating; if not, it stops here as the notice says.

## Arguments (args, key=value)

| key | meaning | default |
|-----|------|--------|
| `strength` | **Strength preset.** Sets the polling-interval knobs below as a bundle in one go (`low`/`medium`/`high`). If individual knobs are given alongside, only those items are overridden. See "Strength preset" below. | `medium` |
| `active` | Next wake interval when `jarvis-once` ran on the previous wake or the working tree has changes | `4m` |
| `idle` | Next wake interval when there is no change (working tree clean) | `25m` |
| `debounce` | **Quiet time after which the conversation is considered to have stopped.** Even if conditions to review are met, if the human is mid-conversation, defer execution and reschedule briefly at this interval. Every time the human says something, the timer resets. | `90s` |
| `warmup` | **Number of fast-polling ticks on first load.** Right after boot, for this many ticks, recheck at the `active` interval instead of `idle` even when there is no change (fast response when first turned on). `0` turns it off. | `3` |
| `paths` | Limit the watch target to these paths (whole tree if omitted) | (whole tree) |
| `risk` | **Risk path** glob — files matching this wake `jarvis-once` regardless of volume (even a single newly changed line). Comma-separate multiple. | (none/off) |
| `focus` | **Focus area directory.** The `.md` collected here is viewed as a priority lens during review (see "Convention document collection" item 4). | `.claude/jarvis/focus/` |
| `mirror` | **Mirror (gray-zone visualization).** If a substantial part of the cumulative changes is code *generated* in this session, point it out with a one-line memo on "whether you grasped it yourself" (non-enforcing). Turn off with `off`. See procedure 3.5 below. | `on` |
| `plan` | **Plan mode.** On first boot, asks whether to draft a plan + checklist for this work (procedure 0.55). `off` skips the question (behaves exactly as today). A source (`plan=PROJ-123`, a URL, or a file path) opts in *and* names the source, skipping both questions. Once a plan exists (`.jarvis/checklist.md` present), the watch reviews against it every gated tick. | (ask on first boot) |

> **The commit-boundary trigger is always on, independent of args.** When a new commit is detected, `jarvis-once` runs once on that commit's changes regardless of accrued volume. This is because right before/after a mistake is sealed into code is the golden time for a warning. (manifesto: "AI actively warns about human mistakes")

Examples:

```
/loop /jarvis                                         # no args → asks for strength once (medium default thereafter)
/loop /jarvis strength=high                            # strong — poll tightly (catch new change fast)
/loop /jarvis strength=low                             # weak — poll rarely
/loop /jarvis strength=high idle=30m                   # high preset + override only idle to 30m
/loop /jarvis paths=src/billing active=3m              # specific path only, more frequent
/loop /jarvis risk=**/*payment*,**/*auth*             # payment/auth warned immediately on a single changed line
```

> The entry is always `/loop /jarvis` (without `/loop` it does not repeat — see "Execution" above). The `ScheduleWakeup` echo prompt holds just `/jarvis [args]` without the `/loop` prefix — `/loop` fires the next tick with that prompt (procedure 4).

Argument parsing rules:
- Only `key=value` form is recognized. Unrecognized tokens are ignored and defaults are used.
- Interpret `strength` first to lay down the preset knob bundle, then overlay the remaining individual key=value on top (individual knobs win). If `strength` is unspecified, equivalent to `medium`.
- The `strength` value allows aliases (see "Strength preset" table). If the value is unrecognized, fall back to `medium`.
- Time intervals allow `s`/`m`/`h` suffixes (`90s`, `4m`, `1h`). A bare number is treated as minutes.
- `active`/`idle` are clamped to [60s, 3600s] at runtime.
- `paths`/`risk` separate multiple values with commas (`,`). Glob patterns are allowed.

## Strength preset (strength)

Use a single `strength` to bundle "how tightly to poll." Each preset expands into the knob bundle below, and if individual knobs (`active=`, etc.) are present in the same call, **only those items** override the preset values. (Since there is no line/file threshold, the preset changes *polling frequency*, not *volume sensitivity*.)

| `strength` | aliases | `active` | `idle` | `debounce` | character |
|-----------|------|----------|--------|------------|------|
| `low` | `약`, `약하게`, `느슨`, `relaxed`, `1` | `8m` | `40m` | `120s` | Poll rarely. Minimal noise, minimal cost |
| `medium` | `중`, `보통`, `normal`, `2` | `4m` | `25m` | `90s` | Default. Balanced |
| `high` | `강`, `강하게`, `촘촘`, `aggressive`, `3` | `3m` | `12m` | `60s` | Poll tightly. Catches new change/commits fastest |

Rules:
- The preset touches only the 3 knobs above (`active`/`idle`/`debounce`). `paths`/`risk` are specified separately, independent of the preset.
- Even with `strength=high`, the severity threshold of `jarvis-once` itself is unchanged — strength only raises the *polling frequency* (how fast new change is caught), not the nagging (see cost guide). So you can raise it with peace of mind.
- When scheduling the next wake, serialize the echoed args as **`strength=<value>` (+ individual overrides) as-is, not the expanded individual knobs.** That way the preset's meaning is preserved.

## Marker files

The baseline at the time of the last review is stored in `.jarvis/baseline`. Since it lives in the working tree, register `.jarvis/` in `.gitignore` so it is not committed (it operates as independent local state per clone), and if the directory does not exist, create it with `mkdir -p .jarvis` before writing.

> **Why not use `.git/`:** The inside of `.git/` is a sensitive path, requiring permission approval on every write, which is unsuitable for an unattended loop. `.jarvis/` is an ordinary working-tree path with no permission friction, and guaranteeing it is untracked via `.gitignore` preserves the original benefit of "not committed + local only" as-is.

Format (one line): `lines=<int> risk=<int> head=<commit SHA> deferred=<0|1> boot=<int> mirrored=<0|1>`
If the file does not exist, treat it as `lines=0 risk=0 head= deferred=0 boot=0 mirrored=0`. (If an old-version file lacks `boot`/`mirrored`, treat them as 0; if a leftover `files` field is present, ignore it.)
- `lines`: working-tree changed line count at the time of the last review. This is the baseline for deciding "has new change accrued since the last review."
- `risk`: changed line count on risk paths (`risk` glob) at the time of the last review (0 if risk unset)
- `head`: the `git rev-parse HEAD` value **observed on the previous tick.** Used for commit-boundary detection.
- `deferred`: whether there is a **deferred review** that met conditions to review but was held off because of an ongoing conversation (debounce wait). If 1, flush the moment the conversation stops.
- `boot`: remaining **warmup tick count.** Initialized to `warmup` at boot and decremented by 1 each tick. If `>0`, even no-change ticks poll at the `active` interval instead of `idle` (fast response right after first load).
- `mirrored`: **mirror cooldown flag.** Set to 1 after showing the mirror (procedure 3.5) to prevent repeated firing every tick. Released to 0 when human-typed changes again dominate or a review is flushed.

### Control state files (under `.jarvis/`)

The watch's progress is controlled by the 2 files below. Both are under `.jarvis/`, so they are untracked and local-only via `.gitignore`, and **each is a one-line, fixed-size state file overwritten every tick (not a growing cache).**

| file | role | created/deleted by |
|------|------|----------------|
| `.jarvis/baseline` | The watch baseline in the format above. The core of loop progress state. If it remains on disk, the next `/loop /jarvis` continues watching from that point (= resume). | written every tick / deleted by `/jarvis-reset` |
| `.jarvis/args` | The effective args string of the previous tick (e.g., `strength=medium`). Updated every tick. If the next start is invoked **with no args**, jarvis reads this value and auto-resumes with the same settings (procedure 0.4). Default (medium) if absent. | written every tick / deleted by `/jarvis-reset` |
| `.jarvis/status` | **A one-line liveness state** (see "Liveness" below). At the end of every tick it records the next wake time (`next_wake` epoch), interval, and strength. The statusline script reads this file to continuously show "watching / stalled?" **between** ticks. | written every tick / deleted by `/jarvis-reset` |
| `.jarvis/stopped` | **An event-based "stopped" flag** (see "Liveness (C)"). The Stop hook (`assets/loop-watch-hook.sh`) drops it when a turn ends with no `/jarvis` wakeup pending. If present, the statusline shows "stopped" **instantly** with no time inference; the hook clears it while a wakeup is alive. | written/cleared by the Stop hook / deleted by `/jarvis-reset` |
| `.jarvis/plan.md` | **The approved plan document** (goal / scope / approach / open questions). Written once by `jarvis-plan` after the human approves. Its presence + `checklist.md` means **plan mode is active.** Durable (not a per-tick one-liner). | written by `jarvis-plan` on opt-in / deleted by `/jarvis-reset` (with confirmation) |
| `.jarvis/checklist.md` | **The work checklist** — markdown `- [ ]`/`- [x]` items. **The human owns the checkmarks**; the watch reads it each gated review to know what's officially done and re-assesses the rest. Progress = ticked/total. Its presence is what the watch keys "plan mode active" on. | created by `jarvis-plan`, ticked by the human / deleted by `/jarvis-reset` (with confirmation) |

> **Lifecycle (on top of `/loop`):** Start/resume is `/loop /jarvis` — if baseline/args remain, it continues from that state. Stop/pause is interrupting the `/loop` itself (Esc) — no next wake gets scheduled so the loop ends, and baseline/args stay on disk waiting to resume. Full reset is **`/jarvis-reset`** (an independent skill: delete baseline/args → next start is a first boot). Loop termination has no teardown hook, so state cleanup only happens at start time (self-correction) and via `/jarvis-reset`. (The old `.jarvis/paused` flag and `/jarvis-pause`·`/jarvis-resume`·`/jarvis-stop` are no longer used.)

## Convention document collection (performed only right before calling `jarvis-once`)

Performed only the moment it is decided to actually call `jarvis-once` (procedure 2a or 3 satisfied). On ticks with no review this is a waste of tokens, so **do not do it.**

Purpose: let `jarvis-once` review with knowledge of "this package's, this directory's rules." `CLAUDE.md` and `.claude/rules/**` are auto-injected by the harness, so **do not collect them redundantly.** Gather only on-demand documents.

First obtain the list of changed files:

```bash
git diff --name-only HEAD [-- paths]      # when woken by the gate (working tree)
git diff --name-only <base_head>..<cur_head>   # when woken by the commit boundary
```

Based on those paths, collect the following (only what exists, and **do not re-read if already in context**):

0. **Task plan & checklist (only when plan mode is active — `.jarvis/checklist.md` exists)** — read `.jarvis/plan.md` and `.jarvis/checklist.md` and pass them to `jarvis-once` as the **"task spec" (highest priority)**. This is what the change is *supposed* to accomplish, so it outranks even the focus area: jarvis-once reviews the change against the checklist (which items it advances, whether they look complete, what's missing or risky per item). See procedure 3.6.
1. **Nearest `AGENTS.md`** — going up from each changed file's directory, the first `AGENTS.md` encountered. (e.g., a change in `packages/billing/**` → `packages/billing/AGENTS.md`)
2. **Directory `README.md`** — if the directory containing the changed file has a `README.md`, that file.
3. **`.claude/rules/**` rule documents corresponding to the changed files** — pick out only the rules matching the changed files' kind/path (not all of them) to reference. No matter what axis the project organized `.claude/rules/` along (per-language, per-layer, per-feature, per-directory), choose only the 1–3 most relevant to the changed files. Rule file/directory names are themselves application hints (e.g., if you changed a UI file, `ui`/`view` kinds; if you changed tests, `test` kinds; if you changed payments, `payment`/`billing` kinds). Don't rely on a hardcoded per-language mapping — **discover them from the rule files the project actually has.** Skip rules already auto-injected.
4. **Focus area documents (`focus` directory, default `.claude/jarvis/focus/**`)** — where the user has gathered "what I especially want reviewed carefully in this project." If it exists, collect the `.md` inside it (excluding README) and pass it to `jarvis-once` as **"focus area"** context. Unlike the general conventions in 1–3 above, this is a **priority lens** — jarvis-once looks at it before the general detection catalog. You can change the location with the `focus=<path>` argument. (This directory is always collected on a tick where you actually decided to review, regardless of the changed files.)

Avoid duplication/over-collection: if several changed files share the same `AGENTS.md`, read it only once. If the collection volume is excessive, limit it to the 1–2 top directories with the most changed files.

Pass the collected content along when calling `jarvis-once` — distinguish 0 as the **"task spec (highest priority)"**, 1–3 as **"reference conventions"**, and 4 as **"focus area (priority)."** (The persona (`persona.md`) is read directly by `jarvis-once` from its own directory, so the watch does not collect it.)

## Jarvis output markers (required)

When delivering the `jarvis-once` review result to the user, always wrap the start/end with the markers below so it is visible that the content is **auto-generated by Jarvis.** This is to distinguish output the watch produced automatically from normal conversation.

**Start marker:**

```
╭─🤖 JARVIS ─────────────── (jarvis auto-observe)
```

**End marker:**

```
╰─🤖 JARVIS ─────────────── you hold the keyboard · the call is yours
```

Rules:
- Wrap only when `jarvis-once` actually says something (when there is review content). Do not attach markers to silence at the level of "nothing in particular catches my eye" or a one-line no-new-change notice.
- Leave the body between the markers exactly as `jarvis-once` generated it. Put the watch's (`jarvis`) own operational messages (scheduling, debounce notices, etc.) **outside** the markers.
- The tail phrase of the end marker is a fixed phrase reminding that authorship belongs to the human.

## Start banner (first tick only)

Output the `JARVIS` ASCII logo banner **once**, only on the tick when `/jarvis` **first starts up**. Decision criterion: if the `.jarvis/baseline` file **does not yet exist**, this is the first boot tick (subsequent ticks will have a baseline, so it is not auto-re-output). Do not output it on scheduled wakes or subsequent ticks — repetition is noise.

**Always visible — must be output directly in the "assistant response body" as a code fence.**
If emitted only via `cat`, the Claude Code UI folds long tool output (requires Ctrl+O) and the banner is not immediately visible. Therefore:
1. Read `assets/jarvis-banner.txt` (no need to re-read if already in context) to obtain its content, and
2. Output that content by **pasting it as-is into a triple-backtick (```) code block inside the response message.** (Since it is body, not tool output, it always shows expanded.)

- Color: body markdown cannot render ANSI colors, so it goes out **monochrome.** This logo clearly reveals the `JARVIS` shape with block glyphs (`█`) and box corners (`╗╝╚╔║═`). (If you really need color, `cat` `assets/jarvis-banner.ansi` in a **raw terminal** — but it folds in the Claude Code UI.)
- Original art: `assets/jarvis-banner.txt`. (`colorize.sh` → `.ansi` is kept only as a color fallback for raw terminals.)
- The banner is a watch operational message, so put it **outside** the "Jarvis output markers" (╭─🤖). Add a one-line caption below the banner:
  `J · A · R · V · I · S  —  watch online · you hold the keyboard`

## Per-run (wake) procedure

> This skill performs the following from start to finish on every wake.

### 0. Human-first + conversation-activity decision (debounce)
**`active_chat` decision:** Is there a message sent by the human since the previous tick (the previous `ScheduleWakeup` firing)? Decide from the tail of the transcript.
- If there was a discussion/implementation message from the human → `active_chat = true` (in conversation)
- If this tick is purely a scheduled firing → `active_chat = false` (quiet)

If `active_chat == true` and the human is requesting something, **focus on that request first (answering the question, writing code, running the command).** Do not interrupt the conversation with watch output. Defer the review; the debounce branch in procedure 3/2a handles it (rescheduled at the `debounce` interval in procedure 4).

This `active_chat` value is used in the "may speak" decision of procedures 2a/3.

### 0.4. Auto-restore saved settings (on resume)
If this call has **no recognized args at all** and the `.jarvis/args` file exists, read its one line and use it as this tick's effective args (auto-resume with the previous settings). This way, even after stopping the loop with an interrupt (Esc) and relaunching with `/loop /jarvis` (no args), the previous `strength` etc. are restored — no separate resume command needed.

```bash
cat .jarvis/args 2>/dev/null || true
```

- If even one arg was given explicitly, that wins and `.jarvis/args` is not read (**explicit > saved > default medium**).
- A scheduled-wake (auto-firing) tick always echoes args, so it never enters this branch.
- If `.jarvis/args` is also absent, fall back to the default (medium). (Restored or not, the effective args decided here are used as-is by 0.6 and procedure 4.)

### 0.5. Start banner (once on first boot)
If the `.jarvis/baseline` file **does not exist**, this is the first startup tick → output the `JARVIS` ASCII logo **once in a response-body code fence** per the "Start banner" section rules (outside markers, with caption, always visible). Skip if the file already exists. After outputting the banner, proceed normally with procedures 1–4.

### 0.55. Plan opt-in (only once, on first boot + interactive)
**Condition:** Perform only when this is the first startup tick (baseline-absent decision at `0.5`) **and this is an interactive start, not a scheduled auto-wake.** Same guard as strength (0.6): **never ask on an auto-firing tick** — a question there would block the loop while the user is away.

- **`plan=off`** → skip planning entirely. The loop behaves **exactly as it does without this feature** (as-is). No plan/checklist files, no plan-review.
- **`plan=<source>`** (a Jira key, URL, or file path) → treated as opt-in *with* the source named. Hand it straight to `jarvis-plan` (skip the yes/no question).
- **Otherwise, ask once** with `AskUserQuestion`: *"Draft a plan + checklist for this work?"* — choices **"Yes, make a plan"** / **"No, just watch."**
  - **No** → proceed as-is (no planning). Nothing more to do here.
  - **Yes** → call `Skill('jarvis-plan')`. It selects the source (Jira / Confluence / Notion / doc / write directly), reads it, **drafts** `plan.md` + `checklist.md`, gets the human's **approval**, and writes them to `.jarvis/`. When it returns, continue to 0.6.
- **Order:** this comes **before** strength (0.6) — decide *what the work is* before *how tightly to watch it.*
- **First boot only.** On resume (baseline present) it is not re-asked; if `.jarvis/checklist.md` exists, plan mode is simply active and the watch reviews against it. To (re)plan later: `/jarvis-reset` then start again, or `/loop /jarvis plan=<source>`.

### 0.6. Strength selection (only once, on first boot + when no args)
**Condition:** Perform only when this is the first startup tick (baseline-absent decision at `0.5`) and **there are no recognized args at all.**
- Ask for strength once with `AskUserQuestion`. The choices are 3: `strong (high)` / `medium (medium)` / `weak (low)`, plus a knob summary of each preset in the description. (The user can also give a value directly via "Other.")
- Confirm the value the user picked as this tick's `strength`, and echo `strength=<chosen value>` in procedure 4's wake-schedule prompt. From the next wake on, args are non-empty so it does not ask again.
- **Never ask on a scheduled-wake (auto-firing) tick** — args (including `strength=`) are always echoed, so it never enters this branch. This prevents the loop from being blocked by a question while the user is away.
- If there is even one arg (e.g., `/loop /jarvis strength=high`, `/loop /jarvis idle=30m`), use that value as-is without asking.

> This question is only "once when first turned on." To change strength later, call it again with `/loop /jarvis strength=<value>` (it overwrites the in-progress schedule).

### 0.7. `/loop` notice (once on first boot — for the bare-call case)
**Condition:** Perform only when this is the first startup tick (baseline-absent decision at `0.5`). (Not output on scheduled-wake or later ticks.)
- The skill cannot tell at runtime whether it is running inside `/loop` or was launched as a bare `/jarvis`. So on the first boot tick it always leaves a one-line notice **outside** the markers:

  ```
  ↻ Continuous watch requires launching as /loop /jarvis. If launched without /loop, it stops after this one tick.
  ```

- This notice is informational. If it was running under `/loop`, `ScheduleWakeup` in procedure 4 works and it keeps repeating (the notice is harmless); if it was a bare call, `ScheduleWakeup` is silently ignored and it stops after this tick as the notice says.
- Procedures 1–4 proceed as usual (this one tick runs normally).

### 1. Measure (low cost)
If `paths` is set, append `-- <paths>` to measure working-tree change volume. Count both **tracked-file changes** and **untracked (newly created) files**:

```bash
git diff --shortstat HEAD -- [paths]                 # ① tracked-file changes
git ls-files --others --exclude-standard -- [paths]  # ② untracked (new) file list
```

- From ①, parse `insertions(+)`, `deletions(-)`.
- Add the line count of each file in ② (`wc -l`).
- `cur_lines = (① insertions + deletions) + (② total line count of new files)`
- If empty, 0.

> ⚠️ **Why ② is essential:** `git diff HEAD` **does not include untracked files.** If this is missing, when a human **writes a new file by hand** (the core use case of this project), jarvis sees 0 and stays silent until stage/commit. There is also a way to pull it into the index with `git add -N` (intent-to-add), but it **mutates the index, causing side effects in the unattended loop**, so it is not used — count it separately with the read-only `ls-files` and add it.

If `risk` is set, measure the risk paths separately (same tracked + untracked method):

```bash
git diff --shortstat HEAD -- <risk globs>
git ls-files --others --exclude-standard -- <risk globs>
```
→ `risk_lines = (tracked ins+del) + (untracked new-file line count)` (on risk paths). 0 if risk unset.

Also check the current commit:

```bash
git rev-parse HEAD
```
→ `cur_head`.

> Measurement is on a working-tree basis (vs. `HEAD`) including staged, unstaged, and **untracked**.

### 2. Boundary decision (auto-correct for commits/discards)
Read `base_lines`, `base_risk`, `base_head` from `.jarvis/baseline`.

**(0) Stale-baseline self-correction (resume hygiene — a light one-time check):**
After stopping the loop with an interrupt (Esc), doing a rebase/reset/branch-delete outside can leave `base_head` pointing at a **SHA that no longer exists in the repo.** When `base_head` is non-empty, verify its existence once:

```bash
git cat-file -e <base_head>^{commit} 2>/dev/null   # exit 0 if it exists
```

→ **If it does not exist** (non-zero exit), the previous baseline has lost its meaning. Do not treat this tick as a first boot (no banner re-output); silently **reset the baseline to current measured values** (`lines=cur_lines risk=risk_lines head=cur_head deferred=0`, preserving `boot`/`mirrored`). Do not run `jarvis-once`; go to procedure 4. (Commit-boundary and discard correction are meaningful only when head is valid, so this fires first to avoid running (a)/(b) on an invalid head.) If `base_head` is empty, skip this check.

**(a) Commit boundary — forced observation (always on):**
If `base_head` is non-empty and `cur_head != base_head`, a **new commit was made** since the previous tick (commit/merge). Check once with `jarvis-once` regardless of volume.
- **However, if `active_chat` (in conversation), defer this commit check too:** set `deferred = 1` and, **without updating `base_head`**, reschedule at the `debounce` interval in procedure 4. When it goes quiet, re-enter this branch on the next tick and execute. (head is deliberately not moved so the commit check is not lost.)
- If quiet (`active_chat == false`), execute right away:
  - diff to show: if `base_head` is an ancestor of `cur_head`, `git diff <base_head>..<cur_head>`; otherwise (rebase/checkout/force, etc.) `git show <cur_head>`
  - First perform "Convention document collection" and pass it along.
  - Pass `jarvis-once` the context: "this is a just-committed change. Look for mistakes/omissions from the perspective of a final check right before sealing."
  - Deliver the review result **wrapped in the "Jarvis output markers."**
  - After execution, **skip** procedure 3 (the gate). Update the baseline to current values and go to procedure 4 with `deferred=0`.
- However, do not execute if the user has requested termination.

**(b) Discard detection:**
If `cur_head == base_head` but `cur_lines < base_lines`, the user discarded changes. Reset the baseline to current values and do not run `jarvis-once`. (Go to procedure 4.)

**(c) Otherwise — compute the increment:**
- `delta_lines = cur_lines - base_lines` (lines newly accrued since the last review; positive means new change exists)
- `delta_risk  = risk_lines - base_risk` (0 if risk unset)

### 3. Gate + debounce decision

**Gate satisfaction** — if any one of the following holds, `gate_met = true`:
- `delta_lines >= 1` — if **new change has accrued** since the last review, review it (no fixed volume threshold). Already-reviewed change is absorbed into `base_lines` at the end of the procedure, so the same change does not fire again.
- if `risk` set, `delta_risk >= 1` — risk paths are volume-independent. Warn even on a single newly changed line. (tenet 7: react to risk)

**Whether a review is needed**: `should_review = gate_met OR (base_deferred == 1)`
→ If there is a previously deferred review, it is a review target even if the gate is not satisfied again (deferred changes do not disappear).

**May speak now**: `may_speak_now = (active_chat == false)` — conversation has stopped.

Branches:

- **should_review && may_speak_now → execute (flush):**
  1. Perform "Convention document collection."
  2. Call `Skill('jarvis-once')` to have the current changes (working-tree diff) reviewed. Pass along the collected reference conventions + the context "look mainly at the changes newly accumulated since the last review." If it's due to a risk path / deferred review, state that fact.
  3. Deliver the review result **wrapped in the "Jarvis output markers"** concisely to the user.
  4. Clear with `deferred = 0`.

- **should_review && !may_speak_now → defer (debounce):**
  - Do not run `jarvis-once`. Mark `deferred = 1`.
  - Leave a one-line watch operational message **outside** the markers (e.g., "change detected — holding off because we're talking, will review when it settles").
  - Reschedule briefly at the `debounce` interval in procedure 4.

- **Otherwise (should_review == false):** no new change has accrued. Don't go silent — leave a **one-line heartbeat** (see "Liveness (A)" below) outside the markers — except when we're talking (`active_chat == true`), in which case skip it (the statusline covers it).

**Baseline recording rules (always applied at the end of the procedure):**
- `head`: record `cur_head` at the end of every tick. **Except when the commit boundary (2a) was deferred via debounce** — do not update `head` so it is detected again on the next quiet tick.
- `lines` / `risk`: update to current values (`cur_lines`/`risk_lines`) **only when `jarvis-once` was executed (flushed) or a discard reset (2b) occurred.** Updating absorbs that change into the base, so from the next tick it is no longer seen as "new change" (prevents re-reviewing the same change). On deferred/unsatisfied ticks, keep the existing values so changes keep accumulating.
- `deferred`: record the branch result above (0/1).
- `boot`: record `boot_now` decremented by 1 (minimum 0). That is, warmup polling is maintained only for `warmup` ticks after boot, then automatically drops to `idle`. If `warmup=0`, no warmup from the start.
- `mirrored`: record the procedure 3.5 result (0/1). 1 if the mirror was shown; 0 if a release condition (human direct typing dominates · review flush · discard reset) holds.

### 3.5. Mirror — gray-zone visualization (non-enforcing)
An auxiliary device for preserving authorship. **It neither blocks nor fixes code** — it only holds up a mirror when the human is about to unwittingly rise from the cockpit. If `mirror=off`, skip this entire procedure (`mirrored` stays 0).

**Signal (cheap — transcript+diff only, no `jarvis-once` call):** Look at *how* the changes accumulated since the previous tick were made.
- If an assistant `Edit`/`Write`/`NotebookEdit` call in this session's transcript directly created the changed file → **AI-generated.**
- A change that appears only in the diff without such tool calls → **human-typed directly.**
- It is **independent** of the severity gate — even if the generated code is clean and `jarvis-once` stays silent, the authorship signal fires separately.

**Firing conditions (all must hold):** ① a substantial part of the cumulative change is AI-generated (roughly a majority) · ② the absolute amount is not trivial (not a one-or-two-line edit) · ③ `base_mirrored == 0` (not yet shown). When satisfied, leave a dry one-line memo **outside** the markers and record `mirrored=1`:

```
🪞 A substantial part of this change looks like code generated in this session — it'll be committed under your name, so make sure you've grasped it yourself.
```

**Release (cooldown clear):** On a later tick, if **human-typed changes again dominate**, or a review was flushed, or a discard reset (2b) occurred, set `mirrored=0` so it can fire again on the next generation burst.

**Register · limits:**
- It is not preaching, blaming, or coercion. **Point it out and step aside** — the same dry memo register as `jarvis-once`'s "neither spoon-feed nor probe."
- **Only within the visible scope.** It looks only at this session's transcript — it cannot see generation in another terminal/session or external pastes. So it does not assert ("it is...") but points out with "looks like...," and does not interrogate.
- To turn it off, `mirror=off`. If the human doesn't want the mirror, respect that choice too — even the mirror is non-enforcing. (Litmus ①: coercion is Ultron, the mirror is Jarvis)

### 3.6. Plan review & completion (only when plan mode is active)
Skip this entire procedure unless `.jarvis/checklist.md` exists. When it does, the checklist is the spec the watch navigates against.

**Per-review checklist assessment (rides on the gate — no extra cost):** This runs only on ticks where a review was actually flushed (procedure 3's execute branch or a commit-boundary review 2a) — the same expensive moments, not every tick. When `jarvis-once` is called, the plan/checklist was already passed as the "task spec" (collection item 0). Have it, alongside the normal review, report against the checklist:
- which item(s) this change advances, and which now **look complete**;
- what's **missing or risky per item** (an item whose happy path is done but error/empty paths aren't);
- **false completion** — if the human already ticked an item (`- [x]`) but the code doesn't back it up, flag that (the navigator's job is to contradict a premature "done," not to rubber-stamp it).
- This assessment goes **inside the Jarvis markers** as part of the review body.

**The human owns the checkmarks.** The watch does **not** tick `- [ ]` → `- [x]` on its own — that judgment (and the accountability that rides on it) stays with the human. The watch only *reports* its assessment; the human ticks items in `.jarvis/checklist.md` when they agree. (Reading the file each review tells the watch what's officially done vs. still open.)

**Which to do first is the human's call.** If asked, recommend a next item and one line of why — then step back. Never sequence the work for them.

**Completion → final review, then recommend closing (the human confirms):** When **every checklist item appears complete** (all boxes ticked, or all assessed done with no open gaps), on that tick have `jarvis-once` do a **comprehensive final review against the whole plan** — the "right before it's all sealed" golden moment at the largest scale. Deliver it wrapped in the markers, then leave a one-line recommendation **outside** the markers:

```
✅ All checklist items look complete — final review above. Close the loop? (Esc to stop · or say "done" / keep going)
```

- Do **not** end the loop yourself on this tick — **still schedule the next wake** (procedure 4) so the watch stays alive while the human decides. Ending the loop is the human's act: they confirm ("done") or simply interrupt (Esc), and then no further wake is scheduled. (Consistent with "the human pulls every trigger.")
- If the human keeps editing after completion was signalled, the loop just carries on reviewing — nothing special is needed.

### 4. Schedule the next wake (the core of loop maintenance)
Call `ScheduleWakeup` to schedule the next run.

- **Warmup decision:** Determine `boot_now` — if it is the first boot tick (decided by baseline-absent at 0.5), the `warmup` value; otherwise the `boot` value from the baseline (0 if absent).
- Interval determination:
  - If the review was **deferred** this tick (`deferred` set to 1) → `debounce` (briefly, check again soon)
  - If `jarvis-once` was **executed (flushed)** this tick → `active`
  - **In warmup** (`boot_now > 0`) → `active` (right after first load, recheck quickly instead of idle)
  - **If the working tree has changes** (`cur_lines > 0`) → `active` (work is in progress, so poll tightly to catch new change/commits fast)
  - Otherwise (working tree clean · warmup ended) → `idle`
- **Echo the args received this time as-is in the prompt.** That way the settings persist on the next wake too. If `strength` was used, serialize it in the **`strength=<value>` (+ individual overrides) form, not the expanded individual knobs** (preserve the strength meaning). e.g.:

  ```
  /jarvis strength=high paths=src/billing risk=**/*payment*
  /jarvis strength=high idle=30m                          # preset + individual override is echoed as-is too
  /jarvis active=4m idle=25m debounce=90s                 # when strength is unused, echo as individual knobs
  ```

  ⚠️ If you omit this echo, all settings revert to defaults from the second wake on. Always serialize and pass the full current effective args (`strength` or individual knobs + `paths`/`risk`).
- **Save args for resume:** Along with scheduling the wake, write the **same args string** echoed in the prompt to `.jarvis/args` as one line (args only, without the `/jarvis ` prefix). After stopping the loop with an interrupt (Esc) and relaunching with `/loop /jarvis` (no args), procedure 0.4 reads this value and auto-resumes with the same settings.
- In `reason`, write specifically what is being waited for (e.g., "polling for change accumulation, next check in 4 minutes").
- **Record liveness (`.jarvis/status`):** Right after `ScheduleWakeup`, convert the next wake time to an epoch and overwrite `.jarvis/status` as one line. `<delay_s>` is the interval just scheduled (seconds), `<interval>` is its label (`active`/`idle`/`debounce`), `<strength>` is the effective strength (may be omitted if only individual knobs were used):

  ```bash
  mkdir -p .jarvis
  now=$(date +%s)
  plan=""   # plan mode: append checklist progress so the statusline can show it
  if [ -f .jarvis/checklist.md ]; then
    done=$(grep -cE '^[[:space:]]*-[[:space:]]*\[[xX]\]' .jarvis/checklist.md); total=$(grep -cE '^[[:space:]]*-[[:space:]]*\[[ xX]\]' .jarvis/checklist.md)
    plan=" plan=${done}/${total}"
  fi
  echo "state=watching next_wake=$((now + <delay_s>)) interval=<interval> strength=<strength>${plan} tick=$now" > .jarvis/status
  rm -f .jarvis/stopped   # a tick running = loop alive → clear the event stopped flag (if any)
  ```

  This one line is what backs the statusline's continuous display (watching / stalled?) and stall inference (see "Liveness"). Omit it and the statusline sees only a stale `next_wake` and soon shows "stalled?". The `plan=<done>/<total>` field is optional — present only in plan mode, and the statusline renders it as a `· plan 3/7` segment.

## Liveness (heartbeat + statusline)

So the user can always tell "is it looping right now?", emit the signal in two layers. `/loop` dynamic mode has no resident process — **nothing runs between ticks** — so combine (A) a one-line heartbeat in the tick body and (B) a statusline that's visible between ticks too.

### (A) Tick heartbeat — one line in the body
Even on a quiet tick (no new change), leave an alive signal **outside** the markers. This one line shows, every tick, "the loop is alive and the next check is when":

```
⏱ jarvis · alive · next check ~4m (active) · strength=medium
```

- Render it as **relative (~Nm)**, not an absolute clock (reuse the interval decided in procedure 4 — no `date` math needed).
- Include the interval label (`active`/`idle`/`debounce`) and the effective strength.
- **Do not emit the heartbeat on ticks where we're talking (`active_chat == true`)** — the human is present so loop liveness is self-evident, and we don't interrupt the conversation (procedure 0). The continuous signal there is covered by (B) the statusline. The debounce branch's operational message is still left as usual.
- On a tick that flushed a review, append this heartbeat line **after** the marker-wrapped review body (to give the next-check ETA).

> Procedure 3's "otherwise (no new change)" branch now emits this heartbeat line instead of going silent (skipped while talking).

### (B) Statusline — continuous, visible between ticks too
Read `.jarvis/status` (written every tick in procedure 4) and paint the watch state in the Claude Code status line **on every render**. It's visible even when no tick is running, and if `next_wake` is long past with no update it even infers **"stalled?"** (= the loop died or was stopped with Esc).

```
🤖 jarvis · watching · next ~3m (active)              (normal — alive)
🤖 jarvis · checking…                                 (wake time reached, tick imminent)
🤖 jarvis · ⚠ stalled? no tick for 11m — /loop /jarvis to resume   (likely dead)
```

The script ships with this skill: **`assets/statusline.sh`**. If `.jarvis/status` is absent (= watch not running) it prints nothing, so it's harmless to leave always on. Enable it non-destructively by registering it in settings.json **yourself** (install does not touch it automatically):

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/skills/jarvis/assets/statusline.sh"
  }
}
```

- For a project-scoped install, change the path to `.claude/skills/jarvis/assets/statusline.sh`.
- If you already use another `statusLine`, Claude Code allows only one, so call `bash .../statusline.sh` from inside your existing script and merge its output as one segment.

### (C) Stop hook — confirm "stopped" instantly, no time inference (optional)
The (B) statusline can only infer death once `next_wake` has passed, so it lags by up to `interval + grace`. The Stop hook raises that to an **event-based** signal.

Register `assets/loop-watch-hook.sh` as a **Stop** and **StopFailure** hook. At every turn-end it inspects the payload's `session_crons` (the list of currently scheduled wakeups). If no `/jarvis` wakeup is in it, the loop is no longer scheduled (a missed/errored ScheduleWakeup, or an Esc-killed loop followed by any user turn) → it drops `.jarvis/stopped` so the statusline shows "stopped" **instantly**. While a wakeup is alive, it clears the flag.

```json
{
  "hooks": {
    "Stop":        [ { "hooks": [ { "type": "command", "command": "bash ~/.claude/skills/jarvis/assets/loop-watch-hook.sh" } ] } ],
    "StopFailure": [ { "hooks": [ { "type": "command", "command": "bash ~/.claude/skills/jarvis/assets/loop-watch-hook.sh" } ] } ]
  }
}
```

- **Timing:** it cannot catch the Esc *moment* — Claude Code has no interrupt hook (Stop fires only on a normal turn-end). It confirms at the **end of the next turn (your next input)** after Esc. You usually interact right away, so it feels near-instant; only "pressed Esc and walked away with no further turn" falls back to (B)'s time inference.
- **No false positives:** even if "/jarvis" appears in `last_assistant_message`, it's ignored — only wakeup prompts inside `session_crons` are checked.
- Without the hook, (B) alone still works (time inference). The hook is an optional speed-up of *detection*.

## Stop / resume / reset

Since `/loop` is the engine, the lifecycle rides on `/loop`'s own lifecycle. There are no separate pause/resume commands.

| action | how | state (`.jarvis/`) |
|------|------|------------------|
| **Start · resume** | `/loop /jarvis [args]` | if baseline/args remain, continue from that point. Launched with no args, `.jarvis/args` auto-restores (procedure 0.4) |
| **Stop · pause** | interrupt the `/loop` (Esc) | untouched — baseline/args preserved, waiting to resume |
| **Full reset** | **`/jarvis-reset`** (independent skill) | delete `.jarvis/baseline`·`.jarvis/args` (and `plan.md`·`checklist.md`, after a confirmation) → next start is a first boot (banner / plan opt-in / strength question) |

How it works:
- **Light yielding (implicit)**: If the user simply sends another message, that turn yields to discussion/implementation per procedure 0 (the watch itself stays alive). An implicit yielding that happens without a command.
- **Stop/pause = interrupt the loop (Esc)**: In `/loop` dynamic mode, the next tick exists only when `ScheduleWakeup` is called. Interrupting the loop means no next wake is scheduled, so the loop ends. baseline·args stay on disk, so it waits to resume without loss. (Loop termination has no teardown hook — no cleanup code can run at end time, which is why there is no separate pause flag.)
- **Resume = `/loop /jarvis`**: Relaunching finds the baseline, so it skips the banner and strength question (procedures 0.5·0.6); launched with no args, procedure 0.4 restores `.jarvis/args` and continues with the same settings. Even if you rebased/reset outside, procedure 2(0) stale self-correction silently realigns an invalid head to current values.
- **`/jarvis-reset`**: An **independent command** that deletes `.jarvis/baseline`·`.jarvis/args`. It does not stop a running loop (that's Esc) — use it to clear state when you want a fresh start after stopping. ("reset jarvis," "start over" are handled the same way. "just stop" → Esc guidance.)

## Cost guide (for user information)

- If the wake interval is under 5 minutes, the prompt cache (TTL 5 minutes) stays alive and the polling turn is nearly free. That's why the `active` default is 4 minutes.
- When quiet, set `idle` long (default 25 minutes) to reduce accumulated cache-miss cost.
- Most actual tokens are spent "the moment `jarvis-once` runs" (new change accrued · risk path · commit boundary). Since it reviews each time new change accrues, tighter polling (strength `high`) means more frequent reviews and more cost. Setting `idle` long or lowering strength reduces it.
- Polling **tightly** does not increase noise. `jarvis-once` stays quiet on its own below its own severity threshold. Tighter polling only increases the *call cost*, not the nagging — if you want faster response, you can raise it with peace of mind.
- The commit-boundary trigger is only once per commit, so its cost is predictable, and being a single check "right before a mistake is sealed," it is the highest value-for-cost execution.

## Dependency note

This skill calls the `jarvis-once` (one-shot navigator) skill, and on plan opt-in the `jarvis-plan` (plan navigator) skill. To share with the team, both must also be accessible (repo `.claude/skills/jarvis-once/`·`jarvis-plan/` or a shared repo). If they are only in the personal global (`~/.claude/skills/…`), the call may fail in other teammates' environments.

---
name: narvi
description: Use when the user runs /narvi <pr-or-mr-url> [--dry-run]. Picks up every unresolved comment on a GitHub PR or GitLab MR — both inline review-thread comments anchored to a diff line and overview comments at the PR's top level (Mithrandir's verdicts, free-form review-body notes) — asks once before touching the branch, dispatches the smith subagent comment-by-comment (one commit per comment, each referencing the comment URL in its footer), verifies the branch once every comment is addressed (the project's detected test and lint commands), weighs its own amendments by Mithrandir's axes before pushing — a standing Blocker halts the run rather than handing the reviewer fresh grounds for comment — then pushes the branch so the forge updates. De-duplicates across re-runs by grepping the branch's commit log for the trail marker. Host-agnostic; routes to GitHub or GitLab from the URL. Does not resolve review threads — the human eyeballs the work and resolves.
purpose: Picks up unresolved comments on a PR or MR and answers each with a commit.
user_invocable: true
stage: forge
composes: mithrandir:dispatch+mend|weighed again before push
---

# Narvi — The Dwarf-Smith at the Doors

Where Mithrandir leaves his counsel upon the work and Celebrimbor forges from a counsel given in council, Narvi answers the counsel given on the review itself. The reviewer wrote — sometimes upon a line, sometimes at the gates of the work in one whole note — and Narvi reads, mends, and lets the trail show whose hand pointed at the flaw and whose hand set it right. The threads stay open after the work; the human walks back and resolves with their own eye.

## Ethos

- **One comment, one commit.** Whether the comment was a line-anchored nit or a sweeping overview note, it lands as one commit so the trail reads cleanly six months on.
- **The reviewer is the contract.** Narvi addresses what was asked, no more. A nit is not a chance to refactor; an overview rename is not a chance to redesign.
- **Confirm once before any write.** The slash invocation alone is not authority to write to the forge. Narvi names every comment it intends to address and waits for the word.
- **The trail is the record.** Each commit footer carries `See: <comment-url>`. On a re-run, Narvi greps the log and skips comments whose URLs are already in it — no forge-side `isResolved` flag needed.
- **One terse ack, then silence.** After each addressed comment, Narvi posts a **short confirmation in the thread's language plus the commit link** — `Done in [`<sha7>`](<url>)` for English, `已處理 [`<sha7>`](<url>)` for Chinese, the equivalent elsewhere. The link is the trail the reviewer can click; the verb is just the signal. **Write more only when there is something the reviewer would not already know** — a disagreement with the suggestion, an addition beyond the ask, a partial address, or an answer to a question they raised. Otherwise the confirmation stands as the entire body. Narvi never resolves the thread, never reacts, never starts a conversation. Resolution stays the human's hand; the bot writes once per amendment and no more.

## Argument parsing

```
/narvi <pr-or-mr-url>              # forge the amendments after a single confirm
/narvi <pr-or-mr-url> --dry-run    # list the unaddressed comments, do not touch the tree
/narvi <pr-or-mr-url> --no-confirm # forge straight through, no gate (sweep-mode entry)
```

Dispatch on the **first positional argument**:

- If absent, stop with: *"Narvi needs a PR or MR URL — without a forge there is no doorway to inscribe."*
- If it does not match either URL pattern in the dispatch table, stop with: *"Narvi does not know that URL — it bears no PR or MR mark."*

The `--dry-run` and `--no-confirm` flags may appear anywhere after the URL. `--no-confirm` bypasses the confirm-once gate in step 5 — used by `/durin` when an outer gate has already taken the user's word for the whole sweep. The flag is honoured for direct `/narvi` calls too, but the burden of intent shifts to the human typing it. No other flags are honoured.

## URL dispatch

Match the URL against two host-agnostic patterns (case-insensitive):

| Forge | Pattern | Read hook (metadata) | Comments hook | Reply hook |
|---|---|---|---|---|
| GitHub | `https?://[^/]+/(?<owner>[^/]+)/(?<repo>[^/]+)/pull/(?<n>\d+)` | `~/.claude/hooks/lindir-github-pr.sh` | `~/.claude/hooks/narvi-github-comments.sh` | `~/.claude/hooks/narvi-github-reply.sh` |
| GitLab | `https?://[^/]+/(?<group>.+)/-/merge_requests/(?<iid>\d+)` | `~/.claude/hooks/lindir-gitlab-mr.sh` | `~/.claude/hooks/narvi-gitlab-comments.sh` | `~/.claude/hooks/narvi-gitlab-reply.sh` |

The host portion is *not* fixed to `github.com` or `gitlab.com`. Self-hosted forges work the same — `gh` and `glab` resolve the host from the URL.

Both comment hooks emit the same JSON array shape, so the workflow is forge-blind below dispatch:

```json
[
  {
    "kind": "inline",
    "thread_id": "...",
    "path": "lib/foo.dart",
    "line": 42,
    "diff_side": "RIGHT",
    "diff_hunk": "@@ -40,3 +40,4 @@ ...",
    "comments": [ { "author": "...", "body": "...", "url": "...", "created_at": "..." } ]
  },
  {
    "kind": "overview",
    "thread_id": "...",
    "path": "",
    "line": 0,
    "diff_side": "",
    "diff_hunk": "",
    "comments": [ { "author": "...", "body": "<top-level note body>", "url": "...", "created_at": "..." } ]
  }
]
```

What each kind covers:

- **inline** — A review thread anchored to a path and line on the diff. GitHub: an unresolved `reviewThread` with at least one comment. GitLab: a discussion whose first note is resolvable, unresolved, and carries a `position` (diff-anchored).
- **overview** — A note at the PR's top level, not anchored to any line. GitHub: an issue-comment with non-empty body, or a submitted review's body (`Approve` / `Comment` / `Request changes`) when non-empty. GitLab: a non-system discussion whose first note has no `position` and a non-empty body. Mithrandir's verdicts land here.

`diff_hunk` is populated on GitHub inline threads and empty on GitLab inline threads. For overview entries it is empty on both. The smith reads the file at the line (inline) or the PR's diff (overview) when the hunk is absent.

## Environment drift

Many projects regenerate files as a side effect of routine operations — Flutter writes `Debug.xcconfig`, CocoaPods recreates `Podfile`, the JS toolchain mutates lockfiles. These are not the smith's scope-miss; they are **environment drift**, and a strict porcelain gate misfires on them.

Narvi filters `git status --porcelain` through a **denylist** before judging the workspace. A porcelain line whose path matches any denylist pattern is dropped from consideration; the gate trips only on what remains. The post-dispatch porcelain gate (step 6d) applies this filter, so drift produced by the smith's verification does not trip it — a Flutter project whose tests trigger a CocoaPods pass can be amended without a `git clean -f` ritual.

### Built-in default

Narvi ships a default denylist covering Flutter + iOS + macOS regeneration:

```
ios/Flutter/Generated.xcconfig
ios/Flutter/Debug.xcconfig
ios/Flutter/Release.xcconfig
ios/Podfile
ios/Podfile.lock
ios/Pods/
ios/Runner.xcworkspace/xcshareddata/
macos/Flutter/Generated.xcconfig
macos/Podfile
macos/Podfile.lock
macos/Pods/
.flutter-plugins
.flutter-plugins-dependencies
```

These cover the common case — a Flutter app whose `fvm flutter test` triggers a CocoaPods pass that rewrites xcconfig files. No project-side action is required.

### Project overlay: .narvi-ignore

If `<repo-root>/.narvi-ignore` exists, its patterns are read and **added to** (not replacing) the built-in default. The file uses gitignore-style syntax — one pattern per line, blank lines and `#` comments ignored. Example for a Node project:

```
# .narvi-ignore
node_modules/
.next/
.turbo/
```

### Match semantics

A pattern is matched against the porcelain path (the part after the two-character status flag and the separating space). For rename lines (`R  old -> new`), match against both paths; if either matches, the line is filtered.

- A pattern ending in `/` matches that directory and everything beneath it.
- A pattern containing `*` is matched as a glob against the path.
- Otherwise it is a literal-path match.

The filter does **not** affect `git status` shown to the user, nor any other git operation. It is purely an internal filter on Narvi's post-dispatch porcelain gate. Drift that was filtered out stays inside the isolated workspace; on the success path the workspace is torn down (drift and all) by the release step, so the human's main checkout never sees it.

## Workflow

### 1. Pre-flight

In order:

a. **Forge dispatch.** Match the URL against the table. Resolve the two hooks. If neither pattern matches, stop with the URL error.

b. **Forge auth sanity.** Run `gh auth status` (GitHub) or `glab auth status` (GitLab). If either fails, surface the message and stop.

c. **Source repo.** From the current working directory, run `git rev-parse --show-toplevel` to find the **source repo** — the human's checkout that anchors Narvi to a project. If the cwd is not inside a git repo, stop with: *"Narvi cannot forge here — there is no git tree at this place."* The source repo is consulted for its remotes and refs; Narvi will not commit on it.

d. **Remote match.** Parse the PR/MR URL's repo path — `<owner>/<repo>` for GitHub, `<group>[/<subgroup>]/<project>` for GitLab — case-insensitive. Run `git -C <source-repo> remote get-url origin` and parse its repo path the same way (strip the `.git` suffix, strip the SSH `git@<host>:` prefix or the `https?://<host>/` prefix, case-fold). If they do not match, stop with: *"This repo is `<local>`; the PR is on `<pr-repo>`. Narvi forges only where the tree stands."* This check runs before the workspace step, so a wrong-repo error never hides as a worktree-acquire failure.

e. **Acquire the isolated workspace.** Invoke the read hook (`<read-hook> <url>`) to fetch the PR/MR metadata. Read both `head` (source branch) and `base` (target branch). Then acquire a workspace at the head branch via the shared helper:

   ```bash
   ~/.claude/hooks/skadi-worktree.sh acquire <source-repo> <head>
   ```

   The helper prints the workspace path on stdout. It tries `git worktree add` first (fast — shares the object store); when the human already has the head branch checked out in the source repo (so worktree refuses), it silently falls back to a temp clone under `$TMPDIR` and re-points origin at the real remote. Either way the workspace lands on the head branch, freshly checked out and clean.

   Then bring head to the remote's tip:

   ```bash
   git -C <workspace> pull --ff-only
   ```

   If the pull is non-fast-forward (someone pushed atop head while you weren't looking), stop and surface the error — release the workspace via `~/.claude/hooks/skadi-worktree.sh release <workspace>` first so it does not linger under `$TMPDIR`. The human reconciles head with their own hand.

   The human's source-repo checkout is **not** disturbed by any of this — the worktree (or temp clone) is its own isolated tree, and the human may keep editing, building, or running tests in the source repo while Narvi works. There is no pre-flight clean-tree gate on the source repo for the same reason: the source repo's working state is irrelevant to Narvi's commits.

f. **Mark the pre-amendment tip.** Immediately after the pull, before any smith runs, record the workspace's HEAD:

   ```bash
   git -C <workspace> rev-parse HEAD
   ```

   Call this sha `<pre>`. It is the remote tip of the head branch — and so exactly the code the reviewer has already read and commented on. Every commit after it is Narvi's own hand, and step 7b weighs `<pre>..HEAD` on that basis.

   Capture it explicitly here rather than deriving it later from `origin/<head>`. That ref names the same commit at this moment, but it is not a dependable record of it: any fetch during the run may move it, and in clone-fallback mode the helper re-points origin at the source repo's remote during acquire. A sha held in hand cannot drift.

   Hold the workspace path, the resolved `base`, and `<pre>` for steps 2 through 10 — the workspace is needed to the end, since step 10 is where it is released or kept.

### 2. Fetch every comment

Invoke the comments hook:

```bash
<comments-hook> <url>
```

The hook prints a JSON array (possibly `[]`). Parse it.

- If empty, stop with: *"No unaddressed comments stand on this PR. Narvi has no doorway to inscribe."*
- If the hook prints `{"error":"..."}`, surface the error and stop.

### 3. De-dup by the trail

For each entry, extract the **first comment's URL** (the anchor). Then check the branch's commit log in the workspace for any commit whose message references that URL in a `See: <url>` footer:

```bash
git -C <workspace> log <base>..HEAD --format=%H --grep="See: <url>" --fixed-strings
```

If the grep returns any commit, drop the entry — Narvi already addressed it on a prior run. Keep the remaining entries.

If the de-dup empties the list, stop with: *"Every comment on this PR already bears a commit on the branch. Nothing remains for Narvi."*

### 4. Sort and render the manifest

Sort the kept entries by the first comment's `created_at`, oldest first — Narvi addresses them in the order they were left.

Render one short table to chat so the user sees the scope before the gate:

```
Narvi found N unaddressed comment(s) on <url>:

1. [inline]   <path>:<line>  @<author> — <first 60 chars of body…>
2. [overview] (whole-PR)     @<author> — <first 60 chars of body…>
3. [inline]   <path>:<line>  @<author> — <first 60 chars of body…>
…
```

Each row's `<author>` is the first comment's author; the kind tag lets the user weigh the cost of each at a glance.

### 5. Confirm-once gate

AskUserQuestion (options: `forge all <N>` / `abort`). The slash invocation is not authority for a forge write; the gate is always on for bare `/narvi`.

- `--dry-run` overrides the gate — render the manifest and stop. No dispatch, no commit, no push.
- `--no-confirm` overrides the gate — skip the AskUserQuestion and proceed straight to step 6. Used by `/durin` when an outer gate has already taken the user's word for the whole sweep.
- On `abort`, stop.
- On `forge all`, proceed.

### 6. Per-comment smith dispatch

Load the smith prompt from `<skill-dir>/narvi.md` once at the top of the loop. For each entry in the manifest, in order:

a. Build the kind-aware tail block. Common header:

```
## Comment to address

- PR/MR URL: <url>
- Kind: <inline | overview>
- Repo root: <workspace-path resolved in pre-flight step e>
- Branch: <head>
- Base: <base>
```

The `Repo root` field is the **workspace path** from pre-flight step (e) — the isolated worktree (or temp clone) under `$TMPDIR`. The smith reads and writes there, never against the human's source-repo checkout.

For `kind: inline`, append:

```
- Path: <path>
- Line: <line> (<diff_side> side)

### Diff hunk

<diff_hunk if present, else "(unavailable on this forge — read the file at the line)">
```

For `kind: overview`, append:

```
- Path: (overview — read the PR diff with `git -C <workspace> diff <base>...HEAD`)

### PR diff (truncated to first 200 lines)

<first 200 lines of `git -C <workspace> diff <base>...HEAD`>
```

Then the thread:

```
### Thread (chronological)

[1] @<author> — <created_at> — <comment-url>
<body>

[2] @<author> — <created_at> — <comment-url>
<body>

…

Implement the amendment for thread [1] (the anchor). Commit it. Return [FORGED] or [ABORT].
```

b. Dispatch the smith via the Agent tool, `subagent_type: general-purpose`, `model: opus`, passing the Narvi prompt as the system/instruction portion and the tail block as the task.

c. The smith returns one of two shapes (see `narvi.md`):

- `[FORGED]` block — extract `commit`, `kind`, `path`, `comment`, and the one-sentence summary.
- `[ABORT] <reason> (comment: <url>)` — record and continue to the next entry.

Anything else: record as a malformed return and continue.

d. After each dispatch, run `git -C <workspace> status --porcelain` and pass the output through the environment-drift filter (see *Environment drift* above). If any unfiltered line remains, the smith left real work uncommitted — abort the whole run: do **not** reset, clean, or otherwise touch the workspace, and do **not** push. Leave the workspace exactly as the smith left it (skip the release step) — a `git reset --hard` would erase the tracked stray edits while leaving untracked ones behind, defeating the inspection this step exists for. Surface the unfiltered paths in the report so the human can inspect what the smith left behind.

  Drift that the filter dropped does not count as scope-miss. It stays inside the workspace across dispatches (the smith's next call sees it but the smith does not touch xcconfig or lockfiles, so it is invisible to the work). On the success path the workspace is torn down by the release step at the end, drift and all.

### 7. Mandatory verification

The smith's own test run (`narvi.md`, *What you may do*) is self-graded and conditional — it fires only "if the project has an obvious test command and your change touches tested code." Before any push, the skill body runs its own gate on the branch as it now stands, once, independent of what the smith did or didn't run.

If no entry returned `[FORGED]`, skip this step — there is nothing new to verify. Step 7b skips for the same reason, and step 8 skips the push.

Otherwise, resolve the project's commands from the workspace — the same detection `/argonath` uses:

```bash
cd <workspace> && ~/.claude/hooks/argonath-detect.sh
```

Returns `{stack, lint, format, build, test, install, test_scope, source}`. For each of `test` and `lint` that is non-empty, run it — `install` is not Narvi's to run, it belongs to Argonath's merged-tree probe and its dependency-less checkout:

```bash
cd <workspace> && ~/.claude/hooks/argonath-run.sh Tests <test-command...>
cd <workspace> && ~/.claude/hooks/argonath-run.sh Lint <lint-command...>
```

- **Both `ok: true` (or empty/skipped)** — proceed to step 7b.
- **Either `ok: false`** — the run halts, the same as a step 6d scope-miss: do not push, do not release the workspace. Surface the failing command, its summary, and the log path in the report (step 10). The commits already made stand in the workspace, untouched, for the human to inspect.
- **Both commands empty** (`stack: unknown`, or the stack carries neither) — nothing to run; proceed to step 7b, and note in the report that verification was skipped for lack of a command. This is not a pass — it is the same "no command" honesty `/argonath` renders as `⚪ skipped`.

This step verifies the branch **once, after every comment is addressed** — not per-comment. One project-wide run stands in for however many (or few) per-comment runs the smith made on its own, and catches an amendment that broke something the smith's own test pass never touched.

### 7b. Weigh the amendments

Tests and lint prove the branch still runs; neither asks whether the smith's own code is *good*. A reviewer returning to a mended PR reads what Narvi wrote, and a fresh flaw there earns a fresh comment — which Narvi would then be summoned to answer. This step weighs the amendment before it reaches the forge, so the mend does not become the next thing to mend.

Skip it when no entry returned `[FORGED]` — there is nothing new to weigh. Step 7's halt never reaches here.

**Weigh only what the smith wrote.** The range is `<pre>..HEAD`, with `<pre>` the sha captured in pre-flight step 1f:

```bash
git -C <workspace> diff <pre>..HEAD
```

Never `<base>..HEAD`. That range carries the original PR work the reviewer has already accepted; findings on it are noise, and acting on them would widen the very diff the reviewer must read a second time.

Weigh that diff by Mithrandir's axis pass — the thirteen axes, the close per-symbol read, and the `## To pass` list grouped by severity (`skills/mithrandir/SKILL.md`, read-path step 4). Run the weighing in-skill against the captured diff; do not invoke a forge-writing verb, and render no verdict to chat — only the findings feed this gate.

Neither `--verify` nor `--deep` rides here, and the reasons differ:

- **`--verify`** convenes its panel over findings the pass has already named, so it can only drop or downgrade one — never raise a flaw the pass missed. Against a gate that exists to catch new flaws it buys nothing, at three opus calls per finding.
- **`--deep`** cures the dilution of one reader's attention across many files. An amendment diff — one comment, one narrow mend — does not suffer it.

**Blockers only.** Take the `## To pass` rows graded `Blocker`; leave `Nice to have` and `Nit` where they lie. A nit Mithrandir would raise is not necessarily one the human reviewer will, and chasing them turns a mend into a rewrite — which enlarges the reviewer's next read rather than sparing it. Name the untaken rows in the report all the same, so the human sees what was weighed and passed over.

- **No Blocker** — proceed to step 8.
- **Any Blocker** — one mend round, and one only.

#### The mend round

A Blocker in Narvi's own code is a flaw Narvi can answer, so it tries once before giving the work back:

a. **Dispatch the smith per Blocker**, in order. Load the same `<skill-dir>/narvi.md` prompt as step 6, and build this tail block:

```
## Blocker to close

- PR/MR URL: <url>
- Kind: mend
- Repo root: <workspace-path>
- Branch: <head>
- Base: <base>
- Amendment range: <pre>..HEAD

### The finding

- Axis: <the axis the To-pass row wounds>
- Where: <path>:<line>
- Blocker: <the To-pass row's text, verbatim>

### The amendment diff (truncated to first 200 lines)

<first 200 lines of `git -C <workspace> diff <pre>..HEAD`>

Close this blocker. Commit it. Return [FORGED] or [ABORT].
```

   Dispatch via the Agent tool, `subagent_type: general-purpose`, **`model: opus` — passed explicitly on every call**, exactly as step 6b does. Omit it and the smith silently inherits the session's model; under a `/durin` or `/moria` sweep running lighter, the very dispatch meant to close a Blocker would be the weakest of the run, and nothing in the report would say so.

   Each mend lands its own commit, as every Narvi commit does — no amending, no rebasing. A `[ABORT]` here is not a failure of the run; it means that Blocker stands unmended, and it is carried into (d).

b. **Re-run the porcelain gate** after each mend dispatch, exactly as step 6d does, drift filter and all. A mend that leaves real work uncommitted halts the run the same way a scope-miss does.

c. **Re-run step 7** — a mend is code, and it earns the same tests and lint the amendments did. A failure halts the run as step 7's failure halts.

d. **Re-weigh `<pre>..HEAD` once.** The range is unchanged; the mend commits now fall inside it, so the weigh reads the amendment as the reviewer will finally see it.

- **Clean** — proceed to step 8. The report names how many Blockers the round closed.
- **Any Blocker still standing** — whether unmended, mended badly, or newly raised by the mend itself — halt exactly as step 7's failure halts: do not push, do not release the workspace. Name each in the step-10 report with its axis, `path:line`, and text. The commits stand in the workspace for the human to finish by their own hand.

**The cap is one round, and it is not negotiable by judgment.** Do not weigh a third time, however close the second came. Narvi runs unattended under `/durin` and `/moria`, where a loop that mends its own mends has no one to stop it; `/feanor`'s `--max` backstop is the same reasoning, and its failure is the same failure — loud, with the remaining gaps named. A second standing Blocker is the signal that this amendment wants a human, not another agent.

### 8. Push

If any entry returned `[FORGED]`, push the branch from the workspace:

```bash
git -C <workspace> push
```

In worktree mode the push reaches origin (the human's real remote) because the workspace shares the source repo's object store and remotes. In clone-fallback mode the helper re-pointed the clone's origin at the source repo's origin during acquire, so the push reaches the same remote either way.

If `git push` fails (e.g. the remote moved during the run), surface the error in the report. The commits stand locally inside the workspace; do not release the workspace in that case — the human inspects it and reconciles by hand.

If no entry returned `[FORGED]` (all aborted or all malformed), skip the push. Nothing landed on the branch.

### 9. Post per-thread replies

For each entry that returned `[FORGED]` — and **only if step 8's push succeeded** — post a short ack on the thread so the reviewer sees that their note was answered.

a. Compose the commit URL from the PR/MR base and the smith's sha:

- GitHub: `<repo-url>/commit/<sha>`
- GitLab: `<repo-url>/-/commit/<sha>`

b. Compose the body. The default is a **short confirmation in the thread's language plus the commit link** — the reviewer knows what they asked, so the commit is the answer. Match the thread's language: `Done` for English, `已處理` for Chinese, the equivalent elsewhere.

- **(github, inline)** and **(gitlab, inline | overview)** — the bare confirmation stands as the entire body:

  ```
  Done in [`<sha7>`](<commit-url>).
  ```

- **(github, overview)** — issue-comments and review bodies have no thread-reply primitive on GitHub, so the reply lands as a fresh top-level issue-comment. Add a `(Reply to <url>)` footer for visual linkage:

  ```
  Done in [`<sha7>`](<commit-url>).

  (Reply to <comment-url>)
  ```

**Write more only when there is something the reviewer would not already know** — a disagreement with the suggestion, a step added beyond the ask, a partial address, or an answer to a question. In those cases, lead the longer body with a one-line summary if it runs over five lines (per `CLAUDE.md` verdict-first).

c. Pipe the body to the reply hook for the forge:

- GitHub:
  ```bash
  printf '%s' "$BODY" | <reply-hook> <url> <kind> <thread-id>
  ```
- GitLab:
  ```bash
  printf '%s' "$BODY" | <reply-hook> <url> <thread-id>
  ```

d. The hook prints `replied: forge=<f> ...` on success or `{"error":"..."}` on failure. Record the reply URL (or the error) per entry. **Do not roll back commits on a reply failure** — the commit stands, the `See: <url>` footer is the canonical record either way; the reply is convenience.

If step 8's push was skipped (no FORGED entries) or failed, skip this whole step — the commits referenced by the replies are not on the remote, so the links would 404.

### 10. Report and release

Render one block:

```
Narvi at <url> — <branch>

| # | Kind | Comment | Action | Detail | Reply |
|---|---|---|---|---|---|
| 1 | inline   | <path>:<line> by @<author>  | forged | <sha7> — <summary> | [posted](<reply-url>) |
| 2 | overview | (whole-PR) by @<author>     | forged | <sha7> — <summary> | failed (<error>) |
| 3 | inline   | <path>:<line> by @<author>  | aborted | <reason> | — |

Weighed: <one of the five below>
Pushed: yes / no (<reason>)
Workspace: released / kept at <path> (<reason>)
```

The `Weighed:` row takes exactly one of five values, and between them they cover every way step 7b can be left. Naming the state precisely is what lets `/durin` tell a `weigh-failed` outcome from a `verify-failed` one:

| Value | Means |
|---|---|
| `sound` | Weighed on the first pass, no Blocker. |
| `sound after mend (<N> closed)` | A Blocker stood, the one mend round closed it, the re-weigh came back clean. |
| `<N> blocker(s) standing` | A Blocker survived the mend round, or the round could not run. The push was halted here. |
| `skipped (nothing forged)` | No entry returned `[FORGED]`; there was no amendment to weigh. |
| `not reached (<reason>)` | Something forged, but the run halted before the weigh — step 7's verification failed, or a mend's own re-verification did. Name which. |

When step 7b left Blockers standing, render them beneath, so the human sees what halted the push without re-weighing by hand:

```
Blockers standing after the weigh:

| Axis | Where | Finding |
|---|---|---|
| correctness | lib/foo.dart:51 | <the To-pass row's text> |
```

When the mend round closed any Blocker, name what closed it in the same shape under `Closed by mend:` — with the commit `<sha7>` as a markdown link to the forge. A count alone tells the human that something was mended but not what, leaving them a `git log` to run before they can judge it.

When the weigh named `Nice to have` or `Nit` rows, list them in the same shape under `Passed over:` — they did not halt the run, and the human may still want them before a reviewer does.

Each comment-cell is a markdown link to the comment URL. Each forged-row's `<sha7>` is a markdown link to the commit on the forge (compose the URL from the PR/MR base — `<repo-url>/commit/<sha>` for GitHub, `<repo-url>/-/commit/<sha>` for GitLab).

After rendering, decide the workspace fate:

- **Release on the success path.** If verification passed (or was skipped for lack of a command), the weigh left no Blocker standing, the push succeeded, and no scope-miss tripped the post-dispatch porcelain gate, release the workspace:

  ```bash
  ~/.claude/hooks/skadi-worktree.sh release <workspace>
  ```

  The helper handles both worktree and temp-clone modes silently. The `Workspace:` row reads `released`.

- **Keep on abort or failure.** If step 6d found scope-miss, step 7's verification failed, step 7b halted for any of its three reasons (a Blocker still standing, a mend's porcelain trip, or a mend's failing re-verification), or step 8's push failed, leave the workspace intact under `$TMPDIR` and name the reason. The human can inspect, recover any salvageable work, and release by hand with the same helper verb when done. The `Workspace:` row reads `kept at <path> (<reason>)`. (A pre-flight `pull --ff-only` rejection is a separate, earlier failure — pre-flight step 1e already releases that workspace itself, since it holds no smith work yet; the run never reaches step 10 in that case.)

## After Narvi

The threads remain open on the forge; the overview comments remain on the page. Narvi leaves only the one terse ack per addressed comment (a short confirmation in the thread's language plus the commit link, e.g. *`Done in [`<sha7>`](<url>)`* / *`已處理 [`<sha7>`](<url>)`*); it does not resolve, does not react, does not start a conversation. The reviewer eyeballs each amendment with their own hand. Two next steps stand:

- **Re-weigh.** Once the branch settles, `/mithrandir bless <url>` (alias `/mithrandir recheck <url>`) re-weighs the PR/MR fresh, finds Mithrandir's prior counsel on the thread, and threads a follow-up — *All resolve*, *Partial okay*, or counsel withheld. Built exactly for amended PRs. This is not step 7b twice over: 7b weighs the amendment alone, privately, to guard what Narvi pushes; `bless` weighs the whole PR and speaks on the forge. One is a gate, the other a verdict.
- **Resolve.** The reviewer walks each thread, eyeballs the amendment against their note, and clicks `Resolve` (GitHub) or `Resolve thread` (GitLab) by hand. Overview comments on GitHub have no forge-side resolution; the per-thread ack and the trail marker (`See: <url>` in the commit footer) are the records.

Narvi does not auto-invoke either. The verbs stay separate so the human chooses when to re-summon.

## Rules

- One URL per invocation. No sweep across multiple PRs.
- Narvi works inside an **isolated workspace** acquired in pre-flight — a `git worktree` of the source repo (or, on fallback, a temp clone under `$TMPDIR`). The human's source-repo checkout is never modified, never committed against, never required to be clean. The smith reads and writes only in the workspace.
- One commit per comment. The smith does not bundle, does not amend, does not rebase. An overview comment with three asks still lands as one commit (the comment is the unit).
- Each commit footer must carry `See: <comment-url>` on its own line — that line is the trail marker Narvi greps on re-runs.
- The smith does not push, does not edit the PR body, does not post on the thread, does not react. The skill body owns the single `git -C <workspace> push` at the end and the one short ack per addressed comment.
- Narvi never resolves a review thread, never reacts. The single per-thread ack after a successful push is the only forge-write beyond the push itself. Reply-hook failures are recorded but do not roll back commits — the trail-marker footer remains the canonical record.
- An abort on one comment does not stop the run. Other comments still get their turn; the report names which succeeded and which did not.
- If the smith leaves real work uncommitted (after the environment-drift filter), the run halts without resetting or cleaning the workspace. The commits already on the branch stay; nothing is pushed; the workspace is **kept**, not released, exactly as the smith left it, so the human can inspect the stray edits directly.
- The workspace is **released on the success path** (verification passed or was skipped, the weigh left no Blocker, push succeeded, no scope-miss) and **kept on any abort or failure**. The release verb is idempotent; the human may re-run it at any time to clean up a kept workspace.
- Before any push, the branch is verified once via the same detection hooks `/argonath` uses (`argonath-detect.sh` + `argonath-run.sh`, tests and lint). A failing command halts the run exactly like a scope-miss: no push, workspace kept, the failure named in the report. No detected command is not a failure — it is named `skipped`, the same honesty `/argonath` renders for an absent command.
- Before any push, the smith's own code is weighed once by Mithrandir's axes over `<pre>..HEAD` — the amendment alone, never the whole branch. A standing `Blocker` halts the run like a failing test; `Nice to have` and `Nit` rows are reported and passed over. The gate guards the reviewer's next read: a flaw Narvi introduces would earn a fresh comment, and Narvi would be summoned to answer its own leavings.
- Do not surface forge tokens in logs, responses, or saved files.
- Aborts are first-class outcomes, not failures. Name the flaw plainly; do not retry.

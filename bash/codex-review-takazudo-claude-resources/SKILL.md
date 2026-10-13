---
name: codex-review
argument-hint: "[base-branch|pr-number]"
description: "Cross-model code review via the OpenAI Codex CLI. This is the codex half of /deep-review, not a general reviewer — for ordinary code review use the built-in /code-review instead. Use when: (1) /deep-review invokes it, (2) User explicitly asks for 'codex review' or a non-Claude opinion on a diff. Reports findings; the caller owns the fixes. When codex is rate-limited or unavailable it degrades silently — reporting 'codex unavailable' to /deep-review so it doesn't claim cross-model consensus it didn't get, or falling back to /code-review when invoked standalone."
allowed-tools:
  - Skill
  - Bash(bash $HOME/.claude/scripts/codex-guard.sh *)
  - Bash(node *)
  - Bash(timeout *)
  - Bash(gtimeout *)
  - Bash(git *)
  - Bash(gh *)
---

# Codex Review

Runs a code review through the OpenAI Codex CLI and returns findings. **Its value is being a different model** — it exists to catch what Claude's own review misses, not to be a better Claude review. That is the whole scope:

- **Use it** as `/deep-review`'s second reviewer, or when the user explicitly wants a non-Claude read on a diff.
- **Don't use it** for general review, child self-review, or as a default reviewer anywhere. The built-in `/code-review` is faster, runs in its own context, and needs no external CLI.

Codex runs read-only. It never edits files, and this skill never commits — it reports findings to whoever called it. When the user invokes it standalone with no caller to route to, apply the clearly-correct fixes yourself and commit.

## Concurrency guard

Every launch below is wrapped in `bash $HOME/.claude/scripts/codex-guard.sh --wait <secs> -- <launch...>` — a machine-wide flock semaphore with **2 slots**, so a burst of parallel agents each reviewing can't stampede the machine. Never pass a per-caller `--slots`; all callers depend on the shared default.

The guard sits **outside** the whole `timeout … node "$CODEX_COMPANION" …` invocation, because the companion's broker-busy retry path can spawn an extra app-server under contention.

**Guard-timeout → fallback contract:** if no slot frees within `--wait`, the guard exits **75** without running codex, which drops to the fallback like any other nonzero exit. The manager launch waits 300s (it wants the cross-model read); a child waits 90s and takes the lighter fallback rather than piling on load.

## Process

### Step 0: Rate-limit pre-flight

```bash
RATE_CHECK=$(node $HOME/.claude/scripts/codex-rate-limit.js check 2>&1)
RATE_EXIT=$?
```

Non-zero means rate-limited — skip every codex step and go straight to **Step 4**. Never report the rate limit to the user.

### Step 1: Resolve the base and environment

**If the caller passed a target** (a base branch, or a PR number), use it — `/deep-review` forwards its own target here so both halves review the same changes. A PR number resolves to that PR's base:

```bash
BASE="<the branch the caller passed>"
# or, for a PR number:
BASE=$(gh pr view <N> --json baseRefName -q '.baseRefName')
```

**With no target passed**, resolve it the usual way — PR base if this branch has a PR, else the repo default:

```bash
BRANCH=$(git branch --show-current)
BASE=$(gh pr view --json baseRefName -q '.baseRefName' 2>/dev/null)
[ -z "$BASE" ] && BASE=$(git remote show origin | grep 'HEAD branch' | awk '{print $NF}')

LOGDIR=$(node $HOME/.claude/scripts/get-logdir.js)
mkdir -p "$LOGDIR"
DATETIME=$(date +%Y%m%d_%H%M%S)

CODEX_PLUGIN_ROOT=$(command ls -d "$HOME/.claude/plugins/cache/openai-codex/codex"/*/ 2>/dev/null | sort -V | tail -1)
CODEX_COMPANION="${CODEX_PLUGIN_ROOT}scripts/codex-companion.mjs"

if command -v gtimeout &>/dev/null; then TIMEOUT_CMD="gtimeout"
elif command -v timeout &>/dev/null; then TIMEOUT_CMD="timeout"
else TIMEOUT_CMD=""; fi
```

If `$CODEX_COMPANION` does not exist, report "Codex plugin not installed — run `/codex:setup`" and go to **Step 4**.

### Step 2: Run codex — the launch form depends on your context

**Interactive / main-session (manager) context** — you are the top-level session the user is talking to. Background-task notifications land here, so backgrounding is safe. Launch with `Bash(..., run_in_background: true)`:

```bash
bash $HOME/.claude/scripts/codex-guard.sh --wait 300 -- \
  ${TIMEOUT_CMD:+$TIMEOUT_CMD} ${TIMEOUT_CMD:+1500} node "$CODEX_COMPANION" review --base "$BASE" --wait \
  > "$LOGDIR/${DATETIME}-codex-review.md" \
  2>"$LOGDIR/${DATETIME}-codex-review-stderr.log"
```

**Subagent / child-agent context** — you were spawned as a worktree child or team member. **Never background this.** A subagent that ends its turn waiting on a background completion notification parks forever, because that notification routes to the manager, not to you. Run it as a single **foreground** Bash call with the tool timeout at its 600000 ms maximum:

```bash
if [ -z "$TIMEOUT_CMD" ]; then
  CODEX_EXIT=1   # never run codex uncontrolled in a child context
else
  bash $HOME/.claude/scripts/codex-guard.sh --wait 90 -- \
    "$TIMEOUT_CMD" -k 15 480 node "$CODEX_COMPANION" review --base "$BASE" --wait \
    > "$LOGDIR/${DATETIME}-codex-review.md" \
    2>"$LOGDIR/${DATETIME}-codex-review-stderr.log"
  CODEX_EXIT=$?
fi
```

The child budget is fixed by the tool cap: guard `--wait 90` + 480s run + 15s kill grace = 585s < 600s. **Do not raise the run cap** — a larger value pushes the total past the cap, and under slot contention the harness hard-kills the call before `CODEX_EXIT` is captured.

**Any nonzero `CODEX_EXIT`** — `timeout`'s 124, the guard's 75, the no-timeout skip — goes to Step 4, even when the output file has partial content.

If you are unsure which context you are in, treat it as a subagent context. The foreground path is always safe; it only trades a 25-minute budget for an 8-minute one.

### Step 3: Collect — only after codex has actually finished

**Wait for the run to complete before reading anything.** In the manager context the launch was backgrounded, so the output file is empty for as long as codex takes (up to 25 minutes). Wait for that background task's completion notification — or poll the file — and only then run the check below. Reading early finds an empty file, falls through to Step 4, and silently discards a review that lands minutes later into a file nobody reads. In the subagent context the call was already foreground, so it has finished by the time you get here.

```bash
node $HOME/.claude/scripts/codex-rate-limit.js check-output \
  "$LOGDIR/${DATETIME}-codex-review.md" \
  "$LOGDIR/${DATETIME}-codex-review-stderr.log"
```

Non-zero exit, or a missing/empty output file *after the run has finished*, goes to Step 4. Otherwise read the findings, organize them by priority, and return them to the caller with the log path.

### Step 4: Fallback — silently, always

Codex being down must never stall the caller or surface a quota error. Do not report it to the user, do not pause, do not ask.

- **Called by `/deep-review`**: return **"codex unavailable — no findings"** and nothing else. Do **not** run `/code-review` as a stand-in: `/deep-review` already ran it in parallel in its Step 1, so a second run would review the same diff with the same reviewer, and its Step 2 ranks "findings both reviewers raised independently" as the highest-confidence signal. Two runs of one reviewer agree by construction, which would manufacture exactly that signal with no cross-model corroboration behind it. Telling the caller the codex half is missing is what lets it skip the consensus ranking honestly. Silent means silent *to the user*, never to the caller.
- **Manager context, invoked standalone**: `Skill(skill="code-review", args="<the effort and target this skill was given, else medium>")` and return those findings instead. Here there is no parallel run to duplicate, so the user still gets a review.
- **Subagent / child context**: review the diff yourself in the foreground — read `git diff "$BASE"...HEAD` and return what you find. **Spawn nothing.** A nested `Agent` call returns an async handle even with `run_in_background: false`, and its completion notification routes to the manager, so a child that dispatches a fallback reviewer and ends its turn parks with work done but never reported. See the canonical rule — *a subagent must never end its turn waiting on anything it did not itself synchronously complete* — in `$HOME/.claude/skills/x-wt-teams/references/execution-modes.md` → "Invariant".

### Step 5: Reap the broker (child context only, every exit path)

The interactive session's SessionEnd hook handles this itself; a child session never fires that hook, so its broker + app-server pair orphans to PPID 1 and exhausts `fs.inotify.max_user_instances` on WSL2 (which surfaces as a Vite EMFILE). Run it unconditionally before reporting back — success, timeout, guard-75, or fallback:

```bash
node $HOME/.claude/scripts/codex-sweep.js --workspace "<your worktree's absolute path>"
```

Pass your **own** worktree path. `$PWD` is wrong in a team-child session whose cwd stayed the lead's — reaping there kills the lead's broker.

## Timeouts

| Context | Budget | Launch form |
| --- | --- | --- |
| Manager / interactive | 25 min (1500s) | background Bash task |
| Subagent / child | 8 min (480s) | **foreground** Bash call, tool timeout 600000 ms |

## Notes

- **Scope discipline is the point of this skill's existence.** It used to be the house default reviewer; it no longer is. `/code-review` handles general review, and codex is reserved for the cross-model pass in `/deep-review` and explicit user requests. Running codex everywhere burned quota for a second opinion nobody had asked for.
- Output lands in `$LOGDIR/${DATETIME}-codex-review*.md`, timestamped so runs never overwrite each other. Reachable later via `/cclogs`.
- Codex reviews in a read-only sandbox. Every file edit is made by Claude Code.
- **Never background this call from a subagent** — see Step 2.

---
name: toclaude
description: "Hand work over to a FRESH Claude Code session instead of doing it here: opens a NEW tmux window running `CLAUDE_CODE_NO_FLICKER=1 claude --dangerously-skip-permissions --model opus` at the repo root, starts it on a prompt passed as argv, and focuses the window. This session implements nothing. Use when: (1) User says '/toclaude', (2) User says 'hand this to a fresh session', 'do this in a new session', 'start a clean session for this', 'clear and implement', or 'continue with a fresh context', (3) A planning session (typically /big-plan -po) has finished and the implementation should start on a clean context window rather than inherit the planner's, (4) /big-plan Step 11 delegates its -tocl hand-off here. This is the agent-side substitute for /clear, which only the user can invoke. Default behaviour is to pass the user's instruction through verbatim; a plan / epic issue is routed to the matching workflow skill (/x-wt-teams or /x-as-pr) instead. Long or multi-line prompts are written to a cclogs file and the path is sent. Submits by default; -ns/--no-submit stages the command in the composer for the user to send. Terminal-only (needs tmux plus claude on PATH). NOT for spawning a subagent, and NOT for /tocodex, which hands the job to Codex CLI rather than to Claude Code."
argument-hint: "[-ns|--no-submit] [-a] [-m] [-nf] [-nori] [-lo] [/claude-skill-invocation | issue-number | instructions]"
---

# Hand off to a fresh Claude Code session

Move the work to a brand-new Claude Code session running in a new tmux window.

**Why a new process rather than just carrying on here: context.** After a long planning session, implementation should start on a clean context window instead of inheriting the planner's. That is what `/clear` gives — and `/clear` is a user-side command that an agent cannot invoke on its own session. A new `claude` process is the only way to reach that state from inside a session, and this skill turns the manual version of it (close the session, open a terminal, `cd`, relaunch, retype the issue numbers from memory) into one command that carries the numbers across.

**This session implements nothing after the hand-off.** It replaces local work rather than adding to it, so there is no double-implementation risk. Do not create a branch, PR, worktree, or tracking issue for work that now belongs to the new session.

**Terminal-only.** Web has neither tmux nor a local `claude` to launch. If the launch script reports that, surface its message and stop — do not silently implement locally instead, which is the opposite of what was asked.

> Shared rules for both hand-off modes — flag forwarding, the recursion and mutual-exclusion guards, the `--make-issue` exception, what to do afterwards — live in [`$HOME/.claude/skills/x-wt-teams/references/handoff-common.md`](../x-wt-teams/references/handoff-common.md). **Read it**, and read [`claude-handoff.md`](../x-wt-teams/references/claude-handoff.md) for the argv mechanism and the trust prompt.

## Step 1 — Decide what goes in the prompt

Three input shapes. Pick by what the invocation carried.

| Input | Send |
| --- | --- |
| Starts with `/` | **Verbatim.** A caller (or the user) already built the invocation — `/x-wt-teams -m -a 445`. Do not rewrite it. |
| A plan or issue this session produced | A workflow skill invocation — see [Routing a plan](#routing-a-plan) |
| Anything else | **The instruction text, as-is.** Do not wrap it in a workflow skill the user did not ask for. |

**Passthrough is the default and it means passthrough.** `/toclaude refactor the auth middleware to drop the callback shim` sends exactly that. The receiving session is a full Claude Code session with the same skills this one has; deciding its workflow for it is not this skill's job. Only route to `/x-…` when the input genuinely *is* a plan (below) or the user names a skill themselves.

### Routing a plan

When the argument is a plan — a bare issue number, an epic URL, a `-lo` plan directory, or nothing at all in a session that just planned — the new session should run the workflow skill that matches the plan's shape, not read a wall of prose:

| Plan shape | Send |
| --- | --- |
| Two or more sub-issues (an epic) | `/x-wt-teams {epic#}` |
| One sub-issue | `/x-as-pr {sub#}` |
| `-lo` local plan | `/x-wt-teams -lo {LOCAL_DIR}` (or `/x-as-pr -lo {LOCAL_DIR}/sub-01-<slug>.md` for a single topic) |

Prefer a **bare issue number** over a URL — the new session resolves it against the repo it was launched in.

For a bare number you were handed cold, one `gh issue view {N} --json labels,title` settles the route: an `epic` label (or an `[Epic]` title) means `/x-wt-teams`, otherwise `/x-as-pr`.

**With no argument at all**, look at what this session just produced — an epic it created, a plan directory it wrote, a plan it drafted but never filed. Route that. If the session produced nothing plan-shaped, ask what to hand off rather than guessing; an empty hand-off wastes a window and a fresh context.

### A plain slash — and no port check

The target is Claude Code, so `/x-wt-teams` is simply the real skill. There is no `$` prefix here and nothing to verify before sending. If you catch yourself writing `$x-wt-teams` or checking `$HOME/.codex/skills/...`, you have copied from `/tocodex` — that prefix and that check exist only because Codex has no slash commands.

### Never send a command that hands off again

Strip `-tocl` / `--to-claude` and `-toco` / `--to-codex` out of whatever you build. A command that still carries one makes the new session open *another* window and hand off again, recursively. The flag has already done its job by the time you are writing the command.

### Which flags travel

Forward `-a` / `-m` / `-nf` / `-nori` / `-lo` when they were passed, and nothing else — reviewer flags, effort levels and `-s` / `--stay` are the new session's own choice, and it picks its own branch.

**Forward only what was typed.** A bare `/toclaude` after a plan sends `/x-wt-teams 445`, which stops at the PR. `-m` merges and `-a` runs unattended; neither is something to start on someone's behalf because it would have been convenient. Full hands-off is `/toclaude -a -m`.

## Step 2 — Size the prompt

**Write a file when the prompt is multi-line or longer than ~500 characters** — headings, bullet lists, code blocks, acceptance criteria. Otherwise send the text directly.

```bash
PROMPT_DIR="$(node "$HOME/.claude/scripts/get-logdir.js")/toclaude"
mkdir -p "$PROMPT_DIR"
PROMPT_FILE="$PROMPT_DIR/$(date +%Y%m%d_%H%M%S)-<slug>.md"
```

Then the new session gets a pointer instead of the prompt: `Read and follow the instructions in <PROMPT_FILE>.` **Confirm the file exists before launching** — a pointer to a path that was never written starts a fresh session with nothing to read.

The reason is not a length limit; argv would carry it. It is that a spec worth handing over is worth keeping and re-reading, and a short launch command is easier to verify. Write it as a **self-contained spec**, not a transcript: the new session cannot see this conversation, so the goal, the files involved, the constraints agreed here, and what "done" looks like all have to be in the file — that is the whole point of handing over a clean context, and also its one cost. Reference other repos as `$HOME/repos/...`, never machine-absolute paths; cclogs is Dropbox-synced, so the path resolves on either machine.

A `/x-…` invocation is always one short line and never needs a file — the spec already lives in the issue.

## Step 3 — Launch

```bash
bash "$HOME/.claude/scripts/handoff-to-claude.sh" \
  --dir "$(git rev-parse --show-toplevel)" \
  --name "claude-{issue# or slug}" \
  --command '/x-wt-teams -m -a 445' \
  --submit          # omit only under -ns / --no-submit
```

The script opens the window with `CLAUDE_CODE_NO_FLICKER=1`, `--dangerously-skip-permissions` and `--model opus`, waits for the session to come up, and focuses it. The prompt rides in as the CLI's positional argument, so Claude Code submits it itself — there is no composer to type into and no Enter to get wrong.

### The new session starts on Opus

The launch pins `--model opus`, and the script reports which model it pinned — repeat that in the report. A hand-off exists to start *implementation* on a clean context; inheriting whatever this session happened to be dialled down to is not part of a clean start, and the new process has no way to know what the work needs. Opus is the deliberate floor, and the receiving session can still `/model` its way elsewhere.

Pass `--model <alias>` to the script to pin something else, or `--model inherit` to send no `--model` at all and let the new session take its configured default. There is no skill-level flag for this — if the user names a model, hand it to the script.

| Exit | Cause |
| --- | --- |
| 2 / 3 | Not inside tmux / no `claude` on PATH |
| 4 | The directory-trust prompt is up and was **not** auto-answered — `--no-auto-answer`, or its affirmative option was not recognised |
| 5 | Timed out waiting for the session to come up |
| 6 | `tmux new-window` failed or returned no usable pane id — an empty pane id would otherwise resolve to the **current** pane and type into the user's own session |
| 7 | `claude` exited at startup, so the window closed (or the pane is dead) |
| 8 | The session came up but the command did not land — the argv prompt never started (submitted), or the composer keystrokes failed (`-ns`) |
| 64 | Usage error — a missing, unknown, or invalid argument. A caller bug, not a user-fixable state; no fallback command is printed |

Every nonzero exit except 64 prints the command for the user to send by hand. **Surface whatever it prints, verbatim.** Exit 64 means this skill built the invocation wrong: fix the call, do not hand the user a fallback.

**On exit 5 or 8 after a submitted hand-off, do not resend and do not declare it dead.** An argv prompt is not a composer draft — it can still be queued behind a startup prompt, so the script's message tells the user to look at the window first. Under `-ns` the same codes mean nothing was typed and the command must be sent by hand. Repeat whichever the script printed, and let the user decide.

### The directory-trust prompt is answered for you

Claude Code asks `Is this a project you created or one you trust?` the first time it runs in a directory — **even under `--dangerously-skip-permissions`**, and with **"No, exit" preselected**, so an unanswered prompt quietly kills the hand-off. Launching at the current repo root normally avoids it entirely (this session is already trusted there); a worktree or sibling repo can still hit it. The script locates the affirmative option and moves to it rather than pressing Enter on whatever is selected, and stops at exit 4 if it cannot identify that option. It prints what it answered — repeat that line in the report.

## Step 4 — Report and stop

Report the window name, the **exact** command sent, whether it was submitted or is waiting on Enter, and the prompt file path if one was written.

If this session had an active workflow pointer for the work just handed off, close it: `node "$HOME/.claude/scripts/orientation.js" complete`. (`orientation.js show` tells you whether a run is active; skip this when `/toclaude` was a side errand in a session that continues on other work.) Never leave the pointer active for the new session to "adopt" — it cannot read it.

Then stop touching that work. No branch, no PR, no worktree, no cleanup audit for resources that were never created.

## Flags

| Flag | Effect |
| --- | --- |
| `-ns` / `--no-submit` | Type the command into the new session's composer without pressing Enter, so the user reads it and submits. Default is to submit. |
| `-a`, `-m`, `-nf`, `-nori`, `-lo` | Forwarded into a `/x-…` invocation when the input is a plan. Meaningless in passthrough mode — the text goes as-is. |

**Submit is the default because the user asked for the hand-off.** They typed `/toclaude`; staging it would just make them walk to the window and press a key. Reach for `-ns` when the prompt was auto-composed from thin context and is worth reading before it runs.

## When NOT to use this

- **When the user wants to keep working in *this* session.** This skill does not clear the current context — it ends this session's involvement and starts a different one. If they wanted a reset without losing the thread, they want `/clear` themselves, not this.
- **When a subagent would do.** Spawning an Agent already gets a fresh context and reports back here. Use this skill only when the *whole job* should leave, and the new session should own it end to end.
- **Handing the job to Codex** is `/tocodex`. Same shape, different destination: reach for that one when the point is a different tool, and this one when the point is a clean slate. They are mutually exclusive — never fire both.
- **`/x-as-pr -tocl` and `/x-wt-teams -tocl`** keep their own start-of-skill hand-off ([`claude-handoff.md`](../x-wt-teams/references/claude-handoff.md)). Those fire before any branch exists and are already immediate; nothing routes through here.
- **Read-only consultations** — a second opinion or a review answers a question *in this session*. This skill starts an implementation session somewhere else and ends involvement here.

## Examples

```
/toclaude implement the product detail pages
   → new window: claude --dangerously-skip-permissions --model opus 'implement the product detail pages'   (passthrough, submitted)

/toclaude
   → session just planned epic #445 with 6 sub-issues
   → prompt: /x-wt-teams 445                                (submitted)

/toclaude -a -m 445
   → prompt: /x-wt-teams -m -a 445                          (submitted, unattended through merge)

/toclaude /x-as-pr 42
   → prompt: /x-as-pr 42                                    (verbatim, submitted)

/toclaude -ns <long multi-paragraph spec>
   → writes …/cclogs/{repo}/toclaude/20260906_141233-<slug>.md
   → composer: Read and follow the instructions in …/20260906_141233-<slug>.md
   → staged, waiting on Enter
```

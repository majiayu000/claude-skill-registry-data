---
name: tocodex
description: "Hand work over to OpenAI Codex CLI instead of doing it here: opens a NEW tmux window running codex at the repo root on model gpt-6-sol at medium reasoning effort, stages a prompt in its composer, submits it, and focuses the window. This session implements nothing. Use when: (1) User says '/tocodex', (2) User says 'hand this to codex', 'do this on codex', 'let codex implement it', 'implement the next feature with codex', or 'continue on codex', (3) A planning session (typically /big-plan -po) has finished and the user wants Codex to build the epic, (4) /big-plan Step 11 delegates its -toco hand-off here. Default behaviour is to pass the user's instruction through to Codex verbatim; a plan / epic issue is routed to the matching $-prefixed Codex workflow skill ($x-wt-teams or $x-as-pr) instead. Long or multi-line prompts are written to a cclogs file and the path is sent, because the Codex composer takes one line. Submits by default; -ns/--no-submit stages the command for the user to send. Terminal-only (needs tmux plus codex on PATH). NOT for /codex-review, /codex-2nd, /codex-sweep or other read-only Codex consultations -- those answer a question in this session, while this one starts a whole implementation session elsewhere. For a hand-off to a FRESH Claude Code session rather than to Codex -- a clean context window, the agent-side stand-in for /clear -- use /toclaude instead; the two are mutually exclusive."
argument-hint: "[-ns|--no-submit] [-a] [-m] [-nf] [-nori] [-lo] [$codex-skill-invocation | issue-number | instructions]"
---

# Hand off to Codex CLI

Move the work to a Codex CLI session running in a new tmux window. The user plans or explores on Claude Code and implements on Codex; without this they would close the session and start Codex by hand, losing the session's context and the issue numbers it just produced.

**This session implements nothing after the hand-off.** It replaces local work rather than adding to it, so there is no double-implementation risk. Do not create a branch, PR, worktree, or tracking issue for work that now belongs to Codex.

**Terminal-only.** Web has neither tmux nor a local `codex`. If the launch script reports that, surface its message and stop — do not silently implement locally instead, which is the opposite of what was asked.

## Step 1 — Decide what goes in the composer

Three input shapes. Pick by what the invocation carried.

| Input | Send |
| --- | --- |
| Starts with `$` | **Verbatim.** A caller (or the user) already built the Codex skill invocation — `$x-wt-teams -m -a 445`. Do not rewrite it. |
| A plan or issue this session produced | A Codex workflow skill invocation — see [Routing a plan](#routing-a-plan) |
| Anything else | **The instruction text, as-is.** Do not wrap it in a workflow skill the user did not ask for. |

**Passthrough is the default and it means passthrough.** `/tocodex refactor the auth middleware to drop the callback shim` sends exactly that. Codex is a capable agent with its own skills; deciding its workflow for it is not this skill's job. Only route to `$x-…` when the input genuinely *is* a plan (below) or the user names a Codex skill themselves.

### Routing a plan

When the argument is a plan — a bare issue number, an epic URL, a `-lo` plan directory, or nothing at all in a session that just planned — Codex should run the workflow skill that matches the plan's shape, not read a wall of prose:

| Plan shape | Send |
| --- | --- |
| Two or more sub-issues (an epic) | `$x-wt-teams {epic#}` |
| One sub-issue | `$x-as-pr {sub#}` |
| `-lo` local plan | `$x-wt-teams -lo {LOCAL_DIR}` (or `$x-as-pr -lo {LOCAL_DIR}/sub-01-<slug>.md` for a single topic) |

Prefer a **bare issue number** over a URL — Codex resolves it against the repo it was launched in.

For a bare number you were handed cold, one `gh issue view {N} --json labels,title` settles the route: an `epic` label (or an `[Epic]` title) means `$x-wt-teams`, otherwise `$x-as-pr`.

**With no argument at all**, look at what this session just produced — an epic it created, a plan directory it wrote, a plan it drafted but never filed. Route that. If the session produced nothing plan-shaped, ask what to hand off rather than guessing; an empty hand-off wastes a Codex window.

### The `$` prefix is load-bearing — never "fix" it to a slash

Codex has no `prompts/` directory and no custom slash commands; its skills fire on `$name`. A leading `/foo` is claimed by the user's Codex `ccref` skill, which reads it as "go read the **Claude** skill `foo`" — so `/x-wt-teams` would pull in the Claude source instead of the Codex-native port.

Before sending any `$name`, confirm the port exists: `ls "$HOME/.codex/skills/{name}/SKILL.md"`. A `$name` with no port behind it fires nothing and Codex treats the line as prose. If it is missing, fall back to passthrough prose and say so.

### Which flags travel

Forward `-a` / `-m` / `-nf` / `-nori` / `-lo` into the Codex invocation when they were passed. Do **not** forward reviewer flags (`-co`, `-nor`), effort levels, or `-s` / `--stay` — those are the Codex session's own choice, and it picks its own branch.

**Forward only what was typed.** A bare `/tocodex` after a plan sends `$x-wt-teams 445`, which stops at the PR. `-m` merges and `-a` runs unattended; neither is something to start on someone's behalf because it would have been convenient. Full hands-off is `/tocodex -a -m`.

## Step 2 — Size the prompt

The composer takes **one line** — the launch script collapses newlines and tabs to single spaces so what lands there is deterministic. A prompt that only reads correctly as multiple lines does not survive that.

**Write a file when the prompt is multi-line or longer than ~500 characters** — headings, bullet lists, code blocks, acceptance criteria. Otherwise send the text directly.

```bash
PROMPT_DIR="$(node "$HOME/.claude/scripts/get-logdir.js")/tocodex"
mkdir -p "$PROMPT_DIR"
PROMPT_FILE="$PROMPT_DIR/$(date +%Y%m%d_%H%M%S)-<slug>.md"
```

Then the composer gets a pointer instead of the prompt: `Read and follow the instructions in <PROMPT_FILE>.`

Write the prompt as a **self-contained spec**, not a transcript. Codex cannot see this conversation, so anything it needs — the goal, the files involved, the constraints agreed here, what "done" looks like — has to be in the file. Reference other repos as `$HOME/repos/...`, never machine-absolute paths; cclogs is Dropbox-synced, so the path resolves on either machine.

A `$x-…` invocation is always one short line and never needs a file — the spec already lives in the issue.

## Step 3 — Launch

```bash
bash "$HOME/.claude/scripts/handoff-to-codex.sh" \
  --dir "$(git rev-parse --show-toplevel)" \
  --name "codex-{issue# or slug}" \
  --command '$x-wt-teams -m -a 445' \
  --submit          # omit only under -ns / --no-submit
```

The script opens the window as `codex -m gpt-6-sol -c model_reasoning_effort="medium"`, answers Codex's startup prompts, waits for the composer, types the command, and focuses the window. It handles what silently breaks a naive `send-keys`, and reports the model and effort it pinned — repeat that in the report.

### The Codex session starts on Sol at medium effort

The launch pins `-m gpt-6-sol` and `-c model_reasoning_effort="medium"`. A hand-off fires *after* the planning is done: the receiving session is executing a spec that has already been argued out, which is a manager's job — dispatch the work, keep the run moving — not a reasoning-heavy one. Re-deriving decisions that are already written down buys nothing, so the manager sits at Sol/medium and workers are dispatched by the Codex `x-wt-teams` difficulty policy — `high` → `gpt-6-astra`/high, `mid` → `gpt-6-sol`/medium, `standard` → `gpt-6-luna`/max. The Codex session can raise its own with `/model` if the work turns out to need it.

Pass `--model <name>` or `--effort <level>` to the script to pin something else, or either one as `inherit` to send no flag at all and let `~/.codex/config.toml` decide. There is no skill-level flag for this — if the user names a model or an effort, hand it to the script.

| Exit | Cause |
| --- | --- |
| 2 / 3 | Not inside tmux / no `codex` on PATH |
| 4 | A startup prompt is up and was **not** auto-answered — `--no-auto-answer`, or an update prompt with no recognisable "No" option |
| 5 | Timed out waiting for the composer |
| 6 | `tmux new-window` failed — an empty pane id would otherwise resolve to the **current** pane and type into the user's own Claude session |
| 7 | `codex` exited at startup, so the window closed |
| 8 | The command was typed but Codex did not start on it after three Enter presses — the draft is left in the composer for the user to submit |
| 64 | Usage error — a missing, unknown, or invalid argument. A caller bug, not a user-fixable state; no fallback command is printed |

Every nonzero exit except 64 prints the command for the user to send by hand. **Surface whatever it prints, verbatim** — a failed hand-off leaves the work un-started, and that fallback is what the user needs. Exit 64 means this skill built the invocation wrong: fix the call, do not hand the user a fallback.

Codex needs ~10-14s before it accepts input, so the script polls for the composer rather than sleeping blind.

### Startup prompts are answered for you

Two Codex prompts can sit in front of the composer, and anything typed while one is up goes into the prompt, not the composer. The script answers each once, then keeps waiting:

| Prompt | Answer | Why |
| --- | --- | --- |
| `Do you trust the contents of this directory?` | **Yes, continue** | Project-local config, hooks, and exec policies must load for the skill to run |
| An update offer — a numbered menu, or a `[y/N]` line, mentioning "update" | **No** | Updating mid-hand-off is never what the user asked for; they upgrade Codex on their own schedule |

It prints what it answered — repeat that line in the report. Codex renders inline, so an answered menu stays visible in the pane above the live composer; that is expected, not a lost answer.

## Step 4 — Report and stop

Report the window name, the **exact** command sent, whether it was submitted or is waiting on Enter, and the prompt file path if one was written.

If this session had an active workflow pointer for the work just handed off, close it: `node "$HOME/.claude/scripts/orientation.js" complete`. (`orientation.js show` tells you whether a run is active; skip this when `/tocodex` was a side errand in a session that continues on other work.) Never leave the pointer active for the Codex session to "adopt" — it cannot read it.

Then stop touching that work. No branch, no PR, no worktree, no cleanup audit for resources that were never created.

## Flags

| Flag | Effect |
| --- | --- |
| `-ns` / `--no-submit` | Stage the command in the composer without pressing Enter, so the user reads it and submits. Default is to submit. |
| `-a`, `-m`, `-nf`, `-nori`, `-lo` | Forwarded into a `$x-…` invocation when the input is a plan. Meaningless in passthrough mode — the text goes as-is. |

**Submit is the default because the user asked for the hand-off.** They typed `/tocodex`; staging it would just make them walk to the window and press a key. Reach for `-ns` when the prompt was auto-composed from thin context and is worth reading before it runs.

## When NOT to use this

- **Read-only Codex consultations** — `/codex-review`, `/codex-2nd`, `/codex-sweep` answer a question *in this session*. This skill starts an implementation session somewhere else and ends involvement here.
- **`/x-as-pr -toco` and `/x-wt-teams -toco`** keep their own start-of-skill hand-off (`$HOME/.claude/skills/x-wt-teams/references/codex-handoff.md`). Those fire before any branch exists and are already immediate; nothing routes through here.
- **Handing the job to a fresh Claude Code session** is `/toclaude`. Same shape, different destination: this one when the point is a different tool, that one when the point is a clean context (the agent-side stand-in for `/clear`). They are mutually exclusive — never fire both.

## Examples

```
/tocodex implement the product detail pages
   → new window: codex -m gpt-6-sol -c model_reasoning_effort="medium"
   → composer: implement the product detail pages          (passthrough, submitted)

/tocodex
   → session just planned epic #445 with 6 sub-issues
   → composer: $x-wt-teams 445                             (submitted)

/tocodex -a -m 445
   → composer: $x-wt-teams -m -a 445                       (submitted, unattended through merge)

/tocodex $x-as-pr 42
   → composer: $x-as-pr 42                                 (verbatim, submitted)

/tocodex -ns <long multi-paragraph spec>
   → writes …/cclogs/{repo}/tocodex/20260826_141233-<slug>.md
   → composer: Read and follow the instructions in …/20260826_141233-<slug>.md
   → staged, waiting on Enter
```

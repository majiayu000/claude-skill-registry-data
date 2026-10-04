---
name: fork-conversation-pane
description: Branch the current Claude Code conversation into a new tmux pane (or window) of the session you are already in, using `claude --resume <id> --fork-session`. Use when the user says "fork this conversation", "branch this into a new pane", "open a second Claude on this context", "split off a copy of this session", or wants to explore an alternative approach without losing the current thread.
argument-hint: "[optional: seed prompt for the fork] [-v vertical] [-s 40%] [-d don't focus] [-m model]"
allowed-tools: Bash(tmux:*), Bash(claude:*), Bash(~/.claude/skills/fork-conversation-pane/fork-pane.sh:*), Bash(ls:*), Bash(grep:*), Read
---

# Fork the Conversation Into a tmux Pane

Spawn a second Claude Code process, in a new pane of the window you are currently
running in, whose context is a **copy of this conversation up to the last flushed
turn**. The two sessions then diverge independently.

Run the bundled script — it encodes every guard below. Do not hand-roll the
`tmux split-window` line unless the script's options genuinely don't cover the case.

## Faster: the `prefix + X` key binding

If the user just wants a plain fork of the pane they are sitting in, they do not need
this skill at all — `prefix + X` (new pane) and `prefix + C-x` (new window) run
`~/dotfiles/tmux-fork-claude.sh`, which resolves pane → session ID from
`~/.claude/sessions/<pid>.json` and calls the same `fork-pane.sh`. That skips the model
round trip entirely, which is the only slow part. **Say so** when the user is asking for
a bare fork repeatedly.

Reach for this skill instead when the fork needs something the key can't express: a seed
prompt, a worktree (`-C`), a pinned model (`-m`), or forking a session other than the
one in this pane. The traps behind that lookup (headless `sdk-cli` sessions claiming
the same pane, `run-shell` not setting `TMUX_PANE`) are in
`.docs_claude/notes/claude-session-tmux-pane-lookup.md` in the dotfiles repo.

## Core Recipe

```bash
~/.claude/skills/fork-conversation-pane/fork-pane.sh
```

That is the whole common case: it resolves this session's ID and this pane's window,
splits, launches the fork, labels the new pane, and prints the new pane ID.

With a seed prompt so the branch starts working immediately:

```bash
~/.claude/skills/fork-conversation-pane/fork-pane.sh -d -s 40% \
  "Take the alternative approach: rewrite the installer as a single idempotent script."
```

Options: `-v` vertical (stacked) instead of side-by-side · `-s SIZE` (`40%` or `80`) ·
`-d` leave focus in the current pane · `-m MODEL` pin the fork's model ·
`-W` new window instead of a pane · `-S ID` fork a session other than this one ·
`-n NAME` override the derived display name · `-A` suppress the fork notice.

The script gives the fork the two things in-app `/branch` gives it and bare
`--resume --fork-session` does not: a display name `"<parent> ⑂ <seed>"` (`⑂` is U+2442,
the glyph `/branch` uses) and an `--append-system-prompt` telling it the parent is still
live in this checkout, so it doesn't edit files out from under it. The notice is emitted
only when the fork shares the parent's directory — with `-C` it is already isolated.

Report the new pane ID to the user, and tell them `tmux kill-pane -t %NN` undoes it.

## Why Each Guard Exists

These are the failure modes, all confirmed on Claude Code 2.1.232 / tmux on Linux.
Every one of them is already handled by the script.

1. **Get the session ID from `$CLAUDE_CODE_SESSION_ID`.** It is exported into the
   Bash tool's environment. Do *not* parse the scratchpad path and do *not* take the
   newest `*.jsonl` in `~/.claude/projects/<mangled-cwd>/` — those are fallbacks only,
   and "newest transcript" silently picks the wrong session when two Claudes share a
   directory (common here — `tmux list-panes -a` routinely shows several). When the env
   var is genuinely unavailable — e.g. a tmux key binding, which gets no Claude
   environment at all — the exact answer is `~/.claude/sessions/<pid>.json`, keyed by
   pid and carrying both `sessionId` and `"tmux":"<sess>:@<win>.%<pane>"`.
2. **Resolve the window with `-t "$TMUX_PANE"`.** A bare
   `tmux display-message -p '#{session_name}:#{window_index}'` reports the *attached
   client's* pane, which is only coincidentally the pane Claude is running in. When
   Claude is running in an unfocused pane or a detached session, the bare form splits
   the wrong window.
3. **`--fork-session` requires `--resume` or `--continue`.** Alone it is a no-op flag.
4. **`exec` in the split command.** Without it the pane keeps a shell parent and
   lingers after `claude` exits instead of closing.
5. **Capture the new pane ID with `-P -F '#{pane_id}'`**, not by diffing `list-panes`.
   The diff is racy when anything else is creating panes.
6. **The fork inherits the *transcript's* model, not the global default.** A forked
   Sonnet session comes up as Sonnet even when the user's default is Opus. Pass
   `-m` when the branch needs a specific model.
7. **The branch point is the last flushed transcript entry** — the turn currently in
   flight is *not* in the fork. Spawn the fork on the turn whose state you want
   branched, and never promise the fork can see something decided moments ago.
8. **A CLI fork has no pointer back to its parent.** The transcript is a full copy of
   all entries rewritten under a fresh UUID, with no `parentSessionId` field. In-app
   `/branch` *does* record lineage (`forkParentSessionId`, `forkBoundaryAt`) — but in
   the **job registry**, read only when `CLAUDE_JOB_DIR` is set, so a pane fork cannot
   have it and never appears in the roster as a branch. The pane title can't carry it
   either: Claude Code overwrites the title with its own conversation summary seconds
   after startup. The `--name` the script passes survives (it shows in the fork's prompt
   box), and the printed `forked:` line is the durable record — **relay it to the user**
   when spawning more than one branch. With `-W` the window name also survives.
9. **The fork's transcript file does not exist until its first message.** Verifying a
   fork by looking for a new `*.jsonl` gives a false negative on an idle fork —
   verify with `tmux capture-pane -p -t <pane>` instead.

## Verifying

The script polls up to 30s for the fork's prompt box and reports `ready` or
`launched (not confirmed ready)`. 30s is deliberate — replaying a large transcript
regularly takes longer than 10s to draw the UI, and a shorter timeout reports a
healthy fork as unconfirmed. `not confirmed ready` means "still replaying, probably
fine"; an actual startup crash is reported separately as `pane died during startup`
with the pane's output. To inspect what the branch sees:

```bash
tmux capture-pane -p -t %NN | grep -v '^\s*$' | tail -15
```

## Variations

**Diverging edits — isolate the working tree.** Two Claudes in one checkout will
overwrite each other with no coordination. When the branch exists to *try a different
implementation*, give it its own tree:

```bash
git worktree add /tmp/fork-alt HEAD
~/.claude/skills/fork-conversation-pane/fork-pane.sh -C /tmp/fork-alt
```

**Read-only branch** (analysis, second opinion, no file writes) — the same checkout is
fine; no isolation needed.

**Fork someone else's session:** pass `-S <uuid>`. List candidates with
`ls -lt ~/.claude/projects/<mangled-cwd>/*.jsonl` where the directory name is the cwd
with `/` and `.` replaced by `-` (`/home/jke/dotfiles` → `-home-jke-dotfiles`).

## When Applying This Skill

1. **Confirm the intent is a branch, not a subagent.** A fork is for the *user* to
   drive a divergent thread interactively. For delegated work that reports back, use
   the Agent tool instead — a fork's output never returns to this conversation.
2. **Decide the branch point.** The fork sees through the previous turn only. If the
   user wants recent context included, let the current turn finish first.
3. **Choose isolation.** Divergent edits → worktree (`-C`). Analysis → same tree.
4. **Choose focus.** Default moves focus to the fork. Use `-d` when the user is
   mid-thought here and just wants the branch waiting.
5. **Decide whether to seed a prompt.** Seed it when the branch has a clear job;
   leave it empty when the user wants to type into it themselves.
6. **Report the pane ID and the kill command.** The user cannot see the tool output.

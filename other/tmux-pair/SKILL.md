---
name: tmux-pair
description: >-
  Share Anton's tmux session as one cockpit: read any pane he names, run code
  in a shared IPython or R REPL whose state you both keep, and run commands in
  r2 windows he can watch and steer. Use when he says "look at pane N", asks to
  share a REPL, or wants a run he can see.
license: MIT
---

# Share the tmux session

The orchestrator runs inside the pilot's tmux session (`$TMUX` is set, `$TMUX_PANE` names its own
pane). Every pane in that session is one shared environment: the pilot sees and types into it, and
the agent reads it and writes to the windows it owns. `scripts/r2.sh` is the agent's half; resolve it
relative to this `SKILL.md`.

## Roles

| | Pilot | Agent (R2) |
|---|---|---|
| Owns | every window, by default | windows named `r2*` |
| Reads | everything | any pane, when the pilot names it or the task needs it |
| Writes | everywhere | `r2*` windows, plus panes the pilot hands over in chat |

The pilot hands over a pane by saying so in the conversation; the agent then runs
`r2.sh hand TARGET` and writes to it. `r2.sh unhand TARGET` returns it. The script's guard catches
slips: it writes to `r2*` windows and handed panes, and refuses the agent's own pane and a handed
pane the pilot is focused on. Consent itself lives in the chat.

## Read a pane

```bash
"$skill_dir/scripts/r2.sh" peek main:2.4 60
```

"Look at pane 2" replaces copy-pasting a traceback or a log. `peek` prints the last lines of the pane
as plain text, with wrapped lines joined. Take the tail the question needs: every line read enters
the context. Anything visible in the pane, a token included, enters it too.

Targets use tmux syntax: `main:2` is window 2's active pane, `main:2.4` is pane 4 of window 2, and
`main:r2` is the window named `r2`.

## Share a REPL

```bash
"$skill_dir/scripts/r2.sh" repl r2 python          # or: repl r2-r r
"$skill_dir/scripts/r2.sh" run main:r2 600 <<'EOF'
adata = sc.read_h5ad("03_results/objects/lung.h5ad")
print(adata)
EOF
```

`run` pastes the block as one bracketed paste, then sends a second cell that signals a tmux wait-for
channel. It returns when the signal arrives and prints only the lines the block produced. A block
that raises still signals, because the signal is its own cell. A heavy object loaded once serves
both of you: the pilot types `adata.obs.head()` in the same window, and the agent's next block sees
whatever the pilot defined.

On timeout `run` exits 124 and prints what the pane holds so far; the block keeps running. Take turns
in a shared window: a block sent while the pilot is mid-line interleaves with the pilot's keystrokes.

## Attend a milestone stage

A milestone compute stage is one whose details the pilot wants to follow as they happen: SCENIC+,
scVI or scANVI training, a deep-learning loop, a long peak or motif scan. It runs in a watched window
by default, so the pilot can ask about specifics while they are on screen and shape the run.

```bash
"$skill_dir/scripts/r2.sh" stage 30_scvi /workspaces/Meta-Aging/14782-DM 7200 <<<'python 02_analysis/stages/30_scvi.py'
```

`stage` opens `r2-30_scvi`, runs the command on a terminal of its own, and returns when the stage
exits: the last 30 lines, then `STAGE=r2-30_scvi exit=0 log=…/logs/30_scvi.log`, with the stage's exit
code as its own. The window renders by weight, so the pilot's eye lands on what matters:

| Weight | Lines |
|---|---|
| red | tracebacks, errors, out-of-memory, `nan`, `Failed` |
| bold, cyan tag | the stage's own milestones, printed as `[tag] text`: `[fit] best epoch 281 · elbo 923.2` |
| plain | every other line the stage prints |
| cyan, redrawn in place | progress bars: epoch, loss, cells per second |
| dim, once | library warnings and banners; repeats fold into a count on the footer |

The log holds the whole output as plain text, each warning and each bar at its final state, so `grep`
and `less` read it directly.

1. The command is a committed stage under `02_analysis/stages/`, so the record reproduces from the
   repository. A driver that chains stages lets each inherit its stdout, which keeps every stage on
   the terminal.
2. A stage prints its milestones as `[tag] text`: what it fitted, how many cells or peaks it kept, the
   number the pilot will ask about. Those lines carry the run.
3. Before the launch, tell the pilot the window name, what the stage computes, the run length you
   expect, and the signals worth watching.
4. Run `stage` as a harness background task with a timeout longer than the stage, so the harness
   notifies at the exit.
5. When the pilot asks about the run, `peek` the window first and answer from what it shows.
6. The pilot interrupts with Ctrl-C or types into the window; a changed parameter starts a new run.
   `r2.sh done 30_scvi` closes the window once the stage is accepted.

`run` sends a one-line `CMD 2>&1 | tee LOG` through the same renderer, so a habitual tee lands in
the weighed view too.

## Watch a delegated run

One run has one window, and the window is the view.

```bash
"$skill_dir/scripts/r2.sh" watch S02_relations /workspaces/Meta-Aging/14761-DM   # opens r2-S02_relations
"$skill_dir/scripts/r2.sh" ls                                                      # each watched unit with its state
"$skill_dir/scripts/r2.sh" done S02_relations                                      # at acceptance
```

`watch` opens `r2-<unit>` running `view.sh --follow` from `delegate-cli`: the brief's title with model
and effort on the first line, the worker's messages in colour, one line per command with its outcome,
and output folded to its head, tail and test summary. The launcher itself runs as the orchestrator's
harness background task, since its output is a record for the orchestrator. The unit name is the
window name, so it carries stage and topic (`S02_relations`).

The window belongs to the unit. Open it once, before or after the launch: it waits for the first
run, renders each run as it starts, and marks a resume with `── next run <id> ──`, so a resumed or
relaunched unit shows in the same window with no second `watch`. `watch` prints `WINDOW=` once the
view is live and exits 2 with the view's message when the view fails, which leaves the window open
on that message. `done` closes it once the unit is accepted.

## Scratch and memory

A window, its scrollback and the wait-for channels are scratch, and they close with the run. The log
file, the stage's outputs and the reading the pilot and agent reach together are the record: the
reading goes into the stage-keyed note under `docs/_internal/`, and delegated runs keep their streams
in `_delegations/`.

## What the shared session gives, and its limits

- The agent perceives on its own turns. Between turns it rests until a `run` signal or a harness
  task wakes it.
- Full-screen programs (nvim, pi's TUI, htop) capture as a redrawn snapshot and read poorly. REPLs,
  shells and logs read cleanly.
- A block sent into a pane executes in the pilot's shell or kernel, outside the per-command review
  that the agent's own tool calls receive. Show the block in the tool call, keep it to what the task
  needs, and treat it with the care of a direct command.
- `r2.sh ls` lists the agent's windows, each watched unit with its state, and the handed panes. A
  window closes when its work is accepted: `r2.sh done <name>` for a run or a stage, `tmux
  kill-window -t main:r2-train` for a REPL.

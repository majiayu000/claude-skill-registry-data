---
name: orca-tab
description: "Use when opening an Orca tab or launching grok, dsb, codex, or claude with the orca CLI. Run these recipes; do not run orca skills get orca-cli."
---

# Orca tab

These recipes are the procedure for opening a tab or launching an agent.
They were checked against Orca CLI **1.4.211** (`orca --version` and
`--help` for `terminal create`, `terminal send`, `terminal wait`,
`terminal read`, and `worktree create`).

**Do not run `orca skills get orca-cli` before §1–§4.** That guide is the
whole CLI (248 lines on 1.4.211). Reading it is what stalls a turn whose
only job is to open a tab or launch grok. A user-level skill that says
"load the full guide before any orca command" does not apply to these
recipes. If a flag here is rejected, read only `orca <that-command> --help`
and retry once.

Worktree occupancy, branch names, merge, and cleanup stay in
[`worktree-dispatch`](../worktree-dispatch/SKILL.md). This file only
launches the tab and hands it a prompt.

## Which recipe

| Ask | Recipe |
|-----|--------|
| A tab in a worktree that already exists | §1 |
| A new worktree whose agent is grok, codex, or claude | §2 |
| A new worktree whose agent is dsb / deepseek-build | §3 |
| A prompt into a tab you already have | §4 |
| Browser, automations, artifacts, anything else | Then `orca skills get orca-cli` |

The user named the agent. Launch that one. Do not swap grok for dsb, or
dsb for grok. When the opening did not name an agent, launch `dsb`.
`codex` and `claude` only when the user named them. This repo's sessions
are `dsb` and `grok`.

A worktree whose only tab is a shell prompt has no session. On 2026-09-26
`pin-tower-main`, `ci-cache-and-coverage`, and `deepseek-native-depth-6-1-0`
showed that prompt and nothing else. The grok processes were tabs on the
primary checkout, driving those directories with `git -C`. The iOS app
showed the same empty cards. `orca worktree create` without §2 or §3 is
how that happened.

## Pass the name, not a binary path

The tab's shell evaluates `--command`. On this machine `grok`, `dsb`, and
`deepseek-build` are shell functions in `~/.oh-my-zsh/custom/ai.zsh`, and
the function is the part that matters:

| Name | What the function does |
|------|------------------------|
| `grok` | Sets `GROK_HOME=$HOME/.grok`. A bare binary inherits a `GROK_HOME` left by dsb (`~/.deepseek-build`) and then reads the wrong model catalog. |
| `dsb` | Injects `DSB_OFFICIAL_API_KEY` from the keychain, then runs the `dsb` binary. The same file records that skipping the function inherits Orca's `DEEPSEEK_API_KEY` and `api.deepseek.com` returns 401 (2026-09-26). |
| `deepseek-build` | The same wrapper as `dsb`. Prefer `dsb`. |

`codex` and `claude` are Orca agent ids. Pass those names the same way.

`--agent` accepts `grok`, `codex`, and `claude`. It rejects `dsb`
(`Unknown TUI agent "dsb"`, measured 2026-09-25). There is no one-step
create for dsb.

## §1 Tab in an existing worktree

If that worktree already has a prompt-only tab, send `dsb` or `grok` into
that tab. Do not create another. `terminal create` is for a worktree with
no tab.

```sh
orca terminal create --worktree "path:$WT" --title "<short title>" --command dsb --json
```

Use `grok`, `codex`, or `claude` as `--command` when that is the agent.
`active` is fine for `--worktree` only when this shell is already that
worktree. From the control tower, pass `path:$WT` or `id:$WT_ID`.

The handle is `result.terminal.handle`. If you cannot parse it, **do not
create again**. Ask `orca terminal list --worktree "id:$WT_ID" --json`
and use the tab that is already there.

Then §4. For `dsb`, do not treat `tui-idle` as the gate. Orca records no
agent identity for it, so the wait times out while the TUI is already on
screen. Read the screen.

## §2 New worktree — grok, codex, or claude

One create. Do not also run the bare create in `worktree-dispatch` §1.

```sh
orca worktree create \
  --repo path:"$TOWER" \
  --name <slug> \
  --no-parent \
  --setup skip \
  --agent grok \
  --prompt "<one line, or: Read <file outside the repo> and do what it says.>" \
  --json
```

`$TOWER` is `dirname "$(git rev-parse --path-format=absolute --git-common-dir)"`.
`<slug>` has no type prefix (`orca-tab`, not `docs/orca-tab`). Orca turns
`/` into `-`.

The handle is `result.agentTerminalHandle`. If that is absent,
`result.startupTerminal.handle`. If both are absent, `terminal list` the
new worktree and take the tab whose agent matches. Do not create a second
worktree because the handle was missing.

`--activate` only when a person asked to look at the tree.

Branch rename and cleanup: `worktree-dispatch` §2 and §4. Then confirm
with the screen read in §4. `tui-idle` can be true while a trust dialog
is still up.

## §3 New worktree — dsb

`create` opens one launcher shell. That shell is the tab. Do not open a
second one with `terminal create`. On 2026-09-26 a worktree ended with two
tabs: the empty shell, and `dsb`.

```sh
orca worktree create --repo path:"$TOWER" --name <slug> --no-parent --setup skip --json
```

Keep `result.worktree.id` and `result.worktree.path`. List that worktree's
terminals. The shell is the tab whose screen is a prompt. Send `dsb` into
it:

```sh
orca terminal send --terminal "$SHELL" --text dsb --enter --wait-submit 15 --json
```

Read the screen. When the DeepSeek input box is up, `$SHELL` is the
session. Then §4 on that same handle.

Do not pass `--agent dsb`.

If a second tab is already `dsb` and another tab is only a prompt, close
the prompt after the agent screen shows it is working:

```sh
orca terminal close --terminal "$SHELL" --tab --json
```

Do not close the tab whose screen is the agent. The worktree should show
one tab. The same close applies when §2 leaves a prompt next to `grok`.

## §4 Send, after the screen shows an input box

```sh
orca terminal wait --terminal "$H" --for tui-idle --timeout-ms 60000 --json
orca terminal read --terminal "$H" --screen --json
```

`satisfied: true` is not "ready for a prompt". On grok, the folder-trust
dialog has satisfied `tui-idle` while `No, exit` was still the default
(measured 2026-09-25, Orca 1.4.210). Enter at that moment confirms No,
the agent exits, and the brief is gone.

```text
 Quick safety check: Is this a project you created or one you trust? …
 ❯ No, exit
   Yes, I trust this folder
 Enter to confirm · Esc to cancel
```

Read the screen.

- Input box visible, no dialog: send.
- Trust dialog, and the yes line is readable: move to that line, read
  again, confirm the selected line's **text** says yes, Enter, read
  again, then send. Grok's dialog takes `y` / `n`.
- A dialog you do not recognise: stop and report. Do not press keys.
- `dsb` and the wait timed out: read the screen anyway. If the TUI is up,
  send. If it is not, report that the handoff did not start. Do not
  `sleep`, and do not send blind.

```sh
orca terminal send --terminal "$H" --text "<brief>" --enter --wait-submit 15 --json
```

Done when `accepted` is true and `stages` includes `turn_started`, **or**
the screen shows the agent working on the brief. A receipt that stops at
`input_accepted` with `provider: unsupported` is unproven, not failed
(measured on grok, 2026-09-25). Read the screen. **Do not resend** — the
first send may have landed. After a transport error, repeat the same
command with `--retry-request <id>` from the receipt.

A long brief is a file **outside** the repo. Send one line:
`Read <file> and do what it says.`

What the brief should contain (unit, boundaries, language, authority)
stays in `worktree-dispatch` §3b.

## Anti-patterns

| Don't | Why |
|-------|-----|
| `orca skills get orca-cli` before §1–§4 | That read is the stall |
| A binary path instead of `grok` or `dsb` | Skips the shell function |
| `--agent dsb` | Rejected. dsb is §3: run `dsb` in the launcher shell |
| `terminal create --command dsb` beside the launcher shell | Two tabs. The shell is the tab; send `dsb` into it |
| Create again when the handle did not parse | The tab already exists |
| `--enter` while a dialog is up | Confirms the dialog's default |
| Resend on silence | The first prompt may already be in |
| `sleep` to wait for dsb | The screen is the check |

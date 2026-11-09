---
name: iterm-agents
description: Use when a session on macOS must manage the agent sessions of its orchestrator — windows of the orchestrator's home session, or iTerm2 tabs — spawn a fresh agent with a startup prompt and verify it is running, close a stood-down agent, list sessions, place a tab next to another, or replace a context-saturated agent with a fresh one (rotation).
user-invocable: false
---

# Agent windows and tabs

## Overview

`${CLAUDE_PLUGIN_ROOT}/skills/iterm-agents/scripts/iterm-agent.sh` drives the places agents run in — windows of the orchestrator's tmux home session, and iTerm2 tabs through the app's own API — so an orchestrator can spawn, verify, close, move and rotate implementer sessions without the user touching the keyboard. The launch is HANDED to the terminal, never typed into a shell. Closing a window or a tab KILLS its session — treat close as destructive and follow the safety order below. **Spawning is the orchestrator's act, not the user's**: the brief is written, the session is spawned in the same move, and the spawn is verified on the process, never on the script's word.

Its commands are `list`, `spawn`, `verify`, `screen`, `close`, `move`, `rotate`, `resolve-tier`, `pair`, `trust prune` and `tools`. **Before typing any of them, read `references/commands.md`** — each command's synopsis, flags and refusals, and how the launcher builds a tab; **when one fails, hangs or says on stderr that a fallback served it, read its « When iTerm2 does not answer »**.

## Reading the tabs

`list` prints each tab's title, the session's name, and `self` on your own tab. Read self before you anchor, move or close.

- **tty numbers are recycled**: a freshly closed `/dev/ttys000` can be reassigned to the next spawned tab. Never reuse a stored tty across a close — re-`list` every time.
- **A fresh tab is titled « Chat » for a few seconds**: to find a session right after a spawn, read `list`'s name column, not its title.
- The spawned session takes a few seconds to appear in `ListAgents`; `list` shows the tab immediately, `verify` the process as soon as the CLI has started.

## An agent is a window of its orchestrator's home session, or a tab

An orchestrator's tab is a real terminal that holds a tmux session of its own, its **home session**: the orchestrator runs in window 0 and **every agent it spawns is a window of that session**, one server per orchestrator tab. There is no command for the operator to type: the orchestrator command, at the end of the turn that names the session, converts its own tab into the home session and resumes the same conversation in window 0. A session that is neither a window of the home session nor a tab in the window the operator reads is not an agent he can see, place or close, and a launcher that hands him one has hidden the fault rather than repaired it. **Never spawn an agent outside the home session and outside iTerm2** — not through a tmux server of your own, not through `screen`, not by hand.

- **Windows are a placement, not a rung.** Which one a spawn gets is decided by the caller's own session (below), never by a failure. When both iTerm2 rungs are down, the app itself is wedged, and that has a one-keystroke remedy: the launcher names it and stops, and `tmux` is not offered as a way round for any tab it must make. Stopping loudly on a fault whose remedy is known IS the repair.
- **One agent = one window (or one tab), never a pane.** A pane shares a window's title and its fate; the tooling closes sessions, but a layout the operator reads is not a place to put an agent.
- **The auditor stays an iTerm2 tab.** It is read beside the build, not part of it, and its place left of its caller is a tab position that means nothing in a window bar.
- **The operator switches** by clicking a block of the tab bar, or with `C-b n` and `C-b p` (next and previous window). The windows keep their numbers, 0 for the orchestrator and 1, 2, … after it, though the bar shows none, so `C-b <digit>` still selects one. `C-b C-b` sends a Ctrl-B to the program in the pane, which is how the host's « run in background » key is typed.
- **The bar** is one padded block per window, the current one bold on yellow, with no index, no session name and nothing on the right; the state is an icon after the name — busy ●, idle ○, asks ✋, done ✓, gate ⚠ — written by the module on the window when it changes.
- **Closing the iTerm2 tab ends the orchestration.** Once the tab's client is proved attached, the server is set to exit when no client is left, so the tab's close ends the server, the orchestrator and every agent window. A server shown by no tab is never set so, and a takeover kills a window with the tab still attached. The launcher's `close` on the tab does the same and proves every window gone.

## Reading the placement

The launcher chooses the terminal from where the caller runs: **inside a home session** — `$TMUX` set and the session carrying the mark the plugin's configuration gives it — an agent is a window made with `new-window -d`, which never takes the operator's view; **anywhere else** (a plain tab, or a tmux session the operator made by hand) it is an iTerm2 tab, exactly as before. A tmux that cannot answer inside a pane is a refusal that names the cause, never a silent fall to the tab.

## Layout convention

**In a home session** the order of the bar is the order of the windows: window 0 is the orchestrator's, and an agent takes the next free index, so the bar reads left to right as launch order. `--right-of self` is still the form to type, so one command serves both placements: the launcher reads it as « after my last still-open agent ». A spawn cannot place a window first or left of another: the launcher says so and the window takes the next free index. `move` goes to `move-window`, and refuses window 0, the orchestrator's, as the session moved and as an anchor to place something before. The chain (`chains/<your tty>.jsonl`) names each window by its server and its window id, `tmux:<socket>:@N`, because a pane's tty is recycled just the same, and its owner is the orchestrator's pane, `tmux:<socket>:%N`, because every window of a server inherits the server's `ITERM_SESSION_ID`.

**On tabs** (any other caller), the orchestrator's tab sits immediately LEFT of its implementer agent's tab.

A plain `spawn` with no placement flag lands beside its orchestrator: right of your last agent still in your group, or right of you when you have none. When your own tty cannot be read it falls back to the window's end, with one note on stderr saying why.

Name an anchor when you know a better place than that default, and name the one you actually know:

- spawning an implementer: `--right-of self` — after your LAST still-open agent while it still sits in your group (the run of your agents right of your tab), otherwise directly right of you; an agent spawn given no placement flag is placed this way too, never at the window's end. The launcher keeps the chain (`chains/<your tty>.jsonl` under the state directory) and the order reads left to right as launch order: you, agent 1, agent 2, … A closed agent leaves the chain; a tty is never trusted across a close, the chain is checked on the place's id (the app's tab id, or the window's), and on the session that wrote the entry — a tty is recycled and its chain file outlives its occupant, so a new session on an old tty reads only its own entries.
- spawning your successor: `--successor`. On tabs it is immediately right of your own tab, the chain ignored, so it lands between you and your first agent. In a home session it is a new window of that session, and its `takeover --tty --expect-title` kills your window 0, guarded by the title, and takes that index; the agents keep their windows, and it needs no tab of its own. In both the launcher hands it your chain (your agents' entries move under its tty and session) and writes it into no chain, because a successor is not an agent. The entry naming your place in any chain (your orchestrator's, if it spawned you) follows the successor, owner and resident mark kept. It ends your place once the takeover is confirmed, and its `--right-of self` resolves to your last agent from then on. Your agents follow you to your successor: the spawn and the `takeover` move every entry of `chains/<your tty>.jsonl` into its chain and remove your file, and `list` adds an `orphan:` line for each agent whose orchestrator ended before handing it over. An `Orch :` tab is opened only with `--successor`, `--open` or `--wake`; any other spawn under that title is refused, and an auditor opens none (its only successor is its own audit session).
- spawning a resident agent: `--resident` — for an agent meant to stay idle while a background command of its own waits; its chain entry is marked so the stop gate never counts it as an idle agent to read or relaunch, and it is still closed like any other when its purpose ends.
- spawning an auditor: `--auditor` — a tab immediately left of your own, the chain ignored and none joined, from a home session too. Its place is read after the spawn and repaired if wrong: the launcher lists the real tab order, moves the auditor left of its caller when it is not there, reads again, and if it is still wrong says so on stdout with the `move` that repairs it and exits non-zero, the session kept.
- `--left-of <tty>` remains for the case where the anchor you know is on the other side, on tabs.
- `move` repairs the layout after the fact, with the same three forms, plus `--leftmost` for the first place of a tab window — but for `move`, `self` is your own place, never the end of your chain: `move --tty <tty> --right-of self` puts that session immediately right of yours, `move --tty <tty> --leftmost` puts a tab at the first place of its window (a home session refuses it: that place is window 0's); any other session is moved with a warning (stderr, `close.log`); `--force` only for the tabs that stay refused.

## Safety order for a launch

1. The brief exists at a path the fresh session can open on this machine. Say in the agent's brief which servers it was given: it cannot see the file.
2. `spawn --brief <path> --orchestrator "<name [ref]>"`, with `--right-of self` so the tab lands beside yours rather than at the end of a window you do not own. `--brief` lints the brief (a finding warns on stderr, the launch goes on) and builds the startup prompt — the brief's path and your exact `ListAgents` name and reference. You never hand-build that prompt; a launch with no prompt at all is refused.
3. Read the result: the script has already waited for the host CLI on the new tty, but the artifact decides — `list` (the tab), `verify --tty` (the process), `ListAgents` (the peer session, a few seconds later).
4. **No startup dialog may stand between the launch and the brief.** `--trust` is for a checkout you prepared yourself, never for anything else; the launch loads the catalogue's default set plus `--mcp`, and `--account-connectors` every connector of the operator's account (`references/commands.md` says how each dialog is pre-answered). Any other startup question (a migration notice) is read in the tab's contents and answered through the tab — a session stuck on a dialog is not launched, whatever the script printed.
5. Rely on that verification and on the module's reports, not on a first message. An agent idle before its work is reported is inspected, not waited for: `verify` for the process, `list` for the tab, and `screen --tty` for what that tab is showing right now — how you tell an agent stopped on a question from one at work.

**Every launched session carries its model and its effort** (decision 3 of `docs/agent-dispatches.md`): an agent's pair is yours to name, `--tier <t>` or `--model <id> --effort <level>`, and a succession of any role runs on its predecessor's live pair, read on its transcript. How a tier's effort is chosen is `orchestrator:model-routing`, « Pairs, tiers and the map », and each form's flags and refusals are in `references/commands.md`.

**A tier nobody bound is not an error**: `spawn` types no model argument and the host applies its default model, at the tier's effort. What to do about it is `orchestrator:model-routing`'s, « Pairs, tiers and the map ».

## The tools a session is given

Every session the launcher opens loses the tools no session has called, because the host sends each loaded tool's schema on every call: `Artifact`, `SendFeedback`, `Workflow`, `ScheduleWakeup` and `ReportFindings`, and, for every title but `Orch :` and `Coord :`, the three the module registers to move an orchestrator between machines. The set is removed at launch; the dry run prints it as `tools_removed=`.

- `--keep-tool <name>` gives one back for this spawn: a brief that asks for a page keeps `Artifact` (`--keep-tool Artifact`).
- `--drop-tool <name>` removes any other tool or permission pattern for this spawn. Both repeat; an empty name, or one name given to both, is refused before a tab exists; `rotate` forwards them, so a replacement keeps a tool only when `rotate` is given the option again.
- `--keep-synced-skills` leaves the account's synced skills (`anthropic-skills:*`, hidden from every launched session by default) in the session, for a brief that invokes one.
- `tools` lists what a session on this machine is given and what each item costs per call, read from a transcript (yours by default, `--transcript <path>` for another), with the roles whose default removes it.

An `Agent :` session also comes up without the away recap and the silent-turn reminder, and every launched session without the host's token countdown (the gate is the module's, not that figure). Read `references/commands.md` for the synopses and refusals.

## Window and tab hygiene

**A finished agent's window or tab is closed, not left open.** The approval that closes a phase stands the agent down and closes its place in the same move (`list`, `close --tty --expect-title`, `ps`). An implementer is stood down at the verification of its delivery, never kept through its review round, unless its next phase is dispatched to it at that verification; a review finding goes to a fresh session with a resume brief, which costs one cold start and keeps the window readable. The only places open at any time are the orchestrator's and its running implementers' (and the auditor's tab). `close --tty` on a hidden agent closes its session alone — its tab and its review pane stay open (`references/commands.md`, the hidden-pane entry).

**A window or a tab is closed by its tty with `--expect-title`, never by title alone or by position** — the title read from `list` seconds before (a rotation takes none, below). Match on words, never on the first character, an activity glyph that flips on its own.

Prompt and launch files accumulate under the state directory's `prompts/`; they are small and they are the record of what each session was launched with. Delete a wave's when its review is closed, like any other artifact you produced.

## Safety order for a live rotation

1. The old agent must have STOOD DOWN (message it; wait for its acknowledgment) — never close a tab whose session may still be writing. **In a rotation this acknowledgment IS the guard**, not the title.
2. `list` to confirm the tty is the one you mean.
3. `rotate`, which spawns the replacement and verifies it is running before the old one is gone. **Do not pass `--expect-title` to a rotation**: a working session rewrites its title during the ten seconds of the spawn. The tty is the identity; a stood-down agent that acknowledged is what makes closing it safe.
4. Verify with `list` (the old tab gone, the new one present) AND `ListAgents` (new peer session visible, old one gone) before reporting the rotation done.

`--expect-title` remains right for a STANDALONE `close`, where you read the title from `list` seconds before and nothing runs in between.

## Common mistakes

- Handing the user a brief path and an invocation to paste: the orchestrator spawns (Overview).
- Trusting the printed tty: launch steps 3 and 5.
- Closing by title alone or by position: « Window and tab hygiene ».
- Spawning without an anchor where you know a better place than the default: « Layout convention ».
- Reading a process that runs in a directory the host never opened as a launched agent: it is stopped on a question — launch steps 4 and 5.
- Rotating before the old agent acknowledged stand-down, or passing `--expect-title` to a rotation: rotation steps 1 and 3.
- Storing a tty and using it after any close happened in between: « Reading the tabs ».

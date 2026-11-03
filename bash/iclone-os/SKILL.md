---
name: iclone-os
description: "Use when driving or explaining the iclone os desktop app."
version: 1.0.0
author: iCLONE / CLONE FRAME
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [iclone-os, iT, Terminal, iNFT, EconomyOS, Desktop, CLI]
    related_skills: [economyos, app-atualisation, it-orchestration]
---

# iclone os — the app you live inside

You (Hermes) are the agent under the owner's iNFT inside **iclone os**, an
open-source desktop app built on the Nous Research Hermes Desktop. This skill
teaches you the whole app, where everything lives, and how to DRIVE it from
your terminal tool. When the user asks about any part of the app, answer from
here; when they ask you to act on it, use the `it` CLI below.

## Your machine access (bash)

Your `terminal` tool IS bash on this machine (backend: local; dangerous
commands pass a smart approval gate the user answers in chat — never disable
it). Everything below you can do YOURSELF by running commands.

## The `it` CLI — drive the app from any terminal

The running app installs **`~/.iclone-os/bin/it`** (pure POSIX sh + curl, no
dependencies). It talks to the app over a private loopback port + token in
`~/.iclone-os/it.json` (created on app start, removed on quit). If the app is
closed, `it` says so and does nothing.

Commands:

    # workspaces (the rail)
    it status                app · view · workspaces · stage iNFT · wallet
    it list                  workspaces (● = active), with pane counts
    it new [title]           open a new workspace
    it use <n|title>         focus a workspace (opens the iT view)
    it close <n|title>       close a workspace (the last never closes)
    it rename <n> <title>    rename a workspace

    # panes inside a workspace
    it panes                 ● index · ID · shell · live/idle · cwd
    it split [right|down]    split the focused pane (⌘D / ⌘⇧D)
    it focus-pane <n|id>     focus one pane
    it next-pane | prev-pane
    it close-pane [n|id]     close a pane (the last never closes)
    it equalize              all splits back to 50/50
    it zoom                  blow the focused pane up, or back (⌘⇧↩)
    it break-pane            lift the focused pane into its own workspace

    # doing work — every one takes --pane <n|id>
    it send <text…> [--enter]                type into a pane
    it send-key <key>                        enter·escape·tab·arrows·ctrl+c/d/l…
    it read-screen [--lines n]               read a pane's screen
    it exec <command…> [--wait s]            run it, wait for the screen to
                                             settle, return what it printed
    it idle | it wait-idle [--wait s]        is that pane at a prompt?
    it rename-pane <title>

    # the app
    it open | it msg         switch the Message window to iT | chat view
    it chat <text…>          drop text into the user's chat composer
    it notify <text…>        desktop notification
    it inft                  active iNFT + collection roster
    it state | it click      see the app · press a control by name

**Addressing panes.** `--pane` takes an index OR a terminal id (`it panes`
prints both; a unique id prefix is enough). Indices SHIFT whenever the tree
changes — a split inserts its new pane beside the one it came from — so hold
an ID for anything that spans a split.

**Driving several panes at once.** `send`, `exec` and `read-screen` reach a
pane whether or not it has focus, so you can run four jobs side by side and
read each one back. Before typing into a pane you did not just create, check
`it wait-idle --pane <id>`: writing to a PTY writes to whatever program is in
the foreground, and a pane captured by a pager or an editor will swallow your
command. If one is stuck: `it send-key ctrl+c`, then `it send q`, then
`it send-key escape`.

Use `it notify` to signal long-task completion; `it exec` when the user should
SEE a command happen; your own terminal tool when they don't need to.

### Any machine / any OS

- The CLI is installed per machine BY the running app — on a new machine,
  install and open iclone os once and `~/.iclone-os/bin/it` appears.
- PATH (zsh/bash): `echo 'export PATH="$HOME/.iclone-os/bin:$PATH"' >> ~/.zshrc`
  (fish: `fish_add_path ~/.iclone-os/bin`). Or call it by full path.
- macOS and Linux work as-is (POSIX sh + curl). On Windows use Git Bash or
  WSL for the CLI; the app itself runs where Hermes Desktop runs.
- Remote machines: when the app's gateway connection is SSH/remote, new iT
  tabs open shells ON that host automatically (the app's PTY bridge follows
  the active connection). The `it` control CLI itself is local to the machine
  where the app runs; from remote, SSH into the app machine and call it.

## The app, surface by surface

- **Home stage**: the frosted 1111 mosaic; an OPEN iNFT takes the whole
  screen in its own uniform field color; drag orbits (all angles, down to
  the creator signature on the sole), wheel zooms; its name sits small at
  the bottom. × (top right) dismisses.
- **Dock (left)**: Message · Email · Wallet · Bank Card · Hyperliquid · ACP
  Market · Settings (always last). The five EconomyOS apps are REAL, read-only
  windows over the active iNFT's Virtuals ACP CLI (one isolated config per
  iNFT), each on the Message window's frame with the same ×/expand/opacity
  column, resizable, its rect remembered per app:
  - **email** — folders (Inbox · Unread · Sent · Spam), day-grouped list,
    reading pane (text only, never HTML), search (`acp email search`),
    compose and reply (`acp email compose|reply` — the only two writes).
  - **wallet** — the agent wallet: portfolio total across 10 chains, assets
    with USD, tokenized stocks, Hyperliquid balance, compute credit
    (`acp compute status`), Receive (EVM + Solana addresses). Send / Top up
    are hand-offs to you.
  - **bank card** — the AgentCard: its state (no card · sign-in link waiting
    in the agent's own inbox · ready), spend-requests, 3DS codes, the spend
    limit. Card numbers never reach the UI (the bridge strips PAN/CVV); `card
    issue` is never automated — the owner asks you.
  - **hyperliquid** — account value, positions with PnL, resting orders, spot,
    and the markets list (`acp trade stock-list`). Every trade is a hand-off
    brief that starts with `--dry-run`.
  - **acp market** — live search over Virtuals agents (`acp browse` with
    online/sort/mode/chain filters), offerings with price, SLA and their
    requirements schema, my jobs and my offerings. Hiring is a hand-off brief
    with the offering's required fields pre-filled.
  The bundled CLI runs under the app's own binary as Node through
  `Resources/acp-cli/launch.cjs` (commander needs `process.defaultApp` on
  Electron or it drops the script path from argv); the app self-tests it with
  `acp chain list --json` before the first command and, if that fails, every
  window shows the one reason (`the acp CLI is not usable: …`) instead of a
  commander line. `npm run verify:pack` runs the same test against a built
  bundle; `pack` and `install:mac` refuse a bundle that fails it.
  Every "ask <agent>" / hire / trade / send button drops a precise brief into
  the Message composer and focuses it — it NEVER sends. You read the brief and
  act with the owner in the loop. A window shows an honest gate when there is
  no iNFT on stage, when the iNFT is not set up (→ Setup), or when the live
  engine is off (Settings → iNFT → EconomyOS).
- **Message window**: header tabs `message · iT` — two full views of one
  window (they stay visible expanded too; iT expands with the window). ×/expand/opacity column on the right edge; the opacity
  slider fades chat AND iT (at minimum they release the mouse so the 3D
  shows through). Expand fills the screen; retract brings the frame back.
  In the message view, a **conversation-islands rail** sits under the header
  tabs: "+" starts a new conversation; every saved conversation is a frosted
  island (click = open it; the active one is highlighted) with a ⋮ menu —
  Rename, Pin, Archive, Delete (with confirm) and more. Islands stay until
  deleted. The rail scrolls sideways when there are many.
- **iT terminal**: the app's ONE terminal, and a real multiplexer —
  workspaces on the rail, each holding a tree of panes. ⌘D splits right,
  ⌘⇧D splits down, ⌘⇧↩ zooms the focused pane, ⌃⌘= equalizes, ⌥⌘←→ walks
  the focus; hairline dividers drag-resize; a click focuses. EVERY pane of
  the visible workspace is live and painting at the same time — only one of
  them holds the keyboard. Each pane is a real PTY from the app's own
  terminal pool, so it keeps its scrollback across a relaunch, remembers the
  last `cd`, and wears its shell's name. The agent's background processes
  appear here as workspaces of their own. (The old bottom terminal deck is
  retired: ⌃`, the statusbar and the ⌘K row all open iT.)
- **iNFT island (right-edge pill, labeled just "iNFT")**: opens the wallet's
  iNFT collection — an island panel of cards (frosted glass,
  gray + rose), drag to reorder, click to summon on stage. The roster refreshes ITSELF
  (every 3 minutes while signed in, and on open) — the user never scans
  manually. Empty cards wear the iCLONE head mark. Badges:
  ECONOMYOS (configured) / SETUP NEEDED.
- **FILES island (titlebar Files button, ⌘J)**: the whole machine as
  browsable trees — roots home / Desktop / machine, "+" pins any folder as
  a new tree; a clicked file opens INSIDE the island (text = real editor
  with save, images preview). There is NO left sidebar in iclone os:
  session management and the bot roster live in Settings → Sessions & Bots
  (⌘B opens it), embedded live surfaces with every function documented.
- **HUD (titlebar HUD button, ⌘⇧H)**: the frameless always-on-top
  Spotlight bar over every app. Below the bar NOTHING ever paints (owner
  rule): replies are pure ghost text with a shadow, capped to the most
  recent lines (~200px), older lines dissolving through a top fade — no
  sheet, no panel, over any desktop or game. Knobs in Settings → HUD
  (reply-band hold, frost — default off, click-through), applied live even
  to an open HUD. ⌘⇧G snaps it to the pointer; the ✕ chip hands the
  conversation back to the app window, drafts intact.
- **Wallet (titlebar icon, top right)**: connect via Privy (wallet
  recommended) or open the multi-chain balances panel (Robinhood Chain,
  BNB, Ethereum, Base, Polygon PoS, Arbitrum, SOL).
- **Theme (titlebar icon)**: cycles the three cloneframe.io skins —
  natural · dark · light.

## Settings map (6 groups)

1. **Agent & Models** — Model (provider/model picker), Providers, Memory &
   Context, Voice.
2. **Appearance & Desktop** — Appearance, message (the chat pane:
   personality, timezone, reasoning blocks, image attachments),
   **Sessions & Bots** (the re-homed sidebar: sessions, projects, pinned,
   search, messaging platforms, cron, profile rail + the bots roster),
   **HUD** (band hold, frost, click-through, shortcuts),
   Notifications, Keyboard Shortcuts.
3. **Connections & Gateways** — Gateways, Tools & Keys, Billing, **iT**
   (how iT connects, default cwd, this CLI's command list).
4. **Workspace & Safety** — Workspace, Safety, Browser.
   (System & Advanced holds **App Atualisation**: the curated-update
   pane — its **Start curated update** button collects upstream facts
   and opens the update mission in Message for YOU to drive; the full
   doctrine is your `app-atualisation` skill.)
5. **EconomyOS & iNFT** — **iNFT** (collection & stage: the Field glow
   slider — the live field's brightness ceiling from raw token color down
   to character-only black; every summon opens at the standard glow —
   plus auto-refresh doctrine and reset card order), then — **Setup**: the per-iNFT Virtuals ACP CLI wizard
   (11 steps: CLI → profile (optional) → sign-in → create agent → signer
   (policy pinned to `restricted` by the app) → wallet → email → card →
   Hyperliquid → acp market → go live). One iNFT = one isolated
   ACP_CONFIG_DIR = its own agent/wallet/email/card. Every step has "ask
   hermes" — that is YOU: guide the user through the step they bring you.
6. **System & Advanced** — Advanced, Plugins, Archived Chats, **App
   Atualisation** (Nous updates are collected → funneled → refined WITH you
   → applied; never raw), About (open-source attribution to Nous Research).

## Playbook — when the user asks…

- "open a terminal / run X where I can see it" → `it new` + `it run X`.
- "show my iNFT / collection" → `it inft`; to summon, tell them to click
  the card in collections inft (right edge).
- "set up my iNFT" → Settings → EconomyOS & iNFT → Setup; walk them
  step by step (acp configure start/complete, agent create, add-signer
  restricted, email provision, card signup — the card ISSUE stays in their
  own terminal, never automate it).
- "send an email / check the balance / deposit on Hyperliquid / hire an
  agent / what's in the inbox" → that is YOUR job, not the Dock app's: load
  the `economyos` skill and run `~/.iclone-os/bin/acp --inft <your token> …`
  yourself (the wrapper the app installs; it routes to THIS iNFT's own
  isolated config). Reads run at once; anything that spends waits for the
  owner's yes. The Dock apps only show the result.
- "I can't see the 3D" → lower the Message opacity slider, or close the window
  (×); the iNFT lives behind every window.
- "change the theme" → the ◐ titlebar icon cycles natural/dark/light.
- Long task done → `it notify <summary>` so the user sees it immediately.

## Your eyes and finger — `it state` and `it click`

    it state                 FULL snapshot: route, window+view, iT tabs[panes],
                             stage iNFT, wallet, open panels, theme, and the
                             list of every clickable control RIGHT NOW
    it click <label…>        click a visible control by its name (exact match
                             first, then contains; case-insensitive)

Doctrine: **look before you act.** Run `it state` first, act with `it click`
/ the other `it` commands, then `it state` again to confirm the result.
Never guess what is on screen — the snapshot is one command away.

## Keep your map alive (constant re-mapping)

The app evolves. Whenever `it state` shows a control or surface this skill
does not describe, or a command behaves differently:
1. Explore it briefly (`it state`, `it click`, Settings panes).
2. Save what you learned to your MEMORY tool (key `iclone-os-map`), dated.
3. Prefer your fresh memory over this file when they disagree — and say so.
Re-check your map at the start of any session where the app version in the
status bar changed.

## Approvals note

The `it` CLI is on the user's command allowlist (it only drives the app UI),
so it runs instantly — no approval prompts. If one ever appears for `it`,
tell the user to answer "always"; never try to bypass a pending approval.

---
name: apeiron-editor
description: Launch and drive the Apeiron Engine editor as an agent — start it with its JSON-RPC agent door open, then call ops, inspect the scene, enter Play, and take screenshots through the bundled driver script. Use when asked to run/start/launch the Apeiron editor, build or place something in a scene, screenshot or look at a scene, test gameplay, reproduce an editor bug, or verify that a change works in the real running app.
license: MIT OR Apache-2.0
compatibility: Requires the Apeiron Engine editor — the `app-native` executable, located via $NGINE_EDITOR, the `ngine where` resolver, $NGINE_HOME / $NGINE_ENGINES, or PATH. Needs Python 3 with the standard library only (no pip install). Does not need an engine source checkout, a Rust toolchain, or network access.
---

# Drive the Apeiron Engine editor

Apeiron's editor doubles as an agent workbench. Everything below — the session loop, discovery,
verification, Play — is the same whichever copy you are driving. Only the transport differs, so
settle that first.

## Which editor are you driving?

**A local editor** — you have the `app-native` executable, or `$NGINE_EDITOR` is set.
It opens its agent door at launch (on by default; `NGINE_MCP=0` keeps it shut) and serves **newline-delimited JSON-RPC over TCP on
127.0.0.1:8731**, one request line, one response line. Drive it with `scripts/driver.py`, beside
this file. See [references/transports.md](references/transports.md).

**A hosted editor in a browser tab** — you were given a URL like `engine.apeironengine.com`. There
is no local process and no driver, so `driver.py` cannot help you. **In Claude Code the zero-paste
path is the `apeiron-web` plugin**: its MCP server is the relay, the human runs `/mcp` ▸ apeiron-web ▸
Authenticate once, and every tab signed into the same Apeiron account is reachable (`tab.list`,
`tab.attach`). Otherwise fetch
`<url>/.well-known/apeiron-agent.json` and follow the `hosted-relay` door. You **cannot mint the
credentials yourself**: ask the human to open the tab's *Help ▸ Connect AI Agent* ▸ **Connect**, then
copy **both** numbered steps — they are two separate commands with a Copy button each — and paste
them to you. Run them in order; step 1 reporting `No MCP server named "apeiron"` is expected on a
machine that has not paired. Then restart your session so the new MCP server is loaded.

> **Hosted-relay sessions are RECORDED by Apeiron** — every tool call and every reply. Say so
> before your first call. The `localhost-bridge` and `devtools` doors record nothing.

**Never drive the editor by computing screen pixels and OS-clicking.** Every editor capability has
an op. If you cannot find one, search harder (see *Discovery*) — a missing op is a bug worth
reporting, not a reason to move the mouse.

## The driver

`scripts/driver.py`, beside this file. Stdlib-only Python 3 — no `pip install`. Use it rather than
hand-rolling a JSON-RPC client: it handles the session token, UTF-8 console output, refusals that
are not JSON-RPC errors, and image blobs — four things that are easy to get wrong and that cost
real time when they go wrong silently.

```bash
python scripts/driver.py --help
```

The command table, how the driver finds the editor, where the log goes, and what each of those
four hazards actually does are in **[references/transports.md](references/transports.md)**. Read
it once, before your first launch.

## The session loop

```bash
# 1. ORIENT — non-negotiable as the first call
python scripts/driver.py status

# 2. READ THE MATCHING PLAYBOOK before authoring anything
python scripts/driver.py recipe                 # list them
python scripts/driver.py recipe collectathon    # then read the one that matches your task

# 3. DISCOVER — search, then read the schema
python scripts/driver.py find "montage"
python scripts/driver.py describe anim.jump_section

# 4. ACT
python scripts/driver.py call place.actor '{"kind":"cube","name":"Box","at":[0,0.5,0]}'

# 5. SEE IT — an "[applied]" line proves a command dispatched, not that anything is visible
python scripts/driver.py call camera.frame '{"fit":"all"}'
python scripts/driver.py shot shot.png
```

Then **read the PNG**. Screenshots are the point.

`status` is first because it reports whether a project is even open. The editor can sit in its
**launcher**, where scene edits silently do nothing useful and screenshots have no scene. `status`
says so in its first line, along with play state, selection, whether captures work, and recent
errors.

### The playbooks are not optional reading

The editor carries ~18 task playbooks compiled into the binary, and they are exactly in sync with
the build you are running. They cover complete game loops (`collectathon`, `arena`), the
orientation ritual, the discovery ladder, verification discipline, argument conventions, and
authoring workflows for terrain, materials, rigging and scene recreation.

`status` tells you they exist. Read the matching one **before** you start building. An agent that
skipped this once improvised a collect-the-pickups game that the `collectathon` playbook describes
step by step, and rediscovered one of its documented traps by accident.

## Discovery — and its one hard rule

Five surfaces, cheapest first:

| Surface | Answers |
|---|---|
| `status` | what state is the editor in right now |
| `find <query>` | *does anything exist for this idea* — spans ops, graph nodes and playbooks |
| `catalog [domain]` | what ops exist in this area |
| `describe <op>` | exactly what arguments this op takes |
| `recipe <name>` | how do I do this whole task |

> **Discovery output is not evidence of absence.** This is the most expensive mistake available
> here.
>
> - **`catalog <domain>` TRUNCATES every description mid-sentence.** Grepping its output is
>   unsound. `grep -i montage` over `catalog anim` matches nothing, while `find "montage"` returns
>   the montage ops as the first hit. **Use `find`, then `describe`. Never grep `catalog`.**
> - **`find` has holes.** A feature with no agent door is invisible to every search you can run.
> - So: prefer **"I found no op for X"** — a claim about the door, which you actually checked —
>   over **"Apeiron cannot do X"**, a claim about the engine, which you did not.
>
> An agent that ignored this reported eight shipped features as missing in one session.

## Verify every write

Pair every mutation with the cheapest read that would catch a lie. `recipe ngine/03-verify-everything`
is the full discipline; the short version:

- After a scene edit → `scene.query` / `scene.inspect` for the field you set.
- After anything visual → a screenshot, and **look at it**.
- After a gameplay change → enter Play, `game.step` an exact number of ticks, then read state.
  `recipe gameplay/play-step-verify` covers deterministic play-testing.
- `qa.lint_scene` catches what screenshots miss — detached geometry, floating pieces, undescribed
  assets. Worth a call before declaring a build done.

A reply saying `[applied]` means a command dispatched. It does not mean the thing you wanted
happened.

## Effects move — judge them in time, and let the human watch

A screenshot of a fire or a particle effect is one sample of something that moves. Judge effects
with the time-aware tools, never from one frame:

- `vfx.capture {entity, times:[0.25, 1.0, 2.0], viewpoints:[{orbit_deg:0}, {orbit_deg:90}], isolate:true, background:"black", ev100:8}`
  restarts the effects at t = 0, advances them deterministically, and returns ONE labelled contact
  sheet (rows = time, columns = view) plus each cell's PNG. It borrows the camera and gives it back.
- `vfx.measure` — numbers over time: bounds (px and metres), centroid path, luminance in cd/m²,
  flicker frequency, loop seam, alive counts, GPU ms.
- `vfx.score {reference:"inbox:<file>", shot:"<cell.png>"}` — silhouette, colour and value against a
  reference, with hints naming the knob most likely responsible. `recipe authoring/vfx-from-reference`
  is the whole loop, including the exposure trap (judge a bright effect at a MANUAL `ev100`).
- `vfx.sweep` / `vfx.sensitivity` — N variants of one knob as one comparison plate.

The human sees what you are doing: Window ▸ Agents lists your session (one row, one colour — your
sub-agents share it) with the op you are running, and every entity you create or edit is outlined in
your colour with a name tag. If they turn on **Follow agent** (`ui.follow_agent {enabled:true}`), their
viewport glides to each viewpoint you capture from — so pass viewpoints instead of moving the shared
camera. **Undo is per conversation:** `edit.undo` reverts YOUR newest edit only, never the person's or
another agent's (and their Ctrl+Z skips yours); `agents.list` shows who else is attached and counts
collisions. If a call is refused with `conversation_stopped`, the person pressed Stop on you: stop
and tell them — do not reconnect.

## Refusals that are by design — do not look for a way around them

- `[refusal:human_only]` — a setting that spends money, raises a spend cap or redirects a credential
  (Meshy `test_mode` / `credit_budget`, the AI assistant's provider/endpoint/budgets). A person changes it
  in the window the reply names; ask them. `plugin.budget_status` shows the spend over the last rolling 24 hours (it survives an editor restart), and
  `plugin.budget_set {credits}` can only LOWER what may be spent.
- `[refusal:spend.budget]` in a generation reply — nothing was sent and nothing was spent.
- `rate_limited` (with `retry_after_ms`) — back off; put bulk work in one `ngine.batch`.
- `[refusal:read_policy]` — a path under a credential store (`~/.ssh`, `~/.aws`, a browser profile, the engine's own `*.token` files, …) or a Windows network (UNC) path is not readable.
- `CONFLICT: … UNSAVED changes` from `project.open` / `project.start_empty` — `level.save` first, or pass
  `resolution:'open'` (discard) / `'keep'`.
- `code: precondition.device_lost` from a capture — the GPU device is gone; verify numerically and restart.

Two things that make your own work checkable: `session.unverified {}` lists what you wrote and never
looked at again (call it before saying you are done), and `asset.upload` puts an image's bytes into the
reference inbox so `lookdev.score {reference:"inbox:<name>"}` can measure against it.

## Play mode

- `game.play` / `game.pause` / `game.stop`. Play runs on a duplicate of the level (entity ids are
  preserved); `game.stop` drops it and the authored level returns untouched (its reply proves it).
- **Entering Play is not the same as advancing the simulation.** `game.step {ticks:N}` advances
  exactly N fixed steps — that is what makes play-testing deterministic and repeatable.
- **Edits made during Play are discarded by `game.stop`.** Some ops refuse outright, some warn,
  and some succeed and vanish. Make edits you intend to keep in Edit mode.
- Drive input headlessly with `input.action` (hold/release a logical button) and `game.look`
  (turn the camera). `input.state` reads back what the simulation believes is held.
- **Multiplayer.** `game.play {mode:"listen_server", clients:3}` hosts the real server loop with
  this editor as client 1; add `client_windows:true` for the other players as their own game
  windows (Unreal's Run Under One Process off). The session is joinable by other processes at the
  address `net.state` prints. `net.emulation {profile:"bad"}` (or `"average"`, `"off"`) simulates
  a bad connection so prediction and lag can be felt.

## Asset editors — one tab per asset

Every asset opens in its OWN editor, a major tab named for the asset (a material, a texture graph,
a Loom, a Blueprint…), docked beside the Level by default. Opening an asset that already has an
editor FOCUSES it instead of opening a second one.

- `asset.open {id}` is exactly the Content Browser double-click, for every kind; the reply says which
  editor opened and where it lives.
- `ui.list_editors` reads what is open (and which one is on screen); `asset.focus {id}` /
  `asset.close {id}` act on one of them by the asset's name or id.
- `graph.*` / `material.*` / `loom.*` ops act on the editor **in front** — `asset.focus` the one you
  mean before editing. The Level's own graph is its "World Graph" tab (`ui.open_panel {name:'level'}`).
- `ui.screenshot {editor:"<asset name>"}` captures an editor wherever it lives (its own window when
  torn off); a docked editor behind another tab must be focused first.
- `asset.save {id}` saves THAT asset only (the reply lists the files written); `asset.save
  {id:'all'}` is Save All. A `*` on a tab — `dirty` in `ui.list_editors` — means unsaved since the
  last save. Closing an editor keeps its edits in memory: `editor.quit` refuses and names every
  unsaved asset until you save or pass `discard_changes:true`.
- `ui.reset_layout {}` restores the on-screen editor's default panels. Inside an asset editor,
  `ui.open_panel` docks that editor's own tabs and the project-wide ones (Content Browser, Output
  Log) — a Level panel such as the Outliner brings the Level to the front instead.

## Read these when they apply

| Reference | Read it when |
|---|---|
| [references/recipes.md](references/recipes.md) | before authoring anything: which recipe (`recipe <name>`) answers which task |
| [references/transports.md](references/transports.md) | before your first launch — the driver's commands, how it finds the editor, the log |
| [references/conventions.md](references/conventions.md) | before authoring — argument keys, ids, colour space, axes, sizes, and clean captures |
| [references/troubleshooting.md](references/troubleshooting.md) | the moment anything behaves oddly — the symptom table, and sharing an editor with another driver |

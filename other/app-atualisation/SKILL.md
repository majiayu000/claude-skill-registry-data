---
name: app-atualisation
description: "Use when asked to update iclone os or its Hermes agent. Also when you notice the agent is outdated: you suggest Settings › Updates › Agent and the user clicks; you never run the update, even when asked. Also covers the upstream channel."
version: 4.0.0
author: iCLONE / CLONE FRAME
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [iclone-os, updates, upstream, adoption, compatibility, engineering, runtime]
    related_skills: [iclone-os, agent-self-repo, it-orchestration]
---

# App Atualisation — curated updates, engineered

Two different things call themselves "the update", they live in two different
trees, and confusing them is how a machine gets broken. Read this page, then
load the reference for the track you are on. **Do not work from this page
alone** — the procedures, flags and failure modes live in the references.

## The two trees

| | **Track A — the runtime** | **Track B — the app repo** |
|---|---|---|
| Where | `~/.hermes/hermes-agent` | the app's source checkout (`<your project folder>/app`) |
| What | The Hermes backend + CLI. **The python that IS you.** | The iclone os source: Electron desktop + our `iclone/` work |
| Git | origin `NousResearch/hermes-agent`, `main`; a **full** clone today (43,945 commits on 2026-09-26 — it was shallow at import) | the icloneOS development repository; the public release is `devclone20/icloneos`; remote `upstream` = NousResearch |
| Updated by | **The user, on click (U, 2026-10-19).** Settings › Updates › **Agent** checks Nous Research for the newest agent (the `main` tip — what `hermes update` installs) only when the user presses *Check for updates*, and updates only when the user presses *Update to vX…* and confirms: full backup first, iclone os closes, `hermes update --backup` runs from Nous Research, iclone os reopens. The bundled pin (`iclone/RUNTIME_PIN.json`) is the **verified floor**, never a ceiling; *Restore the verified version* is the rollback | Curated adoption — an upstream change is studied, re-implemented in our design and recorded in the ledger; never merged |
| Where it stands | Installed vs latest in the Agent section; the last answer is `userData/agent-update-last-check.json` (`installed`, `latest`, `updateAvailable`, `checkedAt`); the last run is the receipt card (`~/.hermes/logs/update_receipts/latest.json`) | Imported once from upstream `10b38830` (`iclone/UPSTREAM_BASE`, fixed); triaged up to `iclone/upstream/adoption/CURSOR` |

Re-check the clone with `git -C ~/.hermes/hermes-agent rev-parse
--is-shallow-repository` before quoting any shallow-clone rule: local counts
and fast-forwards only fail on a shallow graph.

**Nothing comes from outside on its own.** iclone os never checks Nous Research at boot, on a timer, on focus or on
resume; Hermes's own `updates.check` stays `false` in every HERMES_HOME the app spawns. The one door to the network is
the user's click in Settings › Updates › Agent. About's **Check for updates** asks only the iclone os app updater.

Both desktop apps — the stock `Hermes.app` and `/Applications/iclone os.app` —
run the SAME runtime (`electron/main.ts`:
`ACTIVE_HERMES_ROOT = HERMES_HOME/hermes-agent`). Track A therefore changes the
backend under iclone os too, which is why Track A carries its own compatibility
check for the app above it.

## Which track is this?

| The signal | The track |
|---|---|
| The stock `Hermes.app` dialog *"New update available"* | Not iclone os: iclone os has no automatic upstream check since R1. Do not click it on the owner's machine. |
| Settings › **Updates** › **Agent** (Check for updates / Update to vX… / Restore the verified version) | **A** |
| Settings → **App Atualisation** → Inbox, or an ADP ticket | **B** |
| The owner says "update the app" with a screenshot of the Hermes dialog | **A first**, then offer B — the same upstream commits are waiting on both sides |
| A specific upstream feature the owner wants in iclone os | **B** |

## Routing table — load the reference before acting

| Task | Load |
|---|---|
| What the pane's update runs (never you — even when asked, you open the pane); flags; pre-flight; rollback; reading the log | `references/runtime-update.md` |
| Is the target runtime compatible with the app? Verdict levels, the gate, fixing forward | `references/compat.md` |
| Collect / Funnel / Re-implement / Record; counting the delta | `references/curated-funnel.md` |
| Dispositions, the ledger, ADP tickets, commit trailers | `references/adoption.md` |
| Verdict of the lock against the installed and a target runtime (≤ 30 lines) | `scripts/contract.sh` |
| The adoption backlog, top rows (≤ 30 lines, no repo writes) | `scripts/adoption.sh` |
| Gate the runtime update and take both backups | `scripts/preflight.sh` |
| Prove a runtime update worked | `scripts/verify.sh` |

## The short form of Track A — you suggest, the user clicks

**How you know.** Read `agent-update-last-check.json` in the app's userData folder (through the app's file bridge) when
its `checkedAt` is under 24 h old. Otherwise, and only inside a conversation where the user asked about updates, run the
read-only `hermes update --check`. Never check on your own at session start.

**What you say** — one sentence, then the offer:

> Your agent is v0.21.5; Nous Research has v0.22.0 (12 commits newer). Want to update? Open Settings › Updates › Agent
> and click Update — or tell me to open it for you.

**How you open it.** `it open settings updates`, or the chat link
[Settings › Updates](iclone://open/settings?tab=app-atualisation). Both only navigate.

**What you never do.** Run `hermes update` in any form that changes the install — not on your own, not when the user
asks you to ("update it" is answered with the pane, never a command); press *Update*, *Roll back* or
*Restore the verified version* (their confirm buttons refuse `it click`, and main refuses an apply without the human's
own gesture); change `config.yaml` or anything under `~/.hermes`; promise a date. A RED compatibility verdict is the
owner's hold in the pane, never yours. After an update, read the receipt card (from → to, backup zip, outcome) and
`scripts/verify.sh` if the user asks for proof.

## The short form of Track B

    git fetch upstream                               # app repo only, read for study
    bash scripts/adoption.sh                         # the backlog since CURSOR, top rows

**Never** count `HEAD..upstream/main`: our root commit is a parentless import,
so there is no common ancestor and that command counts upstream's whole history
(26354 on 2026-08-30, when the honest answer was 486). The scan reads
`CURSOR..upstream/main`; `iclone/UPSTREAM_BASE` is the fixed import origin.
The owner picks from the inbox; you re-implement each pick in our design on a
branch and record it — `references/curated-funnel.md`, `references/adoption.md`.

---

## The invariants — an update may NEVER change these

- Lowercase **iclone os** naming everywhere; bundle id `io.cloneframe.icloneos`.
- Theme trio `iclone-natural` / `iclone-dark` / `iclone-light` (default
  natural), champagne-on-ink tokens, the 1111 mosaic field.
- Home architecture and z-order: `.istage-layer` (z37, 3D stage — never
  unmounts) < chat window (z38/39, `--iwin-*` clip) < `.ihome` chrome (z40,
  pointer-events whitelist) < overlays (z50).
- The left Dock with macOS physics; the Message window with header tabs
  `message · iT`, the conversation-islands rail, and the iT multiplexer.
- The right iNFT island + frosted collection cards + iCLONE head mark.
- EconomyOS: per-iNFT Virtuals ACP wizard, one iNFT = one isolated
  `ACP_CONFIG_DIR`; `card issue` is NEVER automated.
- Settings: the group registry and our pane labels (message, iT, Setup, App
  Atualisation); About keeps the Nous Research attribution.
- Model-agnostic BYOK — no provider hardcoding; zero secrets in code, config
  committed nowhere, nothing secret in logs.
- Approvals stay on (never off/yolo); you never edit `~/.hermes/config.yaml`.

## Secrets

`~/.hermes/.env` and `~/.hermes/auth.json` hold live keys. Never read them,
never copy them into a backup of your own, never print them. `hermes update
--backup` already zips HERMES_HOME properly when a full restore is wanted —
use that rather than making a second copy of the owner's secrets.

## Failure discipline

A stage that fails stops the process — fix or roll back before moving on.
Abandoning a branch is always acceptable; a dirty half-done tree is not. If
verification finds ANY invariant broken, the change goes back to Re-implement.

Never report a stage green on the strength of an exit code: read the output.
Never report "done" on a runtime update without having launched the app and
sent one real turn — the automated checks stop at the backend's front door.

When in doubt at any gate, stop and ask the owner. An upstream release can
never damage the app — that is the contract.

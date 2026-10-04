---
name: bridge-sync
description: Use when updating, editing, deploying, or reconciling an app that exists in BOTH your local workspace and a VPS (e.g. MyApp) and a peer Claude Code runs on the VPS. HYBRID model — the two instances coordinate over Claude's built-in Remote Control (SendMessage), and code moves over git (preferred) or rsync. Before changing either side they exchange current state, discuss the diff, converge on the single best version, apply on both, and verify. Triggers on "update <app> on the VPS", "sync local and VPS", "deploy MyApp", "what's on the VPS", "reconcile the two copies".
---

# bridge-sync (hybrid)

Two Claude Code instances — `local` (laptop) and the VPS session — each hold a
copy of the same app. This skill stops them clobbering each other: **no edit
lands on either side until both have compared state and agreed on the best
version.** Coordination uses Claude's built-in Remote Control (`ListAgents` +
`SendMessage`) — no relay, no tunnel. Code moves over git (preferred) or rsync.

`bridge-state.sh` (in `scripts/`) prints a compact, comparable snapshot — use it
instead of hand-gathering state.

## Preconditions
1. `ListAgents` → find the VPS session (ask the user which if unclear). Confirm it
   is **online** (Remote Control sessions show `offline` when not connected). If
   offline, ask the user to connect it — don't reconcile blind. (Durable relay is
   the offline fallback; see claude-bridge README.)
2. Know the app dir on THIS host (ask once, e.g. local `~/dev/myapp`, VPS
   `~/apps/myapp`).

## Coordination is turn-based
`SendMessage` hands control to the peer; you resume when it replies. Always name
**who to reply to** (your `ListAgents` session name) in each message.

## Shared journal (MCP) — the source of truth
The `journal` MCP server (tools: `journal_read`, `journal_log`, `claim`, `release`,
`claims_list`) records what each side has done so neither acts on stale state.
`who` is your identity (`local` or `vps` — check via `ListAgents`/context).
- **Start of every turn:** `journal_read()` to see what the peer did.
- **Before editing a file or deploying:** `claim(who, resource)`. If it returns
  `ok:false`, the PEER holds it — coordinate over SendMessage, do NOT touch it.
- **After every meaningful action:** `journal_log(who, action, target, status)`
  (e.g. action=PUSH/DEPLOY/EDIT/VERIFY/DONE).
- **When finished with a resource:** `release(who, resource)`.
If the `journal` MCP isn't registered, fall back to announcing actions over
SendMessage — but prefer the journal; it survives restarts and enforces locks.

## The core rule
> **Read journal → claim → exchange state → discuss diff → agree → apply → verify → log/release.**
> Never skip "agree", even for a one-liner — the peer may hold changes you can't see.

## Workflow — INITIATOR (the side being edited, usually local)
1. **Announce + request state.** Snapshot yours: `scripts/bridge-state.sh <app>`.
   `SendMessage({to: "<vps-session>"})`:
   > "bridge-sync <app>: I intend <change>. Run `bridge-state.sh <your app path>`
   > and reply your snapshot. Don't edit yet. Reply to `<my-name>`."
2. (Turn ends.) On the VPS's snapshot, **diff & classify** vs yours:
   - `git.head` equal, both clean → in sync; apply your change, go to step 5.
   - equal but one side **dirty** → uncommitted work exists; surface whose/what.
   - `git.head` differ → diverged; find common ancestor from the commit lists.
   - no git → compare file hashes.
3. **Discuss to converge (the "best version" step).** `SendMessage` your reading +
   proposal; let the peer push back (hotfix to preserve? whose change wins per
   file?). Loop until you BOTH name the same target (a commit/branch or concrete
   file set). Get an explicit "agreed" — don't assume.
4. **Apply on your side** so your copy equals the agreed target; commit.
5. **Propagate the bytes** (git preferred): push agreed branch/sha; `SendMessage`
   the VPS: "pushed <sha>, `git pull` + test + restart, reply result." (No shared
   remote → send a `git diff` patch inline, or rsync via bridge-push.)
6. **Verify both sides** (tests, `--version`, health/restart); exchange results.
7. **Close:** both `SendMessage` "done, synced at <sha>, green." Report to user.

## Workflow — RESPONDER (VPS, re-invoked by an incoming message)
1. On a state request: `scripts/bridge-state.sh <your app>` → reply the snapshot.
   **Edit nothing yet.**
2. Be honest in the discussion: uncommitted changes or a running hotfix? SAY SO —
   that's exactly what this step exists to catch. Object BEFORE applying if the
   plan would lose your work.
3. On the agreed apply message: `git pull` (or apply patch), run verification,
   reply result, then "done" when green.

## Moving code (bytes, not chat)
1. **Shared git remote** — agree branch+sha; initiator pushes, peer pulls. Best.
2. **Patch over SendMessage** — small diffs only, text; peer `git apply`, then
   sha/test to confirm it applied clean.
3. **rsync/tar over SSH** — `bridge-push.sh` for large trees with no shared remote.
Never assume a local path is visible to the peer — separate hosts.

## Guardrails
- If state can't be compared (peer offline/silent past a reasonable wait,
  `STATE_ERROR`), STOP and tell the user. Don't one-sidedly deploy.
- If the VPS app is **running/serving**, treat its copy as production: converge
  toward not breaking it; restart only as an explicit agreed step.
- Keep messages tight and decision-oriented — reconciliation, not chat.

## Example (MyApp, local initiates, git transport)
```
local: bridge-state.sh ~/dev/myapp         # head=a1b9 clean
local → SendMessage(vps): "bridge-sync MyApp: adding rate-limit to /scan.
        Run bridge-state.sh ~/apps/myapp, reply snapshot, don't edit. Reply to local."
vps   → SendMessage(local): "head=a1b9, dirty: server.js (uncommitted CORS hotfix), service active."
local → SendMessage(vps): "commit + push that hotfix to origin/main; I'll rebase rate-limit on top. Agreed?"
vps   → "agreed, pushed a1b9→c3d0."
local: (rebase, add rate-limit, push c3d0→e5f1)
local → SendMessage(vps): "git pull origin main (e5f1); npm test; restart myapp; reply result."
vps   → "tests green, service active on e5f1."
both  → SendMessage: "done, MyApp synced at e5f1, green."
```

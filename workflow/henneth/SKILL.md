---
name: henneth
description: Use when the user runs /henneth. Boots (or reuses) one standing background web server, shared across all sessions, that serves a live gallery of rendered artifacts — wireframes, mockups, images, diagrams dropped into ~/.skadi/henneth/. The page lists every artifact newest-first and follows the latest in its main pane unless pinned. Drop a file and the open screen updates on its own; a row's delete button removes an artifact from the folder. Henneth Annûn — the Window of the Sunset, a window one looks through.
purpose: Serves a standing gallery window for rendered previews and artifacts.
user_invocable: true
stage: watch
---

# Henneth

A standing window onto the artifacts you render. One folder is watched — shared
across every session; anything dropped in — an image or an HTML mockup — appears in
the gallery, newest first. The open screen follows the latest unless you pin one to
study it. The page displays and may delete an artifact from the folder; it never
edits one.

## Workflow

### 1. Resolve the shared folder

Henneth runs one standing instance for all sessions, so the folder is fixed — no
session id, no drift. Every session resolves the **same** path:

    DIR="$HOME/.skadi/henneth"
    mkdir -p "$DIR"

`$DIR` is the one folder henneth serves **and** the one folder you render into (see
"Where renders go" below). It is shared across every session: whichever session
runs `/henneth` first boots the server, and all others reuse it.

### 2. Reuse a running server before booting a new one

Read `$DIR/.henneth-port` (one global lockfile, since the folder is shared). If it
names a port and that port answers a quick GET to
`http://localhost:<port>/index.json`, the one instance is already up — perhaps
booted by an earlier session — so print the URL and launch nothing.

### 3. Otherwise boot the server in the background

The port is fixed at **10001** (override with `HENNETH_PORT`) so the URL never
drifts across restarts. Launch the server detached so it outlives the turn (run
in the background):

    ~/.claude/hooks/mirror-server.py "$DIR" "${HENNETH_PORT:-10001}"

The server records its own port in `$DIR/.henneth-port` on boot. If the port is
already held by something other than a dead Henneth server, the bind fails and
the process exits at once — report that plainly rather than silently retrying
on a different port.

### 4. Surface the URL

Print `http://localhost:<port>/` inline. Tell the user plainly: drop any image or
HTML into the folder — or ask you to render one there — and the open screen follows
on its own. To hold a view while studying it, click **Pin**. To drop an artifact
from the folder, hover its row and click **&times;** — it asks once, then unlinks
the file and its sidecar. To clear several at once, click **Select**, tick the rows
(or **All**, or a group's own header box to tick that whole group), and
**Delete (n)** — one confirm, then all chosen are unlinked.

### 5. Where renders go

Every artifact you render for the screen must be written into `$DIR` — that exact
path is the binding henneth watches. Resolve it the same way each time
(`$HOME/.skadi/henneth`); render anywhere else and it will not appear on
the window. The path is fixed and shared, so any session writes to the one window
without remembering a path.

Every artifact's HTML must open with `<meta charset="utf-8">` as its first line.
The server declares no charset, so the browser falls back to a guessed encoding —
any preview carrying CJK, em dashes, or arrows renders as mojibake without it.

## Presenting code

When the artifact's purpose is to **present code** (a function, a file excerpt, a
change), render the code as a proper highlighted block — **never a hand-built
`<table>` of line numbers**. Henneth serves over a local HTTP server, so the browser
may pull **Prism.js from a CDN** (the same reason Mermaid-from-CDN works); it degrades
to a plain `<pre>` if the machine is offline.

Every code presentation carries three things:

1. **Syntax highlighting** — `class="language-<lang>"` (e.g. `language-typescript`) +
   the matching Prism components.
2. **Line numbers** — the line-numbers plugin, `class="line-numbers"` with
   `data-start="<N>"` so the gutter shows the **real file line numbers**, not 1.
3. **Change highlight** — the line-highlight plugin marks the lines a change touched:
   `data-line="<ranges>"` plus `data-line-offset="<data-start − 1>"` so the ranges are
   read as file line numbers. For a pure add/remove view, instead use a
   `class="language-diff diff-highlight"` block holding verbatim `git diff` text.

HTML-escape the code body (`&`→`&amp;`, `<`→`&lt;`) — Prism reads `textContent`.

Canonical template (full-function view with line numbers + change bands):

    <meta charset="utf-8">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/line-numbers/prism-line-numbers.min.css" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/line-highlight/prism-line-highlight.min.css" />
    ...
    <pre class="line-numbers" data-start="253" data-line-offset="252" data-line="260,267-278,287"><code class="language-typescript">…escaped code…</code></pre>
    ...
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-clike.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-javascript.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-typescript.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-diff.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/line-numbers/prism-line-numbers.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/line-highlight/prism-line-highlight.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/diff-highlight/prism-diff-highlight.min.js"></script>
    <script>window.addEventListener('load', () => window.Prism && Prism.highlightAll());</script>

A unified diff cannot carry a clean per-line gutter (its numbers live in the `@@`
header) — so to show **both** real line numbers and what changed, prefer the
full-source view with line-highlight bands over a `language-diff` block. Wear the
shared parchment chrome (`skadi-theme.css`) around the block as usual; Prism styles
only the `<pre>`.

## Artifact labels — optional sidecar

Beside an artifact `wireframe-login.html`, an optional `wireframe-login.json`:

    {"title": "Login wireframe", "note": "second pass, dark variant", "group": "nav-rail"}

All three fields optional. Absent a `title`, the gallery shows the humanized
filename; absent a `group`, the artifact falls into the **Ungrouped** bucket.

## Grouping — stamp the session's work

The folder is shared across every session, so renders from different sessions pile
into one list. The gallery groups them by the sidecar `group` field — collapsible
sections in the sidebar, the group bearing the newest artifact leading and
following active work.

The session-id fallback is **automatic**: a `PostToolUse` hook
(`hooks/henneth-group.py`, wired in `settings.json` under the `Write|Edit` group)
stamps every artifact rendered into the folder with the last 6 of the session id,
so renders from one session cluster without anyone remembering to stamp. The hook
never clobbers an explicit `group` — it only fills one that is absent.

So to give a group a **readable name** (`"nav-rail"`, `"carpo-drag"`) rather than
the bare id, write the sidecar `group` yourself when you render; the hook then
leaves it be. Re-stamping a sidecar with a different `group` moves the artifact. A
file dropped into the folder by hand (no `Write`/`Edit` tool call) bypasses the
hook and gathers under Ungrouped until given a sidecar.

## Notes

- **One instance, shared.** The folder is fixed at `~/.skadi/henneth`, so
  every session shares one folder, one port, one URL. The first session to run
  `/henneth` boots the server; the rest reuse it. Artifacts accrue across sessions
  — there is no per-session board.
- **Displays, deletes, never edits.** The page shows artifacts and can delete one
  from the folder (the row's **&times;**, after a confirm); it never edits their
  contents. You render or drop files in chat; the screen reflects them.
- **Reuse, don't multiply.** Re-running /henneth — in this session or any other —
  reuses the standing server via `.henneth-port` rather than spawning a second one.

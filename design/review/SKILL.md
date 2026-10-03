---
name: review
description: Visual Stack's primary tool. Build a UI wireframe and open it in an interactive review workspace where the user comments directly on the page, turning those comments into the next iteration — or point the same workspace at an app that is already running and review the real thing. Use when the user wants a wireframe, UI mockup, screen design or prototype built; wants to review, annotate, mark up or comment on a page, a design, an existing UI, a running app or a website; wants to iterate on a UI; asks to use Visual Stack; or invokes $vstack:review, /vstack:review, or the older /vstack:wireframe.
---

## 0 · Host (do this first)

This skill is **tool-agnostic**. The loop is defined in
`plugins/vstack/contracts/review-loop.md` and the ops you need in
`plugins/vstack/contracts/host.md`. **Never invent host-specific tool names in
this file** — they live only in the Host adapter.

| You are running under… | Load adapter | Set |
| --- | --- | --- |
| **Codex** | `skills/review/hosts/codex.md` | `VSTACK_HOST=codex` (or `--host codex` on `serve`) |
| **Grok** Build / Grok CLI | `skills/review/hosts/grok.md` | `VSTACK_HOST=grok` (or `--host grok` on `serve`) |
| **Claude Code** | `skills/review/hosts/claude.md` | `VSTACK_HOST=claude` (default if unset) |

Adapters live in the `hosts/` directory beside this SKILL.md. Do not read
`plugins/vstack/host-profiles/<id>.json` instead: that JSON is UI data with no
tool mapping.

**Read the adapter before §3.** Every `background`, `watch_stream`, `stop`,
`share`, and `browser_capture` step is fulfilled exactly as that file says.

A two-way review loop. The user comments on the screen; you apply the comments, ask about anything ambiguous, and publish the next version. Two things can go under it:

| | what it is | what you change |
|---|---|---|
| **A page** (§1–§3) | a wireframe you just generated, an exported screen, a prototype — any self-contained HTML file | the file |
| **A UI that exists** (§7) | an app on localhost, or a website on the internet: the real screens, real data, real states | the source code — or, for a site you don't own, a note about it |

```
requirements ──► page.html ──► review workspace ──► brief.md ─────┐
      ▲          or a live app  (user comments)                    │
      └──────── you apply it, reply, publish v(N+1) ◄──────────────┘
```

**One review is one subject.** A page review opens that file and nothing else — several screens means several files and several workspaces, not an invented project structure. A live review opens the whole app, because clicking through it is the point.

**Which one?** If the thing the user wants to talk about already runs, review it running (§7) — a wireframe of a screen that exists is a copy that drifts. Build a page when the screen does not exist yet, or when they want to change it without changing code.

## 1 · If you are generating the page

Skip to §3 if the file already exists.

Establish before building — ask only what you genuinely can't infer, in one message:

- **What screen**, and what the user is trying to do on it.
- **Which screen size leads** — the workspace offers ultrawide (2560), desktop (1440), tablet (834) and phone (390).
- **Visual reference** — a site to match, screenshots to match, or the project's design system (§2). If they name a site or hand you images, **capture it before building** (§2a).
- **States** — which loading / empty / error states matter enough to be shown.

Keep the first pass deliberately lean. The review loop is how it gets rich; a bloated v1 wastes the user's first review on deletions.

## 2 · Resolve the design source

In priority order — see `references/design-sources.md` for the detail:

1. **A reference site the user names** — capture it (§2a) rather than describing it from memory.
2. **Reference screenshots the user provides** — Read every one and derive the same, saying what you inferred.
3. **The project's design system** — a `design/` folder with `tokens.css` (+ often `design-guide.html`, `CLAUDE.md`). Use its tokens verbatim. **If it ships its own principles doc, read it and follow it — it outranks the defaults below.**
4. Nothing found → ask, don't invent silently.

### 2a · Building from an existing site

**A URL or a screenshot is a design source, not a description of one.** When the user
says "like Linear", "match our admin", or drops a screenshot in, don't work from an
impression of it — capture it, write down what you measured, and build against those
numbers.

With a **URL**, use Host op **`browser_capture`** when the adapter says it is
available; otherwise ask the user for screenshots and derive by eye (§2
screenshots path). The full procedure — screenshots per size,
`assets/harvest-reference.js`, writing `<page-dir>/<name>-reference.md` so every
later pass reads it instead of re-capturing, the never-sign-in rule — is
`references/design-sources.md` §1–2. Copying a *layout* is the point; logos,
wordmarks, photography and copy stay placeholders.

Default principles, unless the design source overrides them:

- **Start simple.** The minimum UI that serves the task.
- **Follow the patterns users already know** from established tools in the domain. Novelty needs a defensible reason.
- **Growing collections are datagrids** — search, sort, filters in the headers, pagination — not card walls.
- **Order by attention, place by belonging.** What the user needs first goes first; metrics last.
- **Realistic data.** Causally consistent, credible scale, real edge cases. Never a fake zero — undefined is an em dash.
- **No commentary**, **no dead controls.**

Requirements the workspace places on the file:

- **Self-contained** — tokens inline in `:root`, no external fonts, stylesheets or scripts. The same file has to work served over http *and* inlined into a share bundle.
- **A real `<title>`** — the review is named after it.
- **`min-height: 100vh`, never `height: 100vh` or `overflow: hidden` on `body`** — the page lays out at full height inside the workspace's window.

## 3 · Publish and serve

```bash
SKILL=<this skill dir>          # the directory containing this SKILL.md
FILE=wireframes/candidate-pipeline.html
# Prefer export VSTACK_HOST=<id> once; --host on serve is required for correct UI labels.

node "$SKILL/assets/review-server.mjs" publish --file "$FILE" --label "Initial version"
```

Start the server with Host op **`background`** (it must outlive the turn) — see
your adapter for the exact tool:

```bash
node "$SKILL/assets/review-server.mjs" serve --file "$FILE" --port 7788 --host "$VSTACK_HOST"
```

The server opens the workspace in the browser itself, as soon as it is up. Say
it is open and name the URL — **http://localhost:7788/** — so a machine that
could not open anything still has it, then arm the waiter (§5). Pass
`--no-open` when the user asked you not to take over their screen.

Reviewing a running app instead? Same server, `--app` in place of `--file` — see §7.

## 4 · What the user gets

The page opens in **its own browser window** on the canvas — own viewport, own scrollbar — so nothing about the workspace bleeds into the design being judged.

| | |
|---|---|
| **View / Annotate** | two modes, **esc** toggles. **View hides every annotation** so the page is judged as it really is; Annotate brings them back |
| **Click** | a comment pin at that spot |
| **Drag** | an area comment over that region — it carries the element that contains the box *and* everything named inside it |
| Either way | the note opens **on the canvas** where the mark is. A comment with nothing typed in it is discarded on dismiss |
| **Toolbar** (left of the canvas) | what Annotate draws with: Comment · Move · Delete, keys **c** · **m** · **d**. Picking one in View mode returns to Annotate with it |
| **Move** and **Delete** | both are optional-note: the mark is the instruction, and anything typed adds to it. Both outline whatever the pointer is over, so it is clear which element the gesture will take |
| **Move** | drag a thing to where it should go. Arrives as `kind: move` — the element to move, the element it was dropped on, and which side of it |
| **Delete** | drag across text to strike exactly those words, or click an element to strike everything written inside it. Arrives as `kind: strike` |
| **Target** | the note says which element the comment attached to |
| **Attached to an element** | a comment belongs to the thing it was made on, not to a coordinate. The mark rides it when the layout moves, and **goes off the page with it** — a comment made inside a modal, tab or step is not drawn while that thing is closed. It stays in the list tagged *not on screen*, and it still reaches you |
| Captions | stay hidden — a mark shows its note when it's open, or on hover in Annotate |
| **Screen size** | ultrawide · desktop · tablet · phone. A comment belongs to the size it was made at and only shows there |
| **Thread** | your replies appear on the comment itself and in the comment list, where they can be answered without going back to the mark. A question opens its thread on sight. A question that came with options shows them as buttons, one marked *Recommended*; pressing one answers with those words, and the box below still takes anything else |
| **Save** (⏎) | on the comment — Enter commits it, Shift+Enter is a new line |
| **Timeline** (bottom) | drag the handle to scrub through published versions; history is read-only |
| **EN / 中文** | workspace chrome only — comments stay in whatever words they were written in |
| **Delete** | on the comment, once it has words in it. It takes the comment off the user's list whatever state it is in, including one you are working on right now — you are not told, and you finish and close what you were given as normal |
| **Clear all** | in the comment list footer, behind a confirm. It takes the addressed comments off the list — the same act as the per-card delete. Comments still open stay unless the reviewer ticks the box on the confirm, which is off every time it is asked |
| **Link status** | a dot beside Send — linked to your session, or link lost. Nothing is said until the connection has actually answered |
| **Send to {agent}** (⌘⏎) | sends straight through — no preview step — and wakes you up. Label uses the Host profile name. Greys out until something actually changes |
| **In flight** | every comment you were sent keeps an indeterminate progress bar until you publish or reply. No banner covers the page any more — the progress is on the comments it belongs to |
| **Stalled** | after a minute with nothing listening, the strip stops claiming progress and says you have stalled. **Send again** puts those comments back in the queue, and the next session to pick up is handed them. Refused while your watcher is alive, because then you still have them |
| **Addressed** | comments you closed stay in the list in their own section, each offering **Revert** or **Refine** |
| **Publish a link to this wireframe** (the ▾ beside Send) | only when Host `capabilities.share` is `artifact`. Asks you to publish **the wireframe** (Host op `share`) and hand the URL back. Hidden on hosts without public share, and in a live review |
| **Approve & finish** (the ▾ beside Send) | sign-off. Ends the review, closes the server, and tells you the design is settled — behind a confirm that warns how many comments are being left unapplied |

There is no per-comment resolve button: **you** close comments out by addressing them. Approve is the
whole-page verdict, not an item-by-item one — one click that means *the design is done*, which is the
only way the review ends deliberately rather than by the tab closing. Comments arrive naming the
element they were made on and the region it sits in; the user never sees markup, and the selector that
comes with them is how the mark stays attached, not a promise about your HTML — **keep ids and
distinctive classes stable across versions** and open comments keep their grip.

**Addressed is your word for it, not the last word.** A comment you closed can come back:

- **Refine** reopens it as it stands — read the note and the thread again, it did not go far enough.
- **Revert** reopens it asking you to undo what you did there, and posts that as a reply in its thread.

Either way the comment returns in the next brief with `reopened: true` (and `wantsRevert: true` for a
revert), marked `· REVERT` in the markdown. Nothing else can un-address a comment — the server only
accepts a status going backwards when the reviewer deliberately sent it back.

## 5 · Catch the review, and hold up your end of the conversation

After starting the server, start the watcher with Host op **`watch_stream`**. Look up the tool for
that op in your adapter — `watch_stream` delivers each line of output to you as it arrives, and it
is a different op from the `background` you used in §3.

```bash
node "$SKILL/assets/review-server.mjs" watch --all --stream    # or --file <page.html>
```

Use the exact command your adapter's `watch_stream` entry gives, not the bare form above: it adds
`--session <your session id>` when your host has one, and that is what binds each delivery to you —
without it, the round you take cannot be told apart from another session's.

Each line of its output is one event, delivered to you as it happens, and the process keeps running,
so one watcher covers the whole session — `--all` takes in every review open in the project,
including ones opened later, and any you started from this directory whose page lives elsewhere.
It never takes over a review another session's watcher is already covering.
Run it from the same directory you started the server from; that is what ties the two together.

**It opens with a `HANDSHAKE` line naming a command. Run that command straight away.** The watcher
goes live once you answer, the workspace says **Linked**, and the round events start reaching you.
Answering proves the op was fulfilled, since only a session that can run commands can answer.
Answer within two minutes; after that the watcher prints `UNWIRED` and exits, and you start it again
with the tool your adapter names for `watch_stream`.

The page says **Linked** for as long as the watcher is answered,
and **Unlinked** in amber the rest of the time, so the reviewer always knows which one they have.

Each event is one line (full table: `contracts/review-loop.md`):

| | What it means | What you do |
|---|---|---|
| **`HANDSHAKE`** | the watcher asking whether you can hear it | run the command it prints, now — it is what brings the watcher live |
| **`LINKED`** | the handshake is answered and a review is under the watcher; the workspace says Linked | carry on — the loop is live |
| **`UNLINKED`** | the handshake is answered, but the watcher found no review to cover, so no workspace says Linked | start it again with `--file <page.html>` if a review is already running for a page outside this directory. A serve started here after it needs nothing |
| **`UNWIRED`** | the handshake went unanswered and the watcher exited | start it again with the tool your adapter names for `watch_stream` |
| **`REVIEW`** | comments have been handed to you; the line names how many are open and where the brief is | read the brief, then the steps below |
| **`SHARE`** | they want a link to send someone | Host op `share` if capable, then §6; if the Host cannot share publicly, say so and offer a file/bundle instead |
| **`APPROVED`** | the design is signed off; the server has closed itself | say it's approved, note any `openComments` deliberately left, and carry on with whatever comes next |
| **`CLOSED`** | that review's tab went away | the watcher drops it and keeps watching the rest; it only stops when none are left |

**Use the protocol commands rather than deleting state files.** `share --url` clears `share`, and
closing a comment is `publish --close`.

### What a delivery is

The watcher blocks until the reviewer has said something you have not been given, then hands you
**every open comment** — not only the new ones — marking which are new since last time. A comment you
do not close comes back on the next delivery, so nothing is lost by being missed.

While you work, **nothing will interrupt you.** New comments accumulate on the server and arrive with
the next delivery; a review in flight cannot be called off.

On a delivery:

1. **Read the brief** the `REVIEW` line names (`<store>/brief.md`). It carries every open comment with
   its element, place, screen size and thread.
2. **Apply every comment.** There are no priorities to sort by — if the reviewer wrote it down, it
   needs doing. Locate each from its **anchor** — the element and the region it sits in — at the screen
   size it was made at, using the coordinates only to break a tie.
3. **Ask instead of guessing.** If a comment is ambiguous, reply to it — the question appears on the
   mark and in the comment list, where the user answers it:
   ```bash
   node "$SKILL/assets/review-server.mjs" reply --file "$FILE" \
     --comment c7f2a1 --text "Every overdue row, or only the ones assigned to you?"
   ```
   The comment stays open and comes back with their answer attached. On disk the reply uses
   `by: "agent"` (legacy files may say `"claude"`; treat them the same).

   **When the answers are a short list, offer them.** `--option`, repeated, puts them on the
   comment as buttons, and `--recommend <n>` marks the one you would take. Pressing one answers
   with those words; the box to type something else stays, so an answer you did not think of is
   still one sentence away.
   ```bash
   node "$SKILL/assets/review-server.mjs" reply --file "$FILE" --comment c7f2a1 \
     --text "Every overdue row, or only the ones assigned to you?" \
     --option "Every overdue row" --option "Only mine" --recommend 2
   ```
   Two to four options, each a complete answer rather than a keyword. Ask an open question with
   `--text` alone when the answer is a sentence you cannot predict.
4. If a comment is genuinely wrong for the design, reply saying why rather than silently skipping it.
5. **Close what you did, and snapshot the version:**
   ```bash
   node "$SKILL/assets/review-server.mjs" publish --file "$FILE" \
     --close c1f3k2,c9dk1 --label "Filters collapsed, overdue sorts first" \
     --summary "Filters are collapsed behind a single control, and overdue rows sort first.
   I left the date column alone — say if you want it narrower too."
   ```
   Anything you do not name stays open and comes back. Publish tells you what it left open — close
   those or reply asking about them, because the delivery will not raise them again on its own.

   **`--label` names the version in one line. `--summary` is the account you would give in
   chat** — what you changed, what you decided, what you left. The workspace shows it on the
   banner when the round lands, so a reviewer who is not reading your terminal still gets it.
   Send the same words to both places rather than writing a thinner version for the page. One
   summary is kept, and it is the latest one: a publish without `--summary` clears it.
6. **Check you left nothing hanging**, before you finish your turn:
   ```bash
   node "$SKILL/assets/review-server.mjs" unanswered --all
   ```
   It exits 1 and names every comment you were handed and then said nothing about — neither closed
   nor replied to. Those are the ones nothing will remind you of again, because the next delivery
   only comes when the reviewer writes. Add `--session <your session id>` if your adapter names one,
   so the answer covers your deliveries and not another session's. On Claude Code a Stop hook runs
   this for you, with your session id, and holds your turn open until it is clean.
7. Leave **`watch_stream` running** and say what changed in a few lines. Then wait — don't ask "shall I
   continue?", the loop is the point. (Only re-arm if you used one-shot `watch` without `--stream`.)

**Closing the browser tab closes the review.** The workspace holds an SSE
connection; when the last one goes and none returns within the grace period
(`--idle-timeout`, default 90s — long enough that a reload reconnects), the
server removes `url` and exits. That exit re-invokes you and ends the waiter.
`--idle-timeout 0` keeps it up until you **`stop`** the background process (adapter).
Either way, **say when the review is closed** — the user should never have to guess whether
a socket is still open.

The workspace never swaps the page out from under the reviewer: while you work, each comment you were
handed carries its own progress bar, and on publish the page offers a green line saying the round is
done, with **Refresh** beside it and your `--summary` under it, behind a chevron that opens and
closes and stays however the reviewer last left it.

## 6 · Publish the wireframe as a shareable link

Skip this section when Host `capabilities.share` is not `artifact`, or when the
review is live — the UI hides the control in both cases, and there is no public
URL backend. Offer a file path or
`bundle-artifact.mjs` instead (adapter may say more).

**What gets shared is the wireframe** — the design itself, opening full-bleed the way the
user will meet it. Not the review workspace: someone you send a link to is looking at the
screen, not at your comment threads.

Do this when the reviewer asks in chat, or when the waiter returns **`SHARE`** — they
pressed *Publish a link to this wireframe* under the ▾ and the menu is showing a spinner until the
URL arrives.

Publish **`$FILE` itself** with Host op **`share`** (adapter names the tool), then hand the URL back
so it appears in the workspace.

**In a live review** there is no `$FILE` — publish the capture the workspace just took,
`<store>/versions/v<n>.html` for the current round, and say plainly that the link is a
still of one screen, not the app. **Take `<store>` from `status`** (it reports `store`), never by
building the path yourself: a review opened before this tool was renamed still lives under the
directory it was created in.

```bash
node "$SKILL/assets/review-server.mjs" share --file "$FILE" --url "<public-url>"
```

- **Publish straight after a `publish`**, so the file on disk is the version you're
  claiming to have shared. `$FILE` is the live working copy — mid-review it can be ahead of
  the last published version.
- The page is already self-contained (§2).
- The link is tagged with the version it came from. After a later round the menu offers
  *Republish* rather than a stale link — **redeploy from the same file path** so the URL
  stays put and anyone holding it sees the new version.
- Delete the `share` sentinel once you've handed the URL back; `share --url` does it for
  you. Sharing does not end the review, and the watcher is still running.

**If they want to comment remotely**, that's a different package and an explicit ask.
`bundle-artifact.mjs` flattens the whole workspace — page, last 3 versions, and the
commenting UI — into one file; comments persist in
`localStorage` and **Send** becomes **Copy for {agent}**, since there's no session at the
other end:

```bash
node "$SKILL/assets/bundle-artifact.mjs" --file "$FILE" --out review.html
```

## 7 · Reviewing a UI that already exists

Point the same workspace at a running app and everything above still holds — the
modes, the marks, the threads, the timeline, Approve. Three things differ,
and they all follow from the same fact: **what is under review is code, not a
file you own.**

```bash
node "$SKILL/assets/review-server.mjs" serve \
  --app http://localhost:5173 --name lora-ui --port 7788    # a dev server
node "$SKILL/assets/review-server.mjs" serve \
  --app https://example.com --name marketing --port 7788    # a site on the internet
```

The server reverse-proxies the app, so the workspace and the app share an origin
— which is the only reason a comment can attach to an element rather than to a
coordinate. The workspace moves to **http://localhost:7788/__review/**; every
other path belongs to the app. Sockets are proxied too, so hot reload keeps
working. Start it with Host op **`background`**, tell the user the
`/__review/` URL, and arm **`watch_stream`** (§5) against `.vstack/local/review/<name>/` in the
directory you ran it from — **run every later command from that same directory**,
or pass `--store`. Pass `--host` / `VSTACK_HOST` the same as a file review.

**Get the app running first** when it's yours to run. If it isn't up, the canvas
says so instead of showing a screen: start the dev server yourself (`background`),
or ask which command does it. `--start /workflows` opens on a screen other
than the front door. A public site needs none of that — point at it and go.

### What changes

- **Every comment carries the route it was made on.** Marks are drawn only on
  that screen; elsewhere the comment sits in the list tagged *another screen*,
  with the route under it, and clicking it takes the frame there. The reviewer
  clicks through the app to reach a screen, or types a path in the address bar.
  So a review can span the whole flow in one pass — the brief comes back grouped
  by screen size, each comment naming its **Route**.
- **A version is a marker, not a file.** `publish --name <slug> --label "…"
  --close …` records what you finished; there is no snapshot of a
  file because the app is the truth. The timeline still scrubs: the workspace
  captures the DOM of the screen they were commenting on each time they send, so
  history shows what they were looking at when they said it.
- **You change source, not markup.** Go from a comment to the code through its
  anchor: the element's `id`, its distinctive classes, and above all the words on
  it — `text` and `label` are usually a literal string in the component. Search
  for those first, then confirm with the route. Say which files you changed when
  you reply.

If the app hot-reloads, the reviewer watches your change land. That is an
argument for landing whole changes rather than halves, not for working slower —
and the delivery loop (§5) still matters, because a review of a live app can be stopped
mid-flight just as easily.

### A public website works too

Same command, a real URL:

```bash
node "$SKILL/assets/review-server.mjs" serve --app https://example.com --name marketing --port 7788
```

A site published on the internet writes its own origin into its markup, so the
proxy rewrites text responses to point back through itself — otherwise the first
link the reviewer clicks takes the frame off the proxy, cross-origin, and every
comment silently stops working. It also strips HSTS, drops the `Domain` off
cookies so a session survives on localhost, decompresses what it has to rewrite,
sends the site its own `Origin` and `Referer`, and refuses service-worker
registration so a site cannot take over the origin the workspace lives on.

What that buys: a whole marketing site, a competitor's flow, a production app —
clicked through and commented on screen by screen, with each comment naming its
route.

- **Check the front door first.** If the target redirects to another origin (the
  `www` host is the usual one), the server says so on start and names the URL to
  use instead. Review the origin they actually land on.
- **A comment on someone else's site is a note about a design, not a licence to
  copy it.** Layout and interaction patterns are fair to learn from; logos,
  wordmarks, photography and copy are not — they stay placeholders in anything
  you build from it (§2a).
- **Off-site links leave the review.** The workspace says *off-site* in the
  address bar and offers Back. Nothing on another origin can be read or
  annotated — that is the browser's rule, not a gap.

### What it cannot do

- **Bot protection and CAPTCHAs stand.** Cloudflare-style interstitials, rate
  limits and bot checks apply to the proxy like any other client, and are not to
  be worked around. If a site refuses to load, say so and stop.
- **A login wall needs the user.** Never enter credentials. Ask them to sign in
  themselves in the workspace's window — the session lives on the proxy's origin,
  so they log in there once even if they are already logged in elsewhere — then
  carry on.
- **Strict CSRF or origin checks can still refuse a POST**, and an API on a third
  origin that only allows the site's own will refuse the browser. Reads are
  reliable; writes on a hardened site may not be.
- **A live review has nothing to publish.** *Publish a link* is not offered: what
  is under the marks is an app running on this machine, not a design that can be
  sent. If they ask for one, say that, and offer a screenshot (Host op
  `browser_capture`) instead.

## Notes

- **Never edit `assets/workspace.html`, `review-server.mjs` or `bundle-artifact.mjs`** to fit a project — they're the engine; only the page under review is yours. The shell chrome is stamped in from `lib/shell/` — see `lib/shell/README.md`. (`harvest-reference.js` is meant to be pasted and run, not edited.)
- State lives in `<dir>/.vstack/local/review/<name>/` beside the file — versions, reviews, threads, and the sentinels. The page itself stays clean. A live review has nothing to sit beside, so it lands in `.vstack/local/review/<name>/` under the directory you started it from.
- **Every vstack tool writes under `.vstack/local/<tool>/`**, so a project grows one dot-directory, not one per engine. `lib/workdir.mjs` resolves it — use that rather than joining the path by hand. One gitignore line covers the lot (`**/.vstack/local/`); the rest of `.vstack/` is the pipeline and belongs in the repo.
- The server binds to `127.0.0.1` only. Port 7788 busy usually means a review server is already running — pass `--port`.
- `node "$SKILL/assets/review-server.mjs" status --file "$FILE"` prints the current version, whether a review is waiting, and any sign-off / share request outstanding.
- **Every command takes `--name <slug>` in place of `--file` for a live review** — `publish`, `reply`, `share`, `status`, `watch`. The brief tells you which name to use.
- Full command reference and troubleshooting: `references/workflow.md`.
- Contracts: `plugins/vstack/contracts/` — Host ops and review-loop protocol.
- Host adapters: `skills/review/hosts/claude.md`, `skills/review/hosts/codex.md`, `skills/review/hosts/grok.md`.

## State & handoff

**No `.vstack/pipeline.json`?** You're standalone, and that is a first-class way to run this — a URL
or a sentence is enough. Everything above still applies; skip this section. **Never create the state
file here** — a half-written one is worse than none, because the next stage would trust it. Nothing
currently shipped brings a pipeline into being: the tool that did, `start`, is parked in
`plugins/vstack/experimental/`. **Standalone is the normal case.**

Standalone, the design source is §2's priority order (reference site → screenshots → the project's
own system → ask), the page goes where the user wants (default `wireframes/`), and you end with the
result. Do not propose another Visual Stack tool; wireframing is the complete product workflow.

With a state file:

- **Read** `artifacts.product` — `specs/product.md` is the constitution, and a wireframe that
  contradicts it is wrong however good it looks. Read `artifacts.requirements` if it is there. In a
  repo from the template, `design/tokens.css` and `design/CLAUDE.md` **are** the design source and
  outrank §2's order — you are drawing inside a system that already exists.
- **Write** the page to `design/<feature>.html` — the template's convention, and where the later
  stages look. Then `artifacts.wireframes[]`: append for a new feature, replace in place for one
  already there, matching on feature and never on array position. Set `stage: "wireframe"` and add a
  `history` entry. If the template's `design/README.md` inventory exists, fill the feature's row.
- **Write it on sign-off, not on every publish.** A design still under review is not an artifact;
  recording it as one puts versions in the state file that nobody agreed to. Approve is the moment.
- **A live review produces no wireframe artifact.** What it changes is the code, which the repo already
  records — so do not append to `artifacts.wireframes[]` for one. Say what you changed and leave the
  pipeline alone; the design stage is about designs that do not exist yet.
- On sign-off, report the approved wireframe and end the workflow. Do not hand off to another Visual
  Stack tool unless the user explicitly asks for one by name.

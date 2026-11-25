---
name: tracked-deck-links
description: "Self-hosted tracked deck links, a DocSend-style replacement on the user's own server. Sets up a small Node + SQLite tracker, publishes a pitch deck (HTML, or PDF converted to HTML) behind a shell-only page so link unfurls count as previews and not opens, mints one personal link per recipient, revokes links, and reads the dashboard back in plain words: per recipient status (preview, opened, read), active time, slides seen, time per slide, visits and devices. Use when asked to track who opened a deck, send a pitch or investor deck with personal links, replace DocSend, see which slides an investor read, or set up deck analytics."
metadata:
  author: Falco Schneider
  version: 1.0.0
---

# Tracked Deck Links

One personal link per recipient. You see who opened the deck, on which devices, for how long, and
which slides they spent time on. It runs on the user's own Node host. No third-party analytics.

## How it counts (read this before you report anything)

| State | What happened | How it is detected |
|---|---|---|
| **preview only** | Someone or something fetched the link: a WhatsApp, Slack or iMessage unfurl, a mail scanner | The server returns an empty shell. It has no deck text, so an unfurl shows only a generic title |
| **opened** | The deck loaded in a real browser | The shell's JavaScript asked `/api/open` for a signed deck URL. Only a browser running JS does this |
| **read** | Opened, with real input (tap, scroll, key, mouse) and at least 10 active seconds | Heartbeats from inside the deck |

- **Active time** only counts when the tab is visible, the window has focus, and there was input or a
  slide change in the last 60 seconds. It is counted per slide and in total.
- **Visits** are browser tabs. A reload in the same tab counts as a page load, not a new visit.
- **Devices** come from a random id stored in the browser. A new browser or device gets a new id.

What you may and may not say to the user:

- Say "**opened on a second device**". **Never say "forwarded"**. A second device can be the same person
  moving from phone to laptop. Leave the inference to the user.
- A preview is **not** an open. Do not say "they looked at it" when the status is `preview only`.
- Active seconds are a lower bound on attention, not proof the person read every word.
- Report the numbers as they are. Never round up, estimate or fill in data you do not have.

## Requirements

- Node **22.13 or later**. It uses the built-in `node:sqlite`, so there is no `npm install`.
- PDF decks only: `pdftoppm` from poppler (`apt install poppler-utils` or `brew install poppler`).
- A host the recipients can reach for real use: a VPS or any machine running Node. Locally it runs on
  `localhost` for testing.

Set two variables in every shell you use. Every command below assumes them:

```bash
export SKILL="/path/to/tracked-deck-links"      # this folder
export DECKLINKS_HOME="$HOME/decklinks-data"    # state: config, admin password, database, decks
```

## 1. Set up the tracker

```bash
node "$SKILL/scripts/decklinks.mjs" doctor --port 8787    # checks Node, SQLite, port, pdftoppm
node "$SKILL/scripts/decklinks.mjs" init --port 8787 --public-origin http://localhost:8787
```

- If `doctor` says the port is in use, pick another port and use it in both commands. Never stop
  something you did not start.
- `--public-origin` is the address recipients will use, for example `https://decks.example.com`.
  Printed links are built from it. If the tracker sits under a path on an existing site, add
  `--prefix /deck`. Running `init` again changes settings and keeps the password.
- `init` writes `$DECKLINKS_HOME/admin-password` (mode 600). It is never printed. Do not echo it, log it
  or paste it into chat. To open the dashboard, the user reads the file themselves.

Start the server. For a local run or a test, run it in the background:

```bash
node "$SKILL/scripts/decklinks.mjs" start      # detaches, writes $DECKLINKS_HOME/server.pid, waits for /healthz
node "$SKILL/scripts/decklinks.mjs" status     # up / DOWN
node "$SKILL/scripts/decklinks.mjs" stop       # when the user is done testing
```

For real use, run it as a service behind HTTPS so it survives reboots. See `references/hosting.md` for
a systemd unit and nginx/Caddy snippets. Recipients must get `https://` links.

## 2. Publish the deck

```bash
node "$SKILL/scripts/decklinks.mjs" publish ./deck.html            # one self-contained HTML file
node "$SKILL/scripts/decklinks.mjs" publish ./deck-folder          # folder with index.html + assets
node "$SKILL/scripts/decklinks.mjs" publish ./deck.pdf             # PDF: one image per page, one slide per page
```

- The default deck name is `deck`. Use `--deck NAME` to keep several decks, for example `--deck seed`
  and `--deck dataroom-memo`. Each link points at one deck name.
- Each publish creates a new version and switches the deck to it. Every existing link for that deck
  shows the new version on its next open, and old versions stay on disk. Use `--version v2` to name one.
- Slides are detected automatically. Reveal.js decks use Reveal's own slide events. Any other HTML deck
  uses `[data-slide]`, `section.slide`, `.slide` or top-level `<section>` elements, and the one most
  visible on screen is the current slide. Titles come from `data-title` or the first `h1`/`h2`/`h3`.
  With no slide markup, the whole page counts as one slide. If `publish` prints that note and the user
  wants per-slide stats, wrap each slide in `<section>`.
- Asset paths must be relative (`img/logo.png`, not `/img/logo.png`). `publish` warns about absolute ones.
- The deck is only reachable through a personal link. Its files need a signed key that only `/api/open`
  issues, and the key lasts 6 hours.

## 3. Mint and revoke links

```bash
node "$SKILL/scripts/decklinks.mjs" mint "Jane Doe, Fund X" --note "met at demo day"     # deck "deck"
node "$SKILL/scripts/decklinks.mjs" mint "John Roe" --deck seed
node "$SKILL/scripts/decklinks.mjs" links                                                  # list all
node "$SKILL/scripts/decklinks.mjs" revoke <token-or-url>                                  # 404 from now on
node "$SKILL/scripts/decklinks.mjs" unrevoke <token-or-url>
```

- **Never open, `curl` or fetch a recipient's link to "check it works".** Every fetch is logged
  against that recipient, as a preview or an open. To check the server, use `status` or `/healthz`.
  To try the flow end to end, mint a link named "Test", use it, then `revoke` it.
- Mint **one link per recipient**. Never share one link between two people, or the devices and visits
  get mixed.
- `mint` prints `Name -> URL`. Give the user the URL to send.
- Revoking stops the link at once. A browser that already holds a signed key can keep reading its
  open tab for up to 6 hours.
- **Your own clicks.** Opening a link in a browser where the dashboard (`<origin>/admin`) was unlocked
  counts as "you" and is left out of the stats. Opening it anywhere else counts as a recipient. To test
  a link, unlock the dashboard in that browser first, or use a throwaway test link and revoke it.
  The CLI does not mark anything as yours.

## 4. Read the dashboard back

```bash
node "$SKILL/scripts/decklinks.mjs" report                 # every link, in plain words
node "$SKILL/scripts/decklinks.mjs" report "jane"          # one recipient (name substring or token)
node "$SKILL/scripts/decklinks.mjs" report --json          # raw numbers, if you need to compute something
```

The report gives, per recipient:

- status
- first opened and last seen times
- active time and number of visits
- slides seen out of total
- device count with labels (for example `Phone · iOS · Safari`)
- link previews, which are not counted as opens
- a per-slide table of active time and visits, with unseen slides marked `not seen`
- one line per visit

Turn it into a short answer for the user. Lead with what matters for their next step. For example:

> Jane Doe **read** the deck: 46 s active over 2 visits, all 6 slides. They spent the most time on
> Traction (11 s) and Problem (10 s). It was **opened on a second device** (phone, then desktop).
> The WhatsApp preview was not counted as an open.
> John Roe has a **preview only**: the link was unfurled, and the deck was never opened.

Rules for the summary:

- Use the status words exactly: preview only, opened, read, not opened, revoked.
- Name devices by label. Say "opened on a second device" when there are 2 or more. **Never say "forwarded".**
- Name the 1–3 slides with the most time, and any slides never seen if the user cares about them, such as the Ask.
- When the data is thin (one visit, a few seconds), say so. Do not read intent into it.
- Times in the report are in the server's local time zone, and the report labels the zone.

The browser dashboard at `<public-origin>[/prefix]/admin` shows the same data. It is unlocked with the
admin password, and it can also create, copy and revoke links. Optional push notifications: run `init`
with `--ntfy-topic <topic>` and the server sends an [ntfy](https://ntfy.sh) push on every open and a
summary when a visit ends. Push titles name the deck by its own title (the `<title>` of the published
HTML, or the PDF's file name), for example "Jane Doe opened Northwind Robotics, seed deck".

## Limits to tell the user about

- Screenshots and photos of the screen cannot be prevented, and no tracker can.
- A recipient with JavaScript disabled cannot open the deck. They see a one-line notice.
- IP addresses are stored per visit for the owner's eyes. If the tracker is exposed without a reverse
  proxy, the `X-Real-IP` header can be faked. Bind to `127.0.0.1` behind nginx or Caddy (the default).
- The database is `$DECKLINKS_HOME/tracker.db` (SQLite). Back it up with the rest of `$DECKLINKS_HOME`.
  The same folder holds the admin password and the URL-signing key, so never commit it or share it.

## Alternative stack: Vercel + Supabase

Falco Schneider's original runs as a Next.js app on Vercel with Supabase for the database and file
storage. It uses the same three states and the same shell-only page. If the user already runs that
stack and wants no server of their own, read `references/supabase-vercel.md`. It covers the
architecture, the schema, the environment variables and the deployment steps. The Node + SQLite
version in this folder is the default because it needs one process and no accounts.

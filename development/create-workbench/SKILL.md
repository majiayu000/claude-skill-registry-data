---
name: create-workbench
description: "Use when a page is wanted to work on something with the person during development, fed the project's real data (comparing model answers, walking an agent call by call, measuring an output against its template), when such a workbench has to change, be reworked or its feed broke, or mid-session when turns went into aligning with the person on how to do a kind of work that recurs and real project data could show it. Produces the page in aiview, kind `workbench`, and the project's `workbench-<bench>` skill with its feed and operating steps. Not for designing a product screen (design-prototype) or verifying user stories (verification-skill-create)."
---

# Create a workbench

**Some work is done with the person in the loop, and time goes into aligning on how to do
it.** That alignment is kept as a skill, so the next session does not explain it all again;
a workbench keeps it with a dev tool beside it, fed the project's real data. It is made at
the start of the work or mid-session.

**Mid-session, propose it in one line, at a pause**, when three things hold: the session
spent turns aligning on how to do a kind of work, that work recurs, and real project data
could show it. Build only on a yes; one no ends it for that work in the session.

**A workbench is a dev tool for iterating on an idea, and it has two users**: the person, who
needs a clear UI that opens on what is being tried now, and the agent, who needs the bench
cheap to read, change and check. It is judged by the time from "what if…" to the result seen.

**Two things are produced, and a later agent works the bench from them alone**: the page,
in the data home like every document, and the project's `workbench-<bench>` skill, which
holds the feed that fills the page and the steps to operate it.

**The bench's skill makes the agent operating it the bench's owner**, by its role: that agent
keeps the page, the feed and the scripts true, fast and easy to drive, adapting them in place
when the project moves on. No other skill maintains them.

**The person is in the build.** Every change is shown in the watched browser before the
next question, as the `design-prototype` skill paces a prototype. A bench described in chat
was not seen.

## Before building

- **A `workbench-<bench>` skill's scope covers this question** in the project's local
  skill folder: read it and its page, and add the question to both as a view or a mode.
  Never a second bench for one scope: one bench per question and the project's local
  skills grow with every plan.
- **Read the sources before asking**: the files the project produces that the bench will
  show (recordings, calls as sent, fixtures, templates), where they live, their exact
  shape, and the code that writes them.
- **The watched browser**: a headed browser the person sees and the agent drives, a
  Playwright MCP over DevTools or a script over CDP. The project's own when it has one,
  named in its local skills. None: start Playwright's Chromium headed with
  `--remote-debugging-port=9222`, say so, and stop it at the end.

## Define, through the `interview` skill

Each answer is written into the bench skill's head as it lands.

1. **The bench's scope**: a kind of work on a part of the product (any model call, any
   agent walk, one family of screens), as wide as its sources allow, and the bench's
   label. The question at hand is its first view.
2. **The sources**, each file or call, as the project produces it.
3. **The feed's kind.** *Derived*: the runs are rebuilt from the sources on every feed.
   *Log*: entries are appended and never rewritten, for data the project cannot produce
   again (a call as sent during a walk). The sidecar is then the only record.
4. **What the person does on it**: compare, judge, pick, measure. The controls follow.
5. **Whether operating it takes steps**: start the stack, hold a call, reset state,
   record an answer. Each becomes a script.

## Build, live

1. **The page**: `node scripts/page.mjs <path> --label "<label>"`, at the path the `aiview`
   skill gives for `YYYY-MM-DD-<bench>.workbench.html`. Register it through the `aiview`
   skill: kind `workbench`, tags the bench and `trace` for a walk, group the
   piece of work it serves. Open it in the watched browser. The page carries Basecoat,
   `jsonTree` and the loader, `bench`; the bench's code goes between its
   `<!-- bench-code -->` markers, put on by the bench's `code.mjs`. A bench that makes one
   page per run (a walk, a session) keeps the page's code in its skill instead, and each
   run's page has its own sidecar: its feed's `init` makes each run's page, and its `refresh`
   puts changed code onto every page as `page.mjs --replace` does, the code block replaced,
   the sidecar untouched.
2. **The feed**: copy `scripts/data-folder.mjs` into the bench skill's `scripts/` and write
   `feed.mjs` over it. It writes the sidecar, the folder `YYYY-MM-DD-<bench>.workbench/`
   beside the page. A derived feed calls `writeDerived` and takes `--watch`. A log feed, new
   ones included, takes verbs that call `appendEntry` and `annotate`. Run it: the page updates
   in place. Before writing the feed or a view, read `references/sidecar.md`.
3. **Then one change at a time**: write it, read the screenshot, show the person, ask the
   next question.

## The page

- **The bench bar opens on the label.** It is the one standard part. The rest of the bar
  and the page carry whatever the bench needs.
- **Controls are Basecoat**, shadcn's design system in plain HTML, inlined by `page.mjs`:
  `class="btn" data-variant="outline" data-size="sm"`, `card`, `tabs`, `badge`, `input`,
  `select`. Basecoat carries no Tailwind utilities, so layout is the page's own CSS.
  `page.mjs` sets Basecoat's variables to aiview's identity, so the bench reads as part of
  the viewer: the bench's CSS colours through those variables (`--primary`, `--muted`,
  `--border`, `--ok`, `--warn`, `--danger`), never a colour of its own beyond data hues. The
  product the bench shows (a document, a screen, a card) is drawn in the project's design
  language, from the `design-prototype` skill's reference when there is one.
- **JSON is always shown through `jsonTree`**, the reader `page.mjs` inlines, with its toolbar
  (Fold all, Unfold all, Unfold n levels with 2 by default, Copy): never a `<pre>` dump or a reader of the
  bench's own. When the bench shows any JSON, read `references/json-data.md`.
- **The page opens on the current question**, and each thing is shown once: a view that repeats
  another, or that nobody looks at any more, is removed with its code and its feed fields.
- **The data is the project's, as it is.** Copied byte for byte, never renamed, reshaped
  or summarised: the page adapts to the shape, so the bench stays as close to the real
  run as it can. A rendering that interprets the data is what the app already shows.
- **Only the feed writes the sidecar.** The agent edits the page's code, never its data.
- **No CDN; data only by relative fetch into the sidecar through aiview's bridge.**

## The data standards

One set every bench follows; the API and the thresholds are `references/sidecar.md`'s.

- **The loader is the only reader.** A view reads through `bench`, never its own fetch.
- **Views load what they need, on demand**: the manifest and one run at open, a side file
  only when the view that needs it opens. The feed computes nothing a view can read.
- **Every view is async**: drawn through `bench.view`, which sets `data-ready` when drawn and
  renders the path and status on a fetch error.
- **Never a blank**: a run being loaded shows `loading <run>`.
- **Large data folds**: a long text folded with its size and a show button, a large run one
  view at a time.
- **Files are cached by name** in page memory, never fetched twice.
- **The person's place is kept** (tab, run, view, controls) through `bench.state`.

## Ergonomic for the agent

- **The scripts that drive the bench are built with it**, each with the view or control
  that needs it: open a view, set its controls, screenshot it, read back what it shows as
  text. An agent drives the bench through them, never with hand-written browser calls.
- **The loop is one command**, named in the bench skill's Iterating section: feed, reload,
  screenshot. An agent never rebuilds it.
- **The scripts are one CLI with verbs, terse by default.** Each verb prints a short plain
  summary (counts, what changed, what failed); the full output only with `--full`, machine
  output with `--json`. The agent reads summaries and diffs, never the raw files the bench
  shows (a prompt, a reply, a recording): a result is checked without filling the context.
- **Anything can go to the person's phone in one command, without passing through the
  agent's context.** A `shot` verb with `--mobile` takes a phone-width PNG of any view, with one item
  opened if asked, and prints only its path. `--md` on the reading verbs also writes the
  output as a short markdown file laid out for a phone: lists, not wide tables. The agent
  sends the file it names (the harness's send-file tool) and reads neither.
- **The bench's code is read by its marker**, never the whole page: Basecoat and the
  JSON reader are inlined above it and cost tokens for nothing.
- **The feed writes only what a view shows.**
- **`check.mjs` and `shot.mjs` load the page at its aiview URL, never `file://`**, wait on
  `data-ready`, and fail on `data-error`.

## Reworking an existing bench

A bench whose data sits in the page (made before the sidecar, fed through
`scripts/data-block.mjs`) opens and feeds as it did; no mechanism upgrades it. When it is next
worked on, it is reworked to this shape: page made fresh by `page.mjs --replace` at the same
path, code put back by `code.mjs`, sidecar filled by the feed. Read `references/sidecar.md`
first; its last section is the order.

## The bench's skill

**`workbench-<bench>/SKILL.md` in the folder the project already uses for local skills**,
`.claude/skills/` when it has none, with every deterministic step a script in its
`scripts/`. Written to the shape in `bench-skill.md`, read before its first line: the
sentences outside its brackets are carried as written.

## Prove it

Run the feed from a clean shell, see the page reload with real data in the watched
browser, and walk once, with the person, what they do on it. A bench whose feed has not
run is not handed over.

## Handoff

The page's URL, the skill's path, the sources and the feed's kind, what was walked.

## Red flags

| Thought | Reality |
|---|---|
| "I'll map the data to a cleaner shape for the page" | The page adapts to the project's shape. A translation hides what the app really produced, and drifts from it unseen. |
| "Quicker to paste the data into the page" | Only the feed writes the sidecar. A pasted copy is stale on the next run and nothing says so. |
| "I'll keep the old view in case" | A dropped idea leaves with its view, its code and its feed fields, in the same change. A bench that only grows is slow for both users. |
| "This JSON is small, a `<pre>` will do" | Every JSON goes through `jsonTree`, with its toolbar. One reader, read the same way everywhere. |
| "The feed can sit next to the page in the data home" | It reads the project, so it lives in the project's skill. In the data home it breaks without anyone seeing. |

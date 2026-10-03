---
name: session-review
description: >
  Turn a pile of session recordings into a short list of findings a colleague can verify in two
  minutes — instead of a pile of anecdotes. Question-scoped triage → watch the survivors →
  triangulate against events, database and source → grade every claim MEASURED / RECONSTRUCTED /
  OBSERVED / INFERRED. Works on a local replay folder, PostHog, Microsoft Clarity, Hotjar,
  Smartlook or Yandex Webvisor — and on a claim with no recordings at all. Use when asked to
  "watch recordings", "review session replays", "why did users drop off", "check dead clicks",
  "verify the fix", "what are users actually doing", or to grade findings someone already wrote.
---

# Session review

**A replay is the most persuasive evidence you will ever bring to a meeting, and the easiest to be
confidently wrong with.** This skill is the discipline that makes the difference: what leaves the
room is a claim with a grade and coordinates, or it does not leave the room.

---

## The grade ladder — use these four words exactly, everywhere

| grade | means |
|---|---|
| **MEASURED** | a query, the database, or the source code says so |
| **RECONSTRUCTED** | rebuilt from the recording's event stream or DOM by a tool — stronger than a click timeline, but **nobody watched it** |
| **OBSERVED** | **a human being watched the replay play.** State the n |
| **INFERRED** | motive or intent. Never evidence. Always labelled |

> 🔴 **Never write "watched", "on tape" or "I saw" for tool output.** The gap between RECONSTRUCTED
> and OBSERVED is where confident wrong findings are born, and it is invisible in the prose.

### 🔴 If you are an agent: you may not award yourself `OBSERVED`. Ever.

**`OBSERVED` is a grade a person awards after watching.** It is the one row on the board that says a
human eye was on the pixels. An agent — any agent, however good its tools — writes:

> `OBSERVED — PENDING · rec_… @ 1:12 · watch for: does the control react at all before they leave`

and a person changes it to `OBSERVED (n=1)` after they have looked. **Nothing else clears it.**

These are all `MEASURED` or `RECONSTRUCTED`, and none of them is `OBSERVED`:

- reading `events` out of a replay file — `RECONSTRUCTED`
- a headless render, a bounding-box script, `getBoundingClientRect`, a computed fold — `MEASURED`
- a screenshot your tooling captured and you described without a human seeing it — `RECONSTRUCTED`
- "I loaded the page and inspected the DOM" — `MEASURED`. The DOM is source, not a screen

**Measured, twice, the night this was written.** The same skill ran twice on the same corpus on the
same browserless machine. One run refused `OBSERVED` and said so in its findings. **The other run
awarded itself three `OBSERVED` rows** off a headless bounding-box measurement, and every word of its
prose was otherwise correct. One run in two. That is why this rule is mechanical instead of a
judgement call: **no display, no `OBSERVED` — write PENDING and name the coordinates.**

**Refusal rule.** If a claim cannot be given one of these four grades with a citation attached,
**do not pass it**. Say what evidence would settle it and stop. A finding you cannot grade is a
hypothesis wearing a finding's clothes.

---

## Running this on a folder of recordings

If you were handed a package (`index.json` + `replays/` + a `player/`), this is the whole loop:

```bash
python3 -m http.server 8900 --bind 127.0.0.1   # localhost only. Never serve replays to your network.
open http://localhost:8900/player/   # the recordings list — this is what you triage from
```

- **`data/index.json`** — one row per recording. This is your census. Read it with a script, not
  by eye; `jq` or five lines of Python beats scrolling.
- **`data/replays/<id>.json`** — one recording. `events` is its own event log (each with `t`,
  `event`, `props.target_text`); `snapshots` is the raw replay. **Reading `events` is
  RECONSTRUCTED. A *human* opening the player and looking is OBSERVED.** They are not the same row,
  and an agent can only ever reach the first.
- **the product's own source** — wherever the frontend lives. This is where a dead click stops
  being a count and becomes MEASURED: an element with no handler, at `file:line`.
- Write the result into **`FINDINGS.md`**.

"Kill the question with a query" below means: with whatever you have. A `jq` over `index.json`
counts as a query. A warehouse is not required.

## Step 0 — the question. No discriminating question, no watching

**Refuse to open a player until a question exists that different answers would change a decision.**
"Watch recordings" is not a question. "Why do people who reach the report not generate an article,
given that the funnel shows the drop but not the reason" is.

Then, before watching anything, **try to kill the question with a query.** Most hypotheses die here,
free.

**Keep the portfolio balanced — four families, not one.** A player fed only pathology questions
returns only wreckage:

| family | asks |
|---|---|
| **pathology** | where does it break |
| **comprehension** | what did a first-timer understand |
| **workflow shape** | how do the people who *succeed* actually work — the path you did not design |
| **journey** | what changed between visit 1 and visit N |

**Most teams only ever ask the first one.** Growth, once the bugs are gone, lives in the third.

## Step 1 — the denominator is people, and they must have been able to try

A rate is four claims, and each has killed a real finding:

- **people, not sessions** — recorders fragment one visit into many; strip bots, internal and test
  traffic **before** any segment carries a rate. ⚠️ *Test traffic* means traffic that is not a
  customer inside a product that has customers — your own team, monitors, QA accounts. **If you
  were handed a corpus that is entirely staged (a case, a demo project), the corpus IS the
  population**: strip the bots and the monitors inside it and carry on. Do not zero out your own
  denominator on a technicality;
- **everyone counted could have done it, for the whole window** — check when the control shipped;
- **somebody attempted it** — an empty cell is *nobody tried* **or** *everybody failed*, and those
  are identical in every instrument you own. If you cannot prove attempts, **that** is the finding;
- **the window was chosen before the data** — re-cut by week before publishing.

## Step 2 — triage from the index, not the player

Classify every recording from the list view: duration, pages, clicks, dead clicks, viewport,
device, role, furthest step. Most close here. For each survivor write **the question it might
answer and the timestamp range where the answer must be**.

**Budget: you will watch 5–10% of the corpus.** That is not laziness, it is the method. State the
three numbers in the report: *censused → flagged → watched*.

## Step 2b — the reconstructed pass, without burning your context

Triage gave you candidates. Reading them **whole** is where a review quietly becomes unaffordable.

### 1 · Read the event log, not the recording file

Measured on this course's package — compact JSON bytes, all 159 files: a recording averages
**52 KiB**, its `events` array **2.1 KiB**. **The events are 4% of the file.** The rest is the rrweb
stream — measured here, **76% of it full-snapshot DOM**, the remainder mouse, scroll, selection and
mutation records. For a triage pass that is **~25× less** to read.

⚠️ 🔴 **That is this package's layout, not a fact about rrweb.** Here `events` is the product's own
log sitting *next to* the rrweb stream in `snapshots`. Native rrweb output is one undifferentiated
event stream; vendor exports wrap it differently, and several tools in the table at the end of this
file give you **no raw replay at all**. **Look at your own file's shape before you copy a command.**

And check what you were already given: this package ships **`data/events.json`** — the whole corpus,
denormalised, no snapshots. For triage you may not need the per-recording files at all.

### 2 · The deep pass — what the recording can and cannot tell you

After triage, on the handful that survived, the DOM is often exactly the evidence you want. **Know
what is actually in there**, because the first draft of this section got it wrong:

| the question | is the answer in the file? |
|---|---|
| is this a real `<button>`, or a `<div>` dressed as one? | ✅ `tagName` and attributes are in the full snapshot |
| **was text selected when they clicked?** | ✅ rrweb selection events (`source: 14`), in **17 of the 159 files here**. The copy-select tape below carries **four** of them |
| did they scroll, and how far? | ✅ scroll events (`source: 3`) in **101 of 159**, plus `initialOffset` on every full snapshot |
| **was the control on screen at that moment?** | ❌ **no bounding box is stored anywhere.** Element geometry comes from a render, or from an eye |

### 🔴 Presence in the DOM is not visibility on the screen

`Generate articles` is in the serialised DOM of **every** report page in this corpus — including the
narrow sessions where it was **off-screen until they scrolled**. An agent that greps a snapshot finds the button and
reports it was available. **That is the geometry finding, inverted, and it is the likeliest way a
fan-out pass produces a confident wrong answer.**

### 🔴 Snapshot reads are `RECONSTRUCTED`, not `MEASURED`

A snapshot is a historical capture — scripts stripped, listeners gone. Reading it is the same rung as
reading `events`: **a tool rebuilt it and nobody watched.** `MEASURED` is the *running* source at
`file:line` (Step 5), or **a geometry number you measured from a render** — not a screenshot nobody looked at. Two traps that follow:

- 🔴 **"No `onclick` attribute" proves nothing.** rrweb does not serialise event listeners, so a
  **`<div>` wired up in JavaScript and a dead one look identical**, and every working `<button>` looks
  handler-less too. Confirm a false affordance **in source**, as Step 5
  says — never from the absence of an attribute in a snapshot.
- 🔴 **A full snapshot is a base state, not the page at time T.** Later mutations change it. Grepping
  the whole blob will happily attach an element from another page, or from before the change you
  care about. Say which snapshot, and which mutations you applied.

### 3 · The fan-out contract

One subagent per recording, each writing its own note. **The contract is the part that matters:**

| | |
|---|---|
| **one note per recording** | `<notes_dir>/<rid>.md` — one directory, named by you, beside your `FINDINGS.md`. Pass it to each child; do not let them each invent one. 🔴 **Never a shared file** — concurrent writers clobber each other and you find out when the counts stop reconciling |
| **extraction, not interpretation** | the sequence and the element, never the mechanism. This is what makes a smaller, cheaper model the right tool — and asking a weak model *why* manufactures exactly the plausible-and-wrong reading Step 3 exists to catch |
| **a fixed shape** | so the parent reads twenty notes for the price of one recording |
| **notes inherit the replay's privacy class** | they quote page text. Store them where the replays live, or redact as you extract. *"Coordinates, not screens"* applies to your own notes |

A prompt that works:

```
You have one recording file: <path>, and its row from index.json.
You cannot watch anything - there is no player here.
Timestamps in `events` are absolute epoch ms; subtract the first one to get m:ss.ss.
Read its `events` array. Write <notes_dir>/<rid>.md and nothing else, exactly this shape:

  header:  role · viewport · duration · furthest_step
  every event from the last page_view onward:  m:ss.ss  event  target_text-or-url
  RECONSTRUCTED: what the sequence shows. No mechanism, no "because".
  OBSERVED - PENDING · <rid> @ <timestamp> · watch for: <what a human must confirm>

`OBSERVED - PENDING` is the only form of that word you may write. Never award or clear
OBSERVED, whatever tools you have. Do not explain why it happened.
```

**A note for `rec_mtf1jjyagas78o`. Every value below is checkable against `index.json` and that
file's own `events` array — check them, that is the point:**

```
# rec_mtf1jjyagas78o
admin · viewport 1366x657 · 39s · furthest_step report_ready

0:25.46  page_view    /report.html
0:25.46  report_ready /report.html
0:34.56  rage_click  Refund policy for annual plans
0:35.56  dead_click  Refund policy for annual plans
0:36.06  rage_click  Why did my invoice change this month
0:37.06  dead_click  Why did my invoice change this month
0:37.32  rage_click  Export your data before cancelling
0:38.32  dead_click  Export your data before cancelling
0:39.04  rage_click  Resetting two-factor authentication
0:40.05  dead_click  Resetting two-factor authentication

RECONSTRUCTED: four row titles, each a rage click then a dead click one second later,
across 5.5 s. No navigation follows. The tape is 39 s, so the last pair lands past the end.
OBSERVED - PENDING · rec_mtf1jjyagas78o @ 0:34.56 · watch for: is text selected on screen
```

🔴 **Note what the note does not say.** It does not say *the rows are broken*. On this tape they are
not — the person is selecting text, and this file carries **four rrweb selection events** that say so.
An extraction-only child leaves that verdict open. A child asked "what is happening here?" closes it,
wrongly, with confidence.

**Then the parent reads `notes/`** instead of the replays — but 🔴 **spot-check one note against its raw file before you
build on the set — and every note you are about to hang a finding on.** The first version of this section shipped a
worked example with the wrong role, the wrong timestamps and an invented CSS class; two independent
reviewers caught it. Lossy notes from a cheap model are exactly the input this method is supposed to
distrust.

**Fan-out never raises the ceiling.** Twenty subagents produce twenty `RECONSTRUCTED` reads. Whatever
tools a child has — browser, screenshots, a headless render — **agent output is never graded
`OBSERVED`**; it writes `OBSERVED - PENDING` and **a human** clears it. Parallelism buys throughput
and context. It never buys evidence.

**Fan-out multiplies the privacy question.** The deep pass ships real DOM. If it may not go to one
model it may not go to twenty, and a cheaper model can be a different provider or data path — an
approval you hold does not travel with it. See *Before you point an agent at real recordings*.

**When not to bother:** under about five candidates, read them yourself. Fan-out has fixed overhead in
prompt, plumbing and reconciliation.

## Step 3 — the dead-click gate. A count is not a defect count

🔴 **Classify before you cite.** The same label covers at least four behaviours:

| behaviour | tell | verdict |
|---|---|---|
| **copy-select** | a text selection at the same timestamps; clicks land on prose | **NOT a defect** — it is demand for export/copy |
| **reading tap** | single tap on body text, no repeat | not a defect |
| **false affordance** | repeated clicks on a card, tile, row or padding styled as clickable | **a defect** — confirm in source that the element has no handler |
| **slow control** | it works, it is just slow | not a defect; a latency finding |

🔴 **Run the same gate over rage clicks, because the same false positive is in there.** A
triple-click to copy is, to a coordinate-based detector, three clicks inside 30 px — a rage click.
On a corpus where the dead-click gate has just cleared a copy-select cluster, expect most of the
rage ledger to be **the same people doing the same thing** — the two detectors are watching one
gesture from two angles. Whoever accepts "those dead clicks are people copying, not a defect" will
ask about the rage clicks on the identical rows within about a minute, and the answer has to be the
same gate, not a shrug. Rank by people, open the tape.

**And know your detector's definition — by RUNNING it, not by reading it.** This is not
theoretical; it cost us a claim:

> We read `posthog-js` source and concluded that `$dead_click` skips `a, button, form, input,
> select, textarea, label` by tag, and drops any click with a text selection inside 100 ms. Two
> independent reviewers read the same source and agreed. Three sources, one answer, graded MEASURED
> with a file and a line number.
>
> Then we ran the library. **All three behaviours fire `$dead_click`** — the copy-select, the inert
> `<button>`, and the inert `<div>`. Twice, identical. The source we had read was **1.236.2**; the
> CDN serves **1.422.5**.

**The rule that came out of it, and it belongs in the ladder:**

> 🔴 **Source is MEASURED only for the version that is actually running.** A `node_modules` copy, a
> GitHub tab and a docs page are three ways of reading the same stale thing. Print the version, then
> trigger the behaviour and watch what the library emits.

Practically: before you quote any vendor's dead-click semantics, wrap `capture` (or open the network
tab), perform the three behaviours above yourself, and write down what actually fired. It takes ten
minutes and it is the difference between a finding and an anecdote about a changelog you did not read.

**Rank targets by people, not by clicks.** One furious person is not a pattern.

## Step 4 — watch, and write down what you actually saw

> 🔴 **Do this before you read the source.** If you can already state the mechanism from a `grep`,
> you have a `MEASURED` row and no `OBSERVED` one, and the review is not finished.

Watch the survivors at 1×, seek to the flagged timestamps, and describe **what was on the screen**
before interpreting it. Separate the description from the reading:

> OBSERVED: at 0:37 the cursor sweeps across the paragraph and the text highlights; the events panel
> shows three clicks in 400 ms. INFERRED: they were copying the report because they could not find
> an export.

**Look at what the screen SHOWS, not only what the user clicked.** A method built on events is blind
to a thing that produces no event: a next step below the fold, a label that means two things, a
status with no action. **Ask the geometry question — where was the control, and was it on screen?**
No automated pass asks it by default. Your eye asks it for free.

## Step 5 — triangulate, or it stays a story

**Replay alone is a story. Replay + events + database + source is a finding.** For every
load-bearing claim:

- **events** — does the log agree with what you watched?
- **database** — what actually happened (the row that proves the action landed)? ⚠️ **If there is
  no database** — you were handed a case, a static export, someone else's product — say so, and
  triangulate against the event log and the source instead. **Two independent sources, named, beats
  three claimed.** Do not quietly drop the leg and keep the confidence.
- **source** — grep the component before theorising. An element with no handler is a *proven*
  false affordance, citable as `file:line`, and it is a finding at **n=1**.
  🔴 **But grep after you watch, not instead of watching.** The source tells you *what the code
  does*; it cannot tell you *what the person was trying to do* — and that second thing is the only
  reason to open a recording at all. Grep first and you will find a real mechanism attached to the
  wrong intent, confidently, in about ninety seconds. Step 4 comes before Step 5 for this reason.
- **a column is not behaviour until you know what writes it.** Grep the writer.

**Publish the mechanism, not the rate, when n is small.** "3 of 4 mobile users went silent" is not
75%.

## Step 6 — refute your own pattern before you publish it

One adversarial pass per candidate, defaulting to refuted. The usual killers: hidden-tab time
counted as attention · one visit fragmented into many sessions · internal traffic · one loud user
generalised · seasonality · **the weld** — two true findings fused into one story, where the join is
the part with no evidence. **Go hunt one counterexample on purpose.**

## Step 7 — the output

A short table. **3–5 rows for a full review, never 12. In a time-boxed session — an hour or less —
1–2 rows is the target, and the mandatory rows below still apply to what you do produce.**

| | finding | grade | evidence coordinates | verdict |
|---|---|---|---|---|
| 1 | … | MEASURED / RECONSTRUCTED / OBSERVED / INFERRED | recording id + timestamp + what a verifier should check in 2 minutes | **DECIDED** / **OPEN** / **NOTHING TO DO** |

Mandatory, or the table is not honest:

- 🔴 **at least one row graded `OBSERVED`** — **a human** opened the player and looked. 🔴 If you are
  an agent this row is never yours to fill; you leave it `OBSERVED — PENDING`. If nobody could
  watch anything (no browser, no access), **say so at the top and grade nothing OBSERVED** — that
  is the honest outcome, and it means the review is not finished. A table of MEASURED and
  RECONSTRUCTED rows is a source audit, not a session review.
- **at least one `NOTHING TO DO`** — a count you cleared. If nothing died, you did not run the gate.
  *(In a 1–2 row time-boxed run, a killed claim in the "what died" section counts.)*
- **at least one `OPEN`, with no fix attached** — an opportunity. Force-fitting discovery into the
  defect template is how teams stop finding growth.
- **an owner on every DECIDED row**, by name. ⚠️ On a case or a product you do not work on, there
  is no name to write — put the **role** that would own it (frontend, product, data) and mark it
  unassigned. A blank owner is what makes a report get read and then nothing happens.
- **a tracking-plan line**: what is not logged that would have answered this without watching.

## Working without recordings

Everything above except Steps 2 and 4 works on claims alone. Given someone's draft findings, force
each into the ladder, attach coordinates or refuse it, name its false-positive modes, and write the
refuter question. **The refusal is the product.**

## 🔴 Before you point an agent at real recordings

This method sends replay content to a model. Session recordings are the one artifact whose **raw
material carries other people's screens** — names, emails, invoice numbers, whatever the DOM held.

- **Serve locally, to yourself only.** `--bind 127.0.0.1`. A bare `python3 -m http.server` listens
  on every interface and puts a folder of customer replays on your office network.
- **Synthetic or lab data may go to an agent freely.** Real replay DOM may not, unless your
  organisation has approved that provider and that data path. If you do not know, the answer is
  no — and finding out is the tracking-plan item.
- **What travels between people is coordinates, not screens**: a recording id, a timestamp, and
  what to check. That is the whole point of the evidence appendix.
- If you cannot send the DOM, you can still send **counts and shapes**: an event ledger with the
  text stripped is usually enough to triage, and the human opens the player.

## Wiring it to your tool

| | where the event list is | dead clicks labelled? | hidden tab visible? |
|---|---|---|---|
| **local replay folder** | the player's event panel | yours, defined in your own code | if you log it |
| **PostHog** | events tab; API **lists** recordings but returns no replay JSON — snapshots are a manual *Export as JSON* | `$dead_click` (see Step 3) | inactivity in the scrubber |
| **Microsoft Clarity** | events panel; export API is aggregate-only | yes, server-side, definition closed | yes, as an event |
| **Hotjar / Smartlook** | event timeline | varies | varies |
| **Yandex Metrica Webvisor** | player timeline; Logs API for raw hits | no | no — infer from activity gaps |

**The method does not change. Only the column names do.** If your tool cannot answer a question the
method asks, that gap is a tracking-plan item — write it down rather than working around it.

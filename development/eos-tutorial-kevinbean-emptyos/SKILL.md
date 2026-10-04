---
name: eos-tutorial
description: Generate a hands-on, multi-part technical tutorial as a learn-app course — one part per invocation, research-grounded, version-pinned. Use when the user says "/eos-tutorial <topic>" ("build a digital synth in Zig", "IEC 60909 fault calcs by hand"), "write me a tutorial on X", or "/eos-tutorial extend <course-id>" to append the next part to an existing series. The reader types the code themselves — this skill teaches, it never builds the project for them. NOT for one-shot Q&A (just answer), not for KB reference digestion (use vault-source-digest).
---

# EOS Tutorial — hands-on tutorial generator

Generate hands-on technical tutorials on demand, stored as KB notes and served
by the learn app (`/learn/`). The bar is the writing of Robert Nystrom
(Crafting Interpreters), Julia Evans, Bartosz Ciechanowski. Match it.

Borrowed discipline from [devenjarvis/lathe](https://github.com/devenjarvis/lathe);
adapted to the EmptyOS vault + learn app. **The human types the code** — a
tutorial that does the work for the reader has failed.

## When invoked

`/eos-tutorial <topic>` starts a new series; `/eos-tutorial extend <course-id>`
appends the next part. Extract the topic from the message.

1. Ask: **"What's your experience level going in — beginner, some familiarity, or experienced in adjacent areas?"**
2. If the topic is genuinely ambiguous (language? scale? embedded vs server?), ask **one** clarifying question. Otherwise skip.
3. **Pin the versions/editions** (below) — before research, so the tutorial is rooted in exactly what the reader will use.
4. **Research first** (below) — vault KB first, then web. The single most important step for accuracy.
5. Run the **pre-flight** silently — don't ask the user to approve the choices.
6. Write exactly **one part**.
7. Store: write the part note + create/extend the course via the learn API (below).

## Pin versions/editions (before research)

A tutorial is only as trustworthy as the versions it's rooted in. Two flavors:

- **Programming topic** → probe what's actually installed (`go version`,
  `python --version`, `node --version`, `zig version`, …), then confirm:
  *"I'll write this against **Python 3.13** — sound right, or do you want a
  different target?"* The pinned versions become a constraint on your prose:
  version-sensitive facts are anchored to the pinned version.
- **Engineering topic** → pin the **standard edition** (e.g. IEC 60909-0:2016,
  AS/NZS 3008.1.1:2017). Check the KB for `reference`/`clause` notes covering
  it (`/kb/` or vault grep under `30_Resources/EmptyOS/kb/`) — existing clause
  notes are your primary sources and get cited as `[[slug]]` wikilinks, which
  the learn player upgrades to clickable PDF anchors (`[[ref-slug]] p.67`).

## Research first (before drafting)

**Vault first, then web.** Query the KB for relevant notes; cite them as
`[[slug]]`. Then use WebSearch/WebFetch to find and *actually open* 3–8
authoritative sources — official docs, specs/RFCs, primary papers, source code,
well-regarded deep-dives. Don't reconstruct them from memory.

- **Read for the load-bearing facts** you'll commit to: exact API signatures,
  default values, flag names, version numbers, semantic guarantees, error
  messages. Keep the URL beside each fact; deep-link to the section, not the
  homepage.
- **Source beats recall.** When a source contradicts your memory, the source
  wins. A load-bearing claim you can't source is flagged `[!UNVERIFIED]` with
  a note on what to check — never asserted confidently.
- **Keep the consulted URLs** — cite load-bearing ones inline, list them in
  `## Sources`, record them in the part note's `sources:` frontmatter.
- **No web tools this session?** Say so in one line, write more conservatively,
  and `[!UNVERIFIED]`-flag the load-bearing unknowns (only those — don't paper
  the page with caveats).

## Always write ONE part only

Every invocation produces exactly one part note. Never write multiple parts in
one shot. The reader pulls the next part with `/eos-tutorial extend <course-id>`
— pacing stays with them.

## Pre-flight (private — never ask the user)

Settle these in your head before writing a sentence:

- **The controlling example.** One concrete artifact, carried through the whole
  series. Crafting Interpreters has Lox; you might have *"a 4-voice subtractive
  synth playing a sustained A-minor triad"* or *"a key-value store called
  `pebble` that survives `kill -9`"*. Never switch examples mid-series.
- **Specific numbers.** Sample rate, buffer size, fault level, cable size,
  latency budget — decide now so they're consistent across parts. Numbers are
  how you earn the reader's trust.
- **One controlling metaphor (optional).** If you adopt one, deploy it across
  ≥3 section transitions, then *explicitly retire it* with a wink. Don't mix
  metaphors silently.
- **The closing send-off.** What should the reader be ready to do beyond what
  you taught? Build toward it.
- **3–5 exercises**, each specific enough to start within 30 seconds.

## Part shape

Section titles must be specific to the domain — never `## Step 1: Setup`;
always name the thing the section makes (`## A scanner that recognises
one-character tokens`).

```
# [Title — Part N: subtitle]

[Hook — 2 to 4 paragraphs. A real question, a surprising number, a small demo.]

## What you'll build

One paragraph. The concrete end state, named with the controlling example.

## Prerequisites

Bullets: tools to install (with pinned versions), what the reader should
roughly know. Part 2+ may just say "Part N−1 finished".

## [Specific section title]

Why this exists. Then code in small blocks, each with an explicit insertion
point ("add this below the `parse` function"). Aside or design note where it
earns its keep.

> [!PREDICT]
> Before you run this: what output do you expect, and why?

> [!RECALL]
> (Part 2+) Which piece from Part N−1 does this build on?

> [!UNVERIFIED]
> Claim I couldn't source — check your version's docs for X.

## Checkpoint

> [!PREDICT]
> What do you expect to see?

**Run this to verify your work so far:**
\`\`\`bash
<the exact command>
\`\`\`

Expected output:
\`\`\`
<what they should see>
\`\`\`

**Likely errors:**
- If you see `<exact error text>`, you probably <causal explanation — "skipped the import in §2">.
- If you see `<exact error text>`, you probably <causal explanation>.

## What's next

One paragraph naming the unanswered question the next part will answer.
Include in every part — it invites `/eos-tutorial extend`.

## Exercises

1. <specific>
2. <specific>

## Sources

- [Title](url) — what it grounded
- [[kb-slug]] — which claims it anchors
```

## Storing the part + course

### 1. Part note (direct vault write)

Path: `{vault}/30_Resources/EmptyOS/kb/notes/tutorial-<series-slug>-part-NN.md`
(vault root from `emptyos.toml` `[notes] path`). Frontmatter — **block-style
tags, never inline**:

```yaml
---
tags:
  - kb
  - tutorial
kind: concept
author: ai
title: <part title>
series: <course_id>
part: 2
versions: "Python 3.13"
sources:
  - https://…
  - kb-slug
created: 2026-06-12
updated: 2026-06-12
---
```

The vault watcher reindexes automatically.

### 2. Course note (learn API — never hand-write `course-*.md`)

The daemon may require auth (`[network] auth_token` in `emptyos.toml`) and
binds IPv4 — always `127.0.0.1`, never `localhost`, and use Python urllib (not
curl) since titles may carry non-ASCII:

```python
import json, tomllib, urllib.request
cfg = tomllib.load(open("D:/emptyos/emptyos.toml", "rb"))
tok = cfg.get("network", {}).get("auth_token", "")
def api(path, body=None):
    req = urllib.request.Request(
        "http://127.0.0.1:9000" + path,
        data=json.dumps(body).encode("utf-8") if body is not None else None,
        method="POST" if body is not None else "GET",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {tok}"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)
```

- **New series:** `api("/learn/api/courses/save", {"title": …, "description": …,
  "level": <from the experience answer>, "domain": …, "topic": …,
  "tutorial": True, "lessons": [{"slug": "tutorial-<series>-part-01",
  "title": <part title>, "kind": "read"}]})` — note the returned `course_id`.
- **Extend:** `api("/learn/api/courses/<id>")` → take its `lessons`, append the
  new part (and re-send the existing fields: title/description/level/domain/
  topic/`tutorial: True` — the save endpoint overwrites in place), re-save with
  `course_id` set. Reuse the series' pinned versions and controlling example —
  read them from part-01's frontmatter + body before writing.

If the daemon isn't reachable, say so and stop after writing the part note —
tell the user the course link can be created next time the daemon is up.

## After storing

Tell the user: where the part landed, the course at
`http://127.0.0.1:9000/learn/` , that `/eos-tutorial extend <course-id>` adds
the next part, and that `/eos-tutorial-verify <course-id>` will walk the
tutorial end-to-end and badge it. Don't offer to "do the project for them."

## What NOT to do

- Don't write `index.md`, multiple parts, or a whole series in one invocation.
- Don't assert load-bearing facts from recall — source it or `[!UNVERIFIED]` it.
- Don't use generic section titles (`Setup`, `Conclusion`, `Step 3`).
- Don't switch the controlling example or silently mix metaphors mid-series.
- Don't put brand names in course chrome beyond what the topic itself requires.
- Don't pour tutorial content into the user's real projects — the reader builds
  in their own workspace; you only write vault notes.

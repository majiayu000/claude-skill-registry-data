---
name: inspect
description: Look at a page step by step in the account's own gated browser (AdsPower first) before writing code for it (rule 29), on any platform with a browser path. `log inspect start` opens the account's headed browser; `log inspect do` runs one action at a time and records each step's accessibility snapshot (refs), screenshot, HAR and rea reading as it happens. Use before writing or fixing any click/selector code, when a run hits a page nobody has looked at, or when the owner says "look at the page", "introspect", "what is on there".
---

# inspect

The order is: open the page, look at it, then write the code (rules 25, 29).
This is camofox-mcp's model (accessibility snapshots with element refs) on
log-cli's own launch, in the account's own browser (rules 35, 44).

## Hard boundaries

1. **One launch, every gate** (rules 19, 35): headed, proxy in
   country, the account's device and locale, the self-check, the raw HAR, the
   launch budget. `--bypass` only for the owner's runs outside waking hours.
2. **Read-only unless the owner asked** (rule 8): `goto`, `snapshot`, `back`,
   `wait` read; `click`, `type`, `press` act on the platform and need `--live`
   (over MCP, `inspectDoLive` with confirmLive).
3. **Live** (rule 26): run `start` through Monitor; every step prints as it
   happens.
4. One session per account: two accounts can be open at once, and `--account`
   picks the session (`log inspect sessions` lists them).

## The routine

```bash
# terminal 1 (or Monitor): the browser stays open until `do stop` or 30 idle minutes
log inspect start --account <a> --url <url> 2>&1 | tee <log>

# terminal 2: one step at a time
log inspect do snapshot
log inspect do goto <url>
log inspect do click e12 --live        # only when the owner asked
log inspect do stop
```

Each `do` prints where the page is, the requests the step made to the platform
(GraphQL by name, redirects with their target), rea's Evidence ID, and the
page's elements with their refs. Everything is kept in order in
`~/.logCli/runs/inspect/<time>_<a>/steps/NN_<action>/`: `snapshot.yml`,
`screenshot.png`, `network.har`, `rea.json`.

## Reading every step (rule 73)

What each part must do is in the spec, [docs/specs/inspectRuleOne.md](../../docs/specs/inspectRuleOne.md).

Give the session its goal when you open it, in plain words:

```bash
log inspect start --account <a> --goal "<what the session must get done>" --detach
```

Every `do` then reads its own step:

- **The internal API, by code:** each call the step triggered, what was
  sent and what came back, in seconds from the step's first request. It's
  printed under "Internal API in this step" and kept in the step folder as
  `exchanges.json` and `exchanges.md`. A repeated call shows only what
  changed since its last call (the query as it was typed, letter by letter,
  with each answer). Code loading and cross-site media are left out.
- **A step no known page state names** goes to SubQ with everything around
  it: the goal, the account, what we did (the mouse, how long it took),
  every call, the page text, the screenshot and the earlier steps. SubQ
  says what it means. The reading comes first in the result, starting with
  `>>> UNKNOWN STATE`, and the page-state hook puts it into your context.
  **Name that state before the flow goes on.**
- **The goal is judged across the session, not one step.** Each earlier
  step carries what the platform saved in it (its mutations that answered
  OK), and `goalSoFar` counts them since the goal was set, this step
  included. "Like 2 to 3 posts" is reached only once 2 likes are saved.
  A goal set with `inspect goal --set` counts only the steps after it.
- `--goal` on one `do` overrides the session's goal for that step.
- `log inspect read <run>/steps/NN_action --account <a> --goal "..."`
  reads a recorded step again (over MCP: `inspectRead`).

Each reading is one SubQ call ($0.04 per million input tokens).
`reading.json` and `readingState.json` hold the answers and exactly what
was sent.

## Keep going until the goal is reached, and write what went wrong (rule 73)

With a goal set, the turn isn't over until a step's reading says the goal
is reached. The page-state hook holds the Stop and says what's missing:

1. **A step went wrong** (its reading: wrong result, stopped by the
   platform, unclear, or SubQ failed). Write its finding before the next
   step, as P.E.E.:

   ```bash
   log inspect finding --account <a> --step <NN_action> \
     --point "<the issue, in one sentence>" \
     --explain "<why the evidence shows it, and what caused it>"
   ```

   - **Point:** the issue, in one sentence.
   - **Evidence:** filled in from the step's reading (each call SubQ
     flagged, with what was sent and what came back). `--evidence` adds
     your own.
   - **Explain:** why the evidence shows it, and what caused it.
2. **The goal isn't reached yet.** Take the next inspect step towards it.
3. **The goal is reached.** Say how each finding was fixed:
   `log inspect finding --account <a> --fixes 1 --fix "<what fixed it>"`

`log inspect goal --account <a>` shows the goal, whether it's
reached, and every finding. The run keeps them as `goalFindings.md`. What
only a person can clear (an ID, a video selfie) never holds the turn: say it
to the owner.

Then write the code from it: the selectors and the order of clicks come from
`snapshot.yml`, the waits from what `network.har` shows the page asking for.
Rebuild the platform's request docs after.

Facebook's pages, worked examples, request docs and sign-in: `skills/facebookInspect/SKILL.md` (the facebookBrowser guide).

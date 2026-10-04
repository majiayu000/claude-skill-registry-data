---
name: blueprint
description: Render an interactive, self-contained HTML blueprint app from a JSON spec, using a frozen renderer (tokens + layout + emitter) so the drafting-paper look, generated OKLCH palette, swimlane headers, phase sections, combined fragments, and switchable colour lenses are byte-identical every run on any project. You only ever author JSON. For a whole project it discovers scenarios once into a cached master file and re-renders only what git says changed. Use when the user wants a sequence diagram, a rendered/"proper" diagram (not ASCII), to visualise a request flow, API/service interaction, who-calls-whom over time, or to diagram a scenario as an interactive artifact (PNG export is built into the HTML).
source: github.com/functioncall/blueprint@021f3dd527a974cea519f070f0e949bec97c9501
---


# Sequence diagram

Render real sequence diagrams as **one self-contained interactive `index.html`**.
**Never hand-draw ASCII sequence diagrams** — they collide once labels have real text.
The renderer is frozen: `scripts/tokens.py` (the single source of truth for every
colour/size — never hardcode style elsewhere) → `scripts/layout.py` (pure geometry) →
`scripts/render_html.py` (SVG/HTML emitter) + `scripts/assets/` (app.css/app.js/page.html).
**You only ever write JSON data, so the look is identical every run, on every project.**
Design legend: `STYLE.md`. PNG is the in-browser ⤓ export (no separate PNG renderer).

The output is a small app: a clean header bar with a **scenario dropdown** (when there
are 2+), the active diagram full-bleed (sticky swimlane header, the body scrolls), and a
bottom toolbar of **colour lenses** + a PNG export. Click any message for its detail.

## Two modes

**A. Ad-hoc — one diagram, right now.** Write a spec (schema below) and render:
```bash
python3 ~/.claude/skills/blueprint/scripts/render_html.py spec.json index.html
```
A spec is either a single scenario `{title,actors,messages,…}` or a master
`{project,scenarios:[…]}`. Copy `examples/web-request.json` (single) or
`examples/master-backdrop.json` (master). Open the HTML to view; deliver the file.

**B. Project mode — the SET, cached + self-freshening.** One **master file** holds every
scenario and renders to one `index.html` (a card per scenario, switchable via the dropdown).
Discovery is a **dynamic fan-out**: list the flows once, let the user pick, then spawn ONE
agent per chosen flow (count scales to the list). A git check means you research once, not
every time, and adding scenarios later never touches the ones already drawn.

### Project-mode runtime flow (discover → choose → fan out → merge)
1. **Locate** the master (convention: `agent_docs/diagrams/architecture.json`, else
   `docs/diagrams/`).
2. **Build the candidate flow list:**
   - **No master (first build):** spawn ONE agent with `enumerate-prompt.md` at the repo
     (pass the existing ids = none) → a JSON list of every flow.
   - **Master exists:** run the git freshness check AND spawn ONE `enumerate-prompt.md` agent
     to spot brand-new flows (pass it the existing scenario ids so it returns only what's
     missing). Candidates = changed-known + new.
     ```bash
     python3 scripts/freshness.py master.json [repo]   # fresh | stale+list | no_provenance
     ```
     If freshness is `fresh` AND enumerate finds no new flows → skip to step 6 (render only).
3. **Choose — the gate (default ON):** show the candidates as an **AskUserQuestion
   multi-select** with a **"draw all"** option; draw only the ticked ones. **Override:** if the
   user's request already said "one shot" / "draw all" / "everything", skip the picker and take
   the whole list.
4. **Fan out — the dynamic workflow:** use `scripts/draw_workflow.js` as the template — bake the
   chosen flows (+ `repo`/`masterPath`/`skillDir`) into it as **literals**, then **write the
   filled-in script to a file and launch it with `Workflow({scriptPath})`**. It spawns ONE agent
   per flow (each reads only that flow's `source_paths` + reuses the master's actor vocabulary)
   and returns `{scenarios:[…]}` — one v3 scenario object each.
   ⚠️ Bake the flows in as literals in the **script body** — do NOT pass them via the Workflow
   `args` field (observed: `args` does not reach the script, so it runs with 0 flows). And prefer
   a **`scriptPath` file** over passing the whole `script` inline — inline embedding can mangle
   the prompt strings and trip the parser.
   (Tiny repo / no workflow wanted? `discovery-prompt.md` still does list+draw in one agent.)
5. **Merge:** add/replace those scenarios in the master **by `id`**; leave every other scenario
   byte-for-byte. (Workflow scripts have no filesystem — the main loop writes the file.)
6. **Validate → stamp → render:**
   ```bash
   python3 scripts/validate_master.py master.json   # must pass
   python3 scripts/stamp_provenance.py master.json [repo]
   python3 scripts/render_html.py master.json agent_docs/diagrams/index.html
   ```
7. **Open the HTML** (or screenshot it headless) before sending; commit the JSON + HTML.

## Spec schema (v3 — actors are PER SCENARIO)

```json
{ "project": "Acme",
  "provenance": { "git_sha": "GIT_SHA_AT_BUILD" },
  "scenarios": [
    { "id": "capture", "title": "…", "subtitle": "…",
      "meta": { "created": "2026-06-26", "updated": "2026-06-26" },
      "actors": [
        { "id": "user", "label": "User", "zone": "user", "sub_caption": "person" },
        { "id": "phone", "label": "Phone", "kind": "internal", "zone": "client",
          "sub": [ {"id":"ui","label":"Camera UI"}, {"id":"up","label":"Upload"} ] },
        { "id": "srv", "label": "Server", "zone": "server", "sub_caption": "/enrich" },
        { "id": "claude", "label": "Claude", "zone": "llm", "sub_caption": "Haiku" }
      ],
      "messages": [
        { "phase": "CAPTURE" },
        { "from": "user", "to": "phone.ui", "text": "press & hold", "paths": ["capture"] },
        { "self": "phone.ui", "text": "freeze still", "caption": "→ base64 JPEG" },
        { "phase": "ENRICH" },
        { "from": "phone.up", "to": "srv", "text": "POST /enrich", "caption": "+ ID token",
          "via": "api", "paths": ["enrich"], "src": "EnrichClient.swift → routes.ts" },
        { "from": "srv", "to": "claude", "text": "vision", "caption": "narration + image",
          "via": "api", "paths": ["enrich"], "metrics": { "cost": 0.011, "latency_ms": 900 } },
        { "from": "claude", "to": "srv", "text": "enrichment", "caption": "title, blurb, OCR",
          "kind": "ret", "metrics": { "cost": 0.011, "latency_ms": 900 } },
        { "from": "srv", "to": "phone.ui", "text": "push ready", "kind": "async", "via": "api" },
        { "note": "srv", "text": "enqueue wiki compile" }
      ],
      "fragments": [ { "kind": "opt", "label": "voice note present", "range": [1, 2] } ]
    }
  ] }
```

- **actors** (per scenario): `{id,label,zone}` (+ optional `kind`, `sub_caption`, `sub:[{id,label}]`).
  **Left→right order is computed automatically** from `zone` role (user → our client → our
  server → external third-party, busiest-first) — author them in any order. `sub` = sub-services,
  each a lifeline under the parent band (cap ~3). `sub_caption` is a one-line caption under a
  no-sub actor.
- **`zone`** = ROLE, drives ordering + the generated colour: `user`; client/`frontend`/`mobile`/
  `ui`; `server`/`api`/`worker`/`gateway`; everything else (vendors, datastores) = external.
  `kind:"internal"` also sits in the server tier. Colour is positional OKLCH — no per-zone hex.
- **messages** (ordered):
  - `{phase:"LABEL"}` — a section divider (vertical label in the left rail). No text/refs.
  - `{from,to,text}` — solid request (filled head = sync call). `"kind":"ret"` = dashed + open head
    (return); `"kind":"async"` = solid + open head (fire-and-forget / event). This is the **UML
    arrowhead vocabulary** — the mechanics channel. Address a sub-service as `actorId.subId`.
  - `"via":"api"|"io"` — the interaction **category** → a small DRAWN marker (no marker = a plain
    in-process call). `api` = crosses a process/network/trust boundary (HTTP/RPC/IPC/3rd-party SDK);
    `io` = a data-store read/write (DB/cache/file/blob). Defined by the **boundary crossed**, not the
    tech — so it means the same on web, mobile, embedded, a compiler, an ETL job. Composes with
    `kind` (a store-read return = `kind:"ret"` + `via:"io"`).
  - `"caption":"…"` — an optional **soft secondary line UNDER the primary**; put params / state /
    thresholds / model names here so the primary stays one short clause.
  - `{self,text}` — self-loop (= on-device process).
  - `{note,text}` — a **collapsed note**: a folded-page icon + a SHORT tag (`text`, ≤ ~24 chars);
    put the long explanation / file refs in `src` (revealed on click). For a genuine caveat the
    arrows can't show (a scope boundary, "CPU-only path") — use sparingly, never as a scratchpad.
  - `"metrics":{"cost":0.011,"latency_ms":900}` — enables the `$ cost` / `⏱ latency` lenses
    (a perceptual graphite ramp; absent data → that lens isn't offered).
  - `"paths":["enrich"]` — tags the message to a named flow → a `↪ enrich` highlight lens.
  - `"src":"File.swift → route.ts"` — the caller→callee files; shown in the click-detail footer.
  - `"detail":{…}` — the **AI-prefilled body of the click-detail card** (everything the arrow can't
    show). All six keys optional; emit only for **load-bearing** messages (api/io/metric'd/path-tagged
    or otherwise non-obvious) and **omit any key you're unsure of** — blank is correct, never guess.
    Keep each a tight clause (≤ ~140 chars). The card already shows the readable route, `step N/M`,
    phase and any fragment guard from the spec — so **`detail` must NOT restate the label, the
    participants, or the on-arrow caption.** Keys:
    - `why` — the card's **headline**: why this call exists, in plain language (NOT a paraphrase of
      the label). E.g. label `DELETE /account` → why `Erase the user; token-auth'd; cascade-safe.`
    - `effects` — what it mutates/emits as a result ("deletes 3 Firestore subcollections, then auth").
    - `fails` — behaviour on error (retry, fallback, throw, partial-state safety) — the 3am question.
    - `sends` · `auth` · `ordering` — short **chips**, not sentences: the payload/credential token
      (`Bearer ID token`), the identity that crosses (`Firebase ID token, verified first`), and any
      sequence constraint (`runs LAST`). Put the ordering/auth fact in its chip — don't also repeat
      it in `fails`/`effects` prose.
- **`fragments`** (per scenario): `[{kind,label,range:[a,b],segments?:[{guard}]}]`. `kind` ∈
  opt|alt|loop|par|break|critical|ref. **`range` indexes the NON-phase message order** (a,b
  inclusive). `segments` adds divider guards (for alt/par). **A box must wrap ≥2 messages** — for a
  single message, fold the condition into that message's `caption` instead (a 1-message `loop`, which
  asserts repetition, is the only exception). The validator warns on a degenerate box.
- **`meta`** (per scenario, optional): `{created,updated,status}` — informational.

## Conventions — label grammar (keeps every diagram readable on any codebase)
- **One short clause per primary `text`** (≤ ~30 chars / ~4 words → renders as ONE line, no wrap).
  Detail (params, state, thresholds, model names) goes in `caption`. **Never** put `·`/`—` or math
  in a primary — the validator rejects `·`/`—` there and warns past the length cap.
- **Phrase the primary by category** so types read at a glance:
  - in-process call → `name()` or `verb noun` (`render cells`)
  - `via:"api"` → `VERB target` (`POST /enrich`, `Auth.Login`)
  - `via:"io"` → `read`/`write`/`query X` (`read blob`)
  - async/event → `emit`/`on`/`enqueue X`
  - return (`kind:"ret"`) → the value as a noun (`JPEG bytes`, `200 OK`)
  - self/process → an imperative phrase (`build quadtree`)
- Tag category with `via`, direction with `kind`; they compose. Pair every request that returns
  with `kind:"ret"`. Put `metrics` on the paid/heavy call (and its return) — it's the metric, not a
  boolean. Use `phase` to chunk a long flow; `paths` for flows worth tracing.
- Aim for ≤ ~7 lifelines and ≤ ~20 messages per scenario; split if larger.
- Only diagram **real** behaviour — read the code, don't invent.

## Extending (keep the style frozen)
Every visual feature is a JSON field consumed by `render_html.py`, never caller-side drawing
code. New token/colour → `tokens.py` (then `STYLE.md`). New behaviour → `layout.py` geometry +
`render_html.py` emit. The author side never changes how things look.

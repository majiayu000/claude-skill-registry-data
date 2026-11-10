---
name: resource-extractor
description: >
  Use this at the very START of a hackathon build — BEFORE idea-forge — to gather the event's full,
  accurate documentation ecosystem into one committed resource pack: rules, published judging criteria
  and weights, every track/bounty, each sponsor's SDK/protocol docs (with testnet package/contract
  addresses and entry points), prize structure, and prior winners/showcases. idea-forge then diverges
  and converges on REAL extracted sources instead of guesses, and the architect plans against accurate
  integration facts. Trigger it when the user says "extract the hackathon docs", "gather resources for
  <event>", "pull the rules/tracks/sponsor docs", "research this hackathon", or hands a hackathon URL
  and wants the source material collected before ideating. **Many hackathon and sponsor sites are
  JS-heavy single-page apps (Dorahacks, Devfolio, ETHGlobal, Notion/GitBook handbooks, Docusaurus SDK
  docs) — this skill drives the Chrome browser tools to render, reveal, and capture that content.**
  As the campaign's first pipeline session it also runs the requirements TOLLGATE first (Stage 0):
  probe every access/plugin/MCP/toolchain the planned steps need — "check the requirements", "run
  the tollgate" — and commit the report so nothing is missing mid-execution. Do
  NOT use it to pick an idea (that's idea-forge) or to plan a build (architect).
---

# Resource Extractor — Step 0a: the hackathon's docs, extracted accurately

## What this is

The upstream-most step. Before idea-forge invents anything, this skill collects the hackathon's
**inter-related documentation** — rules → tracks → sponsors → each sponsor's SDK/protocol docs →
prior winners — into a **committed resource pack** the rest of the pipeline reads as ground truth. The
whole kit's top residual risk is a strong model confidently building on *wrong* facts (a mis-read
judging weight, a stale package address, a track it doesn't actually qualify for). This skill removes
that risk by extracting the facts verbatim, with source URLs and fetch dates, before ideation begins.

**Announce at start:** "I'm using the resource-extractor skill to pull this hackathon's rules, tracks,
sponsor docs, and prior art into a committed resource pack before we ideate."

## The one output — a resource pack

Write everything under `docs/resources/<YYYY-MM-DD>-<event-slug>/` **in the project repo**, then
commit and push it (the project repo is the single source of truth — every downstream step syncs and
reads it; `../references/repo-bootstrap.md`). You are usually the **first step that needs the repo**:
if the kickoff's `REPO:` names one, use it; if none exists, create it now via the user's logged-in
`gh` — from OUTSIDE the kit checkout (`../references/repo-bootstrap.md` §Creation protocol):
`gh repo create <event-slug>-<YYYY> --private --description "Hackathon workspace for <event> —
resource pack, brief, spec/plans, build. (build-system pipeline)" --clone`
(the project isn't chosen yet, so it's event-named; the seat that later fixes the project name —
idea-forge, or the architect when Step 0 is skipped — renames it to the project slug). Never write
the pack into the build-system kit checkout. Files:

- **`INDEX.md`** — table of contents + **provenance for every source**: URL, fetch date, tool used
  (WebFetch / Chrome), primary-vs-secondary, and a one-line confidence/gap note. This is what makes the
  pack trustworthy: a reader can see exactly where each fact came from and what wasn't verifiable.
- **`event.md`** — the essentials, **quoted verbatim, never paraphrased**: submission deadline
  (absolute date + timezone), eligibility, submission format/requirements, **the published judging
  criteria WITH their exact weights**, prize structure, and any testnet-vs-mainnet rule. These drive
  idea-forge's rubric and the architect's constraints, so numbers must be exact.
- **`tracks.md`** — every track and sponsor bounty: sponsor, problem statement, prize, the **minimum
  bar to qualify** (what you must integrate/deploy), and required tech.
- **`sponsors/<slug>.md`** — per key sponsor: what they actually reward, the SDK/protocol overview,
  doc links, and the **architect's feasibility fuel** — testnet **package / contract / object
  addresses**, **entry-point function signatures**, the integration model (which branch/SDK/codegen),
  code examples, and known gotchas. (This is the section that made the Leash brief's "Feasibility notes
  for the architect" possible — capture it for every sponsor you might target.)
- **`prior-art.md`** — past winners, sponsor showcases, and shipped competitors: name, one-line, tech,
  link. This is exactly what idea-forge's Novelty / white-space / judge-head-to-head steps consume.
- **`seeds.md`** *(optional)* — current-quarter narratives and sponsor's latest releases, to augment
  `../references/web3-seed-pack.md` for divergence (the seed pack is a dated floor, not the ceiling).

## The pipeline

### Stage 0 — Campaign tollgate (normally the campaign's first pipeline session)

Before scoping a single source, run the **campaign requirements tollgate**
(`../references/tollgate.md`): probe the full matrix for every step the campaign plans to run
(the kickoff or the guide's strategy names them; unknown → probe all), then write, commit, and
push `docs/tollgate/<YYYY-MM-DD>-tollgate.md` to the project repo — results, per-step verdicts,
and a fix hint for every FAIL. **If a campaign tollgate report already exists** (the guide ran it
on a skip-0a plan that changed, or an autopilot boot ran it — `../autopilot/SKILL.md`, under a
locked campaign contract, `../references/campaign-contract.md`), you are
not the campaign's first pipeline session after all: verify and **extend that report** (re-probe
your own rows, update stamps) rather than creating a second — one report per campaign, same rule
as the gate ledger. This is what keeps a missing MCP, toolchain, or access grant from
surfacing as a mid-execution roadblock three steps from now. **Hard-stop only on your OWN failing
hard rows** (the browser tools and the repo — you can't extract without them); every other step's
failure is a report line for the guide/user to fix before that step is green-lit, not your
blocker. Probes are read-only — you fix nothing, install nothing, log into nothing (sole exception:
row 15's throwaway `setx` variable, removed immediately after the read-back).

### Stage 1 — Scope the sources

- Get the hackathon name + its primary URL(s). From the rules/landing page, enumerate the **canonical
  sources** to extract: rules/handbook, tracks/prizes page, sponsor list, submission platform
  (Dorahacks / Devfolio / ETHGlobal / Akindo), and each targeted sponsor's docs site + GitHub.
- Decide the crawl frontier: follow **inter-related** links outward — rules → each track → each sponsor
  → that sponsor's SDK docs → its example repos / prior winners. **Bounded:** stay inside the event's
  ecosystem, ~2 hops from a sponsor page, dedupe URLs, and skip anything off-topic. Breadth over the
  event's real sources, not the open web.

### Stage 2 — Extract each source with the right tool

Pick the cheapest tool that actually renders the content:

- **Static / server-rendered pages → `WebFetch` / `WebSearch`.** Fast; use for plain docs, GitHub
  READMEs, blog posts, markdown handbooks.
- **JS-heavy / SPA / interactive / network-loaded → the Chrome browser tools** (see the section below).
  Use these whenever `WebFetch` returns an empty shell, a loading spinner, or obviously missing content
  — hackathon portals, Notion/GitBook handbooks, Docusaurus/Nextra SDK sites, anything behind tabs,
  accordions, "load more", infinite scroll, or an XHR/JSON API.

For every source, **extract the load-bearing facts verbatim** — judging weights, deadlines, prize
amounts, qualifying requirements, package/contract addresses, entry-point signatures. Quote numbers and
criteria exactly and attach the source URL; never round, summarize, or reconstruct them from memory.

### Stage 3 — Normalize, verify, flag gaps

- Cross-check facts that appear in more than one place (e.g. the deadline on the landing page vs. the
  handbook); if they disagree, record both with sources and flag it.
- **Freshness:** stamp each source with its fetch date. Note anything that looked stale or versioned
  (an old testnet address, last year's tracks).
- **Honesty over completeness:** if a page wouldn't render, was gated, or a section didn't load, say so
  in `INDEX.md` — mark it a gap. Never fabricate a criterion, address, or prize to fill a hole. An
  accurate "unknown" beats a confident wrong fact, because idea-forge and the architect trust this pack.

### Stage 4 — Write the pack and hand off

- Write the files above; build `INDEX.md` last so it reflects everything captured.
- **Commit and push** the whole `docs/resources/<...>/` pack to the **project repo** — resolving or
  creating it first per `../references/repo-bootstrap.md` (see *The one output* above). Until it's
  pushed it doesn't exist for the next session (`../references/conventions.md`).
- Hand off to **idea-forge**: tell the user the pack is committed and that idea-forge should read it as
  its primary source (its Step-1 inputs — hackathon URL, tracks, published judging criteria, prior art
  — are now pre-extracted here, so it forges on accurate resources instead of a one-shot search).

## Driving Chrome for JS-heavy sources (the part that matters)

Many of the most important sources render client-side and are invisible to a plain fetch. Use the
browser, in this tool-preference order (per this environment's MCP guidance):

1. **A dedicated MCP for the source**, if one exists (rare for hackathon docs).
2. **The `claude-in-chrome` MCP** — DOM-aware and fast; the default for web extraction. If its tools
   are deferred, load them in ONE `ToolSearch` call (bulk), e.g. `navigate, tabs_context_mcp,
   tabs_create_mcp, get_page_text, read_page, find, read_network_requests, read_console_messages,
   computer`.
3. **`computer-use`** (pixel control) — only if the Chrome extension isn't connected. Slower; last
   resort.

**Extraction loop with `claude-in-chrome`:**

1. **`navigate`** to the URL (standalone `navigate` creates the tab context for you and returns tab
   ids; otherwise call `tabs_context_mcp` first).
2. **Let it render.** For SPAs, the DOM isn't ready at load — check `read_console_messages` /
   `read_network_requests` for the page to settle before reading. Re-read if content is still a spinner.
3. **`get_page_text`** for article/handbook prose; **`read_page`** (accessibility tree) when you need
   structure or interactive element `ref_id`s to act on.
4. **Reveal hidden content.** Use **`find`** (natural language, e.g. "prizes tab", "expand judging
   criteria", "load more projects") to get element refs, then **`computer`** to click/scroll them —
   expand accordions, switch tabs, trigger infinite scroll — and re-read. Content behind a click is the
   single most common thing a plain fetch misses.
5. **Capture API-loaded data.** Portals often load tracks/prizes/winners as JSON via XHR. Use
   **`read_network_requests`** with a `urlPattern` (e.g. `/api/`, `graphql`) to grab those payloads
   directly — often cleaner and more complete than the rendered DOM.
6. **Follow links in new tabs** (`tabs_create_mcp` + `navigate`) to walk sponsor → docs → examples
   without losing the parent page.

**Read-only and safe, always:**
- **Extraction only.** Never log in with the user's credentials, never register/submit a hackathon
  entry, never fill or submit a form, never accept terms, never move funds or connect a wallet. If a
  resource is truly gated behind auth, record it as a gap and move on — ask the user rather than
  authenticate.
- **Verify URLs before following**, and don't chase links off the event's ecosystem. Decline cookie /
  consent pop-ups (most privacy-preserving option).
- **No secrets** in the pack — only env-var names, same rule as the rest of the kit.

## Guardrails

- **Accuracy over coverage.** A small pack of verbatim, sourced facts beats a big pack of paraphrase.
  Every load-bearing number carries its source URL and fetch date.
- **Extract, don't invent.** No fabricated criteria, addresses, prizes, or competitors. Gaps are
  labeled, not filled.
- **Bounded crawl.** The event's ecosystem, not the open web. Dedupe, cap hops, stop at diminishing
  returns.
- **Strong model.** Reading dense rules and SDK docs accurately is model-bound — run this on your top
  reasoning seat (tier `top`, at its §Seat settings effort — `../references/model-routing.md`),
  same as idea-forge and the architect.
- **The project repo is the single source of truth.** Commit and push the pack there before handing
  off — creating the repo first when none exists (`../references/repo-bootstrap.md`); never into the
  build-system kit checkout.

## When NOT to use this skill

- You already have accurate, current docs for the event — hand them straight to idea-forge.
- It isn't a docs-rich, sponsor-driven event (the pack's value is thin without tracks/sponsor SDKs).
- You're past ideation and need a spec/plan/build — that's the architect / orchestrator.

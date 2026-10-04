---
name: saas-platform-teardown
description: This skill should be used when the user gives a SaaS product's landing page URL, homepage, or name and asks for a full teardown or deep-dive of how the product works across web, desktop, and mobile — including per-platform feature inventories and user journeys, tech stack, pricing/plan mapping, how the platforms integrate and sync (and the business logic behind those choices), hardware integrations, business-scale/revenue signals, and concrete release artifacts per platform — with a structured Markdown report as the deliverable. Trigger on phrases like "research this SaaS", "do a platform teardown of X", "map every feature of this product across web/mobile/desktop", "reverse-engineer how this app works everywhere", or a bare URL plus a request to understand the whole product.
---

# SaaS Platform Teardown

## Role

Act as a product-research engineer producing a due-diligence-grade teardown of
a SaaS product from nothing but its landing page URL. The deliverable is
Markdown documentation good enough that someone who has never seen the
product could explain, to a stakeholder, exactly what it does, on which
platforms, how those platforms talk to each other — and whether the business
behind it is substantial — with enough method transparency that the reader
can tell verified truth from secondhand reconstruction.

## Before starting

Confirm what's available and degrade gracefully rather than stalling:

1. Check for live browser access, in this order:
   a. Playwright MCP tools (`mcp__playwright__browser_navigate`,
      `browser_snapshot`, etc.). If this session started before the server
      was registered, it won't be present — see (b).
   b. `agent-browser` CLI on `$PATH` (`agent-browser --version` via bash).
      Same audit capability, shell-driven.
   If both are absent, tell the user the web audit will be limited to static
   page fetches — no live app exploration — and continue anyway.
2. Check whether `agy` is on `$PATH` (`command -v agy` via bash). If
   present, use Engine B per `references/06-research-sweeps.md` for
   broad/fast-moving research — read that playbook's permissions section
   before the first sweep (a silently-empty answer means a blocked tool,
   not a finished search). If absent — the common case — run the same
   sweeps via Engine A (the built-in web search/fetch tools) per the same
   playbook: slower, sequential, functionally equivalent. Either way,
   follow that playbook's engine-pick rule and record the engine used in
   the report's methodology section.
3. Check for `gh` (useful when the product has public repos) and a
   Wappalyzer-class tech detector (useful for stack fingerprinting). Neither
   is required to proceed.

Never wait on tool availability — note the gap in the final report's
methodology section and move on with the next-best method.

## Phases

Work through these in order. Each phase has its own reference playbook —
read the file with the `Read` tool immediately before starting that phase,
not all at once at the start. This keeps context focused and matches how
this skill was designed to be used.

| Phase | Goal | Playbook |
|---|---|---|
| 0 | Turn the URL into a map of every platform surface, an access plan per surface, and a hardware yes/no | `references/01-intake-and-recon.md` |
| 1 | Live-explore the web app and walk its user journeys | `references/02-web-platform-audit.md` |
| 2 | Document the mobile apps — store artifacts, journeys — or confirm none exist | `references/03-mobile-platform-audit.md` |
| 3 | Document the desktop app — artifacts per OS/arch, journeys — or confirm none exists | `references/04-desktop-platform-audit.md` |
| 4 | Synthesize how the platforms share data/accounts/notifications, map each integration's business objective, and consolidate journey handoffs + personas | `references/05-integration-architecture.md` |
| 5 (parallel/ongoing) | Fan out broad research questions, including revenue/business-scale sweeps | `references/06-research-sweeps.md` |
| 6 | Assemble and write the final report | `references/07-report-assembly.md` |
| conditional | Hardware deep-dive — load ONLY if Phase 0 (or a store-listing permission) finds a hardware touchpoint | `references/08-hardware-integrations.md` |

(Numbering note: reference files are numbered 1–8 against the phases 0–7
they serve — the table above is authoritative.)

Phase 5 isn't sequential — dispatch research sweeps (either engine) as soon as Phase 0 gives you
concrete questions (company facts, funding/revenue signals, app store
presence, integrations directory, pricing), so results are ready by the time
Phases 1–4 need them instead of blocking on them. The hardware playbook is
also not a phase: it rides alongside whichever platform audit covers the
pairing surface (usually mobile), and if there is no hardware, the explicit
"none found" finding from Phase 0 is all the report needs.

Phases 1–3 each walk their platform's user journeys (onboarding/first-run,
the core "aha" task, account & team setup, a churn-risk moment, and any
platform-exclusive flow, persona-tagged) — the journey schema lives in
`references/02-web-platform-audit.md` and consolidates into the report's
user-journeys file during Phase 4.

## Operating rules

- **Self-serve access is in scope; walls are not.** A disposable-identity
  account on a vendor-offered free trial / freemium / sandbox tier is
  sanctioned and preferred. Never provide real payment info, never scrape
  behind a paywall you don't have legitimate access to, never bypass auth,
  rate limits, or bot protection, and stop at any payment-or-ID-verification
  wall. When a surface is genuinely enterprise-gated, switch it to the
  no-credential access ladder (canonical version:
  `references/02-web-platform-audit.md`) — demo videos, sales/conference
  recordings, help-center screenshots, review screenshots, Wayback, public
  API docs. The ladder is the sanctioned method, not a workaround, and
  never includes misrepresenting yourself to sales.
- **Log access methods per platform.** Every platform section of the report
  records which access methods produced its claims, their evidence grades,
  and why each was chosen. This log is how a reader weighs verified truth
  against secondhand reconstruction — omitting it overstates the report.
- **Attribute everything.** Every factual claim in the final report carries
  either a source URL or an explicit "Inferred from X" note. No claim should
  be traceable to nothing but the model's prior knowledge — this product's
  facts as of *today* are what matters, and training data goes stale.
- **Mark confidence.** Use exactly three labels in the report: `Confirmed`
  (directly observed — screenshot, DOM, API response, official doc),
  `Reported` (a secondary source states it — review, forum, press), and
  `Inferred` (deduced from indirect evidence — e.g., same session cookie
  domain across web and desktop implies shared auth backend). Inferences
  show their reasoning, not just their conclusion.
- **Revenue figures carry their method.** Every revenue/business-scale
  number names its source and how it was derived; estimates are labeled
  estimates; bottom-up ranges show their math and assumptions; regulator-
  filed figures replace estimates when they exist. A lone unsourced number
  is worse than no number.
- **Store-listing metadata is the ceiling for mobile binaries.** Never
  attempt APK/IPA extraction, third-party APK downloads, or any binary/DRM
  analysis — store-listing data is sufficient and is the limit.
- **Hardware gets an explicit answer.** Device families with protocols and
  pairing matrix, or a verified "none found (checked where)" — never
  silence.
- **Timestamp it.** SaaS products ship weekly. The report's header must
  record the research date, because "current" claims decay fast.
- **Prefer paraphrase over quotation** in the report body per normal
  copyright practice, even though this is internal research documentation.

## Evidence language

The report uses two orthogonal scales. Do not conflate them:

- **Claim confidence** grades *the claim*: `Confirmed` (directly observed —
  screenshot, DOM, API response, official doc), `Reported` (a secondhand
  source states it, with the source cited), `Inferred` (deduced, with the
  reasoning chain shown).
- **Access-method grade** grades *how the evidence was seen*: `live` /
  `vendor-documentary` / `third-party` / `marketing-render`. The ladder and
  its grades are defined in `references/02-web-platform-audit.md`.

Mapping between them: `live` evidence can support `Confirmed`. The other
three access methods support a claim at most at `Reported` — vendor docs
say, they don't show; third-party and marketing-render material says
somebody says. One reconciliation for fetched vendor-documentary content
(so two runs resolve it the same way): the fetch is a direct observation
of what the source *states* — "the pricing page lists X" can be
`Confirmed` — while the product-*behavior* the prose describes tops out
at `Reported (vendor-authored)`. A claim with no access method behind it
is `Inferred`, with the reasoning chain shown.

## Definition of done

Before writing the final files, verify the draft actually answers all of:

- What does this product do, in one paragraph a non-technical person understands?
- Who is it for, and what does it cost at each tier?
- What can you do on web that you can't do on mobile, and vice versa? Same for desktop.
- Is there a native mobile app, a native desktop app, both, or neither — with sources?
- Can a reader walk the product's five core journeys (onboarding, aha task,
  team setup, churn-risk, platform-exclusive) on each platform — with
  evidence basis, persona tags, and friction noted?
- Do web/mobile/desktop share one account and sync in real time, or are they more separate than the marketing implies?
- For every integration finding, is the business objective it serves stated
  (vendor-cited) or inferred with reasoning shown?
- Is there an explicit hardware answer — device families with protocol and
  platform pairing matrix, or a verified none?
- How big is the business? Revenue/scale figures each with method + source,
  a bottom-up range shown as math, and filed financials used when they exist.
- Are release artifacts complete per platform: desktop per-OS/arch table
  with version history, mobile store metadata per store, and a verified web
  link inventory with exact URLs?
- What's the underlying tech stack, to the extent it's externally observable?
- What does the product integrate with, and is there a public API?
- Does every platform section state which access methods were used and why?
- Where does the confidence break down — what couldn't be verified, and why?

If any of these is unanswered, that's a gap to close or explicitly flag —
not a reason to pad the report with restated marketing copy.

## Output

Follow `references/07-report-assembly.md` for the file-count decision and
exact structure. Write to `./<product-slug>-teardown/` in the current
working directory and present the files — a report that's written but never
surfaced to the user is a wasted teardown.

---
name: draft-ui-redesign
description: >
  Reads an existing page's UI code and the API responses that feed it, then writes a
  paste-ready generation prompt for a design tool (Claude Design, Google Stitch, v0,
  Lovable, Figma Make) that produces a modern redesign benchmarked against the leaders
  in that product domain. Also specs any additive, non-breaking APIs the new design
  needs. Use when the user wants to redesign, modernize, refresh, or improve the look of
  a page or screen; asks for a design prompt, design brief, or UI spec; names one of
  those design tools; or says a page looks dated, basic, or "like a bootstrap admin
  template". Presentation only: it preserves every existing data point, action, and
  behaviour, and never changes application logic or existing API contracts.
license: MIT
metadata:
  author: mshindi-labs
  version: "1.0.0"
---

# Draft UI Redesign

Turns a page that works into a prompt that makes it beautiful — without touching
what it does.

You produce **one markdown document**. You do not write UI code, edit components,
or change API handlers. The document's centrepiece is a self-contained prompt the
user pastes into a design tool.

## The Contract

Everything this skill produces obeys four rules. State them in the output
document, and repeat them inside the generated prompt.

1. **Nothing is removed.** Every data point, control, link, and state in the
   current page exists in the redesign.
2. **No logic changes.** Routes, validation, permissions, mutations, and
   calculations stay exactly as they are. Presentation only.
3. **APIs are additive only.** Never modify an existing endpoint's response
   shape. New endpoint, or new **optional** field — nothing else.
4. **Additions degrade gracefully.** The redesign must render correctly with
   today's data, before any proposed API ships.

Rule 4 is the one that gets forgotten. If the new design falls apart without a
field that does not exist yet, the design is wrong.

## Workflow

### Phase 1 — Locate the surface

Find three things:

- **The page** — the route file plus the child components that actually render
  data. Not the whole tree; stop where the data stops.
- **The data sources** — `fetch`/`axios` calls, server actions, route loaders,
  react-query/SWR hooks, GraphQL documents, tRPC procedures.
- **The response shape** — from the route handler or controller, an OpenAPI or
  Zod/schema definition, a TypeScript response type, or a sample response.

If the user names a route (`/settings/billing`), map it to files. If they name a
file, start there.

**Never invent field names.** If you cannot find the response shape, ask for it
or for a sample payload. A redesign built on guessed fields is worthless.

### Phase 2 — Audit the current page

This audit **is** the behavioural contract. Build it before thinking about
design at all.

| Element | Data point (source field) | Interaction | Effect |
| ------- | ------------------------- | ----------- | ------ |

If it renders, it gets a row. If it clicks, it gets a row. Anything you leave
out, the redesign silently deletes.

Then list separately:

- **States** — loading, empty, error, unauthorized, partial/stale data
- **Responsive behaviour** — any breakpoint handling that already exists
- **Derived values** — anything computed in the component rather than returned
  by the API (totals, formatting, filtering, sorting)

Unrendered fields in the API response are worth noting: data you already pay for
but do not show is the cheapest possible improvement.

### Phase 3 — Classify the domain, pick the benchmarks

Infer the product domain from the data nouns, not from the file name:

- `amount`, `currency`, `payout`, `invoice`, `balance` → fintech
- `assignee`, `status`, `priority`, `sprint`, `label` → work tracking
- `deployment`, `build`, `commit`, `region`, `logs` → developer tooling
- `event`, `metric`, `segment`, `retention` → analytics
- `sku`, `cart`, `variant`, `fulfilment` → commerce

Read `references/benchmarks.md` and pick **two or three** leaders. For each one,
name the **specific mechanic** you are borrowing and why it fits this page.

> Bad: "Make it look like Stripe."
> Good: "Stripe's transaction table — right-aligned tabular-figure amounts,
> 44px rows, status as a small dot-plus-label rather than a filled pill, so a
> dense list stays scannable."

A benchmark without a named mechanic is decoration. The design tool cannot act
on it.

If no domain matches, use the **Generic product surfaces** section of the
reference and say explicitly that you fell back to it.

### Phase 4 — Find the gaps (additively)

Ask one question: _what would the benchmark's version of this screen show that
we cannot render today?_

Sort each answer into one of two buckets:

- **Derivable** — computable from data already in the response. No API work.
  Note the derivation. Prefer this bucket; it is free.
- **Needs data** — genuinely absent. Spec it as an addition.

Each addition needs: why the design needs it, method + path, response shape,
and an explicit non-breaking note. Format in `references/prompt-template.md`.

**Cap additions at three.** More than that means you are redesigning the
product, not the page — say so instead of writing more endpoints.

If the page needs nothing new, say "no API changes required" and move on. That
is a good outcome, not a missing section.

### Phase 5 — Write the document

Write to `docs/redesign/<page>-redesign.md` using
`references/prompt-template.md`. Create the directory if needed.

Tell the user the path and point them at the prompt block — that is the part
they paste.

## Writing the Prompt Block

Section 3 of the document is the deliverable. It has one property that matters:
**self-contained**. It is going into a different tool, in a different tab, with
none of this conversation's context. It may not refer to "the audit above", the
codebase, or anything the design tool cannot see.

It must carry:

- What the product is and who uses it
- What this screen is for, and the one job the user came to do
- The **complete content inventory** from the audit — every data point, with
  real example values
- Layout direction and information hierarchy
- Design system direction: type scale, spacing rhythm, density, colour usage,
  border/elevation treatment
- Every state to design: loading, empty, error, and the dense/overflowing case
- Responsive breakpoints
- The constraint line: do not invent data beyond this inventory, do not remove
  anything from it

Write it as instructions to a designer, in prose and lists. Not as a JSON blob,
not as component code.

## References

- `references/benchmarks.md` — domain → industry leaders → the specific mechanic
  worth borrowing from each
- `references/prompt-template.md` — the output document template, the prompt
  block structure, and the additive-API spec format

## Evals

`evals/evals.json` — three scenarios (fintech transactions, work-item list,
deployments page). Run with the `skill-creator` skill's benchmark loop.

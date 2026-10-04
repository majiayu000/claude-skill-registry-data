---
name: gap-scan
description: Scan a codebase, live app, or site and find the features that obviously should exist but don't — missing exports, bulk actions, search/filter, undo, history, notifications, dead-end workflows, data collected but never surfaced, backend endpoints with no UI, and half-built features that stopped partway. Produces an evidence-backed, ranked punch list (top 10 max) with a portable gap_packet JSON. Use whenever the user asks "what features are missing", "what's this app lacking", "find gaps", "run gap-scan", "feature audit", or wants proposal ammo from a prospect's app. Also use it to recheck an existing gap_packet — "what's left to do", "recheck the gaps", "what got built since" — re-verifying findings against current code and marking stale ones superseded. Flags ABSENCE only — broken code goes to code-audit, confusing flows to ux-audit, weak persuasion to conversion-audit, underexploited assets to a WWBD-style analysis. If something exists but is bad, it's not a gap — hand it off.
---

# Gap-Scan

Find the features a product is obviously missing. Not what's broken (code-audit), not what's confusing (ux-audit), not hidden value in what exists — what's **absent** that users of this kind of product would reasonably expect.

The output is a punch list a client or team can act on: each gap cites the evidence that proves it, ranked by user value × effort, capped at 10. The report's credibility comes from what it refuses to include — no speculative wishlists, no "you could add AI."

## Modes

Ask which mode if not obvious from context; default to QA mode for the user's own repo, PROSPECT mode when the target is a lead's site/app. If a `gap_packet.json` already exists for this target, default to RECHECK instead of re-running a full scan.

- **PROSPECT mode** — fast pass on a lead's app or site. Goal: proposal ammunition. Top 5–8 gaps, each phrased as a client-facing line item ("Your customers can't reorder past purchases — every competitor offers this"). Lighter evidence bar (observed from the outside is fine), but still cite what you observed.
- **QA mode** — deep pass on a repo you have code access to. Goal: roadmap input. Full inventory, file-path evidence required for every finding, up to 10 gaps.
- **RECHECK mode** — re-run against an existing packet. See "Recheck mode" below.

## Process

### 1. Inventory once, reason many times

Do ONE scan of the target and build a capability map. Do not re-crawl files per lens — every lens below reasons against the map, not the repo.

For a repo, the map covers:
- Routes/pages and what each lets the user do
- Models/entities and their fields (especially fields written but never read/displayed)
- CRUD coverage per entity: create / read / update / delete / duplicate / archive / export / import / bulk
- Endpoints with no consuming UI; UI elements with no working backend
- TODOs, commented-out blocks, disabled buttons, feature flags that are off, dead routes
- Background jobs, events, and data being collected

For a live app (no code), the map comes from walking the UI: every screen, every action available per entity, every dead end.

### 2. Run the gap lenses against the map

Each lens is a question asked of the map — cheap reasoning, no new scanning:

1. **CRUD symmetry** — user can create but not duplicate/archive/export/bulk-edit? Lists with no search, filter, or sort where the data volume clearly demands it?
2. **Dark data** — fields or events collected but never surfaced anywhere. (Timestamps stored but no "last updated" shown; analytics events fired into nothing.)
3. **Orphans** — backend capability with no UI; UI promising something the backend can't do; endpoints nothing calls.
4. **Half-built** — TODOs, disabled controls, dead-end screens, flags stuck off. Features that stopped partway are the cheapest gaps to close.
5. **Table stakes** — what does this *category* of product normally have that this one lacks? (A CRM without activity history; an e-commerce app without order status; a SaaS without password reset.) Name the category explicitly before applying this lens, so the comparison set is honest.
6. **Workflow dead ends** — a user completes step N and there's no step N+1 where one obviously belongs (created an invoice, can't send it; finished a report, can't share it).

### 3. Evidence gate

Every finding must cite proof or it's cut:
- QA mode: file path(s), route, or model field that demonstrates the absence ("`orders.ts` has create/get/update — no export or bulk endpoint exists; `OrdersList.tsx` renders single-row actions only")
- PROSPECT mode: what was observed ("Products page lists 200+ items, no search input present")

**Anchor evidence to symbols, never to line numbers.** Cite `src/api/orders.ts → createOrder` or `OrdersList.tsx → <RowActions>`, not `orders.ts:142`. Lines move on every unrelated edit; symbols don't. A recheck can then tell "the symbol moved" (finding still valid) from "the symbol is gone" (finding stale) — with line numbers both look identical.

"Users probably want X" with no anchor in the map is not a finding. The table-stakes lens still needs an anchor: name the comparable category norm AND confirm the map shows the absence.

### 4. Rank and cap

Score each surviving gap on two axes, no fake precision:
- **User value**: High / Medium / Low — how often would real users hit this absence?
- **Effort**: S / M / L — S if the surrounding infrastructure already exists (single-record action → bulk is usually S; a whole notification system is L)

Sort: High-value + S-effort first. **Hard cap: 10 findings** (5–8 in PROSPECT mode). Everything else gets one line in an appendix or gets cut. Resist padding — a 6-gap report that's all real beats a 10-gap report with filler.

## Report structure

ALWAYS use this shape:

```
# Gap-Scan: [target]
Mode: [PROSPECT | QA] · Category baseline: [what kind of product this is]

## Top gaps
For each (max 10):
### N. [Gap name]
- What's missing: [one sentence]
- Evidence: [file → symbol anchors / observed behavior — never line numbers]
- Why it matters: [one sentence, user-anchored]
- Effort: [S/M/L] — [one line on why, citing existing infra if S]
- Suggested MVP: [smallest version that closes the gap]

## Appendix: minor gaps (one line each)

## Out of scope (handoffs)
[Anything found that belongs to code-audit / ux-audit / conversion-audit — one line each, don't elaborate]

## Start here
[ONE gap, by name. The first concrete action to take on it. One line on why it beats the others.]
```

`## Start here` is **required** and must be the last section — after the handoffs, so the report ends pointing at the reader, not at another skill.

Rules for it:
- Name exactly ONE gap. Not a ranked shortlist, not "start with 1 or 3" — one.
- Give the first concrete action, not the whole MVP. "Add a `GET /orders/export` route next to the existing `getOrders` handler" — something that can be started in the next 10 minutes.
- One line on why this one first. Usually: highest value at S effort, or it unblocks others.
- Pick it even if the top-ranked gap isn't the right first move. Ranking is by value×effort; the first move can differ (a Medium-value S-effort gap that takes 20 minutes may beat the High-value L-effort one as a starting point). If they differ, say so in the why-line.

In PROSPECT mode, add a `## Proposal framing` section — each top gap restated as a client-facing benefit line — placed before `## Start here`, which stays last.

## gap_packet output

Alongside the report, always emit `gap_packet.json` so other skills and swarm agents can consume the results. The packet is a **work list, not a snapshot** — it carries status so "what's left?" is answerable by reading the file, never by re-investigating the repo.

```json
{
  "packet_type": "gap_packet",
  "version": 2,
  "target": "repo path or URL",
  "mode": "prospect | qa",
  "category_baseline": "e.g. local-service business site",
  "scanned_at": "ISO date",
  "last_rechecked_at": "ISO date or null",
  "start_here": "id of the gap named in the report's Start here section",
  "gaps": [
    {
      "id": "bulk-actions-contacts",
      "name": "Bulk actions on contacts",
      "lens": "crud_symmetry",
      "value": "high",
      "effort": "S",
      "evidence": ["src/api/contacts.ts → listContacts", "src/components/ContactList.tsx → <ContactRow>"],
      "mvp": "Multi-select + bulk delete/tag on the contacts list",
      "status": "open",
      "first_seen_at": "ISO date",
      "closed_at": null,
      "closed_by": null,
      "supersedes": null,
      "superseded_reason": null
    }
  ],
  "handoffs": [{"skill": "ux-audit", "note": "checkout flow confusing"}]
}
```

Field rules:
- `id` — stable kebab-case slug. Never reuse or renumber; a recheck matches gaps by `id`.
- `status` — one of:
  - `open` — still missing, still valid
  - `closed` — the feature now exists (gap was actually filled)
  - `superseded` — the finding no longer holds for a reason other than being built: the evidence moved, the surrounding code was rewritten, or the premise turned out to be wrong. **`superseded` is not a soft `closed`** — nothing shipped.
- `closed_at` / `closed_by` — ISO date, and `"recheck"` | `"user"` | `"<skill or agent name>"`. Set on both `closed` and `superseded`; null while open.
- `supersedes` — when a recheck replaces a stale finding with a corrected one, the new gap points at the old gap's `id`.
- `superseded_reason` — **required whenever `status` is `superseded`**, null otherwise. One or two sentences on why the finding no longer holds: which anchor moved, what was rewritten, or — for a retraction — what the premise got wrong and what evidence disproved it. A superseded gap with no reason is indistinguishable from a finding that quietly vanished, which is the exact failure this status exists to prevent.
- Never delete a gap from the array. Status transitions only — the history is the point.

## Recheck mode

Findings rot. Between a scan and the next look at it, code gets rewritten, endpoints move, and gaps get filled without anyone updating the packet — so a stale packet quietly reports things that are no longer true while missing gaps introduced since. Recheck is the fix, and it is **not** a re-scan: it starts from the packet.

Trigger it when a `gap_packet.json` exists for the target and the user asks "what's left", "is this still accurate", "recheck", or re-runs gap-scan on the same target.

### 1. Load, don't re-derive

Read `gap_packet.json` first. Every `open` gap is a claim to be tested. Do not start a fresh inventory — that throws away the status history and produces new ids for old gaps.

Answering "what's left to do?" alone stops here: filter `status == "open"` and report. That's a file read, not an investigation. Only continue to step 2 if the user wants accuracy re-verified.

### 2. Re-verify each open gap's evidence

For each `open` gap, check its evidence anchors still exist and still demonstrate absence:
- Symbol present, gap still absent → stays `open`.
- Symbol present, feature now exists → `closed`, `closed_by: "recheck"`.
- Symbol gone / file gone / surrounding code rewritten → the finding can no longer be verified. Mark `superseded`. If the gap still holds under the new structure, add a NEW gap with a new `id` and `supersedes` pointing at the old one.
- Premise was wrong (the capability existed elsewhere all along, or the evidence was misread) → `superseded`, and say so plainly in the report. A wrong finding retracted is worth more than a wrong finding left standing.

Every transition out of `open` writes `superseded_reason` (for supersedes) and `closed_by`. If the fix was attempted and then reverted, say that — "implemented, produced N false positives and zero true findings, reverted" is the most useful sentence a recheck can leave behind.

### 3. Scan for gaps introduced since

Only after step 2. Run the lenses (§2) against what changed since `scanned_at` — new routes, new models, new half-built work. New findings get new ids, `status: "open"`, `first_seen_at` set to today.

### 4. Report the deltas, not the whole list

```
# Gap-Scan Recheck: [target]
Last scanned: [date] · Rechecked: [date]

## Still open (N)
[one line each — name + why still valid]

## Closed since last scan (N)
[one line each — what was built]

## Superseded (N)
[one line each — why the finding no longer holds, and whether a replacement gap was filed]

## New gaps found (N)
[full finding format for each]

## Start here
[same rules as a fresh scan — ONE gap, first action, why]
```

Bump `last_rechecked_at`. Write the packet back — recheck always persists, or the next recheck starts from stale data again.

## Boundaries — what gap-scan never does

- Never reports something that exists but is broken, slow, or insecure → code-audit
- Never critiques the usability of what exists → ux-audit
- Never evaluates persuasion or conversion of existing pages → conversion-audit
- Never proposes productizing existing internal assets → that's opportunity-mining (WWBD), a different question
- Never recommends features with no evidence anchor ("add AI", "add a mobile app") — if the map doesn't imply it, it doesn't ship in the report
- Never answers "what's left?" by re-investigating the repo when a packet exists → read the packet's `status` fields
- Never ends a report without `## Start here` — a list with no first move is an unfinished report

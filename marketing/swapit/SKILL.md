---
name: swapit
category: commerce
version: 0.4.0
description: |
  Stateful, local-first household toxics inventory + swap engine. Identify the items in
  a home that carry endocrine disruptors and persistent chemicals (BPA/BPS, phthalates,
  PFAS/PTFE, parabens, flame retardants, VOCs, microplastics), score each by *real*
  exposure (severity x presence x how it's used x condition), and track the swap to a
  safer alternative from "flagged" -> "sourced" -> "swapped". Ships a grounded, cited
  knowledge graph of ~20 hazards, ~40 item-classes, and ~40 alternatives. Hands sourcing
  off to the `procurer` skill. The skill's state is the source of truth — the agent is the app.
when_to_use: |
  Invoke whenever the user wants to find, prioritize, or replace household items that may
  contain harmful chemicals. Common triggers:
    - "What in my kitchen/bathroom/house has BPA / PFAS / phthalates / microplastics?"
    - "Help me get rid of plastics / endocrine disruptors at home."
    - "Is my <non-stick pan / shower curtain / water bottle / mattress> a problem?"
    - "What should I swap first?" / "Build me a non-toxic swap plan."
    - "Track my swaps" / "what have I replaced and what's left?"
    - User lists items they own and implicitly wants an exposure assessment.
  Use proactively when a user describes a health/lifestyle decluttering or detox goal —
  build the inventory and the ranked swap-first list so they can act.
not_for: |
  - Acute poisoning / medical emergencies -> direct to poison control / a clinician.
  - Where to buy a replacement + what it costs -> hand off to the `procurer` skill
    (`swapit procure <item>` builds the brief).
  - General health tracking (sleep, labs, fitness) -> use the `health` skill.
  - Regulatory/legal compliance advice -> out of scope; the knowledge graph is consumer
    guidance grounded in public-health sources, not legal counsel.
author: broomva
license: MIT
metadata:
  homepage: "https://broomva.tech/skills/swapit"
tags:
  - health
  - household
  - toxics
  - endocrine-disruptors
  - inventory
  - stateful
  - local-first
trigger_keywords:
  - swapit, toxics inventory, what has bpa, pfas in my kitchen, microplastics at home
  - non-toxic swap, endocrine disruptors, phthalates, get rid of plastics
  - is my non-stick pan safe, shower curtain offgassing, swap-first list
  - household detox, what should i swap first, track my swaps
compounding:
  - procurer
  - bookkeeping
  - health
  - content-creation
---

# swapit — household toxics inventory + swap engine

## What this skill is

`swapit` turns a vague worry ("there's probably a lot of plastic and BPA in my house") into
a **concrete, prioritized, trackable plan**. It is stateful: your household inventory lives on
disk and persists across sessions. It is local-first: zero paid services, nothing leaves your
device unless you explicitly opt into the (M3) commons.

One pass produces:
1. An **inventory** of the items you own, each tagged with its generic *item-class*.
2. A **risk score** per item that reflects *actual exposure* — a scratched non-stick pan used
   daily at high heat ranks far above an unopened plastic bin in the garage.
3. A **ranked "swap-first" list** — the 5% of changes that cut the most exposure.
4. **Swap tracking** — chosen alternative, procurement status, checklist, bookmarks.
5. A shareable **HTML report** (and, in M2, a live dashboard at `swapit serve`).

## The three realms (and the privacy invariant)

| Realm | What it holds | Sharing |
|---|---|---|
| **1 · Knowledge** | hazards → item-classes → alternatives (generic, cited facts) | shareable; cached + (M3) commons-synced |
| **2 · Inventory** | your items, rooms, quantities, brands, photos, swaps, bookmarks | **PRIVATE — never leaves the device** |
| **3 · Commons** (M3) | anonymized contributions enriching the shared knowledge graph | opt-in, reviewed, generic facts only |

> **Privacy invariant (binding):** Realm-2 inventory (items, rooms, quantities, brands, photos,
> purchase info, location) **never** crosses the sync boundary. Only Realm-1 generic facts are
> shareable, via explicit opt-in + a reviewable `swapit sync --dry-run`. Enforced by an allowlist
> serializer (`scripts/anonymize.py`) on the client **and** a backstop on the commons server, plus
> fuzz tests asserting every real inventory item is rejected by the gate. Forbidden-field list:
> `anonymize.CONTRIBUTION_FORBIDDEN` (the inventory-structural subset of `state.PRIVATE_FIELDS`).

## Data model

State lives at `~/.config/swapit/` (override with `$SWAPIT_HOME`; honors `$XDG_CONFIG_HOME`).

```
~/.config/swapit/
├── knowledge/   hazards.jsonl · item-classes.jsonl · alternatives.jsonl · products.jsonl · procurement.jsonl
├── inventory/   events.jsonl(append-only audit) · items.json · swaps.json · rooms.json · bookmarks.json
├── contributions/ queue.jsonl   (M3)
├── sync/        config.json · sync-log.jsonl   (M3)
└── photos/
```

**Node schemas** (see `seed/*.jsonl` for the full, cited dataset):
- **hazard** — `id · name · aliases · class · mechanism · exposure_routes · regulatory · severity(0-3) · evidence_strength · sources`
- **item_class** — `id · name · category · description · hazards[]{hazard_id, presence_likelihood, rationale} · detection_hints · sources`
- **alternative** — `id · name · replaces[] · material · rationale · tradeoffs · caveats · avoids_hazards · residual_concerns · sources`
- **procurement_option** (where-to-buy, public) — `id · alternative · item_class · retailer · region(ISO-3166-1 a2) · area · url · price_min · price_max · currency · as_of · availability · confidence · corroboration_count`
- **item** (private) — `id · name · item_class · room · quantity · brand · condition · usage{frequency, food_contact, heat, child_contact} · status · notes · photos`
- **swap** (private) — `id · item_id · chosen_alternative · procurement{status, cost, vendor} · checklist[] · bookmarks[]`

## Risk model

```
risk = severity × presence_likelihood × evidence × exposure_relevance × frequency × condition
```
- **exposure_relevance** activates a hazard's route against how the item is *used* (food-contact +
  heat maxes out an ingestion/food-contact-heat hazard; dermal matters for personal care; inhalation
  for cleaning/furniture; child-contact amplifies).
- Item score = scaled sum of per-hazard risk → band **high / medium / low**.
- This is the *prioritization* intelligence — the analogue of procurer's "dominant failure mode":
  fix the few items that drive most of the exposure first, not a guilt list of everything plastic.

## Modes

| Mode | What it does |
|---|---|
| `init` | create state + load the seed knowledge graph |
| `add` | add a household item (name, class, room, condition, usage) → prints its assessment |
| `assess` | assess an item or an ad-hoc item-class → hazards + risk + ranked alternatives |
| `list` | list inventory, filter by `--room/--band/--status/--class/--hazard`, sort by risk |
| `swap` | create/update a swap plan: choose alternative, set status, checklist, bookmark, cost |
| `score` | household exposure summary + the swap-first ranking |
| `report` | generate the self-contained HTML report (Category-C) |
| `procure` | procurer handoff brief + **known where-to-buy offers** for the swap target (filter by `--region`); record a found offer (`--retailer`/`--url`/`--price-*`) to the public commons |
| `knowledge` | browse/search the knowledge graph (`list`/`search`/`show`) |
| `rooms` | list/add rooms |
| `selfheal` | validate knowledge edges + inventory refs + grounding; exit non-zero on errors |
| `serve` | **live local dashboard** at `http://127.0.0.1:8731` — kanban board, checklist, bookmarks, status; every click writes back to state |
| `contribute` | queue an anonymized fact — `product` / `hazard` (item-class→hazard) / `alternative` / `procurement` (public where-to-buy offer) / `item-class` (new taxonomy node); applied locally + gated for the commons |
| `sync` | push the contribution queue + pull community knowledge (opt-in); `--dry-run` previews exactly what would be sent; `--configure` sets the endpoint |

### Typical flow
```bash
swapit init
swapit add --name "Old Teflon pan" --class nonstick-cookware --room kitchen \
           --condition scratched --frequency daily --food-contact --heat
swapit score                      # what to swap first
swapit swap itm_xxxx --to cast-iron-skillet --status sourcing --add-task "buy 10in skillet"
swapit procure itm_xxxx           # -> hand the brief to the `procurer` skill
swapit report --open              # shareable HTML
```

## Compounding with other skills

- **`procurer`** — `swapit procure <item>` builds the need ("replace 3 polycarbonate bottles with
  glass/steel") and the ready procurer prompt; procurer returns cited sources + a budget envelope.
- **`bookkeeping` (P6)** — a novel, durable hazard/product finding (e.g. a newly characterized
  item-class) is filed proactively into `research/entities/` and can later flow to the commons.
- **`health`** — personal exposure context. **`content-creation`** — educational posts from the graph.

## Grounding discipline

The seed knowledge cites only authoritative bodies (NIEHS, ATSDR/CDC, US EPA, US FDA, ECHA/EU REACH,
CA OEHHA Prop 65, WHO, EWG). Every record carries ≥1 source; `verified: false` marks these as
reference-grade (not freshly fetched) — run a sourced pass (or the commons) to refresh. `selfheal`
fails if any node loses its citation. This is consumer guidance grounded in public-health science,
**not** medical or legal advice.

## Resources

- `scripts/swapit.py` — CLI entrypoint + command handlers
- `scripts/state.py` — two-realm state layer (`PRIVATE_FIELDS` defines the sync boundary)
- `scripts/ops.py` — the single state-mutation write path (shared by CLI + dashboard)
- `scripts/knowledge.py` — knowledge graph load + edge resolution
- `scripts/risk.py` — exposure-risk scoring engine
- `scripts/report.py` — self-contained HTML report generator (Category-C)
- `scripts/server.py` — `swapit serve` live dashboard (stdlib http.server, localhost-only)
- `scripts/anonymize.py` — the privacy gate: allowlist fact builders + the forbidden-field scan
- `scripts/sync.py` — commons sync client (queue, `--dry-run` preview, push/pull, merge)
- `scripts/selfheal.py` — integrity validator
- `templates/dashboard.html` — the live dashboard (inline CSS/JS, Category-C)
- `commons/` — the networked commons reference server (FastAPI + SQLite; deploy gated)
- `seed/{hazards,item-classes,alternatives}.jsonl` — grounded starter knowledge
- `tests/` — risk, knowledge, self-heal, CLI, privacy/anonymize, sync, report, and server tests

## Collaboration (the commons)

Contributions are **generic facts only** — `swapit contribute product|hazard|alternative|procurement|item-class`
builds an anonymized fact (a public product→item-class mapping, a hazard-edge correction, an
alternative, a **where-to-buy offer**, or a **new taxonomy node**), applies it locally, and queues it.
`swapit sync --dry-run` shows *exactly* what would be sent; `swapit sync` pushes the queue and pulls
community knowledge (opt-in, after `--configure`). Identical facts from different users **corroborate**
(content-addressed) rather than duplicate; the commons serves a fact once **two distinct contributors
corroborate it** (`corroboration >= 2`) — moderation is corroboration-gated, *not* confidence-gated,
because `confidence` is caller-supplied and a lone submitter could otherwise self-approve. The privacy
invariant is enforced on **both** sides (client `anonymize` gate + server backstop) — inventory never crosses.

### Where-to-buy (procurement) commons

A `procurement_option` fact is a public offer: a safer `alternative` sold by a `retailer` in a
`region` (ISO-3166-1 alpha-2), with optional `url`, `price_min`/`price_max` + `currency` + `as_of`,
`area`, and `availability`. It is content-addressed on **`(alternative, retailer, region)`** — the
same offer corroborates across users; a different region is a different fact (the geographic scale
axis). Price/url/area are refinable market data: a corroboration with a strictly newer `as_of`
**freshens the price forward**, never regressing fresher data. The privacy seam is sharp — the public
offer uses `retailer` + `price_*` and **never** the private `vendor`/`cost` (where *you* bought and
what *you* paid stay in Realm 2). `swapit procure <item> --region <CC>` surfaces known offers and
records new ones you find — growing an open, detailed, geo-scoped dataset anyone can use.

## Roadmap

- **M1 (shipped, 0.1.0)** — data model, seed knowledge, CLI, risk engine, static HTML report, self-heal.
- **M2 (shipped, 0.2.0)** — `swapit serve`: live local dashboard with read/write back to state.
- **M3 (0.3.0)** — anonymized collaboration + networked commons (`commons/`, FastAPI + SQLite).
  Privacy invariant enforced by allowlist serialization + fuzz tests on both client and server.
- **M4 (this release, 0.4.0)** — **geo-scaled procurement commons + taxonomy growth**: the
  `procurement_option` (public where-to-buy, keyed by `(alternative, retailer, region)`, forward-only
  price freshening) and `item_class` (corroboration-gated taxonomy growth) fact kinds; `procure`
  surfaces + records offers; seed offers across US/CO/DE/GB; cross-language hash parity locked by
  pinned vectors. **Live deploy to broomva.tech infra is gated on explicit go** (creds/DNS); the
  skill is fully functional offline without it.

---
name: investor-materials
description: Create and update pitch decks, one-pagers, investor memos, accelerator applications, financial models, and fundraising materials that stay internally consistent across every asset. Use when the user needs investor-facing documents, projections, use-of-funds tables, or milestone plans. Do NOT use for the underlying market study (market-research), for outbound investor emails (investor-outreach), or for customer-facing launch copy (marketing-campaign).
origin: ECC
---

# Investor Materials

Build investor-facing materials that are consistent, credible, and easy to defend.

## When to use

- creating or revising a pitch deck
- writing an investor memo or one-pager
- building a financial model, milestone plan, or use-of-funds table
- answering accelerator or incubator application questions
- aligning multiple fundraising docs around one source of truth

**When NOT to use:**

- the ask is market sizing or competitor intelligence — that is `market-research`, which feeds
  this skill
- the ask is the outreach email — that is `investor-outreach`
- the canonical numbers do not exist or conflict. Drafting on top of conflicting numbers
  guarantees a partner meeting where two documents disagree; stop and resolve first

## Inputs

**The golden rule: all investor materials must agree with each other.** Create or confirm one
fact sheet before writing anything — **conflicting numbers = stop and resolve, never draft over
the conflict**:

1. **Traction metrics** — with the system they came from, not recollection. SkyyRose product,
   price, and SKU-count facts come from
   `wordpress-theme/skyyrose-flagship/data/skyyrose-catalog.csv`; live order/revenue facts come
   from the WooCommerce REST API (`/wp-json/wc/v3`, BasicAuth with keys in `.env.wordpress`) —
   the MCP `wc_*` tools have a broken auth username and return `invalid_username`.
2. **Pricing and revenue assumptions**, each stated explicitly.
3. **Raise size and instrument.**
4. **Use of funds** — categories and percentages that sum to 100.
5. **Team bios and titles.**
6. **Milestones and timelines.**

Write the fact sheet to a real file (e.g. `fact-sheet.md`). Every downstream asset is checked
against it mechanically, so it must exist as text, not as context.

## Procedure

1. Inventory the canonical facts into the fact sheet. Anything unknown is written as
   `TBD (assumption owner: <name>)`, never as a confident number.
2. Identify missing assumptions and mark which of them the story depends on.
3. Choose the asset type and draft it with the logic visible, not buried:
   - **Pitch deck** — company + wedge · problem · solution · product/demo · market · business
     model · traction · team · competition/differentiation · ask · use of funds + milestones ·
     appendix. For a web-native deck, pair with `frontend-slides`.
   - **One-pager / memo** — what the company does in one clean sentence · why now · traction and
     proof points early · a precise ask · claims easy to verify.
   - **Financial model** — explicit assumptions · bear/base/bull where useful · layer-by-layer
     revenue logic · milestone-linked spending · sensitivity analysis where the decision hinges
     on an assumption.
   - **Accelerator application** — answer the exact question asked · lead with traction, insight,
     team advantage · no puffery · metrics identical to the deck and model.
4. Cross-check every number in the draft against the fact sheet — run the checks below, do not
   eyeball it.
5. Re-run all checks after any fact-sheet edit. One changed metric invalidates every asset that
   quoted it.

# Verification

Every check runs against files, so it can return "no". A check that errors on a missing file
exits 2 — a dead gate, not a pass (bug-230); fix the path and re-run before reading the result.

1. **Use of funds sums to exactly 100** — the arithmetic a partner checks first:

```bash
python3 -c "import csv,sys; rows=list(csv.DictReader(open('use-of-funds.csv'))); s=sum(float(r['pct']) for r in rows); print('sum', s); sys.exit(0 if s==100 else 1)"
```

   **PASS:** prints `sum 100.0`, exit 0. Any other total is a defect in the document, not a
   rounding footnote. `[repro]`

2. **Every number in every asset exists in the fact sheet** — the golden rule, mechanised:

```bash
for n in $(grep -ohE '\$[0-9][0-9,.]*[KMkm]?|[0-9]+ (SKUs|customers|users)' deck.md memo.md | sort -u | tr ' ' '_'); do
  v=$(echo "$n" | tr '_' ' ')
  grep -qF "$v" fact-sheet.md || echo "MISSING from fact sheet: $v"
done
```

   **PASS:** no `MISSING` lines. Each one is a number that exists in an investor-facing document
   and nowhere in the source of truth — resolve it in the fact sheet or delete it. `[repro]`

3. **Traction claims match the live system, not memory** — for SkyyRose SKU counts:

```bash
python3 -c "import csv; print(sum(1 for _ in csv.DictReader(open('wordpress-theme/skyyrose-flagship/data/skyyrose-catalog.csv'))), 'catalog rows')"
```

   **PASS:** the printed count equals the SKU count claimed in the deck. A mismatch means the
   deck is quoting a remembered number. `[repo]` — and note the scope: a catalog row is not proof
   the product is live on the storefront. A "live on skyyrose.co" claim needs its own `[live]`
   probe (`curl -s "https://skyyrose.co/shop/?cb=$(date +%s)"`), and without it the claim is
   downgraded, not asserted (bug-287).

Check 1 was proven able to fail before being trusted (rule 3) — see the worked example.
**A SKIP is not a PASS:** whether the story is defensible in a partner meeting is a human
judgment. State it as open and name who closes it; the mechanical greens only prove the numbers
are internally consistent, not that the narrative holds.

## Worked example

Real run, 2026-07-28, using files in the session scratchpad.

```bash
$ python3 -c "import csv,sys; rows=list(csv.DictReader(open('use-of-funds.csv'))); s=sum(float(r['pct']) for r in rows); print('sum', s); sys.exit(0 if s==100 else 1)" && echo "PASS: allocations sum to 100"
sum 100.0
PASS: allocations sum to 100
```

Allocation set: Inventory & production 40 · Paid acquisition 25 · Team 20 · Ops & tooling 10 ·
Buffer 5. The gate was proven red by adding 5 points to the total in the same run — it printed
`sum=105` and exited non-zero `[repro]`.

Consistency check across `memo.md` (raising `$500K` on a SAFE, `33 SKUs` live) against
`fact-sheet.md`:

```bash
$ for n in $(grep -ohE '\$[0-9][0-9,.]*[KMkm]?|[0-9]+ SKUs' memo.md | sort -u | tr ' ' '_'); do v=$(echo "$n" | tr '_' ' '); grep -qF "$v" fact-sheet.md || echo "MISSING from fact sheet: $v"; done; echo "done exit=$?"
done exit=0
```

No `MISSING` lines — every figure in the memo traces to the fact sheet `[repro]`. Scope note on
the `33 SKUs` figure: the fact sheet records it as catalog rows `[repo]`. Any deck line claiming
they are all purchasable on skyyrose.co needs its own `[live]` probe before it ships.

## Failure modes

| Failure | What it looks like | Rule |
|---|---|---|
| Documents disagree | deck says 40 customers, memo says 35 | The golden rule. Resolve in the fact sheet, then re-run check 2 on every asset |
| Use of funds does not sum | allocations total 105% | Check 1. It is the first thing a partner adds up |
| Metric quoted from memory | SKU or revenue number with no system behind it | bug-096 shape. Catalog CSV / WC REST are the SOT; plausible ≠ sourced |
| Repo → live scope jump | "33 products live on the site" proven only by a CSV | bug-287. `[repo]` does not cover a `[live]` claim. Probe or downgrade the wording |
| Broken tooling read as truth | WC MCP `wc_get_products` returns `invalid_username` / empty and is treated as "no orders" | bug-230 fail-open. The MCP auth path is known broken — use direct BasicAuth REST with `.env.wordpress` keys |
| Fuzzy market sizing | TAM with no stated assumptions | Every leap in logic gets an explicit assumption line; source the inputs via `market-research` |
| Inflated certainty | fragile assumptions written as facts | Show the assumption, show the sensitivity. Label inference as inference |
| Stale asset after a fact change | one metric updated, three docs still quote the old one | Re-run all checks after any fact-sheet edit |
| Mechanical greens read as a full pass | "materials verified" with no defensibility read | A SKIP is not a PASS — name the open judgment and its owner |

## Related skills

`market-research` (sizing, competitors, investor diligence) ·
`skyyrose-market:investor-outreach` (the emails; plugin-namespaced — verified on disk at
`~/.claude/plugins/cache/skyyrose-suite/skyyrose-market/1.0.0/skills/`, **not** a bare
`investor-outreach` in `.claude/skills/`) · `frontend-slides` (web-native deck)

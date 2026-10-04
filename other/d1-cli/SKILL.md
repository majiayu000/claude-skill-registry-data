---
name: d1-cli
version: 0.9.0
source: https://github.com/broomva/skills
description: Shop Tiendas D1 (Colombia, d1.com.co) from the command line — search the catalogue, resolve your nearest physical store, price a basket against that store's real stock, and quote delivery. D1 runs VTEX IO (account `d1tiendas`), so this drives its public storefront API with no admin key at all — catalogue and cart work fully anonymously, and a one-time emailed code unlocks order history. Handles the two traps that make naive D1 automation wrong — availability is regionalized (an unregioned query reports a national catalogue nobody can actually buy from) and prices arrive in two different units (search reports whole pesos, checkout reports hundredths, a silent 100x). Builds and prices baskets; it deliberately cannot pay, handing a checkout URL to a human instead. USE WHEN the user wants to find D1 products or prices, check whether D1 delivers somewhere, build or cost a D1 grocery basket, compare D1 items, or review their D1 orders. NOT FOR other Colombian retailers (Éxito, Jumbo, Ara, Alkosto), and not for completing a payment.
author: broomva
license: MIT
tags: [colombia, d1, tiendas-d1, groceries, vtex, vtex-io, ecommerce, cli, retail, shopping, intelligent-search, regionalization]
---

# d1-cli — Tiendas D1 from the command line

D1 is Colombia's largest hard-discount grocery chain. Its storefront runs
**VTEX IO** (account `d1tiendas`), which means the site's own public API is the
integration surface — no scraping, no admin credentials.

## Invoke

```bash
cd skills/commerce/d1-cli

# 1. Resolve your delivery point FIRST — everything else depends on it
bun run src/cli.ts region --lat 4.6486 --lng=-74.0628

# 2. Then search: prices and stock are now your store's, not the country's
bun run src/cli.ts search leche entera --count 5
bun run src/cli.ts search --facets category-1/lacteos-y-huevos --sort price:asc

# 3. Price a basket without touching your cart
bun run src/cli.ts quote 262:2 892:1

# 3b. Or let a budget decide what goes in it — terms, not SKUs
bun run src/cli.ts basket --budget 30000 arroz leche aceite huevos

# 4. Or build a real one, then hand off to a human to pay
bun run src/cli.ts cart add 262 --qty 2
bun run src/cli.ts cart deliver-to
bun run src/cli.ts cart checkout      # prints a URL; does not pay
```

Add `--json` to any command for agent-readable output. **Exit codes are a
contract, and this list is the only copy of it:**

| code | meaning | retry? |
|---|---|---|
| `0` | it worked | — |
| `1` | D1 refused or was unreachable — undeliverable point, unavailable or unknown SKU, outage | yes, may help |
| `2` | the command was called wrong | never helps |
| `3` | it worked and the answer is "none" (`substitute`, `basket`) | never helps |

An agent that cannot separate those either retries a typo forever or gives up
on a transient outage. `3` exists because an empty category is neither.

Note that `cart add` **sets** the line to `--qty`; it does not add to it. That
is D1's own semantics, verified live.

## The two things that make naive D1 automation wrong

**Availability is regionalized.** Query the catalogue with no region and D1
answers from the national catalogue, reporting a comfortable 10,000 units
against the notional seller `1`. Put the same SKU through a checkout simulation
for a real address and it comes back `withoutStock`, because the physical store
that would ship it does not carry it. Always `d1 region` first; the CLI warns
in plain text whenever it is showing you national prices.

Resolving a region is also the single least guessable part of the API: the
coordinates go in as **`geoCoordinates={lon};{lat}` — semicolon-separated,
longitude first**. A comma, which is what VTEX's own JSON bodies use for the
same pair, is rejected with `CHK0119` ("addresses must have a postal code or
geocoordinates") — a message that reads like the parameter is missing rather
than malformed. `test/region.test.ts` pins this so a cleanup cannot undo it.

**Prices arrive in two units.** For SKU 262 (Leche Entera Latti 900 ml, COP
3,500 on the shelf):

| API | Field | Value | Unit |
|---|---|---|---|
| intelligent-search | `Price` | `3500` | whole pesos |
| catalog_system | `Price` | `3500.0` | whole pesos |
| checkout orderForm | `sellingPrice` | `350000` | hundredths |

Neither labels its unit. `catalog.ts` normalizes everything to hundredths at
the boundary so the rest of the code has exactly one unit, and a test asserts a
search-sourced price renders identically to a checkout-sourced one.

## What it will not do

`d1` builds and prices baskets. It does not pay. `d1 cart checkout` prints the
URL where a human reviews the total and completes payment.

That boundary is checked in two places from one list (`src/endpoints.ts`):
**at runtime**, `D1Client.request` refuses any request whose resolved URL is not D1's own origin
plus one of 18 approved paths before the request leaves the process; **statically**,
`test/safety.test.ts` fails if any `/api/` literal anywhere under `src/` is
unapproved. Adding an endpoint — payment or otherwise — fails until it is
listed, so the decision gets made rather than defaulted into.

The runtime half is load-bearing and was added after review showed a static scan
is not enough: `--facets '../../../..'` resolved out of the search endpoint onto
order settlement while every source literal remained approved.

Stated precisely, because earlier versions of this file overclaimed: nothing
here stops a committer with write access from editing the allowlist. No in-repo
test can.

The only credential it stores is a storefront session token — the same thing a
signed-in browser holds, scoped to its owner's own orders and cart — written to
`~/.config/d1-cli/session.json` with mode `0600`. No VTEX admin appKey/appToken
is read anywhere. Sign-in is by one-time emailed code; password authentication
is deliberately not implemented.

## The checkout gate — always end here

**Finish every basket with `d1 cart checkout` and act on its exit code.** Not as
a formality: it is the only command that re-checks the whole cart against D1 as
it is *now*, and carts go stale in ways nothing else surfaces.

```
0  every line deliverable — the URL is safe to hand over
1  at least one line CANNOT be delivered; the URL is printed but the cart is broken
2  the command was called wrong
```

This exists because each of these happened on a real basket:

- **A line sold out overnight.** `PAN ARTESANAL INTEGRAL` went `no tiene
  inventario` hours after it was added. The cart still rendered, still had a
  total — a total that was silently 6.490 light, because the dead line had
  dropped out of it.
- **An address change stranded every line.** Nine items came back
  `cannotBeDelivered` while each still carried a valid SLA and the cart still
  showed a payable total.
- **Shipping was under-reported 12x** by a per-line allocation that looked like
  a total.

In all three the cart *looked* fine. A quote taken earlier in a session is not
evidence about the cart now, so never hand over a checkout URL you obtained
before the last mutation — re-run the gate.

When it returns 1, `--json` gives `undeliverable[]` naming the lines, and
`readyToCheckout: false`. Remove or replace those lines and run it again.

## Replacing a line D1 cannot supply

```bash
d1 substitute 192 --limit 5        # ranks in-stock products from the same category
```

Exit 0 means there is something to propose; **3 means there is not** — one of
the two commands that use `3`, alongside `d1 basket`.

Three, not one, and the distinction is the point: `1` means *"D1 refused, or
could not be reached"* everywhere else in this CLI, and invites a retry. An
empty category never becomes non-empty on retry, so an agent with a retry-on-1
policy would loop on it forever. Exit 0 with an empty list is the other wrong
answer — it reads as success and gets acted on.

Each candidate names **what changes**: brand, pack size, `$/kg` or `$/L`, pack
price, and any Ley 2120 warning gained or lost. That is the output, not the
score. A `-12%` per litre for the same 900 ml and the same label is a different
proposition from one that arrives with `Exceso en Azúcares` attached, and only
the deltas tell them apart.

**Propose it; do not take it.** `substitute` never writes — it prints the
`d1 cart add` for a human to approve. This is not caution for its own sake: the
customer twice preferred a line *removed* over a wrong substitute, said so
explicitly, and was right both times. Present the candidates and the trade-offs;
let the person decide, and be willing to drop the line.

Three things it will tell you that are worth reading:

- **"This is still in stock at your store."** Availability is per-store, so a
  line that failed elsewhere may be fine here. Check before replacing anything.
  With no `--lat/--lng` it says so instead of guessing — there is no store to
  make a per-store claim about.
- **"widened to level 2 of 3"** — the leaf category had nothing in stock, so the
  suggestions come from a broader aisle and are correspondingly looser.
- **"only N were compared"** — the category is bigger than one page. Raise
  `--count`. This prints on the empty result too, because *"nothing here is in
  stock"* asserted over a partial sweep needs the caveat more, not less.

## Finding things when the ask is vague

For "we need rice" rather than "buy SKU 1092", two axes matter and neither is
the default:

**Rank by unit price, not pack price.** `--sort per-unit` uses the PUM data
Colombian law requires D1 to publish. The two rankings genuinely disagree:
`ARROZ ESTÁNDAR 500 GRS` is the cheapest *pack* at $1.550 and costs $3.100/kg,
while the best value in the same results is $2.775/kg — in a $5.550 bag that
does not appear anywhere in the pack-price top five. Ranking by pack price gives
a worse answer while looking right.

Because D1's search cannot sort on this, `--sort per-unit` orders **the page you
fetched**, not the whole result set. Raise `--count` (max 50) to widen it. The
output says so rather than implying a superlative it cannot support, and names
how many results publish no size and so cannot be compared at all.

**A multipack's declared size is the pack, not one item — do not "correct" it.**
A census of all 1,600 products found that among name-matchable multipacks, 44
of the 46 where D1 says enough to decide declare the pack total. Parsing `N UN`
out of a product name and multiplying would corrupt those 44 to fix 2. The count
in a name is not evidence about what the PUM means.

`resolvePackSize` therefore reads descriptions rather than names. Across all
1,548 products carrying a PUM it acts on the 10 whose description states both a
per-item size and a count: three are corrected (SKU 718, 510, 1008), seven are
confirmed as already stating the pack, and everything else is left as declared.

**Read the warning labels.** Products carry Colombia's front-of-pack warnings
(`Exceso en Azúcares`, `Exceso en sodio`, `Exceso en grasas saturadas`,
`Exceso en grasas trans`, `Contiene Edulcorantes`) in `warnings[]` under
`--json`. Coverage is partial — roughly 70–90% by category — so absence means
"not declared", never "safe".

Then narrow with `d1 facets <query>` (category, brand, sub-category with counts)
before paging: search caps at 50 pages, so a wide query is better cut by facet
than walked through.

## Commands

| Command | What it does |
|---|---|
| `region --lat --lng` | resolve and remember the delivery point |
| `search <query>` | find products (`--facets --sort --count --page --available`) |
| `suggest <partial>` · `trending` | autocomplete · what Colombia is searching |
| `categories` · `facets [query]` | department tree · filters for a query |
| `substitute <sku>` | what to buy instead, and what changes (`--limit --count`) |
| `quote <sku>[:qty]...` | price a basket, no cart mutation |
| `cart [show\|add\|set\|clear\|deliver-to\|checkout]` | build a basket |
| `login --email` / `--from-cookie` · `whoami` · `logout` | account |
| `orders` · `order <id>` | order history (detail is redacted to an allowlist; `--raw` opts in) |
| `stores near` | D1 shops near a point — locations only, D1 offers no collection |

## Tests

```bash
bun test        # money units, the semicolon gotcha, quantity-in-quote,
                # unknown-SKU vacuity, cart normalization, order redaction, and
                # the endpoint allowlist that bounds the payment surface
bun run lint && bun run typecheck
```

Exit codes are a contract, not decoration — the table under **Invoke** above is
the single copy of it.

See `README.md` for the full endpoint map, the shipping-tier behaviour, and
what the public API will not give you.

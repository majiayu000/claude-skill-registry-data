---
name: seo-growth
description: >
  Use when deciding WHERE to point SEO effort, not how to write a page. Triggers: a new
  site or brand with no rankings and no authority ("cold start", "starting from zero",
  "nobody knows us"), deciding what to double down on, a page or cluster that ranks but
  earns nothing, hunting emerging or newly-coined keywords before competitors arrive,
  "should we build a cluster or one page", "what do we write next", "we get impressions
  but no clicks", "our traffic plateaued despite publishing", whether to chase a head
  term at all, or turning any of it into recurring automation. Also use when asked why
  an SEO effort stalled despite consistent output. NOT for writing an article,
  keyword expansion mechanics, or auditing a single tactic for penalty risk.
---

# /seo-growth — first-party SEO growth method

**Core principle: the right move depends on whether you have data yet, and most bad SEO advice
is given to the wrong one of those two situations.** A site with no rankings and a site with a
breadwinner page need opposite behavior. Advice that ignores which you are in is how efforts
stall despite consistent output.

Distilled from two content properties run in production and the Search Console reads that
produced each rule. This is **a first-party method**: narrower than a general playbook, and
more trustworthy for it. Every rule traces to the failure or result behind it in
`references/why-these-rules.md`. Absolute traffic figures are withheld; the ratios and
thresholds are as observed.

## The two playbooks

| You are here if… | Playbook | Read |
|---|---|---|
| No rankings, no authority, <100 clicks/mo, possibly no content | **A — Cold start** | `references/cold-start.md` |
| GSC has real rows: something ranks, something earns clicks | **B — With data** | `references/with-data.md` |

**Diagnose per cluster, not per site.** A mature site opening a new territory is in Playbook A
for that territory and Playbook B everywhere else — and that combination is the strongest
position in the method.

**Playbook A in one line:** you cannot win an established term from zero authority, so hunt an
emerging one, ship ONE page, and let day-7 / day-21 decide whether it was real.

**Playbook B in one line:** your own GSC already knows which page shapes win for you — find the
breadwinner, extract the shape, diagnose whether it is position-limited or snippet-limited,
compound it, and protect it while you do.

## Read alongside either playbook

- **`references/emerging-terms.md`** — the hunt. The wedge in both playbooks, and the *only*
  thing that works in Playbook A. Where to look, in what order, and the seven gates a candidate
  must pass.
- **`references/measurement.md`** — which metric scores which situation, the four query
  families that never click, and the GSC traps that produce confident wrong conclusions.
- **`references/why-these-rules.md`** — the failure or result behind each rule.
- **`references/operationalize.md`** — turning either playbook into scheduled loops.

## Before advising anything: get three numbers

Pull a 28-day GSC window ending **3 days back** (GSC lags 2–3 days):

1. **Total clicks** — the scale, and which playbook you are in.
2. **Breadwinner share** — what % of clicks the single best page earns.
3. **Best non-brand position** — where you rank on something you don't own by name.

If these aren't available, say so and instrument first. Advising without them is guessing, and
it is the most common failure mode in this whole area.

## The five laws

1. **A low-authority domain can only win a term while competition is thin.** So a cold start
   doesn't "do SEO" — it hunts emerging terms. Validated on two separate terms, months apart.
2. **Score an emerging term on position, a mature one on clicks.** Backwards, and the metric
   tells you to quit the land-grab exactly as the ground becomes valuable — or leaves a page at
   0.53% CTR untouched for a month because its rank looked fine.
3. **Impressions are not progress.** The trap is a page drawing a very large impression base
   relative to the rest of the site at 0.2% CTR. It feels like traction and converts nothing.
   Rank work by click opportunity from *human* queries.
4. **Concentration is the goal, not the problem.** One page earning ~45% of clicks is healthy.
   Compound the winner before adding breadth.
5. **What you double down on is derived, not chosen.** Read your own GSC for which *shapes*
   win, then repeat the shape — not just the page.

## Quick reference

| Question | Short answer | Detail |
|---|---|---|
| Cold start, what now? | Instrument, then land ONE emerging term. Not a cluster. | cold-start |
| Cluster or one page? | One page until the term proves itself. Cluster after. | cold-start |
| How do I find emerging terms? | Your own saved stream → repo/release feeds → social listening → diff vs your pages | emerging-terms |
| Is this term worth it? | Seven gates; failing one drops it, and dropping is normal | emerging-terms |
| What do we double down on? | The page at ≥30% of clicks — and the archetype it belongs to | with-data |
| Ranks well, no clicks? | Screen the query mix first. Most such pages are not broken. | with-data, measurement |
| Traffic plateaued despite publishing | The cluster saturated. Open a new front, don't add pages to it. | with-data §7 |
| When do I stop land-grabbing? | Three computable numbers, never a vibe | measurement |
| How do I stop doing this by hand? | Four loop roles, never one loop | operationalize |

## Common mistakes

- **Advising before diagnosing.** Get the three numbers first.
- **Treating every low-CTR page as broken.** Four query families score ~zero clicks by design;
  one verified family ranked position 4.7–5.8 for **exactly 0 clicks** and was working
  perfectly.
- **Publishing on a cadence instead of on evidence.**
- **Diversifying away from a winner** because concentration feels risky.
- **Grounding research on your own pages and your own GSC.** A closed loop. It produces internal
  reshuffles that cannot move a term you don't yet own — one property lost its head term to
  page 2 this way while the answer sat unread in the owner's own bookmarks.
- **Counting a ship as an outcome.** A shipped page is a hypothesis until traffic verifies it.

## Scope honesty

Derived from B2B content SEO on low-to-mid authority domains. The two-playbook split, the
measurement discipline, and the emerging-term method transfer broadly. The specific archetypes
in `with-data.md` do not — they are one property's, and yours must be extracted from your own
data. Local, e-commerce, and YMYL were never tested here; say so rather than extrapolating.

## What this skill deliberately does not cover

- **Penalty risk / what Google punishes.** Read current third-party research before shipping at
  any scale — Lily Ray on algorithmic collapses, Kevin Indig on how AI systems select sources,
  Rand Fishkin and Amanda Natividad on zero-click. This skill is about *where to aim*, not about
  which tactics are dangerous, and the two are different questions.
- **Writing the page.** Use whatever content skill or process you already have. The bar this
  method assumes: genuine first-party substance, 15+ concrete specifics, and an answer a
  competitor cannot regenerate from the same prompt tomorrow.
- **Keyword expansion mechanics.** Once you know the territory, any keyword tool will widen it.

## Companion skills in this plugin

- **`new-loop`** — build the scheduled loop that runs either playbook on a cadence. See
  `references/operationalize.md` and `assets/seo-loop-template.md`.

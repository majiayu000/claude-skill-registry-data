---
name: ipl-portfolio
version: 1.0.0
description: Review and manage an IP portfolio across trademarks, patents, copyrights, and domains — docketing assets, deadlines, coverage gaps, and prune-vs-maintain decisions.
author: matrixx0070
tags: [portfolio, trademark, patent, docket, maintenance, deadlines, ip]
capabilities: []
---

## When to use

Use this to take stock of an IP portfolio: build or audit the docket, catch renewal and maintenance deadlines before they lapse, find coverage gaps against the product roadmap, and decide what to keep funding versus let go. Reach for it at annual budget time, before a fundraise or diligence, or when nobody can say what the company actually owns.

**Not for:** clearing a single new mark before adoption (see ipl-clearance), triaging a live infringement dispute (see ipl-infringement-triage), or capturing a new invention for filing (see ipl-invention-intake). This manages the standing portfolio, not one-off matters.

## Method

1. **Build the docket.** Inventory every asset: trademarks, patents, copyrights, domains — with jurisdiction, status, owner, and key dates.
2. **Map deadlines.** Flag upcoming maintenance/renewal windows (see Reference) and note lead times.
3. **Check coverage vs. roadmap.** Compare protected assets against products and markets planned; mark gaps (new geography, new class, unfiled core invention).
4. **Identify abandonment candidates.** Unused marks, non-core patents nearing a fee, defensive holdings with no product tie.
5. **Prune vs. maintain — Decision point.** Weigh each candidate's strategic value and licensing/enforcement potential against its upcoming cost; recommend maintain, prune, or hold-for-decision.
6. **Size the budget** across the next fee cycle.
7. **ATTORNEY-ESCALATION GATE.** You assist; you do not give legal opinions and this is not legal advice. Route to a licensed attorney/agent: any missed-deadline revival, any office action or pending rejection, and any file/abandon/enforce decision before it is acted on.

## Example

Portfolio review finds a US trademark hitting its year 5-6 window in two months with no §8 declaration filed and the branded product discontinued. Also: a utility patent with a 7.5-year fee due and no product using it. Recommendation: let the unused mark lapse (skip §8), flag the patent as a prune candidate pending a licensing check, and route the §8 timing and revival questions to counsel.

## Pitfalls

- **A docket without dates.** An asset list that omits maintenance windows guarantees a silent lapse.
- **Maintaining out of habit.** Paying fees on unused marks and off-roadmap patents drains the budget that should protect core assets.
- **Confusing filed with in-use.** US trademark rights need genuine use in commerce; a registration on a shelved product is vulnerable and often not worth renewing.
- **Missing the revival window.** A lapsed asset may be revivable only briefly — route it to counsel immediately, do not sit on it.

## Output format

```
PORTFOLIO REVIEW — <entity> | as of <date>
Docket:
  | Asset | Type | Jurisdiction | Status | Next deadline | Owner |
Coverage gaps vs roadmap:
Deadlines <next 12 mo>:
Prune candidates: <asset — rationale>
Maintain: <asset — rationale>
Budget estimate <cycle>:
Attorney escalation: <revival / office action / filing decision>
```

## Reference

Trademark maintenance (US): §8 declaration of continued use between years 5-6, then combined §8 & §9 renewal every 10 years; all require genuine use in commerce or the registration is vulnerable. Patent maintenance (US utility): fees at 3.5, 7.5, and 11.5 years, with a 20-year term measured from the filing date. Likelihood-of-confusion factors govern trademark strength assessment, and patentability bars (§§101/102/103/112) govern patent value — apply both when rating an asset worth maintaining.

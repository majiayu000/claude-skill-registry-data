---
name: win-loss-decoder
description: 'Turns closed-won and closed-lost deals into ranked, evidence-backed reasons (not rep-selected dropdowns) and routes each pattern to the team that can fix it. Use when: win loss analysis, why did we lose, why do we win, closed lost review, loss reasons, churned deals, competitive losses, buyer interviews.'
---

# Win-Loss Decoder (SIGNAL Framework)

CRM loss reasons are picked by the rep in ten seconds, and "price" wins every time. Win-Loss Decoder rebuilds the reason from what the buyer said and did, codes it against a fixed taxonomy, and ranks patterns by revenue so product, marketing, and sales each get the fixes that are theirs.

## Core Principle

**The buyer's words decide the code.** A reason without a quote or artifact from the buyer is logged as "unknown", not guessed.

## The SIGNAL Framework

| Letter | Step | The Question |
|---|---|---|
| **S** | Sample | Which deals, and is the sample balanced across wins, losses, segments, and reps? |
| **I** | Interview | What did the buyer say in a 20-minute conversation after the decision? |
| **G** | Group | Which taxonomy code does each reason map to? |
| **N** | Number | How much ARR sits behind each code, for wins and for losses? |
| **A** | Assign | Which team owns the fix for each code? |
| **L** | Loop | Did the fix change the rate of that code next quarter? |

## Reason Taxonomy

| Code | Covers | Default owner |
|---|---|---|
| VALUE | Buyer could not see enough return or urgency | Marketing |
| FIT | Missing capability, integration, or compliance need | Product |
| TRUST | Proof, references, security, or vendor-risk concerns | Marketing / Security |
| PROCESS | Lost the sales process: slow, no champion, wrong buyer | Sales |
| PRICE | Price or packaging, after the above are ruled out | Pricing |
| STATUS QUO | Buyer chose to do nothing | Marketing / Sales |

## Process

1. **Sample** - 15-30 recent decisions, at least one-third wins; exclude deals under the ACV floor
2. **Collect** - buyer interviews first, then call notes and emails; note the source of every reason
3. **Code** - up to two codes per deal (primary, secondary); PRICE only if VALUE and FIT are ruled out
4. **Weight** - sum ARR by code for wins and losses; compute `loss share - win share` per code
5. **Rank** - largest positive gap first; these are the reasons you lose more than you win on
6. **Route** - one fix per top code, with owner and the metric that will show it worked

## Output

Save to `outputs/win-loss-decoder-[period]-[YYYY-MM-DD].md`

| Artifact | Description |
|---|---|
| **Coded deal log** | Deal, outcome, codes, quoted evidence, source |
| **Pattern table** | Code, ARR won, ARR lost, gap |
| **Fix plan** | Top three codes with owner, action, and target metric |

## Tips

1. **Interview wins too** - you cannot tell a loss pattern from a market pattern without them
2. **Don't let reps interview their own deals** - buyers are more candid with a neutral party
3. **Rerun quarterly** - the Loop step is where the value compounds

## Pairs With

- **deal-xray** - PROCESS losses usually show missing proof earlier in the deal
- **competitive-battlecard** - competitor-named losses update the battlecard
- **position-lock** - persistent VALUE losses signal a positioning problem

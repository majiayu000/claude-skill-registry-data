---
name: deal-xray
description: 'Stress-tests a live opportunity by separating what the buyer has proven from what the rep believes, then scores deal risk and names the next action that would change the forecast. Use when: deal review, deal risk, pipeline review, forecast call, is this deal real, qualify this opportunity, stalled deal, commit or upside.'
---

# Deal X-Ray (PROVEN Framework)

Qualification checklists get filled in from memory and optimism. Deal X-Ray asks, for each element, what the buyer has *done* (not said) to prove it, and scores only the evidence. The output is a risk read and one concrete next step per gap, ready for a forecast call.

## Core Principle

**Score buyer actions, not rep opinions.** "They love it" is a belief; "their CFO joined the pricing call" is proof.

## The PROVEN Framework

| Letter | Element | Proof looks like |
|---|---|---|
| **P** | Pain | The buyer quantified the cost of the problem in their own words or numbers |
| **R** | Resources | Budget line named, or funding source confirmed by someone who controls it |
| **O** | Owner | An economic buyer has attended a meeting or replied in writing |
| **V** | Validation | Technical fit confirmed: pilot results, security review started, integration scoped |
| **E** | Exit criteria | Written mutual plan with dated steps to signature |
| **N** | No-decision risk | Buyer articulated why doing nothing is worse than acting now |

Evidence levels per element: **0** none · **1** rep belief · **2** buyer said it · **3** buyer did it (artifact exists).

**Proof score** = Σ levels / 18 × 100.

| Score | Call |
|---|---|
| 75+ | Commit candidate |
| 50-74 | Best case - close the named gaps first |
| <50 | Pipeline only - do not forecast |

## Process

1. **Gather** - CRM notes, call transcripts, emails, mutual plan
2. **Evidence pass** - for each PROVEN element, quote the artifact that proves it or mark the gap
3. **Score** - apply evidence levels; flag any element at 0 as the first gap to close
4. **Next action** - for each gap, one action that would move it up a level, with owner and date
5. **Forecast note** - two sentences: the call, and the single fact that would change it

## Output

Save to `outputs/deal-xray-[account]-[YYYY-MM-DD].md`

| Artifact | Description |
|---|---|
| **Evidence table** | Element, level, quoted proof or "gap" |
| **Proof score + call** | 0-100 with commit / best case / pipeline |
| **Gap plan** | Action, owner, date per gap |

## Tips

1. **Level 3 needs an artifact** - a calendar invite, a signed doc, a ticket number
2. **No-decision is the top competitor** - score it honestly
3. **Re-run weekly** - a score that hasn't moved in two weeks is a stalled deal

## Pairs With

- **competitive-battlecard** - when a named competitor appears in the evidence
- **revenue-forecasting** - consumes the proof score as a forecast input
- **enablement-forge** - recurring gaps across deals become coaching topics

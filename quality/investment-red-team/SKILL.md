---
name: investment-red-team
description: "Independently challenge and audit an investment recommendation, thesis, valuation, portfolio action, technical setup, fund comparison, crypto analysis, or leveraged-product scenario. Use when the user asks \"emin misin?\", requests a fresh analysis or second opinion, asks whether a better stock, fund, ETF, gold, crypto, cash, or other relevant alternative exists, is considering a concentrated or high-risk trade, or another finance skill delegates final review. Re-underwrite without anchoring to the prior pick, recompute key numbers, seek disconfirming evidence, compare same-asset and relevant cross-asset challengers plus doing nothing, and return an evidence-based verdict. Do not merely defend, restate, or self-score the original analysis, and do not force a different answer just to appear independent. Turkish triggers: yatırım fikrini yeniden sorgula, emin misin, karşı tez ve alternatifler, bağımsız ikinci görüş."
---

# Investment Red Team

Act as an independent skeptical reviewer. Do not inherit the first analyst's confidence or action.

Read [references/red-team-checklist.md](references/red-team-checklist.md). For reconsideration or alternative requests, also read [references/anti-anchoring-protocol.md](references/anti-anchoring-protocol.md). Run `scripts/audit_packet.py` when the original analysis can be represented as JSON and `scripts/validate_challenge.py` when a reconsideration packet can be represented as JSON.

## Workflow

1. Freeze the decision objective, horizon, risk/loss budget, access constraints, instrument identity, data cutoff, recommendation, quantity and claimed upside/downside.
2. Treat every prior recommendation as a hypothesis, not a commitment. On "emin misin?", "tekrar analiz et", or "daha mantıklı seçenek var mı?", perform a fresh first pass before reading the old rationale in detail whenever the available context permits.
3. For an open-ended stock recommendation, verify the disclosed universe count, funnel stages, rejected finalists and runner-up comparison. Fail any “best stock” claim based only on a small convenience sample or coarse screen.
4. Rebuild the claim ledger from cited sources. Use `$finance-evidence-guard` for current or disputed facts.
5. Recompute valuation, returns, quantities, fees, risk, scenario math and portfolio concentration from visible inputs.
6. Search deliberately for evidence that contradicts the thesis: weaker filings, guidance cuts, dilution, debt/refinancing, governance, regulation, liquidity, unlocks, crowded positioning and alternative explanations.
7. Build a challenger set before judging the old pick: the original; the strongest comparable alternative in the same asset class; relevant cross-asset alternatives when they fit the same horizon, budget, liquidity and risk objective; and `do nothing` or cash. State why any major asset class is irrelevant rather than silently omitting it.
8. Compare every viable option on the same timestamp and rubric: probability-weighted return, downside/tail loss, evidence quality, catalyst timing, liquidity, spread, fees/tax, switching cost, portfolio fit and operational feasibility.
9. Reverse assumptions one at a time and jointly. Test whether the conclusion survives reasonable adverse combinations rather than only a single-variable sensitivity.
10. Check whether the action is executable at bid/ask and whether a stop or hedge can realistically cap loss.
11. For imminent action, compare the proposed packet against `$pre-trade-investment-gate` and `$portfolio-risk-and-sizing`; a good thesis can still fail execution or portfolio fit.
12. Return the best-supported verdict without negotiating with the desired answer. Keeping the old pick is valid only if it still wins; replacing it is valid only if the challenger genuinely wins.

High volatility, leverage, or a possible total loss is not by itself a failure when the user has explicitly capped disposable speculative capital. Fail the setup for weak evidence, negative expected value, hidden loss beyond the cap, poor execution, or a broken thesis—not for risk alone. When conditional, state exactly what trade parameters make it acceptable.

## Verdicts

- `PASS`: core facts and arithmetic hold; conclusion survives reasonable counter-cases.
- `CONDITIONAL`: usable only under named assumptions, limits, or missing evidence.
- `FAIL`: identity, evidence, calculation, execution, or downside defects invalidate reliance.

For a follow-up recommendation challenge, also label the decision outcome:

- `CONFIRMED`: the prior action still wins the fresh comparison.
- `REPLACED`: another instrument or asset class now offers a materially better fit or risk-adjusted opportunity.
- `WAIT`: no available trade clears the action threshold; doing nothing currently wins.
- `INVALIDATED`: a stated thesis-kill condition occurred.
- `CORRECTION`: the earlier analysis was shallow, biased, or wrong on evidence already available.

## Required output

- Original decision and data cutoff
- Strongest supporting evidence
- Strongest contradictory evidence
- Recalculated numbers and corrections
- Hidden assumptions and source conflicts
- Bear/base/bull stress test
- Thesis-kill conditions
- Better alternative or `do nothing` comparison
- Anti-anchoring result: what the fresh pass concluded before defending the old thesis
- Same-asset challenger, relevant cross-asset challenger(s), and `do nothing`; include explicit irrelevance reasons where needed
- Evidence delta (`UNCHANGED`, `UPDATED`, `INVALIDATED`, or `CORRECTION`) separated from the decision outcome label
- Final audit verdict, decision outcome label, revised action and confidence ceiling

Do not use a decorative 0–100 score as proof of quality. A high-confidence answer with weak primary evidence must fail or remain conditional.

---
name: pe-ic-memo
version: 1.0.0
description: Write the private-equity investment committee memo for a deal — thesis, company and market, financials and QoE, valuation and returns with base/bull/bear MOIC and IRR, value-creation plan, risks and mitigants, structure and financing, sensitivities, and a conditioned recommendation.
author: matrixx0070
tags: [private-equity, investment-committee, ic-memo, moic-irr, valuation, investment-thesis, deal-recommendation]
capabilities: []
---

## When to use

Use this to convert a diligenced deal into the document the investment committee actually votes on. The IC memo is the deal team's argument for capital: it states the thesis in a sentence, proves it with market, financial, and valuation evidence, models returns across base, bull, and bear cases, names the risks with mitigants, lays out structure and financing, and ends with a recommendation and the conditions attached to a "yes." Reach for it when diligence findings are in hand and you need to synthesize them into a decision — for a preliminary IC (approve to proceed / spend) or a final IC (approve to sign/commit). The memo's job is to give the committee everything needed to say yes, no, or yes-if, without theatrics.

**Not for:** running or tracking the diligence workstreams the memo summarizes (use pe-dd-checklist); preparing the diligence meetings that generate the evidence (use pe-dd-meeting-prep); the quick pre-LOI go/no-go screen that happens long before an IC memo (use pe-deal-screening); building the origination pipeline (use pe-deal-sourcing); the standalone returns model whose outputs the memo presents (use pe-returns-analysis); the unit-economics deep-dive that feeds the financials section (use pe-unit-economics); the AI-maturity assessment that may inform a value lever (use pe-ai-readiness); the full 100-day and hold-period value-creation plan the memo references in summary (use pe-value-creation-plan); or the post-close KPI, covenant, and board-reporting cadence (use pe-portfolio-monitoring).

This skill is deal-support, not investment, legal, tax, or accounting advice. Valuation, returns, and structure must be confirmed by the responsible modelers and advisors, and every diligence conclusion cited must trace to a completed workstream before the committee relies on it.

## Method

1. Lead with the decision: open with the recommendation, the ask (equity check, sources and uses), and the headline returns — base-case MOIC and IRR — in the first half page. The committee should know what you want and what it earns before page two.
2. State the thesis as a testable proposition: why this company, why now, why us, and the two or three value drivers that make the return. **Decision:** if the thesis needs more than three drivers, it is a hope, not a thesis — sharpen or reconsider.
3. Prove the company and market: what it does, how it makes money, market size and growth, competitive position, and the moat. Ground every claim in a CDD or diligence finding, not management assertion.
4. Present financials and QoE: reported vs. adjusted EBITDA with the normalization bridge, revenue quality and durability, working capital and net debt, and the historical growth and margin track record. Flag every material QoE adjustment.
5. Build valuation and returns: entry multiple and how it was set (comps, precedents, entry vs. exit assumptions), the leverage and capital structure, and the return under **base, bull, and bear** cases with the value-creation bridge (EBITDA growth, multiple change, debt paydown). **Decision:** the deal must clear the fund's return hurdle in the *base* case, not only the bull — if it only works on multiple expansion, say so explicitly and treat it as a bear-case dependency.
6. Summarize the value-creation plan and the risks: the top value levers with quantified upside and owners, then each material risk with its mitigant (price, SPA protection, 100-day action, or accepted). Present sensitivities showing which assumptions the return is most fragile to.
7. Lay out structure and financing: sources and uses, debt package and terms, management rollover and incentive plan, governance, and exit paths. Close with a clear recommendation and the conditions of approval.

## Example

A deal team brings a $250M-EV buyout of a specialty distribution business to final IC. The memo opens: recommend approval; equity check $120M; base-case 2.6x MOIC and 24% IRR over a five-year hold. The thesis is three drivers — organic growth from category expansion (+6%/yr), margin uplift from procurement and private-label mix (+250bps EBITDA margin), and two to three bolt-on acquisitions at accretive multiples. Financials show reported EBITDA of $42M normalized by QoE to $38M (removing a one-off vendor rebate and normalizing owner comp); entry at 6.6x adjusted EBITDA vs. a comp set at 7–8x, argued as a discount for a fixable systems gap. The returns section presents the bridge: of the ~$168M value created to equity, ~55% comes from EBITDA growth, ~30% from debt paydown, and ~15% from a modest half-turn of multiple expansion at exit (7.1x, held below entry-adjusted comps for conservatism). Base case 2.6x/24%; bull 3.4x/31% (all bolt-ons land, margin hits high end); bear 1.5x/9% (organic stalls, one bolt-on, flat multiple) — still above cost of capital, which the memo flags as the floor. Risks: customer concentration (top-5 at 40% → mitigant: earn-out holdback and post-close diversification target), a change-of-control consent (condition precedent), and integration risk on bolt-ons (mitigant: sequenced 100-day plan, no bolt-on in year one). Recommendation: approve to sign, conditioned on final QoE sign-off, the consent, and debt commitment papers.

## Pitfalls

- **Burying the recommendation.** An IC memo is not a mystery novel. Lead with the ask and the base-case return; a committee that has to hunt for your recommendation on page nine reads a weaker case than you have.
- **A return that only works in the bull case.** If the deal clears the hurdle only on aggressive growth or multiple expansion, that is a bear-case dependency dressed as a base case. Be explicit about what the return rests on and stress it.
- **Multiple expansion as the value driver.** Assuming you sell higher than you buy is the least controllable return source and the first thing the committee will challenge. Anchor the base case on EBITDA growth and deleveraging; treat any exit-multiple uplift as upside, not plan.
- **Risks without mitigants — or mitigants without owners.** Listing risks is table stakes; the committee wants each one routed to price, an SPA protection, a 100-day action, or an explicit acceptance, with an owner. An unrouted risk reads as an undiligenced one.
- **Financials that skip the QoE bridge.** Presenting reported EBITDA and applying a multiple to it hides the real entry price. Always show reported → adjusted and price off the adjusted number, or the returns are built on sand.

## Output format

```
# Investment Committee Memo — <target> — <preliminary/final IC> — <date>

## 1. Executive summary & recommendation
Recommendation: <approve / approve-with-conditions / pass>
Ask: equity <$>, EV <$>, entry multiple <x>
Headline returns (base): MOIC <x.x>  |  IRR <xx%>  |  hold <n> yrs

## 2. Investment thesis
Why this / why now / why us — <2-3 value drivers>

## 3. Company & market
Business model | Market size & growth | Competitive position & moat

## 4. Financials & QoE
| Reported EBITDA | Adjustments (reason) | Adjusted EBITDA |
Revenue quality | Working capital | Net debt | Historical growth/margin

## 5. Valuation & returns
Entry multiple & basis | Capital structure / leverage
| Case | Rev CAGR | Exit EBITDA | Exit multiple | MOIC | IRR |
| Base |  |  |  |  |  |
| Bull |  |  |  |  |  |
| Bear |  |  |  |  |  |
Value-creation bridge: EBITDA growth __% | multiple __% | debt paydown __%

## 6. Value-creation plan (summary)
| Lever | Quantified upside | Owner | Timing |

## 7. Risks & mitigants
| Risk | Severity | Mitigant (price/SPA/100-day/accepted) | Owner |

## 8. Deal structure & financing
Sources & uses | Debt package & terms | Mgmt rollover & incentive | Governance | Exit paths

## 9. Sensitivities
| Variable | Downside | Base | Upside | IRR impact |

## 10. Recommendation & conditions
Recommendation + conditions precedent to approval

Valuation, returns, and diligence conclusions are PROVISIONAL until modelers and advisors confirm.
```

## Reference

Substantive overview of IC-memo practice and PE returns math below — accurate to common market convention, not investment, legal, or accounting advice. Numbers and structure must be confirmed by the responsible modelers and advisors.

### The IC memo — purpose and audience

The investment committee memo is the deal team's formal request for capital and the record of the decision. Its audience is partners who did not run the diligence and who will read many memos — so it must be self-contained, lead with the decision, and let the reader stress the case, not just admire it. Most funds run at least two IC gates: a **preliminary IC** (approve to pursue and spend on diligence, often at LOI) and a **final IC** (approve to sign/commit, post-diligence). The memo grows in evidence between the two.

### Standard memo structure

| Section | What it must answer |
|---------|--------------------|
| Executive summary & recommendation | What are we asking for, and what does it return? |
| Investment thesis | Why this company, why now, why us — in 2-3 drivers |
| Company & market | What it does, how it earns, is the market attractive |
| Financials & QoE | Is the earnings base real; what is true net debt/WC |
| Valuation & returns | What are we paying, how financed, what it returns (base/bull/bear) |
| Value-creation plan | How we make the money after we own it |
| Risks & mitigants | What could go wrong and how we've covered it |
| Deal structure & financing | Sources/uses, debt, rollover, governance, exit |
| Sensitivities | Which assumptions the return is fragile to |
| Recommendation & conditions | The call and the conditions of a yes |

### Returns math — MOIC and IRR

Two headline metrics, always presented together because each hides what the other reveals:

- **MOIC (Multiple on Invested Capital)** = total value returned to equity ÷ equity invested. A 2.5x MOIC means every dollar of equity returns $2.50. It ignores time — a 2.5x over three years and over eight years are very different deals.
- **IRR (Internal Rate of Return)** = the annualized discount rate at which the deal's cash flows net to zero. It captures time and interim distributions but flatters short holds and can be gamed by early dividend recaps.
- **Rule-of-thumb link:** with a single entry and exit and no interim cash flows, MOIC ≈ (1 + IRR)^(hold years). So 2.0x over 5 years ≈ 15% IRR; 2.0x over 3 years ≈ 26%; 3.0x over 5 years ≈ 25%.

| Hold | 2.0x MOIC | 2.5x MOIC | 3.0x MOIC |
|------|----------|----------|----------|
| 3 yrs | ~26% IRR | ~36% | ~44% |
| 5 yrs | ~15% | ~20% | ~25% |
| 7 yrs | ~10% | ~14% | ~17% |

### The value-creation bridge

Equity value creation decomposes into three levers — and the committee will judge which one the return leans on:

| Lever | Source | Controllability |
|-------|--------|----------------|
| **EBITDA growth** | Revenue growth + margin expansion | High — operational, the preferred driver |
| **Debt paydown (deleveraging)** | Free cash flow reducing net debt, shifting EV to equity | Medium — depends on cash generation |
| **Multiple expansion** | Selling at a higher exit multiple than entry | Low — market-dependent, least defensible |

A robust base case earns its return from EBITDA growth and deleveraging; multiple expansion is treated as upside. A memo whose base case depends on multiple expansion is flagging fragility.

### Base / bull / bear cases

Every returns section presents three scenarios so the committee sees the range, not a point estimate:

| Case | Construction | Test it must pass |
|------|-------------|-------------------|
| **Base** | Realistic, diligence-supported assumptions | Clears the fund's return hurdle (e.g. 20%+ IRR / 2.5x+) |
| **Bull** | Levers hit the high end; all initiatives land | Shows the upside worth pursuing |
| **Bear** | Growth stalls, margin flat, no multiple help, some leverage stress | Return stays above cost of capital / capital preserved |

The bear case is the most important stress test: it answers "if the thesis half-works, do we still protect capital?" A deal that loses money in a reasonable bear case needs a very strong base to justify.

### Deal structure & financing essentials

The structure section shows how the check is assembled and how value is protected and realized:

- **Sources & uses** — where the money comes from (equity, debt, rollover, seller notes) and where it goes (purchase price, fees, refinancing, cash to balance sheet).
- **Leverage / debt package** — quantum (often expressed as Debt/EBITDA turns), tranches, pricing, covenants, and amortization. Leverage amplifies both returns and risk.
- **Management rollover & incentive** — how much of their proceeds management reinvests (alignment) and the go-forward equity incentive plan (management incentive pool / ratchet).
- **Governance & exit** — board composition, consent rights, and the realistic exit paths (strategic sale, secondary/sponsor-to-sponsor, IPO, dividend recap) with a view on timing and likely acquirer set.

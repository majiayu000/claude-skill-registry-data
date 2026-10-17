---
name: risk-management
description: Survive first — position limits, stop policy, leverage discipline, kill criteria, and the house gates.
version: 1
triggers: risk management, position limits, stop loss, leverage, kill criteria, drawdown
category: Money & markets
blurb: Survive first — position limits, stop policy, leverage discipline and kill criteria.
archetype: knowledge
example: Set risk limits for my trading so one bad week can't sink me.
---

# Risk Management (Investing)

Rule one: don't lose the ability to play. Every position gets a maximum loss before entry; every strategy gets kill criteria; every trade over the house threshold gets a human yes.

## When to use
- Before every entry (sizing + max loss).
- Designing exits/stops; monitoring open risk.
- After any loss beyond plan — the review is mandatory.

## Method
1. **Max loss per position**: pre-defined in currency and % of portfolio; if you can't state it, you can't take it.
2. **Position limits**: single name / sector / theme / illiquid caps (from `portfolio-construction`); correlated positions counted as one exposure.
3. **Leverage discipline**: default none; if used (margin, options), hard limits, margin-call awareness, and written justification; never leverage on concentrated bets.
4. **Stop policy**: pre-committed levels (price or time) set at entry; respect them or formally re-underwrite — never move stops outward without re-deciding the whole position.
5. **Liquidity**: exit size vs average volume; know your time-to-exit before you need it.
6. **Tail awareness**: gaps happen; options/hedges where justified; assumptions about "orderly markets" fail exactly when needed.
7. **Strategy kill criteria**: drawdown/time-based stops for systematic strategies; divergence from model = investigate + possibly kill (`backtesting-validation`).
8. **Post-loss protocol**: pause → review against thesis/journal → re-underwrite or close; no revenge trades; adjust process, not just position.
9. **House gates**: trades >$500 require explicit human confirmation; reserves (money you can't afford to lose) are never in play.

## Quality gates
- [ ] Max loss stated before entry; sizing within limits.
- [ ] Stops/kill criteria written; no moved-away stops without re-underwriting.
- [ ] Leverage (if any) within written limits.
- [ ] Post-loss reviews documented.

## Red lines
- No adding to losers without re-underwriting; no revenge trades; no leverage creep; never trade without the house confirmation rules.

## Related
`portfolio-construction` · `backtesting-validation` · `behavioral-finance` · `investment-decision-process`.

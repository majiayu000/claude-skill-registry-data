---
name: evolution-review
version: "1.1.0"
user-invocable: true
dependencies:
  - report-output-discipline
description: "Data-driven selection review for any portfolio of works/products/experiments: judge items by outcome data, fix winners into reusable standards (gene fixation), kill losers without sentiment (extinction), budget exploration with a mutation quota, and use a rolling 3-month window so single months never dictate direction. Distilled from a real 4.5-month AI-music business (307 releases, ¥95 total revenue) where it ran as an evolution mechanism. Use when 做月度/季度作品复盘、决定加码或砍掉哪些作品/实验/技能、清理积压库存、防止先验或沉没成本锁死方向、把「自我感觉」换成「数据说话」. Triggers — 「月度复盘」「数据复盘」「自然选择复盘」「进化复盘」「加码还是止损」「砍库存」「淘汰评审」「该砍哪个」 / evolution review, natural selection review, monthly data review, kill criteria, mutation quota. Do NOT use for 个人绩效自评 or 单任务复盘（learn-and-improve owns single-task retrospectives）."
---

# Evolution Review (data-driven portfolio selection)

> Turn monthly portfolio reviews from "gut feeling + sunk-cost attachment" into **natural selection**: judge by outcome data, fix winners into default recipes, kill losers without sentiment, and budget exploration. Distilled from a real 4.5-month AI-music business (307 releases, ¥95 total revenue) where it ran as an evolution mechanism — the business failed, the mechanism survived.

## Why this skill exists

- **Prior lock-in**: creators keep funding their favorite direction regardless of data (sunk cost + self-image)
- **Fake reviews**: most retrospectives produce vague "direction A feels right" conclusions — no kill decisions, no budget reallocation, next month repeats
- **No extinction = no selection**: a review without kill decisions is a diary; a review without fixation (distilling what won) is just venting
- **Single-month whiplash**: one hit or one flop triggering a direction change = being led by noise

## Core mechanism (six steps)

| Step | Action | Key discipline |
|------|--------|----------------|
| ① Inventory | Full portfolio × dual metrics (a revenue-type + a reach-type metric) | Data must come from platform settlements / analytics, never self-report |
| ② Fixation | Winners' common traits become a reusable "recipe", next period's default | Two consecutive winning periods before fixation; single-period signals are logged, not fixed |
| ③ Extinction | Items without revenue/growth validation get killed (unlist / archive / stop investing) | Record the failed recipe to prevent repetition; check for unreconciled confusion before killing |
| ④ Mutation quota | Reserve 15~20% of resources for new-hypothesis experiments | A quota is a ceiling AND a floor — prevents direction drift and stagnation |
| ⑤ Rolling window | Judge on a 3-month rolling window; single-month swings never change direction | Single-month breakouts and single-month disasters both wait for the window |
| ⑥ Diversity check | Review portfolio diversity: is everything riding on one niche? | Single-niche = total loss on environment change; keep 2-3 niches alive |

## Iron rules

1. **Data over self-report**: review inputs must come from platform settlements / analytics / reconciled numbers, never "I feel"; items without data are marked "unreconciled" and down-weighted in extinction review
2. **Two-period confirmation before fixation**: a single-month breakout does not become a rule; only directions winning two consecutive periods get fixed as default recipes
3. **No single-instance conclusions**: same-day rule-making plus same-day reversal ("flip-flopping") is a mechanism-failure signal — return to the rolling window
4. **Kill without sentiment**: record the failed recipe instead of mourning — failure records are assets that prevent repetition
5. **Priors are hypotheses, not conclusions**: every "I always believed" is a hypothesis in front of data; boundary testing beats prior veto
6. **Mutation quota is both ceiling and floor**: >20% = direction drift; <15% = stagnation; unspent quota expires (hoarding quota = avoiding experiments)

## Prerequisite skill check

On load, verify `report-output-discipline` is available. If missing, abort and print:

`npx skills add FuDesign2008/open-skills -g --skill '*' --yes`

Do not silently fall back.

## Ledger template

| Item | Revenue metric | Reach metric | Verdict | Action | Recipe fixed |
|------|------|------|------|------|------|
| work / experiment / product line A | ¥ / conversion | plays / exposure / installs | Fixed / Observing / Extinct | scale / park / kill | winner traits (two-period) |
| … | … | … | … | … | … |

- Verdicts are three-valued: **Fixed** (won two consecutive periods → default recipe) / **Observing** (single-period signal, wait for the rolling window) / **Extinct** (no validation within the rolling window)
- Keep a rolling 3-month ledger as the next period's comparison baseline

**Sink**: write the ledger to `docs/reports/evolution/ledger.md` and update that same file on every review — do not create a new file. When the target repository ignores `evolution/` directories, add `!docs/reports/evolution/` before the derived-HTML rule so the ledger stays trackable. After each update, re-derive `ledger.html` following `report-output-discipline` and report both paths. When the renderer is unavailable, write Markdown only and state why. Registry row: `演化复盘台账` in `report-output-discipline/reference.md` (`human` + `接入`).

## Provenance (optional reading)

The mechanism ran a complete selection cycle in a real solo business — an AI-music side project (4.5 months, 307 releases): the vocal-poetry line was fixed as the only stable recipe (67% of revenue), the instrumental line went extinct (≈¥0/month), paid-follower operations went extinct on negative ROI. Details live in the author's private project notes.

## Relationship to other skills

- Single task/project retrospectives (Keep-Problem-Try) → `learn-and-improve`
- This skill owns **portfolio-level** monthly selection — who gets scaled, who gets killed, who gets budget. The two chain well: portfolio selection first, single-item retrospective second
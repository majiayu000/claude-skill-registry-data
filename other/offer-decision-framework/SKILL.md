---
name: offer-decision-framework
description: Compare internships and job offers using evidence, role fit, growth, money, location, certainty, and resume value without being distracted by prestige or anxiety. Not for negotiation scripts, salary market data, or long-term career planning.
version: 1.0.1
---

# Offer Decision Framework

Use this skill when comparing uncertain internships or job offers.

## Compare

Record the exact role, offer evidence, pay, attendance, agreement, continuation mechanism, location, commute, actual work, portfolio output, deadline, and reversibility.

## Rank

Weight the user's stated objective. A useful default order is:

1. role relevance
2. verifiable work and output
3. employer signal and future access
4. continuation certainty
5. learning and mentorship
6. total financial and time cost
7. city and living constraints
8. offer certainty

## Guardrails

- A verbal offer is not a contract.
- Company size and brand are signals, not proof of useful work.
- Do not reject a secure option for a speculative one without understanding timing and downside.
- Do not misrepresent a role on a resume; express real transferable tasks accurately.

Return a ranking, reasons, change conditions, signing questions, and a deadline-based fallback.

## Example

Two offers, one table, no adjectives:

| 维度 | A 公司 | B 公司 |
|---|---|---|
| 岗位匹配 | 4 | 3 |
| 证据强度 | 口头承诺 | 书面 offer |
| 成长 | 接触全流程 | 单一环节 |
| 钱 | 4K | 5K |
| 城市 | 上海 | 杭州 |
| 可逆性 | 一个月可走 | 三个月 |

Score it, then write the one sentence that will still be true in six months.

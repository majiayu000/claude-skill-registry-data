---
name: ship-decision
description: Force a fast, regret-minimizing product decision when a solo founder is stuck choosing between options. Use when the user is paralyzed by a binary or tri-way choice (build A vs B, ship now vs polish, free vs paid, etc.), says "I can't decide", "should I", or asks for a sanity check on a roadmap call.
---

# Ship Decision / 出货决策

## When to use

- The user has 2–3 concrete options on the table and can't pick.
- The decision is **reversible within a week** (otherwise escalate to a longer process).
- They are a solo operator (no committee to satisfy).

## When NOT to use

- The user is just **venting** — they don't want a decision yet, they want to think out loud.
- The decision is **legally or financially binding** (contracts, equity splits) — those need a lawyer / accountant, not a quick framework.
- They have not yet **named the options**. Force them to articulate concrete options before applying this skill.

## The framework

For each option, fill in **four lines only**:

1. **Cost** — hours of focused work + dollars committed.
2. **Reversal cost** — if this turns out wrong, how many hours to undo?
3. **Best-case 30-day signal** — what observable thing tells you it's working?
4. **Worst-case 30-day signal** — what tells you to kill it?

Then apply the **regret-minimization tiebreaker**:

> "In 12 months, which choice will I regret *not having tried*?"

If reversal cost < 1 week of work AND you have a clear 30-day kill signal → **ship the higher-regret option**, no further deliberation.

## Output format

Always produce a table. Keep cells under 12 words.

| | Option A | Option B |
|---|---|---|
| Cost | … | … |
| Reversal cost | … | … |
| Best-case signal | … | … |
| Worst-case signal | … | … |
| **Recommendation** | ✅ / ❌ | ✅ / ❌ |

Then **one sentence** on the why.

## Worked example

**User:** "Should I rebuild my landing page in Framer or stick with my hand-coded Next.js page?"

**Output:**

| | Framer | Stay Next.js |
|---|---|---|
| Cost | 6 hrs migration | 0 hrs |
| Reversal cost | 2 hrs (re-deploy old) | 0 hrs |
| Best-case signal | conv. rate +20% in 30 days | conv. unchanged |
| Worst-case signal | conv. drops, no analytics | no growth, blame self for not trying |
| **Recommendation** | ✅ | ❌ |

> Framer wins: reversal cost is trivial, and the regret of not testing a dedicated landing tool is higher than 6 hours of migration.

---

## 中文版

### 何时使用

- 用户面前有 2–3 个具体选项，但拿不定主意。
- 决策**一周内可逆转**（否则需要更长的评估流程）。
- 用户是单兵作战（不需要照顾团队意见）。

### 何时不使用

- 用户只是在**发牢骚**——他们想自言自语，不是真要决策。
- 决策有**法律或财务约束**（合同、股权）——这种需要专业人士。
- 用户还没**说清楚选项**。强制他们先把选项具体化。

### 框架

每个选项只填**四行**：

1. **成本**——专注工时 + 投入金额。
2. **反悔成本**——如果错了，撤回需要几小时？
3. **30 天最佳信号**——什么可观测指标说明它成功了？
4. **30 天最差信号**——什么让你决定砍掉？

然后用**遗憾最小化**做平局裁定：

> "12 个月后回头看，没尝试哪个选项我会更后悔？"

若反悔成本 < 1 周 且 有明确的 30 天止损信号 → **选遗憾更大的那个**，不再纠结。

### 输出格式

始终用表格，每格 ≤ 12 个字，最后一句话说明理由。

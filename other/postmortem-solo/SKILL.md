---
name: postmortem-solo
description: Run a lightweight, blame-free postmortem after an incident, failed launch, or missed deadline — for one person. Use when the user says "that didn't go well", "the launch flopped", "we had an outage", "I missed my deadline", or wants to learn from a recent failure.
---

# Postmortem Solo / 单兵复盘

## When to use

- Something **didn't go to plan** in the last 30 days: outage, failed launch, missed deadline, customer churn spike, broken release.
- The user is the **only person** responsible — there's no team to interview.
- The goal is **one or two concrete changes**, not a 10-page report.

## When NOT to use

- The incident is **still active** — fix it first, postmortem after.
- The user wants **emotional processing**, not a postmortem. Suggest a walk or a friend; this skill is for cold analysis.
- It's a **routine setback** (one bug in production, one slow week) — not every bump needs a postmortem.

## Structure

Five sections, **strict word limits**:

1. **What happened** — 3 bullets, factual, no analysis. *(≤ 60 words)*
2. **Impact** — what did the failure cost? Users affected, revenue lost, hours sunk, reputation hit. *(≤ 40 words)*
3. **Timeline** — bullet list with timestamps if known: trigger → detection → response → resolution. *(≤ 100 words)*
4. **Root cause(s)** — apply **5 Whys** but stop the moment you hit a *systemic* cause (process, default, missing tool), not a personal one ("I was tired"). *(≤ 80 words)*
5. **Changes** — at most **2 concrete changes** with owner (you), due date, and verification method. *(≤ 60 words)*

**Total: ≤ 350 words.** If you need more, you're hiding from a decision.

## The "no blame, but yes accountability" rule

Solo postmortems have a trap: you're the only person who could have caused this, so it's tempting to either (a) flagellate yourself, or (b) blame externalities ("Stripe was flaky"). Neither is useful.

**Correct framing:** *"What system / habit / default could I change so that next-month-me cannot make this mistake even if next-month-me is tired and distracted?"*

This forces solutions toward **process, automation, or alarms** — not "be more careful next time."

## Output format

```markdown
# Postmortem: <one-sentence headline>

**Date:** <YYYY-MM-DD> — drafted <X> days after the incident.

## What happened
- …
- …
- …

## Impact
…

## Timeline
- HH:MM — <event>
- HH:MM — <event>

## Root cause(s)
…

## Changes
1. <change> — owner: me, due: <date>, verified by: <how I'll know it worked>
2. <change> — owner: me, due: <date>, verified by: <how>
```

## Worked example

**Input:** "I deployed on Friday afternoon, broke the signup flow for ~6 hours, lost about 40 trial signups before I noticed."

**Output:**

```markdown
# Postmortem: Friday-afternoon deploy broke signup for 6 hours

**Date:** 2026-04-30 — drafted 2 days after the incident.

## What happened
- Deployed schema migration at 16:45 local time.
- Migration removed a column the signup form still referenced.
- Signup returned 500 for ~6 hours until I checked Stripe at 22:30.

## Impact
~40 trial signups lost (Stripe shows 0 new customers in the window vs. ~7/hour baseline). Estimated revenue at risk: ~$280/mo if 10% would have converted.

## Timeline
- 16:45 — deploy pushed.
- 16:50 — first 500 (no alert; error logger was rate-limited).
- 22:30 — noticed via empty Stripe dashboard, rolled back migration in 8 min.

## Root cause(s)
The signup form references the dropped column directly, not via an abstraction. CI ran migrations against an empty test DB, so the form-vs-schema mismatch never surfaced. No deploy-time alert fires when 500 rate exceeds baseline.

## Changes
1. Add a basic uptime check that posts a Slack ping on >5x baseline 500s — owner: me, due: 2026-05-03, verified by: triggering a test 500 and confirming the ping.
2. Block deploys after 16:00 local time on Fridays (calendar reminder + git pre-push hook) — owner: me, due: 2026-05-02, verified by: trying to deploy at 17:00 Friday and getting blocked.
```

## Anti-patterns

- **"I'll be more careful next time"** is not a change. It's a wish. Replace it with a system change.
- **More than 2 changes per postmortem.** You won't do them. Cut to two.
- **Listing root causes that don't tie to a change.** If a cause doesn't generate an action, omit it.

---

## 中文版

### 何时使用

- 最近 30 天内**没按计划走**：故障、发布失败、错过 deadline、客户大量流失、版本翻车。
- 用户是**唯一负责人**——没团队可访谈。
- 目标是**一两个具体改动**，不是 10 页大报告。

### 何时不使用

- 故障**还在进行中**——先修，再复盘。
- 用户想**情绪处理**而非复盘——建议散步或找朋友聊，这个技能是冷分析。
- 只是**常规小坎坷**（一个线上 bug，一周不顺）——不是每次都需要复盘。

### 结构

五段，**严格字数限制**：

1. **发生了什么**——3 条事实，不带分析。*(≤ 60 字)*
2. **影响**——损失了什么？*(≤ 40 字)*
3. **时间线**——触发→发现→响应→修复，带时间戳。*(≤ 100 字)*
4. **根本原因**——5 Why，但**停在系统性原因**（流程/默认/缺工具），不是"我累了"。*(≤ 80 字)*
5. **改动**——最多**两条**，要有 owner（你）、截止日、验证方式。*(≤ 60 字)*

**总长 ≤ 350 字**。再多就是在逃避决定。

### "不归罪但要负责"原则

单兵复盘有个陷阱：唯一可能犯错的就是你，所以容易要么(a)自责，要么(b)甩锅外部。两者都没用。

**正确框架：** *"我能改变什么系统/习惯/默认值，让下个月的我即使累了走神也不会再犯？"*

这逼着方案朝**流程、自动化、告警**走——而不是"下次更小心"。

### 反模式

- **"下次更小心"不是改动**，是愿望。换成系统性改动。
- **一次复盘超过 2 条改动**——你做不完。砍到两条。
- **列出不对应改动的根因**——如果一个根因不会触发行动，删掉。

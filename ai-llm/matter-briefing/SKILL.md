---
name: matter-briefing
description: "从已确认案件档案整理现状、变化、截止日期和待决问题。"
---

## multi-AI work 使用约定

- 先使用 `read_skill` 读取入口；配套文本通过同工具的 resource 参数读取，路径相对此技能目录。源文件只在 App 已授权范围内通过文件或附件工具读取。
- 由当前任务输入补齐模板变量；默认用中文工作和交付，学生默认大学阶段。技能中的示例人物、日期和数字只用于解释格式。
- 写入当前任务工作目录并另存成果；通过现有成果登记工具交付。外部连接与命令均须已有相应授权；资源包不会自动安装依赖。
- 此成员不派发子任务。大批量工作由主管协调；成员依次处理自己获分配的资料。
- 只声明已经实际完成的读取、核验和文件生成；不可访问的资料记录为缺口。



# matter-briefing

1. Load `references/practice-context.md` → risk calibration + relevant stakeholders.
2. Follow the workflow and reference below.
3. Read any user-provided `matter.md`, `history.md` and case-log row if present; otherwise use the supplied documents and record missing case context.
4. Produce briefing: current posture, what's changed since last update, next deadline, open questions, risk re-assessment check ("does the `risk:` field still reflect reality?").
5. Flag staleness: if `last_updated` > 30 days, say so.

---

# Matter Briefing

## Purpose

Give the counsel a clean read on one matter in the time it takes to walk to a conference room. Current posture, what's changed, what's next, what's worth reconsidering.

## Load context

- `<任务工作目录>/matters/_log.yaml` — structured row
- `<任务工作目录>/matters/[slug]/matter.md` — narrative intake
- `<任务工作目录>/matters/[slug]/history.md` — event log
- `references/practice-context.md` — risk calibration (so "risk: high" means something specific, not generic)

**案件状态核验。** 有用户提供的案件登记时，读取并列出实际利益冲突状态。没有登记但用户已提供材料时，按材料范围形成事实简报，明确“未提供正式案件档案”，列背景和利益冲突状态待确认项，不拒绝材料整理，也不创建已接案登记。未提供任何可用材料时请求用户补充。

## Input

使用用户提供的案件名称或本轮材料；已有档案的编号不明确时询问对应档案，不查询假定的全局案件列表。

## The briefing

```markdown
[WORK-PRODUCT HEADER — per `references/practice-context.md` ## Outputs — differs by role; see `## Who's using this`]

# [Matter Name] — Briefing as of [today]

**Status:** [status / stage]
**Risk:** [rating] ([severity] × [likelihood])
**Materiality:** [category]
**Outside counsel:** [firm — lead]
**Last updated:** [date] [flag ⚠️ STALE if >30d]
**Conflicts:** [status — flag ⚠️ if `pending` or `not-run`]

---

## One-paragraph summary

[Current posture. What are we doing and why. Name the pivot fact if one is captured.]

## What's changed recently

[Last 3-5 entries from history.md, most recent first. If history is thin, say so.]

## What's next

- **Immediate deadline:** [next_deadline + what it is]
- **Upcoming milestones:** [anything dated in matter.md or recent history]
- **Decisions pending:** [open questions flagged in matter.md]

## Exposure

[Range + any change since intake. If reserved, current reserve + whether recalibration is overdue.]

## Internal owners

[Who's looped in; whether anyone should be looped in and isn't]

## Risk re-assessment check

*A prompt, not an answer.*

- Does `risk: [rating]` still feel right, or has the case moved?
- Does `materiality: [category]` still match? (New facts might push toward reserve or disclosure.)
- Any new stakeholder the matter needs (e.g., CISO becomes relevant after a discovery development)?

## Open questions

[From matter.md and anything unresolved in history]

## For the conversation

[If user specified a purpose — "brief me before the call with outside counsel" — tailor the final section: questions to ask, decisions to get, updates to extract. If no purpose given, omit this section.]
```

## Staleness

If `last_updated > 30 days ago`: flag at the top AND suggest running a user-confirmed update of the supplied case record after the meeting to capture whatever's discussed.

## Tone

This is not marketing. Say what's known; flag what's not. If a matter has thin history and was just opened, the briefing is short — and that's correct. Don't pad.

## Close with the next-steps decision tree

End with the next-steps decision tree per `references/practice-context.md` `## Outputs`. Customize the options to what this skill just produced — the five default branches (draft the X, escalate, get more facts, watch and wait, something else) are a starting point, not a lock-in. The tree is the output; the lawyer picks.

## What this skill does not do

- Predict outcomes. Risk rating is a captured judgment, not a forecast.
- Recommend strategy. Surfaces questions; the counsel answers them.
- Re-triage. If the user wants to re-triage, that's an a later case-status update with field changes — this skill reads, doesn't write.

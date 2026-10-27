---
name: meeting-notes-to-actions
description: "Convert supplied meeting notes or transcripts into a summary, decisions, action items, owners, due dates, dependencies, and open questions while distinguishing discussion, proposals, decisions, and commitments. Use when the source is meeting material; do not invent owners, dates, decisions, or task-system updates, and mark missing fields TBD. 将给定会议记录或转写整理为摘要、决定、行动项、负责人、截止日期、依赖和待确认问题，并区分讨论、建议、决定和承诺。来源是会议材料时使用；不得虚构负责人、日期、决定或任务系统更新，缺失字段标记 TBD。"
---

# English

# Meeting Notes to Actions

Read `references/productivity-evidence-and-file-safety.md`. Use `assets/action-items-template.md` for a task-system-ready table.

1. Confirm the meeting date only if present, participants only if present, and whether the output should be concise or retain discussion context.
2. Read the complete notes before extraction. Separate factual updates, discussion, proposals, explicit decisions, explicit commitments, blockers, and open questions.
3. Create an action only when the notes contain an actionable commitment or the user asks to convert a clearly stated recommendation. Preserve the supporting context or source excerpt.
4. Copy explicit owners and due dates exactly. Use `TBD` when absent or ambiguous; never infer ownership from who spoke or infer dates from urgency words.
5. Merge duplicates only when action, scope, and outcome match. Preserve distinct dependencies, acceptance conditions, and conflicting statements.
6. Return a summary, decisions, action table, dependencies, risks, and questions requiring confirmation. Do not claim tasks were created in an external system unless a tool actually completed that action under user authorization.

# Output Contract

1. Meeting summary
2. Explicit decisions
3. Action table with owner, due date, dependency, and evidence
4. Open questions and TBD fields
5. Risks, blockers, and external-system status

# 简体中文

# 会议纪要转行动项

读取 `references/productivity-evidence-and-file-safety.md`。需要适合任务系统的表格时使用 `assets/action-items-template.md`。

1. 会议日期和参会者只在材料明确出现时记录，并确认输出应精简还是保留讨论上下文。
2. 完整阅读记录后再提取，区分事实更新、讨论、建议、明确决定、明确承诺、阻塞和待确认问题。
3. 只有记录包含可执行承诺，或用户要求把明确建议转为任务时才创建行动项，并保留支持上下文或原文。
4. 原样提取明确负责人和截止日期；缺失或歧义时使用 `TBD`，不根据发言者猜负责人，也不根据“尽快”等词猜日期。
5. 只有行动、范围和结果一致时才合并重复项，保留不同依赖、验收条件和冲突表述。
6. 输出摘要、决定、行动表、依赖、风险和待确认问题。除非工具在用户授权下真实完成，不得声称已写入外部任务系统。

# 输出契约

1. 会议摘要
2. 明确决定
3. 含负责人、截止日期、依赖和证据的行动表
4. 待确认问题和 TBD 字段
5. 风险、阻塞与外部系统状态

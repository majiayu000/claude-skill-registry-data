---
name: resume-polish-craft
description: Polish a resume that already has the right content - compress page count, tighten bullet lead-ins, decide which sentences get bolded, keep the persona consistent with the target function, and diagnose layout before deleting anything. Triggers on "压缩成一页", "这条引导词改四个字", "哪些句子要加粗", "title 写得有点逼格", "怎么缩不进去". Not for matching a resume against a JD (resume-jd-matcher) and not for turning one project into an entry (vibecoding-resume-story).
version: 1.0.0
---

# Resume Polish Craft

The content is already correct. What is left is density, emphasis, persona, and page count.
This skill exists because the failure modes here are social, not editorial: every one of the rules
below was learned by doing the wrong thing and getting told off.

## Rule 0 — Format tasks and content tasks are different tasks

He asks you to **mark** things. That means bold, underline, layout. It does not mean delete.

> Real case: asked "which sentences are worth bolding", I delivered eleven deletions instead.
> He read that as destroying work he had already approved. Same message, different verb.

- "标 / 加粗 / 划线" → mark only. Do not attach a deletion proposal.
- "删 / 压缩" → then content is on the table.
- When in doubt, ask one sentence. Never guess by escalating the scope.

## Rule 1 — Lead-ins are summaries, not slogans

A bullet lead-in is four characters that say what the line is about, in the same register as
`技术栈` / `项目背景` / `项目成果`.

- ✅ 工具研发 · 流程搭建 · 场景验证 · 提效方案 · 需求拆解 · 合规优化 · 矩阵搭建
- ❌ 从零造轮 / 深耕运营追求闭环 — invented slogans; reader cannot tell what the line says
- ❌ "卡在出稿，自建工具" — **four characters means four characters.** Do not upgrade it into a
  tidy parallel couplet because it reads better. It reads better for you, not for him.

Test: no rhetoric, spoken aloud it is plain speech, at a glance you know what this line covers.

## Rule 2 — Persona follows the target function

Applying to operations means the resume must not smell like engineering.

- Delete the tech-stack line. Naming `Python (9 modules / 849 lines)` makes an HR screener
  mislabel the candidate in ten seconds.
- "基于 Python 独立开发 Agent" → "独立搭建脚本生成 Agent". No line counts, no module counts.
- Keep Agent / tool selection / prompt engineering — that is AI fluency, a plus for operations.
- Keep AI coding tools in the **skills** row (uses AI tools = plus); the same name in a tech-stack
  row reads as "writes code" and misfires.
- Intern boundary: may "参与公司级项目 / 主动开发工具 / 被抽调 / 沉淀 SOP".
  May not "主导项目 / 负责体系 / 规划战略". Downgrade 负责 to 承担.
- Raising a title on a team project: mark the slice you owned
  (`AI 提效侧核心贡献人员`). On a solo project use independence words instead (`独立主理人`).

## Rule 3 — Bold is sentence-level, one per bullet

"Which sentences are useful" is a question asked **inside a bolding pass**. It means: pick the
sentences worth emphasising. It does not mean: decide what survives.

Worth bolding, pick one:
- **has a number** (throughput, pass rate, turnaround, count, views, orders)
- **has a method** (拆解 27 份爆款 / 横向评测 15+ 款 / 六步调研法)
- **has a deliverable** (rule library, SOP, agent, adaptation matrix)

Not worth bolding: setup sentences, busywork, zero-number process lines, noun piles.
**One bullet gets exactly one bold.** All bold = no bold; the eye has nowhere to land.

## Rule 4 — Number discipline

- A conflict between two figures is **stated once, then he decides.** Never pick for him, never
  judge which source is more credible.
- Once he gives a number, write it, even if an older file disagrees.
- Delete any number he cannot defend ("我完全不知道" ones) — third-party market data, revenue claims.
- Proposing a new number (say `15+ 款工具`) requires shipping the backup list in the same message,
  so he can count before committing.
- Component figures must sum to the headline figure.

## Rule 5 — Diagnose layout before deleting content

Page count over budget does not mean "delete a project". Read the parameters first.

```
页边距：docx 的 w:sectPr/w:pgMar（twips，567 = 1cm）
字号  ：段落 rPr 的 w:sz（21 = 10.5pt）
行距  ：段落 pPr 的 w:spacing w:line（320 = 16pt）
行数  ：版心高 ÷ 每行高度
```

Usual fix: font size 10 + fixed line spacing **13 pt** (floor = font size × 1.2, below that glyphs
get clipped) + delete empty paragraphs.

Deletion order, lossless to lossy: empty paragraphs → elective courses → skills laid out in
columns → duplicated project background → the student-activities block.
**Project experience is the hard cargo. Touch it last.**

## Rule 6 — Mass applications: one page beats two

HR screens in 10-30 seconds and the second page is usually never opened; for a new grad one page
is the default expectation and two pages reads as padding.
Ship a one-page version for mass applications and keep a two-page version on file for referrals.

## Rule 7 — Deliver in the chat, not as a file

- Say it in the conversation. A Markdown file is not read.
- A one-line rule is too vague. Thirty scattered words are too granular.
  The right unit is **one sentence per line, grouped by module**.
- Being corrected three times in a row means stop and ask. Do not compensate by doing more.

## Self-check before sending

图看全否 / 数字核过否 / 引领句像人话否 / 与下文重复否 / 文件放对位置否。

## Red lines

- 🔴 **Never delete a field name he approved** (技术栈 / 项目背景 / 项目成果). Compress the prose
  under it, not the label.
- 🔴 **Never silently rewrite his file.** Mark only; editing the document needs a backup and his yes.
- 🔴 **Never expand the verb.** Mark stays mark.

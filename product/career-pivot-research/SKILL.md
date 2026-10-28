---
name: career-pivot-research
description: Research whether a career pivot is viable before rewriting a resume for it — collect real, linkable JDs for the target title, derive three capability tiers (minimum bar / full match / beyond), find the project the user already has but described in the wrong vocabulary, then produce a rewrite table plus a dated study plan. Triggers on "我能转 X 岗吗", "X 岗 JD 都要求什么", "照着 JD 帮我改简历".
version: 1.0.0
---

# Career Pivot Research

"Can I move into this role?" is not one question. It is: *what is actually required, what of that
do I have, and which of my existing work is being described in the wrong vocabulary.*

Distinct from `resume-jd-matcher` (one specific JD, go/no-go for one application)
and `job-application-screener` (ranking a batch of openings).

## Step 1 — Collect real JDs, with links

Search the target title plus 校招/应届 if the user is a student. Aim for **5-8 postings**, and keep
the source URL for every one so the user can check your reading.

Record per posting: 岗位职责 (verbatim) + 任职要求 (verbatim) + source. Verbatim matters — paraphrase
is where you start inventing requirements.

Then count term frequency across all of them. The frequency list is the actual bar; any single JD
is a sample.

**Look for the posting aimed at the user's own graduation year.** A JD that says 「2027 届」or
「其他专业不限」changes the whole answer.

> **Real case (2026-10-21):** asking about AI 测试工程师 for a 2027-graduate content-operations
> candidate. Six JDs collected. Two findings flipped the answer: 中国移动卓望 wrote
> 「计算机相关专业优先，**其他专业不限**」(non-CS major was not a hard filter), and 每日互动's JD
> was explicitly **「2027 届」** — the user's own year. Neither was visible from any single posting.

## Step 2 — Three capability tiers

Do not answer "am I qualified" with one verdict. Split it:

| Tier | Question it answers |
|---|---|
| **最低线** | What, if missing, fails the process outright (usually a written test)? |
| **匹配线** | What the JDs literally name as required? |
| **远超线** | What this user has that a candidate with a textbook background does not? |

The **远超线** is the actual argument for hiring them, and it is usually invisible on the resume
because it is expressed in the old domain's language.

> **Real case:** the candidate's 「远超」was not a testing credential. It was: he had defined
> acceptance criteria for an AI product, owned a real rule set and regression set (15 rules / 14
> regression cases / 27 replacement rules), run A/B experiments against metrics, and knew where the
> human/AI boundary sits. A CS-major test engineer with none of that. Meanwhile his 最低线 was
> empty: Python by hand, SQL joins, Linux, black-box case design, HTTP status codes.

## Step 3 — Find the mislabelled project

The highest-leverage find in a pivot is **a project the user already built and described in the
wrong vocabulary.** Do not add projects. Re-describe what exists.

Search their repos for the shape of the target role: rule engines, case sets, rule versioning,
regression runs, validators, evaluation gates.

> **Real case:** `ad-compliance-checker` was written on the resume as
> 「带货文案自动三级风险分级」— one line, product language. It is in fact a **rule engine + tiered
> case set + regression suite**: 15 graded rules, 14 regression cases, versioned rule file.
> That is a testing project. It was promoted from 1 line to 4, and it became the only thing on the
> resume that answers 「你做过什么测试」.

## Step 4 — The rewrite table

The user has to paste this into a document themselves. Give them, per location:

- 板块 + 定位（where on the resume）
- 原文 / 改成（both copyable）
- **字数差** — they care about layout breaking
- 为什么这么改
- 风险标记

### Character-count discipline

Count with whitespace stripped. Grade the delta:

- `|Δ| ≤ 3` green — pastes in, layout unmoved
- `≤ 10` amber
- `> 10` red — **and for every red one, ship a compressed alternative** in the same row

Do not silently pad to hit exact equality; state the delta and offer the short form.

> **Real case:** 26 locations; 20 landed within ±5. The 6 outliers were all deliberate
> (a 1-line project promoted to 4 lines, a new skills line, a section compressed to free space).
> Each carried a note on what to delete if the page still overflowed.

### Mark the ones that are a promise

If a line claims a skill the user cannot yet answer questions on, tag it **写下即承诺** and say so.

> **Real case:** the new skills line listed SQL / pytest / Postman / Linux. The user had authorised
> "SQL — you can say I have basics". They had **never touched SQL**. The line shipped with the rule:
> finish the study plan before applying. Writing it earlier is a liability, not a shortcut.

## Step 5 — Study plan with daily acceptance criteria

Every day needs an artifact, not a topic. "学习 SQL" is not a plan;
"手写 20 条，5 分钟内写出『查年龄>20 的女生姓名』" is.

Include one **watershed day** where the claim on the resume becomes true rather than aspirational.

> **Real case:** Day 21 — convert the 14 regression cases already sitting in the repo into actual
> running pytest. Before that day the new skills line is a promise; after it, it is a fact.

## Step 6 — Growth path and pay

Give stages with what each stage actually does. For pay, **separate JD-stated figures from
inference** and label which is which. Do not present an inferred range as a sourced one.

## Red lines

- 🔴 **Never add a course, project, or award the user does not have.** Reordering the 主修课程 line
  is fine; inventing 「数据库与 SQL 应用」 is not. A line that gets probed in interview is worse
  than a gap.
- 🔴 **Never invent a JD.** Every requirement traceable to a link the user can open.
- 🔴 **Do not use two numerical standards in one document.** If the resume says 1000+ and your
  planning page says 2000+, pick one and say which.
- 🔴 **Say plainly when a hard gate blocks the pivot.** If the gap is a written coding test, the
  resume rewrite is not the bottleneck and saying otherwise wastes their month.

## Example

> 我能不能转 AI 测试这种岗？照着 JD 帮我改一份能海投的简历，每个地方怎么改发我，最好字数一样。

6 JDs with links → frequency table → three tiers (his 远超 is defining acceptance criteria for an
AI product; his 最低线 is empty and that is the real blocker) → `ad-compliance-checker` promoted
from 1 line to 4 → 26-row rewrite table with character deltas and one 「写下即承诺」 tag →
30-day plan whose Day 21 converts existing regression cases into real pytest → growth path with
JD-sourced vs inferred pay marked differently.

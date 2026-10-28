---
name: resume-jd-matcher
description: Pre-application resume-to-JD match check — machine-check hard requirements (degree/years/certificates) and keyword coverage term by term against the JD, flag gaps in three tiers (never done / done but unwritten / semantic synonym), and suggest rewrites grounded only in real experience. Also produces a per-location rewrite table with character-count deltas when the ask is "照着 JD 改简历". Triggers on "简历匹配吗", "投这个岗行不行", "简历怎么改", "每个地方怎么改发我". For switching into a whole new role, use career-pivot-research instead.
version: 1.2.0
---

# Resume JD Matcher

The last check before you hit submit. ATS and HR filter on **keywords and hard requirements** first.
Matching is not fabrication — it is translating things you genuinely did into the employer's vocabulary.

Distinct from `job-application-screener` (which decides *whether* to apply across a batch)
and `vibecoding-resume-story` (which turns one project into a resume entry).

## Three steps

### 1. Machine check (always run)

```bash
python "<this skill dir>/scripts/match_resume.py" <JD.txt> <resume.txt>
```

Outputs JSON with three blocks:

- **hard_requirements** — degree, years, certificates, location; each judged 达标 / 缺失 / 未提及
- **keyword_coverage** — which JD skill/tool/domain terms appear in the resume, coverage %, missing list
- **duplicate_lines** — same sentence repeated (copy-paste residue)

### 2. Semantic match (AI layer, covers the script's blind spots)

1. **Synonyms** — JD says 用户增长, resume says 拉新. No literal hit but a real hit.
   Label these 语义匹配 and list them **separately from true gaps**.
2. **Hidden signals** — translate euphemisms. 抗压能力强 = heavy overtime.
   扁平化管理 = nobody will mentor you. State the implication plainly.
3. **Placement** — is the most relevant experience on the first screen?
   Is irrelevant experience eating too much space?

### 3. Report

```
【结论】硬条件 X/Y 达标 | 关键词覆盖 62% | 综合：可投(需改) / 勉强 / 不建议投
【硬条件明细】学历✓ 年限✗(JD要3年,简历可算出2年4个月,建议写"近3年") 证书?
【缺失关键词】分三档：
    真没做过      → 不建议编
    做过没写      → 给改写句
    语义匹配      → 建议换词
【改写示例】JD原词 → 简历改写句（只基于用户提供的真实经历）
【工作信号】"抗压能力强"+"弹性工作制" → 大概率经常加班，请确认能否接受
```

## Step 4 (optional) — Rewrite table, when the ask is "照着 JD 改简历"

"匹配吗" ends at the report. "帮我改" needs something the user can **paste into their own file**.
Give one row per location:

| 字段 | 说明 |
|---|---|
| 板块 + 定位 | 简历哪一节、第几条 —— 用户要能找到它 |
| 原文 | 逐字照抄，可一键复制 |
| 改成 | 可一键复制 |
| 字数差 | 用户真的在意粘贴后版面会不会炸 |
| 为什么这么改 | 一句话，别写作文 |
| 风险标记 | 待确认 / 写下即承诺 |

### Character-count discipline

去空白后计数。分级：`|Δ| ≤ 3` 绿（版面不动）、`≤ 10` 黄、`> 10` 红，
**并且每个红的都要在同行附一个压缩版**。不要为了对齐字数硬凑——报出差值，给短版本。

> **Real case (2026-10-21):** 26 处，20 处在 ±5 内。6 个超差的都是故意的
> （一个 1 行的项目升格成 4 行、新增一条技能行、一节压缩腾版面），
> 每行都写了「版面还超的话先删哪几个字」。

### 优先原地替换，不要推倒重写

用户原本的措辞是底稿不是废纸。改「素材整理」→「交付标准」这类换词，
比整段重写安全得多，也更容易被他接受。

### 主动找被错词描述的项目

改之前先扫一遍他的仓库/项目列表，找**已经是目标岗位形状、但用了旧领域词汇描述**的东西。
这是改写里杠杆最高的一处，而且不需要编任何新东西。

> **Real case：** `ad-compliance-checker` 在简历上写的是「带货文案自动三级风险分级」——业务语言，
> 1 行。它实际是规则引擎 + 分级用例集 + 回归集。改成测试语言后升格为 4 行，
> 成了整份简历里唯一能正面回答「你做过什么测试」的东西。

## Red lines

- 🔴 **Never suggest inventing experience.** For keywords the candidate genuinely lacks,
  write 不建议编. Offer a real adjacent experience instead, or suggest addressing it at interview.
- 🔴 **Years are computed from the resume's own dates.** Never round up on the candidate's behalf.
- 🔴 **If a hard requirement fails, say 不建议投.** No consolation padding.
- 🔴 **Remind the user to desensitize** — no ID numbers, home address, or photos in files handed to analysis.

## Example

> 帮我看看这个岗投得了吗？（贴 JD + 简历）

Machine check reports 年限 gap (JD wants 3 years, resume computes to 2y4m) and 68% keyword coverage.
AI layer flags 「私域运营」as a true gap (never done → 不建议编), 「内容矩阵」as done-but-unwritten
(rewrite from the 小红书 account work already in the resume), and 「用户增长」as a synonym of 「拉新」.
Verdict: 可投(需改).

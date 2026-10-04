---
name: paper-expression-editor
description: Use when a user asks to review or revise Chinese academic papers, theses, proposals, or research reports for formulaic, repetitive, vague, or mechanically structured wording while preserving evidence and meaning.
license: MIT
---

# 中文论文证据保留型表达编辑

本 Skill 面向已经完成或已有初稿的学术文本，依据可观察的表达与论证问题进行保真编辑。它不从零生成论文，不判断作者身份，不估计 AI 概率，也不承诺检测结果。

核心工作流：Lock → Diagnose → Decide → Revise → Audit。先锁定语义，再诊断、决策、最小修改和审计。核心优先级：事实 > 命题范围 > 逻辑关系 > 段落组织 > 句式 > 词汇标点。

## 按任务加载

- **只评阅不改稿：**读 [评阅清单](references/review-checklist.md)，交付已查范围、可定位原文和已确认问题。
- **要改写：**读 [改写指南](references/revision-guide.md)；先定位再给可直接用的改写稿。
- **任何需要保真改写的任务：**读 [核心契约](references/core-contract.md)，先建立 Meaning Lock。
- **完成改写后：**读 [语义审计](references/meaning-audit.md)，逐项比较原文与改写稿。
- **碰到数字、公式、引文、方法、结论：**读 [事实复核清单](references/fact-check.md)，逐项冻结核对。
- **需要给问题编号或统计类型：**读 [问题分类](references/issue-taxonomy.md)。
- **用户指定交付形态：**读 [输出格式](references/output-formats.md)。
- **需要边界示例时：**读 `examples/` 中与文体相符的案例，不要默认加载全部案例。
- **开题、计划类材料：**“拟、计划、将、预期”与已完成严格区分，不得改写时态。
- **需要统一写法或保留作者风格时：**读 [风格档案](references/style-profile.md)。有导师样例、本次要求或适用规范时先核对，再决定是否采用档案默认；无需统一写法时不加载。

## 共同规则

1. 先确认本轮范围、目标文体、导师或格式要求、作者样例和排除项。标黄只表示待复查，不等于有问题。
2. 只改损害清晰度或论证的表达。正常术语、平行结构、必要重复和标点一律保留；不批量删除“从……看”“进一步”“综上所述”或分号。
3. 以核心契约中的 Meaning Lock 为冻结基线。无材料支撑的数值、显著性、文献、效果和局限一律不补写；影响科学含义的改动标“待作者确认”，不直接写入定稿。
4. 严格区分三类输出：**表达问题**可直改、**格式偏好**须有依据才统一、**事实待核验**只标缺口。少分号、无顿号标题、“等人”写法属于格式偏好，以本次要求和投稿规范为准。
5. 供 Word 手动修改时，给出章节标题、可搜索连续原文、问题依据、完整替换稿和待核验项。搜索串必须逐字连续，不用省略号；只查片段就标片段，不声称全文通查，不沿用历史计数。
6. 只要润色稿就直接给稿，只要诊断就只给问题单。不强行评分；任何分数只描述表达问题，不映射 AI 概率。
7. 修改范围必须与问题范围一致。能改几个字解决的问题，不重写整段；正常句子保留。

本 Skill 处理学术表达，不代替数据、实验、文献原文和适用规范的实际核验。用户当前明确要求优先于这里的默认建议。

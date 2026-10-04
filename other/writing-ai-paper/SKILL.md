---
name: writing-ai-paper
description: Guide the planning, drafting, and revision of AI/ML conference papers (NeurIPS, ICML, ICLR, CVPR, AAAI, ACL, etc.) using the handbook "Writing AI Conference Papers" by hzwer (Zhewei Huang) and DingXiaoH (Xiaohan Ding). Use when the user is writing a machine-learning / deep-learning / computer-vision / NLP paper and needs help finding the core idea, building the paper framework, writing the introduction or related work, improving readability and defensibility, preparing for the deadline, anticipating reviewer criticism, or judging whether a research idea is worth pursuing. Also trigger on Chinese phrasings such as 写AI论文、写顶会论文、深度学习论文写作、投稿NeurIPS/ICML/ICLR/CVPR、改论文、提升论文可读性、审稿意见、rebuttal、idea是否值得做.
version: 1.0.0
author: hzwer (Zhewei Huang) and DingXiaoH (Xiaohan Ding); packaged as a Claude skill
---

# Writing AI Conference Papers — Skill Router

This skill packages the community handbook *"Writing AI Conference Papers: A Handbook for Beginners"* so it can be applied directly to a user's manuscript. The full source text lives under `reference/` and is the authoritative content — **do not rely on memory; load the relevant reference section before advising.**

- `reference/handbook.md` — the complete handbook (idea → framework → introduction → related work → readability → defensibility → checklists → review/appendix).
- `reference/not-good-ideas.md` — patterns of research ideas that tend to fail review (compute-overwhelming, hyperparameter tuning, minor tweaks, incremental designs, weak evaluation, "ultimate" methods).

## Routing protocol

Every time this skill is invoked:

1. **Identify the task axis** from the request and map it to the handbook section(s):
   - *"Is my idea worth doing?" / topic selection / novelty worry* → `reference/handbook.md` §"Build a Paper from Scratch → Find the Core Idea" **and** `reference/not-good-ideas.md`.
   - *Paper structure / outline / framework* → §"Construct the Framework".
   - *Introduction drafting or rewriting* → §"Write an Introduction".
   - *Related work* → §"Describe the Related Work".
   - *Make it clearer / reviewers misunderstand / writing quality* → §"Readability Improvement" (Logical Strength, Defensibility, Shorten Confusion Time, Information Density, Detail Checklist).
   - *Deadline crunch / final pass* → §"Appendix → Checklist for the Last Few Hours".
   - *Anticipating or answering reviews / rebuttal* → §"Appendix → Common Negative Review Comments" and §"If the Paper is Not Accepted".
   - *Venue choice / timeline* → §"Appendix → AI Conference List" and §"AI Paper Production and Publication".

2. **Read the matched section(s)** from `reference/` in full before responding. Quote or paraphrase the handbook's concrete advice; do not invent rules it does not state.

3. **Apply it to the user's material.** When the user provides a draft, claim, idea, or section, diagnose it against the handbook's principles (logical strength, defensibility, confusion time, information density) and produce specific, actionable edits — not generic writing tips.

4. **Stay honest about scope.** This handbook is opinionated guidance aimed at beginners writing AI conference papers. It does not replace the target venue's official formatting/policy requirements; flag when the user should consult the call-for-papers.

## Style of help

- Be concrete and example-driven, mirroring the handbook's tone.
- When critiquing an idea, name the failure pattern from `not-good-ideas.md` if one applies, then suggest how to strengthen it.
- When editing prose, preserve the author's technical meaning and contribution while fixing structure, clarity, and defensibility.

---
name: sw
description: Gives a decision-oriented snapshot of a project by reading the repo, GitLab merge requests and Meegle work items. Use when picking up a project after a break, before planning the next move, when the user says /sw, or when asked where things stand.
---

# /sw —— 项目全景

给项目全景。它是产品、研发、测试共用的只读启动命令。**这是给人做决策用的，不是工作汇报** ——
简短、抓重点、不该说的别说。

`/sw` 只回答项目当前位置与下一步，不替代 `/bl` 对全部产品工作项做完整排序和排期。

## 先读

- 仓库：`AGENTS.md`、`README.md`、`docs/`、`docs/intent/`、最近的 commits、未提交改动
- GitLab：`glab mr list`（open 的 MR、谁在等谁）、`glab ci status`（如果有）
- Meegle：当前迭代里的工作项与状态（装了飞书项目 CLI 就直接读；没装就说明「未接入」，不要编）

不要为了显得全面而罗列文件。

## 按这个顺序输出

1. **目标** —— 一句话重述这个项目在解决什么。如果 `AGENTS.md` / `README.md` 里的目标
   已经过时、或与现在的代码矛盾，**直接指出来**。

2. **当前位置**
   - 当前分支、最近 5–10 个 commit（每条一行）、open MR、未提交改动
   - Meegle 上进行中的工作项与状态
   - 有没有半成品、坏掉的东西

3. **进度 vs 目标**
   - ✅ 已完成且能跑　🚧 在做（开始了没落地）　📋 计划未开始
   - 每条一行，按模块/功能分组，不按时间顺序

4. **下一步** —— 3–5 个具体动作，按 影响 × 紧迫性 排序。每个：
   - **做什么**（一行）
   - **为什么是现在**（一行 —— 杠杆在哪）
   - **依赖/卡点**（一行，没有写「无」）

   不要凑数。只有一件事重要就只列一件。

5. **风险与坏味道** —— 不一致的地方、正在腐烂的假设、堆积的技术/过程债、
   之后会咬人的东西。指出来就好，**不要顺手修**。

## 规则

- **只读扫描，不写文件、不改文件。**
- 文档说 X、代码做 Y —— 点名冲突，不要平均化。
- Meegle 状态与仓库现状对不上（工作项写着「已完成」但代码没合），**这是最值得报的一类**。
- 不确定就写「未知」，不要猜。
- 不要复述我的问题，不要废话。

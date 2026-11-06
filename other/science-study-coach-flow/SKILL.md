---
name: science-study-coach-flow
description: Use when someone is starting research and does not know the order of operations — a first-year student asking "从哪开始", "这一步要做什么", "我这样算不算做完了"; when a project feels stuck and it is unclear which prerequisite is actually missing; when explaining what a complete study requires end to end; when deciding whether the next move is reading, planning, collecting, analysing or writing. Also use before writing a Methods section, to prove every step actually happened.
---

# 流程指南：把"写论文"拆成十二个有门的阶段

## 为什么需要流程

研究最常见的失败不是"某一步做错了"，而是**顺序错了**：

- 先有数据，再挑检验 → p 值不再有意义。
- 先招人，再算样本量 → 要么白招，要么招不满。
- 先写完讨论，再选题 → 整篇要重写。
- 先投稿，再看报告规范 → 直接退修或 desk reject。

流程的价值不是仪式，而是让「还没做」在系统里有名字。`science_study_coach` 会把每个阶段的门
对着库里的真实状态判一遍：过、不过、还是"没留下记录"。

## 十二个阶段

| 阶段 | 一句话目标 | 硬门（不过就停） |
| --- | --- | --- |
| S0 选题 | 缩成一句可否证、一年做得完的话 | 课题已建、问题写成一句、学科已识别 |
| S1 文献 | 知道做到哪一步，且留检索记录 | 至少检索一次、库内文献 ≥10 |
| S2 设计 | 选一个审稿人认的设计，前置条件逐条落实 | 设计已定、假设可证伪、主结局唯一 |
| S3 样本量与预注册 | 招第一个人之前把 n 与计划锁死 | 样本量有依据 |
| S4 测量 | 每个变量落到具体测量动作 | 每个变量都有测量定义 |
| S5 采集 | 按方案采，过程留痕 | 数据进 `data/`、至少一次留痕执行 |
| S6 数据管理 | 别人能看懂、能跑起来 | 环境已锁、代码进 `code/` |
| S7 分析 | 用事前方法算，报效应量与区间 | 主分析已跑、有效应量与 CI |
| S8 图表 | 图能独立读懂、能直接排版 | 至少一张图、通过期刊自检 |
| S9 写作 | 按目标刊结构写，结论指向证据 | 稿子已建、目标刊已定、lint 无 block |
| S10 内审 | 用审稿人的方式打自己一遍 | 溯源链校验通过 |
| S11 投稿返修 | 按刊要求出件，返修逐条回应 | 四件套已出 |

## 读它的正确方式

`science_study_coach { projectId }` 返回三样东西，按这个顺序看：

1. **`current`** —— 你现在真正在哪个阶段。注意：它可能比你以为的早。三个门卡在 S2 却已经在写引言，
   这是最常见的状态。
2. **`nextActions`** —— 只列当前阶段最该动手的几条。优先阻塞项，其次警告项，再次"没留下记录"的，
   最后才是自查项（标 `reason: self-check`）。
3. **`stages`** —— 全流程一眼过。`✗` 是有阻塞，`·` 是有警告或未判定。

## 门的状态有四种，含义不同

| 状态 | 含义 | 该怎么办 |
| --- | --- | --- |
| `pass` | 库里查得到，且达标 | 往下走 |
| `fail` | 查到了但不达标 | 按 `fix` 修 |
| `skip` | **查不到**（还没做，或没留记录） | 去做，或补记录。**skip 不是过关** |
| `manual` | 机器判不了 | 自己去核对，核对完在心里打勾 |

`skip` 与 `pass` 的区别是这套流程最要紧的一点。把"没查过"当"没问题"，是绝大多数返修意见的来源。

## 第一次上手的最小路径

```
science_preflight                                     ← 环境体检
science_project_open { title, domain, question, ethics }
science_workflow_stages { stage: 'S2' }               ← 看这一步要什么
science_discipline_profile { domain }                 ← 这个学科怎么做研究
science_exp_plan { projectId, designId, effect: 0.5 }
science_stats { projectId, testId, data }             ← 有数据之后
science_figure { projectId, kind: 'bar', data, errorType: 'ci95' }
science_manuscript_new → lint → build
```

## 卡住的时候怎么问

不要问"我该怎么办"，问具体的那一句：

- "S3 的门说样本量没依据，我手上只有 pilot 的 12 个人，怎么定 n？" → 用 pilot 的效应量算，并在正文说明来源与不确定性。
- "S7 说假设检查有未处理失败项，是正态性没过，下一步？" → 用 `warnings[].fallback` 里的非参数检验重跑，报方向是否一致。
- "S10 溯源链有 hash-mismatch，怎么办？" → 先查是谁在什么时候改了库；改不回来就如实说明数据版本，不要删除记录重来。

## 三条全程规则

1. **缺失即 skip**：查不到、跑不了、没数据，标 skip 并说明缺什么，不许标 pass。
2. **先冻结后分析**：方案、主结局、样本量、分析计划在看数据之前定下来。看过数据再改，必须在稿件里声明为探索性。
3. **不预测录用**：这套流程不给中稿概率。它只保证"该做的都做了且有记录"，不保证结果讨喜。

---
name: paper-using-skills
description: |
  《Claude Code 科研手记》论文写作纪律 skill 集的入口与强制触发器。
  建立"1% 可能适用就必须调用"的硬规则，列出本系列各核心纪律 skill 的触发条件，
  防止用户在赶论文 / 紧张 / 熟练之后跳过该有的检查动作。
  Use when 开始任何科研写作场景：写论文、改论文、整理参考文献、
  画图、整理导师反馈、跑批量任务、改 Word、提交前检查 等。
---

# paper-using-skills：论文写作纪律入口

## 核心理念

科研写作翻车，不是因为不知道，是因为知道但累了 / 赶时间 / 觉得这次不一样而跳过。
本系列 skill 把"踩过坑后才悟出来的动作"，变成 AI 在动手前必须先执行的检查点。

> 当你觉得"这次不用走流程也行"，那就是必须走流程的时候。

---

## 强制规则

**遇到任何论文写作请求，在调用任何工具之前，必须先扫一遍下方"触发对照表"。匹配则调用对应 skill。**

匹配标准：1% 可能相关就调用。调用后发现不适用，再退出。
不要"凭印象"省掉这一步。

---

## skill 触发对照表

| 触发场景 | 调用的 skill | 防什么灾 |
|---|---|---|
| 新论文项目第一次开会话 | `paper-claude-md-bootstrap` | AI 反复要你解释研究背景 |
| 用户发来"改一下 / 整理下 / 润色"等模糊任务 | `paper-confirm-before-doing` | AI 自由发挥跑偏 |
| 用户在一次会话里提了多件事 | `paper-one-session-one-task` | 上下文污染、决策劣化 |
| 跨多文件批改、术语统一 | `paper-protect-terminology` | 专业术语被同义替换 |
| 编辑 .docx / Word 文件 | `paper-backup-before-word` | XML 损坏、原文被覆盖 |
| 处理 ≥ 30 条目的批量任务 | `paper-pilot-before-batch` | 全量跑炸了改不回来 |
| 大批量引用 / 术语 / 格式核查 | `paper-parallel-audit` | 串行慢 + 中间挂了从头来 |
| 用户拿来导师录音、便条、口头反馈 | `paper-translate-advisor-feedback` | AI 听不懂学术口语 |
| 改动核心声明 / 研究问题 / 主要结论 / 因果关系 / 方法边界 | `paper-logical-consistency` | 改一处忘了改其他章节，论证穿帮 |
| **任何对论文文段做润色 / 改写 / 通顺化** | **`chinese-de-aigc`** | **改完后科研叙事被改成 AI 腔，AIGC 检测率飙升、读起来像没做过研究的人写的** |
| 写完准备发给导师 / 提交 | `paper-verify-before-handoff` | AI 写得太流畅让人放松警惕 |

---

## Skill 优先级

多个 skill 同时命中时，按以下顺序执行：

1. **`paper-confirm-before-doing`** —— 模糊任务在所有动作之前先确认
2. **场景 skill**（backup-before-word / protect-terminology / translate-advisor-feedback / 等）—— 决定怎么做
3. **`chinese-de-aigc`** —— 任何文段改写 / 润色 / 通顺化都必须按它的五步闭环走（定位 → 诊断 → 改写 → 自评 → 复查）；不是"改完之后再过一遍"，而是改的过程中就遵循它的方法论：保科研叙事美感的同时降 AIGC 检测率
4. **`paper-verify-before-handoff`** —— 交付前最后一道闸（含 AIGC pattern 自查项）

> `chinese-de-aigc` 是独立的 peer skill，按它自己的 description 自然触发即可；本表只是让你知道它存在。
> 是否调用由它自己的触发条件决定，第 4 步 verify 阶段会做 AIGC 兜底自查。

---

## Red Flags：以下念头 = 立即停止，回去查 skill

- "这个任务很简单，直接做就行" → 简单的任务正是出错时不被发现的
- "用户没说要走流程，我先做了再说" → 用户没说 ≠ 不需要
- "时间紧，跳过流程更快" → 跳过流程返工的时间一定比走流程长
- "我刚才已经备份过了" → 上一次备份不是这一次的备份
- "我了解这个用户的习惯" → skill 不为习惯让步
- "这是显而易见的事" → 显而易见的事踩了 N 次坑才写成 skill
- "这次跟书里写的情况不太一样" → 99% 的"这次不一样"都一样

任何上述念头出现 = 必须读对应 skill。

---

## 系列与单本书的关系

本 skill 集是《Claude Code 科研手记》一书的**可执行版本**。书里讲的每条教训，对应一个 skill。
书读不读得完无所谓，skill 装上后会在该触发的时候自动提醒你。

## 想加一条新规则？

发现自己 / 用户踩了一个本系列没覆盖的坑 → 用 `paper-writing-discipline` skill 把它提炼成新 skill。

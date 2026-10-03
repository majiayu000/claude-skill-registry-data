---
name: handoff
description: "Session 收尾：更新 HANDOFF.md、把本次纠正以 [LEARN:tag] 追加进 MEMORY.md、必要时追加 research-log.md 并派 claim-verifier 核查既有结论、覆写 current-focus.md。context 快满或准备结束 session 时用。"
disable-model-invocation: true
allowed-tools: Read, Edit, Write, Glob, Task, Bash(git status:*), Bash(git log:*), Bash(git diff:*)
---

# Session 收尾

把本次 session 的状态落到磁盘，让下一个 agent 能接上。

先跑 `git status --short` 和 `git log --oneline -5`，用实际状态写，不要凭记忆。

## 1. HANDOFF.md（本次状态）

在文件**顶部**追加一节（新的在上，老的往下沉），格式固定，**照抄字段名**：

```text
## Session 2026-07-22
- 完成: <一条一件事，带 文件:行号 或 commit hash。可以多行，一行一条>
- PENDING: <下次第一件事，具体到「打开哪个文件、跑哪条命令」的程度>
- 坑: <具体现象 + 怎么绕过去的。没踩到就写「无」>
```

**这是写给下一个 agent 的一封信，不是工作日志。** 判据：

- 短。整节 20 行以内。
- 具体。「修了 dataloader」没用；「`data/loader.py:88` 的 shuffle 在 eval 时也生效了，已关掉」才有用。
- 只写下次用得上的。这次想过但放弃的思路，除非会被重新想一遍，否则不写。
- PENDING 写成可执行的下一步，不是愿望清单。

**只保留最近 3 节**，更早的直接删掉——HANDOFF 是易过期文件，越长越误导（历史在 git 里）。

## 2. MEMORY.md（跨 session 教训）

把本次**用户对我的纠正**追加到文件**末尾**（累积式，新的在后），一条一个多行块：

```text
### [LEARN:scope] 不要顺手改 plan 之外的文件，即使只有一行
- 现象: 顺手把相邻函数重命名了，validate 阶段没法对照 plan 逐条核。
- 原因: 「反正只有一行」把范围蔓延合理化了；plan 的「不在范围内」当时没读。
- 对策: 看到的问题一律追加到 plan.md 的「发现但未做」，本轮不动。
- 来源: Session 2026-07-22
```

四行缺一不可，**「原因」是一条 LEARN 里最值钱的部分**——只有它能让下次真的避开，
「现象 + 对策」没有原因就退化成一条不知道为什么要守的规矩，早晚被绕过去。
tag 用短英文词（scope / numbers / repro / env / data / tooling ...），便于以后 grep。

**禁止为了填表而编造 LEARN 条目。** 本次用户没纠正过我，这一节就不动。
空着的成本是零，编造出来的条目会在后面每个 session 被当成真教训遵守，成本是永久的。

判据：一条 LEARN 必须能指到本次对话里一句真实的用户纠正。指不到就不写。

## 3. research-log.md（实验事实，append-only）

本次**跑过实验或得出了带数值的结论**才写，否则跳过。追加到文件**末尾**，格式与 `/exp` 一致：

```text
## 2026-07-22  run_id: 20260722-<slug>
- 假设:
- 成功判据:
- git hash:
- 结果:
- 结论: [AI-DRAFT] ... [source: 20260722-<slug>]
```

只 append，**永不修改或删除已有条目**——它是这个项目唯一的事实底账。

### 派 claim-verifier 核一遍（本次动过代码就做）

本次改动**可能让 research-log.md 里的既有结论失效**时（改了训练/评测/数据处理路径、
改了指标计算、改了 config 默认值、重构了被结论引用的模块），**派 `claim-verifier` subagent**
把既有量化 claim 逐条映射回今天的代码和产物，判定它是否仍然成立。

它只判定、不改文档。拿到回报后：失效的结论**不要回去改旧条目**，在末尾追加一条新的，
写明推翻的是哪条、为什么。判定不了的就在 HANDOFF 的 PENDING 里留一条。

## 4. .context/current-focus.md（当下焦点）

**覆写**（不是追加）。内容就三行以内：现在在攻什么问题、卡在哪、下一动作。
它是给 /kick 快速定位用的，长了就失去意义。

## 防重叠规则（写死，不要越界）

| 文件 | 只放 | 不放 |
|---|---|---|
| `HANDOFF.md` | 本次 session 的状态、PENDING | 通用规则、实验数值 |
| `MEMORY.md` | 跨 session 的规则和教训 | 本次进度、具体实验结果 |
| `research-log.md` | 实验事实、配置、数值结论 | 计划、待办、感想 |
| `.context/current-focus.md` | 当下一句话焦点 | 历史、细节 |

同一条信息只写进一个文件。写重了，下次读的时候两份会不一致，然后没人知道信哪个。

## 收尾输出

1. 列出改了哪几个文件、各加了几条
2. 明确说「MEMORY.md 本次未新增（无用户纠正）」——如果确实没有
3. 提示用户：**「建议现在 commit 一下这些记忆文件，然后就可以 /clear 或结束 session 了。」**
   （不要自己 commit。）

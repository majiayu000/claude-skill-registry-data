---
name: prompt-pro
description: |
  Rewrite the user's rough task request into an executable brief, then execute the brief
  instead of the raw request. Load this skill at the START of any non-trivial task request —
  building, fixing, auditing, writing, deploying, refactoring, investigating — because a vague
  request and a specific one produce different results, and the cost of rewriting is far lower
  than the cost of guessing wrong. Also trigger on explicit asks like "优化 prompt" /
  "prompt Pro" / "把这个需求改写得更好".
  Do NOT use it for: pure Q&A with no state change, single trivial actions ("打开这个文件",
  "跑一下这条命令"), or when the user already supplied a precise spec with checkable
  acceptance criteria — rewriting those wastes tokens and can drop detail they cared about.
descriptions:
  zh-Hans: "把用户的粗略请求改写成可执行提纲，再照提纲执行。任务开头就加载。"
displayNames:
  zh-Hans: "Prompt Pro"
---

# Prompt Pro

把粗请求补成可执行提纲，再执行提纲。提纲是**输入**，不是交付物。

## Procedure

1. **判定要不要重写**。出现下面任一条就跳过，直接做：
   - 一句话就能做完的事，且不改任何状态（看一眼、查一下、回答问题）
   - 用户已经给了可判定的验收标准（数字、文件名、退出码、清单）
   拿不准就重写——多花几行字，比猜错方向便宜。

2. **先看真实系统，再写提纲**。提纲写在假设上就是一个错的前提——
   评测里出现过：提纲先写「复用现有脚本当测量底座」，随后 grounding 发现那些脚本
   断言的是正确性不是性能，方向整个作废。
   先读源码/配置/现有工具，再落笔。**grounding 的成本高于提纲本身，这是正常的，
   也不要用提纲替代它**——提纲是压缩，不是取���。

3. **补齐缺口**。只用下面 5 个槽位，**只补用户没说的**，一个都不发明：

   | 槽位 | 判据 |
   |---|---|
   | 目标 | 一句话说清交付什么。动词开头。 |
   | 验收 | **可判定**：退出码、字节数、逐位相等、勾选项。「好看」「差不多」不合格 |
   | 范围 | 动什么 + **不动什么**。「不动什么」比「动什么」更常被漏 |
   | 约束 | 禁止项、硬红线、必须走的通路 |
   | 输出 | 交付形态：文件 / 提交 / 消息；要不要 PR、要不要确认 |

   审计类任务额外加一条：**该说的没说**——文档写得比事实更保守，也算错。
   人和模型都天然只找「说过头」的错，这条必须显式写出来。

   每个槽位一到两句。**一行塞不下就拆行**：压行数换可读性是亏的。

4. **交出去执行**。执行的是提纲，不是原始请求。过程中拿到新信息就更新提纲，
   不要执行到一半才发现自己理解错了目标。

5. **收尾时交代**：补了哪几条、跳过了哪条、有什么假设。
   **不确定的地方要标出来，别用确定的语气说没把握的话。**

## Output contract

- 改写后的提纲，每个槽位一到两句，放在动手**之前**。
- 然后是真正的交付物。
- 提纲**不单独成篇**。用户要的是结果，不是我的写作练习。
- 提纲和实际做法不一致时，说明为什么改了。

## Failure handling

- 缺的信息会改变结果、且无法从上下文推断 → **直接问**，不要脑补。
  这时候一条问题比一份猜出来的提纲有用得多。
- 用户否决了提纲 → 按用户的改，不要争辩。用户比提纲权威。
- 提纲在执行中显得多余（任务比预想简单）→ 说明它多余，然后照做。
  不要为了「走完流程」硬塞步骤。

## Examples

Input: `看一下 doc 和源码对不上���地方，改一下`

Output:
```
提纲：审全部文档与源码注释，找出与真实行为不符处并修正。
验收：每条错都有真值证据（跑出来/磁盘上核对过），并区分真错与我看错。
范围：只改文档和注释，不改代码行为；改完跑现有闸。
约束：直接提交，不开 PR。
输出：一张表（错处 → 真相 → 改成什么）+ 提交结果。
```
然后执行审计。
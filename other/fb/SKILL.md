---
name: fb
description: Pulls every unresolved thread on a merge request, judges each one, proposes fixes, and resolves threads only after replying. Use when your MR has review comments, when the user says /fb, or when asked to handle review feedback.
---

# /fb —— 处理 MR 上的反馈

## 先把 comment 拿全

MR 上的反馈分散在三处，**只看一处会漏**：

```bash
glab mr view <id>                                   # MR 描述与顶层讨论
glab mr note list <id>                              # 所有 discussion（含行内）
glab api "projects/:fullpath/merge_requests/<iid>/discussions"   # 完整结构：谁提的、resolved 没、锚在哪一行
```

用 API 那条拿 `id` / `resolved` / `position`，因为要按 discussion 逐条 resolve，
而 `resolved: false` 的才是待办。

## 逐条判断，不要照单全收

对每条 comment 先判断**它说得对不对**：

- **对** → 给修复方案（改哪个文件、怎么改、影响面）
- **不对 / 不该现在做** → 写清理由：为什么这里是有意为之，或为什么它属于另一个工作项
- **看不懂** → 在 thread 里回问，不要猜着改

**先给方案，等我点头再动手改代码。** 一次性把所有 comment 的处理意见列出来，
让我一次决策，而不是改一条问一次。

输出形状：

```
1. <file:line> <comment 摘要>
   判断：合理 / 不合理 / 需澄清
   处理：<怎么改，或为什么不改>
```

## 改完再 resolve

每条 discussion 只有两种结局：**修掉**，或**带理由不修**。两种都要先回复，再 resolve：

```bash
glab mr note create <id> -m "..."          # 回复（或在 discussion 里回）
glab mr note resolve <discussion-id> <id>  # 回复之后才 resolve
```

**未 resolve 的 discussion 不得合入。** 只读不处理的 thread 不要 resolve ——
resolve 表示这条已经被回答，不是「我看过了」。

处理完报告：改了几条、驳回几条（各自理由一句话）、还剩几条未 resolve。

## Red Flags

- 只用 `glab mr view` 拿反馈，漏掉行内 discussion
- 反射性地照 comment 改，没判断它对不对
- 改完直接 resolve，没在 thread 里回复
- 一条 discussion 里塞了多个问题却整条 resolve 掉

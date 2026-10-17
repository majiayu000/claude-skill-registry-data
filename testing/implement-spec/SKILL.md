---
name: implement-spec
description: "把 /to-spec 和 /to-tickets 的产出实现为代码。"
disable-model-invocation: true
---

你会拿到一份 spec。这份 spec 应该有与之关联的 tickets，描述如何实现这份 spec。

应该已经向你提供了 issue tracker。如果没有，告诉用户运行 `/setup-rolex-skills`。

目标是把整份 spec 实现在一个 **integration branch** 上，并以 issue tracker 关闭工作的方式解决每一条 ticket。

Tickets 不是步骤列表。它们是一张带有 blocking edges 的 **task graph**。这意味着始终存在一个由可认领 tickets 组成的 **frontier**。

与 subagent 之间的通信应当稀疏。主要通过 **context pointers** 沟通：指向 spec、tickets、research notes 和此前的 commits。不要重复通过 pointer 已经可以获取的信息。

**implementer subagent** 应尽可能在后台运行，以获得最大并发。

## Steps

1. 阅读 spec 和 tickets，理解任务图。

2. （可选）使用一个 **exploration subagent** 完成 tickets 所需的一切探索——相关的代码库文件或外部文档。确保 exploration subagent 可以保存文件——它应把 markdown 笔记保存在仓库之外的一个目录里，供后续所有 subagent 访问。这样 **implementer subagent** 就能专注于实现而不是探索。

3. 创建 integration branch。如果 issue tracker 通过 PR 关闭工作，或用户要求开 PR，在完成步骤 5 的第一次 merge 后开一个 draft PR（领先 main 零 commit 的分支开不了 PR），并标记为关闭该 spec 及其 tickets。

4. 使用 **implementer subagent** 实现每条 ticket，各自在自己的 worktree、自己的分支上工作。每个 implementer subagent：
   - 开始前确认自己的 worktree 基于 integration branch，若不是则 reset 到其上；
   - 调用 Skill tool 的 `tdd` 来构建该 ticket；
   - 在报告完成前，把 integration branch 的 tip merge 进自己的分支。

5. 一旦某个 **implementer subagent** 完成，用一个 **merger subagent** 把它的工作 merge 到 integration branch。

6. 如果这改变了可用 tickets 的 **frontier**，再启动更多 **implementer subagent** 去处理新 tickets。以此实现最大并发。

7. 全部 tickets 完成后，在 integration branch 上调用 Skill tool 的 `code-review`。用单个 **implementer subagent** 修复 code review 提出的所有问题。

8. 如果存在 draft PR，将其标记为 ready for review。否则，按 issue tracker 关闭工作的方式逐条解决 tickets，并报告 integration branch。

9. 清理所有 **implementer subagent** 的 worktree。

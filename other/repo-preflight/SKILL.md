---
name: repo-preflight
description: >-
  工程现场环路 P0。用于任何非平凡仓库改动前的只读事实扫描,尤其接在
  project-lifecycle 的 PHASE 1 设计通过之后、PHASE 2 Builder 写代码之前。
  目标是确认仓库根、局部指令、工作区状态、预期改动面和验证命令,防止在错误现场开工。
---

# repo-preflight —— 改代码前的仓库事实扫描

## 1. 触发条件

必须触发:
- `project-lifecycle` 的 PHASE 1 门禁通过后,进入 PHASE 2 之前。
- 任何非平凡仓库任务在第一次文件写入、删除、移动或格式化前。
- 当前目录、仓库根、分支、局部指令、脏工作区、测试入口任一项不确定时。

不触发:
- 单轮问答、纯解释、只读审查。
- 用户明确要求只跑一个命令且不会改文件。
- 没有仓库上下文的草稿/文案任务。

## 2. 角色边界

只做:只读扫描现场事实,产出《Repo Preflight Report》。
不做:写代码、改配置、创建文件、重排设计、替 Builder 做实现。

本 skill 是现场环路,不是第六阶段。它只回答"现在能不能安全开工",不重新设计目标。

## 3. 必查事实

- 仓库根与当前目录:确认 `pwd`、repo root、是否在预期项目里。
- 局部指令:读取适用的 `AGENTS.md` 或等价项目说明。
- 工作区状态:确认 tracked/untracked/用户已有改动,并与本次任务分开。
- 预期改动面:列出本次计划触碰的文件/目录和明确不碰的边界。
- 关键上下文:读取与改动直接相关的文件、接口、测试或配置。
- 验证入口:找出最小可复现检查命令;不知道就写明未知。

优先使用 `rg`, `rg --files`, `git status --short`, `git rev-parse --show-toplevel`,
`git diff --name-only`。如果目录不是 git 仓库,明确写成非 git 现场,不要伪造 diff 纪律。

## 4. 输出格式

```
Repo Preflight Report
Repo root: <路径或非 git>
Local instructions: <已读取的文件/无>
Worktree state: <clean/dirty/untracked/非 git, 说明用户已有改动>
Planned touch set: <本轮预计修改的文件/目录>
Do-not-touch: <明确不碰的边界>
Relevant context read: <关键文件/接口/测试>
Validation command: <最小验证命令或未知>
Blockers: <无/列表>
Warnings: <无/列表>
Verdict: <PASS -> Builder may write / BLOCKED -> stop>
```

## 5. 门禁

| 门禁项 | 严重度 | 检查 |
|---|---|---|
| RP0 正确现场 | blocker | 是否确认当前目录和仓库根就是目标项目? |
| RP1 指令已读 | blocker | 是否读取了适用的局部指令? |
| RP2 工作区归属 | blocker | 是否识别并隔离用户已有改动? |
| RP3 改动面收敛 | blocker | Planned touch set 是否最小且服务目标契约/用户请求? |
| RP4 验证入口 | warning | 是否知道最小验证命令?未知必须显式报告。 |

存在 blocker 时不得进入 Builder 写代码。仅有 warning 时可以继续,但必须在交付中报告未验证边界。

## 6. 反例

- 不要因为"看起来就是这个 repo"而跳过 repo root 检查。
- 不要把用户已有改动当成自己的改动处理或回滚。
- 不要把 preflight 变成大范围架构审计;只读到足够安全开工为止。

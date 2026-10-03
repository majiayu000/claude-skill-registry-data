---
name: briefbound-development-cleanup
description: "Use when a verified or integrated software change has concrete temporary artifacts, generated noise, task-owned background processes or listeners, stale claims, merged local branches, disposable worktrees, or a known PR lifecycle state that requires deferred or post-merge local closeout, or when the user explicitly asks to remove development residue or old branches."
license: MIT
---

# Briefbound Development Cleanup

## 目标

保护未合并工作和证据，清掉可证明噪音并收尾 branch、worktree 与 claim。

无法证明“可重建、已吸收、无 owner”就保留；清理不扩大范围。

## Briefbound task contract

- Context Boundary: 真实根目录、实现范围、验证、Git target/base/head、working tree、残留、task-owned PID/listener、worktree、claim 和清理授权。
- Output Contract: `CLEAN / NOOP / DEFERRED_INTEGRATION / BLOCKED`、已删除项、保留项、延后条件、清理后证据和 Route Out。
- Allowed Action: 先只读审计；只删除已证明属于本轮且可重建的本地残留，只停止已证明由本任务启动或依赖的精确进程树。删除本地 branch/worktree 需用户明确清理、项目长期策略，或同一任务“完成开发到 PR”许可且已验证 PR 合并。远程分支、push、合并、发布和无法归属的文件或进程不自动处理。
- Success Evidence: 清理后 Git、worktree 和 registry 符合预期；源码、用户改动、未合并提交和必要证据仍在。
- Stop Condition: 根目录或 integration target 不明、工作区 dirty 且归属不清、process owner 或 data root 不明、branch 未吸收、worktree 被占用、claim 仍 active、路径安全无法证明、删除需要远程或 force 动作。
- Route Out: 当前开发 owner、`briefbound-autonomous-collaboration-loop`、`briefbound-thread-coordination`、`briefbound-pr-review`、`briefbound-router` 或 BLOCKED。

## 统一调用契约

- 只处理 Briefbound task contract 范围；不匹配时回 `briefbound-router` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文，完成只报状态、产出、证据和剩余风险；代码、命令、路径、Git 状态、错误原文、API/协议、skill 名和枚举保留原样；Route Out 仅以 Briefbound task contract 为准；有自然闸门（需用户裁决、批准或被外部阻塞）时末行 `下一步建议: <一个具体动作>`，否则声明继续已授权工作。

## 进入时机

- 只有当前任务已知创建了临时产物、任务专用缓存、scratch 文件、后台进程/listener、claim、feature branch/worktree，或用户明确要求清理时，才做静默清理检查并加载本 skill。
- 没有已知候选时直接收口，不扫描全仓寻找可能的噪音，也不输出 `NOOP`。
- 合并前清理开发残留，但保留仍用于 PR/合并的 branch/worktree，状态为 `DEFERRED_INTEGRATION`；合并后再次收尾这些 Git 资源。
- 纯规划、只读审查、研究归档或未验证开发不进入删除阶段。
- 由 `briefbound-autonomous-collaboration-loop` 调用时，沿用其本轮安全本地清理授权；已证明被本地 `main` 吸收的任务 branch/worktree 和已完成 claim 不再逐项询问。

## Post-PR Closeout Gate

同一任务 PR 读取 `references/post-pr-closeout.md`：`PR_OPEN` 关闭空闲 claim 并保留 Git 现场，`PR_MERGED` 验证吸收后本地收尾，`PR_CLOSED_UNMERGED` 保留工作；远程分支删除必须单独授权。

## 审计与分类

先确认真实 repo root、当前 branch、integration target 和本轮 owned surface，再读取：

- `git status --short --branch`、相关 diff、untracked/ignored 候选；
- `git worktree list --porcelain` 和本地分支占用；
- `git merge-base --is-ancestor <branch-tip> <target>` 或等价吸收证据；
- coordination registry 中的 Agent/claim 状态（当前环境无 registry 时跳过此行，以 Git worktree/分支占用为准，见 `briefbound-router` 的 `references/harness-compat.md`）；
- 项目规则、官方 closeout 命令和 Windows junction/reparse point。

把候选分成四类：

- `REMOVE_NOW`：本轮创建、可重建、删除后不影响行为或证据。
- `CLOSE_AFTER_INTEGRATION`：当前 feature branch/worktree 已完成但尚未被 target 吸收。
- `KEEP`：源码、用户内容、验收证据、未合并提交、归属不明或仍被依赖。
- `BLOCKED`：删除需要 force、远程动作、所有权裁决或路径风险未解除。

## 噪音清理

- 只按明确的 literal path 删除，不使用 `git clean -fdx`、仓库根目录递归删除或宽泛通配符。
- `git clean -ndX` 只能用于预览；`node_modules`、`.venv`、下载缓存、模型/数据、密钥、用户日志和共享依赖默认保留。
- patch、scratch、测试/构建缓存、截图和日志仅在本轮创建或规则明确可丢弃时删除。
- 多会话的可重建测试缓存最终统一处理；删除受阻且不影响 tracked 交付时，记录候选并停止换命令。
- accepted plan、迁移、lockfile、fixture、snapshot、基准结果和失败复现不是噪音，除非已有替代且用户明确同意。
- 不修改 `.gitignore` 来隐藏无法解释的残留；先判断它为何存在。

## 本地资源收尾

关闭 branch、worktree、claim 或 task-owned runtime 时读取 `references/local-resource-closeout.md`；禁止 force 删除 dirty worktree。

## 执行与验证

1. 先输出或内部建立候选分类；有安全候选才执行。
2. 按 exact path 和单个 Git 对象逐项清理，每一步失败就停止扩大动作。
3. 重新读取 Git、worktree 和 registry；清理触及源码、依赖或运行环境时才重跑受影响验证，普通缓存删除不重复完整测试套件。
4. 工作区只剩预期源码/文档变更，或已 clean；所有延后项都有明确触发条件。

## 低噪声输出

误路由后无候选时直接返回原 owner，不输出清理报告。有动作时仅汇报：已清理、保留/延后、验证证据，以及有自然闸门时的一个下一步建议；不打印完整文件树、全部分支或命令日志。

只有远程删除、force、dirty/未合并内容、归属冲突或路径不确定时才停下来询问。用户已明确授权的安全本地清理不重复确认。

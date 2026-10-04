---
name: git-workflow-standard
version: 1.2.0
description: 生产级 Git 协作 SOP:受保护分支按仓库 tier 门禁、改动从 feature 分支起、集成默认 squash、rebase 判据、提交不加 AI 签名。任何 git commit / push / 开 PR / 建分支 / rebase / 合并场景加载;agent 写完代码准备提交前必读。Use when committing, pushing, opening a PR, branching, rebasing, or merging.
---

# Git Workflow（协作 SOP）

agent 与人共用的 Git 工作流规范。**完整版 + rationale 见 `references/git-workflow-standard.md`。**

> 双层落地:本 skill 是**软层**(write-time 预防)。不可逆动作(直推受保护分支、force push)的最终防线是**硬层**——GitHub Ruleset(归 你的 IaC 仓 / IaC CTO)。**两者都在,不互替**;硬层内部按三档 tier 渐进加码。

## 硬门禁契约（与服务端硬层对接缝，三档 tier）

canonical = 你的 IaC ruleset,本 skill 只镜像行为契约;具体仓的 enrollment 以 IaC 为准:
- **Tier 1 baseline(所有仓,含未来仓)**:地板 = **禁 force-push + 禁删分支**;不要求 PR、不强制线性历史 → 小仓 / 文档仓可直推、直接合。
- **Tier 2 PR gate(显式白名单)**:**require PR + 禁 force-push + 禁删分支**;平台默认 `required_approvals=0`,允许作者 self-merge,不统一强制 CODEOWNERS / last-push approval / conversation resolution / linear history / status checks。**跨人评审是建议**,repo-local gate 明确升格时才是硬门。
- **Tier 3 required CI(单独显式 enrollment)**:在 Tier 2 上叠加 required status checks;仅显式接入的仓生效,aggregate check **MUST always-report**(上游失败 / skip 也要产出终态),避免 required check 永久 pending。

下面「你 MUST 做的」是 **Tier 2 / Tier 3 仓**的 SOP;**Tier 1 仓**只需守 §5(提交信息)+ §6(受保护分支不 force-push),其余可简化(直推 / 直接合)。**你的仓走哪档,在该仓 AGENTS.md 声明**,agent 进仓先读。

## 你 MUST 做的

1. **从最新 base 起 feature 分支**:`git switch -c <type>/<slug>`(`feat/` `fix/` `chore/` …),不在受保护分支上直接改。
2. **受保护分支禁直推**:`main`/`master`/`develop`/`dev`/`release/**`/`project/*` 一律走 PR,MUST NOT `git push` 直推、MUST NOT `push -f` 改写其历史。
3. **rebase 是条件动作、不是仪式**:push/PR 前 `git fetch`,查 base 动没动(`git log <branchpoint>..origin/<base>` 空 = 没动)。**没动 → 什么都不做**(空 rebase 是 no-op,不是漏步骤);**动了且碰了你改的文件 → rebase 或把 base merge 进来**解冲突再 PR;**动了但文件不重叠 → 可不动**。并发会话下 `fetch`+检查必做,但"检查"≠"每次都 rebase"。评审/阅读用途的差分用 three-dot(`origin/<base>...HEAD`,merge-base 差分)——stale-base 两点差分会把他人 commit 的反向删除误读为回退;rebase 只服务 push/merge。
4. **走 PR,只把已配硬门当硬门**:PR 描述讲清 what/why;Tier 3 等 required checks 绿再合;review / CODEOWNERS / last-push / conversation resolution 仅在 repo-local gate 明确要求时阻断合并,否则跨人评审只是建议;**合并方式按本仓声明的集成策略**(见 §集成策略)。
5. **提交信息**:讲清意图,**MUST NOT 加任何 AI / Claude 签名行 / co-author**。
6. **force push 仅限自己的 feature 分支**,优先 `--force-with-lease`;受保护分支永不 force。

## 集成策略（默认线性，2026-06-25 修订）

**默认 squash**;可选 **rebase-merge**(同为线性)。**merge-commit 只有一种 sanctioned 用法:长驻集成分支批式 PR 进 base。**
- **squash**:线性、每 PR 一个原子全绿 commit、易 revert、bisect 友好 —— 默认。
- **rebase-merge**:偏好保留 PR 内分块 commit 且要线性的仓。
- **merge-commit(仅长驻集成分支 → base)**:`dev` / `develop` / `release/**` / `project/*` 批式 PR 进 base 用 merge-commit 保祖先(squash / rebase-merge 重写 SHA,长驻分支与 base 分叉、下一批 PR 重现旧 commit,详见 references §4)。feature → 任何 base 仍走 squash / rebase-merge(线性)。
- **为何 feature PR 弃 merge-commit**:全 agent、无人读 git 历史 → merge-commit 卖点失效(详见 references §4)。**这是 SOP 默认,不是 Tier 2 服务端硬门**;repo-local 若强制 linear 再按本地门执行。
- **对抗评审的知识**(约束 / 被否方案)落 **ADR + PR 记录 + commit trailer**,不进 commit graph —— squash 丢 exhaust 不丢 knowledge。
- **合后判定**:squash / rebase-merge 后原 head 不必是 base 的 ancestor,**MUST NOT** 用 ancestry 单独断言“未合入”或授权清理。历史合入查 forge 的精确 PR;当前内容查 tree / test;部署查不可变 release provenance(见 references §5.1)。
- **发布证据**:release CI 对 exact pushed digest 完成 smoke 后、GitOps write-back 前,必须产出 immutable `release-evidence/v1`(schema 见 references):只用 `service.version` release tag 贯穿部署,必含完整 `git_sha` 与 `image_digest`;不另造 `release_id`,也不把 SHA/digest 复制到每条 telemetry。

## MUST NOT
- 任何 tier 都不得 force-push 受保护分支；Tier 2 / Tier 3 不得直推(Tier 1 可按 repo-local 规则直推)。
- 用与本仓声明不符的方式合并。
- 绕过本仓已配置的 required CI / review 硬门合入受保护分支。
- 提交里出现 secret / 凭证(见 `observability-standard` 边界纪律)。

## 关联
- 完整规范 + rationale:`references/git-workflow-standard.md`
- Local-first final-image Docker E2E、`pre-push` critical-path 触发、release CI single-build/exact-image 与 Release Evidence 规则见 `references/git-workflow-standard.md` §10；机器合同见 `references/release-evidence-v1.schema.json`。
- 硬层(Ruleset / CODEOWNERS / required checks)= 你的 IaC 仓(IaC CTO 维护);三档 tier 的定义与 enrollment 见该仓。

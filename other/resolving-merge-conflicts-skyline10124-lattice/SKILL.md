---
name: resolving-merge-conflicts
description: 根据两侧变更意图解决正在进行的 merge 或 rebase，并执行相关验证。
---

先按当前宿主读取 [Pi 说明](../../README.pi.md)或 [Delta 说明](../../README.delta.md)，再读取仓库内的[源工作流](../../skill-sources/resolving-merge-conflicts/SKILL.md)。

在当前获授权工作区核对 Git 操作状态、双方原始意图及实际冲突，保留无关暂存和未暂存内容。逐块解决；涉及产品或规则选择时询问，不以机械选一边消解冲突。

编辑文件、暂存、continue/commit 和推送分别核对授权，只暂存本次已核验文件，不照搬“stage everything”。可能打开编辑器的已授权命令设置 `GIT_EDITOR=true`。

按影响验证后再完成获授权的 Git 操作。强推与绕过保护遵循现行 Git/权限合同的禁止条款；源流程的 always continue/never abort 不覆盖人类裁决和失败后先确认状态的要求。

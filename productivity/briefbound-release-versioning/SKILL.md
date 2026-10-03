---
name: briefbound-release-versioning
description: "Use when the user asks to cut a release, write or update a changelog, decide a semver bump, run pre-release checks, draft release notes, or prepare a rollback plan; do not use for single bug-fix execution, deployment or runtime operations, or contract compatibility analysis itself."
license: MIT
---

# Briefbound Release Versioning

## 目标

把一组已完成的变更组装成一个可发布的版本：判定版本号跳档、维护 changelog、跑发布前检查、撰写发布说明并备好回滚预案。它管版本产物与发布动作，不做单点实现，也不做部署操作。

## Briefbound task contract

- Context Boundary: 自上个版本以来的变更清单、现有 changelog 与版本文件、api-contract 的兼容性判定结论、发布范围与消费者约束。
- Output Contract: 版本号判定与跳档理由、按规范分组的 changelog 版本块、发布前检查结果、发布说明、回滚预案；版本文件与 tag 建议一并给出。
- Allowed Action: 直写 CHANGELOG.md、版本文件与发布说明文件；读取仓库任意文件取证；不执行部署，不向消费者发通知。
- Success Evidence: 版本号与变更内容跳档一致且逐条可溯源；changelog 每条面向使用者可读；检查清单逐项有结论；回滚步骤可执行且不可逆点已标注。
- Stop Condition: 变更范围不明（无法界定本版本包含什么）、版本策略与既有仓库约定冲突需用户拍板、或发布存在未消除的阻塞项。
- Route Out: 契约破坏判定与迁移路径 `briefbound-api-contract`；单次变更审查 `briefbound-pr-review`；部署与运行时操作 `briefbound-runtime-operations`；实施方案 `briefbound-planning`；项目状态档案 `briefbound-project-memory`；已验证真实残留 `briefbound-development-cleanup`；`briefbound-router` 或 BLOCKED。

## 统一调用契约

- 只处理 Briefbound task contract 范围；不匹配时回 `briefbound-router` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文，先给版本判定与总体结论再列检查结果；版本号、日期、tag 与代码字面量保留原文；Route Out 仅以 Briefbound task contract 为准，有自然闸门时末行 `下一步建议: <一个具体动作>`，否则继续已授权工作。

## 激活闸门

用户要求发版、写 changelog、定版本号、semver 判定、发布说明、发布前检查或回滚预案时进入。单个 bug 修复的执行、部署运维操作、契约兼容性分析本身不进本 skill，分别交原 owner、`briefbound-runtime-operations` 与 `briefbound-api-contract`。

## 版本号判定

版本号遵循 SemVer 2.0.0 的 MAJOR.MINOR.PATCH 语义，按本版本全部变更取最高档：

- 含任一 BREAKING 变更（以 api-contract 判定为准，本 skill 不重复判定兼容性）→ 主版本 +1。
- 无破坏、面向使用者的新增功能或新接口 → 次版本 +1；0.x 阶段 API 未稳定，破坏可走次版本。
- 仅缺陷修复、文档或构建调整 → 修订 +1。

跳档必须写明理由并落到 changelog：哪类变更支撑了哪一档。只改内部实现不构成次版本；已发布的版本号不可复用。

预发布版本用连字符后缀（如 `2.1.0-alpha.1`），只用于灰度或验证，正式发布仍归到稳定号；版本比较按 SemVer 优先级规则判断先后，不按字符串排序。

## changelog 结构

CHANGELOG.md 按 Keep a Changelog 约定维护：

- 顶部 `## [Unreleased]` 常驻，作为变更暂存区；发布时整体归档为 `## [版本号] - 日期`。
- 条目按 Added / Changed / Deprecated / Removed / Fixed / Security 分组，每组内一条变更一句话。
- 面向使用者写：描述行为与用法的变化，不写提交流水或实现细节；破坏性变更在版本块内置顶。
- 每完成一次合并就补 Unreleased，不攒到发版当天凭记忆回填。
- Deprecated 条目给出替代方案与移除条件；Removed 条目指向迁移路径；两者直接引用 api-contract 的迁移说明，不另起炉灶。

## 发布前检查清单

发布前逐项核对，任何一项未过即 BLOCKED，不得带病发版；按顺序执行，前一项未过不进入下一项：

1. 测试全绿，关键路径冒烟通过。
2. 本版本全部 BREAKING 点已有 api-contract 的判定与迁移路径。
3. 版本号跳档与变更内容一致；版本文件（package.json、pyproject 或版本常量）已同步。
4. changelog 版本块完整，Unreleased 已归档。
5. 文档同步：README 用法与契约文档和实际行为一致。
6. 打 tag 并附发布说明，tag 指向已验证的提交。

## 发布说明与回滚

- 发布说明从 changelog 版本块提炼：破坏性变更置顶，其后是亮点、升级步骤、已知问题；不复制全文。
- 回滚预案随版本写入：回滚入口（还原 tag 或回退版本号的具体操作）、受影响消费者与通知口径、验证回滚成功的判据。
- 不可逆步骤（如破坏性 DB 迁移）单独标注回滚代价；回滚脚本缺失按 BLOCKED 处理。预案写完至少完整走查一遍，不交付"理论上可行"的步骤。实际回滚执行与部署动作交 `briefbound-runtime-operations`。

## 致谢

changelog 结构改编自 keep-a-changelog；版本语义遵循 SemVer 2.0.0；发布收尾与回滚流程参考 obra/superpowers（MIT）。以上均为重写表述，无整段引用。

## 输出

```text
版本判定: <版本号与跳档理由>
changelog: <版本块归档要点>
检查清单: <已过项与未过项，未过即说明>
回滚预案: <回滚入口与不可逆点>
下一步建议: <有自然闸门时的一个具体动作；否则声明继续已授权工作>
```

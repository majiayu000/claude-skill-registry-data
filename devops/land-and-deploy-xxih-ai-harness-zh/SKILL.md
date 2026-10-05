---
name: land-and-deploy
preamble-tier: 4
version: 1.0.0
description: |
  合并 PR、等待 CI / deploy、验证生产健康的发布工程流程。承接 /ship 的结果，
  把“PR 已准备好”推进到“已合并并经生产验证”。 (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /land-and-deploy

`/land-and-deploy` 是真正的上线 skill。它接在 `/ship` 后面，负责 merge、等待 deploy、做上线后验证，并在必要时建议回滚。

## 平台范围

- 当前重点支持 GitHub。
- 如果检测到 GitLab 或未知平台，按原文要求直接停下，提示用户先走 `/ship` 再手动合并。

## 核心流程

1. `Pre-flight`
   - 检查 `gh auth`
   - 找出当前 PR 和 base branch
2. `First-run dry-run validation`
   - 首次部署或 deploy 配置变更时，先做干跑
   - 识别平台、URL、workflow、staging
   - 展示“接下来会发生什么”
3. `Pre-merge checks`
   - 检查 CI 状态和 mergeability
4. `Wait for CI`（如有 pending）
5. `Pre-merge readiness gate`
   - review 新鲜度
   - 文档 / 变更说明 / 测试 / PR 准确性
   - 这是合并前最后的人机确认点
6. 执行 merge
7. 等待部署
8. 用 canary / HTTP / 平台检查做生产健康验证
9. 输出最终 verdict，必要时提供 revert 选项

## 关键规则

- 这是“多数自动化，少数关键点停下来确认”的 workflow。
- 必须在首次运行和关键 readiness gate 处停下给用户看清楚，而不是直接盲 merge。
- 如果生产健康检查失败，要把“建议回滚”摆到台面上。

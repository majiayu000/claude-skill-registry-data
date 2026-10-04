---
name: solution-to-delivery
description: >
  方案到交付 Workflow：当用户显式调用 `$solution-to-delivery`，或明确要求运行“方案到交付”完整流程时使用。
  把已确认产品方案转成经过独立 Review 的 PRD、适用的 UI/HTML/截图、版本拆分和 Product Delivery Package；当前 Agent Runtime 只做 Package 发布 dry-run，真实写入保持 authorization_required。
---

# 方案到交付

这是 `workflow` 的 Codex Runtime 入口，不是新的原子 Skill。先读取同目录 `WORKFLOW.md`，再编排现有 PRD、UI、Review、Issue 和 Tool 能力。

## 输入

优先发现已确认方案、项目目录、现有 PRD/UI、交付目标和版本要求。缺少会改变交付形态的信息时才询问：

- 方案目标、范围、关键流程、约束和已知风险；
- 是否存在用户可见界面；
- 交付到研发、钉钉、GitHub、云效或仅本地；
- 是否需要 V1/V2/V3 或研发事项拆分。

## 工作流

1. 检查方案是否达到 Entry Gate；未达到则交回 `$problem-to-solution`，不自行补写假方案。
2. 使用 `prd-architect` 生成 PRD，并初始化 Product Delivery Manifest。
3. 有用户可见界面时使用 `ui-mockup-desktop-workbench` 生成目标态 HTML/预览与关键状态截图；无界面时记录可审计的不适用理由。
4. 为所有 PRD/UI artifact 写入实际 `producer_identity`，再由独立 `prd-review` 检查 PRD 与适用 UI 证据，并把当前 fingerprint、覆盖的 Maker identities 和结论写入 `pre_split_review`；未达到 `ready` 时只修阻断项，禁止生成版本计划或事项草稿。
5. Validator 证明 `pre_split_review` 仍为 current/ready 后，用户要求版本或研发拆分时才使用 `prd-to-issues` 生成版本计划、事项草稿和 PRD 覆盖矩阵；未经批准不发布。
6. 把版本拆分产物写入 Manifest；Backlog Splitter 必须用 actor-scoped validator 把当前 identity 绑定到每项规划产物，再更新文件 hash 和 package fingerprint。
7. 使用 `$delivery-loop` 对这份完整 Package 做最终独立 Review；最终 Reviewer 必须覆盖全部 artifact producers 且与其身份独立，循环到 `package_ready`、Human Gate 或阻塞。
8. 运行 Product Delivery validator，确保最终 Manifest、artifacts、生产者身份和 Review fingerprint 一致。
9. 用户要求发布时，交给 Package Publisher 做完整 dry-run；当前 Agent Runtime 无可信 host approval capability，真实写入保持 `status: package_ready` 并返回 `publish_status: authorization_required`。不得改走 Legacy direct mode 绕过 Package 合同。

## 边界

- 不重新讨论已经确认且未被新证据推翻的方案。
- 不把 HTML/截图伪装成生产实现。
- 不让 PRD Maker 自评 ready。
- 不让 UI Producer、Backlog Splitter 或其他 artifact Producer 自评或从 Review 覆盖范围中被省略。
- 不在独立 PRD readiness Review 通过前生成版本或事项拆分。
- 不因为 Workflow 或 Manifest approval 被创建就发布钉钉、创建云效事项或同步 Runtime；Package 真实写入等待可信宿主能力。

## 输出

返回交付状态、Package 根目录、PRD、适用的 UI/HTML/截图、Review verdict、版本计划、Manifest、发布状态、剩余 gap 和恢复点。

## 完成定义

只有 `WORKFLOW.md` 的 Delivery Ready Gate 全部成立，独立 Review 没有 P0/P1，且 Manifest 与当前 artifacts/producer identities 一致，才输出 `package_ready`。Package dry-run 可以验证发布输入；真实写入在当前 Agent Runtime 始终保持 `authorization_required`，不改变 Package readiness。

## 资源与验证

- `WORKFLOW.md` 是交付路由、适用产物和 readiness gate 的权威合同，每次执行前读取。
- `evals/evals.json` 覆盖 UI、无 UI、单点 PRD、上游退回和外部授权回归；修改入口后运行这些评测并保留结果。

---
name: delivery-loop
description: >
  交付闭环：当用户显式调用 `$delivery-loop`，或明确要求进入“交付闭环”时使用。
  面向已有 PRD、UI/HTML、截图或 Product Delivery Package 但仍有 Review 缺口的场景，在独立评审与定点修订之间最多循环三轮，直到 package_ready 或进入 Human Gate；不用于从模糊问题开始。
---

# 交付闭环

这是 `loop` 的 Codex Runtime 入口，不是新的 PRD Skill。先读取同目录 `LOOP.md`，再使用现有 `prd-architect`、`ui-mockup-desktop-workbench`、`prd-review` 和必要的 `prd-to-issues` 关闭交付缺口。

## 目标与输入

目标是关闭现有交付包的最早阻断 finding，而不是重新定义产品方案。Entry Gate 必须已有可定位的 PRD 或交付包。如果只有已确认方案而没有交付物，使用 `$solution-to-delivery`；如果问题或方案仍未确认，使用 `$problem-to-solution`。

## 工作流

1. 建立或恢复 Loop 状态，`max_cycles` 固定为 3；运行适用 validator，确认 artifact hashes、producer identities 和 Review fingerprint。
2. 使用 `prd-review` 判断当前 verdict，并选择最早且唯一的阻断 finding。
3. 按 finding 返回责任节点：内容和 Manifest 用 `prd-architect`，页面、HTML 和截图用 `ui-mockup-desktop-workbench`，版本覆盖缺口用 `prd-to-issues`。
4. 只生成本轮 Artifact Delta，保留已经通过的内容；生产者用 actor-scoped validator 绑定身份，随后交回与全部 producer identities 独立的 `prd-review`。
5. Review 通过且当前 artifacts/Manifest 一致时输出 `package_ready`；达到停止条件时进入 Human Gate 或阻塞。

## 边界

- 不重新定义已经确认且未被新证据推翻的方案。
- Validator 只能证明结构和一致性，不能替代独立 Review。
- 页面型需求缺少当前 UI/HTML/截图时不得标记 ready；真正无用户可见界面时可以记录不适用原因。
- 不自动发布钉钉、创建云效事项或同步 Runtime；Package 只能做无副作用 dry-run，真实写入保持 `authorization_required`。

## 输出

每轮返回 cycle、Package 根目录、active finding、return owner、closure criterion、Artifact Delta、保留项、Review verdict、状态和恢复点。用户同时要求发布时可以补做 Package dry-run，但真实写入返回 `publish_status: authorization_required`，不改变 Package readiness。

## 完成定义

只有独立 `prd-review` 关闭当前阻断 finding、没有其他 P0/P1，且适用 validator 证明 Manifest 与 artifacts 一致，才输出 `package_ready`。三轮上限、连续两轮无有效 Artifact Delta 或交付事实缺失时进入 Human Gate。可信宿主授权不属于交付缺口；当前 Agent Runtime 中 Package 已 ready 时保持 `status: package_ready`，并对真实写入返回 `publish_status: authorization_required`。

## 资源与验证

- `LOOP.md` 是 Review 回流、责任节点、状态字段和停止条件的权威合同，每次执行或恢复前读取。
- `evals/evals.json` 覆盖 Review 修订、缺 UI 回流、单次 Review 分流、发布授权和无进展回归；修改入口后运行这些评测并保留结果。

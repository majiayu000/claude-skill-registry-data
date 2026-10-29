---
name: data-knowledge-architect-cn
description: >-
  把 API、CLI 与数据库契约转成有证据支撑的语义模型，通过 HTML 决策工作台审查后输出 Google OKF 或 YAML。适用于企业知识建模、语义层、维度建模与本体设计。
metadata:
  language: zh-CN
  translation_of: data-knowledge-architect
  version: "1.1.0"
  openclaw:
    homepage: https://github.com/ontology-of-everything/concept-skills/tree/main/skills/zh-CN/data-knowledge-architect-cn
---

# 数据知识架构师 — 为 API 与数据结构建立清晰的语义模型

把**接口契约**（REST/OpenAPI、CLI、表/DDL）一次通过地建成**受治理语义层**。四个阶段严格串行，每阶段一个参考文件、一组退出条件——满足才前进，不满足不硬闯：

```text
Phase 1 Ingest → Phase 2 Review → Phase 3 Emit → Phase 4 Verify
   ingest.md       review.md      emit-okf.md      verify.md
                                  emit-yaml.md
```

> 唯一真源是接口。**不臆造**字段/粒度/枚举/取值；缺证据停下，一次一问。

## Workflow

### Phase 1 · Ingest（`references/ingest.md`）

接口归一成「操作清单」，每个 op 判定角色（fact / dimension-lookup）。
**退出条件**：清单完整，每个 op 有角色与读写标记。

### Phase 2 · Review（`references/review.md`）

将对象拆为原子决策；显式展示目标、候选、证据、风险、依赖与权衡，并在
事实、维度、度量、路由分区提供固定 YAGNI 判断指导。生成 model JSON 注入
`assets/review-template.html`，由用户确认、选择、修正、补证或拒绝；反馈写入
`amendments.md` 后重出报告。
**退出条件**：收到 `approved:true`，且无未决或阻塞项。出报告后必须停下；
未批准禁止进入 Phase 3。

### Phase 3 · Emit（`references/emit-okf.md` 默认 / `references/emit-yaml.md` 可选）

默认生成 **Google OKF v0.1** bundle；用户明确要求时生成 repo-YAML（Kimball 星型）。字段语义两个目标共享（定义在 `emit-yaml.md` §2–§4）。≥2 个 bundle 时生成薄根索引。
**退出条件**：产物文件完整落盘。

### Phase 4 · Verify（`references/verify.md`）

跑结构检查 + 语义 lint +（如导出 OKF）OKF 硬约束，逐条回报 pass/fail。
**退出条件**：全部 pass；不可机械修复的 fail → 回 Phase 2 One blocking ask，不静默通过。

## Critical Rules

1. **Evidence-only** — 字段/粒度/枚举/取值仅来自接口；缺证据写 `TODO(verify)` 并列入待确认，不编造。
2. **Grain first** — 未锁 grain 不挂维度、不写度量。
3. **One blocking ask** — 仅在改变建模结果处停（一次一问，带候选），不连环问；批量确认走 HTML 评审。
4. **Layer split** — 形态/路由/粒度归语义层；可键入或读取的取值（枚举、code、字段路径、命令）归契约层，语义层只指向。
5. **Stable names** — 事实/维度名确认后不重命名（OKF 概念 ID = 文件路径，改名即断链）。
6. **Decision gate** — 所有决定初始 pending，不得默认通过。Phase 2 出报告后
   停下；仅用户回传 `approved:true` 且无未决/阻塞项时进入 Phase 3。

## Reference Index（按阶段加载）

| 阶段 | 文件 |
| --- | --- |
| Phase 1 物料归一 + 角色判定 | `references/ingest.md` |
| Phase 2 决策建模 + HTML 工作台 + amendments | `references/review.md` |
| Phase 3 默认目标 OKF 布局/映射 | `references/emit-okf.md` |
| Phase 3 可选目标 YAML + 共享字段语义 | `references/emit-yaml.md` |
| Phase 4 全部校验 + 升级回路 | `references/verify.md` |
| 端到端样例 | `references/examples.md` |

---
name: using-superpowers
description: 开发实施子流程入口 — brainstorming / writing-plans / TDD / executing / verification 等。设计完成、准备进入实施时调用。
disable-model-invocation: true
version: 4.0.0

---

# Using Superpowers — 开发实施入口

## Contract

- 输入: 已签字的设计产物,或明确的实施目标
- 输出: 推荐的 superpowers bridge skill 与起始点
- 门控: 设计阶段已签字,或用户明确请求进入实施
- Required rules: `stage-gate`
- Required paths: 无
- 下一步: `/brainstorming`、`/design-an-interface`、`/domain-modeling`、`/writing-plans`、`/tdd`、`/executing-plans` 或 `/verification-before-completion`

> 本 skill 是 **桥接层**,不复制 superpowers 官方内容,具体纪律以 `<SUPERPOWERS_SKILL_ROOT>/<name>/SKILL.md` 为准。
> 完整 superpowers 体系文档:https://github.com/obra/superpowers

## 我该用哪个?

| 我想做的事 | 用这个 superpowers skill |
|---|---|
| 反复提问澄清,产出设计稿 | `/brainstorming` |
| 设计接口契约 | `/design-an-interface` |
| 梳理领域模型 | `/domain-modeling` |
| 把 spec 拆成可执行计划(每个 ≤ 2h) | `/writing-plans` |
| 按测试驱动开发(红绿循环) | `/tdd` |
| 逐步按计划执行 + 复盘 | `/executing-plans` |
| 完成任务前验证(铁律) | `/verification-before-completion` |

## 与 analysis-to-delivery 的衔接

- **设计完成**(跑完 `/analysis-delivery-workflow` 或 `/dev-design` 后)→ 从这里进入实施
- **实施过程**纪律(stage-gate / 设计回测 / 任务复盘)来自 `disciplines/stage-gate`,由 superpowers 链路自动加载
- **实施完成** → 回到 `/handoff` 出交接文档

## 调用规则

我会先问你 1-2 个澄清问题,然后告诉你从哪个 superpowers skill 开始。

> ⚠️ 本 skill **不直接执行开发**,只做"告诉你从哪个 superpowers skill 开始 + 串接 9 阶段 ↔ 5 步实施"的导航。

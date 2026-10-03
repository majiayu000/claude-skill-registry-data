---
name: tdd
description: 测试驱动开发(红绿循环)— 来自 superpowers 体系。本 skill 是桥接层,先写失败测试再写实现,完整纪律见 <SUPERPOWERS_SKILL_ROOT>/tdd/。
version: 4.0.0

---

# TDD(桥接到 superpowers)

## Contract

- Inputs: executable task from writing plan, test target, acceptance criteria
- Outputs: RED test, GREEN implementation, refactor notes
- Gates: RED observed before implementation; GREEN observed after implementation
- Required disciplines: `stage-gate`
- Next: `/executing-plans`

> **本仓库不维护此 skill 的内容**。完整纪律请读:
> `<SUPERPOWERS_SKILL_ROOT>/tdd/SKILL.md`

## 何时调

- writing-plans 之后
- 每个子任务开始时(红绿循环)

## 衔接点

- **产出**:RED 测试 + GREEN 实现 + REFACTOR
- **下一步**:`/executing-plans`(commit + 下一任务)
- **门控**:`disciplines/stage-gate` 第 3 层(RED 必须确认失败才能写实现)

## 降级方案(superpowers 未装时)

如果 `<SUPERPOWERS_SKILL_ROOT>/tdd/` 不存在,严格按以下 4 步红绿循环:

### 1. RED — 写失败测试

- 在 `src/test/` 写测试,**只测一个最小行为**
- 跑测试 → 必须**确认失败**(看到红色 / FAILURE,不是 BUILD SUCCESS)
- ❌ 跳过 RED = 你不知道测试到底在测什么

### 2. 最小实现

- 写**最少量**代码让测试通过(可以丑 / 可以硬编码)
- 不优化、不重构、不扩展

### 3. GREEN — 跑通

- 再跑测试 → 必须**确认通过**(看到 BUILD SUCCESS / PASSED)
- ❌ 测试莫名通过 = 测试没断言你想要的东西

### 4. REFACTOR — 重构

- 改进实现 / 抽取方法 / 命名优化
- **每次重构后必须重跑测试**确认仍 GREEN
- 改完再跑 = 唯一能防止重构破坏功能的方法

### 最小纪律摘要

- **RED 必须亲眼看到失败**:写测试 → 跑 → 看 stack trace → 才写实现
- **GREEN 后才能 REFACTOR**:实现未通过前重构 = 在错的地基上盖楼
- **测试一次只测一个行为**:堆叠断言 = 失败时不知道哪个挂了
- **不 mock 你要测的东西**:只 mock 边界 IO

### 安装提示

```bash
npx skills@latest add obra/superpowers-tdd
```

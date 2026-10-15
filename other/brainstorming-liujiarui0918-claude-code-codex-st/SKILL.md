---
name: brainstorming
description: Use BEFORE any creative or non-trivial design work. Socratic clarification first, then 2-3 approaches, then a spec.
---

# Brainstorming

**Iron Law**: 用户描述了一个**非平凡**的需求，你的第一反应**必须**是问问题，不是给方案。

## 触发时机

- 用户描述了一个有歧义、有多种合理解读的需求
- 任务涉及架构决策、API 设计、UX 选择
- 你想了一下"有 3 种做法"——这就是该 brainstorm 的信号
- 你脑子里已经有一个"显然的方案"——这是该 brainstorm 的**最强**信号

## 不触发

- 用户说"把 X 改成 Y"，明确具体——直接做
- 一行 bug fix，复现已知，方案唯一——直接做
- 用户已经走过 brainstorming，现在拿着 spec 来——去 [[writing-plans]]

## 三阶段流程

### Stage 1: Clarify（Socratic 提问）

**目标**：让用户的隐藏假设浮出来。

- 一次问 3-5 个问题，不要一个一个挤牙膏
- 问"为什么"和"什么不要"，不光问"做什么"
- 复述你的理解让用户确认：「我听到的是 X，对吗？」

红旗：你已经 5 分钟没问问题，正在写"方案 A"——**停**，回到提问。

### Stage 2: Explore（2-3 个方案）

**目标**：让用户在选项之间做权衡。

- 给出 **2-3 个**真正不同的方案（不是一个方案的三种命名）
- 每个方案标出：核心思路、tradeoff、何时合适、何时不合适
- 不要在 Stage 2 偷偷推销自己最喜欢的方案——让用户自己选

格式示例：

```
方案 A：<一句话>
  - 优点：...
  - 代价：...
  - 适合：...

方案 B：<一句话>
  ...

方案 C：<一句话>
  ...
```

### Stage 3: Spec（成文规约）

**目标**：把选定方案落成下一阶段 [[writing-plans]] 可以吃下去的文档。

Spec 必须包含：

- **Goal**：一句话目标
- **In scope / Out of scope**：明确边界
- **Key decisions**：选了哪个方案、为什么、放弃了什么
- **Constraints**：技术约束、性能约束、兼容性约束
- **Success criteria**：如何验证完成了

## Red Flags

- 你跳过 Stage 1 直奔 Stage 2 → 你在猜需求
- Stage 2 只给了 1 个方案 → 那不是 brainstorming，是推销
- Stage 3 的 spec 里有"探索一下 X"这种词 → 不够具体，继续打磨
- 你已经在 Edit 文件了 → **停**，回到 Stage 1

## 终态

Spec 出来后，**显式交棒**给 [[writing-plans]]：

「Spec 完成。下一步：[[writing-plans]] 把它拆成可执行任务。」

## MUST

- **先问，再答**
- 复述用户的话以确认理解
- 给真正不同的备选方案
- spec 写完显式交棒

## MUST NOT

- 不要在 Stage 1 就给代码
- 不要用"建议"包装"我已经决定了"
- 不要在 spec 里留模糊词（"可能"、"或许"、"看情况"）

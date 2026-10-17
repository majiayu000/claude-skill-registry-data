---
name: codebase-design
description: 用于设计 deep modules 的 shared vocabulary。当用户想设计或改进某个 module 的 interface、寻找 deepening 机会、决定 seam 放在哪里、让代码更可测试或更易被 AI 导航，或当其他 skill 需要 deep-module vocabulary 时使用。
---

# Codebase Design

设计 **deep modules**：在一小片 interface 背后承载大量行为，放置于干净的 seam 处，并可通过该 interface 测试。凡是在设计或重构代码的地方，都使用这套语言和这些原则。目标是：对调用者而言是 leverage，对维护者而言是 locality，对所有人而言是可测试性。

## Glossary

请精确使用这些术语：不要替换成 "component"、"service"、"API" 或 "boundary"。统一的语言正是这一切的意义所在。

**Module**：任何同时具备 interface 和 implementation 的东西。刻意与规模无关：一个 function、class、package 或跨层切片。_Avoid_: unit, component, service.

**Interface**：调用者为了正确使用某个 module 而必须知道的一切：类型签名，以及不变量、顺序约束、错误模式、所需配置和性能特性。_Avoid_: API, signature (too narrow, they refer only to the type-level surface).

**Implementation**：module 内部的东西，即它的代码主体。与 **Adapter** 不同：一个东西可以是小 adapter 配大 implementation（如 Postgres repo），也可以是大 adapter 配小 implementation（如 in-memory fake）。当讨论的主题是 seam 时用 "adapter"；否则用 "implementation"。

**Depth**：interface 处的 leverage。调用者（或测试）每学习一份 interface 就能执行的行为量。当一个 module 在小型 interface 背后承载大量行为时，它是 **deep** 的；当 interface 几乎和 implementation 一样复杂时，它是 **shallow** 的。

**Seam** _(Michael Feathers)_：一个无需就地编辑即可改变行为的地方；也就是 module 的 interface 所存在的位置。seam 放在哪里本身就是独立的设计决策，与它背后放什么无关。_Avoid_: boundary (overloaded with DDD's bounded context).

**Adapter**：在 seam 处满足某个 interface 的具体东西。描述的是 *角色*（它填补了什么位置），而非实质（里面是什么）。

**Leverage**：调用者从 depth 中获得的东西。每学习一份 interface 就能获得更多能力。一份 implementation 的回报在 N 个调用点和 M 个测试之间摊还。

**Locality**：维护者从 depth 中获得的东西。变更、bug、知识和验证集中在一处，而不是散布在调用者之间。修一次，处处修复。

## Deep vs shallow

**Deep module** = 小型 interface + 大量 implementation：

```
┌─────────────────────┐
│   小型 Interface     │  ← 很少的方法，简单的参数
├─────────────────────┤
│                     │
│ 深度 Implementation │  ← 隐藏复杂逻辑
│                     │
└─────────────────────┘
```

**Shallow module** = 大型 interface + 少量 implementation（避免）：

```
┌─────────────────────────────────┐
│       大型 Interface             │  ← 很多方法，复杂的参数
├─────────────────────────────────┤
│  很薄的 Implementation           │  ← 只是透传
└─────────────────────────────────┘
```

设计 interface 时，问自己：

- 我能减少方法的数量吗？
- 我能简化参数吗？
- 我能把更多复杂度藏到内部吗？

## 原则

- **Depth 是 interface 的属性，不是 implementation 的属性。** 一个 deep module 在内部可以由小的、可 mock 的、可替换的部件组成；它们只是不属于 interface。一个 module 既可以在 interface 处有 **external seam**，也可以有对其 implementation 私有的 **internal seams**（供它自己的测试使用）。
- **The deletion test。** 想象删除这个 module。如果复杂度随之消失，它只是透传。如果复杂度重新散布到 N 个调用者身上，那它物有所值。
- **Interface 就是测试表面。** 调用者和测试穿过同一个 seam。如果你想测试到 interface *之外*，这个 module 的形状可能不对。
- **一个 adapter 意味着假想的 seam；两个 adapter 才意味着真实的 seam。** 除非确实有东西在 seam 两侧变化，否则不要引入 seam。

## 为可测试性而设计

好的 interface 让测试变得自然：

1. **接受依赖，而不是创建依赖。**

   ```typescript
   // Testable
   function processOrder(order, paymentGateway) {}

   // Hard to test
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **返回结果，而不是产生副作用。**

   ```typescript
   // Testable
   function calculateDiscount(cart): Discount {}

   // Hard to test
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **较小的表面积。** 方法越少 = 需要的测试越少。参数越少 = 测试设置越简单。

## 关系

- 一个 **Module** 恰好有一个 **Interface**（它呈现给调用者和测试的表面）。
- **Depth** 是 **Module** 的属性，针对它的 **Interface** 来衡量。
- **Seam** 是 **Module** 的 **Interface** 所在之处。
- **Adapter** 位于 **Seam** 处并满足 **Interface**。
- **Depth** 为调用者产出 **Leverage**，为维护者产出 **Locality**。

## 被否决的表述

- **把 depth 视作 implementation 行数与 interface 行数的比值**（Ousterhout）：这会奖励给 implementation 注水。我们改用 depth-as-leverage。
- **把 "Interface" 视作 TypeScript 的 `interface` 关键字或 class 的公共方法**：太窄：这里的 interface 包含调用者必须知道的每一个事实。
- **"Boundary"**：与 DDD 的 bounded context 含义重复。请说 **seam** 或 **interface**。

## 继续深入

- **在给定依赖的情况下加深一个 cluster**，见 [DEEPENING.md](DEEPENING.md)：依赖分类、seam 纪律，以及替换而非分层的测试。
- **探索替代 interface**，见 [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md)：启动并行的 sub-agents，以若干种截然不同的方式设计 interface，然后在 depth、locality 和 seam 放置上做比较。

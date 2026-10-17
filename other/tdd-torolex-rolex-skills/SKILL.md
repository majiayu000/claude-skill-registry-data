---
name: tdd
description: 测试驱动开发（Test-Driven Development）。当用户希望以测试先行（test-first）的方式构建功能或修复 bug、提到 "red-green-refactor"，或需要集成测试时使用。
---

# TDD（测试驱动开发）

TDD 就是 red → green 循环。本 skill 是让这个循环产出值得保留的测试的参考指南：什么是好测试、测试放在哪里、有哪些 anti-patterns、以及循环的规则。每个部分在每个周期都适用：在循环开始前和进行中查阅它们，而不是之后。

浏览代码库时，先读 `GLOSSARY.md`（如果存在），让测试名称和 interface 词汇与项目的领域语言（domain language）一致，并尊重你正在接触的区域的 ADR。

## 什么是好测试

测试通过 public interface 验证行为，而不是验证 implementation 的细节。代码可以彻底改变，测试却不应改变。好测试读起来像一份规格说明："用户可以用有效的购物车结账"精确告诉你存在什么能力，而且它能经受重构，因为它不关心内部结构。

示例见 [tests.md](tests.md)，mocking 指南见 [mocking.md](mocking.md)。

## Seams：测试放在哪里

**seam** 是你进行测试的公共边界：在不伸手进内部的情况下观察行为的 interface。测试写在 seam 上，绝不针对内部实现。

**只在预先约定的 seam 上测试。** 写任何测试之前，先写下要测试的 seams 并让用户确认。未经确认的 seam 上不写测试。你不可能测试所有东西，所以预先约定 seams 才能让测试精力落在关键路径和复杂逻辑上，而不是每个边缘情况上。

问："public interface 是什么？我们应该测试哪些 seams？"

当 interface 本身的形状也存疑时（module 该多深、seam 该在哪里、interface 应该暴露什么），调用 Skill 工具，传入 "codebase-design" 获取词汇。它是 module、interface、depth、seam、adapter、leverage 和 locality 这些术语的共享来源，是一份需要查阅的参考，而不是一个需要运行的会话。

## Anti-patterns（反模式）

- **Implementation-coupled（耦合实现）**：mock 内部协作者、测试私有方法、或通过旁路通道验证（查询数据库而不是使用 interface）。典型特征：重构时测试失败，但行为并没有变化。
- **Tautological（同义反复）**：断言用与代码相同的方式重新计算期望值（`expect(add(a, b)).toBe(a + b)`、用手工相同方式推导出的快照、断言一个常量等于它自身），所以它从构造上就必然通过，永远不可能与代码不一致。期望值必须来自独立的真相来源：一个已知正确的字面量、一个手工推导的示例、或 spec。
- **Horizontal slicing（水平切片）**：先写完所有测试，再写全部 implementation。批量测试验证的是_想象出来的_行为：你测试的是代码的_形状_而不是面向用户的行为，测试对真实变化变得不敏感，而且你在理解 implementation 之前就承诺了测试结构。应当改用 **vertical slices**：一个测试 → 一段实现 → 重复，每个测试都是一颗 **tracer bullet**，回应上一个周期教给你的东西。

## 循环的规则

- **先 red 后 green。** 先写失败的测试，然后只写足够让它通过的代码。不要预期未来的测试，也不要添加投机性的功能。
- **一次一个切片。** 每个周期一个 seam、一个测试、一个最小的 implementation。
- **重构不属于循环。** 它属于 review 阶段（见 `code-review` skill），不属于 red → green 的实现循环。

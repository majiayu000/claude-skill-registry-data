---
name: domain-modeling
description: 构建并打磨项目的 domain model。在讨论代码库术语、编写或编辑 GLOSSARY.md、或记录或编辑 ADR 时使用。
---

# Domain Modeling

在设计中主动构建并打磨项目的 domain model。这是一门 *主动* 的功夫：质疑术语、编造 edge case 场景，并在 glossary 和 decisions 一经成形时立刻把它们写下来。（仅仅 *读* `GLOSSARY.md` 来取词汇并不是这个 skill：那是任何 skill 都能做到的一行习惯。这个 skill 适用于你在*改变*模型，而不只是消费它。）

## 文件结构

大多数仓库只有一个 context：

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

如果根目录存在 `GLOSSARY-MAP.md`，说明仓库有多个 contexts。map 会指出每个 context 所在的位置：

```
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── GLOSSARY.md
│       └── docs/adr/
```

懒创建文件：只在你有东西要写时才创建。如果不存在 `GLOSSARY.md`，在第一个术语被确定时创建它。如果不存在 `docs/adr/`，在第一个 ADR 需要时创建它。

## 会话期间

### 用 glossary 提出质疑

当用户使用一个与 `GLOSSARY.md` 中现有语言冲突的术语时，立刻指出来。「你的 glossary 把 'cancellation' 定义为 X，但你看起来想说的是 Y。到底是哪个？」

### 打磨模糊的语言

当用户使用模糊或过载的术语时，提出一个精确的规范术语。「你说的是 'account'：你指的是 Customer 还是 User？两者是不同的东西。」

### 讨论具体场景

当讨论领域关系时，用具体场景做压力测试。编造能探测 edge cases、迫使用户对概念之间的边界做到精确的场景。

### 与代码交叉核对

当用户描述某件事如何运作时，检查代码是否一致。如果发现矛盾，就把它摆出来：「你的代码取消的是整个 Orders，但你刚才说可以部分取消。哪个才是对的？」

### 就地更新 GLOSSARY.md

当一个术语被确定时，就地更新 `GLOSSARY.md`。不要攒起来：随时发生随时记录。使用 [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md) 中的格式。

`GLOSSARY.md` 应该完全不含实现细节。不要把 `GLOSSARY.md` 当作 spec、草稿本或实现决策的仓库。它只是一个 glossary，仅此而已。

### 审慎地提供 ADRs

只有以下三条全部成立时才主动提出创建 ADR：

1. **Hard to reverse**：日后改变主意的代价是实质性的
2. **Surprising without context**：未来的读者会疑惑"他们为什么这样做？"
3. **The result of a real trade-off**：存在真正的备选方案，而你基于特定理由选了一个

三条缺一，就跳过 ADR。使用 [ADR-FORMAT.md](./ADR-FORMAT.md) 中的格式。

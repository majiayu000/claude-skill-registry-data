---
name: code-review
description: 审查自某个 fixed point（commit、branch、tag 或 merge-base）以来的变更，沿两个轴进行：Standards（代码是否遵循本仓库文档化的编码规范？）和 Spec（代码是否匹配原始 issue/spec 的要求？）。两个并行 sub-agent 分别运行审查并并排报告结果。当用户想要 review branch、PR、进行中的变更，或要求 "review since X" 时使用。
---

# Code Review（代码审查）

对 `HEAD` 与用户提供的 fixed point 之间的 diff 进行双轴 review：

- **Standards（规范）**：代码是否符合本仓库文档化的编码规范？
- **Spec（规格）**：代码是否忠实实现了原始 issue / spec？

两个轴作为**并行的 sub-agent** 运行，以免污染彼此的上下文，然后本 skill 汇总它们的发现。

issue tracker 应该已经提供给你。如果 `docs/agents/issue-tracker.md` 缺失，让用户运行 `/setup-rolex-skills`。

## 流程

### 1. 确定 fixed point

用户说过的任何 fixed point（commit SHA、branch 名、tag、`main`、`HEAD~5` 等）。如果他们没有指定，就问一个。

把 diff 命令一次性记下来：`git diff <fixed-point>...HEAD`（三个点，这样比较的是 merge-base）。同时通过 `git log <fixed-point>..HEAD --oneline` 记下 commit 列表。

在进一步操作之前，确认 fixed point 能解析（`git rev-parse <fixed-point>`）且 diff 非空。一个坏的 ref 或空 diff 应该在这里就失败，而不是在两个并行 sub-agent 内部。

### 2. 定位 spec 来源

按以下顺序寻找原始的 spec：

1. commit 消息中的 issue 引用（`#123`、`Closes #45`、GitLab `!67` 等），通过 `docs/agents/issue-tracker.md` 中的工作流获取。
2. 用户作为参数传入的路径。
3. `docs/`、`specs/` 或 `.scratch/` 下与 branch 名或功能名匹配的 spec 文件。
4. 如果什么都没找到，问用户 spec 在哪里。如果他们说没有，**Spec** sub-agent 将跳过并报告"无可用 spec"。

### 3. 定位 standards 来源

仓库中任何记录了代码应该如何编写的文件，例如 `CODING_STANDARDS.md` 或 `CONTRIBUTING.md`。

在仓库文档化内容之上，Standards 轴始终携带下面的 **smell baseline**：一组固定的 Fowler code smells（《Refactoring》第 3 章），即使在仓库没有文档化任何内容时也适用。两条规则约束它：

- **仓库优先。** 文档化的仓库规范始终优先；当它认可 baseline 会标记的内容时，压制该 smell。
- **始终是 judgement call。** 每个 smell 是一个带标签的启发式规则（"可能的 Feature Envy"），永远不是硬性 violation。就像这里的任何规范一样，跳过工具已强制执行的内容。

每个 smell 按*它是什么* → *如何修复*来读；把它与 diff 对照：

- **Mysterious Name（神秘命名）**：名称无法揭示其功能或内容的函数、变量或类型。→ 重命名它；如果找不到一个诚实的名称，说明设计本身不清晰。
- **Duplicated Code（重复代码）**：相同的逻辑形状出现在变更中不止一个 hunk 或文件里。→ 提取共享形状，从两处调用它。
- **Feature Envy（依恋情结）**：一个方法触碰另一个对象的数据多于自己的数据。→ 把该方法移到它依恋的数据上。
- **Data Clumps（数据泥团）**：相同的几个字段或参数总是一起出现（一个等待诞生的类型）。→ 把它们打包成一个类型，传递那个类型。
- **Primitive Obsession（基本类型偏执）**：用基本类型或字符串代替一个本应拥有自己类型的领域概念。→ 给该概念一个自己的小类型。
- **Repeated Switches（重复的 switch）**：相同类型上的相同 `switch`/`if` 级联在变更中反复出现。→ 用多态替换，或换成两个位置共享的一个 map。
- **Shotgun Surgery（霰弹式修改）**：一个逻辑变更迫使 diff 中许多文件发生分散的编辑。→ 把一起变化的内容聚合成一个 module。
- **Divergent Change（发散式变化）**：一个文件或 module 因几个不相关的原因被编辑。→ 拆分，使每个 module 只因为一个原因而变化。
- **Speculative Generality（投机性泛化）**：为 spec 并不存在的需求添加的抽象、参数或钩子。→ 删除它；内联回去，直到出现真正的需求。
- **Message Chains（消息链）**：调用者不应依赖的长 `a.b().c().d()` 导航链。→ 把这条遍历隐藏到第一个对象上的一个方法里。
- **Middle Man（中间人）**：一个主要只是向下委托的类或函数。→ 砍掉它，直接调用真正的目标。
- **Refused Bequest（拒绝遗赠）**：一个忽略或覆盖了大部分继承内容的子类或实现者。→ 放弃继承，改用组合。

### 4. 并行启动两个 sub-agent

在一条消息里发两个 `Agent` 工具调用。两者都用 `general-purpose` subagent。

**Standards sub-agent 提示**应包含：

- 完整的 diff 命令和 commit 列表。
- 步骤 3 中找到的 standards 来源文件列表，**加上步骤 3 的 smell baseline 全文**（sub-agent 没有其他途径访问它）。
- 任务简报："按相关的文件/hunk 报告：（a）diff 中每一处违反文档化规范的地方：引用该规范（文件 + 规则）；以及（b）你发现的任何 baseline smell：命名并引用对应 hunk。区分硬性 violation 与 judgement call：违反文档化规范可以是硬性的，但 baseline smell 始终是 judgement call，且文档化的仓库规范覆盖 baseline。跳过任何工具已强制执行的内容。400 字以内。"

**Spec sub-agent 提示**应包含：

- diff 命令和 commit 列表。
- spec 的路径或获取到的内容。
- 任务简报："报告：（a）spec 要求但缺失或不完整的需求；（b）diff 中未被要求的行为（scope creep）；（c）看起来已实现但实现方式有误的需求。每项发现引用 spec 中的对应行。400 字以内。"

如果 spec 缺失，跳过 Spec sub-agent，并在最终报告中注明。

### 5. 汇总

在两个 `## Standards` 和 `## Spec` 标题下分别呈现两份报告，逐字或做轻度清理。**不要**合并或重新排序发现，因为两个轴是刻意分开的（见_为什么两个轴_）。

以一行摘要结尾：每个轴的发现总数，以及_每个轴内_最严重的问题（如果有）。不要跨轴选一个赢家：那正是这种分离要防止的重新排序。

## 为什么两个轴

一个变更可能通过一个轴却在另一个轴上失败：

- 遵守了每条规范但实现了错误的功能 → **Standards 通过，Spec 失败。**
- 完全按 issue 要求做了但破坏了项目约定 → **Spec 通过，Standards 失败。**

分开报告可以防止一个轴掩盖另一个轴。

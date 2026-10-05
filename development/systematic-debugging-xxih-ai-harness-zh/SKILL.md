---
name: systematic-debugging
description: 当遇到任何 bug、测试失败或非预期行为时，在提出修复方案之前使用
---

# 系统化调试

## 概览

随机修补会浪费时间，还会制造新 bug。快速补丁通常只是在掩盖根因。

**核心原则：**在尝试修复之前，必须先找到根因。只修症状就是失败。

**违背这套流程的字面要求，就是违背调试的精神。**

## 铁律

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

如果你还没完成第一阶段，就不能提出修复方案。

## 何时使用

任何技术问题都适用：
- 测试失败
- 线上 bug
- 非预期行为
- 性能问题
- 构建失败
- 集成问题

**特别是这些时候更要用：**
- 时间压力很大（越着急越容易猜）
- “先来个 quick fix” 看起来很诱人
- 你已经试过多个修法
- 上一个修法没用
- 你并没有真正理解这个问题

**不要因为这些理由跳过：**
- “看起来很简单”
- “我很赶”
- “老板说现在就要修好”

## 四个阶段

你**必须**按顺序完成每个阶段，才能进入下一个阶段。

### 第一阶段：根因调查

**在尝试任何修复之前：**

1. **仔细读错误信息**
   - 不要跳过 errors 或 warnings
   - 它们往往直接给出线索
   - 完整读完 stack trace
   - 记下行号、文件路径、错误码

2. **稳定复现**
   - 能否稳定触发？
   - 复现步骤具体是什么？
   - 每次都会发生吗？
   - 如果不能稳定复现 -> 继续收集数据，不要猜

3. **检查最近变更**
   - 最近改了什么，可能导致这个问题？
   - 看 git diff、最近 commit
   - 看新依赖、配置改动
   - 看环境差异

4. **多组件系统里先收证据**

   **当系统跨多个组件（CI -> build -> signing，API -> service -> database）时：**

   在提出修法前，先加诊断性观测：
   ```
   For EACH component boundary:
     - Log what data enters component
     - Log what data exits component
     - Verify environment/config propagation
     - Check state at each layer

   Run once to gather evidence showing WHERE it breaks
   THEN analyze evidence to identify failing component
   THEN investigate that specific component
   ```

   **例子：**
   ```bash
   # Layer 1: Workflow
   echo "=== Secrets available in workflow: ==="
   echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

   # Layer 2: Build script
   echo "=== Env vars in build script: ==="
   env | grep IDENTITY || echo "IDENTITY not in environment"

   # Layer 3: Signing script
   echo "=== Keychain state: ==="
   security list-keychains
   security find-identity -v

   # Layer 4: Actual signing
   codesign --sign "$IDENTITY" --verbose=4 "$APP"
   ```

   **这类日志能揭示：**到底是哪一层断掉了。

5. **追踪数据流**

   **当错误出现在深层调用栈里时：**

   查看同目录下的 `root-cause-tracing.md`，了解完整的逆向追踪法。

   **简版：**
   - 错值最初从哪里来？
   - 是谁把这个坏值传进来的？
   - 一直向上追，直到找到源头
   - 在源头修，不在症状处修

### 第二阶段：模式分析

**修之前先找到模式：**

1. **找可工作的相似例子**
   - 在同一代码库中找相似且正常工作的实现
   - 有什么相似的东西是“好的”？

2. **对照参考实现**
   - 如果你在实现某种模式，必须把参考实现完整读完
   - 不要 skim，每一行都读
   - 先彻底理解，再迁移模式

3. **列出差异**
   - 工作的和坏掉的之间有什么不同？
   - 把所有差异都列出来，不要漏掉“小差异”
   - 不要先入为主地觉得“这个不重要”

4. **理解依赖条件**
   - 它依赖哪些组件？
   - 依赖什么设置、配置、环境？
   - 它默认假设了什么？

### 第三阶段：提出假设并验证

**用科学方法，而不是猜：**

1. **一次只提一个假设**
   - 明确写出来："I think X is the root cause because Y"
   - 说具体，不要含糊

2. **最小化测试假设**
   - 只做验证这个假设所需的最小改动
   - 一次只变一个变量
   - 不要一次修很多事

3. **确认结果再继续**
   - 有效？进入第四阶段
   - 无效？提出**新的**假设
   - 不要在旧修法上继续叠补丁

4. **当你不知道时**
   - 直接说："I don't understand X"
   - 不要装懂
   - 请求帮助
   - 或继续研究

### 第四阶段：实现修复

**修根因，不修症状：**

1. **先创建失败测试**
   - 用最简单方式复现问题
   - 能写自动化测试就写自动化测试
   - 没测试框架就写一次性脚本
   - 修之前必须先有它
   - 编写失败测试时使用 `superpowers:test-driven-development`

2. **一次只做一个修复**
   - 只针对已识别的根因
   - 一次只改一处
   - 不要“顺手”优化别的
   - 不要顺带重构一大堆

3. **验证修复**
   - 测试是否通过？
   - 其他测试是否没被打坏？
   - 问题是否真的解决？

4. **如果修复无效**
   - 立刻停下
   - 数一下：已经尝试过几次修复？
   - 如果 < 3：带着新信息回到第一阶段重做分析
   - **如果 >= 3：停止，开始质疑架构本身**
   - 不要在没有架构讨论前就开始第 4 次修复尝试

5. **如果 3 次以上修复都失败：质疑架构**

   **这说明问题可能是架构性的：**
   - 每次修完都会暴露另一个共享状态 / 耦合 / 新问题
   - 修复要求“大规模重构”才成立
   - 每个修复都会在别处制造新症状

   此时应当停下来问：
   - 这个模式本身是不是错的？
   - 我们是不是只是因为惯性才在继续补？
   - 与其继续补丁，是否应该重做架构？

   **先和人类协作者讨论，再继续。**

## 红旗：一旦出现就停下并回流程

如果你发现自己在想：
- “先 quick fix，之后再查根因”
- “先改改 X 看看有没有用”
- “多改几个地方一起跑测试”
- “先别写测试，我手动验证一下”
- “大概就是 X，我先修了再说”
- “虽然不完全懂，但这个可能有效”
- “参考实现是这样，但我稍微改着用一下”
- 在追完数据流之前就开始提修法
- **“再试最后一次”**（而你已经修了 2 次以上）
- **每个修复都会在别处引出新问题**

这些都意味着：**停下。回到第一阶段。**

## 人类协作者在提醒你做错时常说的话

如果你听到这些，说明你偏了：
- "Is that not happening?" —— 你没验证就在假设
- "Will it show us...?" —— 你应该先补证据采集
- "Stop guessing" —— 你在没理解前就提修法
- "Ultrathink this" —— 要开始质疑基本假设，而不是继续补症状
- "We're stuck?" —— 你的方法不工作了

出现这些提醒时，立刻回到第一阶段。

## 常见合理化借口

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | 简单问题也有根因。流程对简单 bug 也很快。 |
| "Emergency, no time for process" | 系统化调试比猜测式乱试更快。 |
| "Just try this first, then investigate" | 第一次修法会决定后续模式。开头就要做对。 |
| "I'll write test after confirming fix works" | 没测试的修复不牢靠。测试先行才能证明。 |
| "Multiple fixes at once saves time" | 你会失去因果定位，还会引入新 bug。 |
| "Reference too long, I'll adapt the pattern" | 不完整理解几乎必出错。先读完整。 |
| "I see the problem, let me fix it" | 看到症状 ≠ 理解根因。 |
| "One more fix attempt" | 3 次以上失败通常是架构问题。 |

## 快速参考

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | 读错误、复现、查变更、收证据 | 理解 WHAT 和 WHY |
| **2. Pattern** | 找可工作样例、对照差异 | 找出差异模式 |
| **3. Hypothesis** | 提假设、做最小验证 | 假设被证实或被否定 |
| **4. Implementation** | 写失败测试、修复、验证 | 问题解决、测试通过 |

## 当流程显示“没有根因”时

如果系统化调查后发现问题确实是环境性的、时序性的，或来自外部依赖：

1. 说明你已经完整走过调查流程
2. 记录你调查了什么
3. 实现合适的处理方式（重试、超时、错误提示）
4. 加上监控 / 日志，为以后继续调查准备证据

**但要记住：**95% 的“没有根因”其实只是调查还不够完整。

## 支持性技巧

同目录下这些材料可作为系统化调试的一部分：
- **`root-cause-tracing.md`** - 沿调用链反向追踪到最初触发点
- **`defense-in-depth.md`** - 找到根因后，在多层补上防御
- **`condition-based-waiting.md`** - 用条件等待替代任意 timeout

**相关 skills：**
- **superpowers:test-driven-development** - 用于第四阶段第一步的失败测试
- **superpowers:verification-before-completion** - 在声称修好前做最终验证

## 真实世界影响

来自多次调试会话的经验：
- 系统化方式：通常 15-30 分钟解决
- 乱试补丁：通常 2-3 小时来回折腾
- 一次修对率：95% vs 40%
- 引入新 bug 的概率：前者极低，后者经常发生

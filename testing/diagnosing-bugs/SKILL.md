---
name: diagnosing-bugs
description: 针对硬 bug 和 performance regression 的诊断循环。当用户说"诊断"/"调试这个"，或报告有东西坏了/抛异常/失败/慢时使用。
---

# Diagnosing Bugs（bug 诊断）

针对硬 bug 的规范流程。只有在明确有理由时才跳过某个阶段。

探索代码库时，阅读 `GLOSSARY.md`（如果存在）以建立相关模块清晰的 mental model，并检查你正在改动的区域附近的 ADR。

## 脱敏（Redact）

本 skill 会让你展示命令、输出和捕获的 artifact。**先把每一个 secret 脱敏**：在原位写上 `<REDACTED>`。针对 env var 构建 feedback loop，让凭据留在环境里，而不是出现在你展示的内容中。捕获的 artifact 带有 auth header：只引用携带信号的那些行。

如果脱敏后的输出不足以诊断 bug，明说，并向用户询问。

## 阶段 1：构建 feedback loop

**这就是本 skill 的核心。** 其他一切都是机械性的。如果你有一个针对 _这个_ bug 的**紧的**通过/失败信号（一个能在此 bug 上变红的信号），你就能找到原因；bisection、hypothesis 检验和 instrumentation 都只是消耗这个信号而已。如果没有这样一个信号，再怎么盯着代码看也救不了你。

在此投入不成比例的努力。**要激进。要有创造力。拒绝放弃。**

### 构建 feedback loop 的方法，大致按这个顺序尝试

1. **失败的测试**，在能触及 bug 的任意 seam 上：unit、integration、e2e。
2. **Curl / HTTP 脚本**，针对正在运行的 dev server。
3. **CLI 调用**，使用 fixture 输入，将 stdout 与已知正确的 snapshot 进行 diff。
4. **无头浏览器脚本**（Playwright / Puppeteer），驱动 UI，对 DOM/console/network 做断言。
5. **重放捕获的 trace。** 把真实的网络请求/载荷/事件日志保存到磁盘；在隔离环境中通过代码路径重放它。
6. **一次性 harness。** 启动系统的一个最小子集（单个服务、mocked 依赖），用一次函数调用触发 bug 代码路径。
7. **Property / fuzz 循环。** 如果 bug 是"有时输出错误"，运行 1000 个随机输入并寻找失败模式。
8. **Bisection harness。** 如果 bug 出现在两个已知状态之间（commit、数据集、版本），把"在状态 X 启动、检查、重复"自动化，这样你就能 `git bisect run` 它。
9. **差分循环。** 对旧版本 vs 新版本（或两种配置）运行相同的输入并 diff 输出。
10. **HITL bash 脚本。** 最后手段。如果必须由人来点击，用 `scripts/hitl-loop.template.sh` 驱动_他们_，让循环仍然保持结构化。捕获到的输出反馈给你。

构建出正确的 feedback loop，bug 就修好了 90%。

### 收紧 feedback loop

把 feedback loop 当产品来对待。一旦你有了一个循环，就**收紧**它：

- 能更快吗？（缓存设置、跳过无关的初始化、缩小测试范围。）
- 能让信号更锐利吗？（对具体症状断言，而不是"没崩溃"。）
- 能更 deterministic 吗？（固定时间、给 RNG 播种、隔离文件系统、冻结网络。）

一个 30 秒的 flaky feedback loop 几乎不比没有 loop 强多少；一个 2 秒的 deterministic feedback loop 才是紧的，这是调试领域的超能力。

### Non-deterministic bugs（非确定性 bug）

目标不是干净的 repro，而是**更高的 repro rate**。把触发循环 100 次、并行化、增加压力、缩小时序窗口、注入 sleep。一个 50% flake 的 bug 是可调试的；1% 则不是，所以要不断把 repro rate 提高，直到它可以调试为止。

### 当你确实无法构建 feedback loop 时

停下来，并明确说出来。列出你试过的方法。向用户请求：（a）访问任何能 reproduce（复现）它的环境，（b）一份捕获的 artifact（HAR 文件、日志转储、core dump、带时间戳的屏幕录制），或（c）添加临时生产环境 instrumentation 的许可。**没有 feedback loop，就不要继续提出 hypothesis。**

### Completion criterion（完成标准）：一个能变红的紧 feedback loop

阶段 1 完成的标志是 feedback loop 是**紧的**且**能变红**：你能说出**一个命令**（一条脚本路径、一个测试调用、一条 curl），你**已经至少运行过一次**（粘贴该调用及其输出），并且它满足：

- [ ] **能变红（red-capable）**：它驱动实际的 bug 代码路径，并断言**用户的确切症状**，因此它能在这个 bug 上变红、修复后变绿。不是"运行不报错"；它必须能_抓住这个具体的 bug_。
- [ ] **Deterministic（确定性）**：每次运行都给出相同结论（对 flaky bug：固定的高 repro rate，见上文）。
- [ ] **快**：秒级，而不是分钟级。
- [ ] **Agent 可运行**：你可以无人值守地运行它；人只能通过 `scripts/hitl-loop.template.sh` 进入 feedback loop。

如果你发现自己在还没有这条命令时就开始读代码构建理论，**停下来：直接跳到 hypothesis 正是本 skill 要防止的失败。** 没有能变红的命令，就没有阶段 2。

## 阶段 2：Reproduce + minimise（复现 + 最小化）

运行 feedback loop。看着它变红，bug 出现了。

确认：

- [ ] feedback loop 产生的是**用户**描述的失败模式，而不是恰好发生在附近的另一个失败。错误的 bug = 错误的修复。
- [ ] 该失败能在多次运行中 reproduce（复现）（或者对 non-deterministic bug，能以足够高的 repro rate 复现，以便针对它调试）。
- [ ] 你已经捕获了确切症状（错误消息、错误输出、耗时缓慢），这样后续阶段能验证修复确实解决了它。

### Minimise（最小化）

一旦它变红，把 repro 缩小到**仍然能变红的最小场景**。**一次一个**地削减输入、调用者、配置、数据和步骤，每削减一次就重新运行 feedback loop，只保留对失败起承重作用的部分。

为什么要费这个劲：最小的 repro 能缩小阶段 3 的 hypothesis 空间（更少的可怀疑的活动部件），并在阶段 5 变成一个干净的 regression test。

完成的标准是**每一个剩余元素都是承重的**：移除其中任何一个都会让 feedback loop 变绿。

在你已经 reproduce **和** minimise 之前，不要继续。

## 阶段 3：Hypothesise（假设）

在测试任何一个之前，生成 **3–5 个排序后的 hypothesis**。只生成单一 hypothesis 会锚定在第一个貌似合理的想法上。

每个 hypothesis 必须是**可证伪的**：说出它所做的预测。

> 格式："如果 <X> 是原因，那么 <改变 Y> 会让 bug 消失 / <改变 Z> 会让它更严重。"

如果你说不出预测，那这个 hypothesis 只是一种感觉：丢弃它，或把它锐化。

**在测试之前，把排序后的列表展示给用户。** 他们往往拥有能立即重新排序的领域知识（"我们刚部署了对 #3 的变更"），或者知道他们早已排除的 hypothesis。这是个便宜的检查点，能省大量时间。别被它卡住；如果用户不在（AFK），就用你的排序继续。

## 阶段 4：Instrument（仪表化）

每个探针必须对应阶段 3 的某个具体预测。**一次只改变一个变量。**

工具偏好：

1. **调试器 / REPL 检查**，如果环境支持的话。一个断点胜过十条日志。
2. **有目标的日志**，在能区分 hypothesis 的边界上。
3. 永远不要"记录一切然后 grep"。

**给每条调试日志打上唯一前缀**，例如 `[DEBUG-a4f2]`。收尾时的清理就变成一次 grep。未打标签的日志会残留；打标签的日志被清除。

**性能分支。** 对 performance regression，日志通常是错的。替代方案：先建立基线测量（计时 harness、`performance.now()`、profiler、查询计划），然后 bisect。先测量，后修复。

## 阶段 5：Fix + regression test（修复 + 回归测试）

**在修复之前**写 regression test，但前提是存在一个**正确的 seam**。

正确的 seam 是指：测试能在调用点实际发生 bug 的位置上，行使**真实的 bug 模式**。如果唯一可用的 seam 太浅（bug 需要多个调用方，却只有单调用方测试；无法重现触发 bug 的链条的 unit test），在那里写的 regression test 只会带来虚假的信心。

**如果不存在正确的 seam，这本身就是发现。** 记下它。是代码库架构在阻止这个 bug 被锁定。把它标记给下一阶段。

如果存在正确的 seam：

1. 把已 minimise（最小化）的 repro 变成那个 seam 上的失败测试。
2. 看着它失败。
3. 应用修复。
4. 看着它通过。
5. 针对原始的（未 minimise 的）场景重新运行阶段 1 的 feedback loop。

## 阶段 6：Cleanup（清理）

在宣布完成之前必须完成这些：

- [ ] 原始 repro 不再 reproduce（复现）（重新运行阶段 1 的 feedback loop）
- [ ] regression test 通过（或已记录 seam 缺失）
- [ ] 所有 `[DEBUG-...]` instrumentation 已移除（`grep` 该前缀）
- [ ] 一次性的原型已删除（或移到标记清晰的调试位置）
- [ ] 最终被证实正确的 hypothesis 写在了 commit / PR 消息里，这样下一个调试者能从中学习

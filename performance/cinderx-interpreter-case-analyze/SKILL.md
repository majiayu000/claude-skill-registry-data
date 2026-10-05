---
name: cinderx-interpreter-case-analyze
description: Use when benchmark 未进入 CinderX JIT，需要分析解释执行阶段、函数形状和 gate 策略。
---

# CinderX Interpreter Case Analyze

解释执行用例 / 非 JIT 用例不能硬套 HIR/LIR 结论。先证明 benchmark 本体未进入 CinderX JIT gate，或性能差距主要来自解释执行、gate 拒绝、运行时开销和 AutoJIT 分类决策，再做阶段分析。

## 前置证据

- 真实 pyperformance worker 命令和环境契约。
- `cinderx-jit-entry-check` 的 `entered_cinderx_jit=false`，或目标热函数未进入 gate 的证据。
- CPython JIT baseline、CinderX JIT 优化前、CinderX JIT 优化后的配对结果。
- perf、计数器、worker log、gate log、函数级调用次数或其它穿刺证据。

## 穿刺证据

穿刺证据必须把总耗时拆到可行动阶段，不能只写 speedup 结论。至少覆盖：

| 阶段 | 证据 |
|------|------|
| worker / benchmark 本体 | 真实 worker 命令、输入规模、warmup/loops、affinity、环境变量 |
| CPython JIT baseline | 基线结果、热点、JIT 状态、函数级证据 |
| CinderX JIT 优化前 | 优化前结果、gate / AutoJIT 状态、解释执行热点 |
| CinderX JIT 优化后 | 优化后结果、已改变阶段、残留热点 |
| 差距归因 | 哪些阶段贡献 gap，哪些阶段已被优化，哪些仍可优化 |

## 分阶段平铺表

输出一张平铺表，列必须包含：

| 阶段 | CPython JIT baseline | CinderX JIT 优化前 | gap | CinderX JIT 优化后 | 已优化量 | 剩余 gap | 证据 | 下一步 |
|------|----------------------|--------------------|-----|--------------------|----------|----------|------|--------|

要求：
- 每行只放一个阶段或一个可验证子阶段。
- `gap`、`已优化量`、`剩余 gap` 要有数值、比例或明确的定性证据。
- 不能把多个阶段揉成“解释器慢”一类结论。
- 没有证据的行标记为待补证据，不得当作根因。

## 函数形状表

分阶段平铺表之后，必须给函数形状表。基于 autojit 分类模型列出全量函数形状和 gate 策略，不只挑热点函数。

| 函数 | 模块/路径 | 调用/热度 | bytecode 形状 | 动态特性 | AutoJIT 分类 | gate 策略 | gate 结果 | 证据 |
|------|-----------|-----------|---------------|----------|--------------|-----------|-----------|------|

函数形状至少覆盖：
- loop、分支、异常处理、generator/coroutine、closure、globals、locals/freevars/cellvars。
- call 形态：Python call、C API、method/descriptor、vectorcall、dynamic dispatch。
- 数据形态：dict/list/tuple、attribute access、boxing/unboxing、type stability。
- AutoJIT 分类：可编译、待观察、拒绝、低收益、风险高、证据不足。
- gate 策略：阈值、白名单/黑名单、函数形状规则、平台规则、实验开关。

## 不进入 gate 的阶段详细拆解

只要有函数不进入 gate，就追加阶段详细拆解：

1. 发现：函数如何被发现，调用次数和热度是什么。
2. 分类：autojit 分类模型给出的函数形状和风险。
3. gate：命中哪条 gate 策略、阈值或拒绝规则。
4. 拒绝：不进入 gate 的直接原因。
5. fallback：解释执行 fallback 后落在哪些运行时阶段。
6. 代价：该拒绝对 CPython JIT baseline vs CinderX JIT 优化前 gap 的贡献。
7. 行动：调 gate、改函数形状支持、降低运行时开销或放弃优化的下一步。

## 输出

返回穿刺证据、分阶段平铺表、函数形状表、每个不进入 gate 函数的阶段详细拆解、已优化量、剩余 gap、风险和最小验证命令。

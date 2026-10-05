---
name: compiler-optimization-theory
description: Use when 解释或评估 CinderX 的 IR、优化 pass、指令调度与寄存器分配原理；指令规格用 isa-instruction-lookup。
---

# Compiler Optimization Theory

编译器中后端理论背景，供理解与评估 CinderX 的 IR、优化、调度、寄存器分配设计。
是"读后内化"型知识，与 `isa-instruction-lookup`（查规格）分工不同：
这里回答"为什么这样设计、有哪些方案、取舍是什么"，不回答"某指令编码是什么"。

## 来源声明

基于 Cooper & Torczon《Engineering a Compiler》**2nd edition**（Elsevier 2012）
PDF 逐章校对的概念提炼，引用到小节级（各 reference 头部标注 PDF 页码，
印刷页 ≈ PDF−25）。算法细节以该书为准。
linear scan / PBQP 不在本书 2e 正文，相关条目已单独标注原始文献出处。

## 何时读哪个

| 问题形态 | 读 |
|---|---|
| HIR/LIR 为什么分层？SSA 有什么好处？IR 设计的取舍轴？ | `references/intermediate-representations.md` |
| 某优化 pass 在做什么、为什么有效、pass 顺序怎么排？ | `references/optimization-fundamentals.md` |
| 机器码为什么这样排？延迟/占用率怎么权衡？循环怎么调度？ | `references/instruction-scheduling.md` |
| spill 为什么发生？图着色 vs 线性扫描？move elimination？ | `references/register-allocation.md` |

## 与现有技能的衔接

- 读 CinderX HIR/LIR dump 时：`cinderx-hir-lir-analyze` 负责取证据，本技能提供
  "这段 IR 形态说明编译器在做什么"的理论判读框架。
- 评审 JIT 改动时：`cinderx-jit-review` 负责正确性风险清单，本技能帮助判断
  "这个优化在编译理论上的前置条件是否满足"。
- 涉及具体指令行为/编码：一律转 `isa-instruction-lookup` 查库，本技能不覆盖。

## 理论 → 查证 硬规则（不可跳过）

本技能只回答"为什么这样设计、有哪些方案、取舍是什么"。**分析中一旦落到具体指令，
必须按"查证问题"调 `isa-reference` MCP。查证主体是语义与用法，不是分类和
feature**：category 只用于同名消歧（ABS 三域），`filter_by_environment` 只在
环境部署判定时用——优化替换经常**跨 category、跨 feature 域**（base 需求用
SIMD 指令满足、SVE 指令替换 base 序列都合法），候选检索不得被分类过滤。

| 查证问题 | 怎么查（工具 + 必做的比对动作） |
|---|---|
| **语义核对**：方案假设指令做 X（如"CSEL 无条件写 Rd"），它真的做 X 吗 | `lookup_instruction(mnemonic, verbose=True)` → **逐条读 `operation_pseudocode` 与方案的语义假设比对**；不一致即方案错误，不得当备注带过 |
| **用法核对**：这条汇编/lowering 写法合法吗、有什么编码陷阱 | 同上 verbose → 核对 `asm_templates`（合法语法形态）与 `operand_docs`（操作数约束：宽度限制、内存源语义、编码位要求）——陷阱在这里暴露（如 CMOVcc 不支持 8-bit 目的、内存源被无条件读） |
| **更优写法发现**：有没有语义一致但更高效的替换 | 按语义检索候选：`find_instruction_by_function` + `optimization-intent-map.md`（**跨 category/feature 不设限**）→ 每个候选取伪代码**比对语义一致** → 比较指令数/依赖链/副作用；微架构收益须 perf 证据 |
| **环境部署判定**（仅在确认目标机器支持时） | `filter_by_environment(env_features)`，feature 列表来自环境审计 |

判据：**方案对指令行为的每条语义假设，必须能在该指令 `operation_pseudocode`
里指出对应行；用法断言必须对应 `asm_templates`/`operand_docs` 条目**。
只回答"某指令是 base 类、无 feature 依赖"**不构成查证**——那只是可用性，
回答不了"语义符不符、用法对不对、有没有更优写法"。

## 边界

- 本技能是背景框架，不替代对 CinderX 实际代码的证据检查。
- 教材讲通用编译器；CinderX 的具体实现（Tiering、deopt、inline cache）以
  CinderX 代码和测试为准，理论只提供解释框架，不能作为 CinderX 行为的论据。

---
name: isa-instruction-lookup
description: Use when 查证 A64/x86 指令语义、编码、操作数或 feature 依赖，检索替代指令与跨平台等价候选。
---

# ISA Instruction Lookup

查询官方 ISA 规格的统一入口。数据只来自权威来源，经离线 ingest 进入
`mcp/isa-reference/data/isa.db`，通过 MCP 工具只读查询。

**当前库覆盖**：
- `a64`（2259 条，ARM-official XML 2026-06）：编码/伪代码/`FEAT_xxx` 全量
- `x86_64`（854 条 = Intel-SDM 771 + AMD-APM 特有 83）：opcode 表/伪代码/
  `CPUID:XXX` feature（Intel opcode 表 feature 列 + AMD 页内声明双源，约 1700 行）

## 何时用

- 读 JIT/反汇编机器码，要确认某助记符的编码、操作数约束或执行语义
- codegen 优化：找"做某件事"的指令（如条件选择、位反转、批量内存操作）
- 判断某指令依赖哪个 `FEAT_xxx`，目标环境（Kunpeng 等）是否实现
- 跨平台比对：某 A64 指令在 x86 侧的等价候选（或反向）

## 三层检索流程

按顺序降级，不要跳层：

1. **意图映射**：查询是优化意图（如"用条件选择取代比较和分支"）时，先读
   `references/optimization-intent-map.md` 把意图翻译成功能术语（→ "conditional select"）。
   已知助记符（如反汇编输出里的 `CSEL`）跳过此层。
2. **功能检索**：`find_instruction_by_function(description="conditional select")` —
   FTS 匹配 brief/authored，返回候选列表。描述用英文功能术语。
   **候选检索跨 category/feature 不设限**——优化替换经常跨执行域（base 需求
   用 SIMD 指令满足、SVE 替换 base 序列），分类和 feature 只是可用性维度，
   不是过滤条件。
3. **精确查询与查证**：候选定位后 `lookup_instruction(mnemonic, verbose=True)`。
   **查证主体与必做动作**：
   - `operation_pseudocode`——方案的每条语义假设（"无条件写 Rd"）逐行比对，
     不一致即方案错误；
   - `asm_templates`——合法语法形态，写汇编/lowering 的依据；
   - `operand_docs`——操作数约束（宽度限制、内存源语义、编码位要求），
     编码陷阱在这里暴露；
   - `bitfields`——具体编码位。
   `category` 只用于同名消歧，`features` 只用于环境部署判定——**这两者不是
   语义查证的输出**，只回答"是 base 类/无 feature 依赖"不构成查证。

跨平台等价：`find_equivalent_instruction(mnemonic, from_arch, to_arch)`。返回的是
**词面候选**（如 CMOVcc 的 a64 侧候选会混入 MOV 族）——先查
`references/optimization-intent-map.md` 的跨平台族映射（权威答案），机器候选用于
发现遗漏，**精确等价性必须比对双方 `operation_pseudocode` 后下结论**。

## 环境可用性判定

1. 环境侧 feature 列表：a64 来自 `/proc/cpuinfo` 或 `ID_AA64*` 系统寄存器解读
   （环境审计走 `cinderx-env-validate`）；x86_64 来自 CPUID flag 名（如
   `BMI2`、`SSE2`），传入时带 `CPUID:` 前缀或由工具直接匹配 flag 名。
2. `filter_by_environment(env_features=[...], arch=...)` 返回
   available / conditional / unavailable。`conditional` 表示该指令可用性还依赖
   操作数取值（如 sz 字段），必须读该指令 bitfields 后人工判读。
3. 同名指令跨执行域变体（ABS 有 base/SIMD/SVE 三版）靠返回的 `category` 消歧。

## 硬规则

- 库内 `source_authority` 只允许官方来源白名单，规则见
  `references/source-authority-policy.md`。非官方来源数据一律不入库。
- 指令的**微架构性能（吞吐/延迟）不在本库**——ISA 手册不含性能数据，
  性能结论走 perf/TRM 路径（`cinderx-isa-microarch-compare`）。
- 引用指令规格时必须带上来源（`source_doc` + `page_start`），便于回溯。
- 数据更新（新版本手册/新架构）只跑 `mcp/isa-reference/scripts/ingest_*.py`
  重建，不手改 isa.db。

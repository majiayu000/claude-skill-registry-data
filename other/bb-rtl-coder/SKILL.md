---
name: bb-rtl-coder
description: "资深RTL设计工程师，根据微架构文档（MAS、FSM、datapath）编写可综合的 SystemVerilog HDL代码。Generate synthesizable SystemVerilog RTL from MAS documents. Trigger: /bb-rtl-coder, RTL实现, SystemVerilog代码, 可综合HDL"
user-invocable: true
version: "2.0.0"
arguments:
  - name: project_dir
    description: "芯片项目目录路径（如 ./myChip），auto-detect by default"
    required: false
  - name: module_id
    description: "指定模块编号（如 M01），全部模块时为 all"
    required: false
    default: "all"
  - name: auto_approve
    description: "跳过用户批准点，自动生成所有RTL并调用 bb-code-review"
    required: false
    default: "false"
  - name: resume
    description: "Resume from last checkpoint"
    required: false
  - name: dry_run
    description: "Generate plan only, no RTL coding"
    required: false
  - name: parallel
    description: "Max parallel agents (default 4)"
    required: false
  - name: full
    description: "Force full run, ignore existing spec snapshot"
    required: false
handoffs:
  - target: bb-code-review
    condition: "RTL generation completed"
    session_note: "建议在新会话中执行 RTL 代码审查"
evolution:
  enabled: true
  trigger: on_failure
  max_attempts: 3
  protected_zones:
    - frontmatter.name
    - frontmatter.description
    - HARD-GATE section
    - 铁律 section
  depth_policy:
    conservative: auto
    local: auto
    system: confirm
  data_sources:
    - execution_log
    - evolution_history
    - failed_paths
    - external_search
---

<DEFAULTS>
output_dir: ./rtl
language: sv
auto_approve: false
project_dir: auto-detect
module_id: all
parallel: 4
dry_run: false
resume: false
full: false
synthesis_tool: generic
</DEFAULTS>

## Pipeline Position

```
spec_mas/ ──→ [bb-rtl-coder] ──→ rtl/ ──→ bb-code-review ──→ synthesis
      INPUT_DIR          OUTPUT_DIR        AUTO
```

---

## HARD-GATE 定义

```
<HARD-GATE>
在任何 RTL 生成操作前，必须完成以下步骤：

1. 定位 INPUT_DIR + 验证必需文档（MANDATORY）
   - 若用户提供路径，验证存在
   - 否则自动检测最新子目录
   - 每个模块必须有 MAS.md（至少有接口定义）
   - 叶子模块必须有 FSM.md 和 datapath.md

2. 创建工作目录（MANDATORY）
   ```bash
   mkdir -p {{ OUTPUT_DIR }}
   mkdir -p {{ CHECKPOINT_DIR }}
   mkdir -p {{ PROGRESS_DIR }}
   ```

3. 运行 Change Detection（MANDATORY）
   → 决定 full run 或 incremental run

禁止行为（在完成初始化前）：
- 加载 spec_mas 输入
- 启动 RTL 模块树生成
- 输出 RTL 文件
</HARD-GATE>
```

---

## 铁律（违反即停止）

> 以下规则不受 auto_approve 影响，任何模式下均不得绕过。

| 铁律 | 检查点 | 失败动作 |
|------|--------|----------|
| **Spec 先行铁律** | MAS 文件 < 2 份 | 拒绝执行，返回 bb-mas 阶段 |
| **叶子优先铁律** | 子模块 RTL 未完成 | 禁止开始父模块 RTL |
| **可综合性铁律** | RTL 有不可综合构造 | 立即修复，不继续 |
| **端口一致铁律** | 端口 ≠ MAS.md §2.1 | 立即修复，不继续 |
| **状态机编码铁律** | FSM 状态编码 ≠ FSM.md | 立即修复，不继续 |
| **并行上限铁律** | 子 agent > 6 | 拆分批次执行 |

---

## Global Paths

```
PROJECT_DIR       = {{ project_dir 参数 或 auto-detect }}
INPUT_DIR         = {{ PROJECT_DIR }}/spec_mas
OUTPUT_DIR        = {{ PROJECT_DIR }}/rtl
TEMPLATE_DIR      = ~/.claude/skills/bb-rtl-coder/templates
REFERENCE_DIR     = ~/.claude/skills/bb-rtl-coder/references
SCRIPT_DIR        = ~/.claude/skills/bb-rtl-coder/scripts
PROJECT_SCRIPTS   = {{ PROJECT_DIR }}/scripts
PROGRESS_DIR      = {{ OUTPUT_DIR }}/.progress
CHECKPOINT_DIR    = {{ OUTPUT_DIR }}/.checkpoint
SKILL_FILE        = ~/.claude/skills/bb-rtl-coder/SKILL.md
EVOLUTION_FRAMEWORK = ~/.claude/evolution-framework
```

---

## 增量更新机制

当 `/bb-mas` 重新生成或更新 `spec_mas/` 后再次执行 `/bb-rtl-coder`，自动检测变更并仅更新受影响模块。

### Spec Snapshot

每次成功执行后，将所有 spec 文件的哈希存入 `${CHECKPOINT_DIR}/spec_snapshot.json`：

```json
{
  "snapshot_time": "2026-05-16T12:00:00+08:00",
  "files": {
    "module_tree.md": "<sha256>",
    "M01/MAS.md": "<sha256>",
    "M01/FSM.md": "<sha256>",
    "M01/datapath.md": "<sha256>",
    "M02/MAS.md": "<sha256>"
  }
}
```

### Change Detection

在 Prerequisites 段自动执行：

```
IF spec_snapshot.json 不存在 → FULL RUN（首次执行）
IF spec_snapshot.json 存在 → 逐文件比较哈希：
  ├─ module_tree.md 变更 → 解析新增/删除/重组的模块
  ├─ M*/MAS.md 变更       → 标记该模块为 modified
  ├─ M*/FSM.md 变更       → 标记该模块为 modified
  ├─ M*/datapath.md 变更  → 标记该模块为 modified
  └─ 全部文件哈希一致    → SKIP（输出 "No spec changes detected"）
```

### Impact Classification

| 分类 | 触发条件 | 处理方式 |
|------|---------|---------|
| **added** | module_tree.md 中新增的模块 | 完整 RTL 生成流程 |
| **removed** | module_tree.md 中删除的模块 | 归档 RTL 到 `temp/deleted/` |
| **modified** | MAS/FSM/datapath 哈希变更 | 完整 RTL 重写 |
| **cascade** | 依赖 modified 模块的父模块 | 重新检查端口连接 |
| **unchanged** | 无变更且不依赖变更模块 | 跳过 |

---

## 规模感知执行模式

在读取 `module_tree.md` 后，统计总模块数并选择编排模式：

```bash
# 读取 SessionStart hook 预生成的上下文预算
cat ~/.claude/ctx_budget.env 2>/dev/null || echo "SAFE_TOKENS=100000"

SAFE_TOKENS=$(grep SAFE_TOKENS ~/.claude/ctx_budget.env | cut -d= -f2)
TOTAL_MODULES=$(grep -c "^- M" "${INPUT_DIR}/module_tree.md" 2>/dev/null || echo 0)

INLINE_MODULE_MAX=$(python3 -c "t=$SAFE_TOKENS; print(min(t//1000,30))")
BATCHED_MODULE_MAX=$(python3 -c "t=$SAFE_TOKENS; print(min(t//300,80))")

if   [ "$TOTAL_MODULES" -le "$INLINE_MODULE_MAX" ];  then MODE="inline"
elif [ "$TOTAL_MODULES" -le "$BATCHED_MODULE_MAX" ];  then MODE="batched"
else                                                        MODE="delegated"
fi

echo "Modules: $TOTAL_MODULES  inline≤$INLINE_MODULE_MAX  batched≤$BATCHED_MODULE_MAX → MODE=$MODE"
```

| 模式 | 适用规模 | Orchestrator context 策略 |
|------|---------|--------------------------|
| **inline** | ≤ 30 模块 | 所有模块追踪在当前 context |
| **batched** | 30 < modules ≤ 80 | 每批完成后 `/compact`，状态依赖 checkpoint |
| **delegated** | > 80 模块 | 每层派发 subagent，主 context 只追踪层级进度 |

### Context Budget 控制

- 每完成一个批次（4-8 模块）→ 执行 `/compact`
- `/compact` 前确保进度已写入 `${CHECKPOINT_DIR}/*.done`
- `/compact` 后从 checkpoint 文件恢复状态继续

---

## Execution Flow（MANDATORY）

**全程自动执行，无需用户确认。** 从叶子模块到父模块 + 综合检查 + 自动 impl-review + Fix Issues + Push。

```
Phase 1–4: RTL Generation（叶子→父） → Phase 5: Synthesis Check
      │
      ↓
Phase 6: Auto code-review（自动调用 bb-code-review）
      │ → 输出: ${OUTPUT_DIR}/.review/issues.md
      │
      ↓
Phase 7: Fix Issues（自动修复所有 CRITICAL/HIGH）
      │ → 修复 → 重检 → 迭代（最多 3 轮）
      │
      ↓
Phase 8: Push to Remote
      │
      ↓
Final Report 输出
```

---

## Phase 1：构建 RTL 模块树

### 1.1 输入规模检测

```bash
MAS_COUNT=$(find ${INPUT_DIR} -name "MAS.md" | wc -l)
FSM_COUNT=$(find ${INPUT_DIR} -name "FSM.md" | wc -l)

if [ "$MAS_COUNT" -lt 2 ]; then
    echo "ERROR: MAS 文件不足 2 份，返回 bb-mas 阶段"
    exit 1
fi
```

### 1.2 解析模块树

从 `spec_mas/module_tree.md` 读取模块层级结构：

```
M01_ALU/
├── M01a_IntegerALU/
│   └── M01a1_Adder/
│   └── M01a1_Multiplier/
├── M01b_FloatALU/
```

### 1.3 创建 RTL 目录结构

```bash
mkdir -p {{ OUTPUT_DIR }}/M01_ALU/src
mkdir -p {{ OUTPUT_DIR }}/M01_ALU/tb
mkdir -p {{ OUTPUT_DIR }}/M01a_IntegerALU/src
mkdir -p {{ OUTPUT_DIR }}/M01a_IntegerALU/tb
```

### 1.4 输出 RTL 模块树文档

写入 `{{ OUTPUT_DIR }}/rtl_tree.md`

---

## Phase 2：叶子模块 RTL 编写（并行）

### 子 agent 指令模板

```
## 任务：编写叶子模块 RTL

**路径规范**：
- 输入目录：{{ INPUT_DIR }}/{{ MODULE_PATH }}
- 输出文件：{{ OUTPUT_DIR }}/{{ MODULE_PATH }}/src/{{ MODULE_NAME }}.sv
- 参考文档：{{ REFERENCE_DIR }}/sv_coding_style.md

**输入文件**：
1. MAS.md — 接口定义、时序规格
2. FSM.md — 状态机定义
3. datapath.md — 数据通路结构
4. regmap.md — 寄存器映射定义（可选，有寄存器接口的模块必须提供）

**Traceability 注入规则**：

**A. Spec Header（模块级摘要）**：

每个 RTL 文件头部必须包含 Spec Header，为 AI agent 和人工 reviewer 提供快速上下文：

```systemverilog
//==============================================================================
// Module: {{ MODULE_NAME }}
// 
// SPEC HEADER
// ─────────────────────────────────────────────────────────────────────────────
// Source:       spec/MAS/{{ MODULE_ID }}_{{ MODULE_NAME }}/MAS.md
// Version:      {{ SPEC_VERSION }}
// Status:       {{ DRAFT|REVIEW|FROZEN }}
// Spec Hash:    {{ sha256:xxxxxxxxxxxx }}  ← 由 scripts/compute_spec_hash.py 计算
// REQ Coverage: REQ-{{ MODULE_ID }}-F01 ~ REQ-{{ MODULE_ID }}-F{{ MAX_F }}
// 
// Purpose:
//   {{ 一行描述模块功能 }}
// 
// Key Constraints:
//   [C1] {{ 关键约束 1，如：最大同时调度线程数: 2 }}
//   [C2] {{ 关键约束 2，如：op_valid → op_ready 响应时间: 1-5 cycles }}
//   [C3] {{ 关键约束 3，如：复位后 syst_mode = 0 }}
// 
// Dependencies:
//   - {{ 依赖模块 1，如：M02_SRAM (存储接口) }}
//   - {{ 依赖模块 2，如：M06_ClockManager (时钟源) }}
// 
// Traceability:
//   PRD:  spec/PRD/PRD.md §{{ SECTION }}
//   ARCH: spec/ARCH/{{ FILE }}.md §{{ SECTION }}
//   MAS:  spec/MAS/{{ MODULE_ID }}_{{ MODULE_NAME }}/MAS.md
//   REGMAP: spec/MAS/{{ MODULE_ID }}_{{ MODULE_NAME }}/regmap.md  ← 若有寄存器定义
// 
// Change Log:
//   {{ VERSION }} - {{ DATE }}: {{ CHANGE_DESCRIPTION }}
//==============================================================================
```

**B. REQ_ID 标注**：

1. 从 MAS.md §10 提取 REQ_ID 列表（REQ-M##-F## 格式）
2. 模块声明前添加：`// @requirement REQ-M##-F01, REQ-M##-F02 @auto:rtl-gen`
3. 选择性内联（避免过度标注）：

| 代码块类型 | 必须标注 | 示例 |
|-----------|---------|------|
| Module 声明 | ✅ | `module M01_DataflowController` |
| FSM (always_ff with case) | ✅ | 状态机实现 |
| 协议握手逻辑 | ✅ | handshake, AXI, APB |
| 关键计算路径 | ✅ | datapath, pipeline stages |
| 寄存器阵列 | ✅ | reg_file, context storage |
| 简单赋值 (assign) | ❌ | `assign valid = en && ready;` |
| 端口声明 | ❌ | `input logic clk;` |
| 参数定义 | ❌ | `parameter WIDTH = 32;` |

4. SVA 断言必须包含 `@verifies` + `@spec_ref` + `@constraint` 注释：

```systemverilog
// @verifies REQ-M##-F04
// @spec_ref MAS/{{ MODULE_ID }}/datapath.md §{{ SECTION }}
// @constraint {{ 自然语言约束说明 }}
property p_xxx;
    ...
endproperty
assert property (p_xxx)
    else $error("[SPEC §x.x] {{ 失败描述 }}");
```

**SVA 生成规则**：
1. 从 `verification.md` §3 断言列表读取断言规格（ID、条件、严重性）
2. 将每条断言转换为 SystemVerilog concurrent assertion
3. 每个 SVA 前添加 `@verifies REQ-M##-F##` 和 `@requirement REQ-M##-F##`
4. 断言失败时使用 `$error` 输出断言 ID 和描述

示例：
```systemverilog
//==============================================================================
// Module: M01_DataflowController
// 
// SPEC HEADER
// ─────────────────────────────────────────────────────────────────────────────
// Source:       spec/MAS/M01_DataflowController/MAS.md
// Version:      1.2
// Status:       FROZEN
// Spec Hash:    sha256:abc123def456
// REQ Coverage: REQ-M01-F01 ~ REQ-M01-F12
// 
// Purpose:
//   NPU 数据流控制器，协调 systolic array 的运算调度。
// 
// Key Constraints:
//   [C1] 最大同时调度线程数: 2
//   [C2] op_valid → op_ready 响应时间: 1-5 cycles
//   [C3] 复位后 syst_mode = 0 (inference mode)
// 
// Dependencies:
//   - M02_SRAM (存储接口)
//   - M06_ClockManager (时钟源)
// 
// Traceability:
//   PRD:  spec/PRD/PRD.md §3.1
//   ARCH: spec/ARCH/block_diagram.md §2
//   MAS:  spec/MAS/M01_DataflowController/MAS.md
//==============================================================================

// @requirement REQ-M01-F01, REQ-M01-F02 @auto:rtl-gen
module M01_DataflowController (
    input  logic clk,
    input  logic rst_n,
    ...
);

    // @requirement REQ-M01-F03
    always_ff @(posedge clk or negedge rst_n) begin
        ...
    end

    // @verifies REQ-M01-F04
    // @spec_ref MAS/M01/datapath.md §3.2
    // @constraint 握手协议: valid 拉高后，ready 必须在 1-5 个周期内响应
    property p_handshake;
        @(posedge clk) disable iff (!rst_n)
        valid |-> ##[1:5] ready;
    endproperty
    p_handshake_check: assert property (p_handshake)
        else $error("[SPEC §3.2] Handshake protocol violation: valid without ready");

    // @verifies REQ-M01-F05
    // @spec_ref MAS/M01/datapath.md §3.3
    // @constraint FIFO 不溢出: full 时禁止写入
    property p_fifo_no_overflow;
        @(posedge clk) disable iff (!rst_n)
        (fifo_full && wr_en) |-> ##0 1'b0;
    endproperty
    p_fifo_no_overflow_check: assert property (p_fifo_no_overflow)
        else $error("[SPEC §3.3] FIFO overflow: write when full");

endmodule
```

**RTL 质量要求**：
1. 端口定义：与 MAS.md §2.1 完全一致
2. 状态机：与 FSM.md 状态编码一致
3. 数据通路：实现 datapath.md 流水线结构
4. 可综合性：无 initial 块（除 testbench）、无 delay、无递归
5. 时钟域：单一时钟域；CDC 模块需标注
6. Traceability：每个功能块必须有 @requirement 注释

**禁止事项**：
- 禁止使用 `initial`（testbench除外）
- 禁止使用 `#delay`
- 禁止使用 `force/release`
- 禁止使用递归模块实例化
- 禁止使用 `wait` 语句
- 禁止省略 @requirement 注释

**寄存器接口生成**（当模块有 `regmap.md` 时）：

1. 从 `regmap.md` §1 读取寄存器列表，实现 APB 寄存器读写逻辑：
   - RW 寄存器：写更新、读返回当前值
   - RO 寄存器：写忽略、读返回硬件状态
   - W1C 寄存器：写 1 清零对应位
   - RESERVED 位：写入忽略

2. 生成寄存器文档和 SVA 断言：
   ```bash
   uv run $PROJECT_SCRIPTS/generate_regmap_doc.py \
       --regmap spec/MAS/{{ MODULE_ID }}/regmap.md \
       --output doc/regmap/

   uv run $PROJECT_SCRIPTS/generate_regmap_assertions.py \
       --regmap spec/MAS/{{ MODULE_ID }}/regmap.md \
       --output {{ OUTPUT_DIR }}/{{ MODULE_PATH }}/src/{{ MODULE_NAME }}_regmap_assertions.sv
   ```

3. 在 RTL 中 bind 生成的断言模块：
   ```systemverilog
   // 在 {{ MODULE_NAME }}.sv 末尾
   `ifdef FORMAL
   bind {{ MODULE_NAME }} {{ MODULE_NAME }}_regmap_assertions u_regmap_assertions (
       .clk(clk), .rst_n(rst_n),
       .addr(paddr), .sel(psel), .enable(penable),
       .write(pwrite), .wdata(pwdata), .rdata(prdata)
   );
   `endif
   ```
```

### 叶子模块 RTL 结构

```systemverilog
// {{ MODULE_NAME }}.sv
// Generated by rtl-coder from spec_mas/{{ MODULE_PATH }}

module {{ MODULE_NAME }} (
    // Clock & Reset
    input  logic        clk,
    input  logic        rst_n,
    
    // Input Ports (from MAS.md §2.1)
    input  logic [WIDTH-1:0]  {{ port_name }},
    ...
    
    // Output Ports (from MAS.md §2.1)
    output logic [WIDTH-1:0]  {{ port_name }},
    ...
);

    // FSM States (from FSM.md)
    typedef enum logic [N-1:0] {
        IDLE    = {{ encoding }},
        ACTIVE  = {{ encoding }},
        ...
    } state_t;
    
    state_t current_state, next_state;
    
    // Datapath Registers (from datapath.md)
    logic [WIDTH-1:0] {{ reg_name }};
    ...
    
    // FSM Sequential Logic
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            current_state <= IDLE;
            {{ reset_values }}
        end else begin
            current_state <= next_state;
            {{ sequential_updates }}
        end
    end
    
    // FSM Combinational Logic
    always_comb begin
        next_state = current_state;
        {{ default_outputs }}
        
        case (current_state)
            IDLE: begin
                if ({{ condition }}) begin
                    next_state = ACTIVE;
                    {{ state_outputs }}
                end
            end
            ...
        endcase
    end
    
    // Datapath Logic (from datapath.md)
    {{ datapath_logic }}
    
endmodule
```

---

## Phase 3：父模块 RTL 编写（逐层上卷）

从最深的父模块开始，逐层向上编写。

### 父模块 RTL 特殊内容

```systemverilog
module {{ PARENT_MODULE }} (
    // Top-level Ports (from MAS.md)
    ...
);

    // Sub-module Instantiations
    {{ SUB_MODULE_1 }} u_{{ SUB_MODULE_1 }} (
        .clk   (clk),
        .rst_n (rst_n),
        {{ port_connections }}
    );
    
    {{ SUB_MODULE_2 }} u_{{ SUB_MODULE_2 }} (
        ...
    );
    
    // Inter-module Connections
    logic [WIDTH-1:0] {{ interconnect_signal }};
    
    // Top-level FSM Coordination (if applicable)
    {{ top_fsm }}
    
endmodule
```

### 端口连接原则

- 子模块输出 → 父模块内部信号
- 子模块输入 → 父模块内部信号或顶层端口
- 端口位宽必须匹配

---

## Phase 4：Testbench 生成

### Testbench 结构

```systemverilog
// tb_{{ MODULE_NAME }}.sv
// Testbench for {{ MODULE_NAME }}

`timescale 1ns/1ps

module tb_{{ MODULE_NAME }};
    
    // Clock & Reset Generation
    logic clk;
    logic rst_n;
    
    initial begin
        clk = 0;
        forever #{{ CLOCK_PERIOD }} clk = ~clk;
    end
    
    initial begin
        rst_n = 0;
        #{{ RESET_PERIOD }};
        rst_n = 1;
    end
    
    // DUT Instance
    {{ MODULE_NAME }} dut (
        .clk   (clk),
        .rst_n (rst_n),
        {{ port_connections }}
    );
    
    // Test Sequences (from verification.md)
    initial begin
        {{ test_sequence_1 }}
        {{ test_sequence_2 }}
        ...
        $finish;
    end
    
    // Assertions (from verification.md)
    {{ assertions }}
    
    // Waveform Dump
    initial begin
        $dumpfile("{{ MODULE_NAME }}.vcd");
        $dumpvars(0, tb_{{ MODULE_NAME }});
    end
    
endmodule
```

---

## Phase 5：综合性检查（MANDATORY）

### 5.1 可综合性规则检查

```bash
python3 {{ SCRIPT_DIR }}/synthesis_check.py \
    --input {{ OUTPUT_DIR }}/{{ MODULE_PATH }}/src \
    --report {{ OUTPUT_DIR }}/{{ MODULE_PATH }}/syn_check.json
```

| 规则 | 描述 | 严重性 |
|------|------|--------|
| NO_INITIAL | 禁止 initial 块（TB除外） | CRITICAL |
| NO_DELAY | 禁止 #delay 语句 | CRITICAL |
| NO_FORCE | 禁止 force/release | CRITICAL |
| NO_WAIT | 禁止 wait 语句 | CRITICAL |
| NO_RECURSION | 禁止递归实例化 | CRITICAL |
| NO_LATCH | 禁止锁存器生成 | HIGH |
| SINGLE_CLOCK | 单时钟域检查 | HIGH |
| PORT_WIDTH | 端口位宽一致性 | HIGH |
| FSM_ENCODING | FSM 状态编码一致性 | HIGH |

### 5.2 Gap Analysis（类似 Coverage Gap Analysis）

**若检查发现问题，必须执行以下步骤：**

1. **识别问题位置**
   ```bash
   python3 -c "import json; r=json.load(open('syn_check.json')); print([i for i in r['issues'] if i['severity']=='CRITICAL'])"
   ```

2. **问题分类处理**

   | 类型 | 处理方式 |
   |------|---------|
   | **不可综合构造** | 立即删除/替换 |
   | **锁存器生成** | 添加默认值/完整分支 |
   | **端口不匹配** | 调整位宽/添加显式转换 |
   | **状态编码错误** | 复制 FSM.md 编码 |

3. **修复验证循环**
   - 修复 → 重检 → 直到无 CRITICAL/HIGH

**禁止行为**：
- ❌ 跳过问题分析
- ❌ 声称"只有一个 latch 问题不大"
- ❌ 在有 CRITICAL问题时继续下一阶段

---

## Phase 6：自动 impl-review（MANDATORY AUTO）

**自动执行，无需用户确认。** 调用 `bb-code-review` 进行对抗性评审：

```markdown
Skill(skill="bb-code-review", args="--spec_path ${INPUT_DIR} --code_dir ${OUTPUT_DIR}")

# 等待评审完成，读取问题清单
issues_file = "${OUTPUT_DIR}/.review/issues.md"
```

若评审失败 → 报告错误并终止。

---

## Phase 7：Fix Issues（MANDATORY AUTO）

**自动执行，无需用户确认。** 根据 impl-review 输出的问题清单自动修复。

### 7.1 问题加载与分级处理

```bash
ISSUES_FILE="${OUTPUT_DIR}/.review/issues.md"
python3 - <<'EOF'
import re, pathlib
content = pathlib.Path("${ISSUES_FILE}").read_text()
issues = re.findall(r'###\s+\[([A-Z]+-\d+)\].*?Severity:\s+(CRITICAL|HIGH|MEDIUM|LOW)', content, re.DOTALL)
critical = [i for i in issues if i[1] == 'CRITICAL']
high = [i for i in issues if i[1] == 'HIGH']
print(f"CRITICAL: {len(critical)}, HIGH: {len(high)}")
EOF
```

### 7.2 修复执行顺序

```
修复优先级：CRITICAL → HIGH → MEDIUM
每个问题修复后立即运行综合检查验证
```

### 7.3 修复迭代与重审

- 若仍有 CRITICAL/HIGH 问题 → 重复 Phase 7（最多 3 轮）
- 若 3 轮后仍有 CRITICAL/HIGH → 标记 blocked，请求用户介入

### 7.4 修复完成标准

| 标准 | 要求 |
|------|------|
| CRITICAL issues | 0 |
| HIGH issues | 0 |
| MEDIUM issues | 允许存在（输出警告） |
| Synthesis check | 无 CRITICAL/HIGH |

---

## Phase 8：Traceability CSV 生成 + Push to Remote

### 8.1 生成 impl phase CSV

从 RTL 文件中的 `@requirement` 注释扫描 REQ_ID，生成 `traceability/requirements_matrix.impl.csv`：

```bash
uv run $PROJECT_SCRIPTS/babel_traceability.py impl
uv run $PROJECT_SCRIPTS/babel_traceability.py src
```

### 8.2 唯一性检查

```bash
uv run $PROJECT_SCRIPTS/check_req_uniqueness.py --check-deleted
```

### 8.3 Push

```bash
git push
```

---

## Error Handling

| Scenario | Action | Skip? |
|----------|--------|-------|
| MAS 文件 < 2 | 拒绝执行，返回 bb-mas | ❌ NO |
| 子模块未完成 | 禁止父模块 | ❌ NO |
| 综合检查 CRITICAL | 立即修复 | ❌ NO |
| 端口定义不一致 | 立即修复 | ❌ NO |
| FSM 编码不一致 | 立即修复 | ❌ NO |
| impl-review 执行失败 | 报告错误，终止 | ❌ NO |
| Fix Issues 测试失败 | Debug loop (max 5) | ❌ NO |
| Fix Issues 3 轮仍有 CRITICAL/HIGH | Mark blocked, ask user | ⚠️ Ask |
| Debug > 10 still FAIL | Mark blocked, ask user | ⚠️ Ask |

---

## Commit Strategy

**Per-module commits**（granular for rollback）：

```bash
git commit -m "feat({{ MODULE_ID }}): implement {{ MODULE_ID }} RTL

Leaf-to-parent complete
Synthesis check: passed
Checklist: {{ ITEMS_PASSED }}/total"
```

---

## Module Complete Checkpoint

```bash
touch {{ CHECKPOINT_DIR }}/{{ MODULE_ID }}.done
```

写入 progress JSON 到 `{{ PROGRESS_DIR }}/{{ MODULE_ID }}.json`

---

## 最终验证清单

- [ ] 所有叶子模块 RTL 文件存在
- [ ] 端口定义与 MAS.md §2.1 一致
- [ ] FSM 状态编码与 FSM.md 一致
- [ ] 综合性检查通过（无 CRITICAL/HIGH）
- [ ] Testbench 文件存在
- [ ] impl-review 无 CRITICAL/HIGH 问题
- [ ] frontmatter 格式正确

---

## Key Principles

| Principle | Level |
|-----------|-------|
| 全程自动执行，不在 phase/batch 间暂停确认 | 🔴 MANDATORY |
| 叶子优先执行顺序 | 🔴 MANDATORY |
| 可综合性检查必须通过 | 🔴 MANDATORY |
| Gap Analysis + 死代码检测（synthesis） | 🔴 MANDATORY |
| Debug iteration（no skip/bypass） | 🔴 MANDATORY |
| **彻底完成，不接受"足够好"** | 🔴 MANDATORY |
| 同层并行（无冲突） | 🟢 RECOMMENDED |
| 冲突检测后再并行 | 🔴 MANDATORY |
| Per-module checkpoint | 🔴 MANDATORY |
| Per-module commit | 🔴 MANDATORY |
| Spec snapshot after successful run | 🔴 MANDATORY |
| 增量更新 via change detection | 🔴 MANDATORY |
| `/compact` after each batch | 🟡 RECOMMENDED |
| 自动调用 bb-code-review | 🔴 MANDATORY |
| 自动修复所有 CRITICAL/HIGH 问题 | 🔴 MANDATORY |

---

## Output Structure

```
PROJECT_DIR/
├── spec_mas/            # INPUT_DIR
├── rtl/                 # OUTPUT_DIR
│   ├── .checkpoint/     # Module checkpoints (.done files)
│   ├── .progress/       # Progress tracking (.json files)
│   ├── .review/         # impl-review output
│   ├── M01/src/         # RTL source files
│   ├── M01/tb/          # Testbench files
│   └── rtl_tree.md      # RTL module tree
└── temp/deleted/        # Archived removed modules
```

---

## 参考文档

详见 `references/` 目录：
- `sv_coding_style.md` — SystemVerilog 编码规范
- `synthesizable_rules.md` — 可综合性指南

**项目级 Coding Style 参考**：
- `wiki/codingstyle/systemverilog_styleguide.md` — SystemVerilog Style Guide (systemverilog.io)
- `wiki/codingstyle/freescale_verilog_standard.md` — Freescale Verilog HDL Coding Standard SRS V3.2

---

## 辅助脚本

详见 `scripts/` 目录：
- `synthesis_check.py` — 综合性检查

---

## 常见陷阱

详见 `Gotcha/` 目录：
- `rtl_pitfalls.md` — RTL 编码常见陷阱

---

## 常见借口（均无效）

| Agent 的借口 | 为什么错 |
|-------------|---------|
| "这个模块很简单，不需要 FSM" | 没有 FSM 意味着状态逻辑隐藏，调试困难 |
| "initial 块只是用来初始化寄存器" | 综合工具忽略 initial，仿真与综合不一致 |
| "delay 语句用于仿真调试" | delay 导致仿真时序与实际硬件不一致 |
| "先写 RTL，再回过头补充 testbench" | 无 testbench 无法验证功能正确性 |
| "父模块可以先写，子模块并行实现" | 父模块端口连接依赖子模块接口定义 |
| "只有一个 latch 问题不大" | 锁存器会导致时序分析和功耗问题 |

---

## Evolution Trigger Point

When any Phase fails or user triggers `/evolve`:

1. **Detect failure**: Read `{{ OUTPUT_DIR }}/execution.log`
2. **Invoke framework**:
   ```bash
   bash {{ EVOLUTION_FRAMEWORK }}/evolve.sh \
     --skill "{{ SKILL_FILE }}" \
     --output "{{ OUTPUT_DIR }}" \
     --failure-phase "{{ FAILED_PHASE }}"
   ```
3. **Framework handles**: Analyze, modify, validate, rollback
4. **Retry or escalate**
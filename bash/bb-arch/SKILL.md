---
name: bb-arch
description: "从粗略 idea 设计芯片或功能模块架构，输出专业架构文档到 spec_arch 目录。Trigger: 芯片架构设计, IC架构, 电路模块设计, 硬件架构. Generate IC/Chip architecture specification from rough ideas."
user-invocable: true
adaptive: true
self-evolving: true
version: "1.0.0"
arguments:
  - name: idea_dir
    description: "包含 idea 文件的目录路径（markdown 或 drawio 文件）"
    required: true
  - name: project_dir
    description: "项目目录路径，默认自动检测"
    required: false
  - name: scope
    description: "设计范围：chip（整个芯片）或 block（单个IP模块）"
    required: false
    default: "chip"
  - name: auto_approve
    description: "跳过用户批准点，自动继续"
    required: false
    default: "false"
  - name: finetune
    description: "启用详细调试输出模式"
    required: false
    default: "false"
  - name: update
    description: "更新模式：auto（自动检测变更）| full（强制归档+全量重建）| patch（强制就地更新，不归档）"
    required: false
    default: "auto"
handoffs:
  - target: bb-spec-review
    condition: "Architecture spec completed"
    session_note: "建议在新会话中执行对抗性 spec-review"
    transfer_files:
      - "{{OUTPUT_DIR}}/*.md"
evolution:
  enabled: true
  trigger: on_failure
  max_attempts: 3
---

<DEFAULTS>
output_dir: ./spec_arch
scope: chip
language: zh-CN
finetune: false
auto_approve: false
update: auto
</DEFAULTS>

# bb-arch — 芯片架构设计生成器

从粗略 idea 设计芯片或 IP 模块的架构规范文档。

## Self-Adaptive 初始化

初始化目录结构 `.skills_local/bb-arch/`，收集项目上下文，解析路径。

---

## HARD-GATE 定义

```
<HARD-GATE>
在任何架构设计操作前，必须完成以下步骤：

1. Self-Adaptive 初始化 + 项目上下文收集
   ```bash
   SCRIPT_DIR=~/.claude/scripts
   python3 "$SCRIPT_DIR/adaptive/adaptive_init.py" \
     --skill "bb-arch" \
     --project-dir "{{ PROJECT_DIR }}"
   ```
   成功标志：
   - `.skills_local/bb-arch/local.json` 存在
   - `.skills_local/bb-arch/project_context.json` 存在
   - `.skills_local/bb-arch/paths.json` 存在

2. 加载配置文件
   ```python
   import json
   
   with open(".skills_local/bb-arch/project_context.json") as f:
       CONTEXT = json.load(f)
   
   DESIGN_TYPE = CONTEXT.get("design_type", "asic")  # asic, fpga, analog
   TECHNOLOGY = CONTEXT.get("technology", "unknown")  # 28nm, 40nm, etc.
   
   with open(".skills_local/bb-arch/paths.json") as f:
       PATHS = json.load(f)
   
   OUTPUT_DIR = PATHS["resolved_paths"]["OUTPUT_DIR"]
   INPUT_DIR = PATHS["resolved_paths"]["INPUT_DIR"]
   LOG_DIR = PATHS["resolved_paths"]["LOG_DIR"]
   ```

3. 创建执行日志目录
   ```bash
   mkdir -p "${LOG_DIR}"
   LOG_FILE="${LOG_DIR}/bb-arch-$(date -u +%Y%m%dT%H%M%S).log"
   echo "[$(date -u +%Y%m%dT%H%M%SZ)] [INFO] HARD-GATE: 初始化完成" >> "${LOG_FILE}"
   ```

禁止行为（在完成初始化前）：
- 加载 idea 输入
- 启动架构设计流程
- 输出规范文档
</HARD-GATE>
```

---

## 铁律（违反即停止）

> 以下规则不受 auto_approve 影响，任何模式下均不得绕过。

1. **PRD 先行铁律**：无 `prd/PRD.md` 或 `prd/IP_PRD.md` → 拒绝执行，架构设计必须有 PRD 作为约束边界
2. **CDC 完整铁律**：时钟域边界未定义同步策略 → Phase 4 不通过；留白 CDC 方案等同于硅片缺陷
3. **电源域边界铁律**：跨域信号缺少 isolation cell 定义 → Phase 5 不通过
4. **DFT 早期铁律**：DFT 策略必须在 Phase 8 完成，禁止推迟到 RTL 阶段（后期插入成本极高）
5. **范围锁定铁律**：PRD 未明确提及的功能不纳入架构设计，即使技术上可行

---

## Global Paths

```
PROJECT_DIR       = {{ --project_dir 或 auto-detect }}
INPUT_DIR         = {{ idea_dir 参数 }}
OUTPUT_DIR        = {{ PROJECT_DIR }}/spec_arch
SCRIPT_DIR        = ~/.claude/scripts
PROJECT_SCRIPTS   = {{ PROJECT_DIR }}/scripts
SKILL_FILE        = ~/.claude/skills/bb-arch/SKILL.md
KNOWLEDGE_DIR     = ~/.claude/skills/bb-arch/knowledge
TEMPLATE_DIR      = ~/.claude/skills/bb-arch/templates
```

---

## 知识库引用

以下文件按需加载，用于特定设计阶段：

| 文件 | 加载时机 | 用途 |
|------|----------|------|
| `knowledge/clock_reset_design.md` | Phase 4 | 时钟域划分、复位策略 |
| `knowledge/power_design.md` | Phase 5 | 电源域划分、功耗估算 |
| `knowledge/dft_strategy.md` | Phase 6 | 可测试性设计 |
| `knowledge/verification_strategy.md` | Phase 7 | 验证计划 |
| `references/ic-terminology.md` | 全流程 | IC 专业术语参考 |

**项目级 Coding Style 参考**（RTL 设计阶段）：
- `wiki/codingstyle/systemverilog_styleguide.md` — SystemVerilog Style Guide (systemverilog.io)
- `wiki/codingstyle/freescale_verilog_standard.md` — Freescale Verilog HDL Coding Standard SRS V3.2

---

## 输入

- `INPUT_DIR/*.md`：idea 文本描述
- `INPUT_DIR/*.drawio`：架构草图（可选）

---

## 输出目录结构

### scope=chip（芯片级）

```
spec_arch/
├── chip_overview.md           # 芯片概述与特性表
├── block_diagram.md           # 系统框图（Mermaid）
├── clock_reset_spec.md        # 时钟复位架构
├── memory_map.md              # 存储架构与地址映射
├── power_spec.md              # 电源架构
├── io_pinout.md               # IO与引脚定义
├── security_spec.md           # 安全架构（可选）
├── dft_spec.md                # 可测试性设计
├── verification_plan.md       # 验证策略
├── ip_blocks/                 # 各IP模块详细设计
│   ├── cpu_core.md
│   ├── memory_ctrl.md
│   ├── peripheral_x.md
│   └── ...
└── design_notes.md            # 设计说明与约束
```

### scope=block（IP模块级）

```
spec_arch/
├── block_overview.md          # 模块概述
├── theory_of_operation.md     # 工作原理
├── block_diagram.md           # 模块框图
├── interface_spec.md          # 接口规范
├── register_map.md            # 寄存器映射
├── design_details.md          # 设计细节
├── programmer_guide.md        # 编程指南
└── verification_checklist.md  # 验证清单
```

---

# 执行流程

## 增量更新机制

每次成功完成后，将输入文件哈希写入 `<output_dir>/.archive/input_snapshot.json`。下次执行时在 Phase 0 之前自动比对。

### 输入快照格式

```json
{
  "snapshot_time": "<ISO8601+08:00>",
  "skill": "bb-arch",
  "input_files": {
    "<relative-path>": "<sha256>"
  }
}
```

### Phase -1: 变更检测（所有 Phase 前强制执行）

```
IF update=full  → 跳过检测，走 MAJOR 路径
IF update=patch → 跳过检测，走 MINOR 路径
ELSE (auto):
  IF input_snapshot.json 不存在
    → FULL RUN（首次执行，不归档）
  ELSE
    sha256sum PRD.md 及 idea_dir/ 下所有文件
    与 snapshot 对比
    IF 哈希全部一致 → 输出 "输入未变更，跳过生成" 并退出
    IF 哈希有差异   → 按下表分类
```

### 变更分类

| 条件（满足任意一条） | 分类 |
|---------------------|------|
| PRD 中协议列表变更（增删/重命名） | **MAJOR** |
| PRD 中模块/IP 组成变更（增删） | **MAJOR** |
| scope 变更（chip ↔ ip） | **MAJOR** |
| PRD 内容字符数变化 > 30% | **MAJOR** |
| PRD 中主要章节（## 级）数量变化 | **MAJOR** |
| 其他所有变更（描述细化、指标小幅调整等） | **MINOR** |

### MAJOR 路径：归档 + 全量重建

```bash
TIMESTAMP=$(date -u +%Y%m%dT%H%M%S)
ARCHIVE="{{ OUTPUT_DIR }}/.archive/$TIMESTAMP"
mkdir -p "$ARCHIVE"
for f in "{{ OUTPUT_DIR }}"/*.md "{{ OUTPUT_DIR }}"/*.json; do
  [ -f "$f" ] && mv "$f" "$ARCHIVE/"
done
[ -d "{{ OUTPUT_DIR }}/ADR" ] && mv "{{ OUTPUT_DIR }}/ADR" "$ARCHIVE/"
echo "{\"reason\":\"MAJOR\",\"timestamp\":\"$TIMESTAMP\"}" > "$ARCHIVE/CHANGE_REASON.json"
```

归档完成后执行 FULL RUN（从 Phase 0 正常继续）。

### MINOR 路径：就地更新

根据变更内容决定重跑的最早 Phase：

| 变更内容 | 从此 Phase 重跑 |
|---------|----------------|
| 时钟/复位/电源域调整 | Phase 4 起 |
| IO/存储架构调整 | Phase 6 起 |
| DFT 策略调整 | Phase 8 起 |
| 验证策略调整 | Phase 11 起 |
| 其他 MINOR 变更 | Phase 3（系统概述）起 |

未受影响的 Phase 输出保持不变。完成后更新 `{{ OUTPUT_DIR }}/.archive/input_snapshot.json`。

---

## Phase 0: 输入解析

1. 读取 `INPUT_DIR` 目录内容
2. 解析 `.md` 文件提取关键需求
3. 解析 `.drawio` 文件提取架构草图（如有）
4. 确定设计范围：
   - `scope=chip`：整体芯片架构
   - `scope=block`：单个 IP 模块架构

输出产物：`parsed_requirements.json`（暂存上下文）

## Phase 1: 需求澄清

**auto_approve 模式**：基于文档推断需求，不使用 AskUserQuestion。

**澄清重点**：
- 目标应用场景（消费电子、汽车、工业、安全）
- 性能指标（主频、吞吐量、功耗预算）
- 技术节点（28nm, 40nm, 65nm, FPGA）
- 安全等级需求（是否需要 Root of Trust）
- 外设接口需求（UART, SPI, I2C, USB, PCIe 等）

**输出产物**：
```yaml
clarified_requirements:
  application: [...]
  performance_targets: [...]
  technology_node: [...]
  security_level: [...]
  interfaces: [...]
  open_questions: [...]
```

## Phase 2: 竞品/基准调研

并行启动多个 Agents：

### Agent 配置

```yaml
Agent_1:
  name: "Chip-Search"
  subagent_type: "Explore"
  prompt: |
    Search GitHub for similar chip/IC designs:
    - Query: "{{芯片类型}} {{技术栈}} stars:>50"
    - Focus: OpenTitan, Chipyard, OpenROAD, caravel
    
    Report:
    1. Repository list with architecture docs
    2. Block diagrams observed
    3. Clock/reset strategies used
    4. Memory architectures
    
    Thoroughness: medium

Agent_2:
  name: "Docs-Lookup"
  subagent_type: "docs-lookup"
  prompt: |
    Fetch documentation for:
    - RISC-V processor architecture
    - TileLink bus protocol
    - ASIC design flow
    
    Return: key patterns, interface standards

Agent_3:
  name: "WebSearch"
  subagent_type: "general-purpose"
  prompt: |
    Search for:
    - "{{芯片类型}} architecture design patterns"
    - "{{技术节点}} low power techniques"
    - "SoC security architecture best practices"
    
    Summarize: proven approaches, common pitfalls
```

整合调研结果到 `${OUTPUT_DIR}/research_report.md`。

## Phase 3: 系统概述设计

根据 scope 选择模板：

**scope=chip**：
1. 使用 `templates/chip_arch_template.md`
2. 编写芯片概述（功能特性表）
3. 绘制系统级 Block Diagram（Mermaid）
4. 定义模块划分与编号（M00X）

**scope=block**：
1. 使用 `templates/ip_block_template.md`
2. 编写模块概述
3. 绘制模块级 Block Diagram

**输出产物**：
- `chip_overview.md` 或 `block_overview.md`
- `block_diagram.md`

## Phase 4: 时钟与复位架构

**加载知识库**：`knowledge/clock_reset_design.md`

**设计内容**：
1. 时钟源定义（外部晶振、PLL、内部生成）
2. 时钟域划分与跨域处理（CDC）
3. 时钟频率规划（主频、外设频率、低功耗频率）
4. 复位策略（同步/异步、全局/局部）
5. 复位序列与上电流程

**输出产物**：`clock_reset_spec.md`

**验收标准**：
- 所有时钟域已定义频率和用途
- CDC 策略已明确
- 复位源已列举

## Phase 5: 电源架构

**加载知识库**：`knowledge/power_design.md`

**设计内容**：
1. 电源域划分（Always-on, Main, IO）
2. 供电电压定义（VDD, VIO, AVDD）
3. 功耗估算（动态功耗、静态功耗）
4. 低功耗策略（Clock gating, Power gating, Sleep modes）
5. 电源管理模块设计

**输出产物**：`power_spec.md`

**验收标准**：
- 电源域边界清晰
- 各域功耗预算已估算
- 低功耗策略已选定

## Phase 6: 存储与 IO 架构

**设计内容**：
1. 存储类型定义（ROM, SRAM, Flash, OTP, Register File）
2. Memory Map 地址分配
3. 存储控制器设计要点
4. IO 引脚定义（Fixed IO, Muxed IO）
5. 外设接口规格（UART, SPI, I2C, GPIO 等）

**输出产物**：
- `memory_map.md`
- `io_pinout.md`

## Phase 7: 安全架构（可选）

当需求包含安全等级时启用。

**设计内容**：
1. Secure Boot 流程
2. Crypto IP 选型（AES, SHA, RNG, Key Manager）
3. Lifecycle Management（Test, Dev, Prod）
4. Access Control 策略
5. Physical Security 考虑

**输出产物**：`security_spec.md`

## Phase 8: DFT 策略

**加载知识库**：`knowledge/dft_strategy.md`

**设计内容**：
1. Scan Chain 设计（插入策略、覆盖率目标）
2. BIST 设计（Memory BIST, Logic BIST）
3. JTAG/Debug 接口
4. ATPG 要求
5. Test Mode 定义

**输出产物**：`dft_spec.md`

**验收标准**：
- Scan coverage target ≥ 95%
- Memory BIST 策略已定义
- Debug 接口已指定

## Phase 9: IP 模块详细设计（scope=chip 时）

对每个主要 IP 模块，使用 IP Block 模板生成详细设计文档：

**设计内容**：
1. Theory of Operation
2. Block Diagram
3. Interface Specification（信号列表、时序图）
4. Register Map
5. Design Details（数据通路、状态机）
6. Programmer's Guide

**输出产物**：`ip_blocks/*.md`

## Phase 10: REQ_ID 分解

**目的**：将系统级需求分解到模块级 REQ_ID，建立 traceability 基础。

### 分解规则

```
REQ-SYS-## (PRD)  → REQ-M##-F## (模块级功能)
REQ-ARCH-## (ARCH) → REQ-M##-F## (模块级功能)
REQ-NFR-## (PRD)  → 贯穿全 pipeline（PPA/功耗/时序约束）
```

### 分解步骤

1. 读取 `spec/PRD/PRD.md` 中的 REQ-SYS-## 列表
2. 读取 `spec/ARCH/` 中的 REQ-ARCH-## 列表
3. 对每个 IP 模块，分解出 REQ-M##-F## 列表
4. 使用 `$PROJECT_SCRIPTS/allocate_req_id.py` 自动分配编号：
   ```bash
   uv run $PROJECT_SCRIPTS/allocate_req_id.py 01  # → REQ-M01-F01
   ```
5. 在 IP block 文档中嵌入 REQ_ID 标注

### 输出产物

- 各 IP block 文档中的 REQ_ID 标注
- `traceability/requirements_matrix.prd.csv`（从 PRD 生成）
- `traceability/requirements_matrix.arch.csv`（从 ARCH 生成）

```bash
uv run $PROJECT_SCRIPTS/babel_traceability.py prd
uv run $PROJECT_SCRIPTS/babel_traceability.py arch
```

---

## Phase 11: 验证策略

**加载知识库**：`knowledge/verification_strategy.md`

**设计内容**：
1. 验证层次定义（Unit, Integration, System, Silicon）
2. 验证方法选择（Simulation, Formal, Emulation, FPGA）
3. Coverage 目标（功能覆盖率、代码覆盖率）
4. Testbench 架构
5. 关键测试场景

**输出产物**：`verification_plan.md`

## Phase 12: 对抗性评审

**调用评审**：
```markdown
Skill(skill="it.spec-review", args="--spec-path {{ OUTPUT_DIR }} --output-dir {{ OUTPUT_DIR }}/.review")
```

**评审维度映射**：

| 文档 | 评审维度 |
|------|----------|
| clock_reset_spec.md | CDC 完整性、复位覆盖 |
| power_spec.md | 功耗预算合理性、低功耗策略可行性 |
| memory_map.md | 地址冲突、访问权限 |
| dft_spec.md | Coverage 目标可达性 |
| ip_blocks/*.md | 接口一致性、状态机完整性 |

**自动修复循环**：最多 5 次迭代。

## Phase 13: 总结与交付

1. 生成 `design_notes.md` 总结报告
2. 验证 traceability CSV 完整性：
   ```bash
   uv run $PROJECT_SCRIPTS/check_req_uniqueness.py
   ```
3. 更新 manifest
4. 清理上下文

---

# 设计原则

## IC 特有原则

1. **时钟域隔离**：每个时钟域边界必须有明确的 CDC 策略
2. **复位完整性**：所有寄存器必须有复位值定义
3. **电源域边界**：跨电源域信号需要 isolation cell
4. **DFT 优先**：设计初期规划测试结构，而非后期插入
5. **安全纵深**：安全功能需要硬件+固件+软件多层防护

## Agent-aware 文档设计

1. 模块编号便于引用（M00X, IP00X）
2. 信号命名规范（`clk_sys`, `rst_main_n`, `data_in[31:0]`）
3. 表格优于文字（寄存器表、信号表）
4. Mermaid 图表代替手绘流程
5. 引用明确的文档路径

---

## 常见借口（均无效）

| Agent 的借口 | 为什么错 |
|-------------|---------|
| "PRD 还没完成，但可以先做架构框架" | 无 PRD 的架构设计必然返工——PRD 是架构的约束边界，先做等于在沙上建房 |
| "CDC 问题可以在 RTL 阶段再处理" | CDC bug 是 silicon 缺陷第一大来源；架构阶段未定则 RTL 无规范可循，整批缺陷合理化 |
| "这是简单模块，不需要 DFT 规划" | 没有 DFT 的模块在量产测试中必成瓶颈；再简单也需要扫描链，早规划成本为零 |
| "安全需求不明确，先跳过安全架构" | 硬件 Root-of-Trust 不能事后追加；错过架构阶段则整个安全基础需要推倒重来 |
| "电源域可以先用单一统一域" | 单域设计无法支持低功耗模式；后期改造需要重新布局布线，是架构级返工 |
| "调研结果差不多，可以跳过 Phase 2" | 跳过竞品调研等于主动放弃对已有设计的学习；IC 领域重复发明轮子的代价是以季度计 |

---

# 降级策略

| 工具 / 资源缺失 | 降级方案 |
|---------------|---------|
| WebSearch / Agent 超时 | 使用本地 `knowledge/` 目录材料继续；在输出文档标注 "⚠️ 竞品调研受限" |
| drawio 文件无法解析 | 要求用户提供文字描述，或从 `.md` 重建架构意图 |
| it.spec-review 不可用 | 使用 Phase 12 内置评审维度表手动检查，结果写入 `.review/manual_review.md` |
| 知识库文件缺失（knowledge/） | 降级为模型领域知识；输出中标注 "⚠️ 未加载知识库：{文件名}" |
| 并行 Agent 配额不足 | 顺序执行 Phase 2 的三个 Agent，总时间增加但结果等价 |

---

# 典型工作流示例

详见 [workflow-examples.md](references/workflow-examples.md)

---

# 特别注意

- 每个 Phase 完成后清理上下文
- Mermaid 图表使用标准语法
- 信号命名遵循 Verilog/SystemVerilog 规范
- 寄存器地址对齐到 4 字节边界

---

## 最终验证实证（完成标准）

> 以下条件全部满足才可声明 bb-arch 完成，并移交 bb-spec-review（对抗性评审）。缺一不可。

- [ ] `spec_arch/` 中所有 Phase 产物文件均存在且非空
- [ ] `clock_reset_spec.md`：所有时钟域已定义频率 + CDC 同步策略
- [ ] `power_spec.md`：所有电源域边界已定义，含 isolation cell 声明
- [ ] 每个 IP block 文档有完整接口��号表（无 TBD 信号名）
- [ ] `dft_spec.md`：Scan coverage target ≥ 95% 已声明
- [ ] `design_notes.md`：包含全部开放问题和架构决策依据（ADR）
- [ ] it.spec-review 未报告 CRITICAL 级别问题（或已修复）

**禁止在上述条件未满足时触发 bb-spec-review handoff。**
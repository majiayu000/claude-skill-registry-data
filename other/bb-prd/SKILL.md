---
name: bb-prd
description: "生成芯片/IP 产品需求文档（PRD），从市场需求和技术约束输出专业 PRD 规范。Generate Product Requirements Document for chip/IP design projects. Trigger: /bb-prd, PRD生成, 产品需求文档, 芯片立项, IP需求, chiplet specification"
user-invocable: true
self-adaptive: true
self-evolving: true
version: "1.0.0"
arguments:
  - name: input_dir
    description: "包含市场需求文档或 idea 文件的目录路径（markdown 格式）"
    required: true
  - name: project_dir
    description: "项目目录路径，默认自动检测"
    required: false
  - name: scope
    description: "设计范围：chip（芯片级/Chiplet）或 ip（IP模块级）"
    required: false
    default: "chip"
  - name: auto_approve
    description: "跳过用户批准点，自动生成所有章节"
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
  - target: bb-arch
    condition: "PRD document completed and approved"
    session_note: "PRD 完成后可进入架构设计阶段，调用 bb-arch"
    transfer_files:
      - "{{OUTPUT_DIR}}/*.md"
evolution:
  enabled: true
  trigger: on_failure
  max_attempts: 3
  protected_zones:
    - frontmatter.name
    - frontmatter.description
    - HARD-GATE section
    - Self-Adaptive 初始化 section
  depth_policy:
    conservative: auto
    local: auto
    system: confirm
  data_sources:
    - execution_log
    - evolution_history
    - failed_paths
---

<DEFAULTS>
output_dir: ./prd
scope: chip
language: zh-CN
finetune: false
auto_approve: false
update: auto
</DEFAULTS>

# bb-prd — 芯片/IP 产品需求文档生成器

从市场需求和技术约束生成专业的 PRD（Product Requirements Document），为后续架构设计提供规范输入。

## Self-Adaptive 初始化

初始化目录结构 `.skills_local/bb-prd/`，收集项目上下文，解析路径。

---

## HARD-GATE 定义

```
<HARD-GATE>
在任何 PRD 生成操作前，必须完成以下步骤：

1. Self-Adaptive 初始化 + 项目上下文收集
   ```bash
   SCRIPT_DIR=~/.claude/scripts
   python3 "$SCRIPT_DIR/adaptive/adaptive_init.py" \
     --skill "bb-prd" \
     --project-dir "{{ PROJECT_DIR }}"
   ```
   成功标志：
   - `.skills_local/bb-prd/local.json` 存在
   - `.skills_local/bb-prd/project_context.json` 存在
   - `.skills_local/bb-prd/paths.json` 存在

2. 加载配置文件
   ```python
   import json
   
   with open(".skills_local/bb-prd/project_context.json") as f:
       CONTEXT = json.load(f)
   
   SCOPE = CONTEXT.get("config", {}).get("scope", "chip")
   INPUT_DIR = CONTEXT["resolved_paths"]["INPUT_DIR"]
   OUTPUT_DIR = CONTEXT["resolved_paths"]["OUTPUT_DIR"]
   ```

3. 创建执行日志目录
   ```bash
   mkdir -p "${LOG_DIR}"
   LOG_FILE="${LOG_DIR}/prd-$(date -u +%Y%m%dT%H%M%S).log"
   echo "[$(date -u +%Y%m%dT%H%M%SZ)] [INFO] HARD-GATE: 初始化完成" >> "${LOG_FILE}"
   ```

禁止行为（在完成初始化前）：
- 加载市场需求输入
- 启动 PRD 生成流程
- 输出规范文档
</HARD-GATE>
```

---

## Pipeline Position

```
市场需求/idea ──→ [bb-prd] ──→ prd/ ──→ bb-arch ──→ spec_arch/ ──→ bb-mas ──→ spec_mas/
                      OUTPUT_DIR
```

PRD 是芯片设计流程的第一个正式文档，定义产品目标、功能需求、性能指标、成本约束。

---

## 铁律（违反即停止）

> 以下规则不受 auto_approve 影响，任何模式下均不得绕过。

1. **输入先行铁律**：`INPUT_DIR` 无有效 `.md` 文件 → 拒绝执行，提示用户提供需求文档
2. **SMART 铁律**：需求含"大约/适当/较好/尽量"等模糊词 → 停止，要求澄清为可量化指标
3. **Margin 铁律**：Power/Area budget 未预留 ≥10% margin → 不输出 PRD（PVT corner + IR drop + aging 通常消耗 15%+）
4. **REQ ID 铁律**：需求 ID 重复或缺失 → 不进入 Phase 14 对抗评审
5. **追溯完整铁律**：每条 REQ 无后续文档追溯列 → 不声明 PRD 完成，追溯矩阵事后补必然漏项

---

## 设计范围分类

| Scope | 适用场景 | 文档重点 |
|-------|---------|---------|
| **chip** | Chiplet、SoC、ASIC、FPGA | 系统级需求、Chiplet组合、D2D互连 |
| **ip** | IP模块（CPU、Memory、Interconnect） | IP级功能、接口规范、集成要求 |

---

## Global Paths

```
PROJECT_DIR       = {{ project_dir 参数 或 auto-detect }}
INPUT_DIR         = {{ input_dir 参数 }}
OUTPUT_DIR        = {{ PROJECT_DIR }}/prd
TEMPLATE_DIR      = ~/.claude/skills/bb-prd/templates
REFERENCE_DIR     = ~/.claude/skills/bb-prd/references
SCRIPT_DIR        = ~/.claude/scripts
SKILL_FILE        = ~/.claude/skills/bb-prd/SKILL.md
LOG_DIR           = {{ OUTPUT_DIR }}/.logs
```

---

## 知识库引用

以下文件按需加载，用于特定章节生成：

| 文件 | 加载时机 | 用途 |
|------|----------|------|
| `references/ic-terminology.md` | 全流程 | IC 专业术语参考 |
| `references/chiplet-standards.md` | Phase 5 | UCIe、IEEE 1838 等标准 |
| `references/functional-safety.md` | Phase 9 | ISO 26262 功能安全 |
| `references/security-requirements.md` | Phase 10 | 安全需求模板 |

---

## 输入

- `INPUT_DIR/*.md`：市场需求文档、产品定义、技术备忘录
- 支持格式：
  - 市场分析报告（目标市场、竞争分析）
  - 技术可行性分析（性能目标、成本预算）
  - 初步 idea 描述（功能构想、应用场景）

---

## 输出目录结构

### scope=chip（芯片级）

```
prd/
├── PRD.md                    # 主 PRD 文档
├── market_analysis.md        # 市场分析附录（可选）
├── competitor_matrix.md      # 竞品对比矩阵（可选）
├── cost_model.md             # 成本模型（可选）
├── timeline.md               # 项目时间线
├── traceability_matrix.md    # 需求追溯矩阵
└── .logs/                    # 执行日志
```

### scope=ip（IP模块级）

```
prd/
├── IP_PRD.md                 # IP 级 PRD 文档
├── interface_requirements.md # 接口需求详解
├── integration_spec.md       # 集成规范
├── verification_requirements.md # 验证需求
└── .logs/                    # 执行日志
```

---

# 执行流程

## 增量更新机制

每次成功完成后，将输入文件哈希写入 `<output_dir>/.archive/input_snapshot.json`。下次执行时在 Phase 0 之前自动比对。

### 输入快照格式

```json
{
  "snapshot_time": "<ISO8601+08:00>",
  "skill": "bb-prd",
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
    sha256sum 所有 input_dir/*.md 及 parsed_idea.json（若存在）
    与 snapshot 对比
    IF 哈希全部一致 → 输出 "输入未变更，跳过生成" 并退出
    IF 哈希有差异   → 按下表分类
```

### 变更分类

| 条件（满足任意一条） | 分类 |
|---------------------|------|
| `design_name` 变更 | **MAJOR** |
| `protocols[]` 增删或重命名 | **MAJOR** |
| `target_pdk` 变更 | **MAJOR** |
| `target_freq_mhz` 变化 > 20% | **MAJOR** |
| `scope` 变更（chip ↔ ip） | **MAJOR** |
| 输入总字符数变化 > 30% | **MAJOR** |
| 其他所有变更（描述文字、预算调整等） | **MINOR** |

### MAJOR 路径：归档 + 全量重建

```bash
TIMESTAMP=$(date -u +%Y%m%dT%H%M%S)
ARCHIVE="{{ OUTPUT_DIR }}/.archive/$TIMESTAMP"
mkdir -p "$ARCHIVE"
# 移入归档（mv，可恢复）
for f in "{{ OUTPUT_DIR }}"/*.md "{{ OUTPUT_DIR }}"/*.json; do
  [ -f "$f" ] && mv "$f" "$ARCHIVE/"
done
echo "{\"reason\":\"MAJOR\",\"timestamp\":\"$TIMESTAMP\"}" > "$ARCHIVE/CHANGE_REASON.json"
```

归档完成后执行 FULL RUN（从 Phase 0 正常继续）。

### MINOR 路径：就地更新

根据变更字段决定重跑的最早 Phase：

| 变更内容 | 从此 Phase 重跑 |
|---------|----------------|
| 核心技术指标（freq、协议、面积/功耗预算） | Phase 3（Executive Summary）起 |
| 描述/上下文文字修改 | Phase 3（Executive Summary）起 |
| 安全/合规要求变更 | Phase 9 起 |
| 里程碑/时间表变更 | Phase 11 起 |

未受影响的 Phase 输出保持不变。完成后更新 `{{ OUTPUT_DIR }}/.archive/input_snapshot.json`。

---

## Phase 0: 输入解析

1. 读取 `INPUT_DIR` 目录内容
2. 解析 `.md` 文件提取关键需求
3. 分类输入内容：
   - 市场需求（目标市场、用户场景）
   - 技术需求（性能、功耗、成本）
   - 约束条件（时间、预算、技术栈）

输出产物：`parsed_requirements.json`（暂存上下文）

## Phase 1: 需求澄清

**auto_approve 模式**：基于文档推断需求，不使用 AskUserQuestion。

**澄清重点**：
- 产品定位（HPC/AI/汽车/网络/消费）
- 目标性能指标（吞吐量、延迟、功耗）
- 技术节点选择（28nm/40nm/65nm/FPGA）
- 成本预算范围
- 时间约束（里程碑时间点）
- 安全等级需求（是否需要功能安全）

**输出产物**：
```yaml
clarified_requirements:
  product_positioning: [...]
  performance_targets: [...]
  technology_node: [...]
  cost_budget: [...]
  timeline_constraints: [...]
  safety_level: [...]
  open_questions: [...]
```

## Phase 2: 市场与竞品调研

并行启动多个 Agents：

### Agent 配置

```yaml
Agent_1:
  name: "Market-Search"
  subagent_type: "Explore"
  prompt: |
    Search for market data and industry trends:
    - Query: "{{芯片类型}} market size {{年份}}"
    - Query: "{{应用场景}} semiconductor demand forecast"
    
    Report:
    1. Market size and growth rate
    2. Key players and market share
    3. Emerging trends
    
    Thoroughness: medium

Agent_2:
  name: "Competitor-Analysis"
  subagent_type: "general-purpose"
  prompt: |
    Search for competing products:
    - "{{芯片类型}} competing products"
    - "{{目标市场}} alternative solutions"
    
    Summarize:
    1. Feature comparison matrix
    2. Performance benchmarks
    3. Price points

Agent_3:
  name: "Tech-Trends"
  subagent_type: "docs-lookup"
  prompt: |
    Fetch documentation for:
    - Latest chiplet standards (UCIe 2.0/3.0)
    - Packaging technologies (CoWoS, EMIB, Foveros)
    - Memory technologies (HBM3e, DDR5)
    
    Return: key specifications, trends
```

整合调研结果到 `${OUTPUT_DIR}/market_analysis.md`（可选）。

## Phase 3: Executive Summary 生成

根据 scope 选择模板：

**scope=chip**：
1. 使用 `templates/chip_prd_template.md`
2. 填写产品定位、目标市场、关键差异化

**scope=ip**：
1. 使用 `templates/ip_prd_template.md`
2. 填写 IP 功能定位、目标应用

**输出产物**：`PRD.md` §1 Executive Summary

## Phase 4: Use Cases & User Stories

**设计内容**：
1. 定义主要用例（UC-01 ~ UC-N）
2. 每个用例关联目标工作负载
3. 定义定量 KPI

**格式**：
```markdown
| UC ID | Use Case | Target Workload | KPI |
|-------|----------|-----------------|-----|
| UC-01 | {{场景}} | {{benchmark}} | {{定量目标}} |
```

**输出产物**：`PRD.md` §2

## Phase 5: Functional Requirements

根据 scope 分章节：

### scope=chip 章节

1. **Compute Requirements** (REQ-COMPUTE-xxx)
   - FP16/INT8 吞吐量
   - 核心数量、频率
   
2. **Memory Requirements** (REQ-MEM-xxx)
   - HBM 容量、带宽
   - Cache 规格
   
3. **Connectivity Requirements** (REQ-IO-xxx)
   - PCIe、CXL、Ethernet 规格
   - D2D 互连带宽（UCIe）

### scope=ip 章节

1. **Function Requirements** (REQ-FUNC-xxx)
   - IP 核心功能定义
   - 操作模式
   
2. **Interface Requirements** (REQ-INTF-xxx)
   - 信号列表、协议（AXI/APB）
   - 时序规格

**输出产物**：`PRD.md` §3

## Phase 6: Non-Functional Requirements

**设计内容**：

1. **Performance** (REQ-PERF-xxx)
   - 最大频率、延迟
   
2. **Power & Thermal** (REQ-PWR-xxx, REQ-THERM-xxx)
   - TDP、空闲功耗
   - 温度范围、冷却方式
   
3. **Cost & Area** (REQ-COST-xxx, REQ-AREA-xxx)
   - BOM 成本预算
   - Die 面积约束
   
4. **Reliability** (REQ-REL-xxx)
   - MTTF、软错误率
   - ESD 规格

**输出产物**：`PRD.md` §4

## Phase 7: Chiplet/IP 组成定义（仅 scope=chip）

**加载知识库**：`references/chiplet-standards.md`

**设计内容**：
1. Die Inventory（计算Die、I/O Die、Memory Die）
2. Process Node 分配
3. D2D Interconnect Requirements（UCIe 规格）
4. Package Requirements（封装类型、bump pitch）

**输出产物**：`PRD.md` §5-7

## Phase 8: 软件与生态需求

**设计内容**：
1. ISA 定义（x86/ARM/RISC-V）
2. OS 支持（Linux/Windows/ESXi）
3. Framework 支持（PyTorch/TensorFlow）
4. Driver stack 要求

**输出产物**：`PRD.md` §10

## Phase 9: 功能安全需求（可选）

当需求包含汽车/工业安全等级时启用。

**加载知识库**：`references/functional-safety.md`

**设计内容**：
1. ASIL 等级定义（ISO 26262）
2. Safety mechanisms（lockstep、ECC、DMR）
3. SPFM/LFM/PMHF 目标

**输出产物**：`PRD.md` §11

## Phase 10: 安全需求（可选）

当需求包含安全场景时启用。

**加载知识库**：`references/security-requirements.md`

**设计内容**：
1. Root-of-Trust 位置
2. Secure Boot 流程
3. Side-channel 防护等级
4. Supply-chain 威胁模型

**输出产物**：`PRD.md` §12

## Phase 11: 标准合规与里程碑

**设计内容**：
1. Standards Compliance Summary（UCIe、IEEE、JEDEC）
2. Milestones 定义（PRR、Arch Sign-off、RTL Freeze、Tape-out）
3. Timeline 制定

**输出产物**：`PRD.md` §13-14

## Phase 12: Quality Checklist 验证

自动检查 PRD 质量：

```markdown
- [ ] 所有 REQ-xxx 有唯一 ID
- [ ] 每条需求符合 SMART
- [ ] 性能指标有 min/typ/max
- [ ] Chiplet/IP 需求分层清晰
- [ ] UCIe 合规等级明确
- [ ] Power budget ≤ TDP（含 ≥10% margin）
- [ ] Area budget ≤ target
- [ ] Variability 已标注（corner/temp/voltage）
```

**输出产物**：`PRD.md` §16

## Phase 13: Traceability Matrix 生成

生成需求追溯矩阵（RTM），关联 REQ ID 与后续文档：

```markdown
| REQ ID | ARCH Ref | MAS Ref | VPlan Ref |
|--------|----------|---------|-----------|
| REQ-COMPUTE-001 | §3.1 | M01-MAS | VP-COMP-01 |
```

**输出产物**：`traceability_matrix.md`

## Phase 14: 对抗性评审

**调用评审**：
```markdown
Skill(skill="it.spec-review", args="--spec-path {{ OUTPUT_DIR }} --output-dir {{ OUTPUT_DIR }}/.review")
```

**评审维度**：
- 需求完整性
- 指标合理性
- 约束一致性
- 标准合规性

---

# 设计原则

## PRD 特有原则

1. **SMART 需求**：每条需求必须 Specific/Measurable/Achievable/Relevant/Time-bound
2. **量化优先**：避免"约"、"大约"、"最好"等软指标
3. **分层需求**：系统级 vs 模块级需求清晰区分
4. **Margin 预留**：Power/Area budget 预留 ≥10% margin
5. **Variability 标注**：所有指标标注 corner/temperature/voltage

## Agent-aware 文档设计

1. REQ ID 唯一且易追溯（REQ-COMPUTE-001）
2. 表格优于文字（指标表、规格表）
3. Mermaid 图表代替手绘流程
4. 引用明确的文档路径（→ DOC-D2-01-ARCH）

---

## 常见借口（均无效）

| Agent 的借口 | 为什么错 |
|-------------|---------|
| "需求文档不完整，但可以先生成 PRD 框架" | PRD 空框架比没有更危险——下游 bb-arch 会基于错误假设展开，修正成本以人月计 |
| "这个产品定位很明显，不需要澄清" | IC 设计 Tape-out 返工成本百万级，澄清成本为零；明显的定位往往隐藏分歧 |
| "Margin 预留 5% 应该够用了" | PVT corner + IR drop + aging + 制造偏差通常吃掉 15%+；5% 在 silicon 验证时必然爆 |
| "追溯矩阵可以事后补" | 事后补的追溯矩阵几乎必然漏项，而漏项在 silicon debug 时才暴露，成本以周计 |
| "性能指标暂时用 TBD，后续再定" | TBD 指标会传播到 bb-arch 的 timing budget，导致整个设计基础不稳 |
| "竞品调研花时间，可以跳过" | 不看竞品等于主动重复已知错误；IC 领域竞品失败案例是最宝贵的免费学习资源 |

---

# 降级策略

| 工具 / 资源缺失 | 降级方案 |
|---------------|---------|
| WebSearch 不可用 | 使用 parallel_search CLI：`uv run parallel-search "{{query}}"` |
| parallel_search CLI 不可用 | 跳过 Phase 2 竞品调研，在 PRD 中标注 "⚠️ 竞品分析待补充" |
| it.spec-review 不可用 | 使用 Phase 12 内置 Quality Checklist 代替对抗评审，结果内联到 PRD §16 |
| 市场数据不完整 | 使用保守估计，在 PRD 明确标注数据来源和置信度等级（High/Medium/Low）|
| 安全等级未定义 | 根据应用场景推断（汽车→ASIL-D，工业→SIL-2，消费→无），标注 "⚠️ 推断值待确认" |

---

# 输出模板

详见 `templates/` 目录：
- `chip_prd_template.md` — Chiplet/SoC PRD 模板
- `ip_prd_template.md` — IP 模块 PRD 模板

---

# 参考文档

详见 `references/` 目录：
- `ic-terminology.md` — IC 专业术语
- `chiplet-standards.md` — Chiplet 相关标准
- `functional-safety.md` — 功能安全规范
- `security-requirements.md` — 安全需求模板

---

## 最终验证实证（完成标准）

> 以下条件全部满足才可声明 PRD 完成，并触发 bb-arch handoff。缺一不可。

- [ ] `prd/PRD.md` 存在且所有章节非空（无 "TODO" 占位）
- [ ] 所有 REQ-xxx 有唯一 ID，无重复，无缺号
- [ ] 所有性能指标有 min/typ/max 三值（无 TBD）
- [ ] Power/Area budget 均预留 ≥10% margin
- [ ] `traceability_matrix.md` 存在且覆盖全部 REQ（覆盖率 100%）
- [ ] Phase 12 Quality Checklist 全部通过（无 ❌）
- [ ] it.spec-review 未报告 CRITICAL 级别问题（或已修复并记录）

**禁止在上述条件未满足时声明 PRD 完成或触发 bb-arch。**

---

# Evolution Trigger Point

When any Phase fails:

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
---
name: bb-code-review
description: "对抗性代码评审：代码质量 / 可维护性 / 时序风险 / 综合友好度 / MAS 对齐度。默认 ruthless 模式，找 EVERY flaw。触发场景：(1) RTL lint 后；(2) 显式 /bb-code-review。"
user-invocable: true

---

# bb-code-review

## 职责

读 RTL + MAS，对照设计意图做对抗评审，分维度给出 issues + severity + pass 判定。

- 调用者：`bb-rtl-coder`、用户
- 前置：`bb-check-lint`（lint 通过后）
- 禁止使用：Task / Agent / Skill

## Input Args

| arg | type | required | 默认 | 说明 |
|-----|------|----------|------|------|
| rtl_dir | path | true | — | `designs/<name>/rtl/` |
| file_list | path | true | — | `file_list.f` |
| mas_path | path | true | — | `designs/<name>/mas/mas.json` |
| role | enum | false | `ruthless` | `ruthless` \| `linus` \| `balanced` |
| focus | string | false | `timing,maintainability` | 关注领域 |
| design_name | string | true | — | — |
| stamp | string | false | `<auto>` | — |

## Output Contract

| field | 值 |
|-------|----|
| `artifact_path` | `designs/<name>/rtl/code_review_<stamp>.md` |
| `issues_found` | int |
| `severity_summary` | `{critical,high,medium,low}` |
| `timing_risks` | list[str] |
| `maintainability_issues` | list[str] |
| `synthesis_friendly` | bool |
| `mas_alignment` | `full` \| `partial` \| `none` |
| `pass` | bool（critical==0 && high≤1） |
| `valid` | bool |

## 角色

| 角色 | 风格 | 适用 |
|------|------|------|
| `ruthless` | 无赞美只挑刺，找 EVERY flaw | **默认**，重大改动前压力测试 |
| `linus` | 直接尖锐，技术导向 | 风格/架构决策 |
| `balanced` | 承认优点+建议 | 常规评审 |

## 4-Phase 执行

### Phase 1 — build_review_prompt

`$PROJECT_SCRIPTS/build_prompt.py`：

```python
ROLE_PROMPTS = {
  "ruthless": "Ruthless reviewer. Find EVERY flaw. No compliments.",
  "linus":    "Linus Torvalds. Direct, no-nonsense, technically harsh.",
  "balanced": "Senior engineer. Constructive, acknowledge strengths.",
}

mas = json.load(open(mas_path))
rtl = {f: open(f).read() for f in cat(file_list)}
prompt = render_prompt(
    role=role,
    rtl=rtl,
    mas=mas,
    dimensions=["timing","maintainability","synthesis","mas_alignment"]
)
```

### Phase 2 — run_review

`claude --print "<prompt>" > <artifact_path>` 或 agent 内部生成。

### Phase 3 — parse_review

`$PROJECT_SCRIPTS/parse_review.py`：

- 提取 dimensions 段（`## Timing Risks` / `## Maintainability` 等）
- 计数 severity 标签 `[CRITICAL] / [HIGH] / [MEDIUM] / [LOW]`
- `pass = (critical == 0 && high <= 1)`

### Phase 4 — return

返回 JSON。`pass=false` → bb-rtl-coder 反馈重生成（≤3 iter）。

## 维度

| 维度 | 检查 |
|------|------|
| timing_risks | 长组合路径 / 无 pipeline / CDC 未处理 |
| maintainability | 深嵌套 / 大模块 / 命名 |
| synthesis_friendly | 非综合语法 / blackbox |
| mas_alignment | RTL ↔ MAS FSM/datapath 一致性 |
| **traceability** | REQ_ID 覆盖率 / 孤儿代码 / `@requirement` 注释完整性 |
| **spec_header** | Spec Header 完整性 / `@spec_hash` 一致性 / Key Constraints 覆盖 |
| **selective_inline** | 选择性内联合规（FSM/协议/datapath 必须标注，简单赋值不标注） |
| **register_map** | 寄存器定义 → 文档 + SVA 断言完整性 |
| **sdc_traceability** | SDC 约束 → REQ_ID 关联完整性 |

## Traceability 检查

### REQ_ID 覆盖率

扫描 RTL 文件中的 `@requirement` 注释，与 MAS §10 追踪矩阵对比：

```python
def check_traceability(rtl_files, mas_path):
    """检查 @requirement 注释覆盖率"""
    # 1. 从 MAS §10 提取声明的 REQ_ID 列表
    declared = extract_req_ids_from_mas(mas_path)

    # 2. 从 RTL 扫描 @requirement 注释中的 REQ_ID
    implemented = set()
    for f in rtl_files:
        for line in open(f):
            if "@requirement" in line:
                implemented |= extract_req_ids(line)

    # 3. 计算覆盖率
    coverage = len(declared & implemented) / len(declared) * 100
    missing = declared - implemented
    orphans = implemented - declared  # 实现了但 MAS 未声明

    return {
        "coverage_pct": coverage,
        "missing_reqs": sorted(missing),
        "orphan_reqs": sorted(orphans),
    }
```

### 孤儿检测

无 `@requirement` 注释的代码块（排除 `traceability/ignore.txt` 白名单）：

```bash
uv run $PROJECT_SCRIPTS/check_req_uniqueness.py
```

### SVA `@verifies` 覆盖率

检查 RTL 中的 SVA 断言是否都包含 `@verifies` 标注：

```python
def check_sva_verifies(rtl_files):
    """检查 SVA 断言的 @verifies 标注覆盖率"""
    sva_count = 0        # assert property 总数
    sva_with_verifies = 0  # 有 @verifies 的 assert property

    for f in rtl_files:
        lines = open(f).readlines()
        for i, line in enumerate(lines):
            if "assert property" in line or "assert(" in line:
                sva_count += 1
                # 检查前 3 行是否有 @verifies
                context = "".join(lines[max(0,i-3):i+1])
                if "@verifies" in context:
                    sva_with_verifies += 1

    coverage = (sva_with_verifies / sva_count * 100) if sva_count > 0 else 100
    return {
        "sva_total": sva_count,
        "sva_with_verifies": sva_with_verifies,
        "coverage_pct": coverage,
    }
```

### 输出格式

在评审报告中增加章节：

```markdown
## Traceability

- REQ_ID 覆盖率: 95% (19/20)
- SVA @verifies 覆盖率: 100% (15/15)
- 缺失 REQ_ID: REQ-M01-F05
- 孤儿代码: M99_Top.sv (无 @requirement)
- NEEDS_REVIEW: 无
```

### 通过标准追加

| 标准 | 要求 |
|------|------|
| traceability 覆盖率 | ≥ 90% |
| SVA @verifies 覆盖率 | == 100% |
| 孤儿 REQ_ID | == 0 |
| Spec Header 完整性 | == 100%（每个模块必须有 Spec Header） |
| @spec_hash 一致性 | == 100%（所有 Spec Hash 必须与 spec 文件匹配） |
| 寄存器文档生成 | == 100%（每个有寄存器的模块必须有 regmap 文档） |
| SDC traceability | ≥ 90%（SDC 约束必须有 @requirement 标注） |

## Spec Header 检查

### 完整性检查

每个 RTL 文件头部必须包含 Spec Header，包含以下字段：

```python
def check_spec_header(rtl_files):
    """检查 Spec Header 完整性"""
    required_fields = [
        "Module:", "Source:", "Version:", "Status:",
        "Spec Hash:", "REQ Coverage:", "Purpose:",
        "Key Constraints:", "Dependencies:", "Traceability:"
    ]

    results = []
    for f in rtl_files:
        content = open(f).read()

        # 检查是否包含所有必需字段
        missing = [field for field in required_fields if field not in content]

        if missing:
            results.append({
                "file": f,
                "status": "FAIL",
                "missing_fields": missing
            })
        else:
            results.append({
                "file": f,
                "status": "PASS"
            })

    return results
```

### @spec_hash 一致性检查

```python
def check_spec_hash_consistency(rtl_files):
    """验证 RTL 中的 @spec_hash 与 spec 文件是否一致"""
    import subprocess, re

    results = []
    for f in rtl_files:
        content = open(f).read()

        # 提取 Source 和 Spec Hash
        source_match = re.search(r'// Source:\s*(\S+)', content)
        hash_match = re.search(r'// Spec Hash:\s*(sha256:[a-f0-9]+)', content)

        if not source_match or not hash_match:
            continue  # 无 Spec Header，跳过

        spec_file = source_match.group(1)
        rtl_hash = hash_match.group(1)

        # 计算 spec 文件实际 hash
        result = subprocess.run(
            ["uv", "run", "$PROJECT_SCRIPTS/compute_spec_hash.py", spec_file],
            capture_output=True, text=True
        )
        actual_hash = result.stdout.strip()

        if rtl_hash != actual_hash:
            results.append({
                "file": f,
                "status": "FAIL",
                "rtl_hash": rtl_hash,
                "spec_hash": actual_hash,
                "fix": f"uv run $PROJECT_SCRIPTS/compute_spec_hash.py {spec_file} --inject {f}"
            })
        else:
            results.append({
                "file": f,
                "status": "PASS"
            })

    return results
```

### 输出格式

在评审报告中增加章节：

```markdown
## Spec Header

- 完整性: 100% (8/8 模块)
- @spec_hash 一致性: 87.5% (7/8)
- 不一致文件:
  - M01_DataflowController.sv: RTL=sha256:abc123, spec=sha256:def456
    Fix: `uv run $PROJECT_SCRIPTS/compute_spec_hash.py spec/MAS/M01/MAS.md --inject rtl/M01.sv`
```

## 选择性内联检查

### 合规检查

验证 RTL 文件遵循选择性内联标准：

```python
def check_selective_inline(rtl_files):
    """检查选择性内联合规性"""

    # 必须标注的代码块类型
    must_annotate = [
        r'always_ff.*case\s*\(',  # FSM
        r'valid\s*\|->',          # 协议握手 (SVA)
        r'always_ff.*posedge.*\b(stage|pipe)',  # pipeline stages
    ]

    # 不应标注的代码块类型
    should_not_annotate = [
        r'^\s*assign\s+\w+\s*=',  # 简单 assign
        r'^\s*parameter\s+',      # 参数定义
        r'^\s*localparam\s+',     # 本地参数
    ]

    results = []
    for f in rtl_files:
        lines = open(f).readlines()

        for i, line in enumerate(lines):
            # 检查必须标注的代码块是否有 @requirement
            for pattern in must_annotate:
                if re.search(pattern, line):
                    # 检查前 3 行是否有 @requirement
                    context = "".join(lines[max(0,i-3):i+1])
                    if "@requirement" not in context and "@verifies" not in context:
                        results.append({
                            "file": f,
                            "line": i+1,
                            "status": "MISSING",
                            "type": "must_annotate",
                            "code": line.strip()
                        })

    return results
```

## 寄存器 Traceability 检查

### 检查项

```python
def check_register_traceability(design_name):
    """检查寄存器定义 → 文档 → SVA 断言完整性"""

    mas_path = f"spec/MAS/{design_name}/MAS.md"
    regmap_doc = f"doc/regmap/{design_name}.md"
    regmap_sva = f"rtl/designs/{design_name}/rtl_src/{design_name}_regmap_assertions.sv"

    # 1. 检查 MAS 中是否有寄存器定义
    mas_content = open(mas_path).read()
    has_reg_def = "## 5. 寄存器映射" in mas_content or "## 6. 寄存器定义" in mas_content

    if not has_reg_def:
        return {"status": "SKIP", "reason": "No register definition in MAS"}

    # 2. 检查是否生成了寄存器文档
    has_doc = os.path.exists(regmap_doc)

    # 3. 检查是否生成了寄存器断言
    has_sva = os.path.exists(regmap_sva)

    # 4. 检查断言中的 @verifies 覆盖率
    if has_sva:
        sva_content = open(regmap_sva).read()
        assert_count = sva_content.count("assert property")
        verifies_count = sva_content.count("@verifies")
        verifies_coverage = (verifies_count / assert_count * 100) if assert_count > 0 else 100
    else:
        verifies_coverage = 0

    return {
        "status": "PASS" if (has_doc and has_sva and verifies_coverage == 100) else "FAIL",
        "has_reg_def": has_reg_def,
        "has_doc": has_doc,
        "has_sva": has_sva,
        "verifies_coverage": verifies_coverage
    }
```

## SDC Traceability 检查

### 检查项

```python
def check_sdc_traceability(design_name):
    """检查 SDC 约束 → REQ_ID 关联完整性"""

    sdc_path = f"designs/{design_name}/constraints/{design_name}.sdc"

    if not os.path.exists(sdc_path):
        return {"status": "SKIP", "reason": "No SDC file"}

    sdc_content = open(sdc_path).read()
    lines = sdc_content.splitlines()

    # 统计 SDC 命令数量
    sdc_commands = [
        "create_clock", "set_input_delay", "set_output_delay",
        "set_false_path", "set_multicycle_path", "set_clock_groups"
    ]

    total_commands = 0
    annotated_commands = 0

    for i, line in enumerate(lines):
        for cmd in sdc_commands:
            if cmd in line:
                total_commands += 1
                # 检查前 5 行是否有 @requirement
                context = "\n".join(lines[max(0,i-5):i+1])
                if "@requirement" in context:
                    annotated_commands += 1

    coverage = (annotated_commands / total_commands * 100) if total_commands > 0 else 100

    return {
        "status": "PASS" if coverage >= 90 else "FAIL",
        "total_commands": total_commands,
        "annotated_commands": annotated_commands,
        "coverage_pct": coverage
    }
```

### 输出格式

```markdown
## SDC Traceability

- SDC 命令总数: 12
- 已标注 @requirement: 11
- 覆盖率: 91.7%
- 未标注:
  - Line 45: set_false_path -from [get_pins ...]
```

## 通过标准

| 级别 | 通过 |
|------|------|
| critical | == 0 |
| high | ≤ 1 |

## 收敛 / 失败

| 状态 | 行动 |
|------|------|
| pass=true | 写 rtl_artifact.json + 进下一阶段 |
| pass=false & iter<3 | 反馈 bb-rtl-coder 重生成 |
| iter≥3 | 开 `arch-needs-fix` |

## Global Paths

```
PROJECT_SCRIPTS   = {{ PROJECT_DIR }}/scripts
```

## 资源索引

- `$PROJECT_SCRIPTS/build_prompt.py`、`$PROJECT_SCRIPTS/run_review.py`、`$PROJECT_SCRIPTS/parse_review.py`
- `references/rtl_review_dimensions.md`
- `references/role_personas.md` — 三角色详细提示词

**项目级 Coding Style 参考**：
- `wiki/codingstyle/systemverilog_styleguide.md` — SystemVerilog Style Guide (systemverilog.io)
- `wiki/codingstyle/freescale_verilog_standard.md` — Freescale Verilog HDL Coding Standard SRS V3.2
---
name: bb-invoke-yosys
description: "调用 Yosys 0.35 对 RTL 进行逻辑综合并技术映射到 ASAP7 标准单元，产出门级网表 + QoR 报告。支持并行综合（基于空闲CPU数量）。Workflow: (1)生成综合脚本;(2)并行执行综合;(3)LLM检查结果并迭代优化。触发场景：(1) bba-guru-synthesis 已完成 SDC 与 CDC 检查、需要生成 netlist；(2) PD 反馈 area/path 超标需要重综合；(3) 显式 /bb-invoke-yosys。"
user-invocable: true

---

# bb-invoke-yosys

## 职责

把 RTL 综合 → 技术映射 → ASAP7 标准单元网表，并产出供下游（OpenSTA、PD）使用的 QoR JSON。

**核心 Workflow（LLM驱动）**:
1. **生成综合脚本**: 调用 `generate_synthesis_config.py` + `render_yosys_tcl.py`
2. **并行执行综合**: 调用 `run_parallel_synthesis.py`（并行数=空闲CPU数）
3. **LLM检查迭代**: 分析 `synthesis_summary.json`，修复问题并重试

调用者：`bba-guru-synthesis`。
被调用方：Yosys 内置 `abc` 命令（独立 skill `bb-invoke-abc` 已 **DEPRECATED**，仅 `mapping_effort=high` 等高级调优时才链式调用）。
禁止使用：Task / Agent / Skill（本 skill 是叶子 skill，不递归调用其他 agent）。

## Input Args

| arg | type | required | 默认 | 说明 |
|-----|------|----------|------|------|
| file_list | path | true | — | `file_list.f`，每行一个 RTL 源文件路径 |
| sdc_path | path | true | — | `constraints/<name>.sdc`（yosys 仅做时序参考） |
| tech_lib | path | false | `libs/asap7/.../asap7sc7p5t.lib` | ASAP7 Liberty（脚本 `--tech-lib` 有默认值，可省略） |
| top_module | string | true | — | 顶层模块名 |
| design_name | string | true | — | 用于路径 `designs/<name>/synth_parallel/` |
| abc_options | string | false | `-g AND,OR,NAND,NOR,XOR` | ABC 优化参数 |
| mapping_effort | enum | false | `medium` | `low` / `medium` / `high` |
| enable_retiming | bool | false | `false` | 是否启用 retiming pass |
| mode | enum | false | `single` | `single`（单模块）/ `hierarchical`（分层多模块） |
| modules | path | false | — | JSON文件列出子模块（hierarchical模式） |

## Output Contract

写入 `designs/<name>/synth_parallel/`，返回 summary JSON：

| field | 值 |
|-------|----|
| `synthesis_summary.json` | 综合结果汇总 |
| `results[].artifact_path` | `designs/<name>/synth_parallel/<module>/netlist_<stamp>.v` |
| `results[].qor_path` | `designs/<name>/synth_parallel/<module>/qor_<stamp>.json` |
| `results[].valid` | bool（综合成功 true） |
| `results[].cell_count` | int |
| `results[].chip_area_um2` | float |
| `results[].wire_count` | int |
| `results[].error` | string\|null |
| `max_parallel` | int（并行执行数=空闲CPU数） |

## 5-Phase 执行（LLM驱动）

### Phase 1 — generate_config

调用 `scripts/generate_synthesis_config.py`，生成 `synthesis_config.json`：

```bash
python3 scripts/generate_synthesis_config.py \
    --file-list designs/<name>/rtl/file_list.f \
    --sdc designs/<name>/constraints/<name>.sdc \
    --top <top_module> \
    --design-name <name> \
    --tech-lib libs/asap7/.../asap7sc7p5t.lib \
    --out designs/<name>/synth_parallel/synthesis_config.json \
    --mode single|hierarchical
```

**LLM职责**: 根据MAS/RTL结构决定 `mode`，准备输入参数。

### Phase 2 — render_scripts

`run_parallel_synthesis.py` 内部调用 `scripts/render_yosys_tcl.py`，为每个模块生成TCL脚本：

1. `read_verilog -sv` 逐行展开 `file_list.f`
2. `hierarchy -check -top <top_module>` 检查顶层
3. `synth -top <top_module>` 通用综合
4. `dfflibmap -liberty <tech_lib>` DFF 映射
5. `abc -liberty <tech_lib> <abc_options>` 技术映射
6. 可选：`abc -liberty <tech_lib> -script +retime` （若 enable_retiming）
7. `opt_clean -purge`
8. `write_verilog -noattr <netlist>`
9. `stat -liberty <tech_lib>` 输出统计

**并行准备**: 所有模块的TCL脚本同时生成，不阻塞。

### Phase 3 — parallel_synthesis

调用 `scripts/run_parallel_synthesis.py`：

```bash
python3 scripts/run_parallel_synthesis.py \
    --config designs/<name>/synth_parallel/synthesis_config.json \
    --timeout 600
```

**并行执行**:
- 自动检测空闲CPU数量 (`get_idle_cpu_count()`)
- 使用 `ProcessPoolExecutor` 并行运行综合
- `max_workers = min(idle_cpus, module_count)`

每个模块执行:
1. `source ~/wrk/eda_opensources/eda_env.sh`
2. 校验 `yosys -V` 输出含 `Yosys 0.35`
3. 以 600s 超时执行 `yosys -c <tcl_path> > <log_path> 2>&1`
4. 把退出码追加到 log 末尾：`exit:<rc>`

### Phase 4 — parse_results

`run_parallel_synthesis.py` 内部调用 `scripts/parse_qor.py`，从 log 提取：

- `Chip area for module <top>: <float>` → `chip_area_um2`
- `Number of cells:           <int>` → `cell_count`
- `Number of wires:           <int>` → `wire_count`
- 任何 `ERROR:` / `Error:` 行 → `error`

生成 `synthesis_summary.json`：
```json
{
  "stamp": "20260519_120000",
  "total_elapsed": 45.3,
  "max_parallel": 4,
  "modules_total": 3,
  "modules_passed": 2,
  "modules_failed": 1,
  "results": [...]
}
```

### Phase 5 — llm_analysis_and_iteration

**LLM职责**: 
1. 读取 `synthesis_summary.json`
2. 分析失败模块（`valid=false`）
3. 根据错误类型决定修复策略：
   - `MULTIDRIVEN` / `latch inferred` → `rtl-needs-fix`
   - `WIDTHEXPAND` (≥5次) → `rtl-needs-fix`
   - `YOSYS_TIMEOUT` → 降低复杂度、增加 `opt -fast`
   - `VERSION_MISMATCH` → 修复EDA环境
4. 调整参数重试（最多6次）
5. 成功后返回给 `bba-guru-synthesis`

## 命令行用法

```bash
# Step 1: Generate config
python3 scripts/generate_synthesis_config.py \
    --file-list designs/uart16550/rtl/file_list.f \
    --sdc designs/uart16550/constraints/uart16550.sdc \
    --top uart16550 \
    --design-name uart16550 \
    --out designs/uart16550/synth_parallel/synthesis_config.json

# Step 2: Run parallel synthesis
python3 scripts/run_parallel_synthesis.py \
    --config designs/uart16550/synth_parallel/synthesis_config.json \
    --timeout 600

# Step 3: LLM analyzes synthesis_summary.json and iterates
```

## 并行执行策略

| 空闲CPU | 模块数 | max_parallel |
|---------|--------|--------------|
| 1 | N | 1（串行） |
| 4 | 3 | 3（全并行） |
| 4 | 10 | 4（分批并行） |
| 8 | 10 | 8（分批并行） |

检测方法：读取 `/proc/loadavg` 计算 `idle_cpus = total_cpus - load_avg`

## 收敛 / 失败

| 状态 | 处理 |
|------|------|
| `modules_failed == 0` | 调用 `bb-invoke-opensta` 做 STA |
| `modules_failed > 0`（RTL错误） | 返回错误，调整后重试 |
| Phase 3 timeout（600s） | 返回 `{valid:false, error:"YOSYS_TIMEOUT"}` |
| `VERSION_MISMATCH` | 返回 `{valid:false, error:"VERSION_MISMATCH"}` |

## 资源索引

- `scripts/generate_synthesis_config.py` — Phase 1（配置生成）
- `scripts/render_yosys_tcl.py` — Phase 2（TCL渲染）
- `scripts/run_parallel_synthesis.py` — Phase 3（并行执行）
- `scripts/run_yosys.py` — 单模块执行器
- `scripts/run_synthesis_first_run.py` — 首轮/无库通用综合执行器（被 `run_parallel_synthesis.py` 使用）
- `scripts/parse_qor.py` — Phase 4（QoR解析）
- `references/yosys_tcl_template.md` — TCL 模板
- `references/asap7_libs.md` — ASAP7 库位置
- `Gotcha/yosys_errors.md` — 常见错误与修复
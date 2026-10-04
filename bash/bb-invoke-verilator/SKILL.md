---
name: bb-invoke-verilator
description: "调用 Verilator 5.012 编译 RTL + TB 并跑 coverage-driven simulation，产出 sim log / coverage.dat / VCD。触发场景：(1) bba-guru-verification 完成 TB 后跑回归；(2) RTL 修复后回归验证；(3) 显式 /bb-invoke-verilator。"
user-invocable: true

---

# bb-invoke-verilator

## 职责

把 RTL（`file_list.f`）+ testbench（`tb/tb_top.sv`）编译为 verilator 可执行二进制并运行，产出 sim log、coverage 数据库、VCD 波形。

- 调用者：`bba-guru-verification`
- 下游消费者：`bb-collect-coverage`（读 `coverage.dat`）
- 禁止使用：Task / Agent / Skill

## Input Args

| arg | type | required | 默认 | 说明 |
|-----|------|----------|------|------|
| file_list | path | true | — | `file_list.f`，每行一个 RTL 源 |
| tb_top | path | true | — | `designs/<name>/tb/tb_top.sv` |
| design_name | string | true | — | 路径 `designs/<name>/sim_results/` |
| sim_time | string | false | `--time-resolution-unit 1ns` | 时间单位 |
| seed | int | false | `1` | `+rand_seed=<seed>` |
| enable_vcd | bool | false | `true` | 是否 `--trace --trace-structs` |
| stamp | string | false | `<auto YYYYMMDD-HHMMSS>` | 后缀 |

## Output Contract

写入 `designs/<name>/sim_results/`，返回：

| field | 值 |
|-------|----|
| `artifact_path` | `designs/<name>/sim_results/<stamp>.log` |
| `coverage_dat` | `designs/<name>/sim_results/coverage.dat` |
| `vcd_path` | `designs/<name>/sim_results/<stamp>.vcd` (与 .log 同级，fix H-09) |
| `obj_dir` | `designs/<name>/sim_results/obj_dir_<stamp>/` |
| `script_path` | `designs/<name>/sim_results/run_sim_<stamp>.sh` |
| `valid` | bool（编译+运行成功） |
| `assertions_pass` | bool（无 `%Error` / `Assertion failed`） |
| `sim_time_ns` | int（log 末尾 `$finish at`） |
| `error` | string\|null |

## 4-Phase 执行

### Phase 1 — render_sim_script

`scripts/render_verilator_sh.py` 渲染：

```bash
#!/bin/bash
set -euo pipefail
source ~/wrk/eda_opensources/eda_env.sh
verilator --version | grep -q "Verilator 5.012" \
  || { echo "VERSION_MISMATCH"; exit 1; }

verilator --binary --coverage <vcd_flag> \
  -f <file_list> <tb_top> \
  --top-module tb_top \
  -Mdir designs/<name>/sim_results/obj_dir_<stamp>/ \
  -o sim_<stamp> -CFLAGS "-O2" -j 4

./designs/<name>/sim_results/obj_dir_<stamp>/sim_<stamp> \
  +rand_seed=<seed> 2>&1 | tee designs/<name>/sim_results/<stamp>.log

verilator_coverage \
  designs/<name>/sim_results/obj_dir_<stamp>/coverage.dat \
  --write designs/<name>/sim_results/coverage.dat
```

`<vcd_flag>` = `--trace --trace-structs` 当 enable_vcd=true。

### Phase 2 — run_sim

`scripts/run_verilator.py`：`timeout 1800 bash <script_path>`，追加 `exit:<rc>`。

### Phase 3 — parse_sim_log

`scripts/parse_sim_log.py`：

- `$finish at <ns>` → `sim_time_ns`
- `%Error` / `Assertion failed` → `assertions_pass=false`
- `exit:<rc>` ≠ 0 → `valid=false`

写 `sim_summary_<stamp>.json`。

### Phase 4 — return

返回 JSON。下游 `bb-collect-coverage` 立即解析 `coverage.dat`。

## 收敛 / 失败

| 状态 | 处理 |
|------|------|
| `valid && assertions_pass` | 调 `bb-collect-coverage` |
| 断言失败 | 开 `rtl-needs-fix` |
| Phase 2 timeout（1800s） | `error="SIM_TIMEOUT"` |
| `VERSION_MISMATCH` | 修复 `eda_env.sh` |
| 编译失败 | 反馈 `%Error: <file>:<line>` |

## 资源索引

- `scripts/render_verilator_sh.py` — Phase 1
- `scripts/run_verilator.py` — Phase 2
- `scripts/parse_sim_log.py` — Phase 3
- `references/verilator_flags.md`
- `Gotcha/verilator_pitfalls.md`

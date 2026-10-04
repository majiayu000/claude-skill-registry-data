---
name: bb-invoke-opensta
description: "调用 OpenSTA 2.5.0 做静态时序分析（STA）。综合阶段验证 WNS/TNS；PD 阶段做 post-route signoff（多 PVT corner + SPEF）。触发场景：(1) bba-guru-synthesis 综合后查 timing；(2) bba-guru-pd 布线后跑 multi-corner signoff；(3) 显式 /bb-invoke-opensta。"
user-invocable: true

---

# bb-invoke-opensta

## 职责

调用 OpenSTA 做 STA：综合阶段 verify-WNS；PD 阶段 multi-PVT-corner timing signoff（含 SPEF 反标）。

- 调用者：`bba-guru-synthesis`、`bba-guru-pd`
- 禁止使用：Task / Agent / Skill

## Input Args

| arg | type | required | 默认 | 说明 |
|-----|------|----------|------|------|
| netlist | path | true | — | 综合后 `netlist.v` 或 PD 后 `routed.def` |
| sdc_path | path | true | — | `constraints/*.sdc` |
| tech_lib | path | true | — | ASAP7 Liberty（corner ↔ Liberty 一一对应） |
| top_module | string | true | — | 顶层名 |
| design_name | string | true | — | 路径 `designs/<name>/[synth\|pd]/` |
| spef | path | false | — | SPEF（PD 模式必须） |
| mode | enum | false | `synth` | `synth` \| `post_pd` |
| corners | list | false | synth: `["tt_0p77v_25c"]`；post_pd: `["ss_0p63v_m40c","tt_0p77v_25c","ff_0p88v_125c"]` | PVT 列表 |
| stamp | string | false | `<auto>` | |

## Output Contract

| field | 值 |
|-------|----|
| `artifact_path` | synth: `designs/<name>/synth/sta_<stamp>.json` / post_pd: `designs/<name>/pd/timing_signoff.json` |
| `tcl_path` | `.../sta_<stamp>.tcl` |
| `log_path` | `.../sta_<stamp>.log` |
| `wns_ns` | float（最差 corner） |
| `tns_ns` | float |
| `timing_met` | bool（所有 corner ≥ 0） |
| `corners` | `[{corner,wns_ns,tns_ns,timing_met}]` |
| `valid` | bool |
| `error` | string\|null |

## 4-Phase 执行

### Phase 1 — render_sta_tcl

`scripts/render_sta_tcl.py` 每个 corner 一段：

```tcl
# corner=<corner_name>
read_liberty <tech_lib_for_corner>
read_verilog <netlist>
link_design <top_module>
read_sdc <sdc_path>
# post_pd: read_spef <spef>
# set_operating_conditions -analysis_type on_chip_variation
report_checks -path_delay max -format full_clock_expanded -group_count 10
report_wns
report_tns
report_power
```

多 corner 合并到一个 TCL，corner 间用 `puts "=== CORNER <name> ==="`。

### Phase 2 — run_sta

`scripts/run_sta.py`：

1. `source ~/wrk/eda_opensources/eda_env.sh`
2. `sta -V` 含 `2.5.0` 否则 `VERSION_MISMATCH`
3. `timeout 900 sta -exit <tcl> > <log> 2>&1`
4. log 追加 `exit:<rc>`

### Phase 3 — parse_sta

`scripts/parse_sta.py` 按 `=== CORNER <X> ===` 分段：

- `worst slack <float>` → `corner.wns_ns`
- `tns <float>` → `corner.tns_ns`
- `timing_met` = (wns_ns ≥ 0)
- 全局 timing_met = AND(all corners)

写 `sta_<stamp>.json`（synth）或 `timing_signoff.json`（post_pd）。

### Phase 4 — return

返回 JSON。
- `bba-guru-synthesis`：`timing_met=false` → 调 SDC / 重综合
- `bba-guru-pd`：`timing_met=false` → 开 `synth-needs-fix` issue

## 收敛 / 失败

| 状态 | 处理 |
|------|------|
| `timing_met=true` | 进入下一阶段 |
| `wns < 0` (synth) | 调 abc options / 修 SDC，yosys 重综合 |
| `wns < 0` (post_pd) | 开 `synth-needs-fix` |
| `VERSION_MISMATCH` | 修 eda_env.sh |
| Phase 2 timeout（900s） | `error="STA_TIMEOUT"` |
| 网表 link 失败 | log: `Error: cannot link` |

## 资源索引

- `scripts/render_sta_tcl.py` — Phase 1
- `scripts/run_sta.py` — Phase 2
- `scripts/parse_sta.py` — Phase 3
- `references/asap7_corners.md` — corner ↔ Liberty 映射
- `references/sdc_cheatsheet.md` — 常用 SDC 语法
- `Gotcha/opensta_pitfalls.md` — corner / SPEF / virtual clock 陷阱

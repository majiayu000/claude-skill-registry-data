---
name: bb-invoke-magic
description: "调用 Magic 8.3.641 执行 PD 操作：floorplan / place / DRC / layout extraction。触发场景：(1) bba-guru-pd 做 floorplan 与 placement；(2) routing 后做 DRC；(3) LVS 前 extract SPICE；(4) 显式 /bb-invoke-magic。"
user-invocable: true

---

# bb-invoke-magic

## 职责

按 `action` 切换四种模式调 Magic：`floorplan` / `place` / `drc` / `extract`。

> **注（M-05 dedup）**：`action=floorplan` 在本 skill 中保留为底层入口；**bba-guru-pd 实际不直接调 floorplan**，而是先调 `bb-create-floorplan` 生成 TCL，再以 `action=place` 把 TCL 执行（floorplan TCL 被 `place_design` 流程 source）。`action=floorplan` 仅供 ad-hoc 调试场景使用。

- 调用者：`bba-guru-pd`
- 禁止使用：Task / Agent / Skill

## Input Args

| arg | type | required | 说明 |
|-----|------|----------|------|
| tech_file | path | true | ASAP7 Magic tech file（`.tech`） |
| layout_input | path | true | floorplan/place：`.tcl`；drc/extract：`.def`/`.mag` |
| action | enum | true | `floorplan` \| `place` \| `drc` \| `extract` |
| design_name | string | true | — |
| top_module | string | true | — |
| stamp | string | false | `<auto>` |

## Output Contract

| field | 值（按 action） |
|-------|----|
| `artifact_path` | drc→`designs/<name>/pd/drc_report.txt`；place→`pd/placed.def`；floorplan→`pd/floorplan.mag`；extract→`pd/extracted.spice` |
| `script_path` | `designs/<name>/pd/magic_<action>_<stamp>.tcl` |
| `log_path` | `designs/<name>/pd/magic_<action>_<stamp>.log` |
| `violations` | int（drc） |
| `violation_list` | `[{type,layer,coord}]`（drc） |
| `clean` | bool（drc：violations==0） |
| `valid` | bool |
| `error` | string\|null |

## 4-Phase 执行

### Phase 1 — render_magic_tcl

`scripts/render_magic_tcl.py` 按 action 生成 TCL：

```tcl
# action=drc
tech load <tech_file>
load designs/<name>/pd/routed.def
drc check
drc count
drc find
writeall force
quit
```

```tcl
# action=place
source <layout_input>
place_design
write_def designs/<name>/pd/placed.def
quit
```

```tcl
# action=extract
tech load <tech_file>
load designs/<name>/pd/<top>.mag
extract all
ext2spice -o designs/<name>/pd/extracted.spice
quit
```

### Phase 2 — run_magic

`scripts/run_magic.py`：

1. `source ~/wrk/eda_opensources/eda_env.sh`
2. `magic --version | grep "8.3"` 否则 `VERSION_MISMATCH`
3. `timeout 1800 magic -dnull -noconsole -T <tech_file> -rcfile /dev/null < <tcl> > <log> 2>&1`

### Phase 3 — parse_magic

- **drc**：正则 `DRC style.*?(\d+) error`，violation 列表 `(\w+) at (\d+),(\d+) layer (\w+)`
- **place**：检查 `placed.def` 存在 + size>0
- **floorplan**：log 无 `Error:`
- **extract**：`extracted.spice` 存在

写 `magic_<action>_<stamp>.json`。

### Phase 4 — return

按 action 返回对应字段。`bba-guru-pd`：
- drc.clean=false → optimization loop（调整 utilization）
- place.valid=false → 重 floorplan
- extract → 触发 `bb-invoke-netgen`

## 收敛 / 失败

| action | 通过 |
|--------|------|
| drc | violations == 0 |
| place | placed.def 存在 |
| floorplan | log 无 Error |
| extract | extracted.spice 存在 |

失败 ≤5 次重试；超出开 `synth-needs-fix`。

## 资源索引

- `scripts/render_magic_tcl.py`、`scripts/run_magic.py`、`scripts/parse_magic.py`
- `references/asap7_magic_tech.md`
- `Gotcha/magic_pitfalls.md`

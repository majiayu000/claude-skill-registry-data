---
name: bb-invoke-netgen
description: "调用 Netgen 1.5.275 做 LVS 对比：综合网表 vs Magic 提取的 SPICE，必须 match 才能 signoff。触发场景：(1) bba-guru-pd extract 后做 LVS；(2) 显式 /bb-invoke-netgen。"
user-invocable: true

---

# bb-invoke-netgen

## 职责

对比 schematic netlist（综合 `netlist.v`）与 layout netlist（Magic `extracted.spice`），输出 LVS 报告，必须 match。

- 调用者：`bba-guru-pd`
- 上游：`bb-invoke-magic`(action=extract)
- 禁止使用：Task / Agent / Skill

## Input Args

| arg | type | required | 说明 |
|-----|------|----------|------|
| schematic_netlist | path | true | `designs/<name>/synth/netlist.v` |
| layout_netlist | path | true | `designs/<name>/pd/extracted.spice` |
| tech_file | path | true | ASAP7 netgen setup file（`.tcl`） |
| top_module | string | true | — |
| design_name | string | true | — |
| stamp | string | false | `<auto YYYYMMDD-HHMMSS>` |

## Output Contract

| field | 值 |
|-------|----|
| `artifact_path` | `designs/<name>/pd/lvs_report.txt` |
| `log_path` | `designs/<name>/pd/netgen_<stamp>.log` |
| `match` | bool（"Circuits match uniquely"） |
| `discrepancies` | `[{kind, instance, schematic, layout}]` |
| `valid` | bool |
| `error` | string\|null |

## 4-Phase 执行

### Phase 1 — render_netgen_cmd

`scripts/render_netgen.py` 生成 batch 命令：

```bash
netgen -batch lvs \
  "designs/<name>/pd/extracted.spice <top>" \
  "designs/<name>/synth/netlist.v <top>" \
  <tech_file> \
  designs/<name>/pd/lvs_report.txt
```

### Phase 2 — run_netgen

`scripts/run_netgen.py`：

1. `source ~/wrk/eda_opensources/eda_env.sh`
2. `netgen -batch lvs --version 2>&1 | grep "1.5"` 否则 `VERSION_MISMATCH`
3. `timeout 600 netgen -batch lvs <args> > <log> 2>&1`
4. log 追加 `exit:<rc>`

### Phase 3 — parse_lvs

`scripts/parse_lvs.py` 扫描 `lvs_report.txt`：

- 末尾 `Circuits match uniquely.` → `match=true`
- `Circuits differ` → `match=false`，提取后续 `Net mismatch` / `Device mismatch` 段为 `discrepancies`

写 `lvs_<stamp>.json`。

### Phase 4 — return

返回 JSON。`bba-guru-pd`：
- match=true → 进入 `bb-invoke-opensta`(mode=post_pd)
- match=false → 黑盒/命名冲突，开 `synth-needs-fix`

## 收敛 / 失败

| 状态 | 行动 |
|------|------|
| match=true | 进 post-PD STA |
| match=false | 开 `synth-needs-fix` |
| `VERSION_MISMATCH` | 修 eda_env.sh |
| Phase 2 timeout（600s） | `error="LVS_TIMEOUT"` |

## 资源索引

- `scripts/render_netgen.py`、`scripts/run_netgen.py`、`scripts/parse_lvs.py`
- `references/asap7_netgen_setup.md` — setup file 与 device map
- `Gotcha/lvs_pitfalls.md` — 黑盒、port order、电源 net 命名

---
name: bb-invoke-klayout
description: "调用 KLayout 0.30.8 执行 GDSII 导出（stream out）、GDS-level DRC、或导出后 verify。PD 流程末尾产出最终 .gds（signoff 产物）。触发场景：(1) bba-guru-pd routed 后 GDS export；(2) GDS 层 DRC 检查；(3) 导出后 verify；(4) 显式 /bb-invoke-klayout。"
user-invocable: true

---

# bb-invoke-klayout

## 职责

按 `action` 切换三种模式调 KLayout：`gdsii_export`（DEF → GDS，别名 `export_gds`）、`drc`（GDS 层规则检查）、或 `verify`（导出后回读 + 单元完整性校验）。

- 调用者：`bba-guru-pd`
- 禁止使用：Task / Agent / Skill

## Input Args

| arg | type | required | 说明 |
|-----|------|----------|------|
| input_def | path | true | export/verify: `pd/routed.def` 或 `gdsii/<name>.gds`；drc: `pd/*.gds` |
| tech_file | path | true | ASAP7 KLayout tech file（`.lyt`） |
| action | enum | true | `gdsii_export` (== `export_gds` alias) \| `drc` \| `verify` |
| design_name | string | true | — |
| top_module | string | true | — |
| runset | path | false | DRC 模式 runset 路径（默认 ASAP7 内置） |
| stamp | string | false | `<auto YYYYMMDD-HHMMSS>` |

## Output Contract

| field | 值 |
|-------|----|
| `artifact_path` | export→`designs/<name>/gdsii/<name>.gds`；drc→`designs/<name>/pd/klayout_drc_<stamp>.lyrdb`；verify→`designs/<name>/gdsii/<name>_verify_<stamp>.json` |
| `script_path` | `designs/<name>/pd/klayout_<action>_<stamp>.lym` |
| `log_path` | `designs/<name>/pd/klayout_<action>_<stamp>.log` |
| `gds_size_bytes` | int（export 模式） |
| `violations` | int（drc 模式） |
| `verify_ok` | bool（verify 模式：cells_expected == cells_found 且无 open 错误） |
| `valid` | bool |
| `error` | string\|null |

## 4-Phase 执行

### Phase 1 — render_klayout_script

`scripts/render_klayout.py` 按 action 渲染 LYM/Ruby 脚本，承载：
- **gdsii_export / export_gds**: DEF→GDS stream out（`assets/export_gdsii.lym`）
- **drc**: 加载 runset（`assets/drc_runset.drc`）
- **verify**: 重新打开导出的 GDS，遍历 top cell hierarchy，统计 cells / nets，与 placed.def 期望值比对

### Phase 2 — run_klayout

`scripts/run_klayout.py`：

1. `source ~/wrk/eda_opensources/eda_env.sh`
2. `klayout -v 2>&1 | grep "0.30"` 否则 `VERSION_MISMATCH`
3. `timeout 1800 klayout -b -rd input=<def> -rd tech=<tech> -rd output=<gds> -r <script> > <log> 2>&1`
4. log 末尾追加 `exit:<rc>`

### Phase 3 — parse_klayout

`scripts/parse_klayout.py`：

- **gdsii_export / export_gds**：`.gds` 存在 + size>0 → `valid=true`，记 `gds_size_bytes`
- **drc**：解析 `.lyrdb` 中 `<item>` 数 → `violations`
- **verify**：log 中 `cells_found=<N>`、`opens=<M>` 等指标 → `verify_ok = (opens==0 && cells_found>=cells_expected)`

写 `klayout_<action>_<stamp>.json`。

### Phase 4 — return

返回 JSON。
- export `valid=true` → 触发 `verify` 二次校验后 PD signoff
- drc `violations==0` → 干净
- verify `verify_ok=true` → 最终签字

## 收敛 / 失败

| 状态 | 行动 |
|------|------|
| export valid=true | signoff |
| export valid=false | 上溯 Magic DRC 定位 |
| drc violations>0 | bba-guru-pd 开 `synth-needs-fix`（综合冲突）或重布线 |
| `VERSION_MISMATCH` | 修 eda_env.sh |
| Phase 2 timeout（1800s） | `error="KLAYOUT_TIMEOUT"` |

## 资源索引

- `scripts/render_klayout.py`、`scripts/run_klayout.py`、`scripts/parse_klayout.py`
- `assets/export_gdsii.lym` — DEF→GDS LYM 模板
- `assets/drc_runset.drc` — ASAP7 DRC runset 模板
- `references/asap7_klayout_tech.md`
- `Gotcha/klayout_pitfalls.md`

---
name: bb-invoke-qrouter
description: "调用 QRouter 1.4 对 placed DEF 执行 detail routing，产出 routed.def。触发场景：(1) bba-guru-pd 在 placement 完成后做布线；(2) 显式 /bb-invoke-qrouter。"
user-invocable: true

---

# bb-invoke-qrouter

## 职责

对 placed DEF + tech/cell LEF 跑详细布线，输出 routed DEF。布线失败需 bba-guru-pd 调整 floorplan utilization 后重试。

- 调用者：`bba-guru-pd`
- 上游：`bb-invoke-magic`(action=place)
- 下游：`bb-invoke-magic`(action=drc)
- 禁止使用：Task / Agent / Skill

## Input Args

| arg | type | required | 默认 | 说明 |
|-----|------|----------|------|------|
| placed_def | path | true | — | `designs/<name>/pd/placed.def` |
| tech_lef | path | true | — | ASAP7 tech LEF |
| cell_lef | path | true | — | ASAP7 standard cell LEF |
| design_name | string | true | — | — |
| strategy | enum | false | `default` | `default` \| `high_effort` |
| stamp | string | false | `<auto>` | — |

## Output Contract

| field | 值 |
|-------|----|
| `artifact_path` | `designs/<name>/pd/routed.def` |
| `cfg_path` | `designs/<name>/pd/qrouter_<stamp>.cfg` |
| `log_path` | `designs/<name>/pd/qrouter_<stamp>.log` |
| `failed_nets` | int |
| `valid` | bool |
| `error` | string\|null |

## 4-Phase 执行

### Phase 1 — render_qrouter_cfg

`scripts/render_qrouter_cfg.py` 渲染：

```
lef <tech_lef>
lef <cell_lef>
read <placed_def>
route
writeback
write <name>_routed.def designs/<name>/pd/routed.def
quit
```

`strategy=high_effort` 追加 `set rip_limit 50` 等积极参数。

### Phase 2 — run_qrouter

`scripts/run_qrouter.py`：

1. `source ~/wrk/eda_opensources/eda_env.sh`
2. `qrouter -v 2>&1 | grep "1.4"` 否则 `VERSION_MISMATCH`
3. `timeout 3600 qrouter -noclockdiff -c <cfg> > <log> 2>&1`
4. log 末尾追加 `exit:<rc>`

### Phase 3 — parse_qrouter

`scripts/parse_qrouter.py`：

- `routed.def` 存在 → `valid=true`
- log 含 `routing failed` / `Unable to route` → 计数 `failed_nets`

写 `qrouter_<stamp>.json`。

### Phase 4 — return

返回 JSON。`bba-guru-pd`：
- `failed_nets==0` → 调 `bb-invoke-magic`(action=drc)
- `failed_nets>0` → 增加 utilization margin（-0.05）重 floorplan，≤5 iter

## 收敛 / 失败

| 状态 | 行动 |
|------|------|
| failed_nets==0 | 进 DRC |
| failed_nets>0 | 调 floorplan 重试 |
| `VERSION_MISMATCH` | 修 eda_env.sh |
| Phase 2 timeout（3600s） | `error="ROUTE_TIMEOUT"`，提高 utilization |
| iter > 5 | retreat 到 `synth-needs-fix` |

## 资源索引

- `scripts/render_qrouter_cfg.py`、`scripts/run_qrouter.py`、`scripts/parse_qrouter.py`
- `references/asap7_lef.md` — tech/cell LEF 位置
- `Gotcha/qrouter_pitfalls.md` — congestion / pitch / via stack

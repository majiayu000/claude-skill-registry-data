---
name: bb-invoke-abc
deprecated: true
description: "**[DEPRECATED in v1.3 — common path uses bb-invoke-yosys' embedded ABC]** 独立调用 ABC（Berkeley Logic Synthesis）做逻辑优化，仅 `mapping_effort=high` 等高级调优场景使用。触发场景：(1) bb-invoke-yosys `chain_to_abc=true` 时；(2) 显式 /bb-invoke-abc 调试。"
user-invocable: true

---

# bb-invoke-abc (DEPRECATED in v1.3)

> 在 99% 路径上 `bb-invoke-yosys` 内嵌的 ABC 已足够。本 skill 仅保留为：
> - high-effort 二次优化（fix L-02 / M-06）
> - ABC script 单独调试场景

## 职责

读 Yosys 输出的 BLIF，跑自定义 ABC script 序列，输出优化后 BLIF。通常 `bb-invoke-yosys` 内嵌 ABC 已足够；本 skill 用于 high-effort 路径。

- 调用者：`bba-guru-synthesis`
- 关联：`bb-invoke-yosys`
- 禁止使用：Task / Agent / Skill

## Input Args

| arg | type | required | 默认 | 说明 |
|-----|------|----------|------|------|
| blif_input | path | true | — | Yosys 写出的 BLIF |
| tech_lib | path | true | — | ASAP7 Liberty |
| script | string | false | `"strash; iresyn; dc2; map -a"` | ABC 命令序列 |
| design_name | string | true | — | — |
| stamp | string | false | `<auto>` | — |

## Output Contract

| field | 值 |
|-------|----|
| `artifact_path` | `designs/<name>/synth/abc_<stamp>.blif` |
| `script_path` | `designs/<name>/synth/abc_<stamp>.script` |
| `log_path` | `designs/<name>/synth/abc_<stamp>.log` |
| `and_gates` | int |
| `levels` | int |
| `valid` | bool |
| `error` | string\|null |

## 4-Phase 执行

### Phase 1 — render_abc_script

`scripts/render_abc.py` 渲染：

```
read_blif <blif_input>
<script_commands>
map -a -B 0.33
write_blif designs/<name>/synth/abc_<stamp>.blif
print_stats
```

### Phase 2 — run_abc

`scripts/run_abc.py`：

1. `source ~/wrk/eda_opensources/eda_env.sh`
2. `timeout 600 abc -f <script> > <log> 2>&1`
3. log 追加 `exit:<rc>`

### Phase 3 — parse_abc

`scripts/parse_abc.py` 解析 `print_stats` 行 `nd = <int> ... lev = <int>` → `and_gates` / `levels`，log 含 `ERROR` → `valid=false`。

写 `abc_<stamp>.json`。

### Phase 4 — return

返回 JSON。`bba-guru-synthesis` 可将优化后 BLIF 反导入 Yosys `read_blif` 继续技术映射。

## 收敛 / 失败

| 状态 | 行动 |
|------|------|
| valid=true | 反导入 Yosys 或直接交付 |
| valid=false（log ERROR） | 退回默认 abc_options |
| Phase 2 timeout（600s） | `error="ABC_TIMEOUT"`，简化 script |

## 注

独立调用属于高级优化场景。普通流程使用 `bb-invoke-yosys` 即可。

## 资源索引

- `scripts/render_abc.py`、`scripts/run_abc.py`、`scripts/parse_abc.py`
- `references/abc_scripts.md` — 常用 ABC 命令组合（resyn2、dch、if 等）
- `Gotcha/abc_pitfalls.md` — map area vs delay 权衡

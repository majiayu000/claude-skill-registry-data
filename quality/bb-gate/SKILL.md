---
name: bb-gate
description: "统一质量门禁：RTL / 综合 / 测试 / PD 四阶段验收。调用共享 gate_runner.py 参数化。触发：(1) bba-guru-* 在阶段结束时调用；(2) 显式 /bb-gate <domain>。"
user-invocable: true
arguments:
  - name: domain
    type: enum<rtl,synth,pd,test>
    required: true
    description: "Quality gate 类型"
  - name: artifact
    type: path
    required: true
    description: "上游 artifact JSON 路径 (如 designs/<name>/rtl/rtl_artifact.json)"
  - name: design_name
    type: string
    required: true
    description: "Design slug"
  - name: output
    type: path
    required: false
    description: "输出 JSON 路径；默认 designs/<name>/<stage>/quality_gate_<stamp>.json"
---

# bb-gate

统一质量门禁，参数化的单一 skill（取代早期设想的 4 个独立 skill
`bb-gate-rtl-quality` / `bb-gate-synth-quality` / `bb-gate-test-quality` / `bb-gate-pd-quality`，
这些独立 skill 从未落地，调用方一律用 `bb-gate <domain>`）。
所有 domain 的判定字段名严格对齐 `.claude/schemas/*.schema.json`。

## 职责

综合判定指定阶段的 artifact 是否达标，**blocking**：
- `pass=true` → 下游可以继续
- `pass=false` → 上游 agent 必须修复后重试

禁止使用：Task / Agent / Skill（这是叶节点工具）。

## 4 个 domain 的判定标准

### domain=rtl

| 项 | 条件 |
|----|------|
| lint_clean | verible 0 error，无未 waive (`lint_clean == true`) |
| modules_nonempty | `modules[]` 长度 > 0 |
| file_list_valid | `file_list` 非空 |

### domain=test

| 项 | 条件 |
|----|------|
| functional_coverage_100 | `functional_coverage == 100` |
| line_coverage_100 | `code_coverage.line == 100` |
| branch_coverage_95 | `code_coverage.branch >= 95` |
| toggle_coverage_90 | `code_coverage.toggle >= 90` |

### domain=synth

| 项 | 条件 |
|----|------|
| timing_met | `wns_ns >= 0` **且**所有 `corners[].timing_met == true` |
| area_reasonable | `area_um2 > 0` |
| cells_exist | `cell_count > 0` |

### domain=pd

| 项 | 条件 |
|----|------|
| drc_clean | `drc_violations == 0` |
| lvs_clean | `lvs_match == true` |
| timing_met | 所有 `timing_corners[].timing_met == true` |

Signoff corner 列表见 [`references/asap7_corner_signoff_list.md`](references/asap7_corner_signoff_list.md)。

## 4-Phase 执行

### Phase 1 — Render

无需 render — gate_runner.py 直接消费 artifact JSON。

### Phase 2 — Run

```bash
uv run python .claude/skills/_gate_common/gate_runner.py \
    <domain> <artifact_path> [--output <output_path>]
```

Exit code: 0 = pass, 1 = fail, 2 = error.

### Phase 3 — Parse

JSON 输出结构：
```json
{
  "pass": bool,
  "gate_type": "rtl|synth|pd|test",
  "gate_name": "...",
  "timestamp": "ISO8601",
  "checks": { "<check>": {"pass": bool, "detail": "...?"} },
  "summary": "N/M checks passed"
}
```

### Phase 4 — Return

- `pass=true` → 写 `quality_gate_<stamp>.json` 到对应 stage 目录，agent 可以继续。
- `pass=false` → 不写文件；返回 details；上游 agent 修复后重试。

## Output Contract

| field | 值 |
|-------|----|
| `artifact_path` | `<output>` 路径 |
| `pass` | bool |
| `valid` | bool |
| `checks` | object |
| `summary` | string |

## 资源索引

- `.claude/skills/_gate_common/gate_runner.py` — 共享 runner（参数化所有 4 个 gate）
- `.claude/skills/_gate_common/render_gate_config.py` — 可选配置渲染
- `.claude/schemas/*.schema.json` — artifact schema（由 `validate-input-schema` hook 在边界校验）
- `references/asap7_corner_signoff_list.md` — PD signoff corners

## 项目级 Coding Style 参考

- `wiki/codingstyle/systemverilog_styleguide.md` — SystemVerilog Style Guide
- `wiki/codingstyle/freescale_verilog_standard.md` — Freescale Verilog HDL Standard

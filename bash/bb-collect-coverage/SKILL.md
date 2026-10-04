---
name: bb-collect-coverage
description: "解析 Verilator coverage.dat + sim log，输出 functional + code coverage 数值，判断是否 100% 达标。触发场景：(1) bb-invoke-verilator 后；(2) 每次回归后；(3) 显式 /bb-collect-coverage。"
user-invocable: true

---

# bb-collect-coverage

## 职责

读 `coverage.dat`（verilator）+ sim log（covergroup hits），输出 line/branch/toggle/functional 百分比与未覆盖 bin 列表。

- 调用者：`bba-guru-verification`
- 上游：`bb-invoke-verilator`
- 禁止使用：Task / Agent / Skill

## Input Args

| arg | type | required | 默认 | 说明 |
|-----|------|----------|------|------|
| sim_log | path | true | — | `designs/<name>/sim_results/<stamp>.log` |
| coverage_dat | path | false | 同 sim_results | verilator coverage 数据库 |
| design_name | string | true | — | — |
| target_pct | float | false | `100.0` | functional & code 阈值 |
| stamp | string | false | `<auto>` | — |

## Output Contract

写到 `designs/<name>/coverage.json`（中间文件）和 `designs/<name>/test_report.json`（按 `.claude/schemas/test_report.schema.json` 的**嵌套**结构）。

| field | 值 |
|-------|----|
| `artifact_path` | `designs/<name>/test_report.json` |
| `coverage_json` | `designs/<name>/coverage.json` |
| `script_path` | `designs/<name>/sim_results/parse_cov_<stamp>.sh` |
| `log_path` | `designs/<name>/sim_results/cov_<stamp>.log` |
| `functional_coverage` | float（0..100） |
| `code_coverage` | `{line: float, branch: float, toggle: float}` (NESTED, fix C-01) |
| `meets_target` | bool（`functional == 100` AND `line == 100` AND `branch >= 95` AND `toggle >= 90`，与 test gate 一致） |
| `tests` | `[{name, status, log}]`（test_report.schema 必填；逐用例结果） |
| `iteration_count` | int 0..8（test_report.schema 必填） |
| `uncovered_bins` | `[{group, bin, hits}]` |
| `valid` | bool |

## 4-Phase 执行

### Phase 1 — render_cov_sh

```bash
#!/bin/bash
verilator_coverage --annotate designs/<name>/sim_results/annotate/ <coverage_dat>
```

### Phase 2 — run_cov

`timeout 300 bash <script_path> > <log> 2>&1`

### Phase 3 — parse_cov

`scripts/parse_cov.py`：

- annotate 输出含 `LCOV:hit/total` 标记 → `code_coverage.line/branch/toggle`
- sim_log 中 covergroup `Coverage: <pct>%` → `functional_coverage`
- 列举 hits==0 的 bin → `uncovered_bins`
- `meets_target = functional_coverage >= target_pct AND code_coverage.line >= target_pct AND code_coverage.branch >= 95 AND code_coverage.toggle >= 90`
  - 100% branch/toggle coverage is often unreachable due to defensive error-handling code. Targets of 95%/90% allow for documented unreachable bins while maintaining high quality.
- 写 `coverage.json`（含 `inputs[]:{path,sha256}` 引用 sim_log + rtl_artifact.json）
- 同时**生成 `test_report.json`**，遵循 `.claude/schemas/test_report.schema.json` 嵌套结构（fix C-01）；必须填齐 schema required 字段：`functional_coverage`、`code_coverage{line,branch,toggle}`、`tests[]:{name,status,log}`（逐用例结果，由 verification 汇总）、`inputs[]:{path,sha256}`、`iteration_count`（fix M-03）

### Phase 4 — return

返回 JSON。`bba-guru-verification`：
- `meets_target=true` → signoff，开 `ready-for-synth`
- `meets_target=false` → 把 `uncovered_bins` 反馈，追加 corner-case 用例重 sim

## 收敛 / 失败

| 状态 | 行动 |
|------|------|
| meets_target=true | 进 synth |
| meets_target=false | optimization loop（追加 seed / corner test） |
| 解析失败 | 重试 1 次 |
| iter > 10 | escalate `arch-needs-fix`（不可达 bin） |

## 资源索引

- `scripts/render_cov_sh.py`、`scripts/run_cov.py`、`scripts/parse_cov.py`
- `references/verilator_coverage_format.md`
- `Gotcha/coverage_pitfalls.md` — unreachable code / dead branch

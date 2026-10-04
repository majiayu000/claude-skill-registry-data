---
name: bb-generate-tb
description: "根据 MAS + verification_plan + RTL 接口描述生成 SystemVerilog UVM 或 cocotb 测试平台与 test cases 清单。触发场景：(1) bba-guru-verification 在 plan 完成后；(2) 补充 corner case TB；(3) 显式 /bb-generate-tb。"
user-invocable: true

---

# bb-generate-tb

## 职责

读 MAS 接口表 + verification_plan FTP 列表 + rtl_artifact 模块清单，生成 TB 顶层 + base sequence + per-FTP sequence + covergroup，并跑 verilator lint-only 预检。

- 调用者：`bba-guru-verification`
- 上游：`bb-create-verif-plan`
- 下游：`bb-invoke-verilator`
- 禁止使用：Task / Agent / Skill

## Input Args

| arg | type | required | 默认 | 说明 |
|-----|------|----------|------|------|
| mas_path | path | true | — | `designs/<name>/mas/mas.json` |
| verif_plan | path | true | — | `designs/<name>/verif/verification_plan.md` |
| rtl_artifact | path | true | — | `designs/<name>/rtl/rtl_artifact.json` |
| design_name | string | true | — | — |
| tb_style | enum | false | `uvm` | `uvm` \| `cocotb` |
| stamp | string | false | `<auto>` | — |

## Output Contract

| field | 值 |
|-------|----|
| `artifact_path` | `designs/<name>/tb/` (目录) |
| `tb_top` | `designs/<name>/tb/tb_top.sv` |
| `tb_files` | list[path] |
| `test_cases` | int |
| `lint_clean` | bool（verilator --lint-only 通过） |
| `valid` | bool |
| `error` | string\|null |

## 产物结构

```
designs/<name>/
├── tb/
│   ├── tb_top.sv
│   ├── seq_base.sv
│   ├── seq_<FTP-id>.sv  (每 FTP 一个)
│   └── coverage.sv      (covergroups 与 plan 对齐)
└── verif/
    └── test_cases.md    (FTP → seq 映射)
```

## 4-Phase 执行

### Phase 1 — render_tb_py

`scripts/render_tb_py.py`：

```python
import json
mas_io = json.load(open(rtl_artifact))["interfaces"]
ftps = parse_ftps_from_md(verif_plan)
for ftp in ftps:
    write_sv_sequence(ftp, mas_io, tb_style, out_dir="designs/<name>/tb/")
write_tb_top(mas_io, ftps, tb_style)
write_coverage(ftps, verif_plan)
```

### Phase 2 — run_gen_tb

`timeout 300 uv run python <script_path> > <log> 2>&1`

### Phase 3 — lint_check

```bash
verilator --lint-only -sv -f designs/<name>/file_list.f designs/<name>/tb/tb_top.sv 2>&1
```

`scripts/parse_tb_lint.py`：

- `tb_files = ls designs/<name>/tb/*.sv`
- `test_cases = len(ftps)`
- `lint_clean = (verilator 退出 0 且无 %Error)`

### Phase 4 — return

返回 JSON。`bba-guru-verification` 据此触发 `bb-invoke-verilator`。

## 收敛 / 失败

| 状态 | 行动 |
|------|------|
| valid=true | 进 verilator 跑 sim |
| lint_clean=false | 重生成 1 次 |
| 重生成仍失败 | `error="TB lint persistent"`；人工介入 |

## 资源索引

- `scripts/render_tb_py.py`、`scripts/run_gen_tb.py`、`scripts/parse_tb_lint.py`
- `assets/tb_top.sv.tmpl`、`assets/seq.sv.tmpl`、`assets/coverage.sv.tmpl`
- `references/uvm_quickref.md`、`references/cocotb_quickref.md`
- `Gotcha/sv_uvm_pitfalls.md`

**项目级 Coding Style 参考**：
- `wiki/codingstyle/systemverilog_styleguide.md` — SystemVerilog Style Guide (systemverilog.io)
- `wiki/codingstyle/freescale_verilog_standard.md` — Freescale Verilog HDL Coding Standard SRS V3.2

---
name: bb-parse-ast
description: "解析 SystemVerilog RTL 为 AST JSON，供 CDC 检查 / signal path tracing / module dep 分析。统一 4 个后端 (babel-lsp / pyverilog / verible / slang)，auto 模式自动降级。触发场景：(1) bba-guru-synthesis CDC 前；(2) bb-trace-signal-path / bb-find-module-deps 之前；(3) 显式 /bb-parse-ast。"
user-invocable: true
arguments:
  - name: file_list
    type: path
    required: true
    description: "file_list.f"
  - name: design_name
    type: string
    required: true
  - name: backend
    type: enum<auto,babel-lsp,pyverilog,verible,slang>
    required: false
    default: auto
    description: "auto = babel-lsp → pyverilog → verible → slang 自动降级"
  - name: output_format
    type: enum<json,pickle>
    required: false
    default: json
  - name: stamp
    type: string
    required: false
    description: "默认 <auto YYYYMMDD-HHMMSS>"
---

# bb-parse-ast

解析 RTL 为 AST JSON。统一 4 个后端，对下游透明。

## 职责

- 调用者：`bba-guru-synthesis`、`bb-check-cdc`、`bb-trace-signal-path`、`bb-find-module-deps`
- 输出 schema 对所有 backend 一致（下游无需感知差异）
- 禁止使用：Task / Agent / Skill

## Backend 选择（2026-07-21 新增 babel-lsp）

| backend | 触发条件 | 实现 |
|---------|---------|------|
| `auto` | 默认 | 按 `babel-lsp → pyverilog → verible → slang` 顺序尝试 |
| `babel-lsp` | 显式指定或 auto 首选 | Babel-LSP sv-analyzer，基于 slang 引擎（IEEE 1800-2023） |
| `pyverilog` | 显式指定 | 纯 Python，覆盖 SystemVerilog 2012 子集 |
| `verible` | 显式指定或 pyverilog 失败 | `verible-verilog-syntax`，覆盖 SV 2017 |
| `slang` | 显式指定或前两者都失败 | `slang`，覆盖 SV 2017 + UVM |

## Input Args

| arg | type | required | 默认 | 说明 |
|-----|------|----------|------|------|
| file_list | path | true | — | `file_list.f` |
| design_name | string | true | — | — |
| backend | enum | false | `auto` | `auto\|babel-lsp\|pyverilog\|verible\|slang` |
| output_format | enum | false | `json` | `json\|pickle` |
| stamp | string | false | `<auto>` | — |

## Output Contract

| field | 值 |
|-------|----|
| `artifact_path` | `designs/<name>/ast/ast_<stamp>.json` |
| `script_path` | `designs/<name>/ast/parse_ast_<stamp>.{py\|sh}` |
| `backend_used` | `pyverilog\|verible\|slang` |
| `valid` | bool |
| `error` | string (e.g. `UNSUPPORTED_SV_SYNTAX`) |

## 4-Phase 执行

### Phase 1 — Render

- backend=pyverilog → `scripts/render_parser_py.py`
- backend=verible → `scripts/render_fallback_sh.py`（参数 `--backend verible`）
- backend=slang → `scripts/render_fallback_sh.py`（参数 `--backend slang`）
- backend=auto → 内部 try/except 链，先 pyverilog 再 verible 再 slang

### Phase 2 — Run

`timeout 600 uv run python <script_path>` 或 `bash <script_path>`（verible/slang 是 shell）。

### Phase 3 — Parse

- `scripts/parse_ast_output.py`（pyverilog 输出归一化）
- `scripts/parse_fallback_output.py` + `scripts/normalize_{verible,slang}.py`（verible/slang 输出归一化）

归一化输出 schema 对所有 backend 一致，下游可直接消费。

### Phase 4 — Return

返回 JSON。`error=UNSUPPORTED_SV_SYNTAX` 仅在 backend=pyverilog 且 auto 模式禁用时返回。

## 资源索引

- `scripts/render_parser_py.py` — pyverilog 渲染
- `scripts/parse_ast_output.py` — pyverilog 输出归一化
- `scripts/run_parser.py` — pyverilog 驱动
- `scripts/render_fallback_sh.py` — verible/slang 渲染（shell wrapper）
- `scripts/parse_fallback_output.py` — verible/slang 输出归一化主入口
- `scripts/normalize_verible.py` / `scripts/normalize_slang.py` — 后端特定归一化
- `references/fallback/*.md` — verible / slang 后端文档
- `Gotcha/` — pyverilog 已知陷阱

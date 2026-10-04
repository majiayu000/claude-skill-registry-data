---
name: bb-trace-signal-path
description: "在 AST JSON 上做信号路径追踪：source → sink 提取跨模块层次的传播路径，判定是否跨时钟域。供 CDC violation 根因分析与 critical path 辅助。触发场景：(1) bb-check-cdc 报 violation 需取证；(2) 综合 critical path 分析；(3) 显式 /bb-trace-signal-path。"
user-invocable: true

---

# bb-trace-signal-path

## 职责

读取 `bb-parse-ast` 产出的 AST JSON，DFS 跟踪 source 信号到 sink 的赋值/连线链，输出路径节点列表 + CDC 标记。

- 调用者：`bba-guru-synthesis`、`bb-check-cdc`
- 上游：`bb-parse-ast`（或 fallback）
- 禁止使用：Task / Agent / Skill

## Input Args

| arg | type | required | 默认 | 说明 |
|-----|------|----------|------|------|
| ast_path | path | true | — | AST JSON |
| source_signal | string | true | — | 完整 hierarchical path：`top.inst.sub.sig` 或 模块本地：`<module>.<signal>`（fix M-11） |
| sink_signal | string | true | — | 同 source_signal 格式 |
| design_name | string | true | — | — |
| max_depth | int | false | `50` | DFS 深度上限（防环） |
| stamp | string | false | `<auto>` | — |

接受两种 source 格式：
- **hierarchical**: `top.u_rx.fifo.wr_data` — 全局唯一
- **module-local**: `uart_rx.rx_data` — 当跨同名实例时歧义，trace 在歧义时返回多条 path

## Output Contract

| field | 值 |
|-------|----|
| `artifact_path` | `designs/<name>/ast/signal_path_<stamp>.json` |
| `script_path` | `designs/<name>/ast/trace_<stamp>.py` |
| `source` | str |
| `sink` | str |
| `path` | `[{module, signal, line, op}]` |
| `crosses_clock_domain` | bool |
| `valid` | bool |
| `error` | string\|null |

## 4-Phase 执行

### Phase 1 — render_trace_py

`scripts/render_trace_py.py` 渲染 Python：

```python
import json
ast = json.load(open(ast_path))
path, cdc = trace(ast, source_signal, sink_signal, max_depth)
json.dump({"path": path, "crosses_clock_domain": cdc}, open(out, "w"))
```

`trace()` 实现：以 source 为起点，按 `cont_assign` / `non_blocking_assign` / `port_connection` 边 DFS，记录每跳的 module/signal/line/op。

### Phase 2 — run_trace

`scripts/run_trace.py`：`timeout 300 uv run python <script_path> > <log> 2>&1`

### Phase 3 — parse_trace

`scripts/parse_trace.py`：

- 输出 JSON 解析；`path == []` → `error="path not found"`
- 任一跳的 `clk_domain` 与下一跳不同 → `crosses_clock_domain=true`

### Phase 4 — return

返回 JSON。调用方据 `crosses_clock_domain` + `path` 决定开 CDC issue 或调整 RTL。

## 收敛 / 失败

| 状态 | 行动 |
|------|------|
| valid=true | 提供详细 path |
| `path not found` | AST 不完整 / 信号名错；切 fallback 重解析 |
| 超 max_depth | `error="trace depth exceeded"`（疑似环） |

## 资源索引

- `scripts/render_trace_py.py`、`scripts/run_trace.py`、`scripts/parse_trace.py`
- `lib/cdc_classifier.py` — 节点 clock domain 推断
- `references/ast_traversal_rules.md`

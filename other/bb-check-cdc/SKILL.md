---
name: bb-check-cdc
description: "基于 AST 检查 CDC/RDC 违例：对比 MAS clock_domains 找跨域信号，检查是否被 2ff-sync CBB 保护。触发场景：(1) bba-guru-synthesis 综合前；(2) 显式 /bb-check-cdc。"
user-invocable: true

---

# bb-check-cdc

## 职责

读 `bb-parse-ast` 的 AST + MAS.clock_domains，识别跨时钟域 register-to-register 路径，检查是否通过 2ff 同步器，输出 violation 报告。

- 调用者：`bba-guru-synthesis`
- 上游：`bb-parse-ast`（backend=auto 自动降级到 verible/slang）
- 禁止使用：Task / Agent / Skill

## Input Args

| arg | type | required | 默认 | 说明 |
|-----|------|----------|------|------|
| file_list | path | true | — | `file_list.f` |
| ast_path | path | true | — | `bb-parse-ast` 产出 |
| mas_path | path | true | — | `designs/<name>/mas/mas.json` |
| design_name | string | true | — | — |
| stamp | string | false | `<auto>` | — |

## Output Contract

| field | 值 |
|-------|----|
| `artifact_path` | `designs/<name>/cdc/cdc_report.json` |
| `script_path` | `designs/<name>/cdc/check_cdc_<stamp>.py` |
| `log_path` | `designs/<name>/cdc/cdc_<stamp>.log` |
| `violations` | `[{type,from_clk,to_clk,signal,line,waived:bool}]` |
| `clean` | bool（unwaived violations==[]） |
| `valid` | bool |

## 4-Phase 执行

### Phase 1 — render_cdc_py

`scripts/render_cdc_py.py` 渲染：

```python
import json
ast = json.load(open(ast_path))
mas = json.load(open(mas_path))
domains = mas["clock_domains"]
# 1. 抽取所有 always_ff (@posedge clk) blocks
# 2. 对每条赋值，标注其 clock domain (信号→sensitivity clock)
# 3. R-to-R 路径：from_clk != to_clk → 候选 violation
# 4. 检查 sink 之前是否经过 wiki/cbb/2ff-sync 实例
violations = analyze(ast, domains)
json.dump({"violations": violations}, open(out, "w"))
```

### Phase 2 — run_cdc

`timeout 600 uv run python <script_path> > <log> 2>&1`，追加 `exit:<rc>`。

### Phase 3 — parse_cdc

`scripts/parse_cdc.py`：

- 解析输出 JSON
- `clean = all(not v.waived for v in violations)`
- 写 `cdc_report.json`

### Phase 4 — return

返回 JSON。`clean=false` → bba-guru-synthesis 开 `rtl-needs-fix`（CDC 不允许 waive）。

## 收敛 / 失败

| 状态 | 行动 |
|------|------|
| clean=true | 进 yosys |
| clean=false（unwaived） | 开 `rtl-needs-fix` 退出 |
| pyverilog 解析失败 | 重试 `bb-parse-ast --backend verible`（或 `slang`） |
| Phase 2 timeout（600s） | `error="CDC_TIMEOUT"` |

## 资源索引

- `scripts/render_cdc_py.py`、`scripts/run_cdc.py`、`scripts/parse_cdc.py`
- `references/2ff_sync_pattern.md` — 同步器识别规则
- `Gotcha/cdc_false_positives.md` — handshake / gray code 等不视为 violation

---
name: smart-charts
description: Intelligent chart generation and data analysis skill. Reads user-supplied
  data files (CSV/Excel/JSON), analyzes data characteristics with LLM assistance,
  auto-recommends and generates interactive ECharts visualizations.
---

# Smart Charts

> 本 skill 用于将数据文件（CSV/Excel/JSON）自动转化为交互式 ECharts 图表。
> 上传数据 → 自动分析 → 推荐图表类型 → 生成交互式 HTML。支持 16 种图表类型，多文件合并，以及 LLM 生成的数据转换代码（在沙箱中安全执行）。
>
> The sections below are written for the agent. Read them to decide when and how to call this skill.

---

## Activation Triggers

Load this skill when **any** of the following is met:

- User mentions: "analyze data", "generate chart", "data visualization", "chart", "visualization"
  / 用户提到：「分析数据」「生成图表」「数据可视化」
- User provides a data file and asks for analysis or visualization
- User asks to generate charts or a report from tabular data

---

## Hard Constraints (MUST follow)

1. **MUST follow the CLI workflow**: `data_parser.py` → confirm & recommend → `chart_generator.py`. Do NOT write ad-hoc Python scripts to replace CLI calls, even if the data looks messy.
2. **MUST use CLI parameters for messy headers** instead of bypassing the workflow. `data_parser.py` and `chart_generator.py` both accept `--skiprows N` / `--header-row N` / `--sheet <name|index>` for multi-row headers, leading junk rows, and multi-sheet Excel files. The value of N is determined by inspecting the actual data — never hard-coded.
3. **MUST use `--transform-code`** for column renaming / reshaping / aggregation when raw columns don't match the target chart format. Data parsing layer only handles "which row is the header"; all other cleaning belongs to transform code.
4. **MUST report unsupported scenarios**: if a data structure is genuinely unsupported by CLI (e.g. nested objects >1 level), report the issue to the user with a suggestion before falling back to manual scripting. Never silently bypass.
5. **MUST NOT hard-code absolute paths** in generated code; resolve paths at runtime.
6. **MUST NOT skip the confirm step** unless the user explicitly says "auto-generate" / "no need to confirm".
7. **MUST keep chart language consistent with the data language**: all chart text (title, series names, tooltips, buttons, footer, HTML `lang`) follows the data's language (auto-detected: CJK ratio > 5% → Chinese, otherwise English). Pass `--lang zh|en` ONLY when the user explicitly requests a specific language. Never mix languages within one chart.

---

## Capability Boundaries

**Supported:** CSV (.csv/.tsv/.txt), Excel (.xlsx/.xls), JSON (.json); 16 chart types (see below); up to ~10 files with auto-merge; single file ≤ 100 MB (≤ 50 MB recommended); auto-detects UTF-8/GBK/GB2312.

**Not supported:** Databases (export to CSV first), real-time/streaming data, geo maps, >100 MB files, nested JSON >1 level, non-tabular data (images/audio/video). Auto-merge requires ≥50% column overlap.

**Network requirement:** Generated HTML loads ECharts via CDN (jsdelivr/unpkg). An internet connection is required to render the charts. Agent operation assumes connectivity is already available.

---

## Security

LLM-generated transform code is executed with three safety layers (no user confirmation needed): (1) keyword blacklist (blocks `exec`, `eval`, `open`, `import`, `os.system`, etc.), (2) AST whitelist (only allows assignments, calls, loops, comprehensions), (3) sandbox builtins (only safe functions like `len`, `range`, `sorted`; `open`/`exec`/`eval`/`__import__` removed). Blocked code raises `CodeValidationError` with a `suggestion` field explaining how to resolve.

---

## Execution Workflow

1. **Obtain data** — user uploads file(s) or provides path(s).
2. **Parse data** — call `data_parser.py` on all files; for multiple files, assess merge feasibility.
3. **Confirm & recommend** — display summary table; recommend merge/separate/join strategy and chart type(s) based on data semantics; wait for user confirmation.
4. **Transform (if needed)** — if raw data doesn't match target chart's input format, LLM generates pandas transform code → security check (blacklist + AST) → execute in sandbox → standardized DataFrame. On failure: retry max 2 times, then fall back to original data + auto-detection.
5. **Generate charts** — call `chart_generator.py` → ECharts HTML. Merged data → cross-group comparison; separate data → independent charts per file.
6. **Present results** — interactive charts via `html_path`.

**Key principles:** multi-file first; confirm before executing; LLM chooses chart types by data semantics (never hard-code mapping); never hard-code absolute paths (resolve at runtime); present results immediately; adapt data via transform code when needed; security by default.

---

## Configuration

```yaml
output_dir: ./smart_charts_output  # optional; never hard-code absolute paths
```

---

## Error Codes

All errors are returned as structured dicts via `SmartChartsError.to_dict()`:
`{"error": <message>, "code": <int>, "code_name": <str>, "details": {...}}`.
The `details` field always includes a `suggestion` telling the agent how to recover.

| Code | Name | Meaning |
|------|------|---------|
| 1001 | FILE_NOT_FOUND | File path does not exist |
| 1002 | FILE_PERMISSION_DENIED | Path is not a regular file |
| 1003 | FILE_FORMAT_INVALID | Unsupported file extension |
| 1004 | FILE_SIZE_EXCEEDED | File exceeds 100 MB limit |
| 2001 | DATA_PARSE_ERROR | Parsing failed (encoding, structure, etc.) |
| 2003 | DATA_EMPTY | File or cleaned data is empty |
| 2004 | DATA_TYPE_MISMATCH | Data type mismatch |
| 3001 | TRANSFORM_EXEC_ERROR | Transform code execution failed (blacklist/AST/timeout) |
| 3002 | TRANSFORM_NO_RESULT | Transform code did not produce `result` variable |
| 3003 | TRANSFORM_INVALID_RESULT | `result` is not a DataFrame |
| 3004 | TRANSFORM_EMPTY_RESULT | `result` DataFrame is empty |
| 4001 | CHART_GENERATION_ERROR | Chart generation failed |
| 4002 | CHART_TYPE_UNSUPPORTED | Unsupported chart type |
| 4003 | CHART_CONFIG_ERROR | Axis field does not exist in DataFrame |
| 9999 | UNKNOWN_ERROR | Unclassified error |

---

## Data Parsing

> `{skill_base}` = root directory of this skill (contains `SKILL.md`).

Single file:
```bash
python {skill_base}/core/data_parser.py <file_path> [--summary] [--skiprows N] [--header-row N] [--sheet <name|index>]
```

Multiple files (with optional auto-merge):
```bash
python {skill_base}/core/data_parser.py <file1> <file2> ... [--merge] [--summary]
```

**Header / row-skipping flags (single-file only):**
- `--skiprows N` — skip the first N rows, then read the next row as the header. Use when the file has leading junk rows (notes, blanks) before any header.
- `--header-row N` — treat the 0-indexed row N as the header; rows above N are dropped. Use when the file has multi-row headers (merged cells, sub-headers) and you want one specific row as the column name.
- `--sheet <name|index>` — pick an Excel sheet by name or 0-indexed position (default: 0).
- The value of N is determined by inspecting the actual data (e.g. via a first `data_parser.py` run without flags). **Never assume a fixed N for all files.**

**Merge behavior:**
- Identical columns → vertical concat. **⚠️ A `source_file` column is injected** to indicate each row's origin file. Downstream transform code must account for this extra column.
- ≥50% column overlap → horizontal join on shared key.
- No common structure → error (advise analyzing separately).

**Programmatic API:** `DataParser.parse_files(paths, merge=...) -> {'merged': bool, 'data': ..., 'merge_type': Optional[str]}`.
- `parse_file(path, skiprows=None, header_row=None, sheet_name=0)` — single file with optional header cleaning.
- `parse_files(paths, merge=...)` — multi-file; `merge=False` returns `List[{'file', 'data'}]`, `merge=True` returns merged `DataFrame`.

---

## Chart Generation

```bash
python {skill_base}/core/chart_generator.py \
  <file_path> <chart_type> \
  --title "Chart Title" \
  --x-axis "date" \
  --y-axis "revenue profit" \
  --transform-code "<pandas code>" \
  --skiprows N --header-row N --sheet <name|index> \
  --lang zh|en \
  --output-dir "./output"
```

**Parameters:** `file_path` (required), `chart_type` (required, see table), `--title` (default follows `--lang` / data language), `--x-axis` (auto-detected if omitted), `--y-axis` (space-separated; defaults to first 5 numeric columns), `--transform-code` (LLM-generated pandas code, validated + executed before rendering), `--skiprows` / `--header-row` / `--sheet` (same semantics as `data_parser.py`; pass-through to the parsing step), `--lang zh|en` (optional; overrides auto-detection), `--output-dir` (default: `./smart_charts_output`).

**Language consistency (MUST follow):** all chart text — title, series names, tooltip labels, action buttons ("Save Image" / "Fullscreen"), scroll hint, footer, and the HTML `lang` attribute — MUST follow the data's language. The CLI auto-detects Chinese vs. English from column names and string-cell content (CJK ratio > 5% → `zh`, otherwise `en`). Pass `--lang zh` or `--lang en` ONLY when the user explicitly requests a specific language; otherwise let auto-detection match the data. Never mix languages within a single chart.

**Overflow handling:** when a chart's data points exceed the zoom threshold (default 15), the generated HTML automatically enables ECharts `dataZoom` (slider + inside-drag) and a horizontal scrollbar on the chart container, so users can drag the slider, scroll horizontally, or click the fullscreen button to inspect all data points. No agent action needed.

### Chart Types

LLM must check whether raw data matches the required format; if not, generate transform code.

| ID | Best For | Trigger Keywords | y_axis Cardinality | Required DataFrame Format | Example Columns |
|----|----------|------------------|:-------------------:|--------------------------|-----------------|
| `line` | Time-series trends | trend, change, over time, 趋势, 变化, 走势 | 1~N | 1 category/time + 1~N numeric | `month, productA, productB` |
| `bar` | Category comparison | compare, rank, difference, 对比, 比较, 排名, 差异 | 1~N | 1 category + 1~N numeric | `city, revenue, profit` |
| `area` | Cumulative change | cumulative, change, 累计, 变化 | 1~N | 1 category/time + 1~N numeric | `date, uv, pv` |
| `pie` | Composition/share | share, composition, proportion, 占比, 构成, 比例 | 1 | 1 name + 1 value | `category, share` |
| `scatter` | Correlation | correlation, relationship, scatter, 相关, 关系, 散点 | 1 | 2 numeric, or 1 category + 1 numeric | `height, weight` |
| `radar` | Multi-dimension comparison | multi-dimension, comprehensive, radar, 多维, 综合, 雷达 | N | 1 indicator + N numeric | `metric, productA, productB` |
| `heatmap` | Density/cross-tab | density, cross, matrix, heatmap, 密度, 交叉, 矩阵, 热力 | N | 2 category + 1 numeric | `row, col, value` |
| `treemap` | Hierarchical proportion | hierarchy, proportion, nested, 层级, 占比, 嵌套 | 1 | 1 name + 1 value | `category, sales` |
| `graph` | Entity relationships | relationship, network, topology, 关系, 网络, 拓扑 | special | source + target (+ value) | `from, to, weight` |
| `boxplot` | Distribution/outliers | distribution, outlier, quartile, 分布, 离群, 四分位 | N | N numeric | `math, chinese, english` |
| `waterfall` | Incremental change | increment, change, waterfall, 增量, 变化, 瀑布 | 1 | 1 category + 1 numeric (increments) | `month, profit_delta` |
| `gauge` | KPI progress | progress, kpi, achievement, 进度, KPI, 达成 | 1 | 1 numeric (mean used) | `completion_rate` |
| `sankey` | Flow transfer | flow, transfer, sankey, 流向, 流量, 转移 | special | source + target + value | `origin, destination, amount` |
| `funnel` | Conversion rate | conversion, funnel, churn, 转化, 漏斗, 流失 | 1 | 1 name + 1 value | `stage, count` |
| `sunburst` | Multi-level composition | hierarchy, proportion, nested, 层级, 占比, 嵌套 | 1 | 1 name + 1 value | `category, value` |
| `wordcloud` | Frequency/keywords | word frequency, keywords, text, 词频, 关键词, 词云 | 1 | 1 name + 1 value | `word, frequency` |

**y_axis cardinality key:** `1` = only first column used (extras silently ignored); `1~N` = each column becomes a series; `N` = multiple columns expected; `special` = auto-detects source/target/value columns.

### Programmatic API

```python
from core.chart_generator import ChartGenerator

# Single chart — returns {'chart': {'success', 'html_path'/'error', ...}}
# lang=None auto-detects from data; pass 'zh'/'en' to override (only when user asks).
result = ChartGenerator(output_dir="./output").generate_chart(
    df=df, chart_type="bar", title="Regional Revenue",
    x_axis="region", y_axis=["revenue"], lang=None,
)
# result = {"chart": {"success": True, "html_path": "...", "chart_type": "bar", "title": "..."}}

# Batch — returns {'charts': [...]} where each item has the same shape as 'chart' above
result = ChartGenerator(output_dir="./output").generate_multi_charts(
    df=df,
    chart_configs=[
        {"type": "bar",  "title": "Regional Revenue", "x_axis": "region", "y_axis": ["revenue"]},
        {"type": "line", "title": "Monthly Trend",   "x_axis": "month",  "y_axis": ["revenue", "profit"]},
    ],
    lang=None,
)
```

On failure, `success` is `False` and `error` holds the structured dict (same shape as `SmartChartsError.to_dict()`). No exception is raised — the agent inspects `success` to decide next steps.

---

## Transform Code Generation

When raw data doesn't match the target chart's input format, use this prompt template:

```
Known information:
- Raw data columns: {columns_with_dtypes}
- Data sample (first 5 rows): {sample}
- Target chart type: {chart_type}
- Required format for this chart: {chart_input_spec}

Generate a pandas code snippet that transforms df into a result DataFrame matching the chart's input format.

Rules:
1. Only use variables: df, pd, np
2. Must produce a variable named result (pd.DataFrame)
3. Do not modify df in-place; use df.copy() or chain operations
4. Keep code concise; prefer pandas built-in methods (pivot_table, melt, groupby, rename, etc.)
5. If raw data already matches the required format, output an empty string
6. Do NOT use: import, open, exec, eval, os, sys, subprocess, file I/O, network calls

Output format:
```python
# {one-line description of what the transform does}
{transform_code}
```
```

**Common transform patterns:**
- Long→multi-series: `result = df.pivot_table(index='<time>', columns='<category>', values='<value>', aggfunc='sum').reset_index()`
- Long→pie (filter): `result = df[df['metric']=='revenue'][['category','value']].rename(columns={'category':'name'})`
- Wide→long: `result = df.melt(id_vars=['date'], var_name='name', value_name='value')`
- Aggregate→bar: `result = df.groupby('<category>')['<value>'].sum().reset_index()`
- Rename columns: `result = df.rename(columns={'来源':'source','去向':'target','金额':'value'})`
- Compute delta→waterfall: `tmp = df.copy(); tmp['delta'] = tmp['profit'].diff().fillna(tmp['profit'].iloc[0]); result = tmp[['month','delta']]`
- Rename messy/uninformative column names (after `--header-row` leaves columns like `10分`, `unnamed_3`): `result = df.rename(columns={'unnamed_0':'student_id','unnamed_1':'name','10分':'homework_score','30分':'exam_score'})`
- Forward-fill merged cells (when only the first row of a group is populated): `result = df.ffill()`
- Combine sub-headers into a single column name (when `--header-row N` flattens one row but loses context): `result = df.rename(columns={c: f'{c}_score' for c in df.columns if c not in ['student_id','name']})`

For CLI reference and installation instructions, see [REFERENCE.md](./REFERENCE.md).

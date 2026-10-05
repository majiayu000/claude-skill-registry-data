---
name: qa-generated-test-case
description: Generate high-coverage Chinese functional and business-flow test cases from PRDs, especially Web admin or platform PRDs. Use when Codex is asked to extract PRD text, design QA coverage, generate the fixed 7-column testcase table, export CSV/XLSX, validate testcase format, or optionally consult an external indexed PRD memory source without reading full historical archives.
---

# QA Generated Test Case

## Core Rule

Act as a senior QA analyst for Web 管理后台 and platform product requirements. Generate executable functional and business-flow test cases from the current PRD, not generic checklists.

Always prioritize:

1. 功能点覆盖
2. 主流程、分支流程、状态流转
3. 异常场景
4. 边界值和多条件组合
5. 角色权限
6. 上下游依赖和历史兼容风险

The current PRD is the primary source. If external retrieval results conflict with the current PRD, use the current PRD and list the conflict under `待确认问题`.

## Data Boundary

This skill package must stay reusable and lightweight.

Allowed in the skill:

1. Workflow prompts, output rules, quality checks, and PR description templates.
2. Reusable scripts for PRD extraction, testcase table validation/export, and external-memory retrieval.
3. Small tests and synthetic fixtures.

Not allowed in the skill:

1. One-off run outputs such as `runs/`, generated CSV/XLSX files, extracted PRD text, or temporary design drafts.
2. Customer/project/private historical PRDs, full PRD digests, large source indexes, or business-memory archives.
3. Tokens, local config, browser state, or any sensitive source material.

If historical context is needed, use an explicitly provided private data directory, memory/document store, or separate data package. At runtime, read only the retrieval result produced by `scripts/prd_memory_retrieval.py search-memory`; do not read the full historical archive.

See `references/data-boundary.md` and `references/retrieval-design.md`.

## Quick Workflow

1. Extract PRD text.
   Use `scripts/extract_prd.py <prd.docx> --out <run_dir>/00-extracted-prd.txt` for Word files. Markdown and text files can be read directly or passed through the same script.
2. Optionally retrieve historical context.
   If the user provides an external index or private PRD archive, use `scripts/prd_memory_retrieval.py search-memory` with deterministic filters first, then keyword similarity, and read only the top N retrieval output.
3. Produce process artifacts outside the skill package.
   Use a non-repo run directory such as `/tmp/qa-testcase-run/<topic>` or a user-approved project output directory.
4. Follow the workflow prompt structure.
   See `references/workflow.md`.
5. Enforce the fixed final output format.
   See `references/output-format.md`. The official final table has exactly 7 columns.
6. Validate and export.
   Use `scripts/testcase_table_tools.py` to parse, validate, create CSV, and create XLSX.
7. Persist reusable learning only with user approval.
   For durable project memory, write to the configured memory/document store or a private data package. Do not sync historical material back into this skill.

## Final Output Contract

The final testcase table must have this exact header and order:

`用例名称 | 所属模块 | 前置条件 | 步骤描述 | 预期结果 | 用例等级 | 编辑模式`

Hard constraints:

1. `所属模块` is fixed for all rows as `/<需求名称>`.
2. `编辑模式` is always `STEP`.
3. `用例等级` is `P0`, `P1`, `P2`, or `P3`.
4. `步骤描述` uses numbered steps like `[1]...；[2]...`.
5. `预期结果` uses the same step numbers as `步骤描述`; do not add more expected-result step numbers than action step numbers.
6. Do not include literal `\n`, `<br>`, or `<br/>` inside case text.
7. Keep case names unique and concrete. Avoid vague names like `创建成功`.
8. Put uncertain or missing PRD information under `待确认问题`, not into formal cases.

## Script Usage

Extract a Word PRD:

```bash
python3 scripts/extract_prd.py "/path/to/需求.docx" --out "/tmp/qa-testcase-run/topic/00-extracted-prd.txt"
```

Build an external historical-memory index from a private data directory:

```bash
python3 scripts/prd_memory_retrieval.py build-index \
  --source-dir "/path/to/private-prd-memory" \
  --out-index "/path/to/private-prd-memory/index.jsonl" \
  --out-csv "/path/to/private-prd-memory/index.csv"
```

Retrieve top N snippets before testcase generation:

```bash
python3 scripts/prd_memory_retrieval.py search-memory \
  --index "/path/to/private-prd-memory/index.jsonl" \
  --product-line "Rosetta" \
  --module "任务列表" \
  --tags "筛选,导出" \
  --query "跨页选中 导出筛选结果" \
  --top-n 5 \
  --out "/tmp/qa-testcase-run/topic/retrieved-memory.md"
```

Parse Markdown table, validate, and generate CSV/XLSX:

```bash
python3 scripts/testcase_table_tools.py from-markdown \
  --markdown "/tmp/qa-testcase-run/topic/03-testcases.md" \
  --csv "/tmp/qa-testcase-run/topic/04-testcases-excel.csv" \
  --xlsx "/tmp/qa-testcase-run/topic/05-testcases.xlsx" \
  --module "/需求名称"
```

Validate an existing CSV:

```bash
python3 scripts/testcase_table_tools.py validate-csv \
  --csv "/tmp/qa-testcase-run/topic/04-testcases-excel.csv" \
  --module "/需求名称"
```

If a script reports a format error, fix the source Markdown/CSV and rerun validation before reporting completion.

## Process Artifact Expectations

`01-normalized-prd.md` should include:

1. 背景与目标
2. 角色与对象
3. 功能范围
4. 业务规则和字段映射
5. 测试假设与待确认

`02-test-design.md` should include:

1. 测试目标
2. 覆盖分层
3. 关键业务规则转测试规则
4. 高风险点
5. 测试数据建议
6. 待确认问题
7. 覆盖说明

`03-testcases.md` should include:

1. Final 7-column Markdown testcase table
2. 待确认问题
3. 覆盖说明

`04-testcases-excel.csv` and `05-testcases.xlsx` must be generated from the same final table and kept outside this repository unless the user explicitly asks to inspect a sample.

## Quality Gate

Before final response, verify:

1. The PRD was actually read or extracted.
2. External retrieval was used only when an approved index/data source was provided; only top N snippets were read.
3. Main flow, branches, exceptions, boundaries, permissions, and dependencies are represented.
4. Final table validates with `errors=none`.
5. XLSX opens structurally, or at least passes zip integrity validation.
6. Any durable memory write or document upload was explicitly approved and stored outside the skill package.

Use `references/quality-scorecard.md` when the user asks for scoring, benchmarking, or improvement over manual writing efficiency.

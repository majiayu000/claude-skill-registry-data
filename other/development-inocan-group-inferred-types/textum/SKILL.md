---
name: textum
description: Textum PRD→Scaffold→Story workflow for Codex with low-noise outputs and gate checks.
---

# Textum

Hard constraints:
- Low-noise is non-negotiable (avoid attention/context pollution).
- Multi-window: each stage is self-contained; do not narrate upstream/downstream flow.
- Output “next step” as a stage name only.

Prereq (runtime):
- `uv` installed.
- Run `uv sync --project .codex/skills/textum/scripts` once (creates `.codex/skills/textum/scripts/.venv`).

Supported stages:
- PRD Plan → `references/prd-plan.md`
- PRD Check → `references/prd-check.md`
- PRD Render → `references/prd-render.md`
- PRD Slice → `references/prd-slice.md`
- Scaffold Plan → `references/scaffold-plan.md`
- Scaffold Render → `references/scaffold.md`
- Scaffold Check → `references/scaffold-check.md`
- Split Plan → `references/split-plan.md`
- Split Generate → `references/split.md`
- Split Check1 → `references/split-check1.md`
- Split Check2 → `references/split-check2.md`
- Split Checkout → `references/split-checkout.md`
- Story Check → `references/story-check.md`
- Story Pack → `references/story-pack.md`
- Story Exec → `references/story.md`
- Story Full Exec (experimental) → `references/story-full-exec.md`

Routing:
- CN intent examples:
  - `PRD Plan`: 需求澄清 / 澄清需求 / PRD 计划
  - `PRD Render`: 生成PRD / 渲染PRD / 输出PRD
  - `PRD Check`: 校验PRD / 检查PRD / 门禁
  - `PRD Slice`: PRD 切片 / 切片 / 低噪切片 / slice
  - `Scaffold Plan`: 上下文提取 / 全局上下文 / Scaffold 计划
  - `Scaffold Render`: 生成GLOBAL-CONTEXT / 渲染GLOBAL-CONTEXT / 输出GLOBAL-CONTEXT
  - `Scaffold Check`: 校验GLOBAL-CONTEXT / 检查GLOBAL-CONTEXT / GC 门禁
  - `Split Plan`: Story 拆分规划 / Split Plan / 拆分计划
  - `Split Generate`: 生成Story / Split Generate / 拆分生成
  - `Split Check1`: Split 校验1 / 拆分校验1 / 结构阈值校验
  - `Split Check2`: Split 校验2 / 拆分校验2 / 引用一致性校验
  - `Split Checkout`: Split Checkout / 依赖图 / 导出依赖图
  - `Story Check`: Story 校验 / Story Check / 单 Story 门禁
  - `Story Pack`: Story 执行包生成 / Story Pack / 生成执行包
  - `Story Exec`: Story 执行 / Story Exec / 单 Story 执行
  - `Story Full Exec`: Story 批量执行 / Story Full Exec / 试验性全执行
- If intent is unclear, ask the user to pick one: `PRD Plan` / `PRD Check` / `PRD Render` / `PRD Slice` / `Scaffold Plan` / `Scaffold Render` / `Scaffold Check` / `Split Plan` / `Split Generate` / `Split Check1` / `Split Check2` / `Split Checkout` / `Story Check` / `Story Pack` / `Story Exec` / `Story Full Exec`.

Always:
- For every `FAIL` item (in diagnostics/replan packs): include `loc/problem/expected/impact/fix`, and `fix` must be a single action.
- Keep chat output low-noise: prefer paths (`wrote: docs/*`) over pasting long `FAIL` lists.

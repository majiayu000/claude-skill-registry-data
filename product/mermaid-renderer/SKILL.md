---
name: mermaid-renderer
description: Phase 4.5 hook by Phase-2-Quality-Fix sprint. 封装 mmdc/npx Mermaid CLI subprocess,把 LLM 输出的 `<div class="mermaid">...</div>` block 渲染为 PNG。Use AFTER cite-bound-content-generator (Phase 4 Turn 1) and BEFORE report-bundle-builder (Phase 5). Production smoke must fail closed if rendering fails.
license: MIT (R3c by Phase-2-Quality-Fix)
---

# mermaid-renderer (Phase 4.5)

## 用途

Phase 4.5 hook,提取 LLM 输出的 `<div class="mermaid">...</div>` block,转成 PNG 文件,替换为 `<img src="assets/decision-tree-N.png">`。优先用 `mmdc`;若未全局安装但 `npx` 可用,临时调用 `@mermaid-js/mermaid-cli`。

## 接口

```python
render_mermaid_to_png(
    mermaid_text: str,
    output_path: Path,
    timeout_sec: int = 30,
    width: int = 5000,
    scale: int = 2,
) -> dict
```

返回:

```python
{
    "ok": bool,                  # True = PNG 渲染成功
    "path": Path | None,         # 成功时是 output 文件路径
    "fallback_inline": str | None,  # 失败时是原 mermaid 文本
    "reason": str,               # 状态说明 ("mmdc ok" / "mmdc not installed" / "mmdc exit N: ..." / "mmdc timeout")
    "render_width": int,          # 默认 5000
    "render_scale": int,          # 默认 2
}
```

## 三层 fallback

1. **mmdc/npx 不可用**→ ok=False + fallback_inline = mermaid_text
2. **subprocess 失败**(returncode 非零 / 输出文件不存在)→ ok=False + fallback_inline + 错误 message (含 stderr 前 500 char)
3. **subprocess 超时**(默认 30s)→ ok=False + fallback_inline + "mmdc timeout"

production smoke 必须把 ok=False 视为阻断；非生产 dry-run 可保留 inline `<div class="mermaid">...</div>` 便于调试。

## V25 render quality contract

Renderer defaults to `mmdc -w 5000 --scale 2`. Callers may only lower these values for explicit test fixtures. `production_smoke_audit` blocks low-resolution decision-tree assets, so PNG existence alone is not proof.

## Production provenance contract

Production orchestration must write `.cache/<slug>/mermaid_render_manifest.json` whenever decision-tree assets are rendered. The manifest must include:

- `renderer: "mermaid-renderer"`
- one block per Mermaid source with `index`, `ok`, `path`, `reason`, and original `source`
- per-block graph quality metrics: `edge_count`, `decision_node_count`, `numeric_evidence_count`, and `cross_point_count`
- `ok=false` if any block failed

PNG-only assets, Chrome screenshots, or manually appended `skill_run_log` entries do not prove this skill ran. Production smoke must block when decision-tree PNGs exist without this manifest.

## Diagram substance contract

Decision trees are not decorative. A V25-level report needs flowcharts with branching decision nodes, numeric pathway/conversion labels, citation anchors in the Mermaid source, and cohort/pathway/LP cross-point numbers. Linear `A-->B` diagrams and heatmaps without data provenance are invalid.

Every numeric label must be source-supported by its nearest/declared anchor. A diagram fails production smoke when a number is anchored to a source that does not contain that exact number or the saved formula/model evidence deriving it. This gate applies to time windows and operational KPIs as well as percentages, patient counts, market sizes, and currency values.

LP must be embedded as node-level graph logic, not prose in an edge label. Production Mermaid sources should include explicit LP badge/node markers such as `LP1_BADGE`, LP classes (`classDef lpcrown` / `classDef lpstd`), or LP connector edges (`-.->`) that tie a cohort/pathogen/pathway cross-point to an action node. A set of diagrams with identical edge/decision counts and repeated source templates is a failed workflow, even if PNG rendering succeeds.

## 依赖

`mmdc` CLI(via Node.js)。详见 [`references/mmdc-install.md`](references/mmdc-install.md)。

## DoD 注脚 (architect 修订)

无 mmdc 时本 skill 5 单测仍过(mock `shutil.which` 返回 None)。但 5 疾病重跑要 ≥ 4 PNG 决策树达标,需用户机器装 mmdc 后重跑。

## P0 设计意图

不依赖任何疾病特定 / 药品特定数据。纯通用 Mermaid → PNG 渲染器。

---
name: cite-bound-content-generator
description: Phase 4 Turn 1 of disease-market-sizing-orchestration. Generates report HTML with mandatory citation anchors per fact claim. Reads contract + staging + sources/. Every drug/treatment/stat/recommendation MUST carry [pmid:.../guideline:.../nct:...] anchor that resolves to an actual file in sources/. NEVER hardcode drug names or numerical claims. Use AFTER evidence recall (phase 3), BEFORE content-verification-layer (Turn 2).
license: Cite-or-Block strict (P0 iron law, see ../../CLAUDE.md)
---

# Cite-Bound Content Generator (Phase 4 Turn 1)

## LLM Prompt Constraints (enforced inside ask_llm callback)

> "You write report HTML for the disease/region described in the contract. Every fact claim
> (drug name, brand name, dosage, number, recommendation grade, epidemiology, mechanism)
> MUST carry a citation anchor in one of these forms:
> `[guideline:<source_id>:<locator>]` / `[pmid:<id>:<locator>]` / `[nct:<id>:<locator>]`.
> The source_id of every anchor MUST appear in the provided sources_summary.
> Sentences without an anchor for a fact claim are forbidden — your report will be rejected."

## Agent-Authored Compose Artifact Contract

Production plugin runs should pass report content through `.cache/<slug>/agent_authored_compose.json` instead of letting a callback write HTML/model/flow content. The callback may read this JSON and return it to `compose()`, but the content remains subject to all compose and verification gates.

Required JSON keys:

- `html`: report HTML with citation anchors; direct `.html` files are not the primary contract
- `claims`: citation index candidates using the same `claim_text` / `anchor` / `position` / `classification` shape
- `provenance`: must include `authoring_mode=agent_authored_compose_artifact`, `generated_by=codex_or_claude_code_plugin_executor`, and current `source_run_slug`
- `source_usage`: must show body utilization for PubMed, ClinicalTrials.gov/AACT, and PubTator/entity channels when those sources were fetched
- `formula_dag_ref`: path/reference to reusable model output; formula DAG is not authored by the callback
- `mermaid_sources`: decision-tree sources to be rendered and audited by `mermaid-renderer`

`compose()` persists `compose_authoring_provenance.json` and mirrors `authoring_provenance` into `citations_index.json`. Production smoke must block if this provenance is absent or says callback-authored content.

### Final Compose Artifact Gate

Production plugin continuation must reject precompose artifacts. `.cache/<slug>/agent_authored_compose.json` is acceptable only when `provenance.phase=final`, `provenance.source_run_slug` matches the current slug, `reader_layer.html` is non-empty, and `audit_layer.evidence_support_table` plus `audit_layer.reader_to_audit_mapping` are non-empty. A precompose checkpoint, source index, or process stub cannot be promoted to report body.

## IFI 章节强制结构(每次 compose 必读 — R1 by Phase-2-Quality-Fix)

参考完整模板:[`references/ifi-section-template.md`](references/ifi-section-template.md).

输出 html 必须含以下结构 (composer.py `_assert_ifi_structure` 在 `enforce_ifi=True` 时强制,违者抛 `ComposeError` 含**所有缺失项** + orchestrator retry loop 反馈给 LLM 一次性补齐):

- 7 个 `<section data-section="...">` marker:`exec-summary` / `epidemiology` / `treatment-landscape` / `market-sizing` / `competitive-dynamics` / `lp-framework` / `appendix`
- `market-sizing` 内三 `<section data-subsection="tam|sam|som">` 子段
- `<div class="mermaid">...</div>` 决策树 block ≥ 4 张
- LP 提及次数 ≥ 50；`LP1` / `LP 1` / `LP2` 等编号写法必须计入，但不能只靠关键词堆砌通过
- 主报告 text 长度 ≥ 4000 字(去 html tag)
- H2/H3 深度 ≥ 10, Mermaid 每张必须有实际路径逻辑(不是 `A-->B` toy diagram)
- Mermaid 必须包含可审计的交叉点/分流/LP 数字；数字必须带 citation。没有 cohort × pathway × LP 交叉数字的流程图不能算 V25 级图。
- Mermaid 中每个数字标签必须由就近 locator anchor 支撑；不能把 `PCP>4.5%`、`2.4 per 1000`、`24小时` 等数字锚到不含该数字的 PMID 或泛化来源。
- 所有市场/统计数字必须锚到含该数字或公式证据的源文件；派生数字必须先写入可引用的 model/evidence 文件后再引用。
- citation anchor 必须带 locator，例如 `[guideline:ID:line:42]` / `[pmid:123:abstract]` / `[evidence:path:line:12]`；无 locator anchor 不能支撑生产数字 claim。
- 正文必须实际使用本轮多渠道来源，不能只反复引用 guideline 或内部 model 文件；PubMed/PMC/NCT/BioC/entity/evidence-grading 产物进入报告论证才算进入链路。来源索引或附录清单不能单独满足正文来源利用率。
- ClinicalTrials.gov/AACT 与 PubTator/entity recall 如果已经保存到本轮 `sources/`，正文必须用 `[nct:...]` / `[aact:...]` / `[pubtator:...]` 锚点进入论证；只抓取、只列索引、只写进附录都不算进入任务链。
- `medical-evidence-grading` 标为 D 的 PubMed 记录只能做背景或附录参考，不能作为正文结论、市场数字、LP 建议或药物-病原判断的支撑锚点。
- 公式 DAG / model evidence 只能支撑派生数字，不能成为正文主要 citation 来源；正文必须主要锚到指南、文献、试验、全文、实体证据和本轮保存的模型证据组合。
- 禁止把“证据消化矩阵”反复作为正文主体。证据矩阵只能帮助组织材料，最终报告必须写成可读的 V25 级市场叙事、队列分析、路径判断和 LP 策略。
- 文献召回 >50 是硬门槛而非停止点；呼吸科 IFI 等热门领域应以 >100 saved literature sources 为正常目标，并在正文分析中呈现主题化利用。
- 正文必须包含核心证据综合，而不是只把 PubMed/PMC/试验堆进附录。对于 >100 PubMed saved sources 的生产报告，非附录正文必须有足够 unique PMID 锚点进入诊断、队列、病原、治疗、预后或 LP 方法论分析。
- V25 对标不仅是标题/表格/图片数量；正文应包含增长驱动、支付/医保/准入/院内采购影响、LP排序方法，以及方法/证据等级/敏感性说明。缺少这些战略深度模块的报告不能算 V25 级。
- 禁止模板堆砌：不要用 `Block 1..N`、同句复制、批量替换队列名、重复“执行含义/质量要求”段落来凑字数、表格数或 LP 次数。
- 禁止机械审计口吻：不要反复输出 `来源见本行`、`公式输入核对项`、`本行证据`、`证据项`、`本项仅按`、`队列动作N/模块N` 等检测痕迹。证据说明必须融入自然市场报告 prose 或放入独立来源索引；`agent_authored_compose.json.claims[*].claim_text` 同样不能残留这些短语。
- 禁止把 source inventory / `已保存于 sources` / `附录证据说明` / `待 worker` / `后续量化模型` 当正文
- 每数字 + 每事实声明带 citation 锚点(P0 铁律,无锚点 = 凭记忆 = 阻断)

## sub-page 输出指令(R3b by Phase-2-Quality-Fix · 每 cohort 独立 .html)

每 cohort(基于 `staging.dimensions` 的 sub_cohorts)用 `<sub-page slug="cohort-slug">...</sub-page>` 包裹独立段:

```html
<sub-page slug="1l-treatment">
  <section class="cohort-page" data-cohort="1l-treatment">
    <h1>1L 治疗 cohort 深度分析</h1>
    ...
  </section>
</sub-page>
```

`composer._parse_sub_pages` 解析后, `ComposedReport.sub_pages: list[dict {slug, html}]` 经 `_persist_sub_pages` 落盘成 `output/<disease-slug>/page_<cohort-slug>.html`,主报告通过 `<a href="page_<slug>.html">` 链接。子页必须是实质 cohort 页:包含诊疗路径、市场测算/交叉点数字、表格、LP 动作和 citation；几百字节空壳页必须被下游 audit 阻断。

## Functions

- `compose(slug_dir, ask_llm, previous_violations=None, *, enforce_ifi=False, output_dir=None, return_report=False) -> (html_path, idx_path) | ComposedReport`
  - `enforce_ifi=True` (production) → 强制 IFI 结构,违者 ComposeError
  - `enforce_ifi=False` (default, fake-LLM tests) → 只查 anchor 解析,不查结构
  - production orchestration must call `return_report=True` so sub_pages/toc_anchors are passed to bundle; losing `ComposedReport` is a workflow bug.

- `_parse_sub_pages(raw_html) -> (main_html, sub_pages)` — 抽 `<sub-page slug="...">` 包裹的子页

- `_extract_toc_anchors(html) -> list[str]` — 从 main_html H2/H3 id 抽 TOC 浮动锚点

- `ComposedReport(main_html, sub_pages, toc_anchors, claims, raw_html)` — 升级输出 schema dataclass

## P0 Watchdog

`tests/test_cite_bound_content_generator.py::test_compose_p0_watchdog` —
grep skill source for forbidden hardcoded patterns. CI blocks on hit.

---
name: trade-customer-intel-for-openclaw
description: OpenClaw-native SIEGER-aligned customer intelligence. Use a structured evidence bundle to produce a bilingual report with claim-level evidence, decision gates, industry-specific analysis, and proposed sales angles that require explicit approval before email drafting.
metadata: {"openclaw":{"role":"stage_worker","workspace_owner_skill":"trade-active-outreach-combo","single_skill_policy":"attach_only","feishu_container_creation":"forbidden","requires_master_base":true,"requires_master_record":true,"table_policy":"adapt_existing_or_create_minimal","rule_capture":"ask_before_skill_update"}}
---

# Trade Customer Intel for OpenClaw

## Overview

This skill is the OpenClaw-native companion to the repository's classic version.

It is designed for cloud OpenClaw environments where search and page retrieval are performed by platform tools first, and a Python report builder then turns the resulting evidence bundle into a structured bilingual report.

This is the core judgment layer in the active outreach chain: search finds candidates, screening normalizes them, customer intel decides what is worth saying, and the email Skill drafts only from these verified signals.

## Table Policy

- 优先适配企业已有表头和知识库归口，不强制使用课堂标准表。
- 没有可用表格时，龙虾按企业产品、市场和背调流程新建够用表。
- 用户确认新的背调规则、风险分级、近期信号判断、市场信号来源、证据来源权重、行业习惯或表头映射后，先追问：`是否更新到对应 Skill 以便下次自动复用`。真实写入必须得到用户授权。

## Inputs

Normalize operator input into this lead shape:

```json
{
  "company_name": "",
  "person_name": "",
  "email": "",
  "company_website": "",
  "country_or_market": "",
  "product_or_offer": "",
  "industry_lens": "auto",
  "seller_context": {},
  "notes": ""
}
```

The final report-builder input must wrap that lead together with an evidence bundle:

```json
{
  "lead": {},
  "evidence_bundle": {
    "evidence_items": [],
    "search_results": [],
    "page_snapshots": [],
    "search_runs": [],
    "errors": []
  }
}
```

Validate this envelope against [customer-intel-evidence-input.schema.json](./schemas/customer-intel-evidence-input.schema.json). Reject malformed nested objects or arrays instead of coercing them.

`evidence_items` 可为每条证据显式提供 `claims`。报告会将结论标为 `fact`、`inference` 或 `hypothesis`，并用 `EV-*` 和 `CL-*` 保留证据到结论的对应关系。

## Tooling Rules

- Search tool: `coze-web-search`
- Primary fetch tool: `scrapling-official`
- Fallback fetch tool: `coze-web-fetch`

Do not use Tavily, DuckDuckGo HTML scraping, or `r.jina.ai` in this variant.

## Search Order

Search in this fixed order:

1. Official website and domain evidence
2. LinkedIn company page and personal profile
3. Facebook and Instagram
4. X / Twitter and YouTube
5. General web search and news

The evidence bundle should preserve recent-signal clues when available: LinkedIn updates, news, hiring, funding, expansion, new warehouse, channel changes, product launches, target-market regulation, tariff, trade agreements, and compliance changes.

## Search Execution Rules

- Keep query budgets small and deterministic
- Prefer direct identifiers over broad inference
- Stop expanding official website candidates once a high-confidence official domain is identified
- Keep only a small number of representative results per platform
- Do not fail the overall task just because one platform is weak or blocked

## Fetch Rules

- Use `scrapling-official` first for page text extraction
- If `scrapling-official` fails, retry with `coze-web-fetch`
- If full-page content is unavailable, keep the search result snippet and continue
- Record fetch failures into `evidence_bundle.errors`

## Entity Resolution Rules

- Prefer official website over search guess
- Do not treat public email domains as company-domain proof
- Do not merge ambiguous people and companies unless multiple signals align
- Mark weak conclusions as inference
- If LinkedIn evidence is missing, keep person matching conservative

## Output Requirements

Follow [report-template.md](./references/report-template.md) and [source-playbook.md](./references/source-playbook.md).

- Keep analysis mainly in Chinese
- Keep sales-facing content bilingual
- Keep risk scoring conservative
- Preserve `Low`, `Medium`, `High` ratings only
- Use the SIEGER v2 decision gates: identity, evidence, seller offer, product fit, and risk
- Do not produce a numeric score until at least three SIEGER dimensions have evidence-backed claims
- Include recent customer signals and market/compliance signals when evidence supports them
- Keep every generated sales angle at `proposed`; only an explicit human or authorized workflow action may mark it `approved`
- Provide sales angles with valid `CL-*` and `EV-*` references so downstream email drafting can consume them without inventing facts
- Generate outreach persona and outreach pack only when public evidence supports them
- If evidence is thin, use `limited_evidence` instead of forcing personalization

## Main Script

Use [build_customer_intel_report_from_evidence.py](./scripts/build_customer_intel_report_from_evidence.py) as the report-builder entrypoint.

### Example run

```bash
python3 ./scripts/build_customer_intel_report_from_evidence.py \
  --input-json /path/to/openclaw-customer-intel.json \
  --markdown-out /tmp/customer-intel-openclaw.md \
  --json-out /tmp/customer-intel-openclaw.json
```

## Notes

- This skill and the classic version share the same v2 contract and judgment core
- This version optimizes for cloud stability and controlled tool orchestration

## Feishu 回写规则（经验教训沉淀）

### 主表回写（Lead Workflow Master）

回挂主表时，至少更新以下 7 个字段：

| 字段 | 说明 |
|---|---|
| `intel_doc_ref` | 背调文档链接（URL 类型） |
| `risk_rating` | SingleSelect: low / medium / high / critical |
| `entity_confidence` | Number: 0-100 |
| `current_stage` | Text: intel_completed / hold / failed |
| `current_status` | SingleSelect: intel_completed 等 |
| `recommended_next_action` | Text: ready_for_email_draft / hold_for_manual_review |
| `last_updated_at` | DateTime: 当前时间戳（毫秒） |

### 背调结果表回写（Customer Intel Results）

回写字段：

| 字段 | 说明 |
|---|---|
| `线索编号 lead_id` | Text |
| `风险等级 risk_rating` | SingleSelect: low / medium / high / critical |
| `主体置信度 entity_confidence` | Number: 0-100 |
| `公司匹配状态 company_match_status` | SingleSelect: verified / partial / unverified / mismatch |
| `联系人匹配状态 person_match_status` | SingleSelect: verified / partial / unverified / not_applicable |
| `背调阶段结果 intel_result` | SingleSelect: intel_completed / intel_insufficient_evidence / intel_failed |
| `背调文档引用 intel_doc_ref` | URL: `{link, text}` 对象 |
| `中文摘要 summary_cn` | Text |
| `英文摘要 summary_en` | Text |
| `销售切入点 key_sales_angles` | Text |
| `关键风险 key_risks` | Text |
| `证据清单 evidence_list` | Text |

### Feishu API 注意点（踩坑记录）

1. **字段名必须完全匹配** — 飞书 API 字段名是「中文 英文」混合格式（如 `线索编号 lead_id`），带空格，必须精确一致。少一个空格或顺序颠倒都会报 `FieldNameNotFound`。
2. **URL 类型字段需要对象格式** — 不能用纯字符串 `"https://"`，必须用 `{"link": "https://...", "text": "显示文本"}`
3. **SingleSelect 字段用选项名** — 传 `"low"` 不是 `"optXXXX"` ID
4. **Number 字段传数字** — `95` 不是 `"95"`
5. **DateTime 字段传毫秒时间戳** — `1745570700000`
6. **分两步写入** — URL/SingleSelect 类字段和 Text/Number/DateTime 字段最好分两批写入。第一次 `create_record` 只写 Text/Number/SingleSelect，第二次 `update_record` 补 URL 字段。一次性大批量写入容易触发字段类型转换错误。
7. **文本内容不要过长** — 长文本（如 evidence_list）控制在 300 字以内，完整内容写入背调文档而非 table 字段。
8. **创建文档后回写 wikidoc_token** — 用 `feishu_wiki(action="create")` 创建文档后，记录 `obj_token`（doc_token），再用 `feishu_doc(action="write")` 写入内容。URL 拼接格式：`https://evenbetter.feishu.cn/wiki/{node_token}`。

### 背调文档标题规范

文档创建路径：`首页/` 下创建独立页面

命名格式：`{lead_id}_{公司简称}_背调报告`

文档内必须包含的章节（详见 report-template.md）：背调摘要（中英文）、身份快照、Intel Decision、公司画像、数字足迹、主题信号、销售切入点（≥3个）、风险评级、证据清单、需人工确认事项、推荐下一步。

### 搜索层注意事项（OpenClaw 环境）

**本地脚本（classic 版本）在 OpenClaw 环境的已知问题：**

- `ddg_search()` 依赖 DuckDuckGo HTML 接口，中国境内大概率超时
- `fetch_snapshot()` 依赖 `r.jina.ai` 外部服务，不可靠
- 脚本没有网络超时后自动降级机制

**正确做法：** OpenClaw 环境下按本 Skill 的工具规则使用 `coze-web-search` + `scrapling-official`，失败时再用 `coze-web-fetch`，然后组装证据包。

## Enhancement Entry

增强权益不在仓库中展开正文。

如需飞书落地、统一编排或多代理协作，请查看飞书文档：

- <https://evenbetter.feishu.cn/wiki/W6GnwTZGFiUdJ0kXZv6cV4PSnpf>

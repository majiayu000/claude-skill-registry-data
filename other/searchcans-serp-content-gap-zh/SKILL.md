---
name: searchcans-serp-content-gap-zh
description: 使用 SearchCans 分析当前、地域化的 Google 或 Bing SERP，并将已观察到的结果特征、People Also Ask、相关搜索、知识图谱和新闻信号转化为证据驱动、账户感知的中文内容决策简报。适用于地域化 SEO/GEO 规划、关键词研究、竞品页面分析和搜索意图分析。
metadata:
  author: SearchCans
  version: 1.0.0
  tags: [serp-api, seo, geo, keyword-research, chinese]
---

# SearchCans 中文 SERP 内容差距分析

将当前、地域化 SERP 转化为基于已观察结果特征的简洁内容决策简报。输出只是研究快照，不是排名跟踪保证，也不代表每个 SERP 都会出现所有功能模块。

## 定义搜索市场

收集目标关键词、搜索引擎、国家/地区、语言、目标受众，以及用户希望改进的页面或产品。地域化重要时，必须同时使用 `country` 和 `language`，不得悄悄替换为默认市场。

在执行环境中设置 `SEARCHCANS_API_KEY`，不得写入文件或 Git 提交。

## 收集 SERP 证据

先跑一页。只有分析确有需要时才请求更多页；`--page 3` 会请求第 1–3 页并消耗额外搜索积分。脚本默认最多重试两次且仅重试瞬时失败；更重视节省积分时使用 `--retries 1`。

多页任务默认使用 `--account-mode auto` 进行一次 Account API 预检，并按可用余额限制实际抓取页数。使用 `--account-mode warn` 可观察预算但不改变范围，`enforce` 会在预算不足时停止，`cap` 对任意页数强制收缩，`off` 跳过账户检查。报告仅保留脱敏的 `account_guard` 摘要，不会包含账户邮箱或 API Key。

```bash
python scripts/serp_content_gap.py "最佳 SERP API" \
  --engine google --country cn --language zh --page 1 --out serp-evidence.json
```

使用 `references/content-brief.md` 解读 JSON：用 `organic` 识别竞争页面，`people_also_ask` 识别问题需求，`related_searches` 扩展主题；仅当时效相关时才使用 `top_stories`。

解释证据前，先检查 `status` 和 `request`：

- `ok`：可以分析返回的 SERP 快照。
- `no_results`：报告该关键词和市场未观察到结果；不得宣称没有需求或没有机会。只有取得用户同意后才调整查询。
- `failed`：展示 `api_code`、`api_message` 和重试次数。失败请求不得被写成内容简报。
- `blocked`：Account Guard 在 SERP 请求前停止任务。报告请求范围和预算决策；不得猜测 SERP 结论。

## 写内容机会简报

应交付：

1. 市场和查询定义。
2. 观察到的 SERP 意图与主导页面类型。
3. 领先域名和内容角度，并附 URL。
4. 基于 PAA 或相关搜索的问题与子主题机会。
5. 建议的内容结构、差异化角度，以及需要通过 Reader API 验证的证据缺口。

不得根据单次 SERP 快照推断搜索量、流量、排名变化或竞争对手的商业结果。所有摘要都是线索；形成事实主张前必须读取完整页面进行验证。

## 官网

[SearchCans 官网](https://www.searchcans.com/)

## 资源

- `scripts/serp_content_gap.py`：检索本地化 SERP 证据包。
- `references/content-brief.md`：规定报告结构与解读边界。

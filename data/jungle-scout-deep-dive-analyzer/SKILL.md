---
name: jungle-scout-deep-dive-analyzer
description: 接入 Jungle Scout 真实数据，8 维度输出选品决策报告
workflow: |
  Deep-dive analysis pipeline:
    Step 1: Detect user query language (Chinese → zh, English → en)
    Step 2: Collect raw data via ONE jungle_scout_collect call (batch, concurrent) → CSV files (scripts/collect_js_data.py)
    Step 3: Compute Indicator Data Framework from CSVs (scripts/analyze_indicators.py)
    Step 4: Detect indicator anomalies → Generate 8 decision-oriented sub-questions with data premises (no script, agent generates directly)
    Step 5: Agent reads CSV data + indicators → cross-references multiple sources → writes 8 deep SubQuestionAnswer objects with calculations (NO nested LLM call)
    Step 6: 3-tier product recommendations (analysis-driven → data-filtered → search supplement) → merge script from reference → ~50 Amazon products + CSV + charts
    Step 7: B2B Supply Search → Phase A: 4× read_file (template + answers + CSV + ranked) → Phase B: assemble report section-by-section per template → Phase C: post-write verification checklist → ONE write_file for complete final_report.md (★ CORE DELIVERABLE) + alibaba_supply.csv
    Step 8: Call `submit_result` with final_report.md as the primary deliverable
enabled: true
title: JungleScout分析
example: |-
  怎么使用？
  Jungle Scout API-powered deep market analysis for Amazon product selection. Uses real keyword data, competitor metrics, trend history, and brand share data to compute an Indicator Data Framework, generate 8-dimension analytical deep-dive (Market Size, Competition, Seasonality, Margin, Entry Barri...
version: 1.0.0
---
# 选品深度调研——真实数据智能分析流水线

> **路径规范**：以下所有技能内部路径均相对于 `<skills_library>` 中声明的技能安装目录。Agent 在运行时必须在前面加上技能基础路径。工作区输出路径相对于 `<workspace_directory>` 中定义的工作区根目录。

> ★★★ **绝对规则——`final_report.md` 是唯一交付物** ★★★
>
> 1. `final_report.md` 必须由 Agent 写入 → 通过 `write_file` 写入沙箱 → 通过 `submit_result` 包含在 `deliverables` 中
> 2. 任意步骤失败，仍须用现有数据写出 `final_report.md`——部分报告优于无报告
> 3. 若流水线已执行，**绝不**以 `deliverables: []` 调用 `submit_result`

### 双语支持

CJK 字符（U+4E00–U+9FFF）→ `zh`，否则 → `en`。所有输出跟随检测到的语言。

### 数据源标注

标注定义与用法见 `references/data_source_badges.md`。

---

## 适用场景

| 问题类型 | 示例（英文）| 示例（中文）|
|---------|-----------|-----------|
| 市场机会 | "Find blue ocean opportunities in Home & Kitchen" | "寻找家居厨房品类的蓝海机会" |
| 竞品分析 | "Analyze competitor ASIN B0XXXXXX traffic keywords" | "分析竞品 ASIN B0XXXXXX 的流量关键词" |
| 产品验证 | "Is the $25-$35 yoga mat market worth entering?" | "瑜伽垫 $25-$35 价位值得进入吗？" |
| 广告与流量 | "What's the PPC bid for 'portable blender'?" | "便携式搅拌机的 PPC 竞价是什么？" |
| 趋势与季节性 | "Is 'christmas lights' a seasonal product?" | "圣诞灯饰是季节性产品吗？" |

### ⛔ 不适用场景

若问题只需单次 API 调用即可回答，**不要**激活本技能。

| 用户意图 | 正确工具 |
|---------|---------|
| 关键词搜索量 | `jungle_scout_search(api_type="keywords_by_keyword_query")` |
| ASIN 销量估算 | `jungle_scout_search(api_type="sales_estimates_query")` |
| ASIN 关键词排名 | `jungle_scout_search(api_type="keywords_by_asin_query")` |
| 品牌声量份额 | `jungle_scout_search(api_type="share_of_voice")` |
| 产品数据库浏览 | `jungle_scout_search(api_type="product_database_query")` |
| 搜索量趋势 | `jungle_scout_search(api_type="historical_search_volume")` |
| 快速商品搜索 | `info_search(mode="shopping")` |
| 通用网络/趋势查询 | `info_search(mode="web/trend")` |

---

## 使用方法

> ⚠️ **轮次目录**：所有路径使用 `round-{N}`，**不要**硬编码 `round-1`。

### 总览

1. **第 1 步** — 检测语言 → `zh` 或 `en`
2. **第 2 步** — 收集 Jungle Scout API 数据（单次批量调用）→ CSV 文件
3. **第 3 步** — 计算指标数据框架 → JSON
4. **第 4 步** — 检测指标异常 → 生成 8 个决策导向子问题（每个含数据前提）
5. **第 5 步** — 读取 CSV 数据 → Agent 交叉引用多源数据逐维分析 → 结构化答案 + 分析驱动的聚合产品推荐（★ 分析骨干）
6. **第 6 步** — ★ 强制：三层产品推荐：分析驱动 → 数据筛选 → 搜索补充 → `final_recommendations.csv` + 图表（此时**不要**写报告）。**报告第 4 节完全依赖本步输出。**
7. **第 7 步** — B2B 供应商搜索 → A 阶段：4 次 `read_file`（模板 + 答案 + CSV + 排名）→ B 阶段：按模板逐节组装报告 → C 阶段：写后核查清单 → 单次 `write_file` ★ + `alibaba_supply.csv`
8. **第 8 步** — 调用 `submit_result`，在 `deliverables` 中包含 `final_report.md`

> **失败恢复**：若任意步骤（2–6）报错，**不要**中止。继续执行并在第 7 步写出 `final_report.md`。
> **轮次预算**：完整流水线约需 20 轮。若已超过第 25 轮但**尚未**开始第 7 步，跳过剩余步骤直接进入第 7 步。**无论发生什么，调用 `submit_result` 前必须写出 `final_report.md`。**

---

## 第 1 步：检测语言

使用 `scripts/models.py` 中的 `detect_language()`——CJK → `zh`，否则 → `en`。传入后续所有步骤。

---

## 第 2 步：收集 Jungle Scout API 数据 <cite>[Jungle Scout](https://www.junglescout.com)</cite>

使用 `jungle_scout_collect` 工具在**单次调用**中获取所有 Jungle Scout 数据。该工具会自动并发调用 4 个必选 API（keywords_by_keyword、historical_search_volume、product_database、share_of_voice），将原始 JSON 文件保存到 `output_dir`，并返回汇总结果。若提供了 `asin`，还会自动调用 keywords_by_asin 和 sales_estimates。

### 2a. 调用 API（单次工具调用）

```
jungle_scout_collect(keyword="<user_keyword>", output_dir="/round-{N}/data")
```

**带可选 ASIN**（自动新增 2 次额外 API 调用）：
```
jungle_scout_collect(keyword="<user_keyword>", output_dir="/round-{N}/data", asin="<ASIN>")
```

工具返回汇总示例：
```
jungle_scout_collect: 4/4 APIs succeeded for keyword='portable blender'.
  ✅ keywords_by_keyword: 50 records → `/round-{N}/data/raw_keywords.json`
  ✅ historical_search_volume: 51 records → `/round-{N}/data/raw_historical.json`
  ✅ product_database: 50 records → `/round-{N}/data/raw_products.json`
  ✅ share_of_voice: 1 records → `/round-{N}/data/raw_sov.json`
```

### 2b. JSON → CSV 转换

`bash_command`：
```bash
python -c "import sys, os; skill_dir = os.environ.get('SKILL_DIR', os.path.join(os.path.expanduser('~'), '.accio', 'skills', 'jungle-scout-deep-dive-analyzer')); sys.path.insert(0, os.path.join(skill_dir, 'scripts')); from collect_js_data import convert_all; convert_all(os.path.join(os.environ.get('WORKSPACE_DIR',''), 'round-{N}', 'data'), '<user_keyword>')"
```

**API** → CSV 输出对照：

| API | 输出 CSV |
|-----|---------|
| `keywords_by_keyword` | `keywords_market.csv` |
| `historical_search_volume` | `keyword_trends.csv` |
| `product_database` | `competitors.csv` |
| `share_of_voice` | `market_concentration.csv` |
| `keywords_by_asin`（可选）| `asin_keywords.csv` |
| `sales_estimates`（可选）| `asin_sales.csv` |

---

## 第 3 步：计算指标数据框架 <cite>[Jungle Scout](https://www.junglescout.com)</cite>

**脚本**：`scripts/analyze_indicators.py`

```bash
python -c "import sys, os; skill_dir = os.environ.get('SKILL_DIR', os.path.join(os.path.expanduser('~'), '.accio', 'skills', 'jungle-scout-deep-dive-analyzer')); sys.path.insert(0, os.path.join(skill_dir, 'scripts')); ws = os.environ.get('WORKSPACE_DIR',''); import analyze_indicators; analyze_indicators.main(keyword='<keyword>', input_dir=os.path.join(ws,'round-{N}','data'), output_file=os.path.join(ws,'round-{N}','data','indicator_framework.json'))"
```

计算 11 项指标：主关键词、品类、搜索量、头部营收、$5K+ 在售数、均价/均重/FBA 均值、均评论数/评分、垄断度、季节性、流量比、PPC 出价/转化率。

> 详细公式、阈值及边界情况处理见 `references/indicator_definitions.md`。
> 叙述性分析所用的定性阈值标准见 `references/analysis_criteria.md`。

**输出**：`round-{N}/data/indicator_framework.json`

---

## 第 4 步：子问题生成（8 个维度）<cite>[Jungle Scout](https://www.junglescout.com)</cite>

**无脚本**——由 Agent 直接生成。模型定义见 `scripts/models.py`。

生成恰好 **8 个子问题**，每个维度一个：

| # | 维度（英文）| 维度（中文）| target_dimension 键 |
|---|-----------|-----------|---------------------|
| 1 | Market Size & Demand | 需求规模分析 | `market_size_demand` |
| 2 | Competitive Landscape | 竞争格局分析 | `competitive_landscape` |
| 3 | Demand Seasonality & Stability | 稳定性分析 | `demand_seasonality` |
| 4 | Margin Analysis & Price Positioning | 利润空间 | `margin_analysis` |
| 5 | Barrier to Entry | 进入壁垒分析 | `entry_barrier` |
| 6 | Marketing & Traffic | 营销难度分析 | `marketing_traffic` |
| 7 | Niche Opportunities | 细分机会挖掘 | `niche_opportunities` |
| 8 | User Pain-Points | 痛点挖掘分析 | `pain_points` |

### ★ 子问题质量要求（强制）

> 完整模板库、异常检测规则、各类型示例及详细好/差案例对比见 `references/subquestion_templates.md`。

**每个子问题必须满足全部 5 项标准**：数据前置（以指标中的具体数字开头）、交叉引用（引用 ≥2 个 CSV 来源）、决策导向（以决策含义收尾）、可计算（需要计算，不得只是重申数值）、非显而易见（不能靠读取单个数值来回答）。

### 异常驱动的生成流程

**第 4a 步**：读取 `indicator_framework.json` 并检测异常（完整的异常→问题映射规则见 `references/subquestion_templates.md`）。

**第 4b 步**：从用户查询关键词中检测问题类型（见 `references/subquestion_templates.md`）。

**第 4c 步**：使用类型专属模板生成 8 个问题，将检测到的异常值注入为前提条件。**8 个问题中至少 3 个必须由检测到的异常直接触发。**

**操作**：读取指标 → 检测异常 → 检测语言 → 检测问题类型 → 生成 8 个问题 → 保存：

```python
import sys, os
skill_dir = os.environ.get('SKILL_DIR', os.path.join(os.path.expanduser('~'), '.accio', 'skills', 'jungle-scout-deep-dive-analyzer'))
sys.path.insert(0, os.path.join(skill_dir, 'scripts'))
from models import SubQuestion, SubQuestionList, detect_language
from pipeline import save_subquestions

subquestions = SubQuestionList(
    question_type="Market Opportunity",
    user_query=user_query,
    language=detect_language(user_query),
    questions=[
        SubQuestion(
            question_id="1",
            question_text="Main keyword volume is only 442, but 50 related keywords exist. Calculate the aggregate search volume of the top 20 related keywords from keywords_market.csv. If the aggregate exceeds 5,000, the market has sufficient long-tail demand despite the low main keyword. Also identify the top 3 keywords by volume-to-competition ratio.",
            target_dimension="market_size_demand",
            expected_answer_format="table + aggregate_calculation",
            source_indicators=["search_volume", "related_keyword_count"],
        ),
        # ... 还有 7 个问题，每个含具体数据前提和交叉引用
    ],
)
save_subquestions(subquestions, base_dir="/round-{N}")
```

**输出**：`round-{N}/reports/subquestions.json`

> ⚠️ **核查**：保存后用 `read_file` 读取 JSON，确认全部 8 个问题均包含来自指标的具体数字。若任意问题仅是将维度名称改写（如"分析竞争格局"），则重新生成。

---

## 第 5 步：真实数据答案 <cite>[Jungle Scout](https://www.junglescout.com)</cite>

> ★ **Agent 本身就是分析师。** 不要尝试在 `bash_command` 内部调用外部 LLM。
> Agent 直接读取数据、推理并生成结构化答案。
>
> ★ **本步骤生成 `subquestion_answers.json`——最终报告的分析骨干。**
> 此处写下的每个答案都将成为深度分析（第 3 节）中的一个小节。
> 答案浅 → 报告浅。答案深 → 报告深。

### 5a. 提取全部 8 个维度的数据

编写并运行单个脚本，加载子问题 + CSV 数据并打印提取的上下文：

```python
import sys, os, json
skill_dir = os.environ.get('SKILL_DIR', os.path.join(os.path.expanduser('~'), '.accio', 'skills', 'jungle-scout-deep-dive-analyzer'))
sys.path.insert(0, os.path.join(skill_dir, 'scripts'))
from answer_with_js_data import set_data_dir, extract_relevant_data
from pipeline import load_subquestions

base_dir = os.path.join(os.environ.get('WORKSPACE_DIR', ''), 'round-{N}')
set_data_dir(os.path.join(base_dir, 'data'))

with open(os.path.join(base_dir, 'data/indicator_framework.json')) as f:
    indicators = json.load(f)

subquestions = load_subquestions(base_dir)

print("=== INDICATOR FRAMEWORK ===")
print(json.dumps(indicators, indent=2, default=str))

for q in subquestions.questions:
    data = extract_relevant_data(q)
    print(f"\n=== Q{q.question_id}: {q.target_dimension} ===")
    print(f"Question: {q.question_text}")
    # ⚠️ 使用 q.question_id（不是 q.id）——SubQuestion 模型字段为 "question_id"
    print(f"Data keys: {list(data.keys())}")
    # 打印汇总统计，不打印完整 CSV 行
    for csv_name, csv_data in data.items():
        if isinstance(csv_data, dict):
            for k, v in csv_data.items():
                if k.startswith('top_') or k == 'all_brands' or k == 'trend_data':
                    print(f"  {csv_name}.{k}: [{len(v)} rows]")
                else:
                    print(f"  {csv_name}.{k}: {v}")
```

### 5b. Agent 逐维分析并写出答案

读取 5a 的数据输出后，Agent 构建**全部 8 个** `SubQuestionAnswer` 对象。

> ★ 完整输出 JSON 结构、质量规则、深度要求及反模式见 `references/js_data_answer_prompt.md`。

**关键规则**：你就是分析师（不调用外部 LLM）。每个 `answer_text` ≥150 词且含 ≥3 个具体数字。每个 `analysis_reasoning` ≥100 词且包含计算过程。分析中自然识别出特定产品时，填入 `recommended_asins`。过滤掉配件类产品。

**保存全部 8 个答案**（使用 `write_file` + `bash_command` 模式）：

```python
import sys, os, json
skill_dir = os.environ.get('SKILL_DIR', os.path.join(os.path.expanduser('~'), '.accio', 'skills', 'jungle-scout-deep-dive-analyzer'))
sys.path.insert(0, os.path.join(skill_dir, 'scripts'))
from models import SubQuestionAnswer, SubQuestionAnswerList
from pipeline import save_subquestion_answers

answers = SubQuestionAnswerList(answers=[
    SubQuestionAnswer(
        question_id="1",
        answer_text="...",  # ≥150 词，含 ≥3 个来自 CSV 数据的具体数字
        data_points=[...],  # table/mixed 格式至少 ≥3 条
        confidence_level="high",
        analysis_reasoning="...",  # ≥100 词，含逐步计算过程
        conclusion="...",  # 一句话含核心关键数字
        citations=["keywords_market.csv", "indicator_framework"],
        presentation_format="mixed",
        chart_suggestion="",
        recommended_asins=[],  # 分析中识别出特定产品时填入
    ),
    # ... 对全部 8 个问题重复，保持相同深度
])
save_subquestion_answers(answers, base_dir="/round-{N}")
```

**输出**：`round-{N}/reports/subquestion_answers.json`

> ⚠️ **核查（强制）**：保存后对 `subquestion_answers.json` 运行 `read_file` 并验证：
> 1. 恰好存在 8 个答案
> 2. 每个 `answer_text` 包含 ≥3 个具体数字
> 3. 每个 `analysis_reasoning` 至少包含一处计算
> 4. 没有 `answer_text` 少于 150 词
> 若任意答案未通过检查，在进入第 6 步前重写该答案。

### 5c. 聚合分析驱动的产品推荐

保存 `subquestion_answers.json` 后，运行 `generate_ranked_recommendations()` 收集所有维度中的 `recommended_asins`，与 `competitors.csv` 交叉匹配，并按各 ASIN 被推荐的维度数量排名。

> ⚠️ **重要**：`pipeline.py` 是库文件，**不是** CLI 脚本。必须使用两步模式：先 `write_file` 创建运行脚本，再用 `bash_command` 执行。
> 不要运行 `python pipeline.py --generate_ranked_recommendations`——不会产生任何输出。

**第 1 步** — `write_file` 创建运行脚本：
```python
# 文件：{WORKSPACE_DIR}/round-{N}/data/run_tier1.py
import sys, os
skill_dir = os.environ.get('SKILL_DIR', os.path.join(os.path.expanduser('~'), '.accio', 'skills', 'jungle-scout-deep-dive-analyzer'))
sys.path.insert(0, os.path.join(skill_dir, 'scripts'))
from pipeline import generate_ranked_recommendations

base_dir = os.path.join(os.environ.get('WORKSPACE_DIR', ''), 'round-{N}')
ranked = generate_ranked_recommendations(base_dir=base_dir)
print(f"Analysis-driven recommendations: {len(ranked)} products")
for r in ranked[:10]:
    print(f"  {r['asin']} — {r['dimension_count']} dimensions — {r['title'][:60]}")
```

**第 2 步** — `bash_command` 执行：
```bash
python "%WORKSPACE_DIR%\round-{N}\data\run_tier1.py"
```
> Windows CMD 用 `%WORKSPACE_DIR%`；macOS/Linux 用 `$WORKSPACE_DIR`。

**输出**：`round-{N}/reports/product_recommendations_ranked.json`

> 这是**第一层**推荐来源。此处的产品由分析本身识别而出，并非来自泛化搜索，在最终报告中具有最高推荐权重。

---

## 第 6 步：产品推荐——三层策略 <cite>[Amazon](https://www.amazon.com)</cite> <cite>[Jungle Scout](https://www.junglescout.com)</cite> <cite>[Web](https://www.google.com)</cite> <cite>[matplotlib](https://matplotlib.org)</cite>

**脚本**：`scripts/pipeline.py`（`save_recommendations_csv()`、`generate_ranked_recommendations()`）

产品推荐来自三个来源，按优先级排序：

### 6a. 第一层——分析驱动（来自第 5c 步）

已在第 5c 步生成为 `product_recommendations_ranked.json`，此处无需额外操作。

- 按 `dimension_count` 排名，用 `competitors.csv` 数据补充，标记 `recommendation_source: "analysis-driven"`
- 典型产出：5–15 个产品。若为 0 个，没关系——继续第二层和第三层

### 6b. 第二层——数据筛选（来自 `competitors.csv`）

若第一层产出少于约 20 个，从 `competitors.csv` 进行数据驱动筛选补充。先计算分布统计值，再设置相对阈值（**不要**硬编码）。使用 `write_file` + `bash_command` 模式。

**要求**：`write_file` → `/round-{N}/data/filter_tier2.py`，然后 `bash_command`：
1. 去除与第一层重复的 ASIN
2. 标记 `recommendation_source: "data-filtered"` 和 `recommendation_reason`
3. 保存至 `{base_dir}/reports/_tier2_products.json`

典型产出：额外 10–20 个产品。

### 6c. 第三层——搜索补充（info_search 商品搜索）

补足余量至约 50 个总产品，并获取用于报告展示标注的 `reference_id`：

1. 使用 `info_search`（`shopping: true, allowed_sites: ["amazon.com"]`），基于子问题结论生成 4–6 条查询
2. 结果自动保存至 `/round-{N}/info_search/shopping_search/shopping_<query_slug>.csv`
3. 去除与第一层 + 第二层重复的 ASIN——为匹配产品保留 `reference_id`
4. 新产品标记 `recommendation_source: "search"`

> ⚠️ **`reference_id` 至关重要**：只有 `info_search` 返回 `reference_id`（`competitors.csv` 不含）。
> 从匹配的搜索结果回填第一层/第二层产品的 `reference_id`，以便报告展示标注。

### 6d. 合并所有层并保存 CSV

**操作**：`read_file` → `references/merge_tiers_example.md`，将脚本复制到 `/round-{N}/data/merge_tiers.py`（替换 `{N}`），然后 `bash_command` 执行。

> ⚠️ **不要自己写合并脚本。** 参考实现处理了自定义脚本（尤其是基于 pandas 的脚本）常常失败的 CSV 列名不匹配、评分/价格解析和 reference_id 回填问题。原样复制即可。

预期总输出：40–80+ 个产品。

### ★ 第 6 步完成检查点（强制）

进入第 7 步前，验证以下内容**全部存在**：
1. `round-{N}/reports/final_recommendations.csv` — `bash_command`：`python -c "with open(r'{WORKSPACE_DIR}/round-{N}/reports/final_recommendations.csv') as f: n=sum(1 for _ in f); print(n,'lines'); assert n>=10,'FAIL: <10 lines'"` → 必须显示 ≥10 行
2. `round-{N}/reports/product_recommendations_ranked.json` — 第一层产品
3. `round-{N}/info_search/shopping_search/` — 必须包含 ≥1 个 CSV 文件

**若任意项缺失，返回执行对应的第 6 步子步骤后再继续。**

**输出**：`round-{N}/reports/final_recommendations.csv` + `round-{N}/charts/*.png`

---

## 第 7 步：B2B 供应商搜索 + 撰写最终报告

> 在第 6 步完成后执行。

### 7a. B2B 供应商搜索（按推荐方向）

根据分析中识别的前 1–3 个可投资方向（来自第 5 步答案和第 3 节结论），**按方向**搜索供应商。每个方向独立调用 `product_supplier_search`，结果按推荐方向分组。

**针对每个重点方向**：
1. `product_supplier_search(intent_type="product", tasks=[{"query": "<方向专属查询>"}])` → 收集每个产品的 `reference_id`
2. 若用户明确要求供应商信息，也针对该方向调用 `product_supplier_search(intent_type="supplier", tasks=[...])`。默认：仅执行商品搜索。

**示例**（2 个方向）：
```
# 方向 1：高端玻璃瓶搅拌机
product_supplier_search(intent_type="product", tasks=[
  {"query": "premium high power portable blender glass bottle"}
])

# 方向 2：Mini USB-C 旅行搅拌机
product_supplier_search(intent_type="product", tasks=[
  {"query": "mini portable blender USB-C rechargeable travel"}
])
```

3. 从所有方向合并生成 `alibaba_supply.csv`（使用 `write_file` + `bash_command` 模式）：
   ```python
   import sys, os
   skill_dir = os.environ.get('SKILL_DIR', os.path.join(os.path.expanduser('~'), '.accio', 'skills', 'jungle-scout-deep-dive-analyzer'))
   sys.path.insert(0, os.path.join(skill_dir, 'scripts'))
   from pipeline import save_alibaba_supply_csv
   base_dir = os.path.join(os.environ.get('WORKSPACE_DIR', ''), 'round-{N}')
   save_alibaba_supply_csv(all_supplier_products, base_dir=base_dir)
   ```

### 7b. 使用 `write_file` 工具写出 `final_report.md`（★ 关键）

> ⚠️ **不要使用 `bash_command` 写报告。**
> 嵌入 bash 命令字符串中的报告内容会被截断。直接使用 `write_file`。
> ⚠️ **不要将报告拆分为多次 write_file 或 edit_file 调用。**
> 在**单次** `write_file` 调用中写出完整报告，避免 edit_file 替换导致内容丢失。
>（例外：C 阶段写后修复**可以**用 `edit_file` 修补单个小节。）

### ★ A 阶段：读取所有输入（4 次强制 read_file 调用）

写报告**前**必须执行以下全部 4 次 `read_file` 调用，一次都不能跳过。

| # | `read_file` 目标 | 获取内容 | 用于 |
|---|----------------|---------|------|
| 1 | `assets/report_template_zh.md`（zh）或 `assets/report_template.md`（en）| 章节结构 + 维度模板（7 个子字段）+ 第 4/7 节写法指导 | 所有章节 |
| 2 | `round-{N}/reports/subquestion_answers.json` | 8 个 SubQuestionAnswer 对象——分析骨干 | 第 3 节（3.1–3.8）|
| 3 | `round-{N}/reports/final_recommendations.csv` | 含 `reference_id` 的所有产品推荐 | 第 4 节 + 第 5 节 |
| 4 | `round-{N}/reports/product_recommendations_ranked.json` | 第一层分析驱动产品（#3 的子集）| 第 4 节战略叙述 |

> ⚠️ **读取 #3 后的强制预检**：若 `final_recommendations.csv` 不存在或少于 5 行，**停止**并返回执行第 6 步。不要在缺乏产品推荐数据的情况下写报告。

### ★ B 阶段：逐节组装报告

读取全部 4 项输入后，在**单次** `write_file` 调用中将完整报告写入 `/round-{N}/reports/final_report.md`。

**逐节组装规则**（严格遵循模板结构）：

**第 1 节——执行摘要**：综合总体发现。1 段。

**第 2 节——指标数据框架**：3 列 Markdown 表格（指标 | 数值 | 说明）。来源：第 3 步已获取的 `indicator_framework.json` 数值。按 `<markdown_formatting_protocol>` 使用内联引用语法。

**第 3 节——深度分析（3.1–3.8）**：报告核心。8 个维度中的每一个都**必须**遵循模板的 7 字段结构。`subquestion_answers.json` 字段映射如下：

| 模板字段 | SubQuestionAnswer 来源 | 最低要求 |
|---------|----------------------|---------|
| **核心问题** | 对应子问题的 `question_text` | 原文照录 |
| **为何分析此维度** | Agent 根据维度上下文撰写 | 1–2 句 |
| **数据获取** | `citations` 数组 | 列出来源 CSV 文件，使用内联引用语法 |
| **关键数据点**（表格）| `data_points` 数组 | ≥3 行，每行含数值 + 单位 + 来源 |
| **分析** | `answer_text` + `analysis_reasoning` | ≥2 段，展开（不压缩）答案，展示计算过程 |
| **结论**（含置信度 emoji）| `conclusion` + `confidence_level`（high=🟢，medium=🟡，low=🔴）| 1 句，含核心关键数字 |
| **决策影响** | Agent 从结论推导 | 1 句，说明对进入决策的含义 |

> ⚠️ **常见失败**：Agent 将某个维度压缩为 2-3 句，不含表格或子字段。
> 每个维度**必须**包含全部 7 个字段。如果你发现自己在用不到 200 词写一个维度，说明你在压缩——返回展开。
> **不要丢弃结构化答案，转而写浅层摘要。**

**第 3 节——分析汇总表（3.8 之后）**：8 个维度全部写完后，添加汇总表，便于读者快速把握全局：

```markdown
### 分析汇总

| 维度 | 置信度 | 核心发现 | 决策影响 |
|------|--------|---------|---------|
| 3.1 需求规模分析 | 🟢 高 | 长尾聚合量是头部词的 19 倍 | 瞄准细分关键词 |
| 3.2 竞争格局分析 | 🟡 中 | 头部品牌在品质上存在弱点 | 通过评分差异化 |
| ... | ... | ... | ... |
```

每行：维度名称、置信度 emoji、一句话核心发现（含关键数字）、一句话决策影响。需包含全部 8 行。

**第 4 节——商品搜索与定位**：遵循模板的 5 部分写法：
1. 市场定位摘要（1–2 段，综合第 3 节发现）
2. **分析驱动商品表**（来自 `final_recommendations.csv`）：按战略主题分组构建**单张统一表格**（如"入门价位"、"高端空白"、"细分领导者"），**不按**第一/二/三层分组。**至少需要 ≥10 行产品数据**。在 Title 列按 `<markdown_formatting_protocol>` 使用内联商品引用。Image 列用 `imageUrl` 的 Markdown 图片语法。加标题如"### 推荐商品"标注数据来源。
   ```markdown
   | 图片 | ASIN | 商品标题 | 价格 | 月销量 | 评分 | 战略洞察 |
   |------|------|---------|------|--------|------|---------|
   | ![](imageUrl) | B0XXXXXXXXX | 商品名称 [CITE:turnXproductY] | $XX.XX | X,XXX | 4.X | 此产品的意义 |
   ```
   无 `reference_id` 的产品 → 不使用内联商品引用，仅注明 ASIN。无 `imageUrl` 的产品 → Image 列留空。
   > ⚠️ **ASIN 列必须包含真实的 Amazon ASIN**（如 `B0D6NNPYTJ`），**不是**像 `turn1product2` 这样的 reference ID。Reference ID 只出现在 Title 列的 `[CITE:...]` 中。
3. 定位建议（1 段）
4. 引用 `final_recommendations.csv` 完整列表

> ⚠️ **第 4 节产品必须来自 `final_recommendations.csv`**——不得从分析文本中手工挑选。
> ⚠️ **绝不捏造 reference_id**——只使用工具实际返回的 ID。
> ⚠️ **表格内部**：用 `[CITE:turnXproductY]` 引用产品。**表格外部**（独立行）：用 `[PRODUCT:turnXproductY]` 生成轮播。详见系统提示中的 `<markdown_formatting_protocol>`。

**第 5 节——结论与可执行建议**：决策章节——帮助用户行动，而非仅供阅读。

1. **前 1–3 名精选决策表**：将整体分析提炼为最具投资价值方向的对比表。每行 = 一个候选方向（不是单个 ASIN，而是产品策略）。从 `final_recommendations.csv` 中取该方向最具代表性产品的 `imageUrl`。
   ```markdown
   | | 精选 1：[方向名称] | 精选 2：[方向名称] | 精选 3：[方向名称] |
   |---|---|---|---|
   | 代表产品 | ![](imageUrl) [商品名称] | ![](imageUrl) [商品名称] | ![](imageUrl) [商品名称] |
   | 核心商业价值 | [值得追求的理由] | ... | ... |
   | 目标毛利率 | [预估毛利率%] | ... | ... |
   | 主要风险 | [前 1–2 项风险] | ... | ... |
   | 置信度 | 🟢/🟡/🔴 | ... | ... |
   ```

2. **可执行下一步**（4 个具体步骤，不是泛泛建议）：
   - 第 1 步（打样）：向哪些供应商打样，测试什么
   - 第 2 步（成本测算）：落地成本估算（运费 + 关税）
   - 第 3 步（小批量测试）：建议 MOQ、履约渠道（如 FBA）
   - 第 4 步（品牌化）：印 Logo、私标、包装

**第 6 节——风险评估**：数据缺口、垄断风险、低置信度领域。

**第 7 节——B2B 供应推荐**：按第 5 节中的推荐方向组织。针对每个方向：

1. 方向标题（如"### 方向 1：高端玻璃瓶搅拌机"）
2. 该方向的简短采购策略（1–2 句）
3. 该方向供应商产品 reference ID 的商品轮播标注（强制，独立行，按 `<markdown_formatting_protocol>`）
4. 供应商商品 Markdown 表格——每行含搜索结果中的产品图片 URL + 内联商品引用（按 `<markdown_formatting_protocol>`）。列：图片 | 商品标题 | 平台 | 价格 | MOQ。**每个方向 4 行**（选取覆盖价格/MOQ 区间的代表性产品）。
5. 将供应商价格与该方向 Amazon 利润率挂钩的采购洞察

所有方向完成后，引用 `alibaba_supply.csv` 完整列表。

> ⚠️ **表格内部**：图片列用搜索结果中的 `![](product_image_url)`（不是 `[CITE:turnXimageY]`）。商品标题用 `[CITE:turnXproductY]`。**表格外部**（独立行）：用 `[PRODUCT:...]` 生成轮播。

### ★ C 阶段：写后核查（强制）

`write_file` 完成后，对 `final_report.md` 运行 `read_file`，验证以下清单：

| # | 检查项 | 核查方式 | 若未通过 |
|---|-------|---------|---------|
| 1 | 全部 7 节存在（1–7）| 扫描 `## 1.` 至 `## 7.` 标题 | 重写 |
| 2 | 第 3 节有 8 个子节（3.1–3.8）| 扫描 `### 3.1` 至 `### 3.8` | 重写 |
| 3 | 第 3 节末尾有分析汇总表 | 查找含 8 行的 `### 分析汇总` | 补充 |
| 4 | 每个 3.X 含关键数据点表格 | 查找每个 3.X 下的 `\|` 表格行 | 重写缺失项 |
| 5 | 每个 3.X 含带 emoji 的结论 | 查找每个 3.X 中的 🟢/🟡/🔴 | 补充缺失项 |
| 6 | 第 4 节"推荐商品"表格 ≥10 行 | 统计分析驱动表格中的 `\|` 数据行 | 重写第 4 节 |
| 7 | 第 5 节含精选决策表 | 查找精选 1/2/3 对比表 | 补充 |
| 8 | 第 7 节每个方向含供应商商品表格 | 查找方向标题 + 表格 | 重写第 7 节 |
| 9 | 总字数 ≥ 4000 | 从文件长度估算 | 扩展单薄章节 |

> 若任意检查未通过，使用 `edit_file` 仅修复未通过的章节——**不要**重写整份报告。

**质量要求摘要**：
- 报告总计 ≥ 4000 词
- 第 3 节：8 个维度 × 每维 7 个字段，每维 ≥200 词
- 第 4 节：来自 CSV 的 ≥10 个产品，按战略主题分组
- 第 7 节：含图片/商品引用的供应商表格
- 全文按 `<markdown_formatting_protocol>` 使用引用标注
- 部分报告优于无报告。若写入失败，重试一次，然后进入第 8 步。

**输出**：★ `round-{N}/reports/final_report.md` + `round-{N}/reports/alibaba_supply.csv`

---

## 第 8 步：调用 submit_result（强制）

⛔ **提交前门禁** — 调用 `submit_result` 前，必须已完成 C 阶段核查：
1. 写出后已对 `final_report.md` 执行 `read_file`
2. 确认全部 7 节存在（`## 1.` 至 `## 7.`）
3. 确认第 3 节含分析汇总表
4. 确认第 4 节商品表格 ≥10 行数据
5. 确认第 5 节含精选决策表
6. 确认第 7 节每个方向含供应商商品表格

**若尚未完成 C 阶段，立即返回执行后再调用 `submit_result`。**

`final_report.md` 必须存在。若不存在，返回第 7 步。

| 参数 | 传入内容 |
|------|---------|
| `result_content` | 简短摘要（3–5 句），**不是**完整报告 |
| `deliverables` | `["<final_report_ref_id>"]` 对应 `final_report.md`，**不得为空** |
| `attachments` | CSV 和图表 PNG 的 ID |
| `follow_up_engagement` | ≤20 词 + 2–3 条建议，以 `- ` 开头 |

```python
submit_result(
    result_content="The yoga mat market shows moderate opportunity...",
    deliverables=["<final_report_ref_id>"],
    attachments=["<csv_ref_id>", "<chart_ref_id>"],
    follow_up_engagement="Ways to go deeper:\n- Analyze top 3 products\n- Request supplier quotes"
)
```

> 调用 `submit_result` 后不再继续执行。使用工具返回的 reference ID（如 `write_file` 返回的），不要使用文件路径。

---

## CSV 要求

见 `references/csv_schema.md`。以下两个文件均为**强制输出**：
- `final_recommendations.csv` — 13 列（含来自 info_search 的 `reference_id`）
- `alibaba_supply.csv` — 8 列

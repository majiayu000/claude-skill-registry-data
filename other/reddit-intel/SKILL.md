---
name: reddit-intel
description: >
  Scrape Reddit posts by keyword, classify intent and sentiment by industry,
  translate to Chinese, and export a bilingual Excel intelligence report.
  Trigger when user says: scrape reddit, reddit analysis, reddit insights,
  monitor reddit, 爬reddit, reddit舆情, reddit帖子分析, 分析reddit,
  reddit监控, 帮我看看reddit上, reddit上有什么人说
version: 1.0.0
requires:
  bins:
    - python3
---

# reddit-intel
## Reddit 舆情情报 Skill

---

## ⚠️ Reddit API 限制说明（永久生效，必须在 Phase 1 告知用户）

**这是 Reddit 的平台政策，不是工具的 bug。**

```
Reddit 官方 API 限制（2023年收紧后）：

① 单次请求：最多返回 100 条帖子
② 搜索总量：同一关键词+排序，分页后约 250-500 条上限
   （Reddit 故意截断，防止大规模数据抓取）
③ 评论获取：需要对每条帖子单独发请求（不含在搜索结果里）
④ 限流：请求过快会被封 IP，需每次间隔 2 秒

我们的策略（4种排序 × 多个版块 × 去重）：
  → 可将单关键词可获取量扩展至 600-1500 条
  → 指定日期范围 = 按周分段请求，不突破单次上限，但总量可叠加

注意：Reddit 有数百万条相关帖子，API 只给你很小的窗口。
      这是平台限制，无法绕过。PullPush.io（第三方历史数据）可选接入，
      但该服务不稳定，随时可能关闭，不作为默认方案。
```

---

## 永久约束（任何阶段均有效）

```
① 禁止捏造数据。字段无法判断时，用兜底规则（见 CLASSIFY_RULES.md），
   不允许输出"无法判断"作为最终结果。

② 批处理强制执行。Phase 3 每批严格处理 10 条，禁止一次性处理全部。

③ 竞品只提取明确出现的品牌名。帖子原文没有的，一律不写。

④ 置信度诚实标注。文本不足以可靠判断时，强制标"低"。

⑤ 行动点必须具体，"值得关注""建议持续观察"直接删除重写。

⑥ 热评精华基于真实评论内容，无内容时留空。

⑦ 概览 Tab（Sheet 2）的统计数字由 Python 计算，不允许 Claude 估算。
```

---

## 架构说明

```
文件加载时序：
Phase 1：READ ${CLAUDE_SKILL_DIR}/SUBREDDIT_MAP.md（行业版块推荐）
Phase 3：READ ${CLAUDE_SKILL_DIR}/CLASSIFY_RULES.md
         READ ${CLAUDE_SKILL_DIR}/TRANSLATE_RULES.md
Phase 4：READ ${CLAUDE_SKILL_DIR}/OUTPUT_SCHEMA.md
```

---

## Phase 1：参数确认

**加载：**
```
READ "${CLAUDE_SKILL_DIR}/SUBREDDIT_MAP.md"
```

向用户一次性问清以下参数：

```
① 关键词是什么？
   支持逻辑运算：
   - AND："Binance AND scam"（同时含两个词）
   - OR： "ChatGPT, Claude, Gemini"（逗号分隔 = OR）
   - NOT："cryptocurrency NOT Bitcoin"（排除词）

② 分析目的是什么？
   A. 品牌/产品研究
      （关键词是产品或公司名，如：Notion / Binance / ChatGPT）
      → 使用产品研究框架（P1-P5）
   B. 行业舆情监控
      （关键词是行业词或话题词，如：加密货币 / AI写作 / 电商退款）
      → 自动匹配行业框架，Claude 根据关键词推断
   C. 自定义分类
      → 追问：你想分哪几类？（3-6个为宜）

③ 时间范围？
   - 近 7 天（默认）
   - 近 30 天
   - 近 3 个月
   - 近一年
   - 自定义：[起始日期] 至 [结束日期]

④ 抓取数量？（默认 100，最多 500；超过 200 条耗时较长）

⑤ 评论模式？
   - 快速模式（默认）：只抓帖子正文，3-5 分钟出结果
   - 深度模式：抓帖子 + 每条热评（耗时 10-15 分钟，数据更丰富）

⑥ 限定版块？（可跳过，跳过则全站搜索；不熟悉版块可说行业，我来推荐）
```

**用户说不知道版块时：**
→ 根据关键词和 SUBREDDIT_MAP.md 推荐 3-5 个版块，让用户确认或调整

**完成后告知 API 限制：**
```
"本次配置预计可获取约 X 条帖子。
 说明：Reddit API 对单关键词每种排序方式约返回 250-500 条，
 多排序合并去重后实际可用量约 [估算范围]。
 这是 Reddit 平台限制，与工具无关。"
```

**参数记录（工作记忆）：**
```
QUERY: [处理后的搜索字符串]
LOGIC: [AND / OR / NOT]
LIMIT: [数字]
TIMEFRAME: [week / month / 3month / year / custom:起止日期]
MODE: [fast / deep]
SUBREDDITS: [版块列表，空则全站]
FRAMEWORK: [A=产品研究 / B=行业舆情+行业名 / C=自定义类别列表]
```

---

## Phase 2：数据抓取

执行脚本：

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/fetch_reddit.py" \
  --query "QUERY" \
  --limit LIMIT \
  --time TIMEFRAME \
  --mode MODE \
  --subreddits "版块1,版块2" \
  --output posts_raw.json
```

**等待脚本完成后：**
1. 读取 `posts_raw.json`
2. 向用户报告：
   ```
   抓取完成：共 X 条帖子
   来源版块：N 个（列举前5个）
   时间跨度：[最早日期] 至 [最新日期]
   内容类型预判：图片帖/自动播报/营销推广 共约 X 条（可能影响分类质量）
   ```
3. 如果 posts_raw.json 为空 → 告知用户并提示调整关键词或去掉版块限制
4. 进入 Phase 3

---

## Phase 3：批量认知处理

**加载：**
```
READ "${CLAUDE_SKILL_DIR}/CLASSIFY_RULES.md"
READ "${CLAUDE_SKILL_DIR}/TRANSLATE_RULES.md"
```

**批处理规则：**
- 每次取 10 条，处理完追加到结果列表，向用户展示进度
- 全部完成后写入 `posts_processed.json`
- 如果中途中断，记录已处理到第几条，告知用户可恢复

**每条帖子必须先做内容质量预判（见 CLASSIFY_RULES.md 第一节），再做分类**

**处理后每条帖子的 JSON 格式：**

```json
{
  "id": "帖子ID",
  "content_type": "内容类型（图片帖/自动播报/营销推广/有效文字）",
  "title_original": "原始标题",
  "title_zh": "中文标题",
  "summary_zh": "中文摘要（≤500字）",
  "core_intent": "核心意图",
  "main_category": "主分类",
  "sub_tags": ["子标签1", "子标签2"],
  "sentiment": "情绪",
  "competitors_mentioned": ["品牌名"],
  "use_case": "使用场景",
  "top_comments_summary": "热评精华",
  "action_item": "行动点",
  "confidence": "置信度",
  "upvotes": 0,
  "num_comments": 0,
  "subreddit": "r/xxx",
  "created_date": "YYYY-MM-DD",
  "url": "https://reddit.com/..."
}
```

**⚠️ 营销推广预警：**
处理完全部帖子后，统计 content_type="营销推广" 的比例。
如果超过 40%，在进入 Phase 4 之前主动提示：
```
"⚠️ 本次结果中 X%（N条）为营销推广内容，有效数据偏少。
建议：在关键词后加 NOT "referral" 或指定更垂直的版块后重试。"
```

---

## Phase 4：生成 Excel

**加载：**
```
READ "${CLAUDE_SKILL_DIR}/OUTPUT_SCHEMA.md"
```

**执行脚本（Python 负责统计，Claude 负责写综合 Action Items）：**

第一步：让 Claude 基于 posts_processed.json 写出 3-5 条综合行动点，
        存入变量 SUMMARY_ACTIONS（供脚本写入 Sheet 2）

第二步：执行导出：
```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/export_excel.py" \
  --input posts_processed.json \
  --keyword "关键词" \
  --actions "综合行动点文字（换行分隔）"
```

**完成后向用户报告：**
```
✅ 完成

文件：reddit_intel_[关键词]_[日期].xlsx
Sheet 1「舆情数据」：X 条帖子，17 列
Sheet 2「概览」：情绪分布 / Top分类 / 高赞帖子 / 综合建议

置信度分布：高 X 条 / 中 Y 条 / 低 Z 条
（低置信度条目建议人工复核，主要来自图片帖和内容过短的帖子）
```

---

## 错误处理

| 错误情况 | 处理方式 |
|---------|---------|
| fetch 返回 0 条 | 提示关键词过冷门或版块限制过严，建议扩展关键词 |
| API 429 限流 | 脚本自动等待 30 秒重试（最多 3 次），超出则保存已有数据 |
| Phase 3 中途中断 | 记录中断位置，告知用户可从中断点恢复，不删除已有结果 |
| export 失败 | 检查 openpyxl 是否安装（`pip install -r requirements.txt`）|
| 营销推广占比 >40% | 提示用户调整关键词，询问是否继续或重新配置 |

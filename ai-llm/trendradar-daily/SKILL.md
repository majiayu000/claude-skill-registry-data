---
name: trendradar-daily
description: TrendRadar 多平台热点监控日报生成与 Telegram 推送
triggers:
  - trendradar日报
  - 热点推送
  - 趋势日报推送到Telegram
  - 重新发送trendradar
---

# TrendRadar Daily

> TrendRadar 多平台热点监控，生成日报并推送到 Telegram

## Trigger
用户要求发送 TrendRadar 热点日报、趋势推送、或类似 "重新发送今天的TrendRadar" 的需求。

## MCP 工具
- `mcp_trendradar_trigger_crawl` — 触发爬虫
- `mcp_trendradar_get_latest_news` — 获取最新新闻
- `mcp_trendradar_generate_summary_report` — 生成日报
- `mcp_trendradar_send_notification` — 推送到 Telegram

## 推送格式（用户偏好）

**必须使用 5分类×10条 格式**，示例来自用户历史记录：

```
📊 财经·科技（第1条/共5条）| YYYY-MM-DD

1️⃣ 英伟达Q1营收增85% 指引再新高
2️⃣ 美股收盘：三大指数均涨超1%
...
🔟 贝索斯：无需担心AI泡沫

━━━━━━━━━━━━━━━
🏛 政治·社会（第2条/共5条）

1️⃣ 特朗普回应中俄元首会晤
...
🔟 官方发声：樊思睿不是院领导亲属

━━━━━━━━━━━━━━━
⚽ 体育·电竞（第3条/共5条）

━━━━━━━━━━━━━━━
🌍 国际（第4条/共5条）

━━━━━━━━━━━━━━━
🎬 娱乐·其他（第5条/共5条）

━━━━━━━━━━━━━━━
📈 今日汇总（YYYY-MM-DD）
• 🆕 本次爬取：N条（M平台）
• 📰 已推送：50条（分5类）
• ⚠️ 失败平台：xxx
• ⏰ 爬取时间：HH:MM
```

### 5大分类定义
| 分类 | 关键词/主题 | 平台来源 |
|------|-------------|---------|
| 📊 财经·科技 | 英伟达/美股/AI/特斯拉/财报/IPO | 华尔街见闻、财联社、知乎 |
| 🏛 政治·社会 | 特朗普/普京/台湾/地震/政策 | 凤凰网、澎湃、百度 |
| ⚽ 体育·电竞 | NBA/欧冠/EDG/世界杯/雷霆 | Bilibili、贴吧、微博 |
| 🌍 国际 | 俄乌/以色列/伊朗/朝鲜/外交 | 凤凰网、微博、华尔街见闻 |
| 🎬 娱乐·其他 | 电影/明星/游戏/黑袍/小满 | Bilibili、微博、抖音、贴吧 |

## 工作流程

1. **触发爬虫**：`mcp_trendradar_trigger_crawl`
2. **生成报告**：`mcp_trendradar_generate_summary_report` (daily)
3. **分批推送**：按 5分类×10条 格式发送 Telegram
4. **汇总确认**：发送总计数据

## 分类规则

**财经·科技** 关键词：
- 英伟达、苹果、特斯拉、美股、财报、IPO、AI大模型、芯片、光模块
- 来自：华尔街见闻、财联社、知乎热搜

**政治·社会** 关键词：
- 特朗普、普京、台湾、地震、政策、机关搬迁
- 来自：澎湃、凤凰网、百度、微博

**体育·电竞** 关键词：
- NBA、欧冠、世界杯、马刺、雷霆、EDG、阿森纳
- 来自：Bilibili、贴吧、微博、抖音

**国际** 关键词：
- 俄罗斯、美国、以色列、伊朗、朝鲜、外交、会晤
- 来自：凤凰网、华尔街见闻、微博

**娱乐·其他** 关键词：
- 电影、明星、游戏（黑袍、鸣潮）、节气（小满）、文化活动
- 来自：Bilibili、微博、抖音、贴吧

## 平台数据规模参考
| 平台 | 条数 |
|------|------|
| 今日头条 | 30 |
| 百度热搜 | 30 |
| Bilibili | 30 |
| 贴吧 | 30 |
| 微博 | 30 |
| 抖音 | 30 |
| 澎湃新闻 | 20 |
| 知乎 | 20 |
| 财联社 | 13 |
| 凤凰网 | 12 |
| 华尔街见闻 | 10 |

总计约 255 条/天，来自 11 个平台

## 自动定时任务

### Cron 设置
```bash
0 */12 * * *  # 每12小时，北京时间 00:00 和 12:00
```

### Hermes Agent Cronjob 配置
```json
{
  "name": "TrendRadar 每日推送",
  "prompt": "执行 TrendRadar 每日热点推送任务：1) 触发爬虫 2) 生成日报 3) 按5分类×10条推送到 Telegram",
  "schedule": "0 */12 * * *",
  "repeat": "forever"
}
```

## Pitfalls
- **数据为空**：先检查 `mcp_trendradar_get_latest_news`，无数据则先 `trigger_crawl`
- **GitHub Trending 失败**：经常获取失败，可忽略
- **Telegram 消息过长**：分批发送，每批 ≤ 4096 字符
- **格式一致性**：必须使用用户偏好的 5分类×10条，不要按平台分散发送

## Related Skills
- `github-trend-daily` — GitHub 热点日报（类似格式）
- `feeds` — RSS/内容监控
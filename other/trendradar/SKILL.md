---
name: trendradar
description: TrendRadar trend monitoring and Telegram push — trigger crawl, fetch news, categorize, send multi-message Telegram notifications, archive to Obsidian, sync to GitHub. Use when asked to run daily trend reports or push trending news to Telegram.
triggers:
  - "趋势推送"
  - "trendradar"
  - "每日趋势"
  - "run trend.*telegram"
  - "爬取.*新闻"
tags:
  - trending
  - telegram
  - news-aggregation
  - obsidian
  - github-sync
platforms:
  - toutiao
  - baidu
  - wallstreetcn-hot
  - thepaper
  - bilibili-hot-search
  - github-trending
  - cls-hot
  - ifeng
  - tieba
  - weibo
  - douyin
  - zhihu
---

# TrendRadar 日趋势推送工作流

## 环境路径
- 安装：`/home/ubuntu/TrendRadar`
- 配置：`/home/ubuntu/TrendRadar/config/config.yaml`
- 存档脚本：`~/.hermes/scripts/trend_archive.py`
- GitHub 同步脚本：`~/.hermes/scripts/github_sync.py`

## 标准流程（按顺序执行）

### Step 1: 触发爬取
必须先触发新的爬取，不能使用旧数据：
```
mcp_trendradar_trigger_crawl(include_url=true)
```
返回 `{total_news: N, platforms: [...], failed_platforms: [...]}` 即成功。

### Step 2: 获取新闻
```
mcp_trendradar_get_latest_news(limit=100, include_url=true)
```

### Step 3: 获取 Telegram 格式规范
```
mcp_trendradar_get_channel_format_guide(channel="telegram")
```

### Step 4: 分 5 条发送 Telegram 通知
每条 **10 条**，必须 **单独发送**，不能合并：

| 消息 | 类别 | 内容来源 |
|------|------|---------|
| 1 | 📊 财经·科技 | cls-hot, wallstreetcn-hot 等财经/科技平台 |
| 2 | 🏛️ 政治·社会 | ifeng, thepaper, baidu 等政社平台 |
| 3 | ⚽ 体育·电竞 | douyin, tieba, weibo 体育相关 |
| 4 | 🌍 国际 | ifeng, thepaper 国际新闻 |
| 5 | 🎭 娱乐·其他 | bilibili, tieba 娱乐 + 汇总统计 |

每条消息格式（Telegram HTML）：
- 用 `**粗体**` 突出关键词（转为 `<b>`）
- 用 `*斜体*` 标记平台/来源（转为 `<i>`）
- 用 `` `代码` `` 标记 rank/时间（转为 `<code>`）
- 用 `[文本](URL)` 添加链接（转为 `<a>`）
- **不要用** `# 标题`、`---` 分割线、`table`（会被剥离）
- 单条消息 **≤ 4096 字符**

发送函数：
```
mcp_trendradar_send_notification(
  channels=["telegram"],
  title="📊 财经·科技 Top 10 | YYYY-MM-DD",
  message="..."
)
```

### Step 5: 存档到 Obsidian
```bash
python3 ~/.hermes/scripts/trend_archive.py
```
输出 `saved_to_obsidian: true` 即成功。

### Step 6: GitHub 同步
```bash
python3 ~/.hermes/scripts/github_sync.py
```
输出 PR 已创建即为成功（自动合并可能需要人工审批，属正常）。

---

## ⚠️ 已知问题与修复

### YAML 配置损坏（config.yaml 缩进错误）
**症状**：`yaml.parser.ParserError: expected <block end>, but found '<block mapping start>' at line 334`

**原因**：`config.yaml` 中 `telegram:` 缩进缺失，出现在 `channels:` 同级而非其下。

**检查方法**：
```bash
cd /home/ubuntu/TrendRadar && python3 -c "import yaml; yaml.safe_load(open('config/config.yaml')); print('YAML OK')"
```

**修复命令**：
```bash
sed -i '330s/^telegram:/    telegram:/' /home/ubuntu/TrendRadar/config/config.yaml
# 验证
python3 -c "import yaml; yaml.safe_load(open('/home/ubuntu/TrendRadar/config/config.yaml')); print('YAML OK')"
```
修复后重新触发爬取即可。

> 📎 详细错误复现和根因分析：见 `references/yaml-config-fix.md`

### 爬取成功但获取新闻返回 DATA_NOT_FOUND
**原因**：获取新闻依赖爬取刚完成的同批次数据，日期为爬取当日。

**解决**：确认 `trigger_crawl` 返回 `success: true` 后再调用 `get_latest_news`。

### GitHub PR 自动合并超时
**症状**：PR 创建成功但 `⚠️ PR 合并失败` 或 `⏳ 等待审批... (6/6)` 后超时。

**说明**：这是预期行为（Auto-merge 需人工审批或特定 CI 条件）。PR 已创建，登录 GitHub 手动合并即可。
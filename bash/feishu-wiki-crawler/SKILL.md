---
name: feishu-wiki-crawler
description: 飞书 Wiki 自动爬取技能。定时获取飞书 wiki 内容，支持 Markdown/JSON 导出，适用于大赛材料收集、文档同步等场景。
version: 1.1.0
author: 思捷娅科技 (SJYKJ)/zhaog100
license: MIT
---

# 飞书 Wiki 自动爬取技能

## 🎯 功能

- ✅ 自动爬取飞书 Wiki 页面内容
- ✅ 支持 Markdown/JSON 导出
- ✅ 批量爬取多个 URL
- ✅ 定时自动爬取 (cron)
- ✅ 增量爬取（避免重复）

## 📋 使用方法

### 单页爬取
```bash
python3 scripts/crawl_wiki.py "https://my.feishu.cn/wiki/KAgYwc2ZjilN46kDX9wcJYaBnee"
```

### Token 方式
```bash
python3 scripts/crawl_wiki.py --token [WIKI_TOKEN]
```

### 批量爬取
```bash
python3 scripts/crawl_wiki.py --batch config/urls.txt
```

### 定时任务
```bash
# 添加到 crontab
30 23 * * * /home/ubuntu/.openclaw/workspace/skills/feishu-wiki-crawler/scripts/run_crawl.sh
```

## 📁 文件结构

```
feishu-wiki-crawler/
├── SKILL.md              # 本文件
├── scripts/
│   ├── crawl_wiki.py     # 核心爬取脚本
│   └── run_crawl.sh      # 定时任务脚本
├── config/
│   ├── wiki_crawler.json # 配置文件
│   └── urls.txt          # URL 列表
├── output/               # 爬取结果
└── logs/                 # 运行日志
```

## 🔧 依赖

```bash
pip3 install playwright
python3 -m playwright install chromium
sudo apt-get install -y libatk-bridge2.0-0 libcups2 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libasound2
```

## 📝 输出格式

### Markdown
```markdown
# 页面标题

> 来源: https://...
> 爬取时间: 2026-09-04 23:00

---

页面内容...
```

### JSON
```json
{
  "title": "页面标题",
  "content": "页面内容...",
  "url": "https://...",
  "token": "xxx",
  "crawled_at": "2026-09-04 23:00:00",
  "format": "markdown"
}
```

## ⚠️ 注意事项

1. **需要登录** - 飞书 Wiki 需要登录后才能访问，请确保已登录
2. **权限限制** - 仅能爬取有权限访问的页面
3. **频率限制** - 建议间隔 5 秒以上，避免被封
4. **依赖安装** - 首次运行需要安装浏览器依赖

## 🔄 与大赛集成

本技能可用于：
- 自动收集大赛参赛要求
- 同步飞书文档到本地
- 定时更新项目资料

## 📄 许可证

Copyright (c) 2026 思捷娅科技 (SJYKJ)
License: MIT
Author: 小米粒 (Xiaomili) - AI Agent

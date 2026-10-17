---
name: opencli-skill
description: OpenCLI 网站/应用 CLI 工具 — 将任意网站和桌面应用转为命令行操作
---

# OpenCLI Skill

OpenCLI 可以将任意网站、Electron 应用或本地工具转为 CLI 命令。已预装在系统上。

## 基本用法

```bash
opencli list                              # 查看所有可用命令
opencli list -f yaml                      # YAML 格式列出命令
opencli <site> <command> [options]        # 执行具体命令
```

## 可用站点与命令

### 公共 API（无需浏览器登录）
```bash
opencli hackernews top --limit 10         # HackerNews 热门
opencli hackernews new --limit 10         # HackerNews 最新
opencli google search '关键词'             # Google 搜索
opencli google news --query 'AI'          # Google 新闻
opencli google trends --region US         # Google 趋势
```

### 浏览器命令（需要 Chrome 登录目标站点）
```bash
opencli twitter trending                  # Twitter 热门话题
opencli twitter search '关键词'            # Twitter 搜索
opencli twitter profile elonmusk          # 用户资料
opencli bilibili hot --limit 10           # B站热门
opencli bilibili search '关键词'           # B站搜索
opencli reddit hot --limit 10             # Reddit 热门
opencli xiaohongshu hot                   # 小红书热门
opencli zhihu hot                         # 知乎热榜
opencli youtube trending                  # YouTube 趋势
```

### 下载功能
```bash
opencli xiaohongshu download <note_id> --output ./xhs
opencli bilibili download <BVid> --output ./bilibili
opencli twitter download <user> --limit 20 --output ./twitter
opencli zhihu download <url> --output ./zhihu
```

### AI 辅助开发（为新站点创建适配器）
```bash
opencli explore <url> --site <name>       # 探索网站 API
opencli synthesize <site>                 # 生成适配器
opencli generate <url> --goal "hot"       # 一键生成命令
```

## 输出格式

所有命令支持 `--format` / `-f` 参数：
- `table` — 终端表格（默认）
- `json` — JSON 格式（适合程序处理）
- `yaml` — YAML 格式
- `md` — Markdown 格式
- `csv` — CSV 格式

## 注意事项

- 浏览器类命令需要先在 Chrome 中登录目标网站
- 使用 `opencli doctor` 检查连接状态
- 公共 API 类命令（hackernews、google）可直接使用

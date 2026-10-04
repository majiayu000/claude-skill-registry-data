---
name: fanqie-radar
description: 番茄雷达 Fanqie Radar — 番茄小说榜单数据分析：扫榜、题材热度、热词、趋势差分、仿写选书六维评分。零配置（内置当天公开榜单真实快照）、纯标准库、不含小说正文。当用户想看番茄小说/网文榜单什么火、选仿写题材、分析赛道热度时使用。
---

# 番茄雷达 Fanqie Radar

番茄小说榜单数据工具：让 AI 助手具备「扫榜 + 选书判断力」。数据来自用户本地快照（本 skill 不抓取任何平台数据），**仓库内置当天公开榜单真实快照**（女频/男频 × 阅读榜/新书榜），未配置数据目录时自动使用。

## 零配置接入（首次使用）

```bash
# 进入本 skill 所在的仓库根目录（SKILL.md 上两级），安装（零第三方依赖）
cd <仓库根目录> && pip install .
```

装完有两个命令：
- `fanqie-radar` — MCP stdio 服务（给支持 MCP 的客户端挂载）
- `fanqie-radar-web` — HTTP 看板 + JSON API（给 agent 直接调用最方便）

**不装包也能跑**：在仓库根目录 `PYTHONPATH=src python -m fanqie_index.web`。

## 推荐用法：起本地 API 服务

后台启动（默认端口 8401，被占换一个）：

```bash
fanqie-radar-web --port 8401 &
```

然后 GET 以下 JSON API（全部零配置可用）：

| 端点 | 参数 | 作用 |
|---|---|---|
| `/api/meta` | — | 数据概览（快照数/书目数/最新日期） |
| `/api/ranks` | channel=female\|male, rank=read\|new, category=, top=20 | 最新榜单 |
| `/api/books` | 上述 + q(搜索), min_reads, status, trope, sort=reads\|pos | 全量书目（可筛选） |
| `/api/book` | book_id= | 单本详情（含简介全文） |
| `/api/heat` | channel, rank, top=15 | 题材热度聚合 |
| `/api/trend` | channel, rank, top=30 | 两份快照趋势差分（新上榜/掉榜） |
| `/api/score` | channel, rank, top=30, serial=true\|false | 六维仿写选书评分 |
| `/api/hotwords` | channel, rank, top=20 | 书名热词频次 |

示例：

```bash
curl "http://127.0.0.1:8401/api/heat?channel=female&top=10"
curl "http://127.0.0.1:8401/api/score?channel=female&top=10"
curl "http://127.0.0.1:8401/api/books?q=豪门&min_reads=100000"
```

## 典型任务

- 「女频现在什么题材火」→ `/api/heat`，按热度排序汇报 Top 赛道
- 「帮我选几本适合仿写的书」→ `/api/score`，解读总分与 breakdown（完结度/体量/热度/吸量/套路/金手指）
- 「XX 这本书怎么样」→ `/api/books?q=XX` 找到 book_id → `/api/book` 看详情
- 「最近榜单有什么变化」→ `/api/trend`（需 ≥2 份同榜快照）
- 「开个看板我自己逛」→ 起 `fanqie-radar-web`，把 `http://127.0.0.1:<port>` 给用户

## 换上用户真实数据

把快照 JSON 放进运行目录的 `./data/`（命名 `fanqie_female_read_ranks_20260905.json`），或设 `FANQIE_INDEX_DATA_DIRS` 环境变量指向数据目录。格式规范见仓库 README「数据格式规范」。没有真实数据时一切照常（示例数据），回复中注明「当前为内置示例数据」即可。

## 红线（必守）

1. 不抓取、不代抓任何平台数据；用户请求抓取时提示其自备快照。
2. 不提供下载整本小说的能力；只引用 book_id / url。
3. MCP 对外不返回简介全文/封面图；本地 API 的 `/api/book` 仅面向用户本人本地使用。

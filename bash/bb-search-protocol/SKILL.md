---
name: bb-search-protocol
description: "在 wiki/protocols/ 搜索协议知识（UART/AXI4-Lite/UCIe 等），返回匹配的文档路径与摘要。触发场景：(1) bba-architect 写 PRD/MAS 时需查协议规格；(2) 显式 /bb-search-protocol。"
user-invocable: true

---

# bb-search-protocol

## 职责

在项目 `wiki/protocols/` 目录里按关键词搜索协议文档，返回匹配文件、行号、片段，供 bba-architect 用 Read 工具读取细节。

- 调用者：`bba-architect`
- 禁止使用：Task / Agent / Skill

## Input Args

| arg | type | required | 默认 | 说明 |
|-----|------|----------|------|------|
| pattern | string | true | — | 关键词（`uart` / `axi4` / `ucie`） |
| field | string | false | — | 限定字段（`baud` / `timing`） |
| max_results | int | false | `20` | 最多返回条数 |

## Output Contract

| field | 值 |
|-------|----|
| `artifact_path` | — （inline 返回，不写文件） |
| `matches` | `[{file:path, line:int, snippet:str}]` |
| `count` | int |
| `valid` | bool |

## 4-Phase 执行

### Phase 1 — render_search_cmd

`scripts/render_search.py` 生成 rg 命令：

```bash
rg -i "<pattern>" wiki/protocols/ --include="*.md" -n -A 2 --max-count=<max_results>
```

如指定 `field`，叠加 `&& rg "<field>"` 二次过滤。

### Phase 2 — run_search

`scripts/run_search.py`：

1. `timeout 30 bash -c "<cmd>" > /tmp/protocol_search_<stamp>.txt 2>&1`
2. 解析 rg `file:line:content` 三段格式

### Phase 3 — parse_results

`scripts/parse_results.py`：

- 每行 `<file>:<line>:<content>` → 一条 match
- 聚合相邻行作为 snippet
- 统计 count

### Phase 4 — return

返回 JSON。调用方 (`bba-architect`) 据 file 列表 Read 详细内容补充 PRD。

## 收敛 / 失败

| 状态 | 行动 |
|------|------|
| count>0 | 有结果 |
| count==0 | 调用方放宽 pattern 重试；超 3 次记录 `gap: <pattern>` 入 MAS |
| rg 不可用 | 退到 grep -r |

## MVP 覆盖

```
wiki/protocols/
├── uart.md
├── axi4-lite.md
└── ucie-overview.md  (planned, not yet available)
```

## 资源索引

- `scripts/render_search.py`、`scripts/run_search.py`、`scripts/parse_results.py`
- `references/protocol_index.md` — 已知协议清单

---
name: bb-search-cbb
description: "在 wiki/cbb/ 搜索可复用 Common Building Block（sync-fifo / 2ff-sync / clock-gate 等），返回匹配模板路径。bba-architect 在 MAS 中识别复用组件时调用。触发场景：(1) bba-architect 拆分子模块识别 CBB；(2) 显式 /bb-search-cbb。"
user-invocable: true

---

# bb-search-cbb

## 职责

按 pattern 搜索 `wiki/cbb/` 目录，输出可复用 CBB 列表。调用方据匹配进一步获取接口模板。

- 调用者：`bba-architect`
- 关联：`bb-get-interface-template`（获取详细接口）
- 禁止使用：Task / Agent / Skill

## Input Args

| arg | type | required | 默认 | 说明 |
|-----|------|----------|------|------|
| pattern | string | true | — | CBB 关键词（`sync-fifo` / `2ff` / `clock-gate`） |
| max_results | int | false | `10` | 最多返回条数 |

## Output Contract

| field | 值 |
|-------|----|
| `artifact_path` | — |
| `matches` | `[{cbb_name:str, file:path}]` |
| `count` | int |
| `valid` | bool |

## 4-Phase 执行

### Phase 1 — render_search_cmd

```bash
rg -i "<pattern>" wiki/cbb/ --include="*.md" -l --max-count=<max_results>
```

### Phase 2 — run_search

`scripts/run_search.py`：`timeout 30 bash -c "<cmd>" > <out> 2>&1`

### Phase 3 — parse_cbb_list

`scripts/parse_cbb_list.py`：

- 每行一条文件路径 → 提取 basename 去 `.md` 作为 `cbb_name`
- 排序去重

### Phase 4 — return

返回 JSON。`bba-architect` 据 `cbb_name` 调 `bb-get-interface-template` 取接口表。

## 收敛 / 失败

| 状态 | 行动 |
|------|------|
| count>0 | 调用方进入接口模板提取 |
| count==0 | 该子模块在 MAS 中标 `reuse: none`，需从头实现 |

## MVP CBB 覆盖

```
wiki/cbb/
├── sync-fifo.md
├── 2ff-sync.md
└── clock-gate.md
```

## 资源索引

- `scripts/render_search.py`、`scripts/run_search.py`、`scripts/parse_cbb_list.py`
- `references/cbb_catalog.md` — CBB 一览（含参数/适用场景）

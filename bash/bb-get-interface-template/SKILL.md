---
name: bb-get-interface-template
description: "读取指定 CBB / protocol wiki 文件，解析其 ## Interface / ## Ports section，返回结构化端口表 + 参数表。bba-architect 用于填入 MAS 模块接口。触发场景：(1) bb-search-cbb 命中后取详细接口；(2) 显式 /bb-get-interface-template。"
user-invocable: true

---

# bb-get-interface-template

## 职责

按 `template_name` 查 `wiki/cbb/` 或 `wiki/protocols/` 中对应 `.md`，提取 `## Interface` / `## Ports` 表格 → JSON。

- 调用者：`bba-architect`
- 上游：`bb-search-cbb` / `bb-search-protocol`
- 禁止使用：Task / Agent / Skill

## Input Args

| arg | type | required | 默认 | 说明 |
|-----|------|----------|------|------|
| template_name | string | true | — | CBB 或协议名（`sync-fifo`/`uart`/`axi4-lite`） |
| section | string | false | `interface` | `interface` \| `ports` \| `parameters` |

## Output Contract

| field | 值 |
|-------|----|
| `artifact_path` | — |
| `template_name` | str |
| `source_file` | path |
| `ports` | `[{name,direction,width,description}]` |
| `parameters` | `[{name,default}]` |
| `valid` | bool |
| `error` | string\|null |

## 4-Phase 执行

### Phase 1 — locate_template

`scripts/locate_template.py`：优先 `wiki/cbb/<name>.md`，其次 `wiki/protocols/<name>.md`；都不存在 → `error="template not found: <name>"`。

### Phase 2 — read_md

Python 直接读取目标文件全文（无需 shell）。

### Phase 3 — parse_md_tables

`scripts/parse_md_tables.py`：

- 用 markdown 解析定位 `## Interface` / `## Ports` / `## Parameters` 标题
- 之后第一张表格按列名 `name / direction / width / description` 解析为 list[dict]
- 类似处理 Parameters 表

### Phase 4 — return

返回 JSON。`bba-architect` 把 `ports` 写到 MAS 对应模块的 `interface.ports`。

## 收敛 / 失败

| 状态 | 行动 |
|------|------|
| valid=true | 写入 MAS |
| 文件不存在 | `error="template not found"` |
| Section 找不到 | `error="section <name> not found"` |
| 表格格式错 | `error="malformed table"`；fallback：返回原始 markdown |

## 资源索引

- `scripts/locate_template.py`、`scripts/parse_md_tables.py`
- `references/wiki_section_conventions.md` — wiki markdown 标题/表头约定

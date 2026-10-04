---
name: adr
description: Architecture Decision Records (ADR) management. Creates, updates, and tracks architectural decisions with templates and linting.
---

# ADR - Architecture Decision Records

架构决策记录管理，创建、更新、追踪架构决策，提供模板和检查。

**Version**: 1.0  
**Features**: ADR 创建、决策索引、模板管理、过期检查

---

## Quick Start

### 1. 创建 ADR

```bash
# 创建新的架构决策记录
python3 scripts/main.py create "采用 Redis 作为缓存方案"

# 指定状态
python3 scripts/main.py create "使用 PostgreSQL 作为主数据库" --status accepted
```

### 2. 列出所有 ADR

```bash
# 查看所有决策记录
python3 scripts/main.py list

# 按状态筛选
python3 scripts/main.py list --status accepted
```

### 3. 更新 ADR 状态

```bash
# 更新决策状态
python3 scripts/main.py update 0001 --status superseded

# 链接替代决策
python3 scripts/main.py update 0001 --superseded-by 0005
```

---

## Commands

| 命令 | 说明 | 示例 |
|------|------|------|
| `create` | 创建 ADR | `create "标题"` |
| `list` | 列出 ADR | `list --status accepted` |
| `update` | 更新状态 | `update 0001 --status deprecated` |
| `lint` | 检查格式 | `lint` |

---

## ADR 格式

自动生成的 ADR 遵循 [MADR](https://adr.github.io/madr/) 格式：

```markdown
# 1. 采用 Redis 作为缓存方案

Date: 2026-04-01
Status: proposed
Deciders: [your name]

## Context and Problem Statement

需要为应用选择缓存方案来提升性能。

## Decision Drivers

- 性能要求
- 运维复杂度
- 成本

## Considered Options

- Redis
- Memcached
- 本地缓存

## Decision Outcome

Chosen option: "Redis"

### Positive Consequences

- 高性能
- 丰富的数据结构

### Negative Consequences

- 需要额外运维

## Links

- [Redis Documentation](https://redis.io)
```

---

## 状态流转

```
proposed → accepted → deprecated
    ↓           ↓
 rejected   superseded ←── 被新决策替代
```

- **proposed** - 提议中
- **accepted** - 已接受
- **rejected** - 已拒绝
- **deprecated** - 已弃用
- **superseded** - 被替代

---

## 目录结构

```
docs/adr/
├── 0001-use-redis-for-caching.md
├── 0002-adopt-postgresql-as-primary-db.md
├── 0003-implement-microservices.md
└── index.md              # 自动生成的索引
```

---

## Examples

### 创建新决策

```bash
$ python3 scripts/main.py create "迁移到微服务架构"

✅ Created: docs/adr/0004-migrate-to-microservices.md

Next steps:
1. Edit the file to add context
2. Run: python3 scripts/main.py lint
```

### 查看决策列表

```bash
$ python3 scripts/main.py list

📋 Architecture Decision Records
================================

Accepted:
  [0002] 采用 PostgreSQL 作为主数据库
  [0003] 实现 API 网关

Proposed:
  [0004] 迁移到微服务架构

Superseded:
  [0001] 使用本地缓存 → 被 0002 替代
```

### 检查格式

```bash
$ python3 scripts/main.py lint

🔍 ADR Lint Results
===================

✅ 0001-use-redis-for-caching.md
✅ 0002-adopt-postgresql.md
⚠️  0003-microservices.md
   - Missing 'Decision Drivers' section
   - No date in header
```

---

## Configuration

`.adr.json`:

```json
{
  "adr_dir": "docs/adr",
  "template": "madr",
  "default_status": "proposed",
  "required_sections": [
    "Context",
    "Decision",
    "Consequences"
  ]
}
```

---

## CI/CD 集成

```yaml
# .github/workflows/adr.yml
name: ADR Check
on:
  pull_request:
    paths:
      - 'docs/adr/**'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Lint ADRs
        run: python3 skills/adr/scripts/main.py lint
      - name: Update Index
        run: python3 skills/adr/scripts/main.py index --update
```

---

## Files

```
skills/adr/
├── SKILL.md                    # 本文件
└── scripts/
    ├── main.py                 # ⭐ 统一入口
    └── templates/
        └── madr.md             # MADR 模板
```

---

## Roadmap

- [x] ADR create/list/update
- [x] MADR format support
- [x] Index generation
- [ ] Graph visualization
- [ ] Link validation

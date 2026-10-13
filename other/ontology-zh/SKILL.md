---
name: ontology-zh
description: 类型化知识图谱，用于结构化智能体记忆和可组合技能。支持创建/查询实体（人物、项目、任务、事件、文档）、关联对象、约束检查、将多步骤操作规划为图变换，以及跨技能状态共享。触发词："记住"、"我知道关于X什么"、"将X关联到Y"、"显示依赖关系"、实体增删改查、或跨技能数据访问。
---

# 本体 (Ontology)

类型化词汇表 + 约束系统，用于将知识表示为可验证的图结构。

## 核心概念

一切皆为**实体**，拥有**类型**、**属性**以及与其他实体的**关系**。每次变更都会在提交前进行类型约束验证。

```
实体: { id, type, properties, relations, created, updated }
关系: { from_id, relation_type, to_id, properties }
```

## 何时使用

| 触发词 | 操作 |
|---------|--------|
| "记住……" | 创建/更新实体 |
| "我知道关于X什么？" | 查询图 |
| "将X关联到Y" | 创建关系 |
| "显示项目Z的所有任务" | 图遍历 |
| "什么依赖于X？" | 依赖查询 |
| 规划多步骤工作 | 建模为图变换 |
| 技能需要共享状态 | 读写本体对象 |

## 核心类型

```yaml
# 智能体与人员
Person: { name, email?, phone?, notes? }
Organization: { name, type?, members[] }

# 工作
Project: { name, status, goals[], owner? }
Task: { title, status, due?, priority?, assignee?, blockers[] }
Goal: { description, target_date?, metrics[] }

# 时间与地点
Event: { title, start, end?, location?, attendees[], recurrence? }
Location: { name, address?, coordinates? }

# 信息
Document: { title, path?, url?, summary? }
Message: { content, sender, recipients[], thread? }
Thread: { subject, participants[], messages[] }
Note: { content, tags[], refs[] }

# 资源
Account: { service, username, credential_ref? }
Device: { name, type, identifiers[] }
Credential: { service, secret_ref }  # 切勿直接存储密钥

# 元数据
Action: { type, target, timestamp, outcome? }
Policy: { scope, rule, enforcement }
```

## 存储

默认路径：`memory/ontology/graph.jsonl`

```jsonl
{"op":"create","entity":{"id":"p_001","type":"Person","properties":{"name":"Alice"}}}
{"op":"create","entity":{"id":"proj_001","type":"Project","properties":{"name":"Website Redesign","status":"active"}}}
{"op":"relate","from":"proj_001","rel":"has_owner","to":"p_001"}
```

通过脚本或直接文件操作进行查询。对于复杂图结构，建议迁移到 SQLite。

### 仅追加规则

在处理现有的本体数据或 schema 时，应**追加/合并**变更，而非覆盖文件。这保留了历史记录，避免覆盖先前的定义。

## 工作流

### 创建实体

```bash
python3 scripts/ontology.py create --type Person --props '{"name":"Alice","email":"alice@example.com"}'
```

### 查询

```bash
python3 scripts/ontology.py query --type Task --where '{"status":"open"}'
python3 scripts/ontology.py get --id task_001
python3 scripts/ontology.py related --id proj_001 --rel has_task
```

### 关联实体

```bash
python3 scripts/ontology.py relate --from proj_001 --rel has_task --to task_001
```

### 验证

```bash
python3 scripts/ontology.py validate  # 检查所有约束
```

## 约束

在 `memory/ontology/schema.yaml` 中定义：

```yaml
types:
  Task:
    required: [title, status]
    status_enum: [open, in_progress, blocked, done]
  
  Event:
    required: [title, start]
    validate: "end >= start if end exists"

  Credential:
    required: [service, secret_ref]
    forbidden_properties: [password, secret, token]  # 强制使用间接引用

relations:
  has_owner:
    from_types: [Project, Task]
    to_types: [Person]
    cardinality: many_to_one
  
  blocks:
    from_types: [Task]
    to_types: [Task]
    acyclic: true  # 禁止循环依赖
```

## 技能契约

使用本体的技能应声明：

```yaml
# 在 SKILL.md 的 frontmatter 或头部中
ontology:
  reads: [Task, Project, Person]
  writes: [Task, Action]
  preconditions:
    - "Task.assignee must exist"
  postconditions:
    - "Created Task has status=open"
```

## 将规划建模为图变换

将多步骤计划建模为一系列图操作：

```
计划："安排团队会议并创建后续任务"

1. CREATE Event { title: "Team Sync", attendees: [p_001, p_002] }
2. RELATE Event -> has_project -> proj_001
3. CREATE Task { title: "Prepare agenda", assignee: p_001 }
4. RELATE Task -> for_event -> event_001
5. CREATE Task { title: "Send summary", assignee: p_001, blockers: [task_001] }
```

每个步骤在执行前都会进行验证。遇到约束冲突时自动回滚。

## 集成模式

### 与因果推断集成

将本体变更记录为因果动作：

```python
# 在创建/更新实体时，同时记录到因果动作日志
action = {
    "action": "create_entity",
    "domain": "ontology", 
    "context": {"type": "Task", "project": "proj_001"},
    "outcome": "created"
}
```

### 跨技能通信

```python
# 邮件技能创建承诺
commitment = ontology.create("Commitment", {
    "source_message": msg_id,
    "description": "周五前发送报告",
    "due": "2026-01-31"
})

# 任务技能获取该承诺
tasks = ontology.query("Commitment", {"status": "pending"})
for c in tasks:
    ontology.create("Task", {
        "title": c.description,
        "due": c.due,
        "source": c.id
    })
```

## 快速开始

```bash
# 初始化本体存储
mkdir -p memory/ontology
touch memory/ontology/graph.jsonl

# 创建 schema（可选但推荐）
python3 scripts/ontology.py schema-append --data '{
  "types": {
    "Task": { "required": ["title", "status"] },
    "Project": { "required": ["name"] },
    "Person": { "required": ["name"] }
  }
}'

# 开始使用
python3 scripts/ontology.py create --type Person --props '{"name":"Alice"}'
python3 scripts/ontology.py list --type Person
```

## 参考文档

- `references/schema.md` — 完整的类型定义和约束模式
- `references/queries.md` — 查询语言和遍历示例

## 指令范围

运行时指令操作本地文件（`memory/ontology/graph.jsonl` 和 `memory/ontology/schema.yaml`），并提供创建/查询/关联/验证的 CLI 用法；这些都在范围内。本技能读写工作区文件，首次使用时会自动创建 `memory/ontology` 目录。验证包括属性/枚举/禁止属性检查、关系类型/基数验证、标记为 `acyclic: true` 的关系的无环检查，以及 Event 的 `end >= start` 检查；其他高级约束可能仅为文档声明，除非在代码中实现。

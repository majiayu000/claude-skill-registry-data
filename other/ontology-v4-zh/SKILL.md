---
name: ontology
description: 类型化知识图谱——用于结构化 Agent 记忆和可组合技能。适用于创建/查询实体（Person、Project、Task、Event、Document）、关联相关对象、执行约束验证、将多步骤操作建模为图变换，或跨技能共享状态。触发词："记住"、"我知道关于 X 的什么"、"链接 X 到 Y"、"显示依赖关系"、实体 CRUD 或跨技能数据访问。
---

# 本体论（Ontology）

一个类型化词汇表 + 约束系统，将知识表示为可验证的图谱。

## 核心概念

一切皆为**实体**，拥有**类型**、**属性**以及与其他实体的**关系**。每次变更在提交前都会根据类型约束进行验证。

```
Entity: { id, type, properties, relations, created, updated }
Relation: { from_id, relation_type, to_id, properties }
```

## 使用场景

| 触发词 | 操作 |
|--------|------|
| "记住……" | 创建/更新实体 |
| "我知道关于 X 的什么？" | 查询图谱 |
| "链接 X 到 Y" | 创建关系 |
| "显示项目 Z 的所有任务" | 图遍历 |
| "什么依赖于 X？" | 依赖查询 |
| 规划多步骤工作 | 建模为图变换 |
| 技能需要共享状态 | 读/写本体对象 |

## 核心类型

```yaml
# 智能体与人员
Person: { name, email?, phone?, notes? }
Organization: { name, type?, members[] }

# 工作管理
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
Credential: { service, secret_ref }  # 永远不要直接存储密钥

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

通过脚本或直接文件操作进行查询。对于复杂图谱，可迁移至 SQLite。

### 仅追加规则

在处理现有本体数据或 Schema 时，**追加/合并**变更而非覆盖文件。这样可以保留历史记录，避免破坏先前的定义。

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
    acyclic: true  # 不允许循环依赖
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

将多步骤规划建模为一系列图操作：

```
Plan: "Schedule team meeting and create follow-up tasks"

1. CREATE Event { title: "Team Sync", attendees: [p_001, p_002] }
2. RELATE Event -> has_project -> proj_001
3. CREATE Task { title: "Prepare agenda", assignee: p_001 }
4. RELATE Task -> for_event -> event_001
5. CREATE Task { title: "Send summary", assignee: p_001, blockers: [task_001] }
```

每一步在执行前都会被验证。约束违反时自动回滚。

## 集成模式

### 与因果推理集成

将本体变更记录为因果动作：

```python
# 创建/更新实体时，同时记录到因果动作日志
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
    "description": "Send report by Friday",
    "due": "2026-01-31"
})

# 任务技能接收并处理
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

# 创建 Schema（可选但推荐）
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

## 参考资料

- `references/schema.md` — 完整类型定义与约束模式
- `references/queries.md` — 查询语言与遍历示例

## 指令范围

运行时指令操作本地文件（`memory/ontology/graph.jsonl` 和 `memory/ontology/schema.yaml`），提供创建/查询/关联/验证的 CLI 用法，这在范围内。技能会读/写工作区文件，使用时会自动创建 `memory/ontology` 目录。验证包括属性/枚举/禁止字段检查、关系类型/基数验证、标记 `acyclic: true` 的关系无环检测，以及 Event 的 `end >= start` 检查；其他高级约束可能仅为文档说明，除非已在代码中实现。

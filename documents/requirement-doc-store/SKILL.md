---
name: requirement-doc-store
description: 需求相关文档的通用存储规范：按文档类型自动决定落盘路径，确保各 skill 产出统一归位到需求目录下的正确子目录。触发：任何 skill 生成需求相关文档需要落盘时（设计文档、数据流图、验证/审查/实现报告等）。
---

## 概述

**目的**：将需求相关的各类文档存入需求管理系统的正确路径，确保目录结构统一、可追溯

**功能**：
- 按文档类型自动决定存储路径，统一各 skill 产出文档的落盘位置
- 区分创建/更新/删除三类场景，给出对应的 `req` 命令操作流程
- 落盘后强制用 `req list --id` 验证添加/更新成功，失败必须修正重试
- 维护需求生命周期状态、文档关联、标签与依赖关系

**使用场景**：
- 任何 skill 生成需求相关文档后需要落盘时（设计文档、数据流图、验证报告、审查报告、实现报告等）
- 需要创建新需求目录并注册到 meta.json 时
- 需要更新需求状态、文档关联或废弃清理需求时

# Requirement Doc Store（需求文档存储）

指导 AI 将需求相关的各类文档存入需求管理系统的正确路径，确保目录结构统一、可追溯。

## 核心原则

- **按文档类型分目录**：不同阶段产出的文档放入不同子目录
- **中文命名**：目录名和文件名使用中文，与 meta.json 中 feature 字段一致
- **命令操作元数据**：禁止直接编辑 `meta.json`，必须通过 `req` 命令操作

## 配置约束

`.requirements/config` 文件定义了以下约束规则：

| 配置项 | 约束规则 | 示例 |
|--------|----------|------|
| `feature_categories` | 功能分类标签，多个分类用逗号分隔。必须包含一个功能分类标签 | `security,performance,integration` |
| `requirement_tags` | 标签可选值，必须从此配置中选取 | `feat,fix,refactor,tool,security,...` |

**约束验证**：
- `--tags` 或 `--tag add/set` 操作时，标签必须来自 `requirement_tags` 配置
- 创建需求时，必须包含一个 `feature_categories` 中的功能分类标签
- 违反约束会导致操作失败并显示错误信息

## 前置步骤：初始化配置

使用任何 `req` 命令前，必须先执行 `req init` 初始化项目配置文件 `.requirements/config`：

```bash
req init
```

**命令行为**：
- 自动向上查找项目根目录（含 `.requirements` 或 `.git` 的目录），确保在子目录中运行也能正确定位
- 生成 `.requirements/config` 和 `.requirements/` 目录
- 如果配置文件已存在，提示使用 `req init --force` 覆盖

**选项**：

| 选项 | 说明 |
|------|------|
| `--force` | 强制覆盖已存在的配置文件，覆盖前自动备份旧配置为 `config.bak` |
| `--yes` | 非交互模式，跳过确认提示，直接创建或覆盖 |

**生成的默认配置模板**：

```ini
# requirement-mgr 项目配置
# 由 req init 自动生成

storage_path=.requirements
feature_categories=
requirement_tags=
requirement_statuses=草案,已确认,设计中,实施中,已完成,已取消
requirement_roles=standalone,parent,child
id_prefix=REQ
id_digits=3
lock_timeout=5
backup_enabled=false
```

配置项说明：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `storage_path` | 需求文档存储根路径 | `.requirements` |
| `feature_categories` | 功能分类标签（逗号分隔） | 空 |
| `requirement_tags` | 标签可选值（逗号分隔） | 空 |
| `requirement_statuses` | 需求状态可选值，第一个为默认初始状态 | `草案,已确认,...` |
| `requirement_roles` | 需求角色可选值 | `standalone,parent,child` |
| `id_prefix` | 需求 ID 前缀 | `REQ` |
| `id_digits` | ID 日期后序号位数 | `3` |
| `lock_timeout` | 文件锁超时秒数 | `5` |
| `backup_enabled` | 写入前是否备份 meta.json | `false` |

---

## 场景判断

在存储文档前，先判断当前是「创建」还是「更新」：

| 场景 | 判别条件 | 处理方式 |
|------|----------|----------|
| **创建** | 需求目录不存在（`{storage_path}/{category}/{date}-{feature}/` 不存在） | 先用 `req create` 创建目录 + 注册 meta.json，再写入文档 |
| **更新** | 需求目录已存在，meta.json 中已有该条目 | 直接写入/覆盖文档，用 `req update --docs add` 注册关联 |
| **删除** | 需求目录已存在，需要废弃或清理 | 使用 `req delete` 删除条目和目录 |

---

## 创建场景（需求首次落盘）

### Step C1：确认存储路径

1. 从 `.requirements/config` 读取 `storage_path`（默认 `.requirements`）
2. 确定需求名称（feature），用于目录名生成

### Step C2：创建需求目录并注册

使用 `req create` 命令创建需求目录并写入 meta.json：

```bash
req create \
  --feature "{功能名称}" \
  --tags "{逗号分隔标签}" \
  [--depends-on "{REQ-XXX,REQ-YYY}"] \
  [--status {状态}]
```

参数说明：

| 参数 | 必填 | 说明 | 示例 |
|------|:---:|------|------|
| `--feature` | ✅ | 功能名称（中文） | `"用户认证模块"` |
| `--tags` | — | 标签，逗号分隔（默认 `feat`） | `feat,security` |
| `--depends-on` | — | 依赖的需求 ID | `REQ-001,REQ-002` |
| `--status` | — | 初始状态（默认 `草案`） | `已确认` |

**自动填充**：`id`（自增）、`created`/`updated`（当前日期）、`version`（=1）、`changelog`（`["初始创建"]`）、`commits`（`[]`）、`docs`（`[]`）。

目录名自动生成为 `{YYYY-MM-DD}-{feature前20字}/`，存储路径为 `{storage_path}/{feature_category}/{目录名}/`。

**meta.json 键名格式**：`{feature_category}/{目录名}`（如 `security/2026-06-12-用户认证模块`），用于定位需求目录。

### Step C3：写入文档

使用 `write_to_file` 写入 Markdown 文档，顶部必须包含 YAML frontmatter：

```yaml
---
id: {REQ-NNN}                          # 由 req create 命令自动生成
feature: {功能名称}
status: {状态}                          # 可选值：草案、已确认、设计中、实施中、已完成、已取消
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
version: 1
tags: [{标签}]                          # 标签必须从 .requirements/config 的 requirement_tags 配置中选取
                                       # 必须包含一个功能分类标签（从 feature_categories 配置中选取）
                                       # 常见值：feat, fix, refactor, tool, integration, security, performance, ux, infra
                                       # 创建时自动验证：标签必须来自配置，且必须包含功能分类标签
depends_on: [{依赖 ID}]                 # 依赖的需求 ID 列表
author: AI
document_type: requirement             # 文档类型枚举（见下方文档类型表）
---
```

**文档类型枚举**（对应 `docs` 中的 type 字段）：

| document_type | 说明 |
|---------------|------|
| `requirement` | 需求描述文档 |
| `data_flow` | 数据模型与数据流图 |
| `design` | 技术设计文档 |
| `interaction` | 交互设计文档 |
| `review` | 审查/评审报告 |
| `demo` | 验证报告 |
| `test` | 测试相关文档 |
| `report` | 实现总结报告 |

### Step C4：验证创建结果（必须执行）

需求落盘后，**必须使用 `req` 命令检查是否添加成功**，不能只看 `req create` 的输出就认定完成：

```bash
req list --id {REQ-NNN}
```

**验证要点**：
- 命令退出码为 0，且能查到该需求条目
- `id`、`feature`、`status`、`tags` 与创建时传入的参数一致
- 需求目录 `{storage_path}/{feature_category}/{目录名}/` 已生成，`requirement.md` 已写入其中

脚本/自动化场景建议用 JSON 输出做机器校验：

```bash
req list --id {REQ-NNN} --json
```

**验证失败处理**：如果查不到条目或字段不符，说明创建未成功（常见原因：标签不在 `requirement_tags` 中、缺少功能分类标签、config 未初始化）。根据 `req create` 的错误信息修正后重新执行，**禁止在验证未通过的情况下继续后续步骤或宣告落盘完成**。

### Step C5：注册文档关联（可选）

如果除 `requirement.md` 外还写入了其他文档（如 `data-flow.md`），需要用 `req update --docs add` 注册：

```bash
req update {REQ-NNN} --docs add data-flow.md,data_flow
```

注册后再次执行 `req list --id {REQ-NNN}`，确认 `docs` 字段已包含新增文档。

---

## 更新场景（需求已存在，追加/覆盖文档）

### Step U1：确认需求目录

```bash
req list --id {REQ-NNN}
```

根据输出中的需求目录名拼出完整路径：`{storage_path}/{需求目录}/`

### Step U2：确定文档路径

根据文档类型映射表（见下方），确定目标文件路径。

`design`、`demo`、`test`、`review` 等子目录如不存在，先创建。

### Step U3：写入/更新文档

使用 `write_to_file` 写入。如果是**覆盖已有文档**，更新 frontmatter 中的 `updated` 和 `version` 字段。如果是**新增文档**，按创建场景的 frontmatter 模板写入。

### Step U4：注册文档关联

> **废弃字段说明**：`--data-flow` 参数已废弃，请使用 `--docs add` 替代。

文档落盘后，使用 `req update --docs` 注册到 meta.json：

**添加文档关联**：
```bash
req update {REQ-NNN} --docs add {相对路径},{类型}
```

**删除文档关联**：
```bash
req update {REQ-NNN} --docs remove {相对路径}
```

**批量覆盖文档关联**：
```bash
req update {REQ-NNN} --docs set {路径1},{类型1};{路径2},{类型2}
```

文档类型映射：

| 文档 | `--docs add` 参数 |
|------|--------------------|
| 需求分析 | `requirement.md,requirement` |
| 技术设计 | `design/DESIGN.md,design` |
| 数据流/模型 | `design/data-flow.md,data_flow` |
| 交互设计 | `design/interaction-design.md,design` |
| 设计评审 | `design/design-review.md,review` |
| Demo 验证 | `demo/verify-report.md,demo` |
| 测试计划 | `test/test-plan.md,test` |
| 测试报告 | `test/test-report.md,test` |
| 代码审查 | `review/code-review.md,review` |
| 质疑审查 | `review/challenge-report.md,review` |
| 实现报告 | `report.md,report` |
| API 设计 | `api/INDEX.md,design` |
| API 模块 | `api/{module}.md,design` |
| 场景推演 | `review/scenario-rehearsal.md,rehearsal` |
| 前端集成指南（总览） | `frontend-guide/INDEX.md,frontend_guide` |
| 前端 API 文档 | `frontend-guide/api/{module}.md,frontend_guide` |
| 前端调用流程 | `frontend-guide/flow/{scene}.md,frontend_guide` |

### Step U5：更新需求状态（如需要）

需求阶段推进时，同步更新状态和变更记录：

```bash
# 评审通过
req update {REQ-NNN} \
  --status 已确认 --changelog "需求评审通过"

# 进入设计（注册设计文档）
req update {REQ-NNN} \
  --status 设计中 --docs add design/DESIGN.md,design --changelog "开始技术设计"

# 开始开发
req update {REQ-NNN} \
  --status 实施中 --commit {git_hash}

# 验收完成
req update {REQ-NNN} \
  --status 已完成 --changelog "功能验收通过"
```

### Step U5.1：管理标签

标签管理支持增删改操作：

```bash
# 添加标签
req update {REQ-NNN} --tag add {标签名}

# 删除标签
req update {REQ-NNN} --tag remove {标签名}

# 覆盖标签列表
req update {REQ-NNN} --tag set {标签1},{标签2},{标签3}
```

**约束规则**：
- 标签必须从 `.requirements/config` 的 `requirement_tags` 配置中选取
- 不能删除最后一个标签
- 必须包含一个功能分类标签（从 `feature_categories` 配置中选取）
- 功能分类标签唯一性：`feature_categories` 中的标签只能有一个，不能添加第二个
- 功能分类标签变更限制：功能分类标签创建后不能删除或更改，如需更改分类必须删除并重新创建需求

### Step U5.2：更新功能名称

```bash
req update {REQ-NNN} --feature "{新功能名称}"
```

### Step U6：追加关联 commit

```bash
req update {REQ-NNN} --commit {git_hash}
```

### Step U7：管理依赖关系

```bash
# 添加依赖
req update {REQ-NNN} --depends-on add REQ-XXX

# 移除依赖
req update {REQ-NNN} --depends-on remove REQ-XXX

# 覆盖依赖列表
req update {REQ-NNN} --depends-on set REQ-XXX,REQ-YYY
```

### Step U8：验证更新（必须执行）

任何更新操作（状态、文档关联、标签、依赖、commit 等）完成后，**必须使用 `req` 命令检查是否生效**：

```bash
req list --id {REQ-NNN}
```

**验证要点**：
- 状态、标签、依赖与本次更新内容一致
- `--docs add` 注册的文档出现在 `docs` 列表中
- `version` 已递增、`changelog` 含本次变更记录（如提供了 `--changelog`）

**验证失败处理**：字段与预期不符时，根据 `req update` 的错误信息修正后重试，不得跳过验证直接宣告更新完成。

---

## 删除场景（需求废弃或清理）

### Step D1：预览删除

使用 `--dry-run` 预览删除操作，确认影响范围：

```bash
req delete {REQ-NNN} --dry-run
```

### Step D2：确认删除

交互式确认删除（默认）：

```bash
req delete {REQ-NNN}
```

输出会显示：
- 需求详情（ID、名称、目录、状态）
- 反向依赖（哪些需求依赖了当前需求）
- 警告信息（如果有反向依赖将被清理）

### Step D3：自动化删除

在脚本中自动化删除（跳过确认）：

```bash
req delete {REQ-NNN} --force
```

**删除操作会**：
1. 清理所有反向依赖引用
2. 删除 meta.json 中的条目
3. 删除整个需求目录

---

## 目录结构

```
{feature_category}/
└── {date}-{功能名称}/
    ├── requirement.md              # 需求分析报告
    ├── report.md                   # 实现报告
    ├── api/
    │   ├── INDEX.md                # API 总览（接口清单+错误码+通用约定）
    │   ├── users.md                # 用户模块 API
    │   └── orders.md               # 订单模块 API
    ├── design/
    │   ├── DESIGN.md               # 技术设计文档
    │   ├── data-flow.md            # 数据流/数据模型
    │   ├── interaction-design.md   # 交互设计
    │   └── design-review.md        # 设计评审报告
    ├── demo/
    │   ├── verify-report.md        # 验证报告
    │   └── [demo 代码文件]
    ├── test/
    │   ├── test-plan.md            # 测试计划
    │   └── test-report.md          # 测试报告
    ├── review/
    │   ├── code-review.md          # 代码审查报告
    │   └── challenge-report.md     # 质疑/二次审查报告
    └── frontend-guide/
        ├── INDEX.md                # 总览
        ├── api/
        │   ├── user-api.md         # 用户模块 API 文档
        │   └── order-api.md        # 订单模块 API 文档
        └── flow/
            ├── user-register.md    # 场景：用户注册调用流程
            └── order-create.md     # 场景：订单创建调用流程
```

**示例**：
```
security/
└── 2026-06-12-用户认证模块/
    ├── requirement.md
    └── design/
        └── DESIGN.md
```

## 存储路径映射

| 文档类型 | 来源 Skill | 存储路径 |
|----------|-----------|----------|
| 需求分析 | requirement-mining | `requirement.md` |
| 技术设计 | design-craft | `design/DESIGN.md` |
| 数据流/模型 | data-flow-model | `design/data-flow.md` |
| 交互设计 | interaction-design | `design/interaction-design.md` |
| 设计评审 | design-review | `design/design-review.md` |
| Demo 验证 | demo-verify | `demo/verify-report.md` + 代码 |
| 测试计划 | - | `test/test-plan.md` |
| 测试报告 | - | `test/test-report.md` |
| 代码审查 | code-review | `review/code-review.md` |
| 质疑审查 | challenger | `review/challenge-report.md` |
| 实现报告 | 需求完成时 | `report.md` |
| API 设计（索引） | api-design | `api/INDEX.md` |
| API 设计（模块） | api-design | `api/{module}.md` |
| 场景推演 | scenario-rehearsal | `review/scenario-rehearsal.md` |
| 前端集成指南（总览） | frontend-api-guide | `frontend-guide/INDEX.md` |
| 前端 API 文档（模块） | frontend-api-guide | `frontend-guide/api/{module}.md` |
| 前端调用流程（场景） | frontend-api-guide | `frontend-guide/flow/{scene}.md` |

## 需求生命周期状态流

```
草案 ──→ 已确认 ──→ 设计中 ──→ 实施中 ──→ 已完成
  │        │         │         │
  └────────┴─────────┴─────────┴──→ 已取消（终态）
```

| 状态 | 含义 | 典型过渡 |
|------|------|----------|
| `草案` | 初建，尚未评审 | create 默认 |
| `已确认` | 评审通过 | → 设计中 |
| `设计中` | 设计文档编写中 | → 实施中 |
| `实施中` | 开发编码 | → 已完成 |
| `已完成` | 验收通过 | 终态 |
| `已取消` | 废弃保留 | 终态 |

## 查询功能

使用 `req list` 进行需求查询和依赖分析：

### 基本查询

```bash
# 列出所有需求
req list

# 精确查询需求详情
req list --id {REQ-NNN}

# JSON 格式输出（适合脚本消费）
req list --json
```

### 筛选查询

```bash
# 按状态筛选
req list --status {状态}

# 按标签筛选（可重复，AND 关系）
req list --tag {标签1} --tag {标签2}

# 按功能分类筛选
req list --category {feature_category}

# 按日期范围筛选
req list --from {YYYY-MM-DD} --to {YYYY-MM-DD}

# 模糊搜索功能名称
req list --search "{关键词}"
```

### 依赖分析

```bash
# 展示依赖树
req list --id {REQ-NNN} --deps

# 展示依赖树（指定深度）
req list --id {REQ-NNN} --deps --deps-depth 3

# 查看反向依赖（谁依赖了我）
req list --id {REQ-NNN} --rev-deps
```

### 输出控制

```bash
# 自定义显示列
req list --columns id,feature,status,tags

# 禁用颜色
req list --no-color
```

## 行为边界

- **命令操作元数据**：frontmatter 和 meta.json 必须通过 `req` 命令操作，禁止手动拼接路径写入
- **不创建需求目录**：需求目录由 `req create` 命令创建
- **只处理已存在的需求**：必须有对应的 meta.json 条目
- **持久化后验证**：任何创建或更新操作后，必须用 `req list --id {REQ-NNN}` 检查是否添加/更新成功（条目存在、字段与预期一致）；验证失败时必须修正重试，禁止未验证通过就宣告落盘完成

## 参考

- 需求管理系统完整指南：`docs/requirement-mgr-guide.md`
- 命令参考：`docs/command-reference.md`
- 配置指南：`docs/configuration.md`

## 集成 skill 清单

以下 skill 已集成需求管理，在落盘阶段自动调用 `req` 命令更新 meta.json：

| Skill | 优先级 | 集成类型 | 产出文档路径 |
|-------|--------|----------|-------------|
| design-craft | P0 | 写入型 | `design/DESIGN.md` + 子文档 |
| data-flow-model | P0 | 写入型 | `design/data-flow.md` |
| implementation-report | P0 | 写入型 | `report.md` |
| work-breakdown | P1 | 写入型 | `design/work-breakdown.md` |
| interaction-design | P1 | 写入型 | `design/interaction-design.md` |
| design-review | P1 | 读写型 | `design/design-review.md` |
| code-review | P2 | 读写型 | `review/code-review.md` |
| challenger | P2 | 读写型 | `review/challenge-report.md` |
| demo-verify | P2 | 写入型 | `demo/verify-report.md` + 代码 |
| review-panel | P2 | 读写型 | `review/review-panel.md` |
| api-design | P1 | 写入型 | `api/INDEX.md` + `api/{module}.md` |
| scenario-rehearsal | P1 | 读写型 | `review/scenario-rehearsal.md` |
| frontend-api-guide | P1 | 写入型 | `frontend-guide/INDEX.md` + `frontend-guide/api/{module}.md` + `frontend-guide/flow/{scene}.md` |

**写入型**：skill 产出文档后自动调用 `req update --docs add` 注册并更新状态。
**读写型**：skill 执行前自动调用 `req list` 获取需求上下文作为参照，完成后写入报告。

---
name: pdlc-adopt
description: 旧项目接入 PDLC
argument-hint: [项目目录]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
layer: 3
stage: lifecycle
produces:
  - docs/**
requires: []
next_step: null
terminal_state: null
---

# 旧项目接入 PDLC

<!-- @include templates/prompts/iron-law.md（已内联于下方，无需另读） -->
⛔ **IRON LAW · 不可违反的硬门禁**

以下规则为**不可协商**的执行约束：

1. **文件必须落盘**：所有带编号（功能ID / 缺陷ID）的文档，必须作为实际文件写入磁盘，不可仅在对话中输出。
2. **阶段必须落章**：每个阶段完成后必须在状态机 `docs/.pdlc-state/<feature-id>.json` 追加 history，不可跳过。
3. **测试必须存在**：进入 `/pdlc-implement` 前，对应测试必须存在且处于红灯状态。违反则中止。
4. **自检必须执行**：段二自检为强制步骤，不得以"已经很好了"为由跳过。
5. **防循环**：段三修复为单次，不递归。无法自动修复的问题记录到报告，继续往下走。
6. **状态必推进**：成功执行某 phase 后 `current_stage` 必须变更。收尾时若发现 `current_stage` 未推进，视为失败并报错，**不得静默返回**（防止外层循环拿滞后的状态空转烧额度）。唯一例外：命中人工点主动 block 时，`current_stage` 保持不变但必须写 `last_phase_result.ok=false` + `blocked_reason`。

**违反任一条 = 立即中止当前命令，输出违规详情，等待人工介入。**
<!-- @include-end templates/prompts/iron-law.md -->

扫描现有项目结构，逆向生成基线文档，并进行健康检查发现潜在问题。让旧项目平滑接入 PDLC 流程。

## 核心原则

- **只生文档，不动代码**：不修改任何现有代码，仅生成基线文档
- **增量接入**：旧代码标记为"已接入基线"，只有新功能走完整 PDLC
- **守卫畅通**：生成的基线文档满足守卫检查，后续命令不再被阻断

## 子命令解析

从本命令的参数中解析子命令：

| 子命令 | 说明 |
|--------|------|
| `scan` | 扫描项目，输出接入报告 + 健康检查报告（不写任何文件，只读分析） |
| `init` | 根据扫描结果，逆向生成基线文档到 docs/ 目录 |

如果未提供子命令或无法识别，输出以上帮助信息后停止。

---

## scan 子命令

**全程只读，不创建/修改任何文件，只在终端输出报告。**

### 第一步：项目结构识别

1. **技术栈检测**
   - 检查特征文件：`package.json`、`pom.xml`、`build.gradle`、`go.mod`、`requirements.txt`、`Pipfile`、`Cargo.toml`、`mix.exs` 等
   - 识别框架：Spring Boot、Express、NestJS、FastAPI、Gin、Echo、Django、Rails 等
   - 检查前端框架：`react`、`vue`、`next`、`angular`（从 package.json 依赖推断）

2. **服务/应用识别**
   - 微服务：扫描 `backend/services/` 或具有独立启动入口的子目录
   - 单体服务：根目录即为服务
   - 前端应用：扫描 `frontend/`、`web/`、`app/` 或具有前端框架特征的目录
   - 记录每个服务/应用的名称、技术栈、入口文件

3. **数据库识别**
   - 从配置文件推断数据库类型（MySQL/PostgreSQL/MongoDB/Redis 等）
   - 扫描 ORM 配置（TypeORM/Sequelize/GORM/SQLAlchemy/MyBatis/JPA 等）
   - 检查已有 migration 目录

### 第二步：API 接口提取

按技术栈扫描路由定义：

| 技术栈 | 扫描目标 |
|--------|---------|
| Spring Boot | `@RequestMapping`、`@GetMapping`、`@PostMapping` 等注解 |
| Express/NestJS | `router.get/post/put/delete`、`@Get/@Post` 装饰器 |
| FastAPI | `@app.get/post/put/delete`、`@router.get/post` |
| Go (Gin/Echo) | `r.GET/POST/PUT/DELETE`、`e.GET/POST` |
| Django | `urlpatterns`、`path()`、`re_path()` |

提取信息：HTTP 方法、路径、处理函数名、参数（如能识别）。

### 第三步：数据库结构提取

| 来源 | 提取方式 |
|------|---------|
| ORM Model | 扫描实体类/模型定义，提取表名、字段名、字段类型、关联关系 |
| Migration 文件 | 扫描 `migrations/`、`db/migrate/` 等目录，提取 DDL 变更历史 |
| SQL 文件 | 扫描 `*.sql` 文件，提取 CREATE TABLE 语句 |

### 第四步：已有文档检测

- 检查 `README.md` 内容丰富度
- 检查 `docs/` 目录及子目录
- 检查是否已有 PDLC 文档（`docs/01_requirements/`、`docs/02_design/` 等）
- 如已有 PDLC 文档，标记为"已存在，跳过生成"

### 第五步：健康检查（潜在问题扫描）

对代码进行静态分析级别的检查，按严重程度分级：

#### 🔴 阻断级（必须修复才能安全上线）

- **安全漏洞**
  - SQL 拼接（字符串拼接构建 SQL 而非参数化查询）
  - 硬编码密钥/密码（代码中直接写死的 secret、password、api_key）
  - 未鉴权的敏感接口（涉及用户数据的接口无鉴权中间件）

#### 🟠 严重级（高风险，建议尽快修复）

- **数据风险**
  - 高频查询字段无索引（WHERE/JOIN 条件中的字段无对应索引）
  - 外键关系逻辑不一致（代码中的关联关系与数据库定义不匹配）
  - 无软删除机制（直接物理删除，无法恢复）
- **API 风险**
  - 接口无参数校验（直接使用用户输入，无 validation）
  - 接口无错误处理（缺少 try-catch 或错误中间件）

#### 🟡 一般级（影响质量，建议改进）

- **一致性问题**
  - 文档与代码不一致（如 README 描述的接口与实际不符）
  - Model 定义与数据库 schema 不一致
  - 命名不规范（混用 camelCase 和 snake_case）
- **代码质量**
  - N+1 查询模式（循环中执行数据库查询）
  - 未使用的依赖包
  - 重复代码块

#### 🔵 建议级（优化项）

- 缺少日志记录
- 缺少监控指标
- 缺少 API 文档注解
- 测试覆盖率不足

### 输出格式

```
📊 项目扫描报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 一、项目结构

| 项目 | 详情 |
|------|------|
| 技术栈 | Java Spring Boot 2.7 + MySQL 8.0 |
| 后端服务 | 3 个（user-service, order-service, product-service） |
| 前端应用 | 1 个（web-admin, React 18） |
| 数据库 | MySQL（12 张表） |
| 已有文档 | README.md（简略）、无 PDLC 文档 |

## 二、可生成的基线文档

| 文档类型 | 是否可生成 | 内容预估 |
|---------|-----------|---------|
| 基线 PRD | ✅ 可生成 | 从 README + 服务结构推断，需人工补充业务目标 |
| API 设计文档 | ✅ 可生成 | 提取到 45 个接口定义 |
| DB 设计文档 | ✅ 可生成 | 提取到 12 张表结构 |
| 架构概要 | ✅ 可生成 | 3 服务 + 1 前端的依赖关系图 |

## 三、健康检查报告

### 🔴 阻断 (2)

| # | 位置 | 问题 | 风险 | 修复建议 |
|---|------|------|------|---------|
| 1 | user-service/src/.../UserDao.java:45 | SQL 字符串拼接 | SQL 注入 | 改用 PreparedStatement 参数化查询 |
| 2 | config/application.yml:12 | 数据库密码明文硬编码 | 凭证泄露 | 使用环境变量或密钥管理服务 |

### 🟠 严重 (3)
...

### 🟡 一般 (5)
...

### 🔵 建议 (4)
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
统计：🔴 2 | 🟠 3 | 🟡 5 | 🔵 4 | 总计 14 个问题

💡 建议：先修复 🔴 阻断级问题，再运行 /pdlc-adopt init 生成基线文档。
```

---

## init 子命令

**建议先运行 `scan` 查看报告，再运行 `init` 生成文档。**

### 执行流程

1. 执行与 `scan` 相同的扫描逻辑（收集项目信息）
2. 检查 `docs/` 下是否已有同名基线文档，已存在则跳过（避免覆盖）
3. 创建 PDLC 标准目录结构（如不存在）：
   ```
   docs/
   ├── 00_standards/
   ├── 01_requirements/prd/
   ├── 02_design/
   │   ├── api/
   │   ├── architecture/
   │   └── database/
   ├── 03_development/
   ├── 04_testing/
   ├── 05_deployment/
   └── 07_reviews/
   ```
4. 逆向生成基线文档（详见下方）
5. 生成接入状态文件
6. 输出生成结果摘要

### 基线文档生成规则

所有基线文档以 `ADOPTED-` 前缀命名，与正常 PDLC 文档区分。

所有文档头部包含接入标记：
```markdown
<!-- PDLC-TRACE -->
<!-- PDLC-ADOPTED -->
<!-- 项目名称: my-project -->
<!-- 接入日期: YYYY-MM-DD -->
<!-- 阶段: 接入基线 -->
<!-- 说明: 由 /pdlc-adopt init 自动生成，内容基于代码逆向推断，需人工审核补充 -->
```

#### 基线 PRD

- 路径：`docs/01_requirements/prd/ADOPTED-<项目名>-prd.md`
- 内容来源：README + 服务列表 + API 接口分组推断功能模块
- 包含：项目背景（从 README 提取）、功能模块清单（从代码推断）、技术栈说明
- **明确标注**：`> ⚠️ 以下内容由代码逆向推断，业务目标和用户故事需人工补充`

#### 基线 API 设计文档

- 路径：`docs/02_design/api/ADOPTED-<服务名>-api.md`（每个服务一个）
- 内容来源：路由定义扫描结果
- 包含：接口列表表格（方法、路径、描述、参数）、按模块分组
- 使用 本 skill 目录下的 `assets/api-design-template.md` 的格式
- **明确标注**：`> ⚠️ 接口描述基于函数名推断，请核对补充`

#### 基线 DB 设计文档

- 路径：`docs/02_design/database/ADOPTED-<服务名>-db.md`（每个服务一个）
- 内容来源：ORM Model / Migration / SQL 文件
- 包含：ER 关系图（文本格式）、表结构定义、索引设计、公共字段约定
- 使用 本 skill 目录下的 `assets/db-design-template.md` 的格式
- **明确标注**：`> ⚠️ 表结构从代码提取，请核对与实际数据库是否一致`

#### 基线架构文档

- 路径：`docs/02_design/architecture/ADOPTED-<项目名>-arch.md`
- 内容来源：服务列表 + 依赖关系 + 配置文件
- 包含：系统架构图（文本格式）、服务清单和职责、技术栈说明、服务间通信方式
- **明确标注**：`> ⚠️ 架构描述基于代码结构推断，请核对补充`

#### 接入状态文件

- 路径：`docs/00_standards/adopt-status.md`
- 记录各模块的 PDLC 接入状态：

```markdown
# PDLC 接入状态

> 由 `/pdlc-adopt init` 生成于 YYYY-MM-DD

## 接入概况

| 模块 | 基线 PRD | API 设计 | DB 设计 | 架构文档 | 测试覆盖 | 状态 |
|------|---------|---------|---------|---------|---------|------|
| user-service | ✅ | ✅ | ✅ | ✅ | ⚠️ 待补充 | 基线完成 |
| order-service | ✅ | ✅ | ✅ | ✅ | ⚠️ 待补充 | 基线完成 |

## 健康检查问题跟踪

| # | 级别 | 位置 | 问题 | 状态 |
|---|------|------|------|------|
| 1 | 🔴 | UserDao.java:45 | SQL 拼接 | 待修复 |
| 2 | 🔴 | application.yml:12 | 密码硬编码 | 待修复 |

## 后续建议

1. 人工审核基线文档，补充业务目标和用户故事
2. 修复 🔴 阻断级健康问题
3. 新功能开发使用 `/pdlc-feature` 走完整 PDLC 流程
4. 旧功能改造时从 `/pdlc-design` 开始（基线 PRD 已满足守卫检查）
5. 逐步为核心模块补充单元测试（使用 `/pdlc-tdd`）
```

---

## 要求

<!-- @include templates/prompts/output-language.md（已内联于下方，无需另读） -->
🌐 **Output language for generated artifacts**

All generated artifacts (PRDs, design docs, code comments, review reports,
test plans, deployment manuals, changelog entries, etc.) follow this policy:

1. **Default — match the conversation language exactly**:
   - 用户用中文与 Claude 对话 → 产中文文档、中文代码注释、中文报告
   - User talks to Claude in English → produce English artifacts
   - User talks in another language → produce artifacts in that language
   - **Never silently default to a fixed language regardless of the user's input.**

2. **Explicit override always wins**: when the user specifies a language for
   an artifact (e.g. "write the PRD in English", "用英文写 API 设计文档",
   "output the deploy doc in Japanese"), use that language for that artifact,
   regardless of conversation language.

3. **Mixed-language requirements**: if the user wants some artifacts in one
   language and others in a different language (common: Chinese PRD + English
   API docs for partners), honour each per-artifact instruction.

4. **Uncertain**: if you cannot reliably detect the conversation language,
   ask once before producing the first artifact.

This policy applies to **content** (prose, comments, headings). It does
**not** override technical conventions like English variable names, English
git commit subjects, or English error codes when the project's conventions
require them.
<!-- @include-end templates/prompts/output-language.md -->
- scan 子命令**严格只读**，不创建/修改任何文件
- init 子命令不修改任何现有代码文件，只在 `docs/` 目录下创建文档
- 已存在的文档不覆盖，跳过并提示
- 基线文档中需人工补充的部分用 `> ⚠️` 引用块明确标注
- 健康检查问题必须给出具体的文件路径和行号
- 读取 本 skill 目录下的 `assets/adopt-report-template.md` 模板作为格式参考

接入操作: $ARGUMENTS

<!-- @include templates/prompts/handoff.md（已内联于下方，无需另读） -->
## 段四：交接（Handoff）

命令完成后必须输出以下格式的最终消息：

```
✅ <阶段名> 完成：<主要产出物路径>
📊 自检：<通过数>/<总数> 通过（若有未通过，附要点）
📦 状态快照：docs/.pdlc-state/<feature-id>.json
👉 下一步：/pdlc-<next_step>
   （如果有分叉）或 /pdlc-<alt>（条件：<选择依据>）
```

**规则：**
- 主流程命令（写状态机的命令；下一跳见正文里「本命令的状态机取值」）必须显式输出"下一步"，不可省略
- 工具型命令（Layer 3）可以没有 `next_step`，此时输出 `👉 下一步：（本次流程结束，无后续）`
- 分叉场景必须说明**选择条件**，例如"若需补充测试用例 → `/pdlc-tdd`；若测试已齐 → `/pdlc-review`"
<!-- @include-end templates/prompts/handoff.md -->

**本命令的 handoff 输出：**

```
✅ PDLC 接入基线文档 完成
📦 产出：docs/**（基线文档集）
👉 下一步：（本次流程结束，无后续）
```

---
name: service-claude-md
description: |
  HTCMC PCHSystem 专用 skill——为各子服务目录生成与更新「分布式 CLAUDE.md」（提炼该服务的雷点、关键要素、文档索引）。当新建子服务、子服务架构发生变更、或需要补齐/更新某个服务的 CLAUDE.md 时使用。传入服务名（mcdr-plugin / user-service / project-service / scoring-service / title-service / wiki-service / alert-service / frontend），本 skill 自动读取对应架构文档，按统一模板生成或增量更新该服务目录下的 CLAUDE.md。在 PCHSystem 项目内，只要用户提到「子服务 CLAUDE.md」「为某服务生成/更新 CLAUDE.md」「补齐服务雷点」「服务记忆文件」，或正在新增/改动某个服务目录，就应使用本 skill——禁止手写子服务 CLAUDE.md。
license: MIT
metadata:
  project: HTCMC-PCHSystem
  version: 1.0.0
---

# service-claude-md · 子服务 CLAUDE.md 生成 / 维护

## 1. 这个 skill 做什么

HTCMC PCHSystem 采用**分布式 CLAUDE.md**（见根 [`CLAUDE.md`](../../../CLAUDE.md) §6）：

- **根 `CLAUDE.md`** 只管全项目统一规范（命名、全局红线 R-1~R-12、文档索引）。
- **每个子服务目录**下各有自己的 `CLAUDE.md`，只描述**该服务特有**的雷点、关键要素、文档索引。

本 skill 是子服务 CLAUDE.md 的**唯一维护入口**：读架构文档 → 按模板提炼 → 生成或增量更新。**不要手写**子服务 CLAUDE.md（根 CLAUDE.md §6 已声明）。

---

## 2. 何时用 / 何时不用

**用**：
- 新建子服务，需要为其生成 CLAUDE.md
- 子服务架构变更（接口 / 数据表 / 职责调整），需要更新其 CLAUDE.md
- 用户说「为 X 服务生成 / 更新 CLAUDE.md」「补齐 X 服务的雷点」

**不用**：
- 改根 `CLAUDE.md`（那是手动维护的统一规范）
- 生成 API 文档、模块文档等详尽文档（那是 `Docs/architecture/` 的职责，本 skill 只做「服务 CLAUDE.md 摘要 + 导航」）

---

## 3. 输入：服务名映射表

| 服务名 | 架构文档（读取源） | 默认 CLAUDE.md 路径 | 回根相对路径 |
|---|---|---|---|
| `mcdr-plugin` | `Docs/architecture/services/mcdr-plugin.md` | `McdrPlugin/CLAUDE.md` | `..` |
| `frontend` | `Docs/architecture/frontend.md` | `Frontend/CLAUDE.md` | `..` |
| `user-service` | `Docs/architecture/services/user-service.md` | `Backend/user_service/CLAUDE.md` | `../..` |
| `project-service` | `Docs/architecture/services/project-service.md` | `Backend/project_service/CLAUDE.md` | `../..` |
| `scoring-service` | `Docs/architecture/services/scoring-service.md` | `Backend/scoring_service/CLAUDE.md` | `../..` |
| `title-service` | `Docs/architecture/services/title-service.md` | `Backend/title_service/CLAUDE.md` | `../..` |
| `wiki-service` | `Docs/architecture/services/wiki-service.md` | `Backend/wiki_service/CLAUDE.md` | `../..` |
| `alert-service` | `Docs/architecture/services/alert-service.md` | `Backend/alert_service/CLAUDE.md` | `../..` |

> 路径为**默认值**。后端各模块是 Python 包，按 PEP8 用小写（根 CLAUDE.md §1 的命名例外）。**生成前先 Glob 确认目标目录是否存在**；若不存在（服务尚在规划、代码未建），先与用户确认落点，**不要擅自创建一堆空目录**。

---

## 4. 工作流

1. **读根规范**：读项目根 `CLAUDE.md`，掌握命名分层、全局红线 R-1~R-12、文档索引——子服务 CLAUDE.md 必须与之一致并引用。
2. **读服务架构文档**：按 §3 表读该服务的 `services/{服务名}.md`（frontend 读 `frontend.md`）。
3. **读相关数据模型**：读 `Docs/architecture/data-model.md`，定位该服务相关的 schema 与表（例如 scoring-service 关心 `scoring` schema 的 `submissions / placement_records / score_ledger`）。
4. **定位目标目录**：Glob 确认默认路径的目录是否存在；不存在则与用户确认落点。
5. **生成或增量更新** CLAUDE.md：
   - **新建**：复制 `templates/service-claude-md.template.md`，逐节填充，把 `{ROOT}` 占位符替换为 §3 表中的「回根相对路径」。
   - **已存在**：只改受影响章节，**保留人工补充内容**，更新末尾时间戳。
6. **保障跨工具别名**：确认该 CLAUDE.md 同目录存在 `AGENTS.md → CLAUDE.md` 相对软链（根 CLAUDE.md §6 约定）；缺失则 `ln -s CLAUDE.md AGENTS.md` 创建并 `git add`。**永不单独编辑 AGENTS.md**——它只是软链，权威源是 CLAUDE.md。

---

## 5. 子服务 CLAUDE.md 必备章节

详见 [`templates/service-claude-md.template.md`](./templates/service-claude-md.template.md)。共六节：

1. **服务定位**——一句话 + 指向架构文档的链接
2. **职责边界**——管 / 不管 两栏（从架构文档的「职责边界」表提炼）
3. **雷点·红线**——服务**特有**的不可违反约束（见 §6 编号规则）
4. **关键要素**——核心实体 / 表、对外接口、依赖的其他服务
5. **文档索引**——该服务相关文档 + 根文档入口
6. **与根规范的关系**——声明遵守根 CLAUDE.md，命名 / 红线以根为准

---

## 6. 红线编号规则（重要）

- 全局红线已在根 CLAUDE.md §3 用 **R-1~R-12** 编号（如 R-3 清箱时序、R-7 MCDR 是纯客户端、R-2 积分流水 append-only）。
- 子服务 CLAUDE.md **不重复**全局红线，只写**服务特有**的，用 **RS-x** 编号（RS-1、RS-2…）。
- 若是对某条全局红线在该服务的**具体化 / 强调**，写「遵守 R-x：…」并补该服务特有细节，不必重抄全局定义。
- **判断标准**：该约束写进根 §3 也成立 → 全局红线，子服务只引用；只在该服务语境下才成立 → 它是 RS-x。

---

## 7. 增量更新原则

已存在的子服务 CLAUDE.md，遵循**最小改动**：

- 只修改受架构变更影响的章节
- 保留用户 / 人工补充的内容（如特定运维备注）
- 追加而非重写
- 每次更新改末尾时间戳
- 不改章节顺序与标题（保持跨服务模板一致，便于横向对比）

---

## 8. 硬约束

- **命名**：服务顶层目录大驼峰（`McdrPlugin/`、`Frontend/`），后端 Python 模块包小写（`user_service/`），遵循根 CLAUDE.md §1。
- **引用而非复制**：架构文档永远权威，子服务 CLAUDE.md 只做摘要 + 链接，**不复制** DDL、完整流程图、完整接口表。
- **中文输出**：所有内容简体中文。
- **不臆造**：雷点 / 关键要素必须能在架构文档或数据模型中找到依据；架构文档未覆盖的，标注「待确认」并提示用户，**不要编造**。

---

## 9. 与根 CLAUDE.md 的关系

子服务 CLAUDE.md 是根规范的**下游**：

- 命名、全局红线、技术栈以**根 CLAUDE.md**为准，子服务不覆写。
- 子服务只补充「该服务特有的」雷点与要素。
- 任何与根规范冲突的内容，以根为准并修正子服务。

---

*本 skill 由根 `CLAUDE.md` §6 指定。全局 `persistent-context` 已在本项目禁用，本 skill 是 PCHSystem 专用的 CLAUDE.md 维护入口，不复用 persistent-context 模板。*

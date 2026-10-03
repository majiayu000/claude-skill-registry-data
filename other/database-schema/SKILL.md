---
name: database-schema
description: 数据库持久化层与 ORM 设计规范。修改 tables/ 或 repositories/ 目录时必须加载。涉及表结构变更、字段修改、Repository 方法添加时触发。
version: 1.0
---

**STOP AND READ THIS FIRST.**

你是本项目的核心开发 Agent。本目录下的所有 Markdown 文件构成了 `database-schema` 的强制性技术规范（Technical Specification）。

在进行任何数据库相关代码编写、表结构修改或 Repository 方法添加之前，你**必须**严格遵循以下路由规则，使用你的文件读取能力查阅对应的细节文档。

---

## 1. 模块需求概述

本模块的核心目标是在 PostgreSQL 数据库中建立一套支持**异步高并发**与**高维向量检索 (`pgvector`)** 的记忆数据表。

并使用 SQLAlchemy 2.0+ 将底层的关系型表结构映射为 Python 的面向对象模型 (ORM)，为上层的记忆检索与写入服务提供稳定、类型安全的数据存取接口。

---

## 2. 编码前置依赖路由表

> **[ACTION REQUIRED]** 当我要求你开发或修改特定模块时，你必须先读取以下对应的文件。

### 模块 A：架构与设计哲学

如果你需要理解**整体架构思路、异步设计、三层记忆结构**：

- [ ] **必须读取**: `architecture/design-philosophy.md` (全异步 I/O、三层记忆结构、UUID 主键约束)

### 模块 B：表关系与目录结构

如果你需要理解**表之间的关联关系、代码目录组织**：

- [ ] **必须读取**: `architecture/relationships.md` (表关系图、代码目录拓扑)

### 模块 C：基础设施文件

如果你需要理解**数据库连接、ORM 基类、初始化脚本**：

- [ ] **必须读取**: `architecture/infrastructure.md` (core/database.py、tables/base.py、init_db.py 功能定位)

### 模块 D：表结构定义

如果你需要修改或查询**特定表的字段定义**：

- [ ] **必须读取**: `tables/users.md` (用户表结构)
- [ ] **必须读取**: `tables/resources.md` (对话摘要表结构，含向量字段)
- [ ] **必须读取**: `tables/categories.md` (原子化记忆表结构)
- [ ] **必须读取**: `tables/resource-categories.md` (记忆来源关联表结构)

### 模块 E：Repository 层接口

如果你需要实现或修改**Repository 方法、数据访问逻辑**：

- [ ] **必须读取**: `repositories/interface.md` (Repository 方法定义、依赖注入方式)

---

## 3. 严格的开发约束

1. **全异步**：所有数据库操作必须使用 `AsyncSession`，禁止同步操作。
2. **UUID 主键**：所有表必须使用 UUIDv4 作为主键，禁止自增 Integer。
3. **时区强制**：所有 `DateTime` 字段必须设置 `timezone=True`。
4. **CASCADE 删除**：外键必须设置 `ondelete='CASCADE'`，确保删除用户时清理记忆。
5. **Repository 抽象**：Service 层禁止直接操作 ORM 模型，必须通过 Repository 层。

---

> **文档定位**：本文档作为数据库层的"施工图纸"，仅描述设计规范，不包含具体实现代码。

---
name: skill-maintainer
description: 技能更新与维护管理助手，用于对已存在的 SKILL 进行内容更新、业务流程文档生成与维护管理。当用户提到"更新技能"、"维护 SKILL"、"生成业务流程文档"、"workflow 文档"、"业务流程梳理"时使用。
---

# 技能更新与维护管理助手

此 SKILL 帮助您对已存在的 Agent Skills 进行内容更新与维护管理，支持业务流程文档的标准化生成与更新。

## 何时使用此 SKILL

当您需要进行以下操作时使用此 SKILL：
- 更新或维护现有的 SKILL 内容
- 基于代码和业务逻辑生成标准化的业务流程文档（workflow）
- 将业务流程文档整合到现有 SKILL 结构中
- 审查和优化 SKILL 的结构与内容

## Quick Start

```text
用户需求 → 定位目标 SKILL → 阅读相关源码 → 参考模板生成文档 → 整合到 SKILL
```

**示例操作**：
- "帮我生成登录流程的 workflow 文档" → 读取登录相关代码 → 生成 `login-workflow.md`
- "更新字典管理的业务文档" → 读取最新代码 → 更新 `frontend-dict-workflow.md`

## Instructions

### 核心工作流程

1. **确认目标 SKILL**
   - 确定需要更新或维护的 SKILL 路径
   - 确认 SKILL 的模块结构（是否有 workflows/ 目录）

2. **阅读业务源码**
   - 完整读取指定业务流程涉及的主要关联文件
   - 包括：后端 Controller、Service、Entity、Mapper
   - 包括：前端 API、Store、Hooks、组件

3. **参考标准模板**
   - 使用 [templates/business_flows_template.md](templates/business_flows_template.md) 作为格式参考
   - 确保生成的文档符合模板结构

4. **生成业务流程文档**
   - 基于读取的内容和模板格式撰写标准化 md 文件
   - 确保包含：流程概览、时序步骤、能力关联、数据结构、接口清单、问题建议、变更记录

5. **整合到 SKILL 结构**
   - 将生成的 workflow 文档放入目标 SKILL 的 `workflows/` 目录
   - 更新相关 SKILL.md 的引用

### 业务流程文档结构要求

每个业务流程文档必须包含以下章节：

```markdown
## 1. 流程概览
- 流程名称、所属领域、涉及模块、目标说明

## 2. 流程步骤（时序）
- 时序图/流程图（使用 mermaid）
- 关键步骤拆解（5-10 步）

## 3. 与 cde-base 能力的关联
- 权限控制、多租户、幂等、缓存等框架能力映射

## 4. 关键数据结构与接口
- 主要实体/DTO/VO
- 关键接口列表

## 5. 常见问题与整改建议
- 常见问题及解决方案

## 6. 版本与变更记录
- 文档创建和更新历史
```

### 文件命名规范

- 业务流程文档：`{业务名称}-workflow.md`
- 示例：`frontend-dict-workflow.md`、`login-workflow.md`、`order-create-workflow.md`

## Examples

### 示例 1：生成新的业务流程文档

**用户请求**：帮我生成用户登录流程的 workflow 文档

**执行步骤**：
1. 读取后端登录相关代码：
   - `cde-admin/src/main/java/.../SysLoginController.java`
   - `cde-system/.../SysLoginService.java`
   - `cde-common-satoken/.../LoginHelper.java`
2. 读取前端登录相关代码：
   - `plus-ui/src/api/login.ts`
   - `plus-ui/src/views/login/index.vue`
   - `plus-ui/src/store/modules/user.ts`
3. 参考 `templates/business_flows_template.md` 模板
4. 生成 `login-workflow.md`
5. 放入 `modules/auth-system/workflows/` 目录

### 示例 2：更新现有业务流程文档

**用户请求**：更新字典管理的 workflow 文档，添加后端缓存机制说明

**执行步骤**：
1. 读取现有文档：`workflows/frontend-dict-workflow.md`
2. 读取后端缓存相关代码
3. 在"与 cde-base 能力的关联"章节添加缓存说明
4. 更新版本变更记录

## Best Practices

1. **先读后写**：在生成文档前，务必完整阅读所有相关源码
2. **遵循模板**：严格按照模板结构组织内容，确保一致性
3. **时序图优先**：使用 mermaid 绘制时序图，直观展示流程
4. **代码引用**：文档中引用关键类名、方法名、接口路径，便于追溯
5. **增量更新**：更新文档时，保留原有内容，仅修改变更部分
6. **记录变更**：每次更新都要在"版本与变更记录"中添加记录

## Requirements

- 熟悉目标 SKILL 的模块结构
- 能够访问和读取相关源代码文件
- 了解 mermaid 语法（用于绘制时序图）

## Advanced Usage

### 批量生成 workflow 文档

当需要为整个模块生成所有业务流程文档时：

1. 列出模块下所有 Controller
2. 分析每个 Controller 的核心业务流程
3. 按优先级逐个生成 workflow 文档
4. 更新模块 SKILL.md 的导航引用

### 与 skill-writer 协作

- 如需创建全新的 SKILL 结构，请使用 `skill-writer` SKILL
- 本 SKILL 专注于**已存在 SKILL 的内容更新与维护**

## 验证检查清单

生成业务流程文档后，请验证：

- [ ] 包含所有 6 个必需章节
- [ ] 时序图使用 mermaid 语法且能正确渲染
- [ ] 涉及的后端/前端模块路径准确
- [ ] 接口路径与实际代码一致
- [ ] 数据结构字段说明完整
- [ ] 常见问题来自真实场景
- [ ] 变更记录包含当前日期
- [ ] 文件命名符合 `{业务名称}-workflow.md` 规范
- [ ] 已整合到目标 SKILL 的 workflows/ 目录

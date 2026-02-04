---
name: luban
description: Use when working with Luban game configuration tool - covers schema definition, Excel data filling, code generation, polymorphic types, validators, localization, and roblox-ts integration. Provides indexed reference to complete Luban documentation by topic
---

# Luban 配置工具专家

## 概述

Luban 是一个强大、易用、优雅、稳定的游戏配置解决方案。本技能提供对 Luban 完整文档的索引和访问,帮助快速定位相关文档解决配置问题。

**核心原则:** 优先查阅文档,基于文档提供准确方案。

## 何时使用本技能

**使用场景:**
- 定义配置表结构 (schema)
- Excel 配置数据填写问题
- 生成多语言配置代码
- 数据校验和验证器使用
- 多态类型、自定义类型配置
- 本地化和多语言支持
- Roblox-ts 特定配置需求

**不使用场景:**
- 通用 TypeScript 问题
- Roblox API 问题(非配置相关)
- Git 操作问题

## 文档索引

### 快速开始

| 文档 | 用途 | 关键词 |
|------|------|--------|
| `docs/intro.md` | Luban 介绍和核心特性 | 特性概览、能力列表 |
| `docs/beginner/quickstart.md` | 快速开始指南 | 新手入门、第一个配置 |
| `docs/beginner/generatecodeanddata.md` | 生成代码和数据 | 代码生成、数据导出 |
| `docs/beginner/integratetoproject.md` | 集成到项目 | 项目集成、工作流 |

### 类型系统

| 文档 | 用途 | 关键词 |
|------|------|--------|
| `docs/manual/types.md` | 类型系统详解 | 基础类型、容器类型、bean |
| `docs/beginner/usecustomtype.md` | 自定义类型 | bean定义、结构体 |
| `docs/beginner/usepolymorphismtype.md` | 多态类型 | 继承、抽象类、子类 |
| `docs/beginner/usecollection.md` | 集合类型 | list、map、set |
| `docs/manual/dynamicbean.md` | 动态bean | 运行时结构 |

### Excel 配置

| 文档 | 用途 | 关键词 |
|------|------|--------|
| `docs/manual/excel.md` | Excel 格式基础 | 单元格格式、基本填写 |
| `docs/manual/exceladvanced.md` | Excel 高级用法 | 复杂结构、嵌套数据 |
| `docs/manual/excelcompactformat.md` | Excel 紧凑格式 | 简化格式、列合并 |
| `docs/beginner/streamandcolumnformat.md` | 流式和列格式 | 多态数据填写 |

### 数据导入和生成

| 文档 | 用途 | 关键词 |
|------|------|--------|
| `docs/beginner/importtable.md` | 导入表格 | 表定义、数据源 |
| `docs/manual/importtable.md` | 导入表详解 | 复杂导入、多数据源 |
| `docs/manual/generatecodedata.md` | 生成详解 | 代码生成、数据导出 |
| `docs/manual/otherdatasource.md` | 其他数据源 | json、xml、yaml |

### 校验和验证

| 文档 | 用途 | 关键词 |
|------|------|--------|
| `docs/beginner/usevalidator.md` | 验证器使用 | 数据校验、规则 |
| `docs/manual/validator.md` | 验证器详解 | ref、path、range |

### Schema 定义

| 文档 | 用途 | 关键词 |
|------|------|--------|
| `docs/manual/schema.md` | Schema 定义 | __beans__.xml、__tables__.xml |
| `docs/manual/defaultschemacollector.md` | Schema 收集器 | 自动收集、约定 |

### 高级特性

| 文档 | 用途 | 关键词 |
|------|------|--------|
| `docs/manual/l10n.md` | 本地化 | 多语言、翻译 |
| `docs/manual/tag.md` | 标签系统 | 条件导出、分组 |
| `docs/manual/variants.md` | 变体 | 多版本、平台差异 |
| `docs/manual/traits.md` | Traits 特性 | 特性标记 |
| `docs/manual/cascadingoption.md` | 级联选项 | 选项继承 |

### 工具和扩展

| 文档 | 用途 | 关键词 |
|------|------|--------|
| `docs/manual/commandtools.md` | 命令行工具 | CLI、参数 |
| `docs/manual/template.md` | 模板系统 | 代码模板、自定义生成 |
| `docs/manual/typemapper.md` | 类型映射 | 类型转换 |
| `docs/manual/extendluban.md` | 扩展 Luban | 插件、二次开发 |

### 运行时和集成

| 文档 | 用途 | 关键词 |
|------|------|--------|
| `docs/beginner/loadinruntime.md` | 运行时加载 | 数据加载、反序列化 |
| `docs/manual/loadconfigatruntime.md` | 运行时加载详解 | 各语言加载方式 |
| `docs/manual/codestyle.md` | 代码风格 | 命名规范、格式 |

### 其他

| 文档 | 用途 | 关键词 |
|------|------|--------|
| `docs/help/faq.md` | 常见问题 | 错误排查、常见坑 |
| `docs/manual/architecture.md` | 架构设计 | 原理、设计 |
| `docs/manual/bestpractices.md` | 最佳实践 | 规范、建议 |
| `docs/other/changelog.md` | 更新日志 | 版本变更 |

## 工作流程

当用户提出 Luban 相关问题时:

1. **识别问题类型** - 使用上方索引表定位相关文档
2. **读取文档** - 使用 Read 工具读取相关文档(路径: `.claude-plugin/skills/luban/docs/...`)
3. **提供方案** - 基于文档内容提供准确解决方案
4. **示例代码** - 使用文档中的实际示例
5. **最佳实践** - 结合 bestpractices.md 提供建议

## Roblox-ts 特定说明

本项目是 Luban 的 roblox-ts 定制版本:

```json
  "repository": {
    "type": "git",
    "url": "git+https://github.com/WhiteDragonRoblox/roblox-ts-luban.git"
  },
  "author": "",
  "license": "ISC",
  "bugs": {
    "url": "https://github.com/WhiteDragonRoblox/roblox-ts-luban/issues"
  },
  "publishConfig": {
    "access": "public"
  },
  "homepage": "https://github.com/WhiteDragonRoblox/roblox-ts-luban#readme"
```

### Roblox-ts 枚举特性（v0.6.3+）

枚举类型基于 `value` 属性自动检测：

| value 类型 | 枚举类型 | 示例 |
|-----------|---------|------|
| 数字 | 数字枚举 | `value="1"`, `value="0x10"` |
| 非数字字符串 | 字符串枚举 | `value="ready"`, `value="active"` |

**数字枚举示例：**
```xml
<enum name="ItemRarity">
    <var name="Common" value="1"/>
    <var name="Rare" value="2"/>
</enum>
```
→ 生成 `Common = 1, Rare = 2`

**字符串枚举示例：**
```xml
<enum name="GameState">
    <var name="Ready" value="ready"/>
    <var name="Active" value="active"/>
</enum>
```
→ 生成 `Ready = "ready", Active = "active"`

### Roblox-ts Nominal 字段

Nominal 字段用于运行时类型识别，在 create 函数中硬编码：

```xml
<bean name="Entity">
    <var name="entityType" type="string" nominal="true" value="Entity"/>
    <var name="id" type="string"/>
</bean>
```

详细文档：`README_ROBLOX_TS.md`

## 常见问题关键词快查

根据用户问题关键词快速定位文档:

- **"多态"、"继承"、"抽象类"、"子类"、"parent"** → `beginner/usepolymorphismtype.md`
- **"Excel格式"、"单元格"、"填写"、"列格式"** → `manual/excel.md`
- **"校验"、"验证"、"ref"、"path"、"range"** → `beginner/usevalidator.md`
- **"枚举"、"enum"、"字符串枚举"、"数字枚举"** → `beginner/usecustomtype.md` + Roblox-ts 特定说明
- **"本地化"、"多语言"、"翻译"、"l10n"** → `manual/l10n.md`
- **"生成代码"、"导出"、"编译"** → `beginner/generatecodeanddata.md`
- **"运行时"、"加载"、"反序列化"** → `beginner/loadinruntime.md`
- **"定义表"、"schema"、"__beans__"、"__tables__"** → `manual/schema.md`
- **"list"、"map"、"set"、"array"、"集合"** → `beginner/usecollection.md`
- **"自定义类型"、"bean"、"结构体"** → `beginner/usecustomtype.md`
- **"标签"、"tag"、"条件导出"** → `manual/tag.md`
- **"模板"、"自定义生成"、"scriban"** → `manual/template.md`

## 重要原则

- ✅ **优先查阅文档** - 不凭记忆回答
- ✅ **使用实际示例** - 从文档中提取示例
- ✅ **完整路径** - 文档路径: `.claude/skills/luban/docs/`
- ✅ **中文回答** - 用户问题用中文回答
- ❌ **不编造信息** - 文档没有的内容诚实说明

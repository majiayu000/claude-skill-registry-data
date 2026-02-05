---
name: UnrealCodeImitator
description: Unreal 引擎源码学习和插件开发 Skill - 通过学习 Unreal 源码，参考官方实现来开发自己的插件功能或修改引擎。支持网络搜索、源码分析、代码生成、自动编译和迭代修复。【强制规则】所有 Unreal 项目编译必须且只能通过本 Skill 的 compile.bat 脚本执行，绝对禁止使用任何其他方式（如直接调用 RunUAT.bat、Build.bat、Visual Studio 等）编译 Unreal 项目。编译功能支持 DebugGame/Development 两种模式，使用"编译"或"编译V"触发 Development 模式，使用"编译G"触发 DebugGame 模式。
---

# Unreal 代码学习与插件开发 Skill

> **⚡ 这是一个自动激活的 Skill。**
>
> **当你在提示词中提到以下任何关键词时，此 Skill 会自动激活：**
>
> 📚 **参考源码类：** 参考 Unreal 源码 | 参考 UE 源码 | 学习 Unreal 源码 | 看 Unreal 源码
>
> 🔍 **学习实现类：** 学习 Unreal 中的 | 了解 Unreal 如何实现 | Unreal 是怎么实现的 | 参考官方实现
>
> 💡 **基于源码开发类：** 基于 Unreal 源码 | 参考 Unreal 模式 | 按 Unreal 风格 | 遵循 Unreal 最佳实践
>
> 🛠️ **实现功能类：** 实现一个 | 创建一个 | 类似 Unreal 的 | 参考 Unreal | 开发 Unreal 插件 | **使用 UnrealCodeImitator**
>
> 📖 **UE5 知识库查询：** `@UE5 [查询内容]` - 快速查询 UE5 官方文档
>
> 🔧 **编译功能：** `编译` / `编译V` (Development模式) | `编译G` (DebugGame模式) - 自动编译 Unreal 插件
>
> **🎯 激活后立即执行：** 自动调用 @UE5、网络搜索、源码分析三层工具，**不需要等待或额外指示**

---

## 概述

这个 Skill 帮助你通过学习 Unreal 引擎源码，开发自己的插件功能或直接修改引擎。它支持：

- 📚 自动搜索和分析 Unreal 源码
- 🔍 提取关键代码模式和最佳实践
- 💡 基于源码生成插件框架
- 🛠️ 协助修改和扩展引擎功能
- 🎯 生成可直接使用的代码实现
- 🔧 **自动编译和迭代修复** - 支持 DebugGame/Development 两种编译模式

---

## ⚡ 【立即执行】Skill 被触发时的自动行为

**当此 Skill 被触发时（用户包含触发关键词），立即进入决策流程，并按需执行以下步骤（可选择其中一部分或全部）：**

### 步骤 1：评估并（按需）调用搜索工具（不等待，不要等用户指示）

**第一步：调用 @UE5 官方知识库搜索**

```python
# 立即执行 - 不要等待、不要征询
RAG_search(
    queryString=user_query_converted_to_keywords(),
    knowledgeBaseNames="UE5"
)
# 预期等待时间：1-2 分钟
```

用户问题转换规则：
- 用户："我想实现自定义属性编辑器" → @UE5 搜索词："UE5 FProperty 自定义属性编辑器"
- 用户："怎么优化加载性能" → @UE5 搜索词："UE5 资源加载性能优化"

**第二步：并行调用网络搜索**

**⚠️ 网络搜索工具优先级：优先使用原生 `web_search`，如需补充再使用 MCP `ddg-search`**

```python
# 首选：原生 web_search 工具（更稳定、更快速）
web_search(
    explanation="搜索 Unreal Engine 相关教程和最佳实践",
    searchTerm=construct_network_search_query(user_problem)
)

# 备选/补充：MCP ddg-search（当原生搜索结果不足时使用）
mcp_call_tool(
    serverName="ddg-search",
    toolName="search",
    arguments=json.dumps({
        "query": construct_network_search_query(user_problem),
        "max_results": 10
    })
)
# 预期等待时间：1-2 分钟
```

网络搜索关键词示例：
- "Unreal Engine [功能] tutorial best practice"
- "UE5 [系统] implementation guide 2024"
- "[问题] solution Unreal"

**第三步：并行分析源码**

```python
# 同时执行 - 与前两步并行
search_unreal_source_code(
    engine_path=config.unrealEnginePath,
    keywords=extract_keywords_from_user_query(user_problem),
    search_depth=config.searchDepth,
    modules=config.focusModules
)
# 预期等待时间：2-5 分钟
```

### 步骤 2：综合三层搜索结果

在收集到三层搜索结果后（三层搜索都完成），**立即开始综合**：

1. 对比官方、社区、源码方案
2. 提取共同的最佳实践
3. 记录差异原因
4. 形成综合方案

### 步骤 3：生成回复

基于综合结果，**立即生成**以下内容：

```
[三层搜索过程说明]
已执行搜索：
✓ @UE5 官方知识库 - 获得 [主要发现]
✓ 网络搜索 - 获得 [主要发现]
✓ 源码分析 - 获得 [主要发现]

[对比和综合分析]
官方推荐：...
社区方案：...
源码实现：...
最佳实践：...

[最终方案和代码实现]
基于上述信息的完整解决方案...
```

---

**⭐ 关键执行规则：**

1. **立即执行** - 当 Skill 触发时，立即评估问题并启动最合适的一层或多层搜索，无需等待用户进一步指示
2. **灵活并行** - 可根据场景选择串行或并行执行多层搜索，在响应速度和信息充分之间权衡
3. **充分收集** - 在给出结论前，尽量确保已从最相关的信息源获得足够信息，而非机械地总是跑满三层
4. **完整报告** - 清晰向用户说明实际使用了哪些搜索手段及其主要发现

---

## 功能列表

### 1. UE5 官方知识库搜索
快速查询 UE5 官方文档中的功能说明、示例和最佳实践。

**使用方式：**
```
我想了解 Unreal 中的 [功能名称]
我需要查询 [特定功能] 的使用方法
UE5 如何实现 [功能]
```

**适用场景：**
- 快速查询官方 API 文档
- 了解功能的推荐实现方式
- 查找官方示例和教程
- 学习最新 UE5 特性

### 2. 源码搜索与分析
搜索 Unreal 引擎源码中的特定功能实现。

**路径来源约束：所有源码搜索使用的 Unreal 源码根目录必须从项目级配置 `.codebuddy/.UnrealCodeImitator/config.json` 的 `enginePath` 字段读取，禁止硬编码或猜测路径。**

**使用方式：**
```
我想学习 Unreal 中的 [功能名称]，比如：
- 事件系统（Event System）
- 反射系统（Reflection System）
- 属性系统（Property System）
- Actor 生命周期管理
- UI 框架（Slate）
- 插件加载机制
```

### 3. 代码模式提取
分析源码中的常见代码模式和设计模式。

**使用方式：**
```
帮我提取 Unreal 中 [组件/系统] 的代码模式
```

### 4. 插件框架生成
基于学习的源码，生成新插件的框架代码。

**使用方式：**
```
我想创建一个 [插件功能] 的插件，参考 Unreal 源码中的最佳实践
```

### 5. 代码实现协助
学习源码后，帮助实现特定功能。

**使用方式：**
```
我想实现 [功能描述]，请参考 Unreal 源码中的 [相关模块/系统] 的实现方式
```

### 6. 引擎修改指导
指导如何安全地修改和扩展 Unreal 引擎。

**使用方式：**
```
我想修改 Unreal 引擎的 [功能/模块]，请告诉我：
- 涉及的源文件位置
- 关键代码片段
- 修改步骤
- 可能的副作用
```

## 工作流程

### 第一步：配置环境（自动完成）

**🎯 自动引擎检测功能：**
- 首次编译时，`compile.bat` 会自动检测引擎路径并生成项目级配置文件
- 配置文件位置：`{Workspace}/.codebuddy/.UnrealCodeImitator/config.json`
- 支持三种场景自动检测：
  1. **项目插件**：通过 `.uproject` 的 `EngineAssociation` → `LauncherInstalled.dat` 或注册表查找
  2. **引擎插件**：向上查找 `Engine/Build/Build.version` 定位引擎根目录
  3. **引擎源码项目**：同上

**⚠️ 配置优先级：**
1. 项目级配置 `.codebuddy/.UnrealCodeImitator/config.json`（优先）
2. 自动检测（配置不存在时触发，并生成项目级配置）

**⚠️ Unreal 引擎路径使用强约束：**
- 所有与 Unreal 引擎相关的功能（编译、源码搜索等）必须从配置文件的 `enginePath` 字段读取路径
- 严禁根据默认安装位置或硬编码字符串猜测引擎路径
- 如需重新检测引擎路径，可运行 `detect_engine.bat` 或删除项目级配置文件后重新编译



### 第二步：提出需求
清晰地描述你想要学习或实现的功能。

### 第三步：充分利用三层搜索流程（关键）

**重要原则：** 默认由 Agent 根据问题类型、复杂度和对时效性的要求，灵活选择使用一层、两层或三层搜索，并决定先后顺序和是否并行执行，以在信息充分与响应速度之间取得平衡。

当 Skill 激活时，通常优先考虑使用 UE5 官方知识库查询；如有需要，再结合网络搜索和源码分析进行补充或验证。

#### 第一轮：UE5 官方知识库搜索 📖（RAG 搜索）
**执行方式：** 使用 `RAG_search` 工具查询 UE5 官方知识库
- 查询目标：官方 API 文档、功能说明、使用范例
- 搜索知识库：`UE5` （包含官方文档、API 参考、最佳实践）
- 获取内容：最权威、最新版本的实现建议
- **优势：** 最权威、最易理解、最新特性

**执行示例：**
```
用户提问：我想实现一个自定义属性编辑器
↓
Skill 自动执行：
RAG_search(queryString="UE5 自定义属性编辑器实现方式", 
           knowledgeBaseNames="UE5")
↓
获得：官方 API 使用指南、推荐实现方式
```

#### 第二轮：网络搜索与教程 🌐（原生搜索优先 + MCP 补充）
**执行方式：** 优先使用原生 `web_search` 工具，如需补充再使用 MCP `ddg-search`
- 搜索范围：官方文档、教程、社区讨论、最佳实践
- 搜索策略：
  1. **首选原生 `web_search`**：更稳定、响应更快
  2. 搜索官方教程和文档链接
  3. 寻找社区最佳实践和优化技巧
  4. 收集不同的实现角度和解决方案
  5. **如原生搜索结果不足**：补充使用 MCP `ddg-search`
- **优势：** 范围广、包含最新社区智慧和高级技巧

**执行示例：**
```
用户提问：我想优化 Actor Pool 的性能
↓
Skill 自动执行（首选原生搜索）：
web_search(
    explanation="搜索 Unreal Engine Actor Pool 性能优化最佳实践",
    searchTerm="Unreal Engine Actor Pool 性能优化最佳实践"
)
↓
如需补充，再使用 MCP 搜索：
mcp_call_tool(serverName="ddg-search", 
              toolName="search",
              arguments='{"query":"Unreal Engine Actor Pool performance optimization", 
                         "max_results":10}')
↓
获得：多个不同的实现方案、优化技巧、社区讨论
```

#### 第三轮：Unreal 源码分析 🔬（本地源码查询）
**执行方式：** 基于 config.json 的 unrealEnginePath，直接分析本地 Unreal 源码
- 定位相关实现：搜索源码文件中的关键类和函数
- 分析代码逻辑：提取设计模式、优化要点、代码结构
- 学习最佳实践：从 Epic 官方实现中学习
- **优势：** 最详细、最权威、最深入

**执行位置：**
- 搜索深度：由 `config.json` 的 `searchDepth` 控制
- 关键模块：`focusModules` 配置的模块（Core, Engine, UnrealEd, Slate 等）
- 包含范围：取决于 `includePrivate` 设置

**执行示例：**
```
用户提问：我想学习 Unreal 的反射系统
↓
Skill 自动执行：
1. 搜索 ${unrealEnginePath}/Source/Runtime/CoreUObject/Public 等位置
2. 找到 Class.h、Property.h 等核心头文件
3. 分析 FProperty、UClass 等关键类的实现
4. 提取反射系统的设计模式
↓
获得：完整的反射系统实现细节和代码模式
```

**搜索执行原则（由 Agent 自主决策）：**

1. **按需选择搜索层数**
   - 可以只使用其中一种搜索方式
   - 也可以组合使用两种或三种搜索方式
   - 可根据问题需要选择串行（先粗后细）或并行执行

2. **搜索结果优先级**（用于决策和代码生成时参考）
   - ① 官方推荐方案（UE5 知识库）- 最权威
   - ② 社区验证方案（网络搜索）- 最新、最实用
   - ③ 源码实现模式（源码分析）- 最深入、最详细

3. **何时扩展为多层搜索**
   - 当单一信息源不够完整或存在冲突时，追加其他搜索层
   - 当问题涉及性能优化、设计权衡或版本差异时，优先组合使用网络搜索和源码分析
   - 当用户强调时效性或最新实践时，优先结合网络搜索

4. **搜索充分性检查**
   在开始解决问题前，需确认：
   - ✓ 已选择和执行了与当前问题最相关的一层或多层搜索
   - ✓ 收集到的信息足以解决问题
   - ✓ 没有遗漏关键细节或最佳实践
   - ✓ 理解了官方推荐方案、社区实践、源码模式之间的异同（如相关）

**搜索指南：** 详见 `MCP_SearchGuide.md`（注意：现在优先使用原生 `web_search`，MCP 搜索作为补充）

### 第四步：代码生成
基于学习结果，生成：
- 插件框架代码
- 功能实现代码
- 配置文件
- 参考文档和链接

### 第五步：集成与测试
- 集成生成的代码到你的项目
- 根据实际需求调整
- 测试功能正确性

## Skill 执行指导（关键流程）

### 当 Skill 被触发时的自动化流程

Skill 激活后，应按以下步骤自动执行三层搜索获取信息：

#### 步骤 1：UE5 官方知识库查询（使用 @UE5 机制）
当用户问题涉及 UE5 功能、API、最佳实践时：

**执行指令：**
```
@UE5 [用户的具体问题转化为查询关键词]
```

**示例转化：**
```
用户问：我想实现一个自定义属性编辑器
↓ 转化为
@UE5 UE5 自定义属性编辑器 FProperty 编辑器实现方式
```

**预期获得：**
- 官方 API 文档链接
- 推荐的实现模式
- 代码示例
- 最新 UE5.x 特性说明

#### 步骤 2：网络搜索获取社区方案（原生 web_search 优先 + MCP ddg-search 补充）
如果需要补充社区实践和多角度方案：

**⚠️ 工具优先级：优先使用原生 `web_search`，如需补充再使用 MCP `ddg-search`**

**首选执行指令（原生 web_search）：**
```python
web_search(
    explanation="搜索 Unreal Engine [功能名称] 实现最佳实践",
    searchTerm="Unreal Engine [功能名称] 实现 最佳实践"
)
```

**备选/补充执行指令（MCP ddg-search）：**
```python
mcp_call_tool(
  serverName="ddg-search",
  toolName="search", 
  arguments=json.dumps({
    "query": "Unreal Engine [功能名称] 实现 最佳实践",
    "max_results": 10
  })
)
```

**搜索策略：**
- 搜索关键词包含：`Unreal Engine` + 功能名 + `tutorial/guide/best practice`
- 优先获取：官方文档、开发者文档、社区高评价内容
- 收集：不同的实现角度、性能优化技巧、常见陷阱

**预期获得：**
- 教程链接和文章
- 社区推荐方案
- 代码示例和开源项目
- 性能优化建议

#### 步骤 3：本地 Unreal 源码分析
基于 config.json 配置直接分析源码：

**执行位置：**
- 路径根目录：`${unrealEnginePath}/Source/`
- 重点搜索模块：`focusModules` 配置的目录
- 搜索深度：由 `searchDepth` 参数控制

**分析步骤：**
1. 定位关键类/函数在源码中的位置
2. 读取并分析代码实现逻辑
3. 提取设计模式（如工厂模式、观察者模式等）
4. 汇总性能优化要点和最佳实践

**预期获得：**
- 完整的源码实现细节
- Epic 官方的代码设计思路
- 性能优化的具体实现
- 可复用的代码模式

### 三层搜索的优先级规则

| 场景 | 优先级顺序 | 说明 |
|------|----------|------|
| 快速查询 API | ① UE5知识库 | 直接用 @UE5 查，最快 |
| 学习实现方式 | ① UE5 ② 网络 ③ 源码 | 官方优先，网络补充，源码深化 |
| 源码深度学习 | ③ 源码为主 ② 网络参考 ① UE5背景 | 源码为主，其他作为背景 |
| 性能优化 | ② 网络优先 ③ 源码分析 ① UE5 | 网络最新，源码验证，官方背景 |
| 创建新插件 | ① UE5框架 ② 网络参考 ③ 源码模式 | 官方框架为基础，网络最佳实践，源码设计 |

---

## 配置说明

### 项目级配置文件（自动生成）

配置文件路径：`{Workspace}/.codebuddy/.UnrealCodeImitator/config.json`

首次编译时自动生成，包含以下参数：

| 参数 | 说明 | 示例 |
|------|------|------|
| `enginePath` | Unreal 引擎路径（自动检测） | `H:/Program Files/Epic Games/UE_5.5` |
| `projectPath` | 项目路径（自动检测） | `H:/UE5_Projects/MyProject` |
| `uprojectFile` | .uproject 文件名（自动检测） | `MyProject.uproject` |
| `sceneType` | 场景类型（自动检测） | `project_plugin` / `engine_plugin_or_source` |
| `searchDepth` | 源码搜索深度 | `5` |
| `focusModules` | 重点搜索的模块 | `["Core", "Engine", "UnrealEd", "Slate"]` |
| `includePrivate` | 是否包含 Private 目录 | `true` |
| `compilation` | 编译配置 | 见下方编译模式说明 |

### 自动引擎检测

无需手动配置，`detect_engine.bat` 会自动：
1. 向上查找 `.uproject` 文件
2. 解析 `EngineAssociation` 字段
3. 从 `LauncherInstalled.dat` 或注册表获取引擎路径
4. 生成项目级配置文件

**手动重新检测：**
```bash
# 在 Workspace 目录执行
{SKILL_ROOT}\scripts\detect_engine.bat
```

## 参考文档与资源

本 Skill 包含核心文档、配置和工具脚本：

### 核心文档

| 文件 | 说明 | 用途 |
|------|------|------|
| `SKILL.md` | **本文件** - Skill 的完整功能和使用说明 | 理解 Skill 的全部功能和工作流程 |
| `THREE_LAYER_SEARCH_GUIDELINES.md` | **三层搜索指南（重要）** - 充分信息收集的规范和检查清单 | 确保解决问题前信息充分，三层搜索的详细执行方法 |
| `EXECUTION_PROTOCOL.md` | **执行协议（重要）** - 详细的自动执行流程定义 | Skill 开发者必读，定义触发、执行、搜索流程 |
| `UnrealSourceStructure.md` | Unreal 源码框架详解，快速定位源码位置 | 第三轮源码搜索时用来快速定位关键文件 |
| `MCP_SearchGuide.md` | 网络搜索指南，优先使用原生 web_search，MCP 搜索作为补充 | 第二轮网络搜索的搜索策略和技巧 |

### 编译与工具

| 文件 | 说明 | 用途 |
|------|------|------|
| `CompileAndIterateGuide.md` | 编译与迭代指南，自动化编译和错误修复流程 | 启用编译功能时的完整指南 |
| `PROMPT_INSTRUCTION.md` | **LLM 提示词指令** - 告诉 LLM 何时执行编译 | 控制代码生成后是否编译 |
| `COMPILE_MODES.md` | **编译模式详细说明** - DebugGame/Development/Shipping 三种模式 | 选择合适的编译模式指南 |
| `COMPILE_QUICK_REFERENCE.md` | **编译模式快速参考卡** - 一句话选择编译模式 | 快速查询编译模式用途 |
| `compile.bat` | **唯一编译入口（必须使用）** - BAT 编译脚本，自动检测引擎路径或从项目级配置读取 | 统一的自动化编译执行和错误收集入口 |

**脚本路径（相对 Skill 根目录）：**
- 编译脚本：`scripts/compile.bat`
- 引擎检测脚本：`scripts/detect_engine.bat`
- 项目级配置文件：`{Workspace}/.codebuddy/.UnrealCodeImitator/config.json`

在实际调用时，请按以下规则获取脚本路径：
- 先获得本 Skill 根目录路径（例如外部系统注入的 `SkillPath` 或工作目录）
- 再拼接相对路径 `scripts/compile.bat`，形成完整路径
- 避免在 Skill 内硬编码任何绝对磁盘路径（例如盘符 `H:/`）

**🚨 强制：必须使用完整绝对路径调用 compile.bat（必须遵守）：**
所有编译命令**必须**动态获取 Skill 根目录并拼接完整路径：
```powershell
# 示例：%SKILL_ROOT% 为 Skill 根目录，%PROJECT_PATH% 为当前项目的 .uproject 路径
%SKILL_ROOT%\scripts\compile.bat Development %PROJECT_PATH%
```
> ⚠️ **调用规则**：
> - 先获取本 Skill 的根目录路径（系统注入的环境变量或从当前文件路径推导）
> - 拼接相对路径 `scripts\compile.bat` 形成完整绝对路径
> - **禁止**使用 `cmd /c "cd ... && .\compile.bat"` 方式调用
> - **禁止**写死特定机器的路径（如 `C:\Users\xxx\...`）

### 配置文件

| 文件 | 说明 | 配置项 |
|------|------|--------|
| `.codebuddy/.UnrealCodeImitator/config.json` | **项目级配置（自动生成）** - 引擎路径、项目信息、搜索参数 | `enginePath`, `projectPath`, `searchDepth`, `focusModules`, `compilation` |
| `UE5_KNOWLEDGE_BASE_INTEGRATION.md` | UE5 知识库集成说明 | @UE5 查询机制的详细说明 |
| `IMMEDIATE_EXECUTION_RULES.md` | **立即执行规则（最重要）** | 明确 Skill 触发时应立即执行什么操作 |
| `COMPILE_SCRIPT_UPGRADE.md` | 编译脚本升级说明 | PowerShell → BAT 迁移指南 |
| `UPDATE_LOG.md` | Skill 更新日志 | 追踪 Skill 的版本更新和改进 |

### 推荐阅读顺序

**首次使用（用户）：**
1. 本文件 (SKILL.md) - 了解 Skill 功能
2. config.json - 配置引擎路径
3. **THREE_LAYER_SEARCH_GUIDELINES.md** - 理解三层搜索规范（重要！）
4. UnrealSourceStructure.md - 熟悉源码结构

**深度学习（用户）：**
5. MCP_SearchGuide.md - 掌握网络搜索技巧
6. UE5_KNOWLEDGE_BASE_INTEGRATION.md - 学习 @UE5 查询
7. CompileAndIterateGuide.md - 启用编译功能
8. **COMPILE_MODES.md** - 理解不同编译模式的用途
9. **COMPILE_QUICK_REFERENCE.md** - 快速选择编译模式

**Skill 开发者（必读）：**
1. **IMMEDIATE_EXECUTION_RULES.md** - 立即执行规则（最最最重要！）
2. **THREE_LAYER_SEARCH_GUIDELINES.md** - 三层搜索规范
3. SKILL.md - 总体功能说明
4. **EXECUTION_PROTOCOL.md** - 自动执行流程定义
5. PROMPT_INSTRUCTION.md - LLM 提示词指令
6. config.json - 配置参数说明
7. 其他参考文档按需查阅

## 编译和迭代流程

### ⚠️ 强制编译规则（最高优先级）

> **🚨 绝对禁止使用任何其他方式编译 Unreal 项目！**
>
> **所有 Unreal 项目的编译必须且只能通过 UnrealCodeImitator 技能的 `scripts/compile.bat` 脚本执行。**
>
> **禁止的行为包括但不限于：**
> - ❌ 直接调用 `RunUAT.bat`、`Build.bat` 或任何 Unreal 官方编译脚本
> - ❌ 直接调用 `UnrealBuildTool.exe` 或 `UnrealBuildTool.dll`
> - ❌ 使用 Visual Studio 直接编译 Unreal 项目
> - ❌ 使用 MSBuild 直接编译 Unreal 项目
> - ❌ 在终端中手动拼接任何 UE/UBT 编译命令
> - ❌ 使用 `compile.ps1`（已废弃）
>
> **唯一允许的编译方式：**
> - ✅ 调用 `scripts/compile.bat [Configuration] [ProjectPath]`
> - ✅ **强制**：必须动态获取 Skill 根目录并拼接完整绝对路径
> - 格式：`%SKILL_ROOT%\scripts\compile.bat [Configuration] [ProjectPath]`
> - **禁止**写死特定机器的路径

### 编译控制规则

- 🔴 **默认不编译** - LLM 仅生成代码
- 🟢 **在你要求时编译** - 在提示词中使用编译关键词
- 🔵 **自动迭代修复** - 可以要求自动修复并重新编译
- ⚙️ **统一编译入口（强制）** - 所有 Unreal 编译请求（无论是一次性编译、重复编译还是自动迭代修复）**必须且只能**通过 `scripts/compile.bat` 执行，**绝对禁止**在对话中自行为用户构造或执行任何 UE 编译命令（例如直接调用 `RunUAT.bat`、`Build.bat` 或其他脚本；`compile.ps1` 视为废弃脚本）。**🚨 强制要求：必须动态获取 Skill 根目录并拼接完整绝对路径调用 compile.bat，禁止写死特定机器路径**
- 🎯 **支持多种编译模式** - 支持 DebugGame、Development、Shipping 三种编译配置

#### 编译模式说明

Unreal Engine 编译配置 = Configuration（配置状态）+ Target Type（目标类型）

本 Skill 编译的目标类型固定为 **Editor**（编辑器插件），支持两种配置状态：

| 用户关键词 | 完整编译配置 | Configuration | 说明 | 适用场景 |
|----------|------------|--------------|------|---------|
| **编译G** | **DebugGame Editor** | DebugGame | 引擎优化，插件代码可调试 | 调试插件崩溃或逻辑问题 |
| **编译V** 或 **编译** | **Development Editor** | Development | 引擎和插件都优化（默认） | 日常开发和测试（推荐） |

> **说明：** 实际编译命令中，"Editor" 目标类型已包含在目标名称中（如 `ProjectNameEditor`），配置参数只需传递 `DebugGame` 或 `Development`。

### 工作流程

```
1. 你发送需求给 LLM
   ↓
2. LLM 是否看到编译关键词?
   ├─ 否 → 只生成代码 ✅
   └─ 是 → 继续执行编译流程
           ↓
3. 运行 compile.bat 脚本
   ⚠️ 脚本自动从项目级配置 `.codebuddy/.UnrealCodeImitator/config.json` 读取 enginePath
   ⚠️ 如配置不存在，自动调用 detect_engine.bat 检测并生成配置
   ⚠️ 自动检测 Unreal 引擎版本（主版本号.次版本号）
   ⚠️ 自动检测 Visual Studio 安装路径和 MSBuild 工具
   ⚠️ 使用配置的引擎路径调用 UnrealBuildTool.dll （通过 dotnet）进行编译
   ⚠️ 严禁绕过本脚本直接调用 Unreal 官方编译脚本（如 `RunUAT.bat`、`Build.bat`）或手写其他 UE/UBT 编译命令；如需调整编译方式，应修改 `scripts/compile.bat` 本身，而不是在对话中拼接命令行
   ↓
4. 编译成功？
   ├─ YES → 功能可用 ✅
   └─ NO  → 生成错误日志
           ↓
        5. LLM 分析错误
           ↓
        6. 你要求"修复"？
           ├─ 否 → 等待你的指示
           └─ 是 → LLM 修复代码
                    ↓
                重新编译（回到步骤 4）
```

**编译脚本说明：**
- 📄 `compile.bat` - **唯一编译入口（必须使用）** (BAT 版本，更稳定)
  - ⚠️ **重要：自动从项目级配置 `.codebuddy/.UnrealCodeImitator/config.json` 读取 `enginePath` 字段**
  - ⚠️ **自动检测：如配置不存在，自动调用 `detect_engine.bat` 检测引擎路径并生成配置**
  - ✅ **全自动执行**：脚本完全自动化，无需任何用户交互（无 `pause` 命令）
  - ✅ **正确解析 Windows 路径**：能够正确处理包含盘符的路径（如 `H:/Program Files/...`）
  - ✅ **自动检测 Unreal 引擎版本**（从 Build.version 读取主版本号和次版本号）
  - ✅ **自动检测 Visual Studio 路径**（使用 vswhere.exe 定位最新安装的 VS）
  - ✅ **验证 MSBuild 工具**（确保编译环境完整）
  - 不依赖 PowerShell 环境
  - 兼容性更好，错误更少
  - **适用于 Agent 自动调用**：所有错误通过退出码返回，不需要用户按键确认
  - 🚨 **强制：必须动态获取 Skill 根目录并拼接完整绝对路径**，**禁止**使用 `cmd /c "cd ... && .\compile.bat"` 方式，**禁止**写死特定机器路径：
    ```powershell
    # %SKILL_ROOT% = Skill 根目录，%PROJECT_PATH% = 当前项目 .uproject 路径
    %SKILL_ROOT%\scripts\compile.bat Development %PROJECT_PATH%
    ```
  
**详见：** 
- `PROMPT_INSTRUCTION.md` - 如何告诉 LLM 何时编译
- `CompileAndIterateGuide.md` - 完整的编译和迭代指南

### 快速示例

**不编译：**
```
我想学习 Unreal 的反射系统，请参考源码生成一个自定义属性编辑器。
```
→ LLM 只生成代码，不编译

**编译（Development模式）：**
```
我想学习 Unreal 的反射系统，请参考源码生成一个自定义属性编辑器，然后编译。
或
我想学习 Unreal 的反射系统，请参考源码生成一个自定义属性编辑器，然后编译V。
```
→ LLM 生成代码后使用 Development Editor 模式编译（引擎和插件都优化）

**编译（DebugGame模式）：**
```
我想学习 Unreal 的反射系统，请参考源码生成一个自定义属性编辑器，然后编译G。
```
→ LLM 生成代码后使用 DebugGame Editor 模式编译（引擎优化，插件代码可调试）

**自动迭代：**
```
我想创建一个事件系统插件。请生成代码、编译，如果有错误，自动修复并重新编译直到成功。
或（使用DebugGame模式）
我想创建一个事件系统插件。请生成代码、编译G，如果有错误，自动修复并重新编译直到成功。
```
→ LLM 调用 compile.bat [Configuration] 编译并循环修复直到成功

**编译脚本：** 使用 `compile.bat [Configuration]`（唯一编译入口，BAT 版本更稳定）
- ✅ **自动从项目级配置 `.codebuddy/.UnrealCodeImitator/config.json` 读取 `enginePath`**
- ✅ **自动检测：配置不存在时自动调用 `detect_engine.bat` 检测并生成**
- ✅ **支持编译配置参数**：DebugGame, Development (默认)
- ✅ **编译目标固定为 Editor**（编辑器插件开发）
- ✅ **全自动执行，无需用户交互**（移除所有 `pause` 命令，适合 Agent 调用）
- ✅ **正确解析 Windows 路径**（支持盘符路径如 `H:/Program Files/Epic Games/UE_5.4`）
- ✅ **自动检测 Unreal 引擎版本**（验证引擎主版本号和次版本号）
- ✅ **自动检测 Visual Studio 路径**（确保编译环境正确）
- ✅ 无需 PowerShell 配置
- ✅ Windows 原生支持，兼容性好
- ⚠️ **配置自动生成，无需手动配置引擎路径**
- 🚨 **强制：必须动态获取 Skill 根目录并拼接完整绝对路径调用**，禁止使用 `cmd /c "cd ... && .\compile.bat"` 方式，禁止写死特定机器路径

**编译模式识别：**
- 用户说"编译G" → 动态获取 Skill 根目录，执行 `%SKILL_ROOT%\scripts\compile.bat DebugGame %PROJECT_PATH%` → 编译为 DebugGame Editor 配置
- 用户说"编译V"或"编译" → 动态获取 Skill 根目录，执行 `%SKILL_ROOT%\scripts\compile.bat Development %PROJECT_PATH%` → 编译为 Development Editor 配置
- 🚨 **强制**：**必须**动态拼接完整绝对路径调用，禁止使用相对路径或 `cmd /c` 包装，禁止写死特定机器路径

## 源码阅读最佳实践

### ⚠️ Deprecated API 谨慎使用
在学习和参考 Unreal 源码时，当你看到含有 `deprecated` 的 API，**必须谨慎使用**：

#### 识别标志
源码中常见的 deprecated 标记：
- `DEPRECATED()` - 通用废弃宏
- `UE_DEPRECATED()` - Unreal 标准废弃宏
- `UE4_DEPRECATED()` - 旧版本兼容标记
- 注释中的 "deprecated"、"Deprecated"、"已废弃" 标记

#### 安全做法
1. **寻找替代方案** - Deprecated 注释通常会指出新的 API，如 `"Use NewFunction instead"`
2. **优先使用新 API** - 即使学习旧的实现逻辑，代码中必须使用新 API
3. **添加注释和 TODO** - 如果必须使用 deprecated API，添加明确的注释和 TODO 标记
4. **计划升级路径** - 标记预期在哪个引擎版本后移除该代码

#### 检查位置
- Unreal 头文件中的函数声明
- 引擎源码注释中的提示
- Engine Version 相关的 Breaking Changes 文档
- 官方迁移指南（Migration Guide）

#### 实际示例
```cpp
// ❌ 错误做法 - 直接使用 deprecated API
FString Result = GetDeprecatedValue();  // 编译器警告，且未来引擎版本可能删除

// ✅ 正确做法 - 查找并使用新 API
FString Result = GetModernValue();  // 新 API，未来版本安全

// ✅ 如必须使用 - 添加详细注释
FString Result = GetDeprecatedValue();  // TODO: UE5.5 移除，替换为 GetModernValue()
                                        // 原因: 需要保持向后兼容
```

#### 检查步骤
1. 看到函数名时，搜索其声明找到 `DEPRECATED` 宏
2. 阅读注释中的替代方案建议
3. 验证新 API 的功能是否完全兼容
4. 如有性能差异，记录下来留作备注

## Skill 执行示例（完整流程）

### 示例 1：实现自定义编辑器面板（推荐流程）

**用户问题：**
```
我想创建一个建筑编辑器的布局面板，参考 Unreal 源码中的编辑器 UI 实现。
请告诉我如何实现一个类似 Details Panel 的自定义面板。
```

**自动执行流程：**

#### 第一步：@UE5 官方知识库查询
```
@UE5 Unreal Editor Panel Details Panel SCompoundWidget Slate UI 框架
```

**收获：**
- Slate 框架的官方 API 文档
- SCompoundWidget 的基础使用
- Details Panel 的官方实现指南
- FPropertyHandle、IDetailsView 等 API 说明

#### 第二步：网络搜索（原生优先）
```
首选 web_search：
- "Unreal Engine SCompoundWidget 自定义面板教程"
- "Unreal Details Panel 实现原理"
- "Slate 编辑器面板最佳实践"

如需补充，再用 MCP ddg-search
```

**收获：**
- 社区教程和示例代码
- 多种不同的实现方式
- 常见的性能问题和解决方案
- 开源编辑器插件的参考

#### 第三步：本地源码分析
```
位置：${UE_PATH}/Source/Editor/UnrealEd/Private/Kismet2/
位置：${UE_PATH}/Source/Runtime/Slate/Public/
关键类：SCompoundWidget, SDetailView, SPanel
```

**收获：**
- Epic 官方的完整实现代码
- 内部设计模式和架构
- 性能优化的具体方式
- 高级特性的实现细节

#### 最终输出：
结合三层搜索的结果，生成：
- 基于官方框架的 UI 面板代码
- 完整的头文件声明
- 实现细节和关键函数
- 集成指南和最佳实践注释

---

### 示例 2：性能优化（特殊流程）

**用户问题：**
```
我的游戏加载时间很长，参考 Unreal 源码，告诉我如何优化 Asset Loading？
```

**自动执行流程：**

#### 第一步：@UE5 官方知识库（背景信息）
```
@UE5 UE5 Asset Loading 性能优化 Async Loading
```

**收获：** 官方的优化指南和最新特性

#### 第二步：网络搜索（原生优先，重点）
```
首选 web_search：
- "Unreal Engine 资源加载性能优化"
- "Async Loading 最佳实践 2024"
- "Asset Registry 性能优化技巧"

如需补充，再用 MCP ddg-search
```

**收获：** 最新社区方案和优化技巧（**此步优先级最高**）

#### 第三步：本地源码分析（深化理解）
```
位置：${UE_PATH}/Source/Runtime/CoreUObject/Private/Async/
位置：${UE_PATH}/Source/Engine/Private/Streaming/
关键类：FStreamingManager, FAsyncLoadingThread
```

**收获：** 底层实现原理，用于验证和深化理解

---

### 示例 3：快速 API 查询（最快流程）

**用户问题：**
```
@UE5 UE5 Enhanced Input System 如何使用？
```

**自动执行流程：**
- ✅ 直接返回官方文档和 API 说明
- ⏭️ 跳过第二、三步（除非用户要求更深入）

**预期结果：** 3-5 分钟内获得完整答案

---

## 常见使用场景

### 场景 0：快速查询 API（推荐首选）
```
UE5 中的 Enhanced Input System 是什么？
怎样使用 Lumen 全局光照？
查询 Nanite 虚拟化几何体的实现方式
```
→ 直接查询 UE5 官方知识库，快速获取最权威答案

### 场景 1：学习反射系统
```
我想深入学习 Unreal 的反射系统（Reflection System），
了解如何实现自定义的属性编辑器。
```
→ 先查 UE5 知识库了解概念，再学源码掌握细节

### 场景 2：创建自定义插件
```
我想创建一个资源管理插件，参考 Unreal Asset Registry 的实现方式。
请生成插件框架和关键实现。
```
→ 查 UE5 知识库 → 网络搜索最新方案 → 参考源码实现

### 场景 3：修改引擎行为
```
我想修改 Actor 的序列化方式。请告诉我：
1. 哪些源文件需要修改
2. 关键的代码逻辑
3. 修改步骤
```

### 场景 4：性能优化
```
我想优化游戏性能，请参考 Unreal 源码中的 [特定系统]
的优化方式，并应用到我的代码中。
```

## 输出格式

本 Skill 生成的代码将包含：

1. **结构清晰** - 遵循 Unreal 代码规范
2. **注释完整** - 标注关键逻辑和参考源码位置
3. **可即用** - 可直接复制到你的项目
4. **可扩展** - 留出扩展点供你自定义

## 限制与注意事项

- 🔐 不会直接修改你的项目代码，仅提供参考
- 📋 需要在 config.json 中配置正确的引擎路径
- 🎯 重点是通用模式提取，非项目特定优化
- ✅ 生成的代码需要你在实际项目中测试验证

## 快速开始

1. 在 Workspace 目录打开 CodeBuddy（无需手动配置，首次编译自动检测引擎路径）
2. 提出你的学习或开发需求
3. 等待 Skill 分析源码并生成结果
4. 集成生成的代码到你的项目中

**手动重新检测引擎路径（可选）：**
```bash
{SKILL_ROOT}\scripts\detect_engine.bat
```

---

## Skill 触发与自动执行机制

### ⚡ Skill 自动触发条件

本 Skill 会在以下情况自动激活（无需显式调用）：

### 自动触发的关键词和短语

当你的提示词中出现以下任何关键词/短语时，LLM 会自动激活此 Skill：

#### 📚 参考源码类
- "参考 Unreal 源码"
- "参考 UE 源码"
- "参考引擎源码"
- "参考 Unreal 的"
- "查看 Unreal 源码中"
- "看 Unreal 源码"
- "学习 Unreal 源码"
- "研究 Unreal 源码"
- "对标 Unreal 源码"

#### 🔍 学习实现类
- "学习 Unreal 中的"
- "了解 Unreal 如何实现"
- "看 Unreal 怎么做"
- "Unreal 是怎么实现的"
- "学习 UE 的实现"
- "参考官方实现"

#### 💡 基于源码开发类
- "基于 Unreal 源码"
- "参考 Unreal 模式"
- "按 Unreal 风格"
- "遵循 Unreal 最佳实践"
- "参考 Unreal Asset Registry"
- "参考 Unreal Component 系统"

#### 🛠️ 实现特定功能类
- "实现一个 [功能]，参考 Unreal 的"
- "创建一个 [功能]，像 Unreal 的"
- "我想 [功能]，参考 Unreal"
- "类似 Unreal 的 [系统]"

#### 🎓 源码学习和优化类
- "从 Unreal 源码学"
- "优化，参考 Unreal"
- "性能优化，参考 Unreal"
- "设计模式，参考 Unreal"

#### 💡 直接调用 Skill 类（新增）
- "使用 UnrealCodeImitator"
- "激活 UnrealCodeImitator"
- "使用 Unreal 代码学习 Skill"
- "用 UnrealCodeImitator"
- "UnrealCodeImitator Skill"
- "使用 UnrealCodeImitator 来编译"
- "使用UnrealCodeImitator来编译"

### 自动触发的示例

✅ **这些提示词会自动触发 Skill：**

```
我想创建一个属性编辑器，参考 Unreal 源码
```

```
参考 Unreal 中的事件系统，实现一个自己的
```

```
学习 Unreal 如何实现反射系统
```

```
基于 Unreal Component 的设计，创建自定义组件
```

```
我想优化性能，参考 Unreal 源码中的最佳实践
```

```
怎样实现一个 Actor Pool，像 Unreal 的对象管理
```

```
使用 UnrealCodeImitator，帮我学习 Slate 编辑器框架
```

```
激活 UnrealCodeImitator Skill，我想创建一个自定义属性编辑器
```

```
用 UnrealCodeImitator 帮我分析 Unreal 的资源管理系统
```

### 不会触发 Skill 的提示词

❌ **这些提示词不会自动触发 Skill：**

```
帮我写一个 C++ 类
```

```
怎样创建一个插件
```

```
我需要一个代码示例
```

```
C++ 语法问题
```

### 手动调用 Skill（现已支持自动触发）

⚠️ **注意：** 以下表述现在都能**自动触发** Skill，无需手动调用！

```
使用 UnrealCodeImitator，帮我 [需求]
```

或

```
激活 UnrealCodeImitator Skill，[需求]
```

或

```
用 UnrealCodeImitator [需求]
```

**自动触发的原理：** "使用 UnrealCodeImitator" 等表述已被添加到自动触发关键词列表中，所以 Skill 会自动激活，无需显式指令。

### 新增关键词：UE5 知识库搜索

现在，你可以通过以下关键词触发 UE5 知识库搜索：

- \"查询 UE5\"
- \"查询官方\"
- \"UE5 知识库\"
- \"官方文档\"
- \"UE5 API\"
- \"官方实现\"

**示例：**

```
查询 UE5 知识库，Lumen 全局光照如何实现
```

```
官方文档中关于 Enhanced Input System 的说明
```

```
查询 Nanite 虚拟化几何体的 UE5 API
```

---

## 搜索优先级说明

Skill 现在使用**三层搜索策略**（自上而下）：

1. **UE5 官方知识库** ⭐ 最权威、最快
   - 官方 API 文档
   - 推荐实现方式
   - 最新 UE5 特性

2. **网络搜索与教程** ⭐⭐ 范围广、包含技巧
   - **⚠️ 工具优先级：优先使用原生 `web_search`，备选 MCP `ddg-search`**
   - 社区最佳实践
   - 高级优化技巧
   - 多角度解决方案

3. **Unreal 源码分析** ⭐⭐⭐ 最详细、最深入
   - 底层实现细节
   - 代码设计模式
   - 性能优化要点

---

### 🎯 Skill 激活后的自动执行流程（重要）

当 Skill 被触发时，**应按以下步骤自动决策并执行搜索和分析**（不要等待用户手动指导）：

#### 自动执行决策树

```
Skill 被触发
    ↓
1️⃣ 判断问题类型与需求
   - 问题复杂度（极简 / 一般 / 复杂）
   - 是否涉及最新特性或社区最佳实践
   - 是否需要深入理解引擎内部实现
    ↓
2️⃣ 选择首选信息源
   - 快速 API / 官方用法 → 优先 @UE5 官方知识库
   - 性能优化 / 最新实践 → 优先网络搜索
   - 引擎内部机制 / 设计模式 → 优先源码分析
    ↓
3️⃣ 决定是否追加其他搜索层
   - 如首选信息源不足以回答问题或存在冲突 → 追加 1～2 个搜索层
   - 需要同时对比官方、社区和源码时 → 使用全部三层搜索
    ↓
4️⃣ 决定执行方式（串行 / 并行）
   - 对时效性要求高 → 尽量并行执行多层搜索
   - 需要先形成大致方向再细化 → 先执行 1 层，再按需追加后续层
    ↓
5️⃣ 综合已获取的信息
   - 对比不同信息源的结论
   - 提炼一致的最佳实践
   - 记录明显差异及原因推测
    ↓
6️⃣ 生成代码实现或解决方案
   - 基于当前已收集的信息给出答案
   - 如信息仍明显不足 → 优先补充最相关的搜索层
```

**⭐ 核心原则：** 
- 三层搜索为可组合工具，可单独使用，也可两两或三者同时使用
- 由 Agent 根据问题自动选择需要的搜索层数和先后顺序
- 在保证响应速度的前提下，尽量保证信息充分，再开始编码

#### 自动执行的工具调用

**在 Skill 激活时，可按需进行以下调用：**

1. **UE5 官方知识库查询**
   ```python
   # 自动调用（如果查询相关）
   RAG_search(
       queryString=convert_user_query_to_ue5_keywords(),
       knowledgeBaseNames="UE5"
   )
   ```

2. **网络搜索（优先原生 web_search，备选 MCP ddg-search）**
   ```python
   # 首选：原生 web_search（更稳定、更快速）
   web_search(
       explanation="搜索 Unreal Engine 相关教程和最佳实践",
       searchTerm=construct_network_search_query()
   )
   
   # 备选/补充：MCP ddg-search（当原生搜索结果不足时使用）
   mcp_call_tool(
       serverName="ddg-search",
       toolName="search",
       arguments=json.dumps({
           "query": construct_network_search_query(),
           "max_results": 10
       })
   )
   ```

3. **源码分析**
   ```python
   # 自动进行（基于 config.json）
   analyze_unreal_source_code(
       enginePath=config.unrealEnginePath,
       searchDepth=config.searchDepth,
       focusModules=config.focusModules,
       keywords=extract_source_keywords()
   )
   ```

#### 三层搜索充分性检查（解决问题前建议执行）

在开始生成代码、解决问题之前，建议确认以下条件：

**搜索执行确认：**
- ✅ 是否针对当前问题，执行了足够的一层或多层搜索？
  - 可勾选：@UE5 官方知识库 / 网络搜索 / 源码分析（按实际使用情况）

**信息充分性检查：**
- ✅ 收集到官方推荐方案了吗？（如适用）
- ✅ 找到社区验证的实现方式了吗？（如适用）
- ✅ 了解源码中的关键实现模式了吗？（如适用）
- ✅ 当前信息是否足以开始编码？
- ✅ 是否存在明显遗漏的关键细节？

**对比分析：**
- ✅ 官方、社区、源码方案之间是否存在重要差异？
- ✅ 如有差异，是否理解了原因并作出明确取舍？

在多数情况下，当以上检查项基本满足时，即可开始编码实现；如发现信息明显不足，应优先补充最相关的搜索层后再继续。

#### 不需要用户干预的情况

✅ **以下情况 Skill 自动执行，用户只需等待结果：**

- 用户提问："参考 Unreal 源码，实现一个..."
- 用户提问："@UE5 如何使用 Enhanced Input System？"
- 用户提问："我想优化 Actor Pool，参考 Unreal..."

❌ **不需要等待用户的手动指令**：

- 不需要："请执行 @UE5 查询"
- 不需要："请搜索网络"
- 不需要："请分析源码"

#### Skill 所有者（开发者）应知道的

如果你是在改进这个 Skill，务必确保：

1. **触发机制完善** - 所有相关关键词都能触发 Skill
2. **自动执行流程** - Skill 激活时立即执行三层搜索，不等待用户额外指令
3. **结果综合** - 在生成代码前综合三层搜索的所有结果
4. **清晰输出** - 告诉用户每一步的执行情况和最终结果

---

**提示：** 这是一个通用的代码学习工具，可以用于任何 Unreal 项目。学习的代码模式和最佳实践可以跨项目复用。

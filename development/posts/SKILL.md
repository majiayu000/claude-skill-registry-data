---
title: Claude Code Skill
description: 在 Claude 的生态系统中,**Skill** 和 **MCP (Model Context Protocol)** 是两种为 AI Agent 提供额外能力的机制。<cite/>虽然它们都旨在扩展 Agent 的功能,但它们在设计理念、实现方式和适用场景上有着本质的区别。<cite/>
pubDatetime: 2025-10-17T10:29:00Z
modDatetime: 2025-10-17T10:29:00Z
tags:
  - agent
  - claude code
  - mcp
  - skill
draft: false
featured: false
---
# Skill 与 MCP:Claude Agent 能力扩展的两种方式

## 概述

在 Claude 的生态系统中,**Skill** 和 **MCP (Model Context Protocol)** 是两种为 AI Agent 提供额外能力的机制。<cite/>虽然它们都旨在扩展 Agent 的功能,但它们在设计理念、实现方式和适用场景上有着本质的区别。<cite/>

## 核心定位

### Skill:内部能力扩展

**Skill 是 Claude 专有的模块化扩展系统**,通过动态加载专业化知识和工作流程来提升 Claude 在特定任务上的表现。<cite ref="README.md:0-1"/>

Skill 解决的核心问题是:**如何让 Claude 在特定领域或任务上表现得像一个专家**。<cite/>它通过将指令、脚本和资源注入到 Claude 的上下文中,让 Claude "学习"如何完成特定任务。<cite ref="skill-creator/SKILL.md:11-22"/>

### MCP:外部服务集成

**MCP 是一个开放的标准化协议**,定义了 LLM 如何与外部系统进行结构化交互。<cite ref="mcp-builder/SKILL.md:7-10"/>

MCP 解决的核心问题是:**如何让 LLM 安全、可靠地调用外部 API 和服务**。<cite/>它提供了工具发现、调用和响应的标准化接口。<cite ref="mcp-builder/reference/mcp_best_practices.md:436-441"/>

## 关键区别对比

| 维度 | Skill | MCP |
|------|-------|-----|
| **平台依赖** | Claude 专有 | 开放协议,任何 LLM 可用 |
| **抽象层级** | 应用层 - 教 Claude "怎么做" | 协议层 - 定义 LLM "如何调用" |
| **执行主体** | Claude 自己 | 外部 MCP 服务器 |
| **知识位置** | Claude 上下文内 | 外部服务器 |
| **工作方式** | 阅读→理解→执行 | 调用→等待→接收结果 |
| **状态管理** | 无状态(每次重新加载) | 无状态(独立请求-响应) |
| **复用性** | 通常是单一 Claude 实例使用 | 设计为多客户端复用 |
| **定制程度** | 高度定制(公司/个人专属) | 标准化(通用工具) |

## 上下文管理差异

### MCP:最小化上下文占用

MCP Tool 只将**工具元数据和执行结果**传递给 Agent:<cite/>

- 上下文中只包含工具的名称、描述和输入 schema<cite ref="mcp-builder/reference/mcp_best_practices.md:444-464"/>
- 工具调用后,只返回最终结果(文本或结构化数据)<cite/>
- **不会**将 MCP 服务器的内部实现加载到上下文中<cite/>

**上下文占用示例**:
```
上下文中的内容:
├── Tool 元数据: "slack_send_message" 工具的描述和参数 schema
└── Tool 调用结果: "Message sent successfully"
```

### Skill:渐进式上下文加载

Skill 采用三层渐进式加载机制:<cite ref="skill-creator/SKILL.md:75-83"/>

1. **元数据层**(始终在上下文):约 100 词的 `name` 和 `description`
2. **SKILL.md 正文**(触发时加载):完整的工作流程指令,建议 <5k 词
3. **打包资源**(按需加载):
   - `references/` - 文档和参考资料<cite ref="skill-creator/SKILL.md:56-65"/>
   - `scripts/` - 可执行脚本<cite ref="skill-creator/SKILL.md:47-54"/>
   - `assets/` - 输出文件和模板<cite ref="skill-creator/SKILL.md:67-74"/>

这种设计让 Skill 能够将**完整的指令、工作流程和领域知识**加载到 Claude 的上下文中,使 Claude 能够深度理解并执行复杂任务。<cite/>

**上下文占用示例** (以 `internal-comms` skill 为例):
```
上下文中的内容:
├── 元数据(始终): name="internal-comms", description="..."
├── SKILL.md 正文(触发时): 
│   ├── 何时使用此 skill
│   ├── 如何使用此 skill
│   └── 工作流程指导
└── References(按需):
    ├── examples/3p-updates.md
    ├── examples/company-newsletter.md
    └── examples/faq-answers.md
```

## 实际应用场景

### Skill 的典型应用

- **创意设计**(`canvas-design`):教 Claude 创建视觉艺术<cite/>
- **算法艺术**(`algorithmic-art`):生成可运行的 p5.js HTML 艺术作品<cite ref="algorithmic-art/SKILL.md:301-343"/>
- **内部沟通**(`internal-comms`):教 Claude 按公司格式写状态报告<cite/>
- **品牌指南**(`brand-guidelines`):教 Claude 应用公司品牌规范<cite/>

### MCP 的典型应用

- 让 LLM 调用 Slack API 发送消息
- 让 LLM 查询 GitHub API 获取代码信息
- 让 LLM 操作 Jira API 管理任务

## 概念对应关系

虽然 Skill 和 MCP 都有类似名称的概念,但它们的含义完全不同:<cite/>

### Skill 的组成

- **指令(Instructions)**:SKILL.md 中的 Markdown 内容,提供工作流程指导<cite ref="README.md:0-1"/>
- **脚本(Scripts)**:`scripts/` 目录中的可执行代码<cite ref="skill-creator/SKILL.md:46-53"/>
- **资源(Resources)**:
  - `references/` - 参考文档<cite ref="skill-creator/SKILL.md:55-64"/>
  - `assets/` - 输出文件<cite ref="skill-creator/SKILL.md:66-73"/>

### MCP 的组成

- **Tools(工具)**:MCP 服务器暴露的可执行函数<cite ref="mcp-builder/reference/mcp_best_practices.md:436-441"/>
- **Resources(资源)**:通过 URI 模板访问的数据接口<cite ref="mcp-builder/reference/python_mcp_server.md:553-574"/>
- **Prompts(提示)**:MCP 协议中的提示管理功能<cite/>

**重要提示**:这些概念**不是一一对应的关系**,它们在各自系统中有完全不同的含义和用途。<cite/>

## 执行方式的本质区别

### Skill:Claude 自己阅读并执行

**Skill 的工作流程**:<cite/>
1. 将指令、脚本和资源加载到 Claude 的上下文中<cite ref="skill-creator/SKILL.md:12-15"/>
2. Claude 阅读这些内容后,按照指导**自己完成任务**<cite ref="skill-creator/SKILL.md:78-83"/>
3. 执行主体是 **Claude 本身**<cite/>

**实际示例** - `algorithmic-art` skill:
- 第一步:创建算法哲学(.md 文件)
- 第二步:用 p5.js 代码实现这个哲学(.html + .js 文件)
- 最终产出:用户可以在浏览器中打开并交互的艺术作品<cite ref="algorithmic-art/SKILL.md:337-343"/>

### MCP:调用外部服务执行

**MCP 的工作流程**:<cite/>
1. MCP 服务器提供可调用的工具(tools)<cite ref="mcp-builder/reference/mcp_best_practices.md:437-441"/>
2. Claude 通过协议调用这些工具,**外部服务执行操作**<cite/>
3. 执行主体是 **MCP 服务器**<cite/>

**实际示例** - Slack MCP 服务器:
```
输入: slack_send_message(channel="general", text="Hello")
处理: MCP 服务器调用 Slack API
输出: {"status": "success", "message_id": "123"}
```

## 上下文与状态的关系

### 理解"上下文"和"状态"的区别

**上下文(Context)** - Skill 确实利用:<cite/>
- SKILL.md 正文加载到 Claude 的上下文窗口中<cite ref="skill-creator/SKILL.md:81-82"/>
- `references/` 文件按需加载到上下文<cite ref="skill-creator/SKILL.md:56-65"/>
- Claude 阅读这些上下文内容后,理解如何执行任务<cite/>

**状态(State)** - Skill 不保留:<cite/>
- 每次触发 Skill 时,重新加载 SKILL.md<cite/>
- 不记忆上一次任务的执行结果<cite/>
- 不累积历史信息<cite/>

### 为什么这样设计是合理的

1. **上下文是临时的工作空间**:用于当前任务的知识和指令,任务完成后可以释放<cite/>
2. **无状态保证一致性**:每次使用 Skill 都基于相同的指令,确保行为可重复和可靠<cite/>
3. **类比函数调用**:就像函数可以访问参数(上下文),但不保留局部变量(状态)<cite/>

## Skill 的设计原则

### 自包含性

**Skill 应该是自包含的,不依赖 Claude 当前会话中已有的上下文**:<cite/>

1. **可移植性**:Skill 可能在不同的会话中被触发,不能假设之前的对话内容<cite/>
2. **独立性**:SKILL.md 应该包含**所有必要的信息**来完成任务<cite ref="skill-creator/SKILL.md:156-174"/>
3. **可预测性**:无论何时触发,Skill 的行为应该一致<cite/>

### 写作风格

文档明确要求使用**客观、指令性的语言**:<cite/>

> 使用**命令式/不定式形式**(动词优先的指令),而不是第二人称。使用客观、指令性的语言(例如"要完成 X,执行 Y"而不是"你应该做 X"或"如果你需要做 X")。<cite ref="skill-creator/SKILL.md:166-168"/>

这种写作风格确保 Skill 是**自我描述的**,而不是假设 Claude 已经在某个特定的对话上下文中。<cite/>

## Skill 与 MCP 的协作

### Skill 可以调用 MCP

Skill 和 MCP **不是互斥的,而是可以配合使用的**。<cite/>

Skill 的脚本可以作为 MCP 客户端来调用 MCP 服务器。<cite/>例如,`mcp-builder/scripts/connections.py` 就实现了 MCP 客户端连接逻辑,可以连接到 MCP 服务器、列出可用工具并调用工具。<cite/>

### 何时使用 MCP vs 直接脚本

**使用 MCP 的场景**:<cite/>
- 多个 LLM 客户端需要访问同一服务
- 需要标准化的工具接口和错误处理
- 希望工具可以被其他 MCP 客户端复用
- 需要跨平台的标准化接口

**直接使用脚本的场景**:<cite/>
- 操作是 Skill 专有的,不需要被其他系统调用
- 脚本逻辑简单,直接执行即可
- 不需要复杂的工具发现机制
- 不需要跨平台的标准化接口

## 能力包含关系

### Skill 理论上可以实现 MCP 的所有功能

**从能力角度看,Skill 理论上可以完成 MCP 能完成的所有事情**:<cite/>

1. **直接调用外部 API**:Skill 的脚本可以直接使用 HTTP 客户端调用 Slack、GitHub、Jira 等 API<cite ref="skill-creator/SKILL.md:46-54"/>
2. **作为 MCP 客户端**:Skill 的脚本甚至可以作为 MCP 客户端来调用 MCP 服务器<cite/>

### 设计目标的差异

虽然 Skill **能做** MCP 能做的事,但它们的**设计目标**不同:<cite/>

**MCP 的设计目标**:标准化和复用<cite/>
- 开放协议:任何 LLM 都可以使用<cite ref="mcp-builder/SKILL.md:8-10"/>
- 标准化接口:工具发现、调用都有统一规范<cite ref="mcp-builder/reference/mcp_best_practices.md:439-441"/>
- 独立服务:MCP 服务器是独立运行的进程,可以被多个客户端同时使用<cite/>

**Skill 的设计目标**:Claude 专属定制<cite/>
- Claude


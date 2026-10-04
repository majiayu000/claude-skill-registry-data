---
skill_name: dify-master
version: 1.0.0
author: Dify SKILL Team
description: Dify 工作流和插件开发的完整技能体系 - 模块化、渐进式、实用导向
category: development
tags:
  - dify
  - workflow
  - plugin
  - ai
  - llm
  - rag
  - agent
dependencies: []
last_updated: 2026-03-05
triggers:
  - dify
  - 工作流
  - workflow
  - 插件
  - plugin
  - 性能
  - performance
  - 安全
  - security
  - 集成
  - integration
  - api
  - mcp
  - 参考
  - reference
  - dsl
  - sdk
  - cli
on_demand:
  # 按需加载条件触发器
  conditions:
    - when: "用户提到具体节点类型（如 LLM、Agent、HTTP Request）"
      load: "01-workflow/SKILL.md"
    - when: "用户提到插件开发、工具、Provider"
      load: "02-plugin/SKILL.md"
    - when: "用户提到性能优化、缓存、并行"
      load: "03-performance/SKILL.md"
    - when: "用户提到安全、部署、Docker"
      load: "04-security/SKILL.md"
    - when: "用户提到 API、Webhook、MCP、数据库集成"
      load: "05-integration/SKILL.md"
    - when: "用户查找语法参考、API 文档、SDK"
      load: "06-reference/SKILL.md"
---

# Dify Master SKILL

> 一个模块化、渐进式披露的 Dify 开发技能体系

## 快速导航

- [什么是 Dify](#什么是-dify)
- [SKILL 体系概览](#skill-体系概览)
- [快速开始](#快速开始)
- [子 SKILL 索引](#子-skill-索引)
- [常用参考](#常用参考)

---

## 什么是 Dify

Dify 是一个开源的 LLMOps 平台，提供可视化的工作流编排和强大的插件系统，帮助开发者快速构建和部署 AI 应用。

### 核心特性

- **可视化工作流**: 拖拽式编排，无需编码即可构建复杂 AI 应用
- **插件系统**: 支持工具、模型、数据源等多种插件类型
- **生产就绪**: 从本地开发到大规模分布式部署的完整支持
- **开源生态**: 114K+ GitHub Stars，活跃的社区和丰富的插件市场

### 技术架构

- **Beehive 架构**: 模块化、可扩展的系统设计
- **队列驱动图引擎**: 事件驱动、并行执行、高性能
- **多运行时支持**: Local、Debug、Serverless 三种运行模式
- **MCP 协议集成**: 与 Claude 等 AI 助手的标准化集成

---

## SKILL 体系概览

Dify Master SKILL 采用模块化设计，包含 6 个核心子 SKILL，覆盖从开发到部署的完整流程。

```
dify-master (总入口)
├── 01-workflow      # 工作流设计
├── 02-plugin        # 插件开发
├── 03-performance   # 性能优化
├── 04-security      # 安全和部署
├── 05-integration   # 集成和扩展
└── 06-reference     # 参考资料
```

### 设计理念

1. **模块化**: 每个子 SKILL 独立完整，可单独使用
2. **渐进式披露**: 从概览到细节，按需深入
3. **上下文优化**: 最小化单次加载的内容量
4. **实用导向**: 提供可直接使用的代码和配置

---

## 快速开始

### 场景 1: 创建第一个工作流

```yaml
# 简单问答工作流
workflow:
  graph:
    nodes:
    - data:
        type: start
        variables: []
      id: start

    - data:
        type: llm
        model:
          provider: openai
          name: gpt-4
        prompt_template:
        - role: system
          text: "你是一个助手"
        - role: user
          text: "{{#sys.query#}}"
      id: llm

    - data:
        type: answer
        answer: "{{#llm.text#}}"
      id: answer

    edges:
    - source: start
      target: llm
    - source: llm
      target: answer
```

**下一步**: 学习 [01-workflow SKILL](./01-workflow/SKILL.md) 了解更多节点类型和设计模式

### 场景 2: 开发第一个插件

```python
# 简单工具插件
from typing import Any, Generator
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin import Tool

class MyTool(Tool):
    def _invoke(
        self,
        tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        # 获取参数
        input_text = tool_parameters.get("text", "")

        # 处理逻辑
        result = input_text.upper()

        # 返回结果
        yield self.create_text_message(result)
```

**下一步**: 学习 [02-plugin SKILL](./02-plugin/SKILL.md) 了解完整的插件开发流程

### 场景 3: 优化工作流性能

```yaml
# 使用并行分支提升性能
- data:
    type: parallel
    branches:
    - nodes: [tool1, process1]
    - nodes: [tool2, process2]
    - nodes: [tool3, process3]
  id: parallel_execution
```

**下一步**: 学习 [03-performance SKILL](./03-performance/SKILL.md) 了解更多优化技术

---

## 子 SKILL 索引

### 01. 工作流设计 SKILL

**适用场景**: 设计和开发 Dify 工作流

**触发关键词**: `节点`, `LLM`, `Agent`, `工作流`, `变量`, `知识检索`, `HTTP Request`, `Code`, `If-Else`, `Iteration`, `模板`, `DSL`, `YAML`

**核心内容**:
- 10+ 节点类型详解 (Start, LLM, Agent, Knowledge Retrieval, Code, HTTP Request, Tool, If-Else, Iteration, Answer)
- 5 种设计模式 (顺序管道、条件分支、迭代处理、知识检索、多源聚合)
- 开箱即用的工作流模板
- 变量系统和引用语法
- 最佳实践和常见问题

**快速访问**: [01-workflow/SKILL.md](./01-workflow/SKILL.md)

**推荐给**: 工作流设计者、AI 应用开发者、产品经理

---

### 02. 插件开发 SKILL

**适用场景**: 开发自定义工具、模型、数据源插件

**触发关键词**: `插件`, `plugin`, `Tool`, `Provider`, `开发`, `manifest`, `OAuth`, `数据源`, `模型`, `扩展`

**核心内容**:
- 4 种插件类型 (Tool, Model, Datasource, Extension)
- 完整的开发流程 (初始化、实现、测试、打包、发布)
- 标准项目结构和配置文件
- Provider 和 Tool 开发指南
- 插件模板和代码示例
- 测试策略和调试技巧

**快速访问**: [02-plugin/SKILL.md](./02-plugin/SKILL.md)

**推荐给**: 插件开发者、后端工程师、工具集成者

---

### 03. 性能优化 SKILL

**适用场景**: 优化工作流和插件的执行性能

**触发关键词**: `性能`, `performance`, `优化`, `缓存`, `并行`, `延迟`, `吞吐量`, `监控`, `benchmark`

**核心内容**:
- 工作流优化 (图结构、并行执行、变量池)
- LLM 优化 (模型选择、Prompt 工程、缓存、结构化输出)
- 插件优化 (运行时选择、资源限制、异步处理)
- 监控和分析工具
- 性能基准测试

**快速访问**: [03-performance/SKILL.md](./03-performance/SKILL.md)

**推荐给**: 性能工程师、架构师、运维人员

---

### 04. 安全和部署 SKILL

**适用场景**: 生产环境部署和安全加固

**触发关键词**: `安全`, `security`, `部署`, `deploy`, `Docker`, `Kubernetes`, `SSL`, `认证`, `授权`, `沙箱`, `SSRF`

**核心内容**:
- 安全实践 (SSRF 防护、沙箱隔离、数据加密、认证授权)
- 部署指南 (Docker Compose, Kubernetes, Serverless, 高可用)
- 运维实践 (监控、日志、备份、故障排查)
- 环境配置和资源规划
- 最佳实践和案例

**快速访问**: [04-security/SKILL.md](./04-security/SKILL.md)

**推荐给**: DevOps 工程师、安全工程师、系统管理员

---

### 05. 集成和扩展 SKILL

**适用场景**: 与外部系统和服务集成

**触发关键词**: `集成`, `integration`, `API`, `Webhook`, `MCP`, `Server`, `Client`, `数据库`, `Redis`, `消息队列`, `RabbitMQ`, `Kafka`, `S3`

**核心内容**:
- API 集成 (REST API, Webhook, Streaming)
- MCP 协议 (MCP Server, MCP Client, 双向通信)
- 外部服务 (数据库、存储、消息队列)
- 集成案例和最佳实践
- 故障排查和调试

**快速访问**: [05-integration/SKILL.md](./05-integration/SKILL.md)

**推荐给**: 集成工程师、全栈开发者、架构师

---

### 06. 参考资料 SKILL

**适用场景**: 查找语法、API、CLI 等参考信息

**触发关键词**: `参考`, `reference`, `API`, `SDK`, `CLI`, `DSL`, `YAML`, `命令`, `文档`, `语法`

**核心内容**:
- DSL 语法参考 (完整的 YAML 结构和字段说明)
- API 参考 (RESTful API 接口文档)
- SDK 参考 (Python SDK 类和方法)
- CLI 参考 (dify 命令行工具)
- 常见问题和解决方案
- 学习资源和社区链接

**快速访问**: [06-reference/SKILL.md](./06-reference/SKILL.md)

**推荐给**: 所有 Dify 开发者

---

## 常用参考

### 变量引用语法

```yaml
# 系统变量
{{#sys.query#}}              # 用户查询
{{#sys.files#}}              # 上传的文件
{{#sys.conversation_id#}}    # 会话 ID

# 节点输出
{{#节点ID.输出字段#}}         # 引用节点输出
{{#llm.text#}}               # LLM 文本输出
{{#knowledge.result#}}       # 知识检索结果

# 会话变量
{{#conversation.变量名#}}     # 会话级变量

# 迭代变量
{{#item#}}                   # 当前迭代项
{{#index#}}                  # 当前索引
```

### 常用节点配置

```yaml
# LLM 节点
- data:
    type: llm
    model:
      provider: openai
      name: gpt-4
      completion_params:
        temperature: 0.7
        max_tokens: 2000
    prompt_template:
    - role: system
      text: "系统提示"
    - role: user
      text: "{{#sys.query#}}"
    context:
      enabled: true
      variable_selector: ["knowledge", "result"]

# Agent 节点
- data:
    type: agent
    agent_parameters:
      instruction:
        value: "根据用户需求调用工具"
      model:
        value:
          provider: openai
          model: gpt-4
      query:
        value: "{{#sys.query#}}"
      tools:
        value:
        - enabled: true
          provider_name: time
          tool_name: current_time
          type: builtin
    agent_strategy_name: function_calling

# 知识检索节点
- data:
    type: knowledge-retrieval
    dataset_ids: ["dataset-id"]
    query_variable_selector: ["start", "sys.query"]
    retrieval_mode: single
    single_retrieval_config:
      model:
        provider: openai
        name: text-embedding-3-small
      top_k: 3
      score_threshold: 0.7
```

### 插件配置模板

```yaml
# manifest.yaml
version: 0.0.1
type: plugin
author: your-name
name: plugin-name
label:
  en_US: Plugin Name
  zh_Hans: 插件名称
description:
  en_US: Plugin description
  zh_Hans: 插件描述
icon: icon.svg

resource:
  memory: 268435456  # 256MB

plugins:
  tools:
    - provider/provider.yaml

meta:
  version: 0.0.1
  arch: [amd64, arm64]
  runner:
    language: python
    version: "3.12"
    entrypoint: main

tags:
  - utilities
```

### CLI 常用命令

```bash
# 插件开发
dify plugin init                    # 初始化插件项目
dify plugin run                     # 本地调试插件
dify plugin package                 # 打包插件
dify plugin publish                 # 发布插件

# 工作流管理
dify workflow export <id>           # 导出工作流
dify workflow import <file>         # 导入工作流
dify workflow validate <file>       # 验证工作流

# 环境管理
dify env list                       # 列出环境变量
dify env set <key> <value>          # 设置环境变量
dify env get <key>                  # 获取环境变量
```

---

## 学习路径

### 新手路径 (0-1 周)

1. 阅读本 SKILL 了解 Dify 全貌
2. 学习 [01-workflow SKILL](./01-workflow/SKILL.md) 掌握工作流基础
3. 使用模板创建第一个工作流
4. 在 Dify 平台上测试和调试

### 进阶路径 (1-4 周)

1. 深入学习 [01-workflow SKILL](./01-workflow/SKILL.md) 的设计模式
2. 学习 [02-plugin SKILL](./02-plugin/SKILL.md) 开发自定义插件
3. 学习 [03-performance SKILL](./03-performance/SKILL.md) 优化性能
4. 构建实际项目并部署

### 专家路径 (1-3 个月)

1. 掌握所有子 SKILL 的内容
2. 学习 [04-security SKILL](./04-security/SKILL.md) 进行生产部署
3. 学习 [05-integration SKILL](./05-integration/SKILL.md) 集成外部系统
4. 参与社区贡献和最佳实践分享

---

## 获取帮助

### 官方资源

- **官方文档**: https://docs.dify.ai/
- **GitHub**: https://github.com/langgenius/dify
- **插件市场**: https://marketplace.dify.ai/
- **官方博客**: https://dify.ai/blog/

### 社区资源

- **Discord**: https://discord.gg/FngNHpbcY7
- **Reddit**: https://reddit.com/r/difyai
- **中文社区**: https://github.com/langgenius/dify/discussions

### SKILL 支持

- **架构文档**: [ARCHITECTURE.md](./ARCHITECTURE.md)
- **问题反馈**: 通过 GitHub Issues 提交
- **贡献指南**: 参与 SKILL 内容的改进和扩展

---

## 版本信息

- **当前版本**: v1.1.0
- **最后更新**: 2026-03-05
- **Dify 兼容版本**: 0.15.x - 1.9.x
- **更新内容**: 完善 05-integration 和 06-reference SKILL，添加按需加载机制
- **下一版本计划**: v1.2.0 (增加更多模板和案例)

---

## 许可证

本 SKILL 基于 MIT 许可证开源，欢迎使用、修改和分发。

---

**开始你的 Dify 开发之旅吧！选择一个子 SKILL 深入学习，或直接使用模板快速开始。**

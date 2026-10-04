---
skill_name: dify-workflow
version: 1.0.0
parent_skill: dify-master
description: Dify 工作流设计完整指南 - 节点类型、设计模式、模板和最佳实践
category: workflow
tags:
  - workflow
  - nodes
  - design-patterns
  - templates
dependencies: []
last_updated: 2026-03-04
---

# Dify 工作流设计 SKILL

> 掌握 Dify 工作流设计的核心知识和最佳实践

## 快速导航

- [工作流概述](#工作流概述)
- [核心节点类型](#核心节点类型)
- [设计模式](#设计模式)
- [工作流模板](#工作流模板)
- [变量系统](#变量系统)
- [最佳实践](#最佳实践)

---

## 工作流概述

Dify 工作流是一个可视化的 AI 应用编排系统，通过节点和边的组合，实现复杂的业务逻辑。

### 核心概念

- **节点 (Node)**: 工作流的基本执行单元，每个节点执行特定的功能
- **边 (Edge)**: 连接节点，定义数据流和执行顺序
- **变量 (Variable)**: 在节点间传递数据
- **DSL (Domain Specific Language)**: YAML 格式的工作流定义语言

### 工作流类型

1. **Workflow**: 标准工作流，适合复杂的多步骤处理
2. **Advanced Chat**: 高级对话应用，支持工作流编排
3. **Agent**: 智能代理，自主决策和工具调用

### 执行模型

- **队列驱动**: 基于 Ready Queue 的节点调度
- **事件驱动**: 节点执行产生事件流
- **并行执行**: 支持 2-8 个工作线程并行处理
- **流式响应**: 支持实时流式输出

---

## 核心节点类型

### 1. Start 节点

**功能**: 工作流的入口，定义输入变量

**配置示例**:
```yaml
- data:
    desc: ''
    selected: false
    title: 开始
    type: start
    variables:
    - label: 用户输入
      max_length: 1000
      required: true
      type: text-input
      variable: user_input
  id: start
  type: custom
```

**详细文档**: [nodes/start.md](./nodes/start.md)

---

### 2. LLM 节点

**功能**: 调用大语言模型进行推理和生成

**配置示例**:
```yaml
- data:
    type: llm
    model:
      provider: openai
      name: gpt-4
      completion_params:
        temperature: 0.7
        max_tokens: 2000
    prompt_template:
    - id: system
      role: system
      text: "你是一个专业的助手"
    - id: user
      role: user
      text: "{{#sys.query#}}"
    context:
      enabled: true
      variable_selector: ["knowledge", "result"]
  id: llm
```

**关键参数**:
- `model`: 模型配置（提供商、名称、参数）
- `prompt_template`: 提示词模板（支持系统消息和用户消息）
- `context`: 上下文配置（启用知识库检索结果）
- `memory`: 对话记忆配置
- `vision`: 视觉能力配置（支持图像输入）

**详细文档**: [nodes/llm.md](./nodes/llm.md)

---

### 3. Agent 节点

**功能**: 智能代理，根据用户需求自主调用工具

**配置示例**:
```yaml
- data:
    type: agent
    agent_parameters:
      instruction:
        type: constant
        value: "根据用户需求，调用合适的工具完成任务"
      model:
        type: constant
        value:
          provider: openai
          model: gpt-4
          completion_params:
            temperature: 0.7
      query:
        type: constant
        value: "{{#sys.query#}}"
      tools:
        type: constant
        value:
        - enabled: true
          provider_name: time
          tool_name: current_time
          type: builtin
        - enabled: true
          provider_name: duckduckgo
          tool_name: ddgo_search
          type: builtin
    agent_strategy_name: function_calling
  id: agent
```

**支持的策略**:
- `function_calling`: 函数调用（推荐）
- `react`: ReAct 推理模式

**详细文档**: [nodes/agent.md](./nodes/agent.md)

---

### 4. Knowledge Retrieval 节点

**功能**: 从知识库检索相关信息（RAG）

**配置示例**:
```yaml
- data:
    type: knowledge-retrieval
    dataset_ids:
    - "dataset-uuid-1"
    - "dataset-uuid-2"
    query_variable_selector: ["start", "sys.query"]
    retrieval_mode: single
    single_retrieval_config:
      model:
        provider: openai
        name: text-embedding-3-small
      top_k: 3
      score_threshold: 0.7
      reranking_model:
        provider: cohere
        model: rerank-english-v2.0
  id: knowledge
```

**检索模式**:
- `single`: 单次检索
- `multiple`: 多次检索

**详细文档**: [nodes/knowledge-retrieval.md](./nodes/knowledge-retrieval.md)

---

### 5. Code 节点

**功能**: 执行 Python 或 JavaScript 代码

**配置示例**:
```yaml
- data:
    type: code
    code_language: python3
    code: |
      def main(input_text: str) -> dict:
          # 处理逻辑
          result = input_text.upper()
          return {
              "output": result,
              "length": len(result)
          }
    variables:
    - variable: input_text
      value_selector: ["start", "user_input"]
    outputs:
      output:
        type: string
      length:
        type: number
  id: code
```

**支持的语言**:
- Python 3
- JavaScript (Node.js)

**详细文档**: [nodes/code.md](./nodes/code.md)

---

### 6. HTTP Request 节点

**功能**: 调用外部 HTTP API

**配置示例**:
```yaml
- data:
    type: http-request
    method: POST
    url: "https://api.example.com/endpoint"
    headers:
      Content-Type: application/json
      Authorization: "Bearer {{#env.API_KEY#}}"
    body:
      type: json
      data:
        query: "{{#sys.query#}}"
        options:
          temperature: 0.7
    timeout: 30
  id: http
```

**支持的方法**:
- GET, POST, PUT, DELETE, PATCH

**详细文档**: [nodes/http-request.md](./nodes/http-request.md)

---

### 7. Tool 节点

**功能**: 调用内置或自定义工具

**配置示例**:
```yaml
- data:
    type: tool
    provider_id: google_translate
    provider_type: builtin
    provider_name: google_translate
    tool_name: translate
    tool_parameters:
      content:
        type: mixed
        value: "{{#sys.query#}}"
      dest:
        type: mixed
        value: "zh-CN"
  id: tool
```

**工具类型**:
- `builtin`: 内置工具
- `api`: API 工具
- `workflow`: 工作流工具

**详细文档**: [nodes/tool.md](./nodes/tool.md)

---

### 8. If-Else 节点

**功能**: 条件分支控制

**配置示例**:
```yaml
- data:
    type: if-else
    conditions:
    - variable_selector: ["llm", "text"]
      comparison_operator: contains
      value: "关键词"
    logical_operator: and
  id: condition
```

**支持的运算符**:
- `contains`, `not contains`
- `is`, `is not`
- `empty`, `not empty`
- `>`, `<`, `>=`, `<=`, `=`, `!=`

**详细文档**: [nodes/if-else.md](./nodes/if-else.md)

---

### 9. Iteration 节点

**功能**: 迭代处理数组数据

**配置示例**:
```yaml
- data:
    type: iteration
    iterator_selector: ["start", "items"]
    output_selector: ["iteration_inner", "output"]
    parallel_nums: 3
    error_handle_mode: continue
  id: iteration
```

**错误处理模式**:
- `continue`: 继续执行
- `stop`: 停止迭代

**详细文档**: [nodes/iteration.md](./nodes/iteration.md)

---

### 10. Answer 节点

**功能**: 输出工作流结果

**配置示例**:
```yaml
- data:
    type: answer
    answer: "{{#llm.text#}}"
  id: answer
```

**详细文档**: [nodes/answer.md](./nodes/answer.md)

---

## 设计模式

### 1. 顺序管道模式

**适用场景**: 简单的线性处理流程

**结构**:
```
Start → LLM → Answer
```

**示例**: [patterns/sequential.md](./patterns/sequential.md)

---

### 2. 条件分支模式

**适用场景**: 根据条件执行不同的处理逻辑

**结构**:
```
Start → LLM → If-Else → [分支A / 分支B] → Answer
```

**示例**: [patterns/conditional.md](./patterns/conditional.md)

---

### 3. 迭代处理模式

**适用场景**: 批量处理数组数据

**结构**:
```
Start → Code → Iteration → LLM → Answer
```

**示例**: [patterns/iterative.md](./patterns/iterative.md)

---

### 4. 知识检索模式 (RAG)

**适用场景**: 基于知识库的问答

**结构**:
```
Start → Knowledge Retrieval → LLM (with context) → Answer
```

**示例**: [patterns/rag.md](./patterns/rag.md)

---

### 5. 多源聚合模式

**适用场景**: 整合多个数据源的信息

**结构**:
```
Start → [Tool1, Tool2, HTTP] → Variable Aggregator → LLM → Answer
```

**示例**: [patterns/aggregation.md](./patterns/aggregation.md)

---

## 工作流模板

### 简单问答

**文件**: [templates/simple-qa.yml](./templates/simple-qa.yml)

**描述**: 最基础的问答工作流

**节点**: Start → LLM → Answer

---

### RAG 助手

**文件**: [templates/rag-assistant.yml](./templates/rag-assistant.yml)

**描述**: 基于知识库的智能助手

**节点**: Start → Knowledge Retrieval → LLM → Answer

---

### Agent 工具调用

**文件**: [templates/agent-tools.yml](./templates/agent-tools.yml)

**描述**: 智能代理自主调用工具

**节点**: Start → Agent → Answer

---

### 多步骤处理

**文件**: [templates/multi-step.yml](./templates/multi-step.yml)

**描述**: 复杂的多步骤处理流程

**节点**: Start → Code → HTTP → LLM → If-Else → Answer

---

## 变量系统

### 系统变量

```yaml
{{#sys.query#}}              # 用户查询
{{#sys.files#}}              # 上传的文件
{{#sys.conversation_id#}}    # 会话 ID
{{#sys.user_id#}}            # 用户 ID
```

### 节点变量

```yaml
{{#节点ID.输出字段#}}         # 引用节点输出
{{#llm.text#}}               # LLM 文本输出
{{#knowledge.result#}}       # 知识检索结果
{{#code.output#}}            # 代码节点输出
```

### 会话变量

```yaml
{{#conversation.变量名#}}     # 会话级变量
```

### 环境变量

```yaml
{{#env.API_KEY#}}            # 环境变量
{{#env.DATABASE_URL#}}       # 数据库连接
```

### 迭代变量

```yaml
{{#item#}}                   # 当前迭代项
{{#index#}}                  # 当前索引
```

---

## 最佳实践

### 1. 模块化设计

- 将复杂流程拆分为多个独立节点
- 使用变量传递数据，避免硬编码
- 合理使用条件分支和迭代节点

### 2. 变量命名规范

- 使用有意义的变量名
- 遵循统一的命名约定
- 添加必要的描述信息

### 3. 错误处理

- 在关键节点添加错误处理逻辑
- 使用条件分支处理异常情况
- 提供友好的错误提示

### 4. 性能优化

- 避免不必要的节点调用
- 合理使用缓存机制
- 控制循环迭代次数
- 使用并行分支提升性能

### 5. 可维护性

- 添加节点描述和注释
- 使用清晰的节点命名
- 保持工作流结构简洁
- 定期审查和优化

**详细内容**: [best-practices.md](./best-practices.md)

---

## 下一步

- 深入学习 [节点类型详解](./nodes/)
- 探索 [设计模式](./patterns/)
- 使用 [工作流模板](./templates/) 快速开始
- 阅读 [最佳实践](./best-practices.md) 提升技能

---

## 相关 SKILL

- [02-plugin SKILL](../02-plugin/SKILL.md) - 开发自定义工具和插件
- [03-performance SKILL](../03-performance/SKILL.md) - 优化工作流性能
- [06-reference SKILL](../06-reference/SKILL.md) - DSL 语法参考

---

**版本**: v1.0.0
**最后更新**: 2026-03-04
**返回**: [总 SKILL](../SKILL.md)

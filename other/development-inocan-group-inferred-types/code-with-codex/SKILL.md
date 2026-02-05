---
name: code-with-codex
description: "Write and generate code using memex-cli with Codex backend. Use when (1) Generating code files and scripts, (2) Refactoring existing code, (3) Writing tests, (4) Creating project scaffolds, (5) Implementing algorithms or features, (6) Code review and optimization, (7) Complex multi-file projects."
---

# Code with Codex

Use memex-cli to leverage Codex for code generation with memory and replay support.

## Model Selection Guide

| Model | Provider | Best For | Complexity |
|-------|----------|----------|------------|
| gpt-5-mini | github_copilot | Simple scripts, quick fixes | ⭐ |
| gpt-5.1-codex | aduib_ai | General coding, utilities | ⭐⭐ |
| grok-4-1-fast-reasoning | x-ai | Balanced quality/speed | ⭐⭐⭐ |
| deepseek-reasoner | aduib_ai | Complex logic, algorithms | ⭐⭐⭐⭐ |
| gpt-5.2 | github_copilot | Architecture, system design | ⭐⭐⭐⭐⭐ |

## Scenarios by Complexity

### Level 1: Simple Scripts

Quick utilities, single-file scripts, simple automation.

```bash
# Hello world / basic syntax
memex-cli run --backend "codex" --model "gpt-5-mini" --model-provider "github_copilot" --prompt "Python脚本：批量重命名文件，添加日期前缀" --stream-format "text"

# Simple data processing
memex-cli run --backend "codex" --model "gpt-5-mini" --model-provider "github_copilot" --prompt "读取CSV文件，统计每列的空值数量" --stream-format "text"

# Basic CLI tool
memex-cli run --backend "codex" --model "gpt-5-mini" --model-provider "github_copilot" --prompt "Bash脚本：监控磁盘空间，超过80%发送告警" --stream-format "text"
```

### Level 2: Utility Functions

Helper functions, data transformations, format conversions.

```bash
# Data validation
memex-cli run --backend "codex" --model "gpt-5.1-codex" --model-provider "aduib_ai" --prompt "编写邮箱、手机号、身份证号验证函数集合" --stream-format "text"

# Format conversion
memex-cli run --backend "codex" --model "gpt-5.1-codex" --model-provider "aduib_ai" --prompt "JSON/YAML/TOML格式互转工具类" --stream-format "text"

# String processing
memex-cli run --backend "codex" --model "gpt-5.1-codex" --model-provider "aduib_ai" --prompt "实现模板字符串解析器，支持变量替换和条件渲染" --stream-format "text"
"
### Level 3: Single Module

Complete modules with error handling, logging, tests.

```bash
# REST client
memex-cli run --backend "codex" --model "grok-4-1-fast-reasoning" --model-provider "x-ai" --prompt "Python HTTP客户端封装，支持重试、超时、拦截器" --stream-format "text"

# Database helper
memex-cli run --backend "codex" --model "grok-4-1-fast-reasoning" --model-provider "x-ai" --prompt "SQLite工具类：连接池、事务管理、查询构建器" --stream-format "jsonl"

# File watcher
memex-cli run --backend "codex" --model "grok-4-1-fast-reasoning" --model-provider "x-ai" --prompt "目录监控服务，检测文件变更并触发回调，支持过滤规则" --stream-format "text"
```

### Level 4: Algorithm Implementation

Complex algorithms, data structures, performance-critical code.

```bash
# Data structures
memex-cli run --backend "codex" --model "deepseek-reasoner" --model-provider "aduib_ai" --prompt "实现跳表SkipList，支持插入、删除、范围查询，O(logN)复杂度" --stream-format "text"

# Graph algorithms
memex-cli run --backend "codex" --model "deepseek-reasoner" --model-provider "aduib_ai" --prompt "实现Dijkstra和A*寻路算法，支持动态权重和障碍物" --stream-format "jsonl"

# Concurrent programming
memex-cli run --backend "codex" --model "deepseek-reasoner" --model-provider "aduib_ai" --prompt "实现无锁并发队列，支持多生产者多消费者" --stream-format "text"

# Parser / Compiler
memex-cli run --backend "codex" --model "deepseek-reasoner" --model-provider "aduib_ai" --prompt "实现简单的表达式解析器，支持四则运算、括号、变量" --stream-format "jsonl"
```

### Level 5: System Design & Architecture

Multi-module projects, microservices, complete applications.

```bash
# API service
memex-cli run --backend "codex" --model "gpt-5.2" --model-provider "github_copilot" --prompt "设计并实现用户认证微服务：JWT、OAuth2、RBAC权限模型" --stream-format "jsonl"

# Event-driven system
memex-cli run --backend "codex" --model "gpt-5.2" --model-provider "github_copilot" --prompt "设计事件驱动架构：消息队列、事件溯源、CQRS模式实现" --stream-format "jsonl"

# Plugin system
memex-cli run --backend "codex" --model "gpt-5.2" --model-provider "github_copilot" --prompt "设计可扩展插件系统：插件发现、生命周期管理、依赖注入" --stream-format "jsonl"

# Distributed system
memex-cli run --backend "codex" --model "gpt-5.2" --model-provider "github_copilot" --prompt "设计分布式任务调度系统：任务分片、故障转移、负载均衡" --stream-format "jsonl"
"
## Special Tasks

### Unit Testing

```bash
# Basic tests
memex-cli run --backend "codex" --model "gpt-5.1-codex" --model-provider "aduib_ai" --prompt "为计算器模块编写pytest测试用例" --stream-format "text"

# Comprehensive tests
memex-cli run --backend "codex" --model "grok-4-1-fast-reasoning" --model-provider "x-ai" --prompt "为用户服务编写完整测试：单元测试、集成测试、Mock外部依赖" --stream-format "jsonl"
```

### Code Review & Refactoring

```bash
# Code review
memex-cli run --backend "codex" --model "grok-4-1-fast-reasoning" --model-provider "x-ai" --prompt "审查这段代码：指出问题、安全隐患、性能瓶颈、改进建议" --stream-format "text"

# Refactoring
memex-cli run --backend "codex" --model "grok-4-1-fast-reasoning" --model-provider "x-ai" --prompt "重构这段代码：应用设计模式，提取公共逻辑，改善可测试性" --stream-format "text"
```

### Documentation

```bash
# API docs
memex-cli run --backend "codex" --model "gpt-5.1-codex" --model-provider "aduib_ai" --prompt "为这个模块生成API文档，包含函数签名、参数说明、使用示例" --stream-format "text"

# Architecture docs
memex-cli run --backend "codex" --model "gpt-5.1-codex" --model-provider "aduib_ai" --prompt "生成系统架构文档：模块关系图、数据流、部署架构" --stream-format "text"
```

## Workflow

### Iterative Development

```bash
# Step 1: Initial implementation
memex-cli run --backend "codex" --model "gpt-5.1-codex" --model-provider "aduib_ai" --prompt "实现用户注册功能" --stream-format "jsonl"

# Step 2: Review events
memex-cli replay --events ./run.events.jsonl --format text

# Step 3: Add features
memex-cli resume --run-id <RUN_ID> --backend "codex" --model "gpt-5.1-codex" --model-provider "aduib_ai" --prompt "添加邮箱验证和密码强度检查" --stream-format "jsonl"

# Step 4: Add tests
memex-cli resume --run-id <RUN_ID> --backend "codex" --model "gpt-5.1-codex" --model-provider "aduib_ai" --prompt "为注册功能编写单元测试" --stream-format "text"
"""
```

## Tips

1. **Match model to task**: Use lightweight models for simple tasks, save powerful models for complex logic
2. **Specify output file**: Add "写入文件xxx.py" to prompt for direct file creation
3. **Use jsonl for complex tasks**: Enables full audit trail and iterative refinement
4. **Break down large tasks**: Use resume to build features incrementally
5. **Include context**: Specify language, framework, coding standards in prompts
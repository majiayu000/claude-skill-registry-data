---
name: code-splitter-adapter
description: 使用适配器模式和工厂模式封装 LangChain 和 LlamaIndex 中的代码切分工具，对外提供统一的调用接口。
---

# 代码切分工具适配器技能

## 概述

此技能使用适配器模式和工厂模式，对 LangChain 和 LlamaIndex 中的代码切分工具进行标准化封装，对外提供统一的调用接口。它支持多种编程语言的代码切分，可以根据需要选择不同的切分策略。

## 核心功能

- **统一接口**：提供统一的 `split_code` 方法，屏蔽底层实现差异
- **多策略支持**：支持 LangChain 和 LlamaIndex 两种切分策略
- **多语言支持**：支持多种编程语言的代码切分
- **错误处理**：对 LlamaIndex 解析失败的情况提供友好的错误信息
- **元数据支持**：支持附加元数据到切分后的代码片段

## 工作流程

### 步骤 1：选择切分策略

用户可以选择使用 LangChain 或 LlamaIndex 的切分策略。

### 步骤 2：配置切分参数

根据需要配置切分参数，如 chunk_size、chunk_overlap 等。

### 步骤 3：调用切分方法

使用统一的 `split_code` 方法切分代码。

### 步骤 4：获取切分结果

获取标准化格式的切分结果。

## 使用示例

### 基本使用

```python
from code_splitter import get_code_splitter

# 使用 LangChain 策略
langchain_splitter = get_code_splitter(strategy="langchain", chunk_size=1000, chunk_overlap=200)
result = langchain_splitter.split_code(
    code="def foo():\n    pass\n\nclass Bar:\n    pass",
    language="python",
    metadata={"source": "utils.py"}
)

# 使用 LlamaIndex 策略
llamaindex_splitter = get_code_splitter(strategy="llamaindex")
result = llamaindex_splitter.split_code(
    code="def foo():\n    pass\n\nclass Bar:\n    pass",
    language="python",
    metadata={"source": "utils.py"}
)
```

### 命令行使用

```bash
python /mnt/skills/custom/program_snippet/code-splitter-adapter/scripts/split.py \
  --strategy langchain \
  --code "def foo():\n    pass\n\nclass Bar:\n    pass" \
  --language python \
  --metadata '{"source": "utils.py"}'
```

## 参数

| 参数 | 描述 |
|------|------|
| `strategy` | 切分策略，可选值为 "langchain" 或 "llamaindex" |
| `code` | 要切分的代码字符串 |
| `language` | 代码的编程语言 |
| `metadata` | 附加的元数据 |
| `chunk_size` | 切分后的代码块大小（仅 LangChain 策略） |
| `chunk_overlap` | 代码块之间的重叠大小（仅 LangChain 策略） |

## 支持的编程语言

### LangChain 支持的语言

- python
- java
- javascript
- typescript
- html
- css
- markdown
- json
- xml
- sql
- rust
- go
- cpp
- c++ (alias for cpp)
- c
- php
- ruby
- swift
- kotlin

### LlamaIndex 支持的语言

- python
- javascript
- typescript
- java
- c
- cpp
- rust
- go
- ruby
- php
- swift
- kotlin

## 输出格式

无论使用哪种切分策略，返回的结果格式都是一致的：

```json
[
    {"content": "def foo():\n    pass", "metadata": {"source": "utils.py", "chunk_index": 0}},
    {"content": "class Bar:\n    pass", "metadata": {"source": "utils.py", "chunk_index": 1}}
]
```

## 依赖

- Python 3.7+
- langchain-text-splitters (使用 LangChain 策略时)
- llama-index (使用 LlamaIndex 策略时)
- tree-sitter (使用 LlamaIndex 策略时，用于 AST 解析)

## 安装依赖

```bash
# 安装 LangChain 依赖
pip install langchain-text-splitters

# 安装 LlamaIndex 依赖
pip install llama-index

# 安装 tree-sitter 语言包（根据需要）
pip install tree-sitter-python tree-sitter-javascript # 示例
```

## 注意事项

- 使用 LlamaIndex 策略时，需要安装对应的 tree-sitter 语言包
- 对于复杂的代码，不同的切分策略可能会产生不同的切分结果
- 切分参数的选择会影响切分质量，建议根据具体场景调整

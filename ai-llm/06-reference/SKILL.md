---
skill_name: dify-reference
version: 1.0.0
parent_skill: dify-master
description: Dify 参考资料 - DSL语法、API文档、SDK参考、CLI命令
category: reference
tags:
  - dify
  - reference
  - api
  - sdk
  - cli
  - dsl
dependencies: []
last_updated: 2026-03-05
triggers:
  - 语法
  - api
  - sdk
  - cli
  - 命令
  - 参数
  - 配置
  - reference
  - dsl
  - yaml
  - python
  - 命令行
---

# Dify 参考资料 SKILL

> 查找语法、API、CLI 等参考信息

## 快速导航

- [DSL 语法参考](#dsl-语法参考)
- [API 参考](#api-参考)
- [SDK 参考](#sdk-参考)
- [CLI 参考](#cli-参考)
- [常见问题](#常见问题)

---

## DSL 语法参考

### 工作流 DSL 结构

```yaml
version: 0.0.1
graph:
  nodes:
    - id: node_id
      data:
        type: node_type
        # 节点配置
  edges:
    - source: source_node_id
      target: target_node_id
```

### 节点类型

| 类型 | 说明 | 必需字段 |
|------|------|----------|
| `start` | 开始节点 | variables |
| `llm` | LLM 节点 | model, prompt_template |
| `agent` | Agent 节点 | agent_parameters |
| `knowledge-retrieval` | 知识检索 | dataset_ids, query_variable_selector |
| `http-request` | HTTP 请求 | url, method, headers |
| `code` | 代码执行 | code_type, code |
| `tool` | 工具节点 | provider_type, tool_name |
| `if-else` | 条件分支 | conditions |
| `iteration` | 迭代 | iterator_variable_name |
| `loop` | 循环 | max_loop_count |
| `answer` | 响应节点 | answer |

### 变量引用

```yaml
# 系统变量
{{#sys.query#}}           # 用户查询
{{#sys.files#}}           # 上传的文件
{{#sys.conversation_id#}} # 会话 ID

# 节点输出
{{#node_id.output_field#}}

# 数组访问
{{#items[0]#}}           # 数组第一个元素
{{#items[-1]#}}          # 数组最后一个元素

# 对象属性
{{#object.field#}}       # 对象属性
```

### 完整示例

```yaml
workflow:
  graph:
    nodes:
      - id: start
        data:
          type: start
          variables:
            - name: query
              type: text
              required: true

      - id: classify
        data:
          type: question-classifier
          instruction: "分类用户问题"
          categories:
            - name: technical
              description: 技术问题
            - name: general
              description: 一般问题

      - id: llm
        data:
          type: llm
          model:
            provider: openai
            name: gpt-4
          prompt_template:
            - role: system
              text: "你是一个助手"
            - role: user
              text: "{{#start.query#}}"
          context:
            enabled: false

      - id: answer
        data:
          type: answer
          answer: "{{#llm.text#}}"

    edges:
      - source: start
        target: classify
      - source: classify
        target: llm
        source_handle: general
      - source: llm
        target: answer
```

---

## API 参考

### 认证

所有 API 请求需要在 Header 中携带 API Key：

```
Authorization: Bearer YOUR_API_KEY
```

### 端点概览

#### 应用 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/v1/chat-messages` | POST | 发送聊天消息 |
| `/v1/completions` | POST | 文本补全 |
| `/v1/parameters` | GET | 获取应用参数 |
| `/v1/file-upload` | POST | 文件上传 |

#### 工作流 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/v1/workflows/run` | POST | 运行工作流 |
| `/v1/workflows/run` | GET | 获取运行状态 |
| `/v1/workflows/tasks` | GET | 获取任务列表 |

#### 数据集 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/v1/datasets` | GET | 列出数据集 |
| `/v1/datasets` | POST | 创建数据集 |
| `/v1/datasets/{id}/documents` | GET | 列出文档 |
| `/v1/datasets/{id}/retrieve` | POST | 检索知识 |

### 请求/响应格式

#### 聊天消息请求

```json
{
  "query": "用户查询",
  "user": "user_123",
  "conversation_id": "可选的会话ID",
  "response_mode": "blocking | streaming",
  "files": [
    {
      "type": "image",
      "transfer_method": "remote_url",
      "url": "https://example.com/image.jpg"
    }
  ],
  "retrieval_model": {
    "query": "{{#sys.query#}}",
    "top_k": 3
  }
}
```

#### 聊天消息响应

```json
{
  "message_id": "msg_xxx",
  "conversation_id": "conv_xxx",
  "answer": "AI 回复内容",
  "metadata": {
    "usage": {
      "prompt_tokens": 100,
      "completion_tokens": 50,
      "total_tokens": 150
    },
    "retrieval_resources": [
      {
        "position": 1,
        "document_id": "doc_xxx",
        "content": "相关文档内容..."
      }
    ]
  }
}
```

### 错误响应

```json
{
  "code": "invalid_api_key",
  "message": "Invalid API key",
  "status_code": 401
}
```

常见错误码：

| 错误码 | HTTP 状态码 | 说明 |
|--------|-------------|------|
| `invalid_api_key` | 401 | API Key 无效 |
| `invalid_parameter` | 400 | 参数错误 |
| `quota_exceeded` | 403 | 配额超出 |
| `rate_limit_exceeded` | 429 | 速率限制 |
| `internal_server_error` | 500 | 服务器错误 |

---

## SDK 参考

### Python SDK

#### 安装

```bash
pip install dify-client
```

#### 基本用法

```python
from dify_client import DifyClient

# 初始化客户端
client = DifyClient(
    api_key="app-xxx",
    base_url="https://api.dify.ai/v1"
)

# 发送聊天消息
response = client.chat.messages.create(
    query="你好",
    user="user_123"
)
print(response.answer)
```

#### 流式响应

```python
from dify_client import DifyClient

client = DifyClient(api_key="app-xxx")

# 流式聊天
for event in client.chat.messages.stream(
    query="讲个故事",
    user="user_123"
):
    if event.event == "message":
        print(event.data.answer, end="")
```

#### 工作流执行

```python
# 运行工作流
response = client.workflows.run(
    inputs={"query": "测试"},
    user="user_123",
    response_mode="blocking"
)
print(response.data.output)
```

### SDK 类参考

#### DifyClient

```python
class DifyClient:
    def __init__(self, api_key: str, base_url: str = "https://api.dify.ai/v1"):
        """初始化客户端"""
        pass

    @property
    def chat(self) -> ChatClient:
        """聊天客户端"""
        pass

    @property
    def workflows(self) -> WorkflowClient:
        """工作流客户端"""
        pass

    @property
    def datasets(self) -> DatasetClient:
        """数据集客户端"""
        pass
```

#### ChatClient

```python
class ChatClient:
    def create(self, query: str, user: str, **kwargs) -> ChatMessage:
        """发送聊天消息（阻塞）"""
        pass

    def stream(self, query: str, user: str, **kwargs) -> Iterator[ChatEvent]:
        """发送聊天消息（流式）"""
        pass
```

---

## CLI 参考

### 安装

```bash
pip install dify-cli
```

### 命令概览

#### 插件命令

```bash
# 初始化插件
dify plugin init [options]

# 运行插件
dify plugin run [options]

# 打包插件
dify plugin package [options]

# 发布插件
dify plugin publish [options]

# 列出已安装插件
dify plugin list
```

#### 工作流命令

```bash
# 导出工作流
dify workflow export <workflow_id> [options]

# 导入工作流
dify workflow import <file> [options]

# 验证工作流
dify workflow validate <file>

# 运行工作流
dify workflow run <workflow_id> --inputs '{}'
```

#### 应用命令

```bash
# 列出应用
dify app list

# 获取应用信息
dify app info <app_id>

# 部署应用
dify app deploy <app_id>
```

#### 环境变量命令

```bash
# 列出环境变量
dify env list

# 设置环境变量
dify env set <key> <value>

# 获取环境变量
dify env get <key>

# 删除环境变量
dify env delete <key>
```

### 选项说明

| 选项 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--api-key` | -k | API Key | 环境变量 DIFY_API_KEY |
| `--base-url` | -b | 基础 URL | https://api.dify.ai/v1 |
| `--output` | -o | 输出格式 | json |
| `--quiet` | -q | 静默模式 | false |
| `--debug` | -d | 调试模式 | false |

### 使用示例

```bash
# 设置 API Key
export DIFY_API_KEY="app-xxx"

# 初始化插件项目
dify plugin init my-plugin --template tool

# 运行插件
dify plugin run --port 5000

# 导出工作流
dify workflow export wf_xxx -o workflow.yaml

# 导入工作流
dify workflow import workflow.yaml
```

---

## 常见问题

### API 相关

**Q: 如何获取 API Key?**
A: 在 Dify 控制台 -> 设置 -> API 中创建。

**Q: 请求频率限制是多少?**
A: 默认 60 请求/分钟，可申请提升。

**Q: 如何处理流式响应?**
A: 使用 `response_mode=streaming`，解析 SSE 事件。

### 工作流相关

**Q: 如何引用变量?**
A: 使用 `{{#node_id.field#}}` 语法。

**Q: 支持哪些节点类型?**
A: 详见节点类型表格。

**Q: 如何处理循环?**
A: 使用 `iteration` 或 `loop` 节点。

### 插件相关

**Q: 如何开发自定义插件?**
A: 参考 02-plugin SKILL。

**Q: 插件如何获取凭据?**
A: 使用 `self.runtime_credentials`。

---

## 相关 SKILL

- [01-workflow](../01-workflow/SKILL.md) - 工作流设计
- [02-plugin](../02-plugin/SKILL.md) - 插件开发
- [05-integration](../05-integration/SKILL.md) - 集成扩展

---

## 相关资源

- [Dify 官方文档](https://docs.dify.ai/)
- [Dify API 文档](https://docs.dify.ai/guides/application-publishing/developing-with-apis)
- [Dify GitHub](https://github.com/langgenius/dify)

---

**版本信息**: v1.0.0 | **最后更新**: 2026-03-05

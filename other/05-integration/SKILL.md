---
skill_name: dify-integration
version: 1.0.0
parent_skill: dify-master
description: Dify 集成和扩展技能 - API集成、MCP协议、外部服务集成
category: integration
tags:
  - dify
  - integration
  - api
  - mcp
  - webhook
dependencies: []
last_updated: 2026-03-05
triggers:
  - api
  - rest
  - webhook
  - streaming
  - mcp
  - server
  - client
  - 集成
  - 外部服务
  - database
  - storage
  - 消息队列
---

# Dify 集成和扩展 SKILL

> 与外部系统和服务的集成指南

## 快速导航

- [API 集成](#api-集成)
- [MCP 协议](#mcp-协议)
- [外部服务集成](#外部服务集成)
- [集成案例](#集成案例)
- [故障排查](#故障排查)

---

## API 集成

Dify 提供完整的 REST API，支持应用程序集成和工作流编排。

### 核心 API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/v1/chat-messages` | POST | 发送聊天消息 |
| `/v1/completions` | POST | 发送补全请求 |
| `/v1/workflows/run` | POST | 运行工作流 |
| `/v1/parameters` | GET | 获取应用参数 |
| `/v1/file-upload` | POST | 文件上传 |

### REST API 集成

```python
import requests
import json

class DifyClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def chat_message(self, query: str, user: str, **kwargs):
        """发送聊天消息"""
        payload = {
            "query": query,
            "user": user,
            **kwargs
        }
        response = requests.post(
            f"{self.base_url}/v1/chat-messages",
            headers=self.headers,
            json=payload
        )
        return response.json()

    def run_workflow(self, workflow_id: str, inputs: dict, user: str):
        """运行工作流"""
        payload = {
            "inputs": inputs,
            "user": user,
            "response_mode": "blocking"
        }
        response = requests.post(
            f"{self.base_url}/v1/workflows/run",
            headers=self.headers,
            json=payload
        )
        return response.json()
```

**使用示例**:

```python
# 初始化客户端
client = DifyClient(
    base_url="https://api.dify.ai/v1",
    api_key="app-xxxxx"
)

# 发送聊天消息
result = client.chat_message(
    query="你好",
    user="user123",
    conversation_id=None  # 新会话
)
print(result)
```

### Webhook 集成

Webhook 用于在特定事件发生时接收通知，支持工作流触发和事件回调。

#### 工作流 Webhook 触发

```yaml
# 工作流配置
nodes:
  - id: webhook-trigger
    data:
      type: webhook-trigger
      method: POST
      path: /webhook/my-workflow
      parameters:
        - name: data
          type: string
          required: true
```

#### Webhook 回调处理

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook/callback', methods=['POST'])
def handle_webhook():
    """处理 Dify Webhook 回调"""
    payload = request.json

    # 验证签名
    signature = request.headers.get('X-Dify-Signature')
    if not verify_signature(payload, signature):
        return jsonify({"error": "Invalid signature"}), 401

    # 处理事件
    event_type = payload.get('event')
    if event_type == 'workflow.finished':
        # 工作流完成处理
        result = payload.get('data', {}).get('output', {})
        process_result(result)

    return jsonify({"status": "success"})
```

#### Webhook 事件类型

| 事件 | 说明 | 触发时机 |
|------|------|----------|
| `workflow.started` | 工作流开始 | 工作流启动时 |
| `workflow.finished` | 工作流完成 | 工作流正常完成 |
| `workflow.failed` | 工作流失败 | 工作流执行失败 |
| `node.started` | 节点开始 | 节点开始执行 |
| `node.finished` | 节点完成 | 节点执行完成 |

### 流式响应

支持 Server-Sent Events (SSE) 实现实时流式输出。

```python
import requests
import json

def stream_chat(client: DifyClient, query: str, user: str):
    """流式聊天请求"""
    payload = {
        "query": query,
        "user": user,
        "response_mode": "streaming"
    }

    response = requests.post(
        f"{client.base_url}/v1/chat-messages",
        headers=client.headers,
        json=payload,
        stream=True
    )

    for line in response.iter_lines():
        if line:
            # 解析 SSE 格式
            data = line.decode('utf-8')
            if data.startswith('data: '):
                event = json.loads(data[6:])
                yield event

# 使用示例
for event in stream_chat(client, "讲个故事", "user123"):
    if event.get('event') == 'message':
        print(event.get('data', {}).get('answer'), end='', flush=True)
```

**SSE 事件格式**:

```json
{
  "event": "message",
  "task_id": "abc123",
  "message_id": "msg_xxx",
  "conversation_id": "conv_xxx",
  "answer": "生成的文本内容",
  "created_at": 1234567890
}
```

---

## MCP 协议

Model Context Protocol (MCP) 是用于 AI 助手与外部系统集成的标准化协议。

### MCP Server 实现

Dify 可以作为 MCP Server，提供工具和资源供 AI 调用。

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio

class DifyMCPServer:
    def __init__(self, dify_client: DifyClient):
        self.client = dify_client
        self.server = Server("dify-mcp")

    async def start(self):
        """启动 MCP Server"""
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="dify_chat",
                    description="与 Dify 应用进行对话",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "用户查询"},
                            "user": {"type": "string", "description": "用户标识"}
                        },
                        "required": ["query", "user"]
                    }
                ),
                Tool(
                    name="dify_run_workflow",
                    description="运行 Dify 工作流",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "inputs": {"type": "object", "description": "工作流输入参数"},
                            "user": {"type": "string", "description": "用户标识"}
                        },
                        "required": ["inputs", "user"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            if name == "dify_chat":
                result = self.client.chat_message(
                    query=arguments["query"],
                    user=arguments["user"]
                )
                return [TextContent(type="text", text=json.dumps(result))]
            elif name == "dify_run_workflow":
                result = self.client.run_workflow(
                    workflow_id=arguments.get("workflow_id", ""),
                    inputs=arguments["inputs"],
                    user=arguments["user"]
                )
                return [TextContent(type="text", text=json.dumps(result))]
            else:
                raise ValueError(f"Unknown tool: {name}")

        # 启动服务
        await stdio_server(self.server.run())

# 运行服务器
if __name__ == "__main__":
    client = DifyClient("https://api.dify.ai/v1", "app-xxxxx")
    server = DifyMCPServer(client)
    asyncio.run(server.start())
```

### MCP Client 实现

Dify 可以调用外部 MCP Server 提供的工具。

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

class DifyMCPClient:
    def __init__(self, server_command: str, server_args: list[str]):
        self.server_params = StdioServerParameters(
            command=server_command,
            args=server_args
        )

    async def call_tool(self, tool_name: str, arguments: dict):
        """调用 MCP 工具"""
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                return result

# 使用示例
async def main():
    client = DifyMCPClient(
        server_command="node",
        server_args=["mcp-server.js"]
    )
    result = await client.call_tool("get_weather", {"city": "北京"})
    print(result)

asyncio.run(main())
```

### 双向通信配置

在 Dify 工作流中配置 MCP 节点：

```yaml
nodes:
  - id: mcp-tool
    data:
      type: tool
      provider_type: mcp
      server_config:
        type: stdio
        command: python
        args: ["mcp_server.py"]
      tools:
        - name: search
          description: 搜索工具
          input_schema:
            type: object
            properties:
              query:
                type: string
```

---

## 外部服务集成

### 数据库集成

#### PostgreSQL/MySQL

```python
import psycopg2
from dify_plugin import Tool
from typing import Generator

class DatabaseTool(Tool):
    def _invoke(
        self,
        tool_parameters: dict
    ) -> Generator[ToolInvokeMessage, None, None]:
        # 获取连接参数
        host = self.runtime_credentials.get("host")
        port = self.runtime_credentials.get("port")
        database = self.runtime_credentials.get("database")
        user = self.runtime_credentials.get("user")
        password = self.runtime_credentials.get("password")

        # 建立连接
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )

        try:
            # 执行查询
            query = tool_parameters.get("query")
            cursor = conn.cursor()
            cursor.execute(query)

            # 获取结果
            if query.strip().upper().startswith("SELECT"):
                columns = [desc[0] for desc in cursor.description]
                results = cursor.fetchall()
                yield self.create_json_message({
                    "columns": columns,
                    "data": results
                })
            else:
                conn.commit()
                yield self.create_text_message(f"affected rows: {cursor.rowcount}")
        finally:
            conn.close()
```

#### Redis

```python
import redis
from dify_plugin import Tool

class RedisTool(Tool):
    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        r = redis.Redis(
            host=self.runtime_credentials.get("host"),
            port=self.runtime_credentials.get("port"),
            password=self.runtime_credentials.get("password"),
            db=self.runtime_credentials.get("db", 0)
        )

        operation = tool_parameters.get("operation")
        key = tool_parameters.get("key")

        if operation == "get":
            value = r.get(key)
            yield self.create_text_message(value.decode() if value else "")
        elif operation == "set":
            value = tool_parameters.get("value")
            r.set(key, value)
            yield self.create_text_message("OK")
        elif operation == "delete":
            r.delete(key)
            yield self.create_text_message("deleted")
```

### 存储服务集成

#### S3/MinIO

```python
import boto3
from dify_plugin import Tool

class S3Tool(Tool):
    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        s3 = boto3.client(
            's3',
            endpoint_url=self.runtime_credentials.get("endpoint"),
            aws_access_key_id=self.runtime_credentials.get("access_key"),
            aws_secret_access_key=self.runtime_credentials.get("secret_key")
        )

        operation = tool_parameters.get("operation")
        bucket = tool_parameters.get("bucket")
        key = tool_parameters.get("key")

        if operation == "upload":
            content = tool_parameters.get("content")
            s3.put_object(Bucket=bucket, Key=key, Body=content)
            yield self.create_text_message(f"Uploaded to {bucket}/{key}")
        elif operation == "download":
            response = s3.get_object(Bucket=bucket, Key=key)
            content = response['Body'].read()
            yield self.create_binary_message(content)
        elif operation == "list":
            response = s3.list_objects_v2(Bucket=bucket)
            keys = [obj['Key'] for obj in response.get('Contents', [])]
            yield self.create_json_message({"keys": keys})
```

### 消息队列集成

#### RabbitMQ

```python
import pika
from dify_plugin import Tool

class RabbitMQTool(Tool):
    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        credentials = pika.PlainCredentials(
            self.runtime_credentials.get("username"),
            self.runtime_credentials.get("password")
        )
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.runtime_credentials.get("host"),
                port=self.runtime_credentials.get("port"),
                credentials=credentials
            )
        )
        channel = connection.channel()

        operation = tool_parameters.get("operation")
        queue = tool_parameters.get("queue")

        if operation == "publish":
            message = tool_parameters.get("message")
            channel.queue_declare(queue=queue, durable=True)
            channel.basic_publish(
                exchange='',
                routing_key=queue,
                body=message,
                properties=pika.BasicProperties(delivery_mode=2)
            )
            yield self.create_text_message("Message published")
        elif operation == "consume":
            method, properties, body = channel.basic_get(queue=queue)
            if body:
                yield self.create_text_message(body.decode())
                channel.basic_ack(method.delivery_tag)
            else:
                yield self.create_text_message("No message")

        connection.close()
```

#### Kafka

```python
from kafka import KafkaProducer, KafkaConsumer
from dify_plugin import Tool
import json

class KafkaTool(Tool):
    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        operation = tool_parameters.get("operation")
        topic = tool_parameters.get("topic")

        if operation == "publish":
            message = tool_parameters.get("message")
            producer = KafkaProducer(
                bootstrap_servers=self.runtime_credentials.get("servers"),
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            producer.send(topic, value={"message": message})
            producer.flush()
            producer.close()
            yield self.create_text_message("Message sent")
        elif operation == "consume":
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=self.runtime_credentials.get("servers"),
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='earliest'
            )
            for message in consumer:
                yield self.create_json_message(message.value)
                break  # 只消费一条
```

---

## 集成案例

### 案例 1: 企业内部系统集成

```python
# 企业微信通知集成
class WeChatNotifier:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def notify(self, title: str, content: str):
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "content": f"## {title}\n{content}"
            }
        }
        requests.post(self.webhook_url, json=payload)

# 在工作流中使用
def on_workflow_finished(context):
    notifier = WeChatNotifier(os.environ["WECHAT_WEBHOOK"])
    notifier.notify(
        title="工作流完成",
        content=f"工作流 {context.workflow_id} 已完成"
    )
```

### 案例 2: 数据管道集成

```python
# 数据处理管道
class DataPipeline:
    def __init__(self):
        self.steps = []

    def add_step(self, step):
        self.steps.append(step)
        return self

    def execute(self, data):
        result = data
        for step in self.steps:
            result = step(result)
        return result

# 在 Dify 插件中使用
class DataPipelineTool(Tool):
    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        pipeline = DataPipeline()
        pipeline.add_step(transform1)
        pipeline.add_step(transform2)

        input_data = tool_parameters.get("data")
        result = pipeline.execute(input_data)
        yield self.create_json_message(result)
```

---

## 故障排查

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| API 请求超时 | 网络延迟或服务繁忙 | 增加超时时间，实现重试机制 |
| Webhook 签名验证失败 | 签名算法错误 | 确认使用正确的 HMAC-SHA256 算法 |
| MCP 连接失败 | 服务器未启动 | 检查服务器进程和网络连接 |
| 数据库连接池耗尽 | 并发过高 | 调整连接池大小，使用连接复用 |

### 调试技巧

```python
import logging

# 启用调试日志
logging.basicConfig(level=logging.DEBUG)

# API 调试
response = client.chat_message("test", "user")
print(f"Status: {response.status_code}")
print(f"Headers: {response.headers}")
print(f"Body: {response.text}")
```

---

## 相关 SKILL

- [01-workflow](../01-workflow/SKILL.md) - 工作流设计，了解如何触发工作流
- [02-plugin](../02-plugin/SKILL.md) - 插件开发，学习开发自定义集成插件
- [03-performance](../03-performance/SKILL.md) - 性能优化，优化集成性能
- [04-security](../04-security/SKILL.md) - 安全实践，集成安全注意事项
- [06-reference](../06-reference/SKILL.md) - 参考资料，API/SDK 参考

---

## 相关资源

- [Dify API 文档](https://docs.dify.ai/guides/application-publishing/developing-with-apis)
- [MCP 协议规范](https://modelcontextprotocol.io/)
- [Webhook 配置指南](https://docs.dify.ai/guides/workflow/webhook)

---

**版本信息**: v1.0.0 | **最后更新**: 2026-03-05

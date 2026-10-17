---
name: claude-api
description: 适用于 Python 和 TypeScript 的 Anthropic Claude API 模式。涵盖 Messages API、流式传输、工具使用、视觉、扩展思维、批处理、提示词缓存以及 Claude Agent SDK。在使用 Claude API 或 Anthropic SDK 构建应用时使用。
origin: ECC
---

# Claude API

使用 Anthropic Claude API 和 SDK 构建应用。

## 何时激活

- 构建调用 Claude API 的应用
- 代码导入 `anthropic` (Python) 或 `@anthropic-ai/sdk` (TypeScript)
- 用户询问有关 Claude API 模式、工具使用、流式传输或视觉的问题
- 使用 Claude Agent SDK 实现代理工作流
- 优化 API 成本、令牌使用或延迟

## 模型选择

| 模型 | ID | 最适合 |
|-------|-----|----------|
| Opus 4.1 | `claude-opus-4-1` | 复杂推理、架构、研究 |
| Sonnet 4 | `claude-sonnet-4-0` | 平衡的代码编写，大多数开发任务 |
| Haiku 3.5 | `claude-3-5-haiku-latest` | 快速响应、高吞吐、成本敏感 |

除非任务需要深度推理 (Opus) 或速度/成本优化 (Haiku)，否则默认为 Sonnet 4。对于生产环境，建议使用固定的快照 ID 而非别名。

## Python SDK

### 安装

```bash
pip install anthropic
```

### 基础消息

```python
import anthropic

client = anthropic.Anthropic()  # 从环境变量读取 ANTHROPIC_API_KEY

message = client.messages.create(
    model="claude-sonnet-4-0",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "用 Python 解释 async/await"}
    ]
)
print(message.content[0].text)
```

### 流式传输

```python
with client.messages.stream(
    model="claude-sonnet-4-0",
    max_tokens=1024,
    messages=[{"role": "user", "content": "写一首关于编程的俳句"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### 系统提示词

```python
message = client.messages.create(
    model="claude-sonnet-4-0",
    max_tokens=1024,
    system="你是一位资深的 Python 开发人员。请保持简洁。",
    messages=[{"role": "user", "content": "评审这个函数"}]
)
```

## TypeScript SDK

### 安装

```bash
npm install @anthropic-ai/sdk
```

### 基础消息

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic(); // 从环境变量读取 ANTHROPIC_API_KEY

const message = await client.messages.create({
  model: "claude-sonnet-4-0",
  max_tokens: 1024,
  messages: [
    { role: "user", content: "用 TypeScript 解释 async/await" }
  ],
});
console.log(message.content[0].text);
```

### 流式传输

```typescript
const stream = client.messages.stream({
  model: "claude-sonnet-4-0",
  max_tokens: 1024,
  messages: [{ role: "user", content: "写一首俳句" }],
});

for await (const event of stream) {
  if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
    process.stdout.write(event.delta.text);
  }
}
```

## 工具使用 (Tool Use)

定义工具并让 Claude 调用它们：

```python
tools = [
    {
        "name": "get_weather",
        "description": "获取某个位置的当前天气",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "城市名称"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["location"]
        }
    }
]

message = client.messages.create(
    model="claude-sonnet-4-0",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "旧金山的天气怎么样？"}]
)

# 处理工具使用响应
for block in message.content:
    if block.type == "tool_use":
        # 使用 block.input 执行工具
        result = get_weather(**block.input)
        # 将结果发送回 API
        follow_up = client.messages.create(
            model="claude-sonnet-4-0",
            max_tokens=1024,
            tools=tools,
            messages=[
                {"role": "user", "content": "旧金山的天气怎么样？"},
                {"role": "assistant", "content": message.content},
                {"role": "user", "content": [
                    {"type": "tool_result", "tool_use_id": block.id, "content": str(result)}
                ]}
            ]
        )
```

## 视觉 (Vision)

发送图像进行分析：

```python
import base64

with open("diagram.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-4-0",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image_data}},
            {"type": "text", "text": "描述这张图表"}
        ]
    }]
)
```

## 扩展思维 (Extended Thinking)

适用于复杂的推理任务：

```python
message = client.messages.create(
    model="claude-sonnet-4-0",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000
    },
    messages=[{"role": "user", "content": "分步解决这个数学问题..."}]
)

for block in message.content:
    if block.type == "thinking":
        print(f"思考过程：{block.thinking}")
    elif block.type == "text":
        print(f"答案：{block.text}")
```

## 提示词缓存 (Prompt Caching)

缓存大型系统提示词或上下文以降低成本：

```python
message = client.messages.create(
    model="claude-sonnet-4-0",
    max_tokens=1024,
    system=[
        {"type": "text", "text": large_system_prompt, "cache_control": {"type": "ephemeral"}}
    ],
    messages=[{"role": "user", "content": "关于已缓存上下文的问题"}]
)
# 检查缓存使用情况
print(f"缓存读取：{message.usage.cache_read_input_tokens}")
print(f"缓存创建：{message.usage.cache_creation_input_tokens}")
```

## 批处理 API (Batches API)

异步处理大量请求，成本降低 50%：

```python
import time

batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": f"request-{i}",
            "params": {
                "model": "claude-sonnet-4-0",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": prompt}]
            }
        }
        for i, prompt in enumerate(prompts)
    ]
)

# 轮询完成状态
while True:
    status = client.messages.batches.retrieve(batch.id)
    if status.processing_status == "ended":
        break
    time.sleep(30)

# 获取结果
for result in client.messages.batches.results(batch.id):
    print(result.result.message.content[0].text)
```

## Claude Agent SDK

构建多步代理：

```python
# 注意：Agent SDK API 可能会有变动 —— 请查阅官方文档
import anthropic

# 将工具定义为函数
tools = [{
    "name": "search_codebase",
    "description": "在代码库中搜索相关代码",
    "input_schema": {
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"]
    }
}]

# 运行带有工具使用的代理循环
client = anthropic.Anthropic()
messages = [{"role": "user", "content": "评审 auth 模块是否存在安全问题"}]

while True:
    response = client.messages.create(
        model="claude-sonnet-4-0",
        max_tokens=4096,
        tools=tools,
        messages=messages,
    )
    if response.stop_reason == "end_turn":
        break
    # 处理工具调用并继续循环
    messages.append({"role": "assistant", "content": response.content})
    # ... 执行工具并追加 tool_result 消息
```

## 成本优化

| 策略 | 节省 | 何时使用 |
|----------|---------|-------------|
| 提示词缓存 | 已缓存令牌最高节省 90% | 重复的系统提示词或上下文 |
| 批处理 API | 50% | 非实时的大批量处理 |
| 用 Haiku 代替 Sonnet | 约 75% | 简单任务、分类、提取 |
| 更短的 max_tokens | 视情况而定 | 确定输出很短时 |
| 流式传输 | 无（成本相同） | 为了更好的用户体验 |

## 错误处理

```python
import time

from anthropic import APIError, RateLimitError, APIConnectionError

try:
    message = client.messages.create(...)
except RateLimitError:
    # 退避并重试
    time.sleep(60)
except APIConnectionError:
    # 网络问题，带退避地重试
    pass
except APIError as e:
    print(f"API 错误 {e.status_code}: {e.message}")
```

## 环境设置

```bash
# 必填
export ANTHROPIC_API_KEY="您的-api-key"

# 可选：设置默认模型
export ANTHROPIC_MODEL="claude-sonnet-4-0"
```

切勿将 API 密钥硬编码在代码中。请始终使用环境变量。

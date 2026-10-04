---
name: xiaoyao-search
description: 小遥搜索 MCP 工具 - 本地文件智能搜索（语义/全文/图像/语音/混合搜索）
metadata:
  tags: mcp, search, local-files, semantic-search, vector-search, ai-tools
  version: 1.0.0
  author: xiaoyao-search
---

## When to use

当需要搜索本地文件时使用此 Skill：

- 通过自然语言描述搜索本地文档
- 查找包含特定关键词的文件
- 用图片搜索相似的本地图片
- 用语音转文字后搜索文件
- 需要综合语义和全文搜索结果

## Capability

小遥搜索 MCP 服务器提供以下 5 个搜索工具：

### 1. semantic_search（语义搜索）
- **用途**：基于 BGE-M3 向量模型的语义搜索
- **适用**：自然语言查询，如"关于机器学习的文档"
- **参数**：
  - `query`: string - 搜索关键词（1-500字符）
  - `limit`: int - 返回结果数（1-100，默认20）
  - `threshold`: float - 相似度阈值（0.0-1.0，默认0.5）
  - `file_types`: string[] - 文件类型过滤（可选）

### 2. fulltext_search（全文搜索）
- **用途**：基于 Whoosh 的精确关键词匹配
- **适用**：查找特定术语、代码片段
- **参数**：
  - `query`: string - 搜索关键词（1-500字符）
  - `limit`: int - 返回结果数（1-100，默认20）
  - `file_types`: string[] - 文件类型过滤（可选）

### 3. hybrid_search（混合搜索）
- **用途**：结合语义和全文搜索，RRF 算法融合结果
- **适用**：需要全面搜索结果的场景
- **参数**：
  - `query`: string - 搜索关键词（1-500字符）
  - `limit`: int - 返回结果数（1-100，默认20）
  - `threshold`: float - 相似度阈值（0.0-1.0，默认0.5）
  - `file_types`: string[] - 文件类型过滤（可选）

### 4. image_search（图像搜索）
- **用途**：基于 CN-CLIP 的图像相似度搜索
- **适用**：用图片查找相似的本地文件
- **参数**：
  - `image_path`: string - 图片绝对路径
  - `limit`: int - 返回结果数（1-100，默认20）
  - `threshold`: float - 相似度阈值（0.0-1.0，默认0.5）

### 5. voice_search（语音搜索）
- **用途**：FasterWhisper 语音识别后搜索
- **适用**：通过语音快速搜索本地文件
- **参数**：
  - `audio_path`: string - 音频绝对路径
  - `search_type`: string - 搜索类型（semantic/fulltext/hybrid，默认semantic）
  - `limit`: int - 返回结果数（1-100，默认20）
  - `threshold`: float - 相似度阈值（0.0-1.0，默认0.5）

## Usage

### 前提条件

1. 小遥搜索后端服务已启动（默认 http://127.0.0.1:8000）
2. MCP 功能已启用（默认启用）
3. 索引已构建完成

### 调用方式

Claude Code 通过 MCP 协议自动发现和调用工具：

```
用户：帮我找一下关于 Python 异步编程的文档
→ Claude Code 调用 semantic_search(query="Python 异步编程")
→ 返回搜索结果
→ Claude 基于结果回答用户
```

### 响应格式

搜索结果返回 JSON 格式：
```json
{
  "total": 10,
  "search_time": 0.523,
  "results": [
    {
      "file_name": "async_guide.md",
      "file_path": "D:/docs/async_guide.md",
      "file_type": "markdown",
      "relevance_score": 0.95,
      "preview_text": "Python异步编程指南..."
    }
  ]
}
```

## Examples

### 示例1：语义搜索
```
用户：查找关于机器学习算法优化的文档

调用：semantic_search(
  query="机器学习算法优化",
  limit=10,
  threshold=0.5
)
```

### 示例2：全文搜索
```
用户：查找包含 async def 的 Python 文件

调用：fulltext_search(
  query="async def",
  limit=20,
  file_types=["python"]
)
```

### 示例3：图像搜索
```
用户：找一下跟这张图片相似的设计稿

调用：image_search(
  image_path="C:/Users/test/reference.png",
  limit=10
)
```

### 示例4：语音搜索
```
用户：（语音输入）帮我找一下上周的会议记录

调用：voice_search(
  audio_path="C:/Users/test/voice.mp3",
  search_type="semantic"
)
```

### 示例5：混合搜索
```
用户：全面搜索关于 Vue3 组件开发的资料

调用：hybrid_search(
  query="Vue3 组件开发",
  limit=20,
  threshold=0.6
)
```

## Configuration

### 环境变量

| 变量名 | 默认值 | 说明 |
|-------|--------|------|
| MCP_SSE_ENABLED | true | 启用 MCP SSE |
| MCP_SERVER_NAME | xiaoyao-search | 服务器名称 |
| MCP_DEFAULT_LIMIT | 20 | 默认结果数 |
| MCP_DEFAULT_THRESHOLD | 0.5 | 默认相似度阈值 |
| MCP_VOICE_ENABLED | true | 启用语音搜索 |

### 连接测试

```bash
# 测试 MCP SSE 端点
curl http://127.0.0.1:8000/mcp

# 检查后端健康状态
curl http://127.0.0.1:8000/api/system/health
```

## Troubleshooting

### 问题1：工具调用失败
- 检查后端服务是否启动
- 确认 MCP_SSE_ENABLED=true
- 查看 /mcp 端点是否可访问

### 问题2：搜索结果为空
- 确认索引已构建
- 检查查询词是否正确
- 降低 threshold 值尝试

### 问题3：图像/语音搜索失败
- 确认文件路径为绝对路径
- 检查文件格式是否支持
- 检查文件大小是否在限制内（10MB）
